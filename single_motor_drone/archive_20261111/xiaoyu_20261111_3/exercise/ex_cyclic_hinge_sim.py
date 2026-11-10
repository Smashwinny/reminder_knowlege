#!/usr/bin/env python3
"""Numerical experiments for Joshua Bird's single-motor hinged-propeller drone.

All numbers labelled "author-reported" come from the YouTube video
description / indexed narration, the GitHub README, or the X posts.
Model parameters that were NOT measured on the real vehicle are labelled
"assumed".  Do not treat assumed-model outputs as flight-test data.

Steps:
  1. Geometry, tip Mach, once-per-rev timing vs firmware latency
  2. Lag-pitch kinematics of a skewed hinge (why 45 degrees)
  3. Time-domain lag oscillator + blade-element mean side force
  4. 160 Hz vibration vs rotor harmonics, blade-stiffness scaling
  5. MCOUT packet CRC / framing round-trip (from published protocol)
  6. Area comparison with PULSAR and "300 times/s" consistency

Usage:
  python3 ex_cyclic_hinge_sim.py --outdir ./out
"""
from __future__ import annotations

import argparse
import json
import math
import os
import struct
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path


G = 9.80665
RHO = 1.225  # kg/m^3, ISA sea-level, assumed
A_SOUND = 343.0  # m/s, 20 C dry air, assumed
INCH = 0.0254


# ---------------------------------------------------------------------------
# Step 5 helpers: MCOUT CRC and a minimal framer (from jyjblrd/moteus
# fw/mcout_protocol.h at SHA 704a0dd9f30a3704e8915a82c1631301fdbff9bd)
# ---------------------------------------------------------------------------

def crc16_xmodem(data: bytes, crc: int = 0) -> int:
    """XMODEM CRC-16, poly 0x1021, init 0. Bit-compatible with ArduPilot crc_xmodem."""
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


MCOUT_MAGIC = 0xC04D
MCOUT_VERSION = 1
MCOUT_LENGTH = 84
MCOUT_MSG_ID = 1
MCOUT_FLAG_MOTORS_ARMED = 1 << 0
MCOUT_FLAG_SOFT_ARMED = 1 << 1
MCOUT_FLAG_INTERLOCK = 1 << 2
MCOUT_FLAG_ESTOP = 1 << 3
MCOUT_FLAG_OUTPUT_ENABLED = 1 << 6


def pack_mcout(
    sequence: int,
    timestamp_usec: int,
    flags: int,
    spool_state: int,
    desired_spool: int,
    roll: float,
    pitch: float,
    yaw: float,
    throttle: float,
) -> bytes:
    """Pack an 84-byte little-endian MCOUT ControlOutputPacket, CRC last."""
    body = struct.pack(
        "<HBBHIQ HBB" + "f" * 15,
        MCOUT_MAGIC,
        MCOUT_VERSION,
        MCOUT_LENGTH,
        MCOUT_MSG_ID,
        sequence & 0xFFFFFFFF,
        timestamp_usec & 0xFFFFFFFFFFFFFFFF,
        flags & 0xFFFF,
        spool_state & 0xFF,
        desired_spool & 0xFF,
        roll, pitch, yaw, throttle,
        0.0, 0.0, 0.0,  # feedback
        0.0, 0.0, 0.0,  # feedforward
        throttle, throttle,  # filtered / out
        0.0, 0.0,  # forward / lateral
        0.0025,  # dt, 400 Hz
    )
    assert len(body) == 82, len(body)
    crc = crc16_xmodem(body)
    return body + struct.pack("<H", crc)


def parse_mcout(pkt: bytes) -> dict:
    if len(pkt) != 84:
        raise ValueError(f"bad length {len(pkt)}")
    magic, ver, length, mid, seq, ts, flags, spool, despool = struct.unpack_from(
        "<HBBHIQ HBB", pkt, 0
    )
    floats = struct.unpack_from("<15f", pkt, 22)
    crc_wire = struct.unpack_from("<H", pkt, 82)[0]
    crc_calc = crc16_xmodem(pkt[:82])
    required = (
        MCOUT_FLAG_MOTORS_ARMED
        | MCOUT_FLAG_SOFT_ARMED
        | MCOUT_FLAG_INTERLOCK
        | MCOUT_FLAG_OUTPUT_ENABLED
    )
    output_allowed = (flags & required) == required and (flags & MCOUT_FLAG_ESTOP) == 0
    return {
        "magic": magic,
        "version": ver,
        "length": length,
        "message_id": mid,
        "sequence": seq,
        "timestamp_usec": ts,
        "flags": flags,
        "spool_state": spool,
        "desired_spool": despool,
        "roll": floats[0],
        "pitch": floats[1],
        "yaw": floats[2],
        "throttle": floats[3],
        "crc_wire": crc_wire,
        "crc_calc": crc_calc,
        "crc_ok": crc_wire == crc_calc,
        "header_ok": magic == MCOUT_MAGIC and ver == MCOUT_VERSION
        and length == MCOUT_LENGTH and mid == MCOUT_MSG_ID,
        "output_allowed": output_allowed,
    }


# ---------------------------------------------------------------------------
# Steps 1-4, 6 physics
# ---------------------------------------------------------------------------

def lag_to_pitch(zeta_rad: float, alpha_deg: float) -> float:
    """Pitch angle from lag for a skewed lag-pitch hinge in the (e_r, e_z) plane.

    Rotation about hinge axis ê_h = cos(α) ê_z + sin(α) ê_r decomposes into
    lag ζ = β cos(α) and pitch θ = β sin(α), hence θ = ζ tan(α).
    At α = 45°, tan(α) = 1, so pitch equals lag.  This is a kinematic
    identity, not a flight measurement.
    """
    return zeta_rad * math.tan(math.radians(alpha_deg))


def tip_speed(rpm: float, diameter_m: float) -> float:
    return (rpm / 60.0) * math.pi * diameter_m


@dataclass
class LagOscillator:
    """Relative lag of a blade in the hub frame.

    I ζ̈ + C ζ̇ + K ζ = -I ω̇_hub

    I, C, K are ASSUMED (order-of-magnitude for a small 3D-printed blade
    with centrifugal / counterweight restoring).  They are not identified
    from Bird's vehicle.
    """
    inertia: float  # kg m^2, assumed
    damping: float  # N m s / rad, assumed
    stiffness: float  # N m / rad, assumed (centrifugal + counterweight + hinge)

    def freq_response(self, omega: float, alpha_hub: float) -> complex:
        """ζ / (hub angular acceleration) * alpha_hub, phasor at frequency omega.

        Forcing is -I * alpha_hub (alpha_hub is the complex amplitude of ω̇).
        """
        denom = -self.inertia * omega ** 2 + 1j * self.damping * omega + self.stiffness
        return (-self.inertia * alpha_hub) / denom

    def natural_hz(self) -> float:
        return math.sqrt(self.stiffness / self.inertia) / (2 * math.pi)


def blade_element_side_force(
    rpm: float,
    radius: float,
    chord: float,
    cl_alpha: float,
    theta0_rad: float,
    zeta_amp: float,
    zeta_phase: float,
    alpha_hinge_deg: float,
    n_psi: int = 720,
    n_r: int = 24,
    root_cutout: float = 0.2,
) -> dict:
    """Mean side force from two opposite-sense lag-pitch blades.

    Blade 0: θ = θ0 + tan(α) ζ,  Blade 1: θ = θ0 - tan(α) ζ,
    ζ(ψ) = ζ_amp cos(ψ - zeta_phase).  Inflow and stall are ignored
    (ASSUMED linear cl = cl_alpha * θ).  Forces are in the hub frame.
    """
    omega = rpm * 2 * math.pi / 60.0
    coupling = math.tan(math.radians(alpha_hinge_deg))
    rs = [root_cutout * radius + (1 - root_cutout) * radius * (i + 0.5) / n_r for i in range(n_r)]
    dr = (1 - root_cutout) * radius / n_r
    fx = fy = fz = 0.0
    # also run a no-cyclic baseline inside the same loop structure
    fx0 = fy0 = 0.0
    for k in range(n_psi):
        psi = 2 * math.pi * k / n_psi
        zeta = zeta_amp * math.cos(psi - zeta_phase)
        thetas = (theta0_rad + coupling * zeta, theta0_rad - coupling * zeta)
        # blade azimuths  ψ  and  ψ+π
        azis = (psi, psi + math.pi)
        for theta, azi in zip(thetas, azis):
            dL_sum = 0.0
            for r in rs:
                u = omega * r
                cl = cl_alpha * theta
                dL = 0.5 * RHO * u * u * chord * cl * dr
                dL_sum += dL
            # lift along shaft; in-plane force neglected (small angle)
            # A cyclic dL difference produces a lateral force in the disk plane
            # via the tilted blade lift?  For a first-order cyclic-pitch model
            # the *moment* is more direct; the mean in-plane force from
            # vertical lift components is zero, but a tilted tip-path / cyclic
            # lift distribution is equivalent to a tilting of the thrust vector.
            # We accumulate the lift-weighted disk tilt:
            fx += dL_sum * math.cos(azi)  # "forward" if psi=0 is +x
            fy += dL_sum * math.sin(azi)
            fz += dL_sum
        # baseline: zeta=0
        for theta0, azi in ((theta0_rad, psi), (theta0_rad, psi + math.pi)):
            dL_sum = 0.0
            for r in rs:
                u = omega * r
                dL_sum += 0.5 * RHO * u * u * chord * cl_alpha * theta0 * dr
            fx0 += dL_sum * math.cos(azi)
            fy0 += dL_sum * math.sin(azi)
    inv = 1.0 / n_psi
    return {
        "Fx_N": fx * inv,
        "Fy_N": fy * inv,
        "Fz_N": fz * inv,
        "Fx_baseline_N": fx0 * inv,
        "Fy_baseline_N": fy0 * inv,
        "tilt_angle_deg": math.degrees(math.atan2(math.hypot(fx, fy), max(fz, 1e-12))),
    }


def cantilever_flap_hz(E: float, I: float, mass: float, length: float) -> float:
    """First-mode frequency of a cantilever beam, f = (1.875)^2 / (2π) * sqrt(EI / (μ L^4)).

    ASSUMED uniform beam, clamped at the root.  Real hinged blades are not
    ideal cantilevers; this is only used to show how frequency scales with
    stiffness.
    """
    mu = mass / length  # linear density
    lam = 1.875104
    return (lam ** 2) / (2 * math.pi) * math.sqrt(E * I / (mu * length ** 4))


def svg_line_chart(xs, series, width=640, height=240, xlabel="", ylabel="", title="", colors=None):
    colors = colors or ["#1769ff", "#ff7900", "#00b7d5", "#d4286a"]
    pad_l, pad_r, pad_t, pad_b = 58, 16, 28, 40
    w, h = width - pad_l - pad_r, height - pad_t - pad_b
    xmin, xmax = min(xs), max(xs)
    ymin = min(min(s) for _, s in series)
    ymax = max(max(s) for _, s in series)
    if ymin == ymax:
        ymax = ymin + 1.0
    # pad y
    yr = ymax - ymin
    ymin -= 0.08 * yr
    ymax += 0.08 * yr

    def xx(x):
        return pad_l + (x - xmin) / (xmax - xmin) * w

    def yy(y):
        return pad_t + (ymax - y) / (ymax - ymin) * h

    def ticks(a, b, n=5):
        return [a + (b - a) * i / (n - 1) for i in range(n)]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" font-family="sans-serif">',
        f'<rect width="{width}" height="{height}" fill="#f7fcff"/>',
        f'<text x="{width/2}" y="18" text-anchor="middle" font-size="13" fill="#0866ca" font-weight="700">{title}</text>',
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+h}" stroke="#9bb8c9"/>',
        f'<line x1="{pad_l}" y1="{pad_t+h}" x2="{pad_l+w}" y2="{pad_t+h}" stroke="#9bb8c9"/>',
    ]
    for y in ticks(ymin, ymax):
        parts.append(
            f'<line x1="{pad_l}" y1="{yy(y):.1f}" x2="{pad_l+w}" y2="{yy(y):.1f}" stroke="#e3eef4"/>'
        )
        parts.append(
            f'<text x="{pad_l-6}" y="{yy(y)+4:.1f}" text-anchor="end" font-size="10" fill="#577288">{y:.3g}</text>'
        )
    for x in ticks(xmin, xmax):
        parts.append(
            f'<text x="{xx(x):.1f}" y="{pad_t+h+16}" text-anchor="middle" font-size="10" fill="#577288">{x:.3g}</text>'
        )
    parts.append(
        f'<text x="{width/2}" y="{height-6}" text-anchor="middle" font-size="11" fill="#17324d">{xlabel}</text>'
    )
    parts.append(
        f'<text x="14" y="{pad_t+h/2}" text-anchor="middle" font-size="11" fill="#17324d" '
        f'transform="rotate(-90 14 {pad_t+h/2})">{ylabel}</text>'
    )
    legend_x = pad_l + 8
    for i, (name, ys) in enumerate(series):
        c = colors[i % len(colors)]
        pts = " ".join(f"{xx(x):.2f},{yy(y):.2f}" for x, y in zip(xs, ys))
        parts.append(f'<polyline fill="none" stroke="{c}" stroke-width="2.4" points="{pts}"/>')
        parts.append(f'<rect x="{legend_x}" y="{pad_t+4}" width="10" height="10" fill="{c}"/>')
        parts.append(f'<text x="{legend_x+14}" y="{pad_t+13}" font-size="11" fill="#17324d">{name}</text>')
        legend_x += 8 * max(len(name), 6) + 28
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default="./out")
    args = ap.parse_args()
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    started = time.time()
    report = {"steps": {}, "meta": {}}

    # ------------------------------------------------------------------
    # Step 1
    # ------------------------------------------------------------------
    D_in = 6.0  # author-reported
    D = D_in * INCH
    R = D / 2
    rpm_author = 20000.0  # author-reported: "almost 20,000 RPM"
    acc_per_s_author = 300.0  # author-reported: "more than 300 times per second"
    omega = rpm_author * 2 * math.pi / 60.0
    f_rev = rpm_author / 60.0
    T_rev_ms = 1000.0 / f_rev
    v_tip = tip_speed(rpm_author, D)
    mach = v_tip / A_SOUND
    v_tip_mph = v_tip * 2.236936292
    v_tip_kmh = v_tip * 3.6

    # latency → degrees
    latencies_ms = [0.033, 0.2, 0.167, 2.0, 3.0]  # 1/30 kHz, claimed 0.2, 20deg-equivalent, mis-heard 2ms, 1 rev
    deg_per_s = rpm_author * 360.0 / 60.0
    latency_table = []
    for ms in latencies_ms:
        deg = deg_per_s * (ms / 1000.0)
        latency_table.append({
            "latency_ms": ms,
            "rotation_deg_at_20k_rpm": deg,
            "fraction_of_rev": deg / 360.0,
        })
    # exact latency that equals 20 degrees
    ms_for_20deg = 20.0 / deg_per_s * 1000.0

    # ESC failure threshold 50 acc/s (author-reported)
    esc_limit_hz = 50.0
    rpm_if_once_per_rev_at_esc_limit = esc_limit_hz * 60.0

    step1 = {
        "diameter_in_author": D_in,
        "diameter_m": D,
        "radius_m": R,
        "rpm_author_almost": rpm_author,
        "rev_frequency_Hz": f_rev,
        "period_ms": T_rev_ms,
        "omega_rad_s": omega,
        "tip_speed_m_s": v_tip,
        "tip_speed_mph": v_tip_mph,
        "tip_speed_kmh": v_tip_kmh,
        "mach_at_343mps_assumed": mach,
        "author_phrase_half_speed_of_sound": "tips approaching half the speed of sound",
        "acc_dec_per_s_author": acc_per_s_author,
        "acc_per_rev_if_20k_rpm": acc_per_s_author / f_rev,
        "rpm_if_exactly_300_once_per_rev": acc_per_s_author * 60.0,
        "deg_per_second": deg_per_s,
        "latency_ms_for_exactly_20_deg": ms_for_20deg,
        "latency_table": latency_table,
        "esc_loses_sync_above_Hz_author": esc_limit_hz,
        "rpm_at_which_1_per_rev_equals_esc_limit": rpm_if_once_per_rev_at_esc_limit,
        "moteus_control_rate_kHz_author_spec": [15, 30],
        "updates_per_rev_at_15kHz": 15000.0 / f_rev,
        "updates_per_rev_at_30kHz": 30000.0 / f_rev,
        "mcout_publish_Hz_firmware": 400,
        "mcout_updates_per_rev_at_20k": 400.0 / f_rev,
        "note": (
            "2 ms at 20,000 RPM is 240°, not 20°. 20° corresponds to 0.1667 ms. "
            "Toms Hardware and a YouTube comment both say sub-0.2 ms; 0.2 ms is 24°. "
            "Auto-transcript '2 milliseconds is 20°' is internally inconsistent."
        ),
    }
    report["steps"]["1_geometry_timing"] = step1

    # ------------------------------------------------------------------
    # Step 2 kinematics
    # ------------------------------------------------------------------
    alphas = list(range(15, 76, 5))
    zeta_sample_deg = 8.0  # assumed example lag
    pitches = [math.degrees(lag_to_pitch(math.radians(zeta_sample_deg), a)) for a in alphas]
    couplings = [math.tan(math.radians(a)) for a in alphas]
    step2 = {
        "formula": "theta = zeta * tan(alpha)",
        "sample_lag_deg_assumed": zeta_sample_deg,
        "alpha_deg": alphas,
        "coupling_tan_alpha": couplings,
        "pitch_deg_at_sample_lag": pitches,
        "at_45_deg_coupling": math.tan(math.radians(45)),
        "why_45": "tan(45°)=1, so a lag of N degrees becomes a pitch of N degrees. Opposite hinge sense on the two blades yields pure cyclic pitch.",
        "at_30_coupling": math.tan(math.radians(30)),
        "at_60_coupling": math.tan(math.radians(60)),
    }
    report["steps"]["2_kinematics"] = step2
    (out / "step2_kinematics.svg").write_text(
        svg_line_chart(
            alphas,
            [
                ("耦合比 tan(α)", couplings),
                (f"滞后 {zeta_sample_deg:g}° 时的变距 (°)", pitches),
            ],
            xlabel="铰链倾角 α (度)",
            ylabel="耦合比 / 变距角",
            title="斜置滞后-变距铰链的运动学（θ = ζ tan α）",
        ),
        encoding="utf-8",
    )

    # ------------------------------------------------------------------
    # Step 3 dynamics + side force
    # ------------------------------------------------------------------
    # Assumed blade inertia: treat each blade as 4 g at 4 cm radius of gyration
    m_blade = 0.004  # kg, ASSUMED
    k_gyr = 0.040  # m, ASSUMED
    I_blade = m_blade * k_gyr ** 2
    # Restoring: counterweights + centrifugal.  Pick K so the 1/rev lag is
    # a few degrees under a modest once-per-rev acceleration.
    # Natural frequency a bit above 1/rev would be "stiff"; below would be
    # inertia-dominated.  We sweep K later; default: wn = 1.4 * Ω
    wn_ratio = 1.4  # ASSUMED
    K = I_blade * (wn_ratio * omega) ** 2
    # Light damping, zeta_damp = 0.25 (ASSUMED)
    zeta_damp = 0.25
    C = 2 * zeta_damp * math.sqrt(K * I_blade)
    osc = LagOscillator(I_blade, C, K)

    # Speed variation: ω(t) = Ω + δΩ sin(Ω t),  ω̇ = δΩ Ω cos(Ω t)
    # Pick δΩ so peak-to-peak speed change is 4% of Ω (ASSUMED command size)
    d_frac = 0.04
    d_omega = d_frac * omega
    alpha_amp = d_omega * omega  # amplitude of ω̇
    zeta_phasor = osc.freq_response(omega, alpha_amp)
    zeta_amp = abs(zeta_phasor)
    zeta_phase = math.atan2(zeta_phasor.imag, zeta_phasor.real)  # phase of ζ relative to ω̇ (cos)

    theta0 = math.radians(12.0)  # ASSUMED collective
    chord = 0.018  # m, ASSUMED ~18 mm mean chord
    cl_alpha = 5.73  # 1/rad ≈ 2π, ASSUMED thin-airfoil, unstalled
    forces = blade_element_side_force(
        rpm_author, R, chord, cl_alpha, theta0, zeta_amp, zeta_phase, 45.0
    )
    forces_no = blade_element_side_force(
        rpm_author, R, chord, cl_alpha, theta0, 0.0, 0.0, 45.0
    )

    # Sweep cyclic amplitude (speed variation fraction)
    fracs = [i / 100.0 for i in range(0, 11)]
    side, tilt, pitch_amp = [], [], []
    for fr in fracs:
        a_amp = (fr * omega) * omega
        zp = osc.freq_response(omega, a_amp)
        f = blade_element_side_force(
            rpm_author, R, chord, cl_alpha, theta0, abs(zp),
            math.atan2(zp.imag, zp.real), 45.0,
        )
        side.append(math.hypot(f["Fx_N"], f["Fy_N"]))
        tilt.append(f["tilt_angle_deg"])
        pitch_amp.append(math.degrees(abs(zp)))  # θ_amp = ζ_amp at 45°

    # Time series for one revolution (for the log / a plot)
    n = 720
    tseries = []
    for k in range(n):
        psi = 2 * math.pi * k / n
        wdot = alpha_amp * math.cos(psi)
        zeta = zeta_amp * math.cos(psi - zeta_phase)
        theta_a = lag_to_pitch(zeta, 45)
        theta_b = -theta_a
        tseries.append({
            "psi_deg": math.degrees(psi),
            "hub_accel_rad_s2": wdot,
            "lag_deg": math.degrees(zeta),
            "pitch_bladeA_deg": math.degrees(theta_a),
            "pitch_bladeB_deg": math.degrees(theta_b),
        })

    step3 = {
        "assumed": {
            "blade_mass_kg": m_blade,
            "radius_of_gyration_m": k_gyr,
            "inertia_kgm2": I_blade,
            "wn_over_Omega": wn_ratio,
            "damping_ratio": zeta_damp,
            "stiffness_Nm_per_rad": K,
            "damping_Nms_per_rad": C,
            "collective_deg": 12.0,
            "mean_chord_m": chord,
            "cl_alpha_per_rad": cl_alpha,
            "speed_variation_fraction": d_frac,
        },
        "natural_freq_Hz": osc.natural_hz(),
        "once_per_rev_Hz": f_rev,
        "zeta_amp_deg": math.degrees(zeta_amp),
        "theta_amp_deg_at_45": math.degrees(zeta_amp),  # tan45=1
        "zeta_phase_rel_accel_deg": math.degrees(zeta_phase),
        "hub_accel_amp_rad_s2": alpha_amp,
        "forces_with_cyclic": forces,
        "forces_without_cyclic": forces_no,
        "side_force_N": math.hypot(forces["Fx_N"], forces["Fy_N"]),
        "baseline_side_force_N": math.hypot(forces_no["Fx_N"], forces_no["Fy_N"]),
        "thrust_N": forces["Fz_N"],
        "tilt_deg": forces["tilt_angle_deg"],
        "sweep_speed_frac": fracs,
        "sweep_side_force_N": side,
        "sweep_tilt_deg": tilt,
        "sweep_pitch_amp_deg": pitch_amp,
        "note": (
            "Side force and tilt are from an assumed linear blade-element model "
            "with no inflow or stall. They demonstrate the mechanism (cyclic pitch "
            "→ mean lateral force) and must not be quoted as Bird's measured thrust vector."
        ),
    }
    report["steps"]["3_dynamics_side_force"] = step3
    (out / "step3_timeseries.csv").write_text(
        "psi_deg,hub_accel_rad_s2,lag_deg,pitch_bladeA_deg,pitch_bladeB_deg\n"
        + "\n".join(
            f"{r['psi_deg']:.4f},{r['hub_accel_rad_s2']:.6f},{r['lag_deg']:.6f},"
            f"{r['pitch_bladeA_deg']:.6f},{r['pitch_bladeB_deg']:.6f}"
            for r in tseries
        )
        + "\n",
        encoding="utf-8",
    )
    (out / "step3_side_force.svg").write_text(
        svg_line_chart(
            [f * 100 for f in fracs],
            [
                ("平均侧向力 (N)", side),
                ("推力倾斜角 (°)", tilt),
                ("变距振幅 (°)", pitch_amp),
            ],
            xlabel="转速一次谐波幅值 δΩ/Ω (%)（假设）",
            ylabel="力 / 角度",
            title="周期调速幅值增大时，平均侧向力与变距振幅（假设模型）",
        ),
        encoding="utf-8",
    )
    (out / "step3_one_rev.svg").write_text(
        svg_line_chart(
            [r["psi_deg"] for r in tseries],
            [
                ("桨叶A变距 (°)", [r["pitch_bladeA_deg"] for r in tseries]),
                ("桨叶B变距 (°)", [r["pitch_bladeB_deg"] for r in tseries]),
                ("滞后角 (°)", [r["lag_deg"] for r in tseries]),
            ],
            xlabel="方位角 ψ (度)",
            ylabel="角度 (度)",
            title="一转内的滞后与周期变距（α=45°, 假设 4% 一次谐波调速）",
        ),
        encoding="utf-8",
    )

    # ------------------------------------------------------------------
    # Step 4  160 Hz vs harmonics and stiffness
    # ------------------------------------------------------------------
    f160 = 160.0  # author-reported vibration that swamped the IMU
    # half-rev at 20k would be 166.67 Hz — close
    f_half = f_rev / 2.0
    rpm_where_1per_rev_is_160 = 160.0 * 60.0
    rpm_where_half_is_160 = 160.0 * 2.0 * 60.0

    # Assumed blade as cantilever for scaling ONLY
    # Choose EI so that a "soft" blade's first flap mode sits near 160 Hz
    length = 0.062  # m, from hinge to tip, ASSUMED (6" radius minus hub)
    # f = k * sqrt(EI / (μ L^4))  →  EI = (f*2π/λ^2)^2 * μ L^4
    lam = 1.875104
    mu = m_blade / length
    def ei_for_freq(f):
        return (f * 2 * math.pi / lam ** 2) ** 2 * mu * length ** 4

    EI_soft = ei_for_freq(160.0)
    stiffness_mults = [0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0]
    flap_freqs = [160.0 * math.sqrt(m) for m in stiffness_mults]

    step4 = {
        "author_vibration_Hz": f160,
        "once_per_rev_at_20k_Hz": f_rev,
        "half_per_rev_at_20k_Hz": f_half,
        "abs_diff_160_vs_half_rev_Hz": abs(f160 - f_half),
        "rpm_if_160_is_1_per_rev": rpm_where_1per_rev_is_160,
        "rpm_if_160_is_half_rev": rpm_where_half_is_160,
        "interpretations": [
            "160 Hz is 6.7 Hz below Ω/2 at 20,000 RPM (166.7 Hz). Close, but the author fixed it by stiffening the blades, which points to a structural/flap mode rather than a locked rotor harmonic.",
            "Early hover RPM may have been lower than 20,000; 9,600 RPM would put 1/rev exactly at 160 Hz.",
            "A flap or body mode near 160 Hz can still be excited by 1/rev or 2/rev content and swamp a flight-controller accelerometer.",
        ],
        "assumed_blade_length_m": length,
        "EI_soft_if_flap_equals_160Hz": EI_soft,
        "stiffness_multipliers": stiffness_mults,
        "flap_freq_Hz": flap_freqs,
        "freq_scales_as": "sqrt(EI)  (and sqrt(E) if geometry is unchanged)",
        "double_EI_new_Hz": 160.0 * math.sqrt(2.0),
        "note": "The cantilever model is only for scaling. Hardware/strobe photos and the flight fix remain 待验证.",
    }
    report["steps"]["4_vibration_160Hz"] = step4
    (out / "step4_stiffness.svg").write_text(
        svg_line_chart(
            stiffness_mults,
            [
                ("一阶挥舞频率 (Hz)", flap_freqs),
                ("160 Hz 参考", [160.0] * len(stiffness_mults)),
                ("20k RPM 的 1/rev = 333 Hz", [f_rev] * len(stiffness_mults)),
            ],
            xlabel="相对软桨的弯曲刚度倍数 EI / EI_soft（假设）",
            ylabel="频率 (Hz)",
            title="更硬桨叶如何把挥舞频率移离 160 Hz（缩放模型）",
        ),
        encoding="utf-8",
    )

    # ------------------------------------------------------------------
    # Step 5 MCOUT protocol
    # ------------------------------------------------------------------
    flags_ok = (
        MCOUT_FLAG_MOTORS_ARMED
        | MCOUT_FLAG_SOFT_ARMED
        | MCOUT_FLAG_INTERLOCK
        | MCOUT_FLAG_OUTPUT_ENABLED
    )
    pkt = pack_mcout(
        sequence=42,
        timestamp_usec=1_000_000,
        flags=flags_ok,
        spool_state=3,
        desired_spool=2,
        roll=0.25,
        pitch=-0.10,
        yaw=0.8,  # yaw is carried on the wire; moteus docs say it is ignored in mixing
        throttle=0.55,
    )
    decoded = parse_mcout(pkt)
    # mutate one payload byte and confirm CRC fails
    bad = bytearray(pkt)
    bad[34] ^= 0x01  # flip a bit in throttle
    decoded_bad = parse_mcout(bytes(bad))
    # disarm: missing INTERLOCK
    pkt_disarm = pack_mcout(
        43, 1_000_100, flags_ok & ~MCOUT_FLAG_INTERLOCK, 3, 2, 0.25, -0.10, 0.8, 0.55
    )
    decoded_disarm = parse_mcout(pkt_disarm)
    # estop
    pkt_estop = pack_mcout(
        44, 1_000_200, flags_ok | MCOUT_FLAG_ESTOP, 3, 2, 0.25, -0.10, 0.8, 0.55
    )
    decoded_estop = parse_mcout(pkt_estop)

    # Docs discrepancy
    step5 = {
        "packet_len": len(pkt),
        "crc_known_vector": {
            "empty": crc16_xmodem(b""),
            "abc": crc16_xmodem(b"abc"),
            # XMODEM CRC-16 of "123456789" is the well-known 0x31C3
            "123456789": crc16_xmodem(b"123456789"),
            "expected_123456789": 0x31C3,
            "abc_ok": crc16_xmodem(b"123456789") == 0x31C3,
        },
        "roundtrip_ok": decoded["crc_ok"] and decoded["header_ok"] and decoded["output_allowed"],
        "decoded": {k: (float(v) if isinstance(v, float) else v) for k, v in decoded.items()},
        "corrupted_crc_ok": decoded_bad["crc_ok"],
        "disarmed_output_allowed": decoded_disarm["output_allowed"],
        "estop_output_allowed": decoded_estop["output_allowed"],
        "docs_protocol_number": {
            "moteus_guide_SERIALx_PROTOCOL": 50,
            "ardupilot_README_SERIALx_PROTOCOL": 51,
            "note": "Pinned SHAs disagree (moteus 704a0dd vs ardupilot 455b266). Treat as a documentation inconsistency to verify on hardware, not as a flight result.",
        },
        "cyclic_isr_formula": "base + amp * sin(2*pi*(harmonic*(angle-zero_angle)+phase)) at PWM rate 15-30 kHz",
        "yaw_in_firmware": "MCOUT packet carries yaw; moteus MCOUT guide states yaw commands are ignored because a single underactuated propeller has no (cyclic) yaw authority.",
    }
    report["steps"]["5_mcout_protocol"] = step5
    assert crc16_xmodem(b"123456789") == 0x31C3, "CRC test vector failed"
    assert decoded["crc_ok"] and decoded["output_allowed"]
    assert not decoded_bad["crc_ok"]
    assert not decoded_disarm["output_allowed"]
    assert not decoded_estop["output_allowed"]
    # float roundtrip
    assert abs(decoded["roll"] - 0.25) < 1e-6
    assert abs(decoded["pitch"] + 0.10) < 1e-6
    assert abs(decoded["throttle"] - 0.55) < 1e-6

    # ------------------------------------------------------------------
    # Step 6 comparisons
    # ------------------------------------------------------------------
    # PULSAR rotor diameter 37.6 cm (HKU / Science Robotics 2023, secondary
    # report of the paper).  Area ratio vs 6 inch.
    D_pulsar = 0.376  # m, from HKU/paper reporting
    area_bird = math.pi * (D / 2) ** 2
    area_pulsar = math.pi * (D_pulsar / 2) ** 2
    area_ratio = area_pulsar / area_bird
    # Paulos 2013: 38.6 cm rotor, ~1 N at 1200 rpm, 30 Nmm moment, 358 g coaxial, TWO motors
    D_paulos = 0.386
    area_paulos = math.pi * (D_paulos / 2) ** 2
    step6 = {
        "pulsar_diameter_m_reported": D_pulsar,
        "pulsar_source": "HKU PULSAR page / Science Robotics 10.1126/scirobotics.ade4538 (2023): 37.6 cm single propeller; the vehicle itself self-rotates (different architecture).",
        "bird_disk_area_m2": area_bird,
        "pulsar_disk_area_m2": area_pulsar,
        "pulsar_over_bird_area": area_ratio,
        "author_claim": "over six times less propeller area than the Pulsar drone",
        "claim_holds_on_37_6cm": area_ratio > 6.0,
        "paulos_2013_diameter_m": D_paulos,
        "paulos_2013_area_m2": area_paulos,
        "paulos_over_bird_area": area_paulos / area_bird,
        "paulos_2013_notes": "IROS 2013: 38.6 cm hinged rotor, ~1 N at 1200 rpm, 30 N·mm control moment, flight vehicle is a 358 g coaxial with TWO motors (hinged top + fixed bottom). Custom motor controller + 12-bit magnetic encoder (1/4096 rev). They also used a xenon-strobe camera — the same diagnostic idea Bird later rebuilt.",
        "tom_stanton": "Author notes Tom Stanton's swashplateless helicopter still needs two motors.",
        "architectural_distinctions": [
            "Paulos 2013: two motors (coaxial), large slow rotor, lab MAV.",
            "PULSAR 2023: one motor, but the whole airframe self-rotates; 37.6 cm rotor.",
            "Bird 2026: one motor, finned TPU body that is *meant* not to spin with the prop (it still slowly rotates; yaw/heading via reaction torque + fins + IR beacon). 6 inch, ~20,000 RPM.",
        ],
    }
    report["steps"]["6_comparisons"] = step6

    report["meta"] = {
        "script": "ex_cyclic_hinge_sim.py",
        "python": sys.version.split()[0],
        "elapsed_s": time.time() - started,
        "cwd": os.getcwd(),
        "outdir": str(out.resolve()),
        "status": {
            "numerical_experiments": "真实完成",
            "hardware_print_hover_strobe": "待验证",
            "youtube_full_asr_captions": "受阻 (timedtext empty / yt-dlp HTTP 429)",
        },
    }

    (out / "results.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    # Human-readable log fragment
    def fnum(x, n=4):
        return f"{x:.{n}g}" if isinstance(x, float) else x

    lines = []
    lines.append("# Experiment results (machine-written)\n")
    lines.append(f"- Python {sys.version.split()[0]}, elapsed {report['meta']['elapsed_s']:.3f}s\n")
    lines.append("## Step 1 Geometry and timing\n")
    lines.append(
        f"- 6 inch diameter = {D:.4f} m. At 20,000 RPM, 1/rev = {f_rev:.4f} Hz, period = {T_rev_ms:.4f} ms.\n"
    )
    lines.append(
        f"- Tip speed = {v_tip:.2f} m/s = {v_tip_mph:.1f} mph = {v_tip_kmh:.1f} km/h, Mach {mach:.3f} (a=343 m/s assumed).\n"
    )
    lines.append(
        f"- 300 acc/dec per s at 20,000 RPM is {acc_per_s_author/f_rev:.3f} events/rev, not exactly 1. "
        f"Exactly once-per-rev at 300 Hz would be {acc_per_s_author*60:.0f} RPM.\n"
    )
    lines.append(
        f"- 0.2 ms → {deg_per_s*0.0002:.2f}°. 2 ms → {deg_per_s*0.002:.2f}°. Exactly 20° → {ms_for_20deg:.4f} ms.\n"
    )
    lines.append(
        f"- moteus 15–30 kHz ISR: {15000/f_rev:.1f}–{30000/f_rev:.1f} updates/rev. MCOUT 400 Hz: {400/f_rev:.2f} packets/rev.\n"
    )
    lines.append("## Step 2 Kinematics\n")
    lines.append(f"- θ = ζ tan(α). At 45°, coupling = 1. At 30° {math.tan(math.radians(30)):.4f}, at 60° {math.tan(math.radians(60)):.4f}.\n")
    lines.append(f"- An assumed 8° lag becomes {math.degrees(lag_to_pitch(math.radians(8),45)):.2f}° pitch at 45°, "
                 f"{math.degrees(lag_to_pitch(math.radians(8),30)):.2f}° at 30°, "
                 f"{math.degrees(lag_to_pitch(math.radians(8),60)):.2f}° at 60°.\n")
    lines.append("## Step 3 Dynamics (ASSUMED model)\n")
    lines.append(
        f"- I={I_blade:.3e} kg m², wn=1.4 Ω ({osc.natural_hz():.1f} Hz), ζ_damp=0.25, δΩ/Ω=4%.\n"
    )
    lines.append(
        f"- Lag / pitch amplitude = {math.degrees(zeta_amp):.3f}°, phase vs acceleration = {math.degrees(zeta_phase):.1f}°.\n"
    )
    lines.append(
        f"- Mean thrust Fz = {forces['Fz_N']:.3f} N. Side force = {math.hypot(forces['Fx_N'], forces['Fy_N']):.4f} N, "
        f"tilt = {forces['tilt_angle_deg']:.3f}°. Baseline side force (no cyclic) = {math.hypot(forces_no['Fx_N'], forces_no['Fy_N']):.2e} N.\n"
    )
    lines.append("## Step 4 160 Hz\n")
    lines.append(
        f"- Ω = {f_rev:.2f} Hz, Ω/2 = {f_half:.2f} Hz, |160−Ω/2| = {abs(160-f_half):.2f} Hz.\n"
    )
    lines.append(
        f"- Doubling EI moves a 160 Hz flap mode to {160*math.sqrt(2):.1f} Hz (scaling only).\n"
    )
    lines.append("## Step 5 MCOUT protocol\n")
    lines.append(
        f"- CRC test vector '123456789' → 0x{crc16_xmodem(b'123456789'):04X} (expected 0x31C3): "
        f"{'PASS' if crc16_xmodem(b'123456789')==0x31C3 else 'FAIL'}.\n"
    )
    lines.append(
        f"- 84-byte round-trip CRC_ok={decoded['crc_ok']}, output_allowed={decoded['output_allowed']}; "
        f"corrupted CRC_ok={decoded_bad['crc_ok']}; missing INTERLOCK output_allowed={decoded_disarm['output_allowed']}; "
        f"ESTOP output_allowed={decoded_estop['output_allowed']}.\n"
    )
    lines.append(
        "- Docs inconsistency: moteus guide SERIALx_PROTOCOL=50 vs ArduPilot README =51 at pinned SHAs.\n"
    )
    lines.append("## Step 6 Comparisons\n")
    lines.append(
        f"- Disk area 6 inch = {area_bird:.5f} m², PULSAR 37.6 cm = {area_pulsar:.5f} m², ratio = {area_ratio:.3f} "
        f"({'supports' if area_ratio>6 else 'does not support'} the 'over six times less area' claim).\n"
    )
    lines.append(
        f"- Paulos 2013 38.6 cm area ratio vs Bird = {area_paulos/area_bird:.2f}×; that vehicle used two motors.\n"
    )
    (out / "results.md").write_text("".join(lines), encoding="utf-8")
    print("".join(lines))
    print(f"Wrote {out}/results.json and figures.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
