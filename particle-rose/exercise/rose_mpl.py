# -*- coding: utf-8 -*-
"""
粒子玫瑰 · Python/matplotlib 版
==============================
用"参数方程生成玫瑰表面 + 随机采样成粒子云"的方式画一朵 3D 玫瑰。
这是粒子玫瑰的数学核心，Three.js 版（rose.html）用的是同一套公式。

运行: python rose_mpl.py
输出: rose_mpl.png
"""
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)

# ---------------------------------------------------------------
# 核心公式：一片花瓣 = 一个参数曲面
#   t ∈ [0,1]  沿花瓣长度（0=花心, 1=瓣尖）
#   s ∈ [-1,1] 沿花瓣宽度（横切方向）
#   层叠方式：内层花瓣小而直立，外层花瓣大而外翻下垂 —— 这就是玫瑰的"包心"结构
# ---------------------------------------------------------------
def petal_layer(rng, n_petals, R, a0, a1, fold, curl, z_base, phase, n_samples, palette):
    """
    一层花瓣的粒子点集与颜色。
    花瓣中心线 = 一条从"近竖直"弯到"外翻"的弧线：
      α(t) = a0 → a1  （α 是偏离竖直方向的角度，弧度）
      中心线: r = R·sin(α), z = z_base + R·cos(α)
    再沿瓣宽方向加横向内折（边缘比中肋低 → 瓣面呈勺状）。
    """
    t = rng.random(n_samples)                      # 沿瓣长随机采样
    s = rng.uniform(-1.0, 1.0, n_samples)          # 沿瓣宽随机采样
    alpha = a0 + (a1 - a0) * t                     # 中心线弧线：瓣根竖直 → 瓣尖外翻
    r = R * np.sin(alpha)
    zc = z_base + R * np.cos(alpha)

    w = 0.40 * (2 * np.pi / n_petals) * np.sin(np.pi * np.clip(0.12 + 0.88 * t, 0, 1)) ** 0.7  # 瓣宽包络：随瓣数自适应，留出瓣间缝隙
    theta0 = 2 * np.pi * np.arange(n_petals) / n_petals + phase
    pick = rng.integers(0, n_petals, n_samples)    # 每个粒子随机属于哪一瓣
    phi = theta0[pick] + s * w                     # 绕花轴的方位角（被瓣宽约束）

    x = r * np.cos(phi)
    y = r * np.sin(phi)
    z = zc + R * fold * s**2 * t                   # 横向内折：瓣边缘向"下"弯 → 勺状瓣面
    # 瓣尖上卷：真实玫瑰外层瓣尖会往回勾
    tip = np.clip((t - 0.55) / 0.45, 0, 1)
    z += R * curl * tip**2

    # 微抖动让粒子云有"绒"感
    x += rng.normal(0, 0.012, n_samples)
    y += rng.normal(0, 0.012, n_samples)
    z += rng.normal(0, 0.012, n_samples)

    # 颜色：瓣根深红 → 瓣尖亮粉
    c0, c1 = np.array(palette[0]), np.array(palette[1])
    cols = (1 - t)[:, None] * c0 + t[:, None] * c1
    return np.column_stack([x, y, z]), cols

# 四层花瓣：α0/α1 = 瓣根/瓣尖偏离竖直的角度。
# 内层近乎直立包心，越往外越摊开、瓣尖甚至下垂（>90°）——这就是玫瑰的"包心"结构。
D = np.pi / 180
layers = [
    dict(n_petals=4,  R=0.40, a0=  8*D, a1= 35*D, fold=0.30, curl=0.10, z_base=0.46, phase=0.00,       n=5000, pal=((0.42,0.00,0.05),(0.88,0.08,0.16))),
    dict(n_petals=7,  R=0.65, a0= 22*D, a1= 56*D, fold=0.26, curl=0.18, z_base=0.34, phase=np.pi/7,    n=7000, pal=((0.50,0.01,0.06),(0.97,0.14,0.22))),
    dict(n_petals=10, R=0.88, a0= 40*D, a1= 76*D, fold=0.22, curl=0.28, z_base=0.24, phase=np.pi/4,    n=9000, pal=((0.58,0.03,0.08),(1.00,0.22,0.30))),
    dict(n_petals=14, R=1.02, a0= 58*D, a1= 93*D, fold=0.18, curl=0.40, z_base=0.14, phase=np.pi/16,   n=11000,pal=((0.66,0.05,0.10),(1.00,0.40,0.47))),
]

pts_all, col_all = [], []
for L in layers:
    p, c = petal_layer(rng, L["n_petals"], L["R"], L["a0"], L["a1"], L["fold"], L["curl"], L["z_base"], L["phase"], L["n"], L["pal"])
    pts_all.append(p); col_all.append(c)

# 花蕊：中心一小簇深红密集粒子
n_core = 1500
core = np.column_stack([
    rng.normal(0, 0.06, n_core),
    rng.normal(0, 0.06, n_core),
    rng.normal(0.72, 0.07, n_core),
])
pts_all.append(core)
col_all.append(np.tile((0.35, 0.00, 0.04), (n_core, 1)))

# 花茎：一条带弧度的绿色粒子线
t = np.linspace(0, 1, 900)
stem = np.column_stack([
    0.15 * np.sin(2.2 * t),       # 微微弯一下更自然
    0.10 * np.sin(3.1 * t + 1.0),
    0.05 - 2.7 * t,
])
pts_all.append(stem)
col_all.append(np.tile((0.10, 0.45, 0.12), (len(stem), 1)))

P = np.vstack(pts_all); C = np.clip(np.vstack(col_all), 0, 1)

# ---------------------------------------------------------------
# 绘图
# ---------------------------------------------------------------
fig = plt.figure(figsize=(8, 9), facecolor="black")
ax = fig.add_subplot(111, projection="3d", facecolor="black")
ax.scatter(P[:,0], P[:,1], P[:,2], c=C, s=1.2, marker="o", depthshade=False, linewidths=0)
ax.set_axis_off()
ax.set_box_aspect((1, 1, 1.5))                     # 茎在下方，纵向拉长
ax.view_init(elev=20, azim=-60)
ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3); ax.set_zlim(-2.9, 1.5)
ax.set_title("Particle Rose  ·  matplotlib", color="w", pad=2)
plt.tight_layout()
plt.savefig("rose_mpl.png", dpi=130, facecolor="black")
print(f"OK: rose_mpl.png saved, particles = {len(P)}")
