# -*- coding: utf-8 -*-
"""ex2: 用 MuJoCo 加载 OpenArm v1 单臂 MJCF —— 关节解剖 + FK + 失力下坠 + PD 保持实验。"""
import os, numpy as np, mujoco

XML = os.path.join(os.path.dirname(__file__), "..", "repo", "subs",
                   "openarm_mujoco", "v1", "openarm.xml")
model = mujoco.MjModel.from_xml_path(XML)
data = mujoco.MjData(model)

print("== 模型总览 ==")
print(f"nq(位置维)={model.nq}  nv(速度维)={model.nv}  nu(执行器)={model.nu}  "
      f"nbody={model.nbody}  njnt={model.njnt}")
print(f"dt={model.opt.timestep}s   总质量={sum(model.body_mass):.3f} kg")

print("\n== 关节解剖（7 hinge + 2 slide）==")
for i in range(model.njnt):
    name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, i)
    jtype = "hinge" if model.jnt_type[i] == 3 else "slide"
    lo, hi = model.jnt_range[i]
    print(f"  [{i}] {name:<26} {jtype:<6} range=[{lo:+.3f}, {hi:+.3f}] rad")

# ---- FK：全部关节角=0（竖直伸展位），看末端在哪 ----
mujoco.mj_resetData(model, data)
mujoco.mj_forward(model, data)
hand_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "openarm_hand")
p_zero = data.xpos[hand_id].copy()
print(f"\n== FK（全零位）== 末端 openarm_hand 位置 = "
      f"[{p_zero[0]:+.4f}, {p_zero[1]:+.4f}, {p_zero[2]:+.4f}] m")

# 摆一个姿势：joint2 抬 90°，joint4 抬 90°（前伸抓取姿）
data.qpos[1] = np.pi / 2   # joint2
data.qpos[3] = np.pi / 2   # joint4
mujoco.mj_forward(model, data)
p_pose = data.xpos[hand_id]
print(f"== FK（joint2=90°, joint4=90°）== 末端位置 = "
      f"[{p_pose[0]:+.4f}, {p_pose[1]:+.4f}, {p_pose[2]:+.4f}] m")
print(f"   末端位移 |Δp| = {np.linalg.norm(p_pose - p_zero)*1000:.1f} mm")

# ---- 实验 A：断电下坠（ctrl=0，无重力补偿，2 秒）----
mujoco.mj_resetData(model, data)
q2_start = float(data.qpos[1])
traj = []
for _ in range(1000):           # 2.0 s
    data.ctrl[:] = 0.0
    mujoco.mj_step(model, data)
    traj.append(data.qpos[1])
traj = np.array(traj)
print(f"\n== 实验 A：断电下坠 2s ==")
print(f"  joint2 从 {q2_start:+.4f} rad 掉到 {traj[-1]:+.4f} rad "
      f"（行程 {abs(traj[-1]-q2_start)*57.3:.1f}°）")
print(f"  峰值角速度 {np.abs(np.diff(traj)).max()/model.opt.timestep:.2f} rad/s")
print("  => 高反驱机械臂断电即被重力拖着走：安全（不较劲），但也证明『必须重力补偿才能定住』")

# ---- 实验 B：纯 PD 力矩保持 vs 加入"重力补偿前馈" ----
def pd_hold(gcomp=False, seconds=3.0):
    mujoco.mj_resetData(model, data)
    kp, kd = np.full(9, 40.0), np.full(9, 2.0)
    kp[1], kd[1] = 120.0, 4.0                      # 肩关节加大增益
    q_des = np.zeros(9)
    errs, max_ctrl = [], 0.0
    gcomp_tau = np.zeros(9)
    if gcomp:  # 用 mj_inverse 在目标位姿算静态所需力矩当"重力补偿前馈"
        mujoco.mj_resetData(model, data)
        mujoco.mj_forward(model, data)
        data.qacc[:] = 0
        mujoco.mj_inverse(model, data)
        gcomp_tau = np.clip(data.qfrc_inverse[:9], -10, 10)
    steps = int(seconds / model.opt.timestep)
    for _ in range(steps):
        tau = kp * (q_des - data.qpos[:9]) - kd * data.qvel[:9] + (gcomp_tau if gcomp else 0)
        max_ctrl = max(max_ctrl, float(np.abs(tau).max()))
        data.ctrl[:] = np.clip(tau[:8], -10, 10)
        mujoco.mj_step(model, data)
        errs.append(data.qpos.copy())
    errs = np.array(errs)
    return np.abs(errs[:, :7]).max(axis=0), max_ctrl

e_pure, c1 = pd_hold(gcomp=False)
e_gc,   c2 = pd_hold(gcomp=True)
print(f"\n== 实验 B：竖直伸展位姿保持 3s（该位姿重力矩最大）==")
print(f"  {'关节':<10}{'纯PD稳态误差(°)':>16}{'PD+重力补偿(°)':>16}")
for i in range(7):
    print(f"  joint{i+1:<6}{np.degrees(e_pure[i]):>16.3f}{np.degrees(e_gc[i]):>16.3f}")
print(f"  纯PD max|ctrl|={c1:.1f}  PD+重力补偿 max|ctrl|={c2:.1f}（限幅 ±10）")
imp = 1 - np.degrees(e_gc).sum() / max(np.degrees(e_pure).sum(), 1e-9)
print(f"  7 关节误差总和改善 {imp*100:.1f}%")

# ---- 附：尝试离屏渲染一张结构图（失败则如实说明）----
try:
    # 用 MjSpec 注入一盏方向光再渲染（原 MJCF 无灯光，裸渲染全黑；spec 保留 mesh 相对路径）
    spec = mujoco.MjSpec.from_file(XML)
    spec.worldbody.add_light(pos=[0, 0, 3], dir=[0, 0, -1],
                             type=mujoco.mjtLightType.mjLIGHT_DIRECTIONAL, intensity=8)
    spec.worldbody.add_light(pos=[0.8, -0.8, 0.8],
                             type=mujoco.mjtLightType.mjLIGHT_POINT, intensity=5)
    lit = spec.compile()
    r = mujoco.Renderer(lit, height=480, width=640)
    model, data = lit, mujoco.MjData(lit)
    mujoco.mj_resetData(model, data)
    data.qpos[1] = np.pi / 2
    data.qpos[3] = np.pi / 2
    mujoco.mj_forward(model, data)
    r.update_scene(data, camera=mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_CAMERA, "side"))
    png = r.render()
    out = os.path.join(os.path.dirname(__file__), "ex2_render.png")
    try:
        from PIL import Image
        Image.fromarray(png).save(out)
        print(f"\n[渲染] 已保存 {out}")
    except Exception as e2:
        print(f"\n[渲染] 渲染成功但写 PNG 失败：{e2}")
except Exception as e:
    print(f"\n[渲染] 无头环境无 GL 上下文，离屏渲染不可用（如实记录）：{type(e).__name__}: {e}")
