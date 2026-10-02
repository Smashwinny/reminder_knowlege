# -*- coding: utf-8 -*-
"""Microduck 复刻契约对拍实验（来源：X article 2094807636084682752 DIY 复刻教程）

验证复刻教程的核心论断——"真机与训练必须共享同一份契约"：
  1. 15 关节线序 + Dynamixel ID 表（repo/duck-control/src/model.rs）
  2. home pose：训练端(repo_rl/microduck_constants.py HOME_FRAME) vs 运行端(model.rs DEFAULT_POSITION) 数值对拍
  3. 61 维观测向量拼装（repo/duck-control/src/obs.rs 布局注释的 Python 复现）
  4. index-9 陷阱：14 维动作 naive 直拷 vs 正确跳嘴插入 15 槽
  5. XL330 编码器 raw→rad 换算 q = 2*pi*raw/4096 - pi
  6. ONNX 发布契约常量（repo_rl/src/mjlab_microduck/publish/manifest.py）
"""
import math
import re
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1] / "repo"
REPO_RL = Path(__file__).resolve().parents[1] / "repo_rl"
MODEL_RS = REPO / "duck-control" / "src" / "model.rs"
PROTO_RS = REPO / "duck-ipc-proto" / "src" / "lib.rs"
CONSTANTS_PY = REPO_RL / "src" / "mjlab_microduck" / "robot" / "microduck_constants.py"
MANIFEST_PY = REPO_RL / "src" / "mjlab_microduck" / "publish" / "manifest.py"

ok = fail = 0
def check(name, cond, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print(f"  PASS  {name}  {detail}")
    else:
        fail += 1
        print(f"  FAIL  {name}  {detail}")

print("=" * 72)
print("步骤 1  解析运行端源码：15 关节线序(duck-ipc-proto) / ID 表 / MOUTH_INDEX / home pose(model.rs)")
print("=" * 72)
rs = MODEL_RS.read_text(encoding="utf-8")
proto = PROTO_RS.read_text(encoding="utf-8")
joint_names = re.findall(r'"([a-z_]+)"', re.search(r"pub const JOINT_NAMES[^=]*=\s*\[(.*?)\];", proto, re.S).group(1))
ids_txt = re.search(r"pub const JOINT_IDS[^=]*=\s*\[(.*?)\];", rs, re.S).group(1)
joint_ids = [int(x) for x in re.findall(r"\d+", re.sub(r"//.*", "", ids_txt))]
mouth_index = int(re.search(r"pub const MOUTH_INDEX: usize = (\d+);", rs).group(1))
dp_txt = re.search(r"pub const DEFAULT_POSITION[^=]*=\s*\[(.*?)\];", rs, re.S).group(1)
dp_vals = [float(x) for x in re.findall(r"-?\d+\.\d+", re.sub(r"//.*", "", dp_txt))]
check("JOINT_NAMES 长度=15", len(joint_names) == 15, str(len(joint_names)))
check("JOINT_IDS 长度=15", len(joint_ids) == 15, str(joint_ids))
check("MOUTH_INDEX==9（嘴占线序第 9 槽）", mouth_index == 9, f"mouth={joint_names[mouth_index]}")
print(f"  线序: {joint_names}")
print(f"  ID表: {joint_ids}")
check("左腿 ID=20..24", joint_ids[0:5] == [20, 21, 22, 23, 24])
check("颈/头/嘴 ID=30..34", joint_ids[5:10] == [30, 31, 32, 33, 34])
check("右腿 ID=10..14", joint_ids[10:15] == [10, 11, 12, 13, 14])
check("IMU ID=200", "IMU_DXL_ID: u8 = 200" in rs)
check("波特率 1_000_000", "BAUD_RATE: u32 = 1_000_000" in rs)
runtime_home = dict(zip(joint_names, dp_vals))
check("DEFAULT_POSITION 15 个数值", len(dp_vals) == 15)

print()
print("=" * 72)
print("步骤 2  home pose 对拍：训练端 HOME_FRAME（microduck_constants.py）vs 运行端")
print("=" * 72)
py = CONSTANTS_PY.read_text(encoding="utf-8")
hf_txt = re.search(r"HOME_FRAME = EntityCfg\.InitialStateCfg\(\s*joint_pos=\{(.*?)\},\s*joint_vel", py, re.S).group(1)
rl_home = {}
for pat, val in re.findall(r'(r"[^"]+")\s*:\s*(-?\d+\.\d+)', hf_txt):
    rl_home[pat.strip('r"')] = float(val)
check("训练端 home 模式解析后覆盖 14 关节（无嘴）",
      sum(1 for j in joint_names if any(re.search(p, j) for p in rl_home)) == 14,
      str(len(rl_home)))
resolved = {}
print(f"  训练端关节: {sorted(rl_home)}")
mismatch = []
for name, rv in rl_home.items():
    for j in joint_names:
        if re.search(name, j):
            resolved[j] = rv
mismatch = [(j, rv, runtime_home[j]) for j, rv in resolved.items() if abs(runtime_home[j] - rv) > 1e-6]
check("14 关节 home pose 两端逐值一致", not mismatch and len(resolved) == 14, str(mismatch))
print(f"  例: left_hip_pitch 训练={rl_home[r'.*left_hip_pitch.*']} 运行={runtime_home['left_hip_pitch']}")
check("嘴在训练端无 home（策略不驱动）", "mouth" not in " ".join(rl_home))

print()
print("=" * 72)
print("步骤 3  61 维观测向量拼装（obs.rs 布局的 Python 复现）")
print("=" * 72)
Gyro = np.zeros(3); Gravity = np.array([0.0, 0.0, -1.0])
rng = np.random.default_rng(0)
joint_pos = rng.normal(0, 0.05, 15)   # 15 槽线序（含嘴）
joint_vel = rng.normal(0, 1.0, 15)
prev_action = rng.normal(0, 0.1, 14)
cmd = dict(vx=0.3, vy=0.0, vyaw=0.1, head=[0.35, 0.35, 0.0, 0.0],
           body=[0.0, 0.0, 0.02, 0.0, -0.01, 0.0])  # x,y,yaw 恒零（obs.rs 注释第 1 条）
# obs.rs joint_of: slot<9 ? slot : slot+1 —— 14 槽策略序跳过嘴
def joint_of(slot): return slot if slot < mouth_index else slot + 1
policy_pos = np.array([joint_pos[joint_of(s)] - runtime_home[joint_names[joint_of(s)]] for s in range(14)])
policy_vel = np.array([joint_vel[joint_of(s)] for s in range(14)])
obs = np.concatenate([Gyro, Gravity, policy_pos, policy_vel, prev_action,
                      [cmd["vx"], cmd["vy"], cmd["vyaw"], *cmd["head"], *cmd["body"]]])
check("观测维度=61", obs.shape == (61,), str(obs.shape))
widths = [3, 3, 14, 14, 14, 13]
names = ["gyro", "projected_gravity", "joint_pos-home", "joint_vel", "prev_action", "command"]
off = 0
for w, n in zip(widths, names):
    print(f"  [{off:2d}..{off+w:<2d}) {w:2d}  {n}")
    off += w
check("分块宽度 3+3+14+14+14+13=61", sum(widths) == 61)
check("重力单位向量模长=1", abs(np.linalg.norm(obs[3:6]) - 1) < 1e-12)
check("命令块 x/y/yaw 恒零（nominal 编码）", obs[55] == 0 and obs[56] == 0 and obs[60] == 0)
check("body 块顺序 z,roll,pitch（obs.rs 注释警告项）",
      obs[57] == cmd["body"][2] and obs[58] == cmd["body"][3] and obs[59] == cmd["body"][4])

print()
print("=" * 72)
print("步骤 4  index-9 陷阱复现：14 维动作 -> 15 槽目标")
print("=" * 72)
action = np.zeros(14); action[9] = 0.5  # 策略第 9 维 = 右髋 yaw（动作序 [左5|头颈4|右5]）
targets_naive = np.zeros(15)
targets_naive[:14] = action                      # 错误：直拷前 14 槽
targets = np.zeros(15)
for s in range(14):
    targets[joint_of(s)] = action[s]             # 正确：跳过 index 9
check("naive 直拷把右髋 yaw 命令写进嘴", targets_naive[9] == 0.5 and joint_names[9] == "mouth")
print(f"  naive : 嘴槽目标 = {math.degrees(targets_naive[9]):+.1f}°  <- 右髋 yaw 命令误入嘴！")
print(f"  正确  : 嘴槽目标 = {math.degrees(targets[9]):+.1f}°, 右髋 yaw = {math.degrees(targets[10]):+.1f}°")
check("正确映射嘴槽为 0（嘴不在策略内）", targets[9] == 0.0)
check("正确映射右腿整体后移一槽", np.allclose(targets[10:15], action[9:14]))
err = int(np.sum(targets_naive[9:] != targets[9:]))
print(f"  两种映射在 15 槽里有 {err} 个槽不同（嘴+右腿全部）——复刻最不能出错的一行代码")

print()
print("=" * 72)
print("步骤 5  XL330 编码器 raw→rad 换算 q = 2*pi*raw/4096 - pi")
print("=" * 72)
to_rad = lambda raw: 2 * math.pi * raw / 4096 - math.pi
check("raw=2048 -> 0 rad（零位）", abs(to_rad(2048)) < 1e-12)
check("raw=0 -> -pi", abs(to_rad(0) + math.pi) < 1e-12)
_step = 2 * math.pi / 4096
check("raw=4095 -> 距 +pi 一个量化格以内", 0 <= math.pi - to_rad(4095) <= _step + 1e-12,
      f"gap={math.pi - to_rad(4095):.6f} step={_step:.6f}")
print(f"  例: raw=2048 -> {to_rad(2048):+.6f} rad; raw=2570 -> {to_rad(2570):+.4f} rad = {math.degrees(to_rad(2570)):+.2f}°")

print()
print("=" * 72)
print("步骤 6  ONNX 发布契约常量（publish/manifest.py，纯 stdlib 可导入）")
print("=" * 72)
sys.path.insert(0, str(MANIFEST_PY.parent))
import manifest
check("OBS_LEN==61", manifest.OBS_LEN == 61, str(manifest.OBS_LEN))
check("ACTION_LEN==14", manifest.ACTION_LEN == 14, str(manifest.ACTION_LEN))
check("control_hz==50（20ms 闭环）", manifest.ROBOT["control_hz"] == 50)
check("策略文件名固定 policy.onnx", manifest.POLICY_FILE == "policy.onnx")
print(f"  MODEL_API={manifest.MODEL_API} schema=v{manifest.SCHEMA_VERSION} slots={manifest.SLOTS}")

print()
print("=" * 72)
print(f"结果: {ok} PASS / {fail} FAIL")
print("=" * 72)
sys.exit(1 if fail else 0)
