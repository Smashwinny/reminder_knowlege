"""把实验2录制的 trace_*.npy 轨迹画成对比图（PNG），供 PDF 插图使用。"""

import glob

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

fig, ax = plt.subplots(figsize=(9, 5))
colors = {"linear": "#888888", "minjerk": "#00A8E8", "ease_in_out": "#FF6B35", "cartoon": "#E63946"}

for f in sorted(glob.glob("trace_*.npy")):
    method = f.replace("trace_", "").replace(".npy", "")
    z = np.load(f)
    t = np.arange(len(z)) * 0.01
    ax.plot(t, z, label=method, color=colors.get(method, None), linewidth=2)

ax.axhline(20, color="green", linestyle="--", linewidth=1, label="目标 z=20mm")
ax.set_xlabel("时间 (s)")
ax.set_ylabel("头部 z 位置 (mm)")
ax.set_title("实验2：四种插值方法的真实运动轨迹（100Hz 采样自 MuJoCo 仿真）")
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("exp2_traces.png", dpi=150)
print("[OK] 已生成 exp2_traces.png")
