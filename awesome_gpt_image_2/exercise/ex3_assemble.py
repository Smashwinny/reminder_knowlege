# -*- coding: utf-8 -*-
"""实验3：Prompt as Code——用模板函数'填空组装'新提示词
模板来源：docs/templates.md 的 UI 截图常规模板（改写成 Python 函数）
演示：只改一个参数（主色），看组装结果怎么变——这就是'提示词当代码写'
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def assemble_ui_prompt(product, platform, features, layout, theme,
                       primary, accent, typography, ratio):
    """UI 截图模板：来自 repo/docs/templates.md 的'UI与界面·常规模板'"""
    feats = "、".join(features)
    return f"""为{product}生成一张{platform}界面图。
核心功能：{feats}。
视觉风格：{theme}，主色{primary}，强调色{accent}。
布局：{layout}，信息层级清晰，留白充足。
输出：高保真UI截图，文字清晰可读，比例{ratio}。"""

# 同一份模板，两个版本只差主色一个参数 —— 类比改代码里的一个常量
v1 = assemble_ui_prompt(
    product="健身打卡App", platform="iOS",
    features=["每日步数", "训练日历", "好友排行榜"],
    layout="顶部导航+卡片流+底部Tab栏",
    theme="极简", primary="荧光绿", accent="深灰",
    typography="无衬线", ratio="9:16")

v2 = assemble_ui_prompt(
    product="健身打卡App", platform="iOS",
    features=["每日步数", "训练日历", "好友排行榜"],
    layout="顶部导航+卡片流+底部Tab栏",
    theme="极简", primary="落日橙", accent="深灰",
    typography="无衬线", ratio="9:16")

print("【版本A：主色=荧光绿】")
print("-" * 50)
print(v1)
print("\n【版本B：主色=落日橙（只改了 1 个参数）】")
print("-" * 50)
print(v2)

import difflib
diff = [l for l in difflib.unified_diff(v1.splitlines(), v2.splitlines(), lineterm="") if l[:1] in "+-" and l[:3] not in ("+++", "---")]
print("\n【两版 diff】")
print("\n".join(diff))

print("\n结论：模板函数化后，'换皮肤'=改一个实参，提示词永远结构完整，")
print("      这就是 Prompt as Code：把提示词从'一次性的文案'升级为")
print("      '可参数化、可批量、可测试的代码资产'。")
