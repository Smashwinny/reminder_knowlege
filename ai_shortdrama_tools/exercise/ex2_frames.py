# -*- coding: utf-8 -*-
"""
实验步骤2：逐帧配图 + 烧字幕（对标 produce_assets 阶段的图像环节 + 帧模板合成）
真实项目里配图由 ComfyUI 工作流 / 直连 API（DashScope、Seedream 等）生成，
再套 HTML 模板（templates/1080x1920/default.html）渲染合成帧；
本实验用 PIL 画"渐变底 + 主题字 + 底部字幕"离线复刻，竖屏 1080x1920。
运行：python ex2_frames.py
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

EX = Path(__file__).parent
OUT = EX / "output"
W, H = 1080, 1920  # 与上游 StoryboardConfig 默认帧模板 1080x1920 同尺寸

# 每帧一个强调色（模拟多模板/风格切换）
ACCENTS = ["#FF4757", "#1E90FF", "#2ED573", "#FFA502", "#B14AE2"]
FONT_TITLE = "C:/Windows/Fonts/msyhbd.ttc"   # 微软雅黑 Bold
FONT_SUB = "C:/Windows/Fonts/msyh.ttc"


def grad_image(c1, c2):
    """竖向双色渐变底图（占位 AI 配图）"""
    r1, g1, b1 = tuple(int(c1[i:i + 2], 16) for i in (1, 3, 5))
    r2, g2, b2 = tuple(int(c2[i:i + 2], 16) for i in (1, 3, 5))
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        color = (int(r1 + (r2 - r1) * t), int(g1 + (g2 - g1) * t), int(b1 + (b2 - b1) * t))
        for x in range(0, W, 4):
            for dx in range(4):
                if x + dx < W:
                    px[x + dx, y] = color
    return img


def main():
    sb_path = OUT / "storyboard.json"
    data = json.loads(sb_path.read_text(encoding="utf-8"))

    for fr in data["frames"]:
        i = fr["index"]
        accent = ACCENTS[i % len(ACCENTS)]
        img = grad_image("#10102A", accent)
        d = ImageDraw.Draw(img)

        # 顶部主题大字（占位"模板标题区"）
        f_title = ImageFont.truetype(FONT_TITLE, 88)
        title = f"帧 {i + 1}"
        tw = d.textlength(title, font=f_title)
        d.text(((W - tw) / 2, 160), title, font=f_title, fill="white")

        # 底部字幕条（真实项目烧在 composed_image_path，这里直接画进底图）
        f_sub = ImageFont.truetype(FONT_SUB, 52)
        y = H - 420
        for line in wrap(fr["narration"], f_sub, d, W - 160):
            lw = d.textlength(line, font=f_sub)
            d.text(((W - lw) / 2, y), line, font=f_sub, fill="white")
            y += 78

        # 图像提示词小字（演示 image_prompt 与画面的对应）
        f_hint = ImageFont.truetype(FONT_SUB, 34)
        hint = fr["image_prompt"][:52]
        hw = d.textlength(hint, font=f_hint)
        d.text(((W - hw) / 2, H - 180), hint, font=f_hint, fill=(255, 255, 255, 200))

        p = OUT / f"frame_{i}.png"
        img.save(p)
        fr["image_path"] = str(p)

    sb_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    for fr in data["frames"]:
        print(f"[ex2] 帧{fr['index']} -> {Path(fr['image_path']).name} ({W}x{H})")

    # 验证：文件存在且尺寸正确
    for fr in data["frames"]:
        with Image.open(fr["image_path"]) as im:
            assert im.size == (W, H), im.size
    print(f"[ex2] PASS: {len(data['frames'])} 张 1080x1920 配图生成")
    return 0


def wrap(text, font, draw, max_w):
    lines, cur = [], ""
    for ch in text:
        if draw.textlength(cur + ch, font=font) > max_w:
            lines.append(cur)
            cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return lines


if __name__ == "__main__":
    sys.exit(main())
