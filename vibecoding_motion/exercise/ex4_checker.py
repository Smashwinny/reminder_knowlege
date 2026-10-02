# ex4 动效描述体检器：给一句自然语言动效需求打分，指出缺了词表四要素里的哪几项（零依赖）
import re

CHECKS = [
    ("触发 trigger", [r"点击|悬停|加载|出现|滚动|入场|离场|切换|按下"]),
    ("动作原语 primitive", [r"淡入|淡出|滑入|滑出|缩放|放大|缩小|模糊|弹|翻转|fade|slide|scale|blur|pop", ]),
    ("缓动 easing", [r"缓动|easing|ease|linear|线性|弹簧|spring|回弹|bounce|贝塞尔|cubic-bezier|快进慢出|先快后慢|先慢后快"]),
    ("时序 duration/stagger", [r"\d+\s*m?s\b|毫秒|秒|错峰|间隔|延迟|delay|stagger"]),
]

def audit(desc: str) -> dict:
    results = {}
    for name, pats in CHECKS:
        results[name] = any(re.search(p, desc, re.I) for p in pats)
    score = sum(results.values())
    missing = [k for k, ok in results.items() if not ok]
    return score, missing, results

CASES = [
    ("坏描述（AI 只能瞎猜）", "帮我做一个卡片动画"),
    ("好描述（四要素齐）", "页面加载时 5 张卡片从下方滑入，先快后慢，每张 300ms，错峰间隔 60ms"),
]

print("=== 动效描述体检器 ===")
for name, desc in CASES:
    score, missing, detail = audit(desc)
    print(f"\n[{name}]「{desc}」")
    for k, ok in detail.items():
        print(f"  {'OK  ' if ok else 'MISS'} {k}")
    verdict = "可直接派给 AI 执行" if score == 4 else f"先补齐：{'、'.join(missing)}"
    print(f"  得分 {score}/4 → {verdict}")
    if "坏" in name:
        assert score < 4, "坏描述应被检出缺项"
    else:
        assert score == 4, "好描述应满分"
print("\n[OK] 体检器 2 用例全部符合预期（坏描述被拦下，好描述放行）")
