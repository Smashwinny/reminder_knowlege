# -*- coding: utf-8 -*-
"""实验1/实验3 材料：用 Pillow 自绘 RuiC-card-skill 的四层图。
确定性(固定随机种子)，1024x1536 同一画布：
  assets/background.png  不透明星空夜潜背景
  assets/subject.png     锦鲤主体，真 RGBA 透明
  assets/lineart.png     深色线稿绘于白底(与主体同一套形状，保证轮廓对位)
  assets/text.png        卡框+标题文字，真 RGBA 透明
用法: python make_layers.py <输出项目根>
"""
import sys, math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1536
random.seed(42)

# ---------- 形状定义（主体与线稿共用同一套形状 => 轮廓精确对位） ----------
def koi_shapes():
    """返回主体图形的绘制指令列表 (kind, args)。"""
    s = []
    # 尾鳍（大展开三叉）
    s.append(('poly', [(640, 700), (900, 560), (830, 730), (920, 860), (660, 880)]))
    # 身体
    s.append(('ell', (300, 640, 700, 930)))
    # 背鳍
    s.append(('poly', [(420, 660), (560, 560), (600, 690)]))
    # 胸鳍
    s.append(('poly', [(380, 880), (300, 1010), (470, 930)]))
    # 腹鳍
    s.append(('poly', [(560, 900), (560, 1030), (660, 910)]))
    return s

def draw_koi_mask(size=(W, H), angle=-12):
    m = Image.new('L', size, 0)
    d = ImageDraw.Draw(m)
    for kind, a in koi_shapes():
        if kind == 'ell':
            d.ellipse(a, fill=255)
        else:
            d.polygon(a, fill=255)
    return m.rotate(angle, resample=Image.BICUBIC, center=(512, 780))

# ---------- 背景：星夜深潭 ----------
def make_background():
    img = Image.new('RGB', (W, H))
    px = img.load()
    top = (13, 18, 58); mid = (24, 46, 96); bot = (10, 44, 74)
    for y in range(H):
        t = y / (H - 1)
        if t < 0.55:
            k = t / 0.55
            c = tuple(int(top[i] + (mid[i] - top[i]) * k) for i in range(3))
        else:
            k = (t - 0.55) / 0.45
            c = tuple(int(mid[i] + (bot[i] - mid[i]) * k) for i in range(3))
        for x in range(W):
            px[x, y] = c
    d = ImageDraw.Draw(img, 'RGBA')
    # 月亮 + 光晕
    for r, a in [(150, 22), (110, 34), (72, 66)]:
        d.ellipse((800 - r, 260 - r, 800 + r, 260 + r), fill=(255, 244, 200, a))
    d.ellipse((800 - 52, 260 - 52, 800 + 52, 260 + 52), fill=(255, 246, 214, 255))
    # 星星
    for _ in range(260):
        x, y = random.randint(0, W - 1), random.randint(0, 900)
        r = random.choice([1, 1, 1, 2, 2, 3])
        b = random.randint(120, 255)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 230, b))
    # 水波涟漪
    for _ in range(9):
        y = random.randint(950, 1500)
        x = random.randint(60, 700)
        w = random.randint(90, 260)
        d.arc((x, y, x + w, y + 46), 200, 340, fill=(180, 220, 255, 60), width=3)
    return img

# ---------- 主体：白底橙斑锦鲤（真 alpha） ----------
def make_subject():
    mask = draw_koi_mask()
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, H), fill=(245, 243, 238, 255))  # 先铺白底再抠
    # 橙红斑块
    rng = random.Random(7)
    for _ in range(7):
        cx, cy = rng.randint(340, 660), rng.randint(680, 900)
        rx, ry = rng.randint(50, 110), rng.randint(36, 80)
        d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(232, 90, 40, 255))
    d.ellipse((380, 700, 520, 820), fill=(232, 90, 40, 255))
    # 头部留白 + 眼睛
    d.ellipse((330, 730, 400, 800), fill=(30, 26, 24, 255))
    img.putalpha(mask)
    return img

# ---------- 线稿：同一套形状的深色轮廓，绘于白底 ----------
def make_lineart():
    m = Image.new('RGB', (W, H), (255, 255, 255))
    d = ImageDraw.Draw(m)
    for kind, a in koi_shapes():
        if kind == 'ell':
            d.ellipse(a, outline=(45, 38, 34), width=9)
        else:
            d.line(list(a) + [a[0]], fill=(45, 38, 34), width=9, joint='curve')
    # 细节：鳃线、鳞弧
    d.arc((430, 690, 590, 880), 60, 300, fill=(45, 38, 34), width=5)
    for i in range(5):
        d.arc((420 + i * 46, 700, 560 + i * 46, 900), 200, 340, fill=(70, 60, 55), width=4)
    return m.rotate(-12, resample=Image.BICUBIC, center=(512, 780), fillcolor=(255, 255, 255))

# ---------- 文字层：卡框 + 排版（真 alpha，网页不做视差，钉在卡边） ----------
def font(sz, bold=False):
    name = 'msyhbd.ttc' if bold else 'msyh.ttc'
    return ImageFont.truetype(C('C:/Windows/Fonts/' + name), sz)

def make_text():
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # 双线卡框
    d.rectangle((28, 28, W - 29, H - 29), outline=(212, 175, 96, 255), width=10)
    d.rectangle((52, 52, W - 53, H - 53), outline=(212, 175, 96, 200), width=4)
    # 标题
    d.text((80, 120), '锦鲤如意', font=font(120, True), fill=(255, 250, 235, 255),
           stroke_width=6, stroke_fill=(60, 34, 16, 255))
    d.text((84, 270), 'KOI OF FORTUNE', font=font(40), fill=(255, 244, 214, 230))
    # 右上编号
    d.text((W - 320, 92), 'No.001', font=font(56, True), fill=(255, 226, 150, 255))
    # 底部说明
    d.text((80, H - 210), '招式 · 鱼跃龙门', font=font(52, True), fill=(255, 248, 228, 255))
    d.text((80, H - 140), '星夜深潭，一跃而过。', font=font(36), fill=(235, 240, 250, 235))
    # 稀有度徽标
    d.rounded_rectangle((W - 300, H - 220, W - 90, H - 140), 20,
                        fill=(212, 175, 96, 235))
    d.text((W - 272, H - 204), '传说 SSR', font=font(44, True), fill=(60, 34, 16, 255))
    return img

def C(p): return p  # 占位保持结构

def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('card')
    (root / 'assets').mkdir(parents=True, exist_ok=True)
    make_background().save(root / 'assets' / 'background.png')
    make_subject().save(root / 'assets' / 'subject.png')
    make_lineart().save(root / 'assets' / 'lineart.png')
    make_text().save(root / 'assets' / 'text.png')
    print('layers written to', (root / 'assets').resolve())

if __name__ == '__main__':
    main()
