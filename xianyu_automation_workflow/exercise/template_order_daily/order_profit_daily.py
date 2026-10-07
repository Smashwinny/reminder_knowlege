# -*- coding: utf-8 -*-
"""订单利润日报工具（闲鱼自动化脚本模板 · 工作流实验产物）。

按《xianyu_automation_workflow》文中工作流真实执行：
  ① 客户原话 → 一句明确 spec
  ② Claude 角色：架构/异常处理/定时逻辑/操作说明（见 ARCHITECTURE.md）
  ③ Codex 角色：本可运行脚本（stdlib，无第三方依赖）
  ④ 本地跑通 + 交付物结构（README + 示例数据 + 一键运行）

spec：把导出的多份订单 CSV 合并成一份利润日报，标记异常订单，输出 HTML。
用法：python order_profit_daily.py 数据目录 --out 日报.html
"""
import argparse
import csv
import html
import sys
from collections import defaultdict
from pathlib import Path

# 平台扣点（对应原文"算错了一个平台扣点"的坑：扣点必须显式可配）
PLATFORM_FEES = {"淘宝": 0.05, "拼多多": 0.06, "抖店": 0.05}
ABNORMAL_LOW_PROFIT_RATE = 0.10   # 利润率低于 10% 标红


def load_orders(data_dir):
    rows = []
    files = sorted(Path(data_dir).glob("*.csv"))
    if not files:
        raise SystemExit(f"目录无 CSV：{data_dir}")
    for f in files:
        with f.open(encoding="utf-8-sig", newline="") as fp:
            for r in csv.DictReader(fp):
                r["_来源文件"] = f.name
                rows.append(r)
    return rows


def compute(rows):
    """利润 = 实收 - 成本 - 运费 - 平台扣点。字段缺失必须显式抛错（隐藏成本坑）。"""
    out = []
    for r in rows:
        try:
            amount = float(r["实收"])
            cost = float(r["成本"])
            ship = float(r.get("运费") or 0)
            platform = r["平台"]
        except (KeyError, ValueError) as e:
            raise SystemExit(f"数据字段异常（{r['_来源文件']}）：{e}；"
                             "字段需含 实收/成本/运费/平台")
        fee_rate = PLATFORM_FEES.get(platform)
        if fee_rate is None:
            raise SystemExit(f"未知平台 '{platform}'：请先在 PLATFORM_FEES 配置扣点")
        fee = amount * fee_rate
        profit = amount - cost - ship - fee
        out.append({**r, "扣点费": round(fee, 2), "利润": round(profit, 2),
                    "利润率": round(profit / amount, 4) if amount else 0})
    return out


def render(orders, out_path):
    by_platform = defaultdict(lambda: [0.0, 0.0])
    abnormal = []
    for o in orders:
        p = by_platform[o["平台"]]
        p[0] += o["实收"] and float(o["实收"]) or 0
        p[1] += o["利润"]
        if o["利润率"] < ABNORMAL_LOW_PROFIT_RATE:
            abnormal.append(o)
    total_rev = sum(v[0] for v in by_platform.values())
    total_profit = sum(v[1] for v in by_platform.values())

    def money(x): return f"¥{x:,.2f}"
    rows = "".join(
        f"<tr class='{'abn' if o in abnormal else ''}'><td>{html.escape(o['订单号'])}</td>"
        f"<td>{html.escape(o['平台'])}</td><td>{money(float(o['实收']))}</td>"
        f"<td>{money(o['扣点费'])}</td><td>{money(o['利润'])}</td>"
        f"<td>{o['利润率']*100:.1f}%</td></tr>"
        for o in orders)
    pf = "".join(
        f"<tr><td>{k}</td><td>{money(v[0])}</td><td>{money(v[1])}</td>"
        f"<td>{v[1]/v[0]*100 if v[0] else 0:.1f}%</td></tr>"
        for k, v in by_platform.items())
    Path(out_path).write_text(f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<title>订单利润日报</title><style>
body{{font-family:"Microsoft YaHei";margin:32px;background:#f0f9ff}}
h1{{color:#0369a1}} table{{border-collapse:collapse;background:#fff;width:100%;margin:14px 0}}
th{{background:#0284c7;color:#fff;padding:8px}} td{{border:1px solid #bae6fd;padding:6px 10px}}
tr.abn td{{background:#fee2e2;color:#b91c1c;font-weight:bold}}
.kpi{{display:inline-block;background:#fff;border-radius:12px;padding:12px 22px;margin:6px;
border:2px solid #0ea5e9;font-size:1.1em}} .kpi b{{color:#0369a1}}</style></head><body>
<h1>订单利润日报</h1>
<div class="kpi">总实收 <b>{money(total_rev)}</b></div>
<div class="kpi">总利润 <b>{money(total_profit)}</b></div>
<div class="kpi">利润率 <b>{total_profit/total_rev*100 if total_rev else 0:.1f}%</b></div>
<div class="kpi">异常订单 <b>{len(abnormal)} 笔</b>（利润率&lt;{ABNORMAL_LOW_PROFIT_RATE*100:.0f}%）</div>
<h2>按平台汇总（扣点已扣）</h2><table><tr><th>平台</th><th>实收</th><th>利润</th><th>利润率</th></tr>{pf}</table>
<h2>明细</h2><table><tr><th>订单号</th><th>平台</th><th>实收</th><th>扣点费</th><th>利润</th><th>利润率</th></tr>{rows}</table>
</body></html>""", encoding="utf-8")
    return total_rev, total_profit, abnormal


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data_dir")
    ap.add_argument("--out", default="日报.html")
    args = ap.parse_args()
    orders = compute(load_orders(args.data_dir))
    rev, profit, abnormal = render(orders, args.out)
    print(f"订单 {len(orders)} 笔 | 实收 {rev:,.2f} | 利润 {profit:,.2f} | 异常 {len(abnormal)} 笔")
    print(f"日报已生成：{args.out}")


if __name__ == "__main__":
    main()
