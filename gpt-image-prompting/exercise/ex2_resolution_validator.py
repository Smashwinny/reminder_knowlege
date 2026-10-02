# -*- coding: utf-8 -*-
"""
ex2 分辨率参数校验器：官方指南给出的自定义分辨率硬约束，逐条翻译成代码，
验证文档中的示例尺寸全部 PASS、构造的非法尺寸全部 FAIL。

官方约束（gpt-image-2.5 自定义 WIDTHxHEIGHT）：
  - 每条边 <= 3840 px
  - 两边都是 16 的倍数
  - 长短边比 <= 3:1
  - 总像素在 655,360 ~ 8,294,400 之间
  - 总像素 > 3,686,400（即超过 2560x1440）属于实验区
"""
import sys

MIN_PX, MAX_PX = 655_360, 8_294_400
MAX_EDGE = 3_840
EXP_PX = 3_686_400


def validate(w: int, h: int):
    errs = []
    if w > MAX_EDGE or h > MAX_EDGE:
        errs.append(f"边超限({w}x{h}): 每条边须<= {MAX_EDGE}px")
    if w % 16 or h % 16:
        errs.append(f"非16倍数({w}x{h}): 两边都必须是16的倍数")
    lo, hi = sorted((w, h))
    if hi / lo > 3:
        errs.append(f"比例超限({w}x{h}): 长短边比须<=3:1")
    total = w * h
    if not (MIN_PX <= total <= MAX_PX):
        errs.append(f"总像素越界({total}): 须在 {MIN_PX}~{MAX_PX}")
    experimental = total > EXP_PX
    return (not errs), errs, experimental, total


DOC_SIZES = [
    ("1024x1024 方形基准", 1024, 1024),
    ("1536x1024 横版", 1536, 1024),
    ("1024x1536 竖版", 1024, 1536),
    ("2048x2048 高清方", 2048, 2048),
    ("2048x1152 高清横", 2048, 1152),
    ("3840x2160 4K横", 3840, 2160),
    ("2160x3840 4K竖", 2160, 3840),
]
BAD_SIZES = [
    ("1000x1000 非16倍数", 1000, 1000),
    ("4000x1000 比例4:1", 4000, 1000),
    ("5000x5000 边超3840", 5000, 5000),
    ("640x640 总像素不足", 640, 640),
    ("3840x1280 比例3:1临界", 3840, 1280),
]


def main():
    print("=" * 72)
    print("官方自定义分辨率硬约束校验器（约束全部来自 image-prompting 官方文档）")
    print("=" * 72)
    print("\n-- 文档示例尺寸（应全部 PASS）--")
    ok_all = True
    for name, w, h in DOC_SIZES:
        ok, errs, exp, total = validate(w, h)
        tag = "PASS" if ok else "FAIL"
        exp_tag = " [实验区>2560x1440]" if exp else ""
        print(f"  [{tag}] {name:22s} {w}x{h} = {total:>9,} px{exp_tag}")
        ok_all &= ok
    print(f"  --> 文档示例全部通过: {ok_all}")

    print("\n-- 构造的非法/临界尺寸（应 FAIL 或标记实验区）--")
    for name, w, h in BAD_SIZES:
        ok, errs, exp, total = validate(w, h)
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {'; '.join(errs) if errs else '合法' + ('（实验区）' if exp else '')}")

    print("\n结论：文档约束可 1:1 翻译成确定性代码；'3840x1280' 恰好 3:1 临界合法，")
    print("比 3:1 再宽一位就 FAIL——参数纪律是可计算的，不必靠猜。")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
