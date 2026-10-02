# -*- coding: utf-8 -*-
"""
ex4 主实验：商品慢扫光动态广告 —— "1 张底图 + Python 程序化光带"管线真跑通
来源：Adrian Punk《Image2.5 玩法全公开》电商玩法#1。
文章核心工程结论：让模型直接生成 6/10 帧分镜再拼 GIF 会抖（每帧都是重绘，几何不一致）；
改成"1 张商品底图从头到尾像素复用 + 只叠加一条 softbox 高斯亮度光带"，
从构造上保证 瓶身不动、Logo 不动、文字不动。
诚实声明：本机无图像模型 API key，"多帧重绘抖动"失败模式用确定性仿射抖动模拟演示
（仅演示量级，非真实模型输出）；管线本身全部真实运行。
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W = H = 800
SS = 4  # 超采样倍率，抗锯齿
FONT_DIR = "C:/Windows/Fonts"

# ---------- 第 1 步：合成一张"商品底图"（模拟模型生成的商品照，只生成这一次） ----------
def build_base():
    img = Image.new("RGB", (W * SS, H * SS), (244, 240, 234))
    d = ImageDraw.Draw(img)
    # 摄影棚背景：上亮下暗的柔和渐变 + 台面阴影
    for y in range(H * SS):
        t = y / (H * SS)
        r = int(244 - 26 * t); g = int(240 - 24 * t); b = int(234 - 22 * t)
        d.line([(0, y), (W * SS, y)], fill=(r, g, b))
    d.ellipse([90 * SS, 560 * SS, 310 * SS, 610 * SS], fill=(210, 202, 192))  # 台面软阴影
    # 瓶身（琥珀色玻璃瓶）
    d.rounded_rectangle([120 * SS, 180 * SS, 280 * SS, 580 * SS], radius=34 * SS,
                        fill=(196, 138, 58), outline=(150, 100, 38), width=3 * SS)
    d.rounded_rectangle([140 * SS, 200 * SS, 200 * SS, 560 * SS], radius=22 * SS,
                        fill=(214, 164, 84))  # 左侧高光面
    d.rectangle([176 * SS, 120 * SS, 224 * SS, 185 * SS], fill=(178, 122, 52))  # 瓶颈
    d.rounded_rectangle([168 * SS, 80 * SS, 232 * SS, 128 * SS], radius=8 * SS,
                        fill=(60, 52, 48))  # 瓶盖
    # 标签 + Logo + 文字（重点保护对象）
    d.rounded_rectangle([138 * SS, 300 * SS, 262 * SS, 480 * SS], radius=10 * SS,
                        fill=(250, 246, 238))
    d.ellipse([178 * SS, 316 * SS, 222 * SS, 360 * SS], fill=(226, 96, 60))  # Logo 圆点
    try:
        f_big = ImageFont.truetype(FONT_DIR + "/arialbd.ttf", 40 * SS)
        f_sm = ImageFont.truetype(FONT_DIR + "/arial.ttf", 18 * SS)
    except OSError:
        f_big = f_sm = ImageFont.load_default()
    d.text((200 * SS, 372 * SS), "LUMI", font=f_big, fill=(52, 46, 42), anchor="mm")
    d.text((200 * SS, 418 * SS), "AMBER SERUM 30ml", font=f_sm,
           fill=(120, 108, 96), anchor="mm")
    return img.resize((W, H), Image.LANCZOS)

# ---------- 第 2 步：softbox 高斯光带（纯函数叠加，只动亮度/色温，不动几何） ----------
def softbox_frame(base_arr, center_x, band_w=W * 0.28, peak=34.0, warm=0.55):
    xs = np.arange(W, dtype=np.float64)
    sigma = band_w / 4.0  # 光带边缘高斯羽化（softbox 亮度分布）
    prof = np.exp(-0.5 * ((xs - center_x) / sigma) ** 2)          # (W,)
    prof[prof < np.exp(-0.5 * 3.2 ** 2)] = 0.0  # 3.2σ 外硬截止：光带有确定支撑域
    # 坑：叠加向量必须保持 1D(W,) 与 (H,W) 做尾轴广播。
    # 若 reshape 成 (1,W,1) 再加 (H,W)，当 H==W 时会静默广播成 (H,W,W)
    # （800x800 图 = 4GB 临时数组），且每像素错拿 prof[0] 的值。
    r_add, g_add, b_add = peak * prof, peak * prof * 0.92, peak * prof * 0.80
    wg_r = 1.0 + warm * prof                       # 暖色轻微提升（R 增益最大）
    wg_g = 1.0 + (warm - 0.35) * prof * 0.3
    out = base_arr.astype(np.float64).copy()
    out[..., 0] = np.clip(out[..., 0] * wg_r + r_add, 0, 255)  # R 受暖偏+亮度
    out[..., 1] = np.clip(out[..., 1] * wg_g + g_add, 0, 255)
    out[..., 2] = np.clip(out[..., 2] + b_add, 0, 255)         # B 提升最少 -> 偏暖
    return out.astype(np.uint8)

# ---------- 第 3 步：扫光序列（底图像素从头到尾完全复用） ----------
def sweep_frames(base, n=48):
    arr = np.asarray(base)
    lo, hi = -0.25 * W, W + 0.25 * W
    centers = np.linspace(lo, hi, n, endpoint=False)
    return [Image.fromarray(softbox_frame(arr, c)) for c in centers]

# ---------- 第 4 步：验证 ----------
def verify(base, frames, centers_list):
    base_arr = np.asarray(base).astype(np.int16)
    sigma = (W * 0.28) / 4.0
    logo = (138, 300, 262, 480)  # 标签/Logo/文字区域
    lb = base_arr[logo[1]:logo[3], logo[0]:logo[2]]

    # 不变量1：每一帧在光带 3.2σ 支撑域之外与底图逐像素严格一致（几何冻结的构造性证明）
    xs = np.arange(W, dtype=np.float64)
    ok1, worst = 0, 0
    for c, fr_img in zip(centers_list, frames):
        fr = np.asarray(fr_img).astype(np.int16)
        outside = np.abs(xs - c) >= 3.2 * sigma
        d = np.abs(fr[:, outside] - base_arr[:, outside]).max()
        worst = max(worst, d)
        if d == 0:
            ok1 += 1
    print(f"[V1] 48帧光带支撑域外逐像素==底图: {ok1}/48 (最大偏差 {worst}) "
          + ("PASS" if ok1 == 48 and worst == 0 else "FAIL"))

    # 不变量2：光带未触及时的 Logo/文字像素零改动
    ok2, tot2 = 0, 0
    for c in centers_list:
        if c + 3.2 * sigma <= logo[0] or c - 3.2 * sigma >= logo[2]:
            tot2 += 1
            idx = int(round((c - centers_list[0]) / (centers_list[1] - centers_list[0])))
            fr = np.asarray(frames[idx]).astype(np.int16)
            if np.abs(fr[logo[1]:logo[3], logo[0]:logo[2]] - lb).sum() == 0:
                ok2 += 1
    print(f"[V2] Logo/文字区零改动帧: {ok2}/{tot2} " + ("PASS" if ok2 == tot2 and tot2 > 0 else "FAIL"))

    # GIF 回读验证（GIF 为 256 色调色板，有损编码：报告量化偏差的实际量级）
    # 结论口径：几何不变量在合成帧层严格为 0（V1/V2）；GIF 调色板层只引入色差、不动几何
    import io
    pal = frames[0].quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    q_frames = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
    buf = io.BytesIO()
    q_frames[0].save(buf, format="GIF", save_all=True, append_images=q_frames[1:],
                     duration=50, loop=0)
    buf.seek(0)
    g = Image.open(buf)
    n_ok = g.n_frames == len(frames)
    loop_ok = g.info.get("loop") == 0
    f0 = np.asarray(g.convert("RGB")).astype(np.int16)
    dq = np.abs(f0 - np.asarray(frames[0]).astype(np.int16))
    q_max, q_mean = dq.max(), dq.mean()
    print(f"[V3] GIF 回读: n_frames={g.n_frames}=={len(frames)} {n_ok}, loop=0 {loop_ok}, "
          f"首帧量化色差 max={q_max} mean={q_mean:.2f} (mean<=3 {q_mean <= 3})")
    return buf.getvalue()

# ---------- 第 5 步：反例演示（模拟"多帧重绘抖动"，确定性种子，非真实模型输出） ----------
def jitter_fail_demo(base, n=6, seed=7):
    """模拟模型逐帧重绘：每帧给底图一个微小仿射抖动（±3px 平移 + 0.4° 旋转）。"""
    rng = np.random.default_rng(seed)
    out = []
    for i in range(n):
        dx, dy = rng.integers(-3, 4, 2)
        ang = rng.uniform(-0.4, 0.4)
        rot = base.rotate(ang, resample=Image.BICUBIC, translate=(int(dx), int(dy)),
                          fillcolor=(244, 240, 234))
        out.append(rot)
    return out

def jitter_metric(frames, base):
    """瓶身边缘错位量：与底图逐像素平均绝对差（越大越'抖'）。"""
    base_arr = np.asarray(base).astype(np.int16)
    diffs = []
    for fr in frames:
        d = np.abs(np.asarray(fr).astype(np.int16) - base_arr)
        diffs.append(d.mean())
    return diffs

def bottle_edge_x(img, row=None):
    """行扫描：瓶身左边缘的 x 坐标（背景→琥珀色瓶身的第一个突变列）。"""
    row = row or H // 2
    arr = np.asarray(img).astype(np.int16)
    bg = arr[row, 5].astype(np.int16)
    d = np.abs(arr[row] - bg).sum(axis=1)
    return int(np.argmax(d > 60))

if __name__ == "__main__":
    base = build_base()
    base.save("ex4_base.png")
    print(f"[S1] 底图生成 ex4_base.png {base.size}")

    frames = sweep_frames(base)
    centers_list = list(np.linspace(-0.25 * W, W + 0.25 * W, 48, endpoint=False))
    print(f"[S2] softbox 光带: band_w={W*0.28:.0f}px sigma={(W*0.28)/4:.1f}px peak=34/255 暖偏0.55")

    gif_bytes = verify(base, frames, centers_list)
    with open("ex4_light_sweep.gif", "wb") as f:
        f.write(gif_bytes)
    print(f"[S3] 扫光 GIF 导出 ex4_light_sweep.gif ({len(gif_bytes)/1024:.0f} KB, 48帧, 50ms, loop=0)")

    jf = jitter_fail_demo(base)
    jd = jitter_metric(jf, base)
    base_edge = bottle_edge_x(base)
    j_edges = [bottle_edge_x(f) - base_edge for f in jf]
    s_edge = bottle_edge_x(frames[0]) - base_edge
    print(f"[S4] 反例(模拟逐帧重绘, seed=7): MAD={['%.2f' % x for x in jd]} max={max(jd):.2f}；"
          f"瓶身左边缘位移={['%+d' % e for e in j_edges]}px -> 几何被逐帧搬动")
    # 扫光管线同指标应为 0（光带远离时整帧==底图）
    sd = jitter_metric([frames[0]], base)
    print(f"[S5] 对照(底图复用管线): 首帧 MAD={sd[0]:.2f}，瓶身边缘位移 {s_edge:+d}px -> "
          f"0 改动，几何由构造保证")
