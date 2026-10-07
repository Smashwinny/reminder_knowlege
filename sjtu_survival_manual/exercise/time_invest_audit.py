# -*- coding: utf-8 -*-
"""一周时间投资审计器 —— 《上海交通大学生存手册》"正确地浪费时间"一章的动手实验。

读取 exercise/week_log.csv（date,activity,hours 三列），把每项活动按
"时间尺度价值"四档分类，输出文本报告并生成彩色 HTML 报告 report.html。

分类表 CATEGORY_MAP 可自由编辑：改一个活动的档位，重跑脚本，看报告变化。
只依赖 Python 标准库。
"""
import csv
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
LOG_CSV = BASE / "week_log.csv"
OUT_HTML = BASE / "report.html"

# 四档时间尺度价值（对应手册 li-zhi-pian/zheng-que-di-lang-fei-sheng-xia-de-shi-jian.md）
# lifelong  = 对整个人生产生正面影响（值得做）
# midterm   = 对中期未来产生影响（适度做）
# shortterm = 只获得转瞬即逝的满足（少做）
# negative  = 负向消耗（应避免）
TIERS = {
    "lifelong": ("终身受益", "#16a34a"),
    "midterm": ("中期影响", "#2563eb"),
    "shortterm": ("短期满足", "#f59e0b"),
    "negative": ("负向消耗", "#dc2626"),
}

CATEGORY_MAP = {
    "跟着文档学习": "lifelong",
    "跑 img2threejs 实验": "lifelong",
    "读 SurviveSJTU 生存手册": "lifelong",
    "复习整理自己的知识库": "lifelong",
    "写学习疑问清单": "lifelong",
    "健身房锻炼": "lifelong",
    "户外跑步": "lifelong",
    "通勤路上听技术播客": "lifelong",
    "做 changeheadanddance 报告": "midterm",
    "帮同学调试代码并写复盘": "lifelong",
    "学校英语课": "lifelong",
    "突击备考背考点": "shortterm",
    "刷短视频": "negative",
    "无意义群聊灌水": "negative",
    "打游戏": "negative",
    "给社团活动搬桌子当壮丁": "negative",
    "失眠熬夜刷手机": "negative",
}

# 手册《你的身价是多少》中的价格锚点（数据更新于 2024 年，仅作对标参照）
PRICE_ANCHORS = [
    ("跨国投资银行分析师首年月薪", "约 70000 元/月"),
    ("美国大学奖学金（平均）", "约 15000 元/月"),
    ("交大应届毕业生平均月薪（含本研）", "约 12000 元/月"),
    ("企业培训讲座主讲人出场费", "约 2000~30000 元/场"),
    ("北京新东方讲师课时工资", "约 500~1000 元/课时"),
    ("高中生家教市价", "约 100~300 元/小时"),
    ("上海小时最低工资", "24 元/小时"),
    ("校内勤工助学值班", "20~25 元/小时"),
]


def tier_of(activity: str) -> str:
    for key, tier in CATEGORY_MAP.items():
        if key in activity:
            return tier
    return "midterm"  # 未登记的活动默认按中期影响处理，并在报告中提示


def load_rows():
    rows = []
    with open(LOG_CSV, encoding="utf-8") as f:
        for i, row in enumerate(csv.DictReader(f), start=2):
            try:
                hours = float(row["hours"])
            except (KeyError, ValueError):
                print(f"[警告] 第 {i} 行 hours 不是数字，已跳过：{row}")
                continue
            rows.append({"date": row["date"], "activity": row["activity"], "hours": hours})
    return rows


def audit(rows):
    per_tier = {k: 0.0 for k in TIERS}
    per_activity = {}
    unknown = []
    for r in rows:
        tier = tier_of(r["activity"])
        if not any(k in r["activity"] for k in CATEGORY_MAP):
            unknown.append(r["activity"])
        per_tier[tier] += r["hours"]
        per_activity[r["activity"]] = per_activity.get(r["activity"], 0.0) + r["hours"]
    total = sum(per_tier.values())
    return per_tier, per_activity, total, sorted(set(unknown))


def score(per_tier, total):
    """时间投资评分：终身*1.0 + 中期*0.5 + 短期*0.1 + 负向*(-0.5)，归一到百分制。"""
    if total == 0:
        return 0.0
    raw = per_tier["lifelong"] * 1.0 + per_tier["midterm"] * 0.5 \
        + per_tier["shortterm"] * 0.1 - per_tier["negative"] * 0.5
    return max(0.0, min(100.0, raw / total * 100))


def print_report(per_tier, per_activity, total, unknown, sc):
    print("=" * 56)
    print("一周时间投资审计报告（依据《上海交通大学生存手册》时间价值四档）")
    print("=" * 56)
    print(f"记录总时长：{total:.1f} 小时")
    for tier, (label, _c) in TIERS.items():
        h = per_tier[tier]
        pct = h / total * 100 if total else 0
        bar = "█" * int(pct / 2)
        print(f"{label:<6} {h:5.1f} 小时 ({pct:5.1f}%)  {bar}")
    print(f"\n时间投资评分：{sc:.1f} / 100")
    print("\n按活动明细（降序）：")
    for act, h in sorted(per_activity.items(), key=lambda kv: -kv[1]):
        label = TIERS[tier_of(act)][0]
        print(f"  {act:<28} {h:5.1f} h   [{label}]")
    if unknown:
        print("\n[提示] 以下活动未在 CATEGORY_MAP 登记，默认按中期影响处理：")
        for act in unknown:
            print(f"  - {act}")


def write_html(per_tier, per_activity, total, unknown, sc):
    bars = []
    for tier, (label, color) in TIERS.items():
        h = per_tier[tier]
        pct = h / total * 100 if total else 0
        bars.append(
            f'<div class="bar-row"><span class="bar-label">{label}</span>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{pct:.1f}%;'
            f'background:{color}"></div></div><span class="bar-num">{h:.1f}h（{pct:.1f}%）</span></div>'
        )
    acts = "".join(
        f"<tr><td>{act}</td><td>{h:.1f}</td><td>{TIERS[tier_of(act)][0]}</td></tr>"
        for act, h in sorted(per_activity.items(), key=lambda kv: -kv[1])
    )
    anchors = "".join(f"<tr><td>{name}</td><td>{price}</td></tr>" for name, price in PRICE_ANCHORS)
    unknown_html = (
        "<p>未登记活动（默认中期）：" + "、".join(unknown) + "</p>" if unknown else ""
    )
    html = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<title>一周时间投资审计报告</title><style>
body{{font-family:"Microsoft YaHei",sans-serif;margin:32px;background:#fff7ed;color:#1f2937}}
h1{{color:#ea580c}} h2{{color:#b45309}}
.bar-row{{display:flex;align-items:center;margin:8px 0}}
.bar-label{{width:90px;font-weight:bold}}
.bar-track{{flex:1;background:#fee2e2;border-radius:8px;height:22px;margin:0 10px}}
.bar-fill{{height:22px;border-radius:8px}}
.bar-num{{width:150px}}
table{{border-collapse:collapse;margin:12px 0}}
td,th{{border:1px solid #fdba74;padding:6px 12px}}
th{{background:#ffedd5}}
.score{{font-size:2em;color:#dc2626;font-weight:bold}}
</style></head><body>
<h1>一周时间投资审计报告</h1>
<p>方法来源：《上海交通大学生存手册 · 正确地浪费剩下的时间》——任务价值取决于它在时间尺度上的作用效率。</p>
<p>时间投资评分：<span class="score">{sc:.1f}</span> / 100（终身×1.0 + 中期×0.5 + 短期×0.1 − 负向×0.5）</p>
<h2>四档时间分布</h2>{''.join(bars)}
<h2>活动明细</h2><table><tr><th>活动</th><th>小时</th><th>档位</th></tr>{acts}</table>
{unknown_html}
<h2>身价对标锚点（手册《你的身价是多少》，数据 2024）</h2>
<table><tr><th>劳动形式</th><th>价格</th></tr>{anchors}</table>
</body></html>"""
    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"\nHTML 报告已生成：{OUT_HTML}")


def main():
    rows = load_rows()
    if not rows:
        print("week_log.csv 没有有效记录，请先填写时间日志。")
        sys.exit(1)
    per_tier, per_activity, total, unknown = audit(rows)
    sc = score(per_tier, total)
    print_report(per_tier, per_activity, total, unknown, sc)
    write_html(per_tier, per_activity, total, unknown, sc)


if __name__ == "__main__":
    main()
