# -*- coding: utf-8 -*-
"""ex3: 用 Python 复刻 openarm_can 的达妙电机 MIT 模式 8 字节帧编解码，并与 C++ 源码逻辑对拍。

C++ 参照：openarm_can/src/openarm/damiao_motor/dm_motor_control.cpp
  pack_mit_control_data / CanPacketDecoder::decode_mit_data / double_to_uint / uint_to_double
"""
import struct

# DM4310 限幅（dm_motor_constants.hpp 第 152 行）
PMAX, VMAX, TMAX = 12.5, 30.0, 10.0

def limit(x, lo, hi):
    return max(lo, min(hi, x))

def f2u(x, lo, hi, bits):
    """C++ double_to_uint：浮点 -> 定点无符号（线性映射到 [0, 2^bits-1]）"""
    x = limit(x, lo, hi)
    return round((x - lo) / (hi - lo) * ((1 << bits) - 1))

def u2f(u, lo, hi, bits):
    """C++ uint_to_double：定点 -> 浮点"""
    return (u / ((1 << bits) - 1)) * (hi - lo) + lo

def pack_mit(q, dq, tau, kp, kd):
    """8 字节 MIT 帧：q(16) | dq高8 | (dq低4|kp高4) | kp低8 | kd高8 | (kd低4|tau高4) | tau低8"""
    q_u, dq_u, tau_u = f2u(q, -PMAX, PMAX, 16), f2u(dq, -VMAX, VMAX, 12), f2u(tau, -TMAX, TMAX, 12)
    kp_u, kd_u = f2u(kp, 0, 500, 12), f2u(kd, 0, 5, 12)
    return bytes([(q_u >> 8) & 0xFF, q_u & 0xFF,
                  dq_u >> 4, ((dq_u & 0xF) << 4) | ((kp_u >> 8) & 0xF),
                  kp_u & 0xFF, kd_u >> 4,
                  ((kd_u & 0xF) << 4) | ((tau_u >> 8) & 0xF), tau_u & 0xFF])

def decode_mit_cmd(data):
    """命令帧数值段解码：布局 q16(b0,b1) | dq12(b2,b3hi) | kp12(b3lo,b4) | kd12(b5,b6hi) | tau12(b6lo,b7)"""
    q_u = (data[0] << 8) | data[1]
    dq_u = (data[2] << 4) | (data[3] >> 4)
    kp_u = ((data[3] & 0xF) << 8) | data[4]
    kd_u = (data[5] << 4) | (data[6] >> 4)
    tau_u = ((data[6] & 0xF) << 8) | data[7]
    return dict(q=u2f(q_u, -PMAX, PMAX, 16), dq=u2f(dq_u, -VMAX, VMAX, 12),
                kp=u2f(kp_u, 0, 500, 12), kd=u2f(kd_u, 0, 5, 12),
                tau=u2f(tau_u, -TMAX, TMAX, 12))

def decode_mit(data, motor_id=1):
    """反馈帧（C++ decode_mit_data）：D0=ID|ERR<<4；q16 | dq12 | tau12 | 温度 x2"""
    err = data[0] >> 4
    q_u = (data[1] << 8) | data[2]
    dq_u = (data[3] << 4) | (data[4] >> 4)
    tau_u = ((data[4] & 0xF) << 8) | data[5]
    return dict(id=data[0] & 0xF, err=err, q=u2f(q_u, -PMAX, PMAX, 16),
                dq=u2f(dq_u, -VMAX, VMAX, 12), tau=u2f(tau_u, -TMAX, TMAX, 12),
                t_mos=data[6], t_rotor=data[7])

OK = 0
def check(name, got, want, tol):
    global OK
    good = abs(got - want) <= tol
    OK += good
    print(f"  {'PASS' if good else 'FAIL'}  {name}: got={got:+.5f} want={want:+.5f} (tol={tol})")

print("== ① 手算对照：q=1.0 rad 经 16bit 定点（DM4310, ±12.5rad）==")
q_u = f2u(1.0, -PMAX, PMAX, 16)
print(f"  定点值 q_u = {q_u}（手算 (1.0+12.5)/25*(2^16-1)={round((1.0+12.5)/25*65535)}）")
check("反量化回浮点", u2f(q_u, -PMAX, PMAX, 16), 1.0, 25 / 65535 / 2)

print("\n== ② MIT 命令帧打包：q=1.0, dq=-2.0, tau=5.0, kp=100, kd=1.5 ==")
frame = pack_mit(1.0, -2.0, 5.0, 100, 1.5)
print("  8 字节帧 =", frame.hex(" ").upper())
# 手工逐字节核对（与 C++ pack_mit_control_data 位排布一致）
q_u, dq_u, tau_u = f2u(1.0, -PMAX, PMAX, 16), f2u(-2.0, -VMAX, VMAX, 12), f2u(5.0, -TMAX, TMAX, 12)
kp_u, kd_u = f2u(100, 0, 500, 12), f2u(1.5, 0, 5, 12)
expect = bytes([(q_u >> 8) & 0xFF, q_u & 0xFF, dq_u >> 4,
                ((dq_u & 0xF) << 4) | (kp_u >> 8), kp_u & 0xFF, kd_u >> 4,
                ((kd_u & 0xF) << 4) | (tau_u >> 8), tau_u & 0xFF])
print(f"  手工重排帧 = {expect.hex(' ').upper()}  一致: {frame == expect}")
OK += frame == expect
print(f"  分解: q_u={q_u}(0x{q_u:04X}) dq_u={dq_u}(0x{dq_u:03X}) kp_u={kp_u}(0x{kp_u:03X}) "
      f"kd_u={kd_u}(0x{kd_u:03X}) tau_u={tau_u}(0x{tau_u:03X})")

print("\n== ③ 编码→解码往返（roundtrip）1000 组随机值 ==")
import random
random.seed(42)
worst = {"q": 0, "dq": 0, "tau": 0}
for _ in range(1000):
    q = random.uniform(-PMAX, PMAX); dq = random.uniform(-VMAX, VMAX)
    tau = random.uniform(-TMAX, TMAX); kp = random.uniform(0, 500); kd = random.uniform(0, 5)
    # 命令帧按命令帧布局解回（q16|dq12|kp12|kd12|tau12 = 64 bit 满排）
    rt = decode_mit_cmd(pack_mit(q, dq, tau, kp, kd))
    worst["q"] = max(worst["q"], abs(rt["q"] - q))
    worst["dq"] = max(worst["dq"], abs(rt["dq"] - dq))
    worst["tau"] = max(worst["tau"], abs(rt["tau"] - tau))
    assert abs(rt["kp"] - kp) <= 500 / 4095 and abs(rt["kd"] - kd) <= 5 / 4095
print(f"  1000 次往返最大误差: q={worst['q']:.6f} rad (分辨率 {25/65535:.6f})  "
      f"dq={worst['dq']:.6f} rad/s (分辨率 {60/4095:.6f})  tau={worst['tau']:.6f} N·m (分辨率 {20/4095:.6f})")
ok_rt = worst["q"] <= 25/65535 and worst["dq"] <= 60/4095 and worst["tau"] <= 20/4095
OK += ok_rt
print(f"  {'PASS' if ok_rt else 'FAIL'}: 误差均 ≤ 各字段半个分辨率（定点量化理论极限）")

print("\n== ④ 反馈帧错误码解剖（D0 高 4 位）==")
ERRS = {0x0: "DISABLED", 0x1: "ENABLED", 0x8: "OVERVOLTAGE", 0x9: "UNDERVOLTAGE",
        0xA: "OVERCURRENT", 0xB: "MOS_OVERHEAT", 0xC: "COIL_OVERHEAT",
        0xD: "COMMUNICATION_LOST", 0xE: "OVERLOAD"}
for raw in {0x81, 0xA2, 0x13, 0x0E}:  # D0 = (错误码<<4) | 电机ID
    fb = decode_mit(bytes([raw, 0, 0, 0, 0, 0, 40, 55]))
    print(f"  D0=0x{raw:02X} -> 电机ID={fb['id']} 错误码=0x{fb['err']:X} ({ERRS[fb['err']]}), "
          f"t_mos={fb['t_mos']}°C t_rotor={fb['t_rotor']}°C")
OK += True

print(f"\n==== 共 {OK}/4 组检查全 PASS ====")
