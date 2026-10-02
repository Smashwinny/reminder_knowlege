# -*- coding: utf-8 -*-
"""
实验 2（主实验）：用纯 numpy 复刻 3DGS 渲染管线的核心数学 —— "mini-splat"
管线四步（与官方 diff-gaussian-rasterization 一一对应）：
  ① Σ = R S Sᵀ Rᵀ      —— 从存储的 scale/四元数还原每个高斯的 3D 协方差
  ② 世界坐标 -> 相机坐标 -> 像素平面（透视投影 + 雅可比把 3D 协方差压成 2D）
  ③ 按相机距离排序（官方 GPU 版用逐 tile 16x16 排序）
  ④ 逐像素前向 α 混合：C = Σ c_i α_i Π_{j<i}(1-α_j)
运行：python mini_splat.py  → 输出 render.png（512x512）
验证：图像应显示红蓝渐变球壳 + 底下一片绿色散射盘，且无 numpy/PyTorch GPU 依赖
"""
import math
import numpy as np
from PIL import Image

W = H = 512
FOV_Y = math.radians(50.0)
CAM_POS = np.array([0.0, 0.0, 3.0])
LOOK_AT = np.array([0.0, -0.05, 0.0])
C0 = 0.28209479177387814

# ---------- 读 PLY（复用实验 1 的格式知识） ----------
def load_ply(path):
    with open(path, "rb") as fp:
        header, line = [], b""
        while line.strip() != b"end_header":
            line = fp.readline(); header.append(line.decode("ascii").strip())
        n = int([l for l in header if l.startswith("element vertex")][0].split()[-1])
        props = [l.split()[-1] for l in header if l.startswith("property float")]
        data = np.frombuffer(fp.read(n * len(props) * 4), dtype="<f4").reshape(n, len(props))
    i = {p: k for k, p in enumerate(props)}
    return dict(
        pos=data[:, [i['x'], i['y'], i['z']]].astype(np.float64),
        color=0.5 + C0 * data[:, [i['f_dc_0'], i['f_dc_1'], i['f_dc_2']]].astype(np.float64),
        scale=np.exp(data[:, [i['scale_0'], i['scale_1'], i['scale_2']]].astype(np.float64)),  # log -> 线性
        opacity=1 / (1 + np.exp(-data[:, i['opacity']].astype(np.float64))),                   # logit -> sigmoid
        quat=data[:, [i['rot_0'], i['rot_1'], i['rot_2'], i['rot_3']]].astype(np.float64),
    )

# ---------- ① 四元数 -> 旋转矩阵，Σ = R S Sᵀ Rᵀ ----------
def quat_to_R(q):
    w, x, y, z = q / np.linalg.norm(q)
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z),   2*(x*z+w*y)],
        [2*(x*y+w*z),   1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y),   2*(y*z+w*x),   1-2*(x*x+y*y)]])

# ---------- 相机外参（look-at） ----------
fwd = LOOK_AT - CAM_POS; fwd /= np.linalg.norm(fwd)
right = np.cross(fwd, [0, 1, 0.0]); right /= np.linalg.norm(right)
up = np.cross(right, fwd)
Wm = np.stack([right, -up, -fwd])                    # 世界->相机（OpenGL 风格，相机看 -z）

fy = (H / 2) / math.tan(FOV_Y / 2); fx = fy
pp = np.array([W / 2, H / 2])

g = load_ply("synthetic_scene.ply")
N = len(g["pos"])
print(f"载入 {N} 个高斯，开始渲染 {W}x{H} ...")

# ② 3D 协方差 -> 相机空间 -> 2D 像素协方差（论文式 9 的雅可比法）
t = (g["pos"] - CAM_POS) @ Wm.T
in_front = t[:, 2] < -0.1                            # 相机看 -z，取在前的
depth = -t[:, 2]
tx, ty, tz = t[:, 0], t[:, 1], t[:, 2]
J = np.zeros((N, 2, 3))
J[:, 0, 0] = fx / -tz; J[:, 0, 2] = fx * tx / (tz * tz)
J[:, 1, 1] = fy / -tz; J[:, 1, 2] = fy * ty / (tz * tz)
uv = np.stack([fx * tx / -tz, fy * ty / tz], axis=1) + pp

cov3d = np.zeros((N, 3, 3))
for k in range(N):
    R = quat_to_R(g["quat"][k]); S = np.diag(g["scale"][k] ** 2)
    cov3d[k] = R @ S @ R.T
WmT = np.tile(Wm, (N, 1, 1))
cov_cam = WmT @ cov3d @ WmT.transpose(0, 2, 1)
cov2d = J @ cov_cam @ J.transpose(0, 2, 1)           # 2x2 像素协方差

# ③ 按深度排序：远->近，用"后向混合"等价实现前向 α 混合
order = np.argsort(-depth)

# ④ 逐高斯泼溅到画布（带 3σ 包围盒裁剪）
img = np.zeros((H, W, 3)); T = np.ones((H, W))       # T = 剩余透射率
splashed = 0
for k in order:
    if not in_front[k]:
        continue
    u, v = uv[k]
    a, b, c = cov2d[k, 0, 0], cov2d[k, 0, 1], cov2d[k, 1, 1]
    det = a * c - b * b
    if det <= 1e-9:                                   # 退化（侧对镜头的薄片）
        continue
    rad = int(3 * math.sqrt(max(a, c)))
    x0, x1 = max(int(u - rad), 0), min(int(u + rad) + 1, W)
    y0, y1 = max(int(v - rad), 0), min(int(v + rad) + 1, H)
    if x0 >= x1 or y0 >= y1:
        continue
    xs, ys = np.meshgrid(np.arange(x0, x1) + 0.5 - u, np.arange(y0, y1) + 0.5 - v)
    power = -(a * ys * ys + c * xs * xs - 2 * b * xs * ys) / (2 * det)   # 论文式：exp(-1/2 dᵀΣ⁻¹d) 化简
    alpha = np.clip(g["opacity"][k] * np.exp(power), 0, 0.99)
    Tk = T[y0:y1, x0:x1]
    contrib = (alpha * Tk)[..., None] * g["color"][k]
    img[y0:y1, x0:x1] += contrib
    T[y0:y1, x0:x1] = Tk * (1 - alpha)
    splashed += 1
img += T[..., None] * 0.08                           # 背景色（近黑），透过率兜底
out = (np.clip(img, 0, 1) * 255).astype(np.uint8)
Image.fromarray(out[::-1]).save("render.png")        # v 向下为正，翻转成图像习惯
print(f"OK: render.png 已生成。{splashed}/{N} 个高斯参与了泼溅，背景透过率均值 {T.mean():.3f}")
