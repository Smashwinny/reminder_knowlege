#!/usr/bin/env python3
"""教学用单位经济 / 漏斗模型。

所有输入必须带 source 标签。author_claim / author_claim_derived 不是实测。
teaching_assumption 不是作者数据。本程序不调用任何付费 API，不改任何账户。
"""
from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ASSUMPTION_PATH = HERE / "assumptions.json"
CURRENCY = "CNY"


class AssumptionError(ValueError):
    pass


def load_assumptions(path: Path = ASSUMPTION_PATH) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if "meta" not in data or "economics" not in data:
        raise AssumptionError("assumptions.json 缺少 meta 或 economics")
    return data


def field(block: dict[str, Any], key: str) -> tuple[float, str, dict[str, Any]]:
    item = block[key]
    if "value" not in item or "source" not in item:
        raise AssumptionError(f"{key} 缺少 value 或 source")
    source = item["source"]
    if source not in {"author_claim", "author_claim_derived", "teaching_assumption"}:
        raise AssumptionError(f"{key} 的 source 不合法: {source}")
    return float(item["value"]), source, item


def format_money(x: float) -> str:
    sign = "-" if x < 0 else ""
    return f"{sign}¥{abs(x):,.2f}"


def funnel_counts(impressions: float, ctr: float, inquiry_rate: float, close_rate: float) -> dict[str, float]:
    if min(impressions, ctr, inquiry_rate, close_rate) < 0:
        raise AssumptionError("漏斗参数不能为负")
    clicks = impressions * ctr
    inquiries = clicks * inquiry_rate
    paid = inquiries * close_rate
    return {
        "impressions": impressions,
        "clicks": clicks,
        "inquiries": inquiries,
        "paid": paid,
    }


def unit_economics(
    *,
    n_paid: float,
    price: float,
    refund_rate: float,
    fee_rate: float,
    delivery_cost_ratio: float,
    traffic_cost: float,
    fulfillment_per_order: float = 0.0,
) -> dict[str, float]:
    """一期贡献利润。

    revenue              = n_paid * price
    refunds              = revenue * refund_rate
    net_revenue          = revenue - refunds
    fees                 = net_revenue * fee_rate
    delivery             = net_revenue * delivery_cost_ratio
    fulfillment          = n_paid * (1 - refund_rate) * fulfillment_per_order
    contribution         = net_revenue - fees - delivery - fulfillment - traffic_cost
    CAC                  = traffic_cost / n_paid   (n_paid>0)
    contribution_margin  = contribution / revenue  (revenue>0)
    """
    if n_paid < 0 or price < 0 or traffic_cost < 0 or fulfillment_per_order < 0:
        raise AssumptionError("人数、价格、流量成本和履约成本不能为负")
    for name, rate in {
        "refund_rate": refund_rate,
        "fee_rate": fee_rate,
        "delivery_cost_ratio": delivery_cost_ratio,
    }.items():
        if rate < 0:
            raise AssumptionError(f"{name} 不能为负")

    revenue = n_paid * price
    refunds = revenue * refund_rate
    net_revenue = revenue - refunds
    fees = net_revenue * fee_rate
    delivery = net_revenue * delivery_cost_ratio
    fulfillment = n_paid * (1.0 - refund_rate) * fulfillment_per_order
    contribution = net_revenue - fees - delivery - fulfillment - traffic_cost
    cac = (traffic_cost / n_paid) if n_paid > 0 else float("inf")
    cm = (contribution / revenue) if revenue else float("nan")
    contribution_per_order = (contribution / n_paid) if n_paid else float("nan")
    return {
        "n_paid": n_paid,
        "price": price,
        "revenue": revenue,
        "refunds": refunds,
        "net_revenue": net_revenue,
        "fees": fees,
        "delivery": delivery,
        "fulfillment": fulfillment,
        "traffic_cost": traffic_cost,
        "contribution": contribution,
        "cac": cac,
        "contribution_margin": cm,
        "contribution_per_order": contribution_per_order,
    }


def break_even_traffic_cost(ue_kwargs: dict[str, float]) -> float:
    """使 contribution == 0 的最大流量成本（其他条件不变）。"""
    kwargs = dict(ue_kwargs)
    kwargs["traffic_cost"] = 0.0
    base = unit_economics(**kwargs)
    # contribution(t) = contribution(0) - t  => t* = contribution(0)
    return base["contribution"]


def break_even_close_rate(
    *,
    impressions: float,
    ctr: float,
    inquiry_rate: float,
    price: float,
    refund_rate: float,
    fee_rate: float,
    delivery_cost_ratio: float,
    cpc: float,
    fulfillment_per_order: float = 0.0,
    lo: float = 0.0,
    hi: float = 1.0,
    tol: float = 1e-8,
) -> float:
    """二分查找使贡献利润 >= 0 的最小成交率。若即使用 close=1 仍亏损，返回 inf。"""

    def contrib(close: float) -> float:
        counts = funnel_counts(impressions, ctr, inquiry_rate, close)
        traffic = counts["clicks"] * cpc
        return unit_economics(
            n_paid=counts["paid"],
            price=price,
            refund_rate=refund_rate,
            fee_rate=fee_rate,
            delivery_cost_ratio=delivery_cost_ratio,
            traffic_cost=traffic,
            fulfillment_per_order=fulfillment_per_order,
        )["contribution"]

    if contrib(hi) < 0:
        return float("inf")
    if contrib(lo) >= 0:
        return lo
    for _ in range(64):
        mid = (lo + hi) / 2.0
        if contrib(mid) >= 0:
            hi = mid
        else:
            lo = mid
        if hi - lo < tol:
            break
    return hi


def sensitivity_table(
    base_kwargs: dict[str, float],
    shocks: dict[str, float],
    deltas: tuple[float, ...] = (-0.3, -0.1, 0.1, 0.3),
) -> list[dict[str, Any]]:
    """单因子敏感分析。shocks 给出基准值；对每个因子按相对幅度扰动。"""
    base = unit_economics(**base_kwargs)
    rows = []
    for name, base_val in shocks.items():
        for d in deltas:
            kwargs = dict(base_kwargs)
            new_val = base_val * (1.0 + d)
            if name in kwargs:
                kwargs[name] = new_val
            else:
                raise AssumptionError(f"敏感分析因子 {name} 不在单位经济参数中")
            # n_paid 与 traffic 可能联动；此处按「其余冻结」教学口径
            out = unit_economics(**kwargs)
            rows.append(
                {
                    "factor": name,
                    "delta": d,
                    "new_value": new_val,
                    "contribution": out["contribution"],
                    "contribution_change": out["contribution"] - base["contribution"],
                    "contribution_margin": out["contribution_margin"],
                }
            )
    return rows


def tornado(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """按 |贡献利润变化| 的最大振幅排序。"""
    by_factor: dict[str, list[dict[str, Any]]] = {}
    for r in rows:
        by_factor.setdefault(r["factor"], []).append(r)
    summary = []
    for factor, items in by_factor.items():
        changes = [i["contribution_change"] for i in items]
        summary.append(
            {
                "factor": factor,
                "min_change": min(changes),
                "max_change": max(changes),
                "amplitude": max(abs(min(changes)), abs(max(changes))),
            }
        )
    summary.sort(key=lambda x: x["amplitude"], reverse=True)
    return summary


def pretty_ue(name: str, ue: dict[str, float], tags: dict[str, str] | None = None) -> str:
    lines = [f"## {name}"]
    if tags:
        lines.append("输入标签：")
        for k, v in tags.items():
            lines.append(f"  - {k}: {v}")
    mapping = [
        ("n_paid", "成交单数", False),
        ("price", "客单价", True),
        ("revenue", "收入", True),
        ("refunds", "退款", True),
        ("net_revenue", "净收入", True),
        ("fees", "平台/支付手续费", True),
        ("delivery", "交付成本", True),
        ("fulfillment", "履约成本", True),
        ("traffic_cost", "流量成本", True),
        ("contribution", "贡献利润", True),
        ("cac", "CAC（流量成本/成交单数）", True),
        ("contribution_per_order", "单笔贡献利润", True),
        ("contribution_margin", "贡献利润率", False),
    ]
    for key, label, money in mapping:
        val = ue[key]
        if key == "contribution_margin":
            lines.append(f"  {label}: {val:.2%}")
        elif key == "n_paid":
            lines.append(f"  {label}: {val:.4f}")
        elif money:
            lines.append(f"  {label}: {format_money(val)}")
        else:
            lines.append(f"  {label}: {val}")
    return "\n".join(lines)


def cmd_assumptions(data: dict[str, Any]) -> int:
    print("货币:", data["meta"]["currency"])
    print("说明:", data["meta"]["purpose"])
    print("标签定义:")
    for k, v in data["meta"]["source_tags"].items():
        print(f"  [{k}] {v}")
    print()
    for section in ("funnel_teaching", "economics"):
        print(f"=== {section} ===")
        for key, item in data[section].items():
            extra = []
            if "quote" in item:
                extra.append(f"原文：「{item['quote']}」")
            if "note" in item:
                extra.append(item["note"])
            suffix = ("  " + " ".join(extra)) if extra else ""
            print(f"  {key}: {item['value']}  [{item['source']}]{suffix}")
    print()
    print("校验：每条输入都带 source，模型拒绝无标签数值直接入账。")
    return 0


def teaching_custom_kwargs(data: dict[str, Any], delivery_key: str = "delivery_cost_ratio_solo") -> tuple[dict[str, float], dict[str, str], dict[str, float]]:
    f, e = data["funnel_teaching"], data["economics"]
    impressions, s_imp, _ = field(f, "impressions")
    ctr, s_ctr, _ = field(f, "ctr")
    inquiry_rate, s_inq, _ = field(f, "inquiry_rate")
    close_rate, s_close, _ = field(f, "close_rate_custom")
    cpc, s_cpc, _ = field(f, "cpc")
    price, s_price, _ = field(e, "custom_aov_teaching")
    refund, s_ref, _ = field(e, "refund_rate_custom")
    fee, s_fee, _ = field(e, "platform_fee_rate")
    pay, s_pay, _ = field(e, "payment_fee_rate")
    delivery, s_del, _ = field(e, delivery_key)
    counts = funnel_counts(impressions, ctr, inquiry_rate, close_rate)
    traffic = counts["clicks"] * cpc
    kwargs = dict(
        n_paid=counts["paid"],
        price=price,
        refund_rate=refund,
        fee_rate=fee + pay,
        delivery_cost_ratio=delivery,
        traffic_cost=traffic,
        fulfillment_per_order=0.0,
    )
    tags = {
        "impressions": s_imp,
        "ctr": s_ctr,
        "inquiry_rate": s_inq,
        "close_rate_custom": s_close,
        "cpc": s_cpc,
        "custom_aov_teaching": s_price,
        "refund_rate_custom": s_ref,
        "fees": f"{s_fee}+{s_pay}",
        delivery_key: s_del,
    }
    funnel = dict(counts, cpc=cpc, close_rate=close_rate, impressions=impressions, ctr=ctr, inquiry_rate=inquiry_rate)
    return kwargs, tags, funnel


def teaching_course_kwargs(data: dict[str, Any]) -> tuple[dict[str, float], dict[str, str], dict[str, float]]:
    f, e = data["funnel_teaching"], data["economics"]
    impressions, s_imp, _ = field(f, "impressions")
    ctr, s_ctr, _ = field(f, "ctr")
    inquiry_rate, s_inq, _ = field(f, "inquiry_rate")
    close_rate, s_close, _ = field(f, "close_rate_course")
    cpc, s_cpc, _ = field(f, "cpc")
    price, s_price, _ = field(e, "course_price")
    refund, s_ref, _ = field(e, "course_refund_rate")
    fee, s_fee, _ = field(e, "platform_fee_rate")
    pay, s_pay, _ = field(e, "payment_fee_rate")
    fulfill, s_ful, _ = field(e, "course_fulfillment_cost")
    counts = funnel_counts(impressions, ctr, inquiry_rate, close_rate)
    traffic = counts["clicks"] * cpc
    kwargs = dict(
        n_paid=counts["paid"],
        price=price,
        refund_rate=refund,
        fee_rate=fee + pay,
        delivery_cost_ratio=0.0,
        traffic_cost=traffic,
        fulfillment_per_order=fulfill,
    )
    tags = {
        "impressions": s_imp,
        "ctr": s_ctr,
        "inquiry_rate": s_inq,
        "close_rate_course": s_close,
        "cpc": s_cpc,
        "course_price": s_price,
        "course_refund_rate": s_ref,
        "fees": f"{s_fee}+{s_pay}",
        "course_fulfillment_cost": s_ful,
    }
    funnel = dict(counts, cpc=cpc, close_rate=close_rate)
    return kwargs, tags, funnel


def cmd_base(data: dict[str, Any]) -> int:
    print("【教学保守情景】定制商单漏斗（全部关键成本为 teaching_assumption，客单价也是教学假设，不是自述 GMV）")
    kwargs, tags, funnel = teaching_custom_kwargs(data)
    print(
        "漏斗：展示 {impressions:.0f} → 点击 {clicks:.2f} → 咨询 {inquiries:.2f} → 成交 {paid:.4f}".format(
            **funnel
        )
    )
    print(f"流量成本 = 点击 × CPC = {funnel['clicks']:.2f} × {format_money(funnel['cpc'])} = {format_money(kwargs['traffic_cost'])}")
    ue = unit_economics(**kwargs)
    print(pretty_ue("定制商单 · 独自交付假设", ue, tags))
    print()
    kwargs2, tags2, _ = teaching_custom_kwargs(data, "delivery_cost_ratio_outsourced")
    ue2 = unit_economics(**kwargs2)
    print(pretty_ue("定制商单 · 外包交付假设（同一漏斗，只改交付成本占比）", ue2, tags2))
    print()
    ck, ct, cf = teaching_course_kwargs(data)
    print(
        "课程漏斗：展示 {impressions:.0f} → 点击 {clicks:.2f} → 咨询 {inquiries:.2f} → 成交 {paid:.4f}".format(
            **cf
        )
    )
    ue3 = unit_economics(**ck)
    print(pretty_ue("课程（标价来自作者自述 2980，其余成本与转化为教学假设）", ue3, ct))
    print()
    print("结论边界：以上贡献利润只在给定假设下成立，不能证明原帖收入或融资。")
    return 0


def cmd_sensitivity(data: dict[str, Any]) -> int:
    kwargs, _, _ = teaching_custom_kwargs(data)
    base = unit_economics(**kwargs)
    print("基准贡献利润（教学保守 / 独自交付）:", format_money(base["contribution"]))
    shocks = {
        "price": kwargs["price"],
        "refund_rate": kwargs["refund_rate"],
        "fee_rate": kwargs["fee_rate"],
        "delivery_cost_ratio": kwargs["delivery_cost_ratio"],
        "traffic_cost": kwargs["traffic_cost"],
        "n_paid": kwargs["n_paid"],
    }
    rows = sensitivity_table(kwargs, shocks)
    print("factor\tdelta\tnew_value\tcontribution\tchange\tmargin")
    for r in rows:
        print(
            f"{r['factor']}\t{r['delta']:+.0%}\t{r['new_value']:.6f}\t"
            f"{r['contribution']:.2f}\t{r['contribution_change']:.2f}\t{r['contribution_margin']:.2%}"
        )
    print()
    print("龙卷风（按贡献利润变化振幅降序）：")
    for t in tornado(rows):
        print(
            f"  {t['factor']}: 最小变化 {format_money(t['min_change'])}, "
            f"最大变化 {format_money(t['max_change'])}, 振幅 {format_money(t['amplitude'])}"
        )
    print("说明：本表把各因子当作其余冻结的自变量。现实中成交单数与流量成本往往联动，振幅排序只用于找出最危险的假设，不是因果证明。")
    return 0


def cmd_breakeven(data: dict[str, Any]) -> int:
    kwargs, _, funnel = teaching_custom_kwargs(data)
    t_star = break_even_traffic_cost(kwargs)
    n_paid = kwargs["n_paid"]
    cac_star = t_star / n_paid if n_paid else float("inf")
    print("【教学保守 / 独自交付】")
    print(f"  使贡献利润=0 的最大流量成本: {format_money(t_star)}")
    print(f"  对应最大 CAC: {format_money(cac_star)}")
    print(f"  当前流量成本: {format_money(kwargs['traffic_cost'])}，当前 CAC: {format_money(kwargs['traffic_cost']/n_paid if n_paid else float('inf'))}")
    close_star = break_even_close_rate(
        impressions=funnel["impressions"],
        ctr=funnel["ctr"],
        inquiry_rate=funnel["inquiry_rate"],
        price=kwargs["price"],
        refund_rate=kwargs["refund_rate"],
        fee_rate=kwargs["fee_rate"],
        delivery_cost_ratio=kwargs["delivery_cost_ratio"],
        cpc=funnel["cpc"],
    )
    print(f"  使贡献利润>=0 的最小成交率: {close_star:.4%}" if close_star != float("inf") else "  即便成交率=100% 仍亏损")
    print(f"  当前教学成交率: {funnel['close_rate']:.4%}")

    print()
    print("【课程轨道】标价来自自述 2980，成本和转化仍是教学假设")
    ck, _, cf = teaching_course_kwargs(data)
    t2 = break_even_traffic_cost(ck)
    print(f"  最大流量成本: {format_money(t2)}")
    if ck["n_paid"]:
        print(f"  最大 CAC: {format_money(t2/ck['n_paid'])}")
    close2 = break_even_close_rate(
        impressions=funnel["impressions"],
        ctr=funnel["ctr"],
        inquiry_rate=funnel["inquiry_rate"],
        price=ck["price"],
        refund_rate=ck["refund_rate"],
        fee_rate=ck["fee_rate"],
        delivery_cost_ratio=ck["delivery_cost_ratio"],
        cpc=funnel["cpc"],
        fulfillment_per_order=ck["fulfillment_per_order"],
    )
    print(f"  最小成交率: {close2:.4%}" if close2 != float("inf") else "  即便成交率=100% 仍亏损")
    print("融资额、办公面积和「一条视频值几十万」不进入盈亏平衡，因为它们不是单笔经营的单位经济。")
    return 0


def cmd_narrative(data: dict[str, Any]) -> int:
    e = data["economics"]
    gmv, s_gmv, gmv_item = field(e, "claimed_year_gmv")
    orders, s_ord, ord_item = field(e, "claimed_year_orders")
    aov, s_aov, aov_item = field(e, "custom_aov_from_claim")
    course_rev, s_cr, cr_item = field(e, "claimed_video_course_revenue")
    invest, s_inv, inv_item = field(e, "claimed_investment")
    course_price, s_cp, _ = field(e, "course_price")
    print("【自述情景对照】以下全部标记为未核实，不是本批实测。")
    print(f"  2025 GMV: {format_money(gmv)}  [{s_gmv}] 原文：「{gmv_item['quote']}」")
    print(f"  订单数下沿: {orders:.0f}  [{s_ord}] 原文：「{ord_item['quote']}」")
    print(f"  粗除客单价: {format_money(aov)}  [{s_aov}]  {aov_item['note']}")
    derived = gmv / orders
    print(f"  现场复核 500000/100 = {format_money(derived)} （与 JSON 中 custom_aov_from_claim 一致: {abs(derived-aov)<1e-9}）")
    print(f"  课程标价: {format_money(course_price)}  [{s_cp}]")
    print(f"  单条视频课程收入下沿: {format_money(course_rev)}  [{s_cr}] 原文：「{cr_item['quote']}」  {cr_item['note']}")
    implied_course_units = course_rev / course_price
    print(f"  若把「10万课程收入」按 2980 反推销量 ≈ {implied_course_units:.2f} 份（ demonstrative only）")
    print(f"  融资: {format_money(invest)}  [{s_inv}] 原文：「{inv_item['quote']}」  {inv_item['note']}")
    print()
    # Apply claimed AOV onto the SAME teaching funnel, still with teaching costs
    kwargs, tags, funnel = teaching_custom_kwargs(data)
    kwargs["price"] = aov
    tags["price"] = s_aov + "（仅替换客单价，成本和转化仍是教学假设）"
    ue = unit_economics(**kwargs)
    print(pretty_ue("把自述粗除客单价代入教学漏斗——仍然不是对 50 万 GMV 的证实", ue, tags))
    print()
    print("为什么不能把 50 万 GMV 写成「已验证收入」：")
    print("  1. 没有订单流水、平台账单或税务记录；")
    print("  2. GMV 不是贡献利润，未扣退款、投流、交付分成和自己的时间；")
    print("  3. 「上百单」不是精确计数，客单价只是下沿粗除；")
    print("  4. 融资是资本项，不能加进贡献利润，更不能用来证明获客效率。")
    return 0


def cmd_stress(data: dict[str, Any]) -> int:
    kwargs, _, _ = teaching_custom_kwargs(data)
    base = unit_economics(**kwargs)
    print("基准（教学保守 / 独自交付）贡献利润:", format_money(base["contribution"]))
    print("fault\tdelivery_ratio\trefund_rate\tcontribution\tmargin\tstatus")
    cases = [
        ("交付占比升到 0.80", 0.80, kwargs["refund_rate"]),
        ("退款率升到 0.30", kwargs["delivery_cost_ratio"], 0.30),
        ("交付 0.80 且退款 0.30", 0.80, 0.30),
        ("交付占比 1.10（成本超过净收入）", 1.10, kwargs["refund_rate"]),
    ]
    negative = 0
    for name, d, r in cases:
        k = dict(kwargs)
        k["delivery_cost_ratio"] = d
        k["refund_rate"] = r
        ue = unit_economics(**k)
        status = "亏损" if ue["contribution"] < 0 else "仍为正（仅在本假设下）"
        if ue["contribution"] < 0:
            negative += 1
        print(
            f"{name}\t{d:.2f}\t{r:.2f}\t{ue['contribution']:.2f}\t{ue['contribution_margin']:.2%}\t{status}"
        )
    print()
    print(f"故障注入结果：{negative}/{len(cases)} 组贡献利润为负。")
    print("这证明单位经济对交付成本和退款率敏感；不能在未测成本前按自述 GMV 扩张外包或投放。")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="教学用单位经济模型")
    parser.add_argument(
        "command",
        choices=["assumptions", "base", "sensitivity", "breakeven", "narrative", "stress"],
    )
    parser.add_argument("--assumptions", default=str(ASSUMPTION_PATH))
    args = parser.parse_args(argv)
    data = load_assumptions(Path(args.assumptions))
    dispatch = {
        "assumptions": cmd_assumptions,
        "base": cmd_base,
        "sensitivity": cmd_sensitivity,
        "breakeven": cmd_breakeven,
        "narrative": cmd_narrative,
        "stress": cmd_stress,
    }
    return dispatch[args.command](data)


if __name__ == "__main__":
    sys.exit(main())
