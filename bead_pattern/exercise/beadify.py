# -*- coding: utf-8 -*-
"""拼豆图纸生成器 —— 照片 → 拼豆像素图纸（纯 Python 标准库）。

算法管线（对应指南 Q4）：
  1. 解析 24 位无压缩 BMP（BITMAPINFOHEADER，自底向上行，4 字节对齐）
  2. 盒式降采样（box filter）到 W×H 豆格：每格取区域平均色
  3. 固定豆色调色板最近色量化（RGB 欧氏距离；感知改进见指南 Q8）
  4. 输出彩色 HTML 图纸（色块网格 + 图例 + 用量统计）与 CSV 用量表

用法：
    python beadify.py <photo.bmp> --width 48 --out pattern.html
    python beadify.py --self-test
"""
import argparse
import csv
import html
import struct
import sys
from collections import Counter
from pathlib import Path

# 24 色入门豆色调色板（近似常见拼豆品牌通用色；实际品牌色卡有 60+ 色）
PALETTE = [
    ("K",  "黑",   0x18, 0x18, 0x18), ("W",  "白",   0xF8, 0xF8, 0xF8),
    ("GY", "中灰", 0x80, 0x80, 0x80), ("LG", "浅灰", 0xC8, 0xC8, 0xC8),
    ("DGY","深灰", 0x40, 0x40, 0x40), ("R",  "红",   0xD0, 0x20, 0x20),
    ("DR", "暗红", 0x88, 0x14, 0x14), ("O",  "橙",   0xF0, 0x80, 0x18),
    ("Y",  "黄",   0xF8, 0xD8, 0x18), ("CR", "米白", 0xF0, 0xE8, 0xD0),
    ("BN", "棕",   0x78, 0x50, 0x30), ("LB", "浅棕", 0xB0, 0x88, 0x58),
    ("TN", "肤色", 0xE8, 0xC0, 0xA0), ("P",  "粉",   0xF0, 0xA8, 0xC0),
    ("HP", "品红", 0xE0, 0x40, 0x90), ("PU", "紫",   0x88, 0x40, 0xA8),
    ("DB", "深蓝", 0x20, 0x38, 0x88), ("B",  "蓝",   0x30, 0x70, 0xD0),
    ("LBU","浅蓝", 0x90, 0xC0, 0xF0), ("T",  "青",   0x20, 0xA8, 0xA8),
    ("G",  "绿",   0x28, 0x90, 0x38), ("LG2","浅绿", 0x88, 0xC8, 0x70),
    ("LM", "黄绿", 0xB8, 0xD8, 0x30), ("BG", "米色", 0xE8, 0xD8, 0xB0),
]


PALETTE_MAP = {p[0]: (p[1], p[2:5]) for p in PALETTE}


def read_bmp24(path):
    """返回 (width, height, pixels)；pixels[y][x] = (r, g, b)，y 自顶向下。"""
    data = Path(path).read_bytes()
    if data[:2] != b"BM":
        raise ValueError("不是 BMP 文件")
    pixel_offset = struct.unpack_from("<I", data, 10)[0]
    header_size = struct.unpack_from("<I", data, 14)[0]
    if header_size < 40:
        raise ValueError("只支持 BITMAPINFOHEADER 及以后")
    width = struct.unpack_from("<i", data, 18)[0]
    height = struct.unpack_from("<i", data, 22)[0]
    planes, bpp = struct.unpack_from("<HH", data, 26)
    compression = struct.unpack_from("<I", data, 30)[0]
    if bpp != 24 or compression != 0:
        raise ValueError(f"只支持 24 位无压缩 BMP（实际 {bpp}bpp, compression={compression}）")
    bottom_up = height > 0
    height = abs(height)
    row_size = (width * 3 + 3) & ~3
    pixels = []
    for y in range(height):
        src_y = height - 1 - y if bottom_up else y
        base = pixel_offset + src_y * row_size
        row = []
        for x in range(width):
            b, g, r = data[base + x * 3: base + x * 3 + 3]
            row.append((r, g, b))
        pixels.append(row)
    return width, height, pixels


def downsample(pixels, W, H):
    """盒式滤波降采样到 W×H。"""
    src_h, src_w = len(pixels), len(pixels[0])
    grid = []
    for gy in range(H):
        y0, y1 = gy * src_h // H, (gy + 1) * src_h // H
        row = []
        for gx in range(W):
            x0, x1 = gx * src_w // W, (gx + 1) * src_w // W
            n = (y1 - y0) * (x1 - x0)
            r = sum(pixels[y][x][0] for y in range(y0, y1) for x in range(x0, x1)) // n
            g = sum(pixels[y][x][1] for y in range(y0, y1) for x in range(x0, x1)) // n
            b = sum(pixels[y][x][2] for y in range(y0, y1) for x in range(x0, x1)) // n
            row.append((r, g, b))
        grid.append(row)
    return grid


def nearest_bead(rgb):
    r, g, b = rgb
    best, best_d = None, 1 << 62
    for sym, name, pr, pg, pb in PALETTE:
        d = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
        if d < best_d:
            best, best_d = (sym, name, (pr, pg, pb)), d
    return best


def quantize(grid):
    return [[nearest_bead(px) for px in row] for row in grid]


def render_html(beads, out_path, title):
    H, W = len(beads), len(beads[0])
    counts = Counter(sym for row in beads for sym, _, _ in row)
    cells = []
    for row in beads:
        for sym, _, (r, g, b) in row:
            fg = "#000" if (r * 299 + g * 587 + b * 114) // 1000 > 140 else "#fff"
            cells.append(f'<td style="background:rgb({r},{g},{b});color:{fg}">{sym}</td>')
    legend = "".join(
        f'<tr><td style="background:rgb({PALETTE_MAP[sym][1][0]},{PALETTE_MAP[sym][1][1]},{PALETTE_MAP[sym][1][2]})">&nbsp;</td>'
        f'<td><b>{sym}</b> {PALETTE_MAP[sym][0]}</td><td>{n} 颗（{n*100/(W*H):.1f}%）</td></tr>'
        for sym, n in counts.most_common())
    Path(out_path).write_text(f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<title>{html.escape(title)}</title><style>
body{{font-family:"Microsoft YaHei";margin:24px;background:#fff8f0}}
h1{{color:#ea580c;font-size:1.4em}}
table.grid{{border-collapse:collapse;margin:16px 0}}
table.grid td{{border:1px solid #999;width:15px;height:15px;text-align:center;
font-size:7px;font-weight:bold;padding:0}}
table.legend{{border-collapse:collapse;background:#fff}}
table.legend td{{border:1px solid #ddd;padding:4px 10px}}</style></head><body>
<h1>{html.escape(title)}</h1>
<p>尺寸：{W}×{H} = <b>{W*H}</b> 颗豆；使用 {len(counts)} 种颜色。
每格符号 = 对应色号；打印后按格铺豆、覆纸熨烫。</p>
<table class="grid">{''.join('<tr>'+''.join(cells[y*W:(y+1)*W])+'</tr>' for y in range(H))}</table>
<h2>色号与用量</h2><table class="legend"><tr><th>色</th><th>代号</th><th>用量</th></tr>{legend}</table>
</body></html>""", encoding="utf-8")
    return counts


def cmd_convert(args):
    w, h, pixels = read_bmp24(args.bmp)
    H = args.height or max(1, round(args.width * h / w))
    print(f"源图：{w}×{h} → 豆格：{args.width}×{H}（共 {args.width*H} 颗）")
    grid = downsample(pixels, args.width, H)
    beads = quantize(grid)
    counts = render_html(beads, args.out, Path(args.out).stem)
    csv_path = Path(args.out).with_suffix(".csv")
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["代号", "颜色", "用量(颗)"])
        for sym, n in counts.most_common():
            wr.writerow([sym, PALETTE_MAP[sym][0], n])
    print(f"图纸：{args.out}")
    print(f"用量表：{csv_path}")
    print(f"用色 {len(counts)} 种，前 5：", counts.most_common(5))


def cmd_self_test(_):
    # T1 最近色匹配：纯红 → R
    sym, name, _ = nearest_bead((210, 30, 30))
    assert sym == "R", sym
    # T2 近白 → W
    assert nearest_bead((250, 250, 250))[0] == "W"
    # T3 盒式降采样 4×4 → 2×2 平均值
    px = [[(0, 0, 0)] * 4, [(0, 0, 0)] * 4, [(255, 255, 255)] * 4, [(255, 255, 255)] * 4]
    g = downsample(px, 2, 2)
    assert g[0] == [(0, 0, 0), (0, 0, 0)] and g[1] == [(255, 255, 255), (255, 255, 255)], g
    # T4 降采样不丢尺寸
    g = downsample([[(1, 2, 3)] * 30 for _ in range(30)], 7, 7)
    assert len(g) == 7 and len(g[0]) == 7
    print("self-test: 4/4 通过（最近色×2、盒式均值、尺寸保持）")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd")
    c = sub.add_parser("convert")
    c.add_argument("bmp")
    c.add_argument("--width", type=int, default=48)
    c.add_argument("--height", type=int, default=None)
    c.add_argument("--out", required=True)
    sub.add_parser("self-test")
    args = p.parse_args()
    if args.cmd == "self-test":
        cmd_self_test(args)
    else:
        cmd_convert(args)


if __name__ == "__main__":
    main()
