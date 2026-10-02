# -*- coding: utf-8 -*-
"""
KV 内存账本仿真：为什么"无距离上限"在数学上成立？
复现 SLAM-Former 论文的三种 token 保留策略，在 CPU 上算一笔长序列内存账：
  策略A 不剪枝        —— KV 随帧数线性涨（首帧锚定法的账单）
  策略B 恒定保留率 γ  —— 前端每帧只看 γ·n 个 token，账本被压到 γ
  策略C 动态保留率    —— KV 池取 log/sqrt(n) 帧的量，账本近乎封顶
并模拟"后端每 10 关键帧全注意力精化 + KV 写回"的事件节奏。
零依赖 numpy + matplotlib。
运行: python kv_ledger_sim.py
"""
import io, os, sys
import numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 中文字体（Windows）
for f in ["Microsoft YaHei", "SimHei"]:
    if any(f.lower() == x.name.lower() for x in font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = f
        break
plt.rcParams["axes.unicode_minus"] = False

# ---- 假设参数（量级取自 SLAM-Former demo 默认值：518 输入、37x37 patch 网格量级） ----
PATCH_PER_FRAME = 37 * 37 // 2      # 剪枝后的有效 token/帧 量级（示意）
DIM = 1024                          # 隐藏维
BYTES = 2                           # fp16
GAMMA = 0.5                         # 论文默认 retention_ratio
GAMMA_EVAL = 0.125                  # 论文实测"指标几乎不降"的保留率
frames = np.unique(np.logspace(1, 5, 200).astype(int))  # 10 ~ 100000 帧（17km 量级）

def kv_bytes(kept_tokens):
    """K+V 各一份：2 * tokens * dim * bytes"""
    return 2 * kept_tokens * DIM * BYTES

# 三种策略的"累计保留 token 数"
tok_A = frames * PATCH_PER_FRAME                       # 不剪枝：线性
tok_B = GAMMA * tok_A                                  # 恒定 γ：斜率变 γ
tok_C = np.log2(np.maximum(frames, 2)) * PATCH_PER_FRAME  # 动态 log 池：近乎封顶

def fmt(b):
    for u in ["B", "KiB", "MiB", "GiB", "TiB"]:
        if b < 1024: return f"{b:,.1f} {u}"
        b /= 1024
    return f"{b:,.1f} PiB"

# ---- 账本表 ----
print("=" * 78)
print("KV 内存账本仿真（dim=%d, fp16, K+V；token/帧=%d 示意）" % (DIM, PATCH_PER_FRAME))
print("=" * 78)
print(f"{'帧数':>8} | {'A 不剪枝':>12} | {'B γ=0.5':>12} | {'C 动态log池':>12} | C 相对 A 节省")
print("-" * 78)
marks = [100, 1_000, 12_000, 100_000]
for n in marks:
    i = np.argmin(np.abs(frames - n))
    a, b, c = kv_bytes(tok_A[i]), kv_bytes(tok_B[i]), kv_bytes(tok_C[i])
    print(f"{n:>8,} | {fmt(a):>12} | {fmt(b):>12} | {fmt(c):>12} | {a/c:>10,.0f}x")
print("-" * 78)
print("结论：A 的账单随里程无限涨（首帧锚定 + 全量 KV 的死穴）；")
print("      B 把斜率砍到 γ（12.5% 时重建指标几乎不降：Chamfer 0.026→0.029，加速 2/4/8x）；")
print("      C 用 log/sqrt 池让账本近乎封顶 —— 这就是'无距离上限'的数学前提。")

# ---- 后端节奏仿真：每 10 关键帧一次全注意力精化 + KV 写回 ----
N_KF = 1000
backend_ticks = np.arange(0, N_KF + 1, 10)   # bn_every=10
print()
print(f"后端节奏（bn_every=10）：{N_KF} 关键帧触发 {len(backend_ticks)-1} 次全局精化，")
print(f"每次对全部 {N_KF} 帧 map tokens 做一次全注意力前向（等价回环检测+位姿图优化），")
print(f"精化后 KV 写回前端（cache sharing）→ 前端在干净账本上继续增量跟踪。")

# ---- 彩色图 ----
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.patch.set_facecolor("#FFFDF5")

ax = axes[0]
ax.set_facecolor("#FFFDF5")
ax.plot(frames, tok_A, color="#E63946", lw=3, label="A 不剪枝（线性涨）")
ax.plot(frames, tok_B, color="#F77F00", lw=3, label=f"B 恒定保留率 γ={GAMMA}")
ax.plot(frames, tok_C, color="#2A9D8F", lw=3, label="C 动态 log 池（近乎封顶）")
ax.axvline(12000, color="#6C757D", ls="--", lw=1)
ax.text(12000, tok_A.max()*0.55, " 17km 序列\n ≈1.2万帧", fontsize=11, color="#495057")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("序列帧数（对数轴）", fontsize=12)
ax.set_ylabel("累计保留 token 数", fontsize=12)
ax.set_title("KV 账本：三种保留策略", fontsize=15, fontweight="bold", color="#D62828")
ax.legend(fontsize=11); ax.grid(alpha=.3, ls=":")

ax = axes[1]
ax.set_facecolor("#FFFDF5")
ax.step(backend_ticks, np.arange(len(backend_ticks)), where="post",
        color="#1D3557", lw=2.5)
ax.fill_between(backend_ticks, 0, np.arange(len(backend_ticks)), step="post",
                color="#A8DADC", alpha=.6)
for t, lab in [(0, "全局精化\n+KV写回"), (500, "…每 10 关键帧重复…"), (1000, "全局精化\n+KV写回")]:
    ax.annotate(lab, (t, backend_ticks.searchsorted(t) if t else 1),
                fontsize=11, color="#1D3557", fontweight="bold", xytext=(6, 6),
                textcoords="offset points")
ax.set_xlabel("关键帧序号", fontsize=12)
ax.set_ylabel("全局精化次数", fontsize=12)
ax.set_title("后端节奏：每 10 关键帧一次全注意力精化", fontsize=15,
             fontweight="bold", color="#1D3557")
ax.grid(alpha=.3, ls=":")

plt.suptitle("SLAMFormer-∞ 为什么敢说'无距离上限'——内存账本仿真",
             fontsize=16, fontweight="bold", color="#E63946")
plt.tight_layout(rect=[0, 0, 1, 0.93])
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kv_ledger_sim.png")
plt.savefig(out, dpi=150)
print(f"\n图已保存: {out}")
