#!/usr/bin/env python3
"""make_atlas.py — 模拟一张 AI 生成的 2x2 贴图集（asset kit），供 grid_slice.py 切片实验。

SKILL.md 里的真实用法：让图像模型把多个道具画进一张 1K 大图（省钱），
再用 tools/grid_slice.py --grid 2x2 切成单个 sprite。
这里用 Pillow 画一张 1024x1024 的四色"道具集"模拟该产物。
"""
from PIL import Image, ImageDraw

CELLS = [("sword", (220, 40, 40)), ("shield", (40, 90, 220)),
         ("potion", (40, 180, 90)), ("helm", (240, 180, 30))]

img = Image.new("RGB", (1024, 1024), (245, 245, 240))
d = ImageDraw.Draw(img)
for i, (name, color) in enumerate(CELLS):
    row, col = divmod(i, 2)
    x0, y0 = col * 512, row * 512
    d.rectangle([x0 + 32, y0 + 32, x0 + 480, y0 + 480], fill=color, outline=(30, 30, 30), width=8)
    d.text((x0 + 60, y0 + 60), name, fill=(255, 255, 255))

img.save("atlas.png")
print("saved atlas.png 1024x1024 (2x2 kit: sword/shield/potion/helm)")
