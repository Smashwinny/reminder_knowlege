#!/usr/bin/env python3
"""Teaching lab for private IP, CIDR, DHCP, LPM routing.

This is original instructional code. It does not talk to Tailscale
servers, does not use user keys, and does not change host networking.
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import os
import platform
import socket
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHANGHAI = timezone(timedelta(hours=8))
# RFC 1918 §3
RFC1918 = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
]
# RFC 6598 Shared Address Space / CGNAT
RFC6598 = ipaddress.ip_network("100.64.0.0/10")


def now() -> str:
    return datetime.now(SHANGHAI).strftime("%Y-%m-%d %H:%M:%S %Z")


def classify(ip: str) -> str:
    addr = ipaddress.ip_address(ip)
    if addr in RFC6598:
        return "RFC6598-CGNAT-shared"
    for net in RFC1918:
        if addr in net:
            return f"RFC1918-private:{net}"
    if addr.is_loopback:
        return "loopback"
    if addr.is_link_local:
        return "link-local"
    if addr.is_multicast:
        return "multicast"
    if addr.is_reserved or addr.is_unspecified:
        return "other-special"
    return "public-or-other"


def cmd_out(argv: list[str]) -> str:
    r = subprocess.run(argv, capture_output=True, text=True)
    return (r.stdout or "") + (f"\n[stderr]\n{r.stderr}" if r.stderr else "") + f"\n[exit {r.returncode}]"


def run_env() -> dict:
    ifaces = cmd_out(["ip", "-br", "addr"])
    routes = cmd_out(["ip", "route"])
    routes6 = cmd_out(["ip", "-6", "route"])
    try:
        fwd = Path("/proc/sys/net/ipv4/ip_forward").read_text().strip()
    except Exception as e:
        fwd = f"unreadable: {e}"
    info = {
        "when": now(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "hostname_not_secret": socket.gethostname(),
        "iproute": cmd_out(["ip", "-V"]).strip(),
        "host_ip_forward": fwd,
        "ip_addr": ifaces.strip(),
        "ip_route": routes.strip(),
        "ip_route6": routes6.strip(),
        "note": (
            "This is the cloud box underlay, not the author's home LAN. "
            "172.30.0.0/24 and 172.17.0.0/16 are observed here; both sit in RFC1918 172.16.0.0/12. "
            "host_ip_forward is only read, never written by this lab."
        ),
    }
    print("=== E1 environment ===")
    print(json.dumps({k: info[k] for k in ("when", "python", "platform", "host_ip_forward")}, ensure_ascii=False, indent=2))
    print("--- ip -br addr ---")
    print(ifaces)
    print("--- ip route ---")
    print(routes)
    return info


def run_subnet() -> dict:
    # Examples taken from the original post (author typo 当腰访问 ignored).
    host = ipaddress.ip_interface("192.168.1.20/24")
    cases = [
        ("192.168.1.30", "192.168.1.0/24", True, "same /24, stay local"),
        ("192.168.2.30", "192.168.1.0/24", False, "different /24, go to gateway"),
        ("192.168.1.20", "192.168.1.0/25", True, "/25 lower half includes .20"),
        ("192.168.1.150", "192.168.1.0/25", False, "/25 lower half excludes .150"),
        ("192.168.1.150", "192.168.1.128/25", True, "/25 upper half includes .150"),
        ("192.168.1.20", "192.168.1.128/25", False, "/25 upper half excludes .20"),
        ("100.90.0.1", "192.168.1.0/24", False, "Tailscale example is not on home LAN"),
        ("100.90.0.1", "100.64.0.0/10", True, "example is inside RFC6598/CGNAT range"),
        ("192.168.1.20", "192.168.0.0/16", True, "RFC1918 16-bit block contains this LAN"),
    ]
    rows = []
    for ip, net, expect, why in cases:
        got = ipaddress.ip_address(ip) in ipaddress.ip_network(net)
        rows.append({"ip": ip, "network": net, "member": got, "expected": expect, "ok": got is expect, "why": why})
        assert got is expect, (ip, net, got, expect)

    net24 = ipaddress.ip_network("192.168.1.0/24")
    usable = list(net24.hosts())
    assert str(net24.network_address) == "192.168.1.0"
    assert str(net24.broadcast_address) == "192.168.1.255"
    assert len(list(net24)) == 256
    assert str(usable[0]) == "192.168.1.1" and str(usable[-1]) == "192.168.1.254"
    # gateway occupies one of the usable addresses, as the post said
    remaining_if_gw = len(usable) - 1
    assert remaining_if_gw == 253

    classes = {
        "192.168.1.20": classify("192.168.1.20"),
        "192.168.1.30": classify("192.168.1.30"),
        "192.168.2.30": classify("192.168.2.30"),
        "100.90.0.1": classify("100.90.0.1"),
        "8.8.8.8": classify("8.8.8.8"),
        "172.30.0.2": classify("172.30.0.2"),
        "10.66.0.1": classify("10.66.0.1"),
    }
    assert classes["192.168.1.20"].startswith("RFC1918")
    assert classes["100.90.0.1"] == "RFC6598-CGNAT-shared"
    assert classes["8.8.8.8"] == "public-or-other"

    # Two isolated networks may both number a host 192.168.1.20 (RFC1918 reuse).
    net_home = ipaddress.ip_network("192.168.1.0/24")
    net_other = ipaddress.ip_network("192.168.1.0/24")
    a = ipaddress.ip_address("192.168.1.20")
    reuse_ok = (a in net_home) and (a in net_other)
    # Membership alone cannot tell two physically separate 192.168.1.0/24s apart.

    dhcp = simulate_dhcp()

    out = {
        "host_example": str(host),
        "network": str(host.network),
        "netmask": str(host.netmask),
        "prefix": host.network.prefixlen,
        "address_count": len(list(net24)),
        "usable_first": str(usable[0]),
        "usable_last": str(usable[-1]),
        "usable_count": len(usable),
        "remaining_if_gateway_takes_one": remaining_if_gw,
        "membership": rows,
        "classify": classes,
        "rfc1918_reuse_same_number_is_legal_in_isolated_nets": reuse_ok,
        "dhcp_simulation": dhcp,
    }
    print("=== E2 subnet / RFC class / DHCP sim ===")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return out


def simulate_dhcp() -> dict:
    """State machine only — no packets, no host DHCP client."""
    pool = [ipaddress.ip_address(f"192.168.1.{i}") for i in range(100, 200)]
    reserved = {"phone-mac": ipaddress.ip_address("192.168.1.30")}
    used = {ipaddress.ip_address("192.168.1.1")}  # router / server itself
    options = {
        "mask": "255.255.255.0",
        "router": "192.168.1.1",
        "dns": ["192.168.1.1"],
        "lease_seconds": 3600,
    }

    def alloc(client_id: str, requested=None):
        log = []
        log.append(("client", "DHCPDISCOVER", {"client": client_id}))
        if client_id in reserved:
            offer = reserved[client_id]
        elif requested and requested not in used and requested in pool:
            offer = requested
        else:
            offer = next(ip for ip in pool if ip not in used)
        log.append(("server", "DHCPOFFER", {"yiaddr": str(offer), **options}))
        log.append(("client", "DHCPREQUEST", {"requested": str(offer), "client": client_id}))
        used.add(offer)
        log.append(("server", "DHCPACK", {"yiaddr": str(offer), **options}))
        return {"client": client_id, "assigned": str(offer), "options": options, "trace": log}

    phone = alloc("phone-mac")
    laptop = alloc("laptop-mac")
    # reservation must stick even if the next pool address would have been .100
    assert phone["assigned"] == "192.168.1.30"
    assert laptop["assigned"] == "192.168.1.100"
    return {
        "rfc2131_four_way": ["DHCPDISCOVER", "DHCPOFFER", "DHCPREQUEST", "DHCPACK"],
        "phone_reservation": phone,
        "laptop_dynamic": laptop,
        "note": "Reservation still uses DHCP; the address is just reserved in the pool. Not a static, manually filled host config.",
    }


def lpm(routes: list[dict], dest: str) -> dict:
    """Longest prefix match. Connected routes beat a default if they match."""
    addr = ipaddress.ip_address(dest)
    hits = []
    for r in routes:
        net = ipaddress.ip_network(r["dst"])
        if addr in net:
            hits.append({**r, "prefix": net.prefixlen})
    if not hits:
        return {"dest": dest, "match": None, "reason": "unroutable"}
    best = sorted(hits, key=lambda x: (-x["prefix"], x["dst"]))[0]
    return {"dest": dest, "match": best, "candidates": hits}


def run_route() -> dict:
    # A host like the post: 192.168.1.20/24, default via 192.168.1.1, plus a Tailscale-like overlay route.
    table = [
        {"dst": "192.168.1.0/24", "dev": "wlan0", "via": None, "kind": "connected-lan"},
        {"dst": "100.64.0.0/10", "dev": "tailscale0", "via": None, "kind": "overlay-cgnat"},
        {"dst": "0.0.0.0/0", "dev": "wlan0", "via": "192.168.1.1", "kind": "default-gateway"},
    ]
    dests = [
        "192.168.1.30",
        "192.168.2.30",
        "100.90.0.1",
        "8.8.8.8",
        "192.168.1.150",
        "10.0.0.1",
    ]
    results = [lpm(table, d) for d in dests]
    # Assertions matching the post + official 100.64/10 range
    expect = {
        "192.168.1.30": "connected-lan",
        "192.168.2.30": "default-gateway",
        "100.90.0.1": "overlay-cgnat",
        "8.8.8.8": "default-gateway",
        "192.168.1.150": "connected-lan",  # still in the /24, unlike a /25 split
        "10.0.0.1": "default-gateway",
    }
    for r in results:
        kind = r["match"]["kind"] if r["match"] else None
        assert kind == expect[r["dest"]], (r, expect[r["dest"]])

    # /25 split table: .20 and .150 take different connected routes.
    split = [
        {"dst": "192.168.1.0/25", "dev": "office0", "via": None, "kind": "office"},
        {"dst": "192.168.1.128/25", "dev": "guest0", "via": None, "kind": "guest"},
        {"dst": "0.0.0.0/0", "dev": "office0", "via": "192.168.1.1", "kind": "default-gateway"},
    ]
    s20 = lpm(split, "192.168.1.20")
    s150 = lpm(split, "192.168.1.150")
    assert s20["match"]["kind"] == "office"
    assert s150["match"]["kind"] == "guest"

    # Negative: a /24 would hide the /25 difference if it were also present and preferred? No — /25 wins LPM.
    mixed = split + [{"dst": "192.168.1.0/24", "dev": "wrong0", "via": None, "kind": "too-wide"}]
    m150 = lpm(mixed, "192.168.1.150")
    assert m150["match"]["kind"] == "guest" and m150["match"]["prefix"] == 25

    out = {
        "table": table,
        "lookups": results,
        "split_25": {"table": split, "192.168.1.20": s20, "192.168.1.150": s150},
        "lpm_prefers_25_over_24": m150,
    }
    print("=== E3 longest-prefix match ===")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return out


def run_verify(results: dict) -> dict:
    # Re-run pure functions and compare.
    again_sub = run_subnet()
    again_rt = run_route()
    ok = (
        again_sub["membership"] == results["subnet"]["membership"]
        and again_sub["classify"] == results["subnet"]["classify"]
        and again_rt["lookups"] == results["route"]["lookups"]
    )
    out = {"ok": ok, "when": now()}
    print("=== E6 verify ===")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if not ok:
        raise SystemExit("verify mismatch")
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("step", nargs="?", default="all", choices=["env", "subnet", "route", "verify", "all"])
    args = p.parse_args()
    results_path = HERE / "results.json"
    if args.step == "env":
        data = {"env": run_env()}
    elif args.step == "subnet":
        data = {"subnet": run_subnet()}
    elif args.step == "route":
        data = {"route": run_route()}
    elif args.step == "all":
        data = {"env": run_env(), "subnet": run_subnet(), "route": run_route()}
        data["verify"] = run_verify(data)
        results_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        print("wrote", results_path)
        return
    else:
        prev = json.loads(results_path.read_text()) if results_path.exists() else {}
        data = prev
        data["verify"] = run_verify(prev)
    if results_path.exists() and args.step != "verify":
        prev = json.loads(results_path.read_text())
        prev.update(data)
        data = prev
    if args.step != "verify":
        results_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
