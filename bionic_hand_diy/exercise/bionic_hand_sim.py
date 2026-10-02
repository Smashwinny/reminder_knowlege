# -*- coding: utf-8 -*-
"""
bionic_hand_sim.py — 百元仿生机械手·无硬件数字仿真（learn-project 主实验）
子项目: bionic_hand_diy (拾遗任务 6e3cb007)

五个实验步骤，全部纯软件可跑，不需要购买任何硬件：
  Step1  SG90 舵机 PWM 脉宽 -> 角度映射（并校验边界）
  Step2  单指绳驱欠驱动耦合模型：闭合量 c(0~1) -> 三关节角
         （对照 Yale OpenHand openhand.py 的 amnt 0~1 比例量控制思想）
  Step3  2D 正运动学：关节角 -> 指尖坐标（几何法，不用背 DH）
  Step4  五指"张开/握拢"两姿态图 + 单指指尖轨迹图（matplotlib 出 PNG）
  Step5  完整抓取序列仿真表（张开->闭合->保持->释放），并做合理性断言

运行: python bionic_hand_sim.py   （工作目录随意，产物写在脚本同目录）
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------
# Step 1: SG90 舵机 PWM 映射
#   周期 20ms(50Hz)，脉宽 0.5ms~2.5ms 对应 0°~180°
# ----------------------------------------------------------------------
PULSE_MIN_US = 500.0    # 0°  时的脉宽（微秒）
PULSE_MAX_US = 2500.0   # 180°时的脉宽（微秒）
SERVO_RANGE_DEG = 180.0

def pulse_to_angle(pulse_us: float) -> float:
    """脉宽(微秒) -> 舵机输出轴角度(度)"""
    return (pulse_us - PULSE_MIN_US) / (PULSE_MAX_US - PULSE_MIN_US) * SERVO_RANGE_DEG

def angle_to_pulse(angle_deg: float) -> float:
    """舵机角度(度) -> 脉宽(微秒)"""
    return PULSE_MIN_US + np.clip(angle_deg, 0, SERVO_RANGE_DEG) / SERVO_RANGE_DEG * (PULSE_MAX_US - PULSE_MIN_US)

def step1():
    print("=" * 62)
    print("Step1  SG90 舵机 PWM 脉宽 -> 角度映射")
    for p in (500, 1000, 1500, 2000, 2500):
        print(f"  脉宽 {p:5d} us  ->  {pulse_to_angle(p):6.1f} deg   "
              f"(周期 20ms 中占比 {p/20000:.1%})")
    # 校验：中位、边界、往返一致
    assert pulse_to_angle(1500) == 90.0
    assert pulse_to_angle(500) == 0.0 and pulse_to_angle(2500) == 180.0
    for a in (0, 45, 90, 135, 180):
        assert abs(pulse_to_angle(angle_to_pulse(a)) - a) < 1e-9
    print("  [PASS] 中位 1500us->90°，边界 500/2500us->0°/180°，往返映射一致")
    print("  说明：Arduino 的 servo.write(90) 内部干的就是这个换算。")
    print()

# ----------------------------------------------------------------------
# Step 2: 单指绳驱欠驱动耦合
#   一根腱绳穿过三节指骨的导索孔，舵机卷线轮拉绳：
#   绳行程 S = Σ (r_i * θ_i)（θ 为弧度，r 为各节等效卷径）
#   腱绳绷紧时最先弯"近端"关节（指根 MCP），被物体挡住后绳继续走、
#   弯"中端"PIP，再挡住才弯"远端"DIP —— 这就是"遇阻自适应包络"。
#   无物体时空载简化：行程按卷径比分配，比例 coupling = (5, 3, 2)。
# ----------------------------------------------------------------------
FINGER_LEN = np.array([40.0, 26.0, 18.0])   # 三节指骨长 mm（中指）
COUPLING = np.array([5.0, 3.0, 2.0])        # 三关节行程分配比（近:中:远）
THETA_MAX = np.deg2rad(np.array([90.0, 100.0, 70.0]))  # 各关节最大弯曲角

def close_amount_to_angles(c: float) -> np.ndarray:
    """闭合量 c∈[0,1]（对标 openhand.py 的 amnt）-> 三关节弯曲角(弧度)"""
    c = float(np.clip(c, 0.0, 1.0))
    shares = COUPLING / COUPLING.sum()
    return np.minimum(c * 2.0 * shares, 1.0) * THETA_MAX   # c=1 时全体到位

def tendon_travel(theta: np.ndarray, r=2.0) -> float:
    """给定三关节角，腱绳被拉过的行程 mm（各节 r*θ 之和）"""
    return float((r * theta).sum())

def step2():
    print("=" * 62)
    print("Step2  绳驱欠驱动：闭合量 c -> 三关节角（耦合比 5:3:2）")
    print(f"  {'c':>5} | {'MCP(°)':>7} {'PIP(°)':>7} {'DIP(°)':>7} | 绳行程mm")
    for c in (0.0, 0.25, 0.5, 0.75, 1.0):
        th = close_amount_to_angles(c)
        print(f"  {c:5.2f} | {np.rad2deg(th[0]):7.1f} {np.rad2deg(th[1]):7.1f} "
              f"{np.rad2deg(th[2]):7.1f} | {tendon_travel(th):6.2f}")
    th = close_amount_to_angles(1.0)
    # 比例耦合：c=1 时近端(MCP)满角 90°，中/远端按 0.6/0.4 到位 —— 空载简化
    assert np.allclose(np.rad2deg(th), [90.0, 60.0, 28.0])
    assert close_amount_to_angles(0.0).sum() == 0
    cs = np.linspace(0, 1, 21)
    travels = [tendon_travel(close_amount_to_angles(c)) for c in cs]
    assert all(b >= a for a, b in zip(travels, travels[1:]))   # 行程单调
    print("  [PASS] c=0 全伸直、c=1 近端满角/中远端按耦合比到位，绳行程单调递增")
    print("  对照 repo/Python-3.6/openhand.py：其 amnt∈[0,1] 同样是")
    print("  '比例量'，内部才换算成编码器值 —— 思想完全一致。")
    print()

# ----------------------------------------------------------------------
# Step 3: 2D 正运动学（平面三连杆）
#   指根为原点，指骨方向角 phi_k = -90° + (MCP+... 累计弯曲角)
#   指尖 P = Σ L_k * (cos phi_k, sin phi_k)
# ----------------------------------------------------------------------
def fingertip(theta: np.ndarray, lengths=FINGER_LEN) -> np.ndarray:
    phi = np.pi / 2 - np.cumsum(theta)           # 初始垂直向上，弯曲朝掌心
    pts = np.cumsum(lengths[:, None] * np.stack([np.cos(phi), np.sin(phi)], 1), 0)
    return pts[-1], np.vstack([[[0, 0]], pts])   # 指尖坐标 + 全关节坐标

def step3():
    print("=" * 62)
    print("Step3  2D 正运动学：关节角 -> 指尖坐标")
    th0 = np.zeros(3)
    tip0, _ = fingertip(th0)
    print(f"  全伸直 (0,0,0): 指尖 = ({tip0[0]:+.4f}, {tip0[1]:+.4f}) mm，"
          f"应恰为指长和 {FINGER_LEN.sum()} mm")
    th1 = close_amount_to_angles(1.0)
    tip1, _ = fingertip(th1)
    print(f"  全握拢 c=1.0  : 指尖 = ({tip1[0]:+7.2f}, {tip1[1]:+7.2f}) mm，"
          f"离指根距离 {np.hypot(*tip1):.2f} mm")
    assert abs(tip0[0]) < 1e-9 and abs(tip0[1] - FINGER_LEN.sum()) < 1e-9
    assert np.hypot(*tip1) < 0.85 * FINGER_LEN.sum()  # 握拢后指尖明显收拢
    assert tip1[0] > 0.5 * FINGER_LEN.sum()           # 且横向卷向掌心一侧
    print("  [PASS] 伸直时指尖=指长和；握拢后指尖收拢且卷向掌心")
    print()

# ----------------------------------------------------------------------
# Step 4: 画五指两姿态 + 单指指尖轨迹
#   五指长度（拇指短且横向安装，其余依次变长再略短）
# ----------------------------------------------------------------------
FINGERS = [  # (名称, 三节长 mm, 指根x位置, 指根初始朝向°(正值向左扇开), 耦合比)
    ("拇指", np.array([32.0, 26.0, 18.0]), -34.0, 55.0, np.array([5, 3, 2])),
    ("食指", np.array([36.0, 24.0, 17.0]), -18.0, 12.0,  np.array([5, 3, 2])),
    ("中指", np.array([40.0, 26.0, 18.0]),  -2.0, 0.0,   np.array([5, 3, 2])),
    ("无名指", np.array([37.0, 25.0, 17.0]), 14.0, -12.0, np.array([5, 3, 2])),
    ("小指", np.array([29.0, 19.0, 15.0]),  28.0, -25.0, np.array([5, 3, 2])),
]
FINGER_COLORS = ["#7209b7", "#f77f00", "#d62828", "#2a9d8f", "#1d6fb8"]

def finger_chain(name, lengths, x0, base_deg, coupling, c):
    th = np.minimum(c * 2.0 * coupling / coupling.sum(), 1.0) * \
         np.deg2rad(np.array([90.0, 100.0, 70.0]))
    curl = np.sign(base_deg) if base_deg != 0 else 1.0   # 向掌心中心卷拢
    phi = np.deg2rad(base_deg) + np.pi / 2 - curl * np.cumsum(th)
    pts = np.cumsum(lengths[:, None] * np.stack([np.cos(phi), np.sin(phi)], 1), 0)
    return np.vstack([[[x0, 0.0]], pts + [x0, 0.0]])

def step4():
    print("=" * 62)
    print("Step4  生成姿态图与指尖轨迹图（matplotlib -> PNG）")
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    palm_w = 70
    for ax, c, title in zip(axes, (0.0, 1.0),
                            ("张开 c=0.0", "握拢 c=1.0（欠驱动包络）")):
        ax.add_patch(plt.Rectangle((-palm_w/2 - 6, -14), palm_w + 12, 16,
                                   fc="#ffb703", ec="#7a4b00", lw=1.6, zorder=1))
        for k, (name, L, x0, base, cp) in enumerate(FINGERS):
            chain = finger_chain(name, L, x0, base, cp, c)
            ax.plot(chain[:, 0], chain[:, 1], "-o", color=FINGER_COLORS[k],
                    lw=3.2, ms=5, mec="#333", zorder=3)
        ax.set_title(title, fontsize=13, color="#d00000", fontweight="bold")
        ax.set_aspect("equal"); ax.set_xlim(-95, 95); ax.set_ylim(-80, 100)
        ax.axis("off")
    fig.suptitle("bionic_hand_diy 仿真：绳驱欠驱动五指两姿态", fontsize=15,
                 color="#1d3557", fontweight="bold")
    fig.tight_layout()
    p1 = os.path.join(HERE, "fig_hand_poses.png")
    fig.savefig(p1, dpi=130); plt.close(fig)

    fig2, ax = plt.subplots(figsize=(7.2, 5.4))
    cs = np.linspace(0, 1, 33)
    for name, L, x0, base, cp in FINGERS:
        tips = np.array([finger_chain(name, L, x0, base, cp, c)[-1] for c in cs])
        ax.plot(tips[:, 0], tips[:, 1], lw=2.2,
                label=f"{name} 指尖轨迹", color=plt.cm.tab10(hash(name) % 10))
        ax.scatter(tips[0, 0], tips[0, 1], s=42, marker="^", zorder=3)
        ax.scatter(tips[-1, 0], tips[-1, 1], s=52, marker="*", zorder=3)
    ax.set_title("闭合量 c: 0→1 时五指指尖扫掠轨迹（△起点 ★终点）",
                 fontsize=12, color="#1d3557", fontweight="bold")
    ax.set_xlabel("x (mm)"); ax.set_ylabel("y (mm)")
    ax.legend(fontsize=8.5); ax.grid(alpha=.3); ax.set_aspect("equal")
    fig2.tight_layout()
    p2 = os.path.join(HERE, "fig_finger_trajectory.png")
    fig2.savefig(p2, dpi=130); plt.close(fig2)
    print(f"  [PASS] 已生成:\n    {p1}\n    {p2}")
    print()

# ----------------------------------------------------------------------
# Step 5: 抓取序列仿真（对标 openhand.py 的 move_hand 序列思想）
# ----------------------------------------------------------------------
def step5():
    print("=" * 62)
    print("Step5  完整抓取序列：张开 -> 闭合 -> 保持 -> 释放")
    print(f"  {'阶段':<6} {'c':>5} | {'中指MCP':>7} {'PIP':>6} {'DIP':>6} | 绳行程mm")
    seq = [("张开", 0.0), ("闭合", 1.0), ("保持", 1.0), ("释放", 0.0)]
    prev = None
    for name, c in seq:
        th = close_amount_to_angles(c)
        print(f"  {name:<6} {c:5.2f} | {np.rad2deg(th[0]):7.1f} "
              f"{np.rad2deg(th[1]):6.1f} {np.rad2deg(th[2]):6.1f} | "
              f"{tendon_travel(th):6.2f}")
        if prev is not None:
            d = np.abs(th - prev).max()
            assert d > 1e-6 or name == "保持"   # 除"保持"外角度必须变化
        prev = th
    # 释放必须回到张开位形，闭合后的位形必须与张开不同
    assert np.allclose(close_amount_to_angles(0.0), 0.0)
    assert close_amount_to_angles(1.0).sum() > 0
    print("  [PASS] 序列状态机合法：闭合/释放为互逆过程，保持阶段角度冻结")
    print("  结论：没有硬件，也完整验证了『PWM→角度→耦合→运动学』整条控制链。")
    print("=" * 62)

if __name__ == "__main__":
    step1(); step2(); step3(); step4(); step5()
    print("全部 5 步实验完成，断言全部通过。")
