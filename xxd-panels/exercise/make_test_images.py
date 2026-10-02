# -*- coding: utf-8 -*-
"""实验材料生成器：造一张 3:4 '仿真照片' 和一张同尺寸'设计图'，
用于跑通 xxd-panel 的 compose_panel.py 排版与审计。"""
from PIL import Image, ImageDraw
import math, random

random.seed(116)

# --- 仿真照片：暖色日落海边，1536x2048 (3:4) ---
W, H = 1536, 2048
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)
for y in range(H):  # 天空->海面渐变
    if y < H * 0.62:
        t = y / (H * 0.62)
        r, g, b = int(255 - 40 * t), int(190 - 90 * t), int(120 - 40 * t)
    else:
        t = (y - H * 0.62) / (H * 0.38)
        r, g, b = int(70 + 30 * t), int(120 + 20 * t), int(150 + 30 * t)
    d.line([(0, y), (W, y)], fill=(r, g, b))
d.ellipse([W * 0.62, H * 0.18, W * 0.78, H * 0.30], fill=(255, 236, 180))  # 太阳
for i in range(24):  # 海面波光
    y = int(H * 0.65 + i * 28)
    x = int(W * 0.55 + random.randint(-60, 60))
    d.line([(x, y), (x + random.randint(80, 300), y)], fill=(255, 220, 170), width=3)
d.polygon([(W*0.28, H*0.62), (W*0.33, H*0.50), (W*0.38, H*0.62)], fill=(60, 50, 70))  # 帆
d.polygon([(W*0.30, H*0.62), (W*0.44, H*0.62), (W*0.40, H*0.66), (W*0.32, H*0.66)], fill=(90, 40, 40))
img.save("photo.jpg", quality=92)

# --- 设计图：同尺寸"粉彩蜡笔涂鸦风"（程序近似，仅作占位材料） ---
design = Image.new("RGB", (W, H), (250, 247, 240))
dd = ImageDraw.Draw(design)
coral, sky, mint = (240, 128, 110), (110, 160, 210), (120, 190, 160)
dd.arc([W*0.30, H*0.30, W*0.70, H*0.55], 200, 340, fill=(240, 200, 120), width=14)  # 太阳弧线
dd.ellipse([W*0.56, H*0.32, W*0.66, H*0.40], outline=coral, width=10)
dd.line([(W*0.25, H*0.60), (W*0.75, H*0.60)], fill=mint, width=8)  # 海平线
dd.polygon([(W*0.36, H*0.60), (W*0.40, H*0.50), (W*0.44, H*0.60)], outline=sky, width=8)  # 帆
dd.ellipse([W*0.34, H*0.615, W*0.47, H*0.65], outline=coral, width=8)  # 船身
for i in range(6):  # 涂鸦小星星
    x, y = random.randint(100, W - 100), random.randint(120, int(H * 0.28))
    r = random.randint(10, 22)
    dd.regular_polygon((x, y, r), 5, rotation=random.randint(0, 72), outline=coral, width=5)
dd.text((W*0.30, H*0.72), "SUNSET / 116", fill=(90, 80, 90))
design.save("design.png")

# --- 故意做一张 45:55 的错位拼接图，用来演示 audit 的检测能力 ---
bad = Image.new("RGB", (W, H))
bad.paste(img.crop((0, 0, W, int(H * 0.45))), (0, 0))
bad.paste(design.crop((0, 0, W, H - int(H * 0.45))), (0, int(H * 0.45)))
bad.save("bad-split.png")

print("photo.jpg", img.size, " design.png", design.size, " bad-split.png", bad.size)
