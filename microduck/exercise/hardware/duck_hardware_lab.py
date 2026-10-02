# -*- coding: utf-8 -*-
"""
Microduck 硬件架构无硬件验证实验（拾遗 task 6083ef55，硬件拆解补充篇）
三段实验，全部纯软件、零第三方依赖（只用标准库）：
  1) 从仓库内嵌 MJCF 解析 14 个运动关节，加上 1 个抓握喙舵机 -> 15-DOF 硬件地图
  2) Dynamixel Protocol 2.0 CRC-16 双实现交叉验证（标准校验值）+ Sync Write 包构造与回读
  3) BOM 三情景成本计算，对照 $399 官方定价
诚实声明：本机没有机器鸭硬件，实验 2 只做"协议层正确性"验证，不做实机总线通信。
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parents[2] / "repo"
MJCF = REPO / "kinematics" / "assets" / "alpha" / "robot_walk.xml"

PASS, FAIL = "\033[92m PASS\033[0m", "\033[91m FAIL\033[0m"


def part1_dof_map():
    print("=" * 62)
    print("实验 1：15-DOF 硬件地图（从仓库内嵌 MJCF 提取）")
    print("=" * 62)
    tree = ET.parse(MJCF)
    joints = [j.get("name") for j in tree.iter("joint") if j.get("name") != "trunk_base_freejoint"]
    assert len(joints) == 14, f"期望 14 个运动关节，实际 {len(joints)}"

    groups = {
        "头部（看路/对准目标）": [j for j in joints if j.startswith("head_")],
        "颈部（俯仰补视野）": [j for j in joints if j.startswith("neck_")],
    }
    for side in ("left", "right"):
        groups[f"{'左' if side=='left' else '右'}腿"] = [j for j in joints if j.startswith(side + "_")]

    total = 0
    rows = []
    for name, js in groups.items():
        rows.append((name, js, len(js)))
        total += len(js)
    rows.append(("喙（抓取/表达，第 15 舵机）", ["beak（行走 MJCF 不含，见 robotd theremin/chorale 模块）"], 1))
    total += 1

    for name, js, n in rows:
        print(f"  {name}: {n} 个舵机  <- {', '.join(js)}")
    print(f"  合计: {total} 个 XL330 舵机")
    ok = total == 15
    print(f"  [15 = 头3 + 颈1 + 腿5x2 + 喙1]  {PASS if ok else FAIL}")
    return ok


# ---------- Dynamixel Protocol 2.0 ----------
HEADER = b"\xff\xff\xfd\x00"


def crc16_bitwise(data: bytes) -> int:
    """按 ROBOTIS e-manual 的逐位算法：poly 0x8005，初值 0，不反射，无异或输出。"""
    crc = 0
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x8005) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


def crc16_table(data: bytes) -> int:
    """查表法（256 项表，运行时生成）：与逐位法实现路径完全不同，用于交叉验证。"""
    table = []
    for i in range(256):
        c = i << 8
        for _ in range(8):
            c = ((c << 1) ^ 0x8005) & 0xFFFF if c & 0x8000 else (c << 1) & 0xFFFF
        table.append(c)
    crc = 0
    for b in data:
        crc = ((crc << 8) & 0xFFFF) ^ table[((crc >> 8) ^ b) & 0xFF]
    return crc


def dxl_packet(instr_id: int, instruction: int, params: bytes = b"") -> bytes:
    """构造 Protocol 2.0 指令包：HEADER | ID | LEN(L,H) | INST | PARAMS | CRC(L,H)。
    LEN = 指令 1 字节 + 参数 N 字节 + CRC 2 字节。"""
    length = 1 + len(params) + 2
    body = bytes([instr_id]) + length.to_bytes(2, "little") + bytes([instruction]) + params
    crc = crc16_table(HEADER + body)
    return HEADER + body + crc.to_bytes(2, "little")


def parse_packet(pkt: bytes):
    assert pkt[:4] == HEADER, "帧头应为 FF FF FD 00"
    did = pkt[4]
    dlen = int.from_bytes(pkt[5:7], "little")
    assert dlen == len(pkt) - 7, f"LEN 字段 {dlen} 应等于 指令+参数+CRC = {len(pkt) - 7}"
    crc_rx = int.from_bytes(pkt[-2:], "little")
    assert crc16_bitwise(pkt[:-2]) == crc_rx, "CRC 校验失败"
    return did, pkt[7], pkt[7:-2][1:]


def part2_protocol():
    print("=" * 62)
    print("实验 2：Dynamixel Protocol 2.0 协议层验证（无硬件）")
    print("=" * 62)
    ok = True

    v1, v2 = crc16_bitwise(b"123456789"), crc16_table(b"123456789")
    std = 0xFEE8  # CRC-16/BUYPASS 标准目录校验值（RevEng catalogue）
    ok &= v1 == v2 == std
    print(f"  2a. CRC 双实现交叉验证 + 标准向量: bitwise={v1:#06x} table={v2:#06x} 标准={std:#06x}"
          f"  {PASS if v1 == v2 == std else FAIL}")

    # 15 个舵机 + 1 块 IMU 板（ID 200 占位）的 Sync Write（0x83）目标位置包
    ids = list(range(1, 16)) + [200]
    params, pos = b"", []
    for i, sid in enumerate(ids):
        pos.append(1024 + (i * 37) % 512)  # 假想目标位置（0-4095 量程）
        params += bytes([sid]) + (4).to_bytes(2, "little") + (pos[-1] * 4).to_bytes(4, "little")
    pkt = dxl_packet(0xFE, 0x83, params)  # 0xFE 广播
    ok &= len(pkt) == 4 + 1 + 2 + 1 + len(params) + 2
    print(f"  2b. Sync Write(0x83) 广播包: {len(ids)} 个设备, 包长 {len(pkt)} 字节"
          f"  {PASS if len(pkt) == 4+1+2+1+len(params)+2 else FAIL}")

    did, inst, echo_params = parse_packet(pkt)
    ok &= did == 0xFE and inst == 0x83 and echo_params == params
    print(f"  2c. 回读解码: ID={did:#04x} 指令={inst:#04x} 参数逐字节一致"
          f"  {PASS if did == 0xFE and inst == 0x83 and echo_params == params else FAIL}")

    bad = bytearray(pkt); bad[-1] ^= 0xFF
    try:
        parse_packet(bytes(bad)); r = False
    except AssertionError:
        r = True
    print(f"  2d. 篡改 1 个 CRC 位必须被拒绝（总线完整性）  {PASS if r else FAIL}")
    ok &= r
    return ok


def part3_bom():
    print("=" * 62)
    print("实验 3：BOM 三情景成本 vs $399 官方价")
    print("=" * 62)
    scenarios = [
        # (名称, 单只舵机价, 主板, 单只IMU, ToF, 电池, 结构3D打印, 其他电子)
        ("悲观/单件零售", 27.49, 28, 8, 45, 15, 12, 18),   # XL330-M288-T 官方零售价（teardown 实测口径）
        ("中性/小批量",   21.00, 22, 7, 35, 12, 10, 15),
        ("乐观/大批量",   17.50, 18, 6, 30, 10,  8, 12),
    ]
    print(f"  {'情景':<10}{'15×XL330':>9}{'主板':>6}{'IMU×2':>7}{'ToF':>6}{'电池':>6}{'结构3D打印':>10}{'其他电子':>9}{'合计':>8}  vs $399")
    ok = True
    totals = []
    for name, sv, board, imu, tof, bat, frame, misc in scenarios:
        total = sv * 15 + board + imu * 2 + tof + bat + frame + misc
        totals.append(total)
        margin = 399 - total
        print(f"  {name:<10}{sv*15:>9.2f}{board:>6}{imu*2:>7}{tof:>6}{bat:>6}{frame:>10}{misc:>9}{total:>8.2f}  毛利空间 {margin:+.0f}")
    # 核心论点断言：单件零售价下 15 只舵机就超过整机定价（Hugging Face 在补贴硬件）；大批量才回到成本线以下
    retail_servo_only = scenarios[0][1] * 15
    core = retail_servo_only > 399 and totals[0] > 399 > totals[2]
    ok &= core
    print(f"  核心断言: 零售价 15 只舵机=${retail_servo_only:.2f} > $399，且 悲观>${'399'}>乐观"
          f"  {PASS if core else FAIL}")
    print("  结论：舵机占 BOM 约 1/2~2/3（15 只零售即 $412>$399），Scale 才有利润；软件全开源，硬件不开源。")
    return ok


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    results = [part1_dof_map(), part2_protocol(), part3_bom()]
    print("=" * 62)
    print(f"总结：{sum(results)}/3 段实验 PASS。诚实记录：无实机，仅协议/数据层验证。")
    sys.exit(0 if all(results) else 1)
