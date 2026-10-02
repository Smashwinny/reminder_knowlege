# -*- coding: utf-8 -*-
"""
ex3 编辑提示词约束检查器：官方第 6/8 条原则的落地——
"将修改与约束分开" + "谨慎地进行迭代"。

一条合格的编辑提示词必须有三段：
  A. 修改段：只/仅 + 改什么（一次只改一个变量）
  B. 保留段：明确列出哪些东西绝对不能动（镜头角度/构图/光线/阴影/背景/其他物体…）
  C. 排除段：负向约束（不要多余文字/Logo/水印，不要新元素）
官方提醒：重复编辑会悄悄改掉本该保留的细节 → 每轮都要重申关键约束。
"""
import re
import sys

CHANGE = r"(只|仅|只把|只将|只改)[^。；]{0,30}(改|换|替换|移除|去掉|删除|变成|改成)"
PRESERVE = r"(保持|保留|不变|不要动|不动|维持)"
PRESERVE_ITEMS = [
    ("镜头角度", r"(镜头|机位|相机角度|视角)"),
    ("构图", r"构图"),
    ("光线/阴影", r"(光线|光照|阴影|影调)"),
    ("背景", r"背景"),
    ("其他物体/家具", r"(其他|其余|周围|家具|物体|人物|地板|服饰|布局)"),
]
EXCLUDE = r"(不要|不得|无|不添加|不出现)[^。；]{0,20}(文字|水印|logo|标志|多余|新元素)"
ITERATE = r"(一次只|只改一|这一个变量|与上一|之前一样|保持一致)"


def check_edit(prompt: str):
    report, score = [], 0
    a = bool(re.search(CHANGE, prompt))
    b = bool(re.search(PRESERVE, prompt))
    items = [n for n, pat in PRESERVE_ITEMS if re.search(pat, prompt)]
    c = bool(re.search(EXCLUDE, prompt))
    d = bool(re.search(ITERATE, prompt))
    if a:
        score += 35
        report.append("  [PASS] A 修改段：写清'只改什么'")
    else:
        report.append("  [FAIL] A 修改段：缺少'只/仅+改动对象'，模型可能顺手改别的")
    if b and len(items) >= 3:
        score += 40
        report.append(f"  [PASS] B 保留段：明确不能动的清单（{ '、'.join(items) }）")
    else:
        report.append(f"  [FAIL] B 保留段：保留项不足（仅 {len(items)} 项，需>=3；官方：列出身份/几何/布局/光照/标签）")
    if c:
        score += 15
        report.append("  [PASS] C 排除段：负向约束到位（无多余文字/水印/新元素）")
    else:
        report.append("  [FAIL] C 排除段：没有负向约束，容易长出多余文字和水印")
    if d:
        score += 10
        report.append("  [PASS] D 迭代纪律：声明一次只改一个变量/与上轮一致")
    else:
        report.append("  [FAIL] D 迭代纪律：多轮修改未声明单变量，易累积跑偏")
    return score, report


CASES = [
    ("推文原例（官方风格）",
     "只把画面中的白色椅子改成木质椅子，保持原来的镜头角度、构图、光线、阴影、背景和其他家具完全不变。"),
    ("坏例：只说改什么",
     "把椅子改成木头的"),
    ("好例：翻译信息图（官方编辑例）",
     "把信息图中的文字翻译成西班牙语，只更改文字内容本身，保持版式、图表、颜色、布局和其他所有元素完全不变，"
     "不要添加任何新的文字或水印。"),
]

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 72)
    print("编辑提示词约束检查器（官方第6/8条：修改与约束分开 + 谨慎迭代）")
    print("=" * 72)
    for title, p in CASES:
        score, report = check_edit(p)
        print(f"\n【{title}】 得分 {score}/100")
        print("\n".join(report))
    print("\n结论：坏例 0 分、推文家具例 75 分（A+B 满格）——模型不是笨在'改什么'，")
    print("是笨在'什么不能动'。翻译例 50 分则暴露另一坑：'其他所有元素不变'属于泛泛而谈，")
    print("不如像家具例那样逐项点名（镜头/构图/光线/背景/家具）。C/D 两段是满分的最后 25 分。")
