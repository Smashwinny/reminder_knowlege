# analyze_ab.py — A/B 截图像素级分析：像素化(480x270 RT+最近邻) vs 直接渲染(960x540)
# 指标：1) 两图均非零差异（证明后处理真的改变了渲染） 2) 像素化版"块状度"更高
# 块状度 = 水平相邻像素相等的比例（大色块内部相邻相等的概率远高于高清渐变边缘）
import sys
from PIL import Image
import numpy as np

a = np.asarray(Image.open(sys.argv[1]).convert('RGB'), dtype=np.int16)   # pixel on
b = np.asarray(Image.open(sys.argv[2]).convert('RGB'), dtype=np.int16)   # pixel off
h = min(a.shape[0], b.shape[0]); w = min(a.shape[1], b.shape[1])
a, b = a[:h, :w], b[:h, :w]

diff = np.abs(a - b).mean()
print(f"mean_abs_diff={diff:.2f}")
print("AB_DIFF_NONZERO" if diff > 1.0 else "AB_DIFF_ZERO")

def blockiness(img):
    eq = (np.diff(img, axis=1) == 0).all(axis=2)   # 水平相邻全通道相等
    return eq.mean()

ba, bb = blockiness(a), blockiness(b)
print(f"blockiness_pixel={ba:.4f} blockiness_direct={bb:.4f}")
print("PIXEL_BLOCKIER" if ba > bb else "PIXEL_NOT_BLOCKIER")

ua, ub = len(np.unique(a.reshape(-1, 3), axis=0)), len(np.unique(b.reshape(-1, 3), axis=0))
print(f"unique_colors_pixel={ua} unique_colors_direct={ub}")
