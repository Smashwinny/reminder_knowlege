# -*- coding: utf-8 -*-
"""实验4：Prompt Lint——给提示词做'出厂质检'
思想来自 repo/templates.md 各模板的'避坑指南'（模糊指令/文字没锁定/比例没写），
实现方式呼应知识库的 [[质检Gate]]：用确定性规则当裁判，提交前先过 Gate。
"""
import io, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

CHECKS = [
    ("主体任务明确",   lambda p: len(p) > 30,
     "提示词太短，连'画什么'都没说清"),
    ("比例锁定",       lambda p: re.search(r"(?<![.\d])\d{1,2}:\d{1,2}", p),
     "没写宽高比（如 16:9 / 9:16），模型默认抽卡"),
    ("文字渲染要求",   lambda p: re.search(r"text|文字|label|标题|字体", p, re.I),
     "没提文字/标签要求——画面里有字的必须逐字锁定"),
    ("风格或材质描述", lambda p: re.search(r"风格|style|材质|光|texture|摄影|插画", p, re.I),
     "没写风格/材质，出图风格随缘"),
    ("布局或构图描述", lambda p: re.search(r"布局|构图|layout|左|右|顶部|底部|居中", p, re.I),
     "没写构图/布局，元素位置随机"),
    ("负向约束",       lambda p: re.search(r"no |without|avoid|不要|避免|禁止", p, re.I),
     "没有负向约束（不要出现什么）"),
    ("无残留占位符",   lambda p: not re.search(r"\[[A-Z][A-Z /-]{2,}\]", p),
     "还有 [PLACEHOLDER] 没填！"),
]

def lint(prompt):
    fails = [(name, why) for name, fn, why in CHECKS if not fn(prompt)]
    score = (len(CHECKS) - len(fails)) / len(CHECKS) * 100
    return score, fails

good = """为健身打卡App生成一张iOS界面图。核心功能：每日步数、训练日历、好友排行榜。
视觉风格：极简，主色荧光绿，强调色深灰。布局：顶部导航+卡片流+底部Tab栏，信息层级清晰。
输出：高保真UI截图，文字清晰可读，比例9:16，不要出现乱码按钮。"""

bad = "画一个好看的app界面"

for name, p in [("合格样例（实验3的组装结果）", good), ("不合格样例", bad)]:
    score, fails = lint(p)
    verdict = "✅ PASS" if not fails else "❌ FAIL"
    print(f"[{name}]  得分 {score:.0f}/100  {verdict}")
    for fname, why in fails:
        print(f"   ✗ {fname}: {why}")
    print()

print("结论：把'避坑指南'翻译成 7 条确定性规则，就能在生成前拦住烂提示词。")
print("      这正是知识库 [[质检Gate与自我纠错循环]] 在提示工程里的落地：")
print("      裁判必须是确定性脚本，LLM 才能据失败原因自动改写重提。")
