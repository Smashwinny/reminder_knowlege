# -*- coding: utf-8 -*-
"""
实验 1：手工构造一个 3DGS 格式的合成 PLY 点云
目的：搞清楚一个"高斯"在文件里到底存了哪些字段（3DGS 的数据结构是理解一切的钥匙）
运行：python make_synthetic_ply.py
输出：synthetic_scene.ply（1500 个高斯，组成一个红-蓝渐变的球壳 + 一个绿色高散射盘）
"""
import numpy as np
import struct

C0 = 0.28209479177387814  # SH 基函数 Y_00，DC 项颜色 = 0.5 + C0 * f_dc
N_SHELL, N_DISK = 1000, 500

rng = np.random.default_rng(42)

def make_gaussian(pos, color, scale, opacity, rot_quat):
    """返回一个高斯的全部存储字段（3DGS train.py 保存的就是这些）"""
    return dict(
        x=pos[0], y=pos[1], z=pos[2],
        nx=0.0, ny=0.0, nz=0.0,                       # 法线：3DGS 不用，全 0 占位
        f_dc=[(c - 0.5) / C0 for c in color],         # SH DC 项（视角无关的基础色）
        f_rest=[0.0] * 45,                            # SH 高阶项（视角相关颜色），全 0 = 无视角效果
        opacity=opacity,                              # 注意：存的是 logit，渲染时要过 sigmoid
        scale=[np.log(s) for s in scale],             # 注意：存的是 log，渲染时要 exp
        rot=rot_quat,                                 # 单位四元数 (w,x,y,z)
    )

gaussians = []
# --- 球壳：红蓝按纬度渐变，模拟"用高斯拼出实体表面" ---
for i in range(N_SHELL):
    v = rng.uniform(-1, 1); theta = rng.uniform(0, 2 * np.pi)
    r = np.sqrt(1 - v * v)
    pos = np.array([r * np.cos(theta), v, r * np.sin(theta)]) * 1.0
    pos += rng.normal(0, 0.01, 3)                      # 表面加一点厚度噪声
    color = [0.7 + 0.2 * v, 0.2, 0.7 - 0.2 * v]        # 上红下蓝渐变
    q = rng.normal(0, 1, 4); q /= np.linalg.norm(q)    # 随机朝向
    gaussians.append(make_gaussian(pos, color, [0.02, 0.02, 0.02], 2.5, q))

# --- 散射盘：大而扁的绿色高斯，模拟"半透明大片"（灵隐寺里像香火烟雾） ---
for i in range(N_DISK):
    rr, ang = 0.4 * np.sqrt(rng.uniform(0, 1)), rng.uniform(0, 2 * np.pi)
    pos = np.array([rr * np.cos(ang), -1.15, rr * np.sin(ang)])
    gaussians.append(make_gaussian(pos, [0.1, 0.8, 0.2], [0.15, 0.008, 0.15], 1.0, [1, 0, 0, 0]))

# --- 写二进制 little-endian PLY（3DGS 的标准输出格式）---
fields = ["x", "y", "z", "nx", "ny", "nz",
          "f_dc_0", "f_dc_1", "f_dc_2",
          *[f"f_rest_{i}" for i in range(45)],
          "opacity", "scale_0", "scale_1", "scale_2", "rot_0", "rot_1", "rot_2", "rot_3"]
header = ["ply", "format binary_little_endian 1.0", f"element vertex {len(gaussians)}",
          *[f"property float {f}" for f in fields], "end_header"]
rows = np.zeros((len(gaussians), len(fields)), dtype=np.float32)
for gi, g in enumerate(gaussians):
    for fi, f in enumerate(fields):
        if f in g:
            rows[gi, fi] = g[f]
        elif f.startswith("f_dc_"):
            rows[gi, fi] = g["f_dc"][int(f[-1])]
        elif f.startswith("f_rest_"):
            rows[gi, fi] = g["f_rest"][int(f.split("_")[-1])]
        elif f.startswith("scale_"):
            rows[gi, fi] = g["scale"][int(f[-1])]
        elif f.startswith("rot_"):
            rows[gi, fi] = g["rot"][int(f[-1])]

with open("synthetic_scene.ply", "wb") as fp:
    fp.write(("\n".join(header) + "\n").encode("ascii"))
    fp.write(rows.tobytes())

print(f"OK: synthetic_scene.ply written, {len(gaussians)} gaussians, "
      f"{len(fields)} fields each, {rows.nbytes} bytes payload")
print("字段清单:", fields[:10], "...", fields[-6:])
