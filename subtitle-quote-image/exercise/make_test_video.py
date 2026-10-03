# -*- coding: utf-8 -*-
"""自制带烧录字幕的测试视频（避免版权问题，全部自绘）：
Pillow 画 40 帧画面（含底部中文字幕）→ imageio-ffmpeg 编码成 40 秒 mp4。
对应 native-subtitle-quote-image 的原生字幕模式素材要求（字幕已烧进像素）。
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FRAMES_DIR = os.path.join(OUT_DIR, "frames")
VIDEO = os.path.join(OUT_DIR, "demo_native_subtitle.mp4")

W, H = 1280, 720
FPS = 1
DURATION_S = 40

FONT = "C:/Windows/Fonts/msyh.ttc"

# 模拟一段"金句访谈"：每 8 秒一句字幕，每句在一个新时间点完整出现
QUOTES = [
    (2,  "AI 已经比我会做抖音了"),
    (10, "平均每个视频赞藏一千"),
    (18, "还是那个 skill 升级到 2.0"),
    (26, "精确取帧不重绘字幕"),
    (34, "一句话就能出社交长图"),
]

os.makedirs(FRAMES_DIR, exist_ok=True)
font_sub = ImageFont.truetype(FONT, 44)
font_title = ImageFont.truetype(FONT, 64)

for t in range(DURATION_S):
    img = Image.new("RGB", (W, H), (24, 32, 58))
    draw = ImageDraw.Draw(img)
    # 背景渐变
    for y in range(H):
        r = 24 + int(60 * y / H)
        g = 32 + int(80 * y / H)
        b = 58 + int(90 * y / H)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    # 模拟人物主体（椭圆 + 标题）
    draw.ellipse([W // 2 - 120, 120, W // 2 + 120, 360], fill=(245, 183, 49))
    draw.text((W // 2, 430), "程意 demo", font=font_title, fill=(255, 255, 255), anchor="mm")
    # 底部烧录字幕（像素级，无法关闭）
    current = [q for q in QUOTES if q[0] <= t]
    if current:
        _, text = current[-1]
        bw, bh = 1180, 90
        bx, by = (W - bw) // 2, int(H * 0.82)
        draw.rectangle([bx, by, bx + bw, by + bh], fill=(0, 0, 0))
        draw.text((W // 2, by + bh // 2), text, font=font_sub,
                  fill=(255, 255, 255), anchor="mm")
    img.save(os.path.join(FRAMES_DIR, f"frame_{t:03d}.png"))

import imageio_ffmpeg
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
cmd = [ffmpeg, "-y", "-framerate", str(FPS), "-i",
       os.path.join(FRAMES_DIR, "frame_%03d.png"),
       "-c:v", "libx264", "-pix_fmt", "yuv420p", VIDEO]
print("RUN:", " ".join(cmd))
subprocess.run(cmd, check=True)
print("OK:", VIDEO, os.path.getsize(VIDEO), "bytes")
print("字幕句与时间点:", QUOTES)
