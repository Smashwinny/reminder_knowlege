# -*- coding: utf-8 -*-
"""实验1：把 541 条案例当数据库查——awesome-gpt-image-2 数据面摸底
数据源：../repo/data/cases.json（项目自己维护的结构化案例库）
"""
import json, re, collections, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

DATA = "../repo/data/cases.json"
d = json.load(open(DATA, encoding="utf-8"))
cases = d["cases"]

print("=" * 60)
print(f"案例总数: {len(cases)}   (README 宣称 544，实测数据文件 {d['totalCases']})")
print(f"类别数: {len(d['categories'])}   风格标签: {len(d['styles'])}   场景标签: {len(d['scenes'])}")

# 1. 类别分布
cat_count = collections.Counter(c["category"] for c in cases)
print("\n--- 类别分布（多者为王）---")
for cat, n in cat_count.most_common():
    bar = "#" * (n // 2)
    print(f"{cat:<28}{n:>4}  {bar}")

# 2. 提示词长度分布
lens = [len(c["prompt"]) for c in cases]
lens.sort()
avg = sum(lens) / len(lens)
print(f"\n--- 提示词长度（字符数）---")
print(f"最短 {lens[0]} / 平均 {avg:.0f} / 中位 {lens[len(lens)//2]} / 最长 {lens[-1]}")

# 3. 结构化特征覆盖率："Prompt as Code" 是不是真的？
def has_ratio(p):   # 比例锁定，如 16:9 / 4:5 / 9:16
    return bool(re.search(r"(?<![.\d])\d{1,2}:\d{1,2}", p))
def has_text(p):    # 文字/标签渲染要求
    return bool(re.search(r"text|文字|label|typography|字体|标题", p, re.I))
def has_style(p):   # 风格/材质描述
    return bool(re.search(r"style|风格|材质|lighting|光|texture", p, re.I))
def has_negative(p):# 负向约束（不要什么）
    return bool(re.search(r"no |without|avoid|不要|避免|无 ", p, re.I))
def has_placeholder(p):  # [XXX] 大写占位符
    return bool(re.search(r"\[[A-Z][A-Z /-]{2,}\]", p))

n = len(cases)
feats = {"比例锁定 aspect ratio": has_ratio, "文字渲染要求": has_text,
         "风格/材质描述": has_style, "负向约束": has_negative,
         "[占位符] 槽位": has_placeholder}
print("\n--- 结构化特征覆盖率（541 条实测）---")
for name, fn in feats.items():
    k = sum(1 for c in cases if fn(c["prompt"]))
    print(f"{name:<24}{k:>4} 条  ({k/n*100:.0f}%)")

# 4. 风格标签 Top10
style_count = collections.Counter()
for c in cases:
    s = c["styles"]
    if isinstance(s, str):
        try: s = eval(s)
        except Exception: s = [s]
    for t in (s or []): style_count[t] += 1
print("\n--- 风格标签 Top 10 ---")
for t, k in style_count.most_common(10):
    print(f"{t:<16}{k:>4}")

print("\n结论：这不是'329 条句子'，是一个带标签体系的结构化数据集，")
print("      所以才能被 Agent / 脚本按 category+style+scene 检索复用。")
