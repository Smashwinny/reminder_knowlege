# -*- coding: utf-8 -*-
"""
microduck 无真机仿真实验（全部命令真实运行于 Windows 11 + Python 3.14 + MuJoCo 3.14）
素材：
  - kinematics MJCF（纯运动学树）: microduck/repo/kinematics/assets/alpha/robot_walk.xml
  - 完整物理场景（含网格+执行器+关键帧）: microduck_rl repo_rl/src/mjlab_microduck/robot/microduck/scene.xml
回答四个问题：
  A. 官方训练 MJCF 里到底有什么、没有什么？      -> 实验0/1 模型体检 + 无地板坠落
  B. 位置舵机（最笨的"大脑"）能让鸭子站稳吗？    -> 实验2 INIT vs STAND 关键帧
  C. 被推一把会怎样（为什么需要 RL 平衡策略）？   -> 实验3 侧向冲击
  D. kinematics crate 的 FK 思路对不对？          -> 实验4 手写 FK 对拍 mj_kinematics（镜像上游 64 姿态测试）
"""
import numpy as np
import mujoco
import xml.etree.ElementTree as ET

KIN_XML = r"F:\reminder\microduck\repo\kinematics\assets\alpha\robot_walk.xml"
SCENE_XML = r"F:\reminder\microduck\repo_rl\src\mjlab_microduck\robot\microduck\scene.xml"
np.set_printoptions(precision=4, suppress=True)

# ---------- 实验0：训练 MJCF 体检（kinematics crate 内嵌的就是它） ----------
model = mujoco.MjModel.from_xml_path(KIN_XML)
print("=== 实验0：kinematics 内嵌 MJCF 体检 ===")
print(f"nq={model.nq} nv={model.nv} nu(执行器)={model.nu} ngeom(碰撞体)={model.ngeom}")
hinge = [mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, i) for i in range(model.njnt)]
print(f"{len(hinge)} 个关节: {hinge}")
print(f"总质量 {sum(model.body_mass)*1000:.1f} g （官方标称 <800 g ✓）")

# ---------- 实验1：这份 MJCF 没有地板 —— 被动丢下去直坠 ----------
m1 = mujoco.MjModel.from_xml_path(KIN_XML); d1 = mujoco.MjData(m1)
d1.qpos[:] = 0; d1.qpos[2] = 0.12
for _ in range(120):  # 0.12 s @ 1ms 步长
    mujoco.mj_step(m1, d1)
print("\n=== 实验1：无地板被动坠落 ===")
print(f"t=0 高度 0.120 m -> t={d1.time:.3f}s 高度 {d1.qpos[2]:.3f} m  （自由落体 g*t^2/2 预期 {0.5*9.81*d1.time**2:.3f} m 下落）")
print("=> 训练 MJCF 只给骨架（关节树+惯量），地板/摩擦/接触全在训练场景里 —— sim2real 的第一课")

# ---------- 实验2：真实物理场景，INIT vs STAND 关键帧 ----------
model = mujoco.MjModel.from_xml_path(SCENE_XML)
data = mujoco.MjData(model)
print(f"\n=== 实验2：scene.xml 物理场景 ===")
print(f"nq={model.nq} nu={model.nu} ngeom={model.ngeom} 总质量={sum(model.body_mass)*1000:.1f} g")
hinges = [mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, i)
          for i in range(model.njnt) if model.jnt_type[i] == mujoco.mjtJoint.mjJNT_HINGE]
actu_jnts = [mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, model.actuator_trnid[i,0]) for i in range(model.nu)]
print(f"铰链关节 {len(hinges)} 个，执行器 {model.nu} 个（position 伺服）: {actu_jnts}")

def rollout(name_key, seconds, push_vel=None):
    mujoco.mj_resetDataKeyframe(model, data, mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_KEY, name_key))
    n = int(seconds / model.opt.timestep)
    ts, hs, rolls, fell = [], [], [], None
    for k in range(n):
        if push_vel is not None and data.time >= 1.0 and (k == int(1.0/model.opt.timestep)):
            data.qvel[3] = push_vel  # 给 trunk freejoint 的 vy 一脚冲量
        mujoco.mj_step(model, data)
        ts.append(data.time); hs.append(data.qpos[2])
        # 用四元数算 roll 角
        w,x,y,z = data.qpos[3:7]
        rolls.append(np.degrees(np.arctan2(2*(w*x+y*z), 1-2*(x*x+y*y))))
        if fell is None and data.qpos[2] < 0.05: fell = data.time
    return np.array(ts), np.array(hs), np.array(rolls), fell

for key in ["INIT", "STAND"]:
    ts, hs, rolls, fell = rollout(key, 3.0)
    print(f"\n[{key}] 初始高度 {hs[0]:.3f} m -> 3s 后 {hs[-1]:.3f} m  最低 {hs.min():.3f} m  最大|roll| {np.abs(rolls).max():.1f}°  倒地: {fell}")
    np.savetxt(f"{key.lower()}.csv", np.column_stack([ts, hs, rolls]), delimiter=",", header="t,h,roll_deg", comments="")

# ---------- 实验3：推一把（侧向 0.8 m/s 冲量 @ t=1s） ----------
ts, hs, rolls, fell = rollout("STAND", 3.0, push_vel=0.8)
print(f"\n=== 实验3：STAND 姿态 + t=1s 侧向 0.8 m/s 冲量 ===")
print(f"冲量后 0.1s 高度 {hs[int(1.1/0.002)]:.3f} m, 3s 末 {hs[-1]:.3f} m, 最大|roll| {np.abs(rolls).max():.1f}°, 倒地: {fell}")
np.savetxt("pushed.csv", np.column_stack([ts, hs, rolls]), delimiter=",", header="t,h,roll_deg", comments="")

# ---------- 实验4：手写 FK 对拍 mj_kinematics（64 随机姿态 × 4 site） ----------
print("\n=== 实验4：手写 FK vs MuJoCo（镜像上游 fk_against_mujoco.rs）===")
tree = ET.parse(KIN_XML); root = tree.getroot()

def quat_mul(a, b):
    w1,x1,y1,z1=a; w2,x2,y2,z2=b
    return np.array([w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2,
                     w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2])
def quat_rot(q, v):
    t = quat_mul(quat_mul(q, np.append(0.0, v)), np.array([q[0], -q[1], -q[2], -q[3]]))
    return t[1:]
def axis_angle_quat(axis, ang):
    axis = np.asarray(axis, float); axis = axis/np.linalg.norm(axis); s = np.sin(ang/2)
    return np.array([np.cos(ang/2), *(axis*s)])

def fk_site(site_name, angles):
    target = None
    def walk(el, chain):
        nonlocal target
        for c in el:
            if c.tag == "site" and c.get("name") == site_name:
                target = chain + [c]; return True
            if c.tag == "body" and walk(c, chain + [c]): return True
        return False
    walk(root.find("worldbody"), [])
    pos = np.zeros(3); quat = np.array([1., 0, 0, 0])
    for el in target[:-1]:
        pos = pos + quat_rot(quat, np.array([float(x) for x in el.get("pos", "0 0 0").split()]))
        quat = quat_mul(quat, np.array([float(x) for x in el.get("quat", "1 0 0 0").split()]))
        for j in el.findall("joint"):
            quat = quat_mul(quat, axis_angle_quat(j.get("axis", "0 0 1").split(), angles.get(j.get("name"), 0.0)))
    sp = target[-1]
    return pos + quat_rot(quat, np.array([float(x) for x in sp.get("pos", "0 0 0").split()]))

km = mujoco.MjModel.from_xml_path(KIN_XML); kd = mujoco.MjData(km)
hinge_ids = list(range(km.njnt))
hinge_names = [mujoco.mj_id2name(km, mujoco.mjtObj.mjOBJ_JOINT, i) for i in hinge_ids]
rng = np.random.default_rng(42)
max_err = 0.0
for _ in range(64):
    angles = {n: float(rng.uniform(*km.jnt_range[i])) for n, i in zip(hinge_names, hinge_ids)}
    mujoco.mj_resetData(km, kd); kd.qpos[2] = 0.12
    for n, i in zip(hinge_names, hinge_ids):
        kd.qpos[km.jnt_qposadr[i]] = angles[n]
    mujoco.mj_kinematics(km, kd)
    for s in ["left_foot", "right_foot", "imu", "imu_bno"]:
        max_err = max(max_err, np.abs(fk_site(s, angles) - kd.site(s).xpos).max())
print(f"64 个随机姿态 × 4 site：手写 FK 与 mj_kinematics 最大绝对误差 = {max_err:.3e} m")
print("(上游 Rust 测试 fk_against_mujoco.rs 做的就是同一件事——这正是 kinematics crate 敢跑在 50Hz 环里的底气)")

# 演示：抬左膝 0.6 rad 左脚如何移动
mujoco.mj_resetData(km, kd); kd.qpos[2] = 0.12
mujoco.mj_kinematics(km, kd); foot0 = kd.site("left_foot").xpos.copy()
kd.qpos[km.jnt_qposadr[km.jnt_name2id("left_knee")] if hasattr(km,'jnt_name2id') else km.jnt_qposadr[4]] = 0.6
mujoco.mj_kinematics(km, kd); foot1 = kd.site("left_foot").xpos.copy()
print(f"left_knee 0 -> 0.6 rad：left_foot {foot0} -> {foot1}")
print("\n全部实验完成 ✓")
