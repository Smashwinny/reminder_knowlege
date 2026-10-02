# -*- coding: utf-8 -*-
"""实验2：解剖一条真实提示词——六块结构拆解
对象：案例 #544（幼儿词汇拆解学习卡，Charts & Infographics 类）
"""
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

d = json.load(open("../repo/data/cases.json", encoding="utf-8"))
case = [c for c in d["cases"] if c["id"] == 544][0]

print(f"案例 #{case['id']}  《{case['title']}》  类别: {case['category']}")
print("=" * 62)
print("【原文】")
print(case["prompt"])
print("=" * 62)

# 六块结构拆解（启发式切段 + 人工标注归属）
blocks = [
    ("① 主体与任务",  "Create a clean, child-friendly educational vocabulary poster ...",
     "先说'画什么+给谁用'：教育海报、给幼儿。一句话锁定任务边界。"),
    ("② 构图与布局",  "Feature [FRUIT] as the main large realistic object on the left, ... on the right. Connect the two with a playful dotted curved arrow ...",
     "左大右小 + 虚线箭头连接 + 小人指向：空间关系全部写死，模型没自由发挥的余地。"),
    ("③ 文字与标签",  "Add the word “[FRUIT NAME]” in large bold uppercase letters at the top and “[PART NAME]” ... underneath ...",
     "文字内容、位置、字重全部锁定——文字渲染是图像模型最大的翻车点，必须逐字指定。"),
    ("④ 风格与材质",  "soft white and very light pastel-blue background, rounded image panels, ... realistic fruit photography, simple blue typography ...",
     "配色、圆角面板、写实摄影质感、字体风格：风格靠具体名词堆出来，不靠'好看'这种虚词。"),
    ("⑤ 整体氛围",    "The overall design should feel bright, educational, modern, uncluttered ...",
     "兜底的氛围句：前四块管不了的整体感觉，在这里补一层。"),
    ("⑥ 比例/输出/负向", "Vertical 4:5 composition, high resolution, soft lighting, clear labels, no unnecessary decorations.",
     "比例 4:5 竖版 + 高分辨率 + 'no unnecessary decorations' 负向约束收尾。"),
]
for name, quote, note in blocks:
    print(f"\n{name}")
    print(f"  原文节选: {quote[:80]}...")
    print(f"  ★ {note}")

print("\n" + "=" * 62)
print("结论：所谓'逆向'，就是把别人晒图配的散文提示词，按六块协议重新")
print("      归位标注。套路可复制：任何好图提示词都能拆进这六个抽屉。")
