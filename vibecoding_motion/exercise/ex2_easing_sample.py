# ex2 缓动函数采样验证：用数字证明"性格差异"，并生成 SVG 曲线图（零依赖）
import math

def linear(t): return t
def ease_out_cubic(t): return 1 - (1 - t) ** 3
def ease_in_out_cubic(t):
    return 4*t*t*t if t < 0.5 else 1 - (-2*t + 2) ** 3 / 2
def ease_out_back(t, s=1.70158):
    return 1 + (s+1)*(t-1)**3 + s*(t-1)**2

FUNCS = {"linear": linear, "easeOutCubic": ease_out_cubic,
         "easeInOutCubic": ease_in_out_cubic, "easeOutBack": ease_out_back}

# 1) 关键采样点表
print(f"{'t':>5} | " + " | ".join(f"{n:>14}" for n in FUNCS))
for t in [0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0]:
    print(f"{t:>5} | " + " | ".join(f"{FUNCS[n](t):>14.3f}" for n in FUNCS))

# 2) 结论验证：easeOutCubic 用 30% 的时间走完多少路程？
v = ease_out_cubic(0.3)
print(f"\n[验证] easeOutCubic 在 t=0.30 时路程 = {v:.3f}（>0.6 即'前30%时间走完60%路'成立）")
assert v > 0.6
v2 = ease_out_back(1.1)  # t>1 没意义，检查过冲：在 [0,1] 内最大值
peak = max(ease_out_back(t/1000) for t in range(1001))
print(f"[验证] easeOutBack 峰值 = {peak:.3f}（>1.0 即存在过冲回弹）")
assert peak > 1.0

# 3) 生成 4 条曲线的对比 SVG（供 PDF 引用）
W, H = 760, 420
paths, labels = [], []
colors = ["#9AA3AF", "#FF3D3D", "#00A3FF", "#7C3AED"]
for (name, fn), color in zip(FUNCS.items(), colors):
    pts = []
    for i in range(101):
        t = i / 100
        x = 60 + t * 640
        y = 370 - fn(t) * 300          # y 翻转：值 1 在上
        pts.append(f"{x:.1f},{y:.1f}")
    paths.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>')
    labels.append(f'<text x="90" y="{60 + len(labels)*30}" fill="{color}" font-size="20" font-weight="bold">{name}（峰值 {max(fn(i/1000) for i in range(1001)):.2f}）</text>')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="sans-serif">
<rect width="{W}" height="{H}" fill="#FFF8F0"/>
<line x1="60" y1="370" x2="700" y2="370" stroke="#333" stroke-width="2"/>
<line x1="60" y1="370" x2="60" y2="40" stroke="#333" stroke-width="2"/>
<line x1="60" y1="70" x2="700" y2="70" stroke="#888" stroke-dasharray="6 5" stroke-width="1"/>
<text x="668" y="62" fill="#888" font-size="14">值=1.0</text>
<text x="640" y="392" fill="#333" font-size="14">时间 t 0.0 → 1.0</text>
{''.join(paths)}{''.join(labels)}
</svg>'''
open("ex2_curves.svg", "w", encoding="utf-8").write(svg)
print("[OK] ex2_curves.svg 已生成")
