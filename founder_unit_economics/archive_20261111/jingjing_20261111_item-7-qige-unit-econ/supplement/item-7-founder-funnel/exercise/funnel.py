#!/usr/bin/env python3
"""Labeled-assumption unit-economics / funnel model.

Every numeric input is tagged: author_claim (unverified self-report),
teaching_assumption (ours, for sensitivity only), or derived.
Author claims are NEVER treated as measurements.
"""
from __future__ import annotations
import json, math, csv, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Inputs. "source" must stay attached wherever a number is used.
INPUTS = {
    "photo_price": {"value": 5, "unit": "CNY", "source": "author_claim", "note": "旗哥自述闲鱼上架5元AI修图，目的是跑通接单流程"},
    "year_gmv": {"value": 500000, "unit": "CNY", "source": "author_claim", "note": "自述25年GMV大概50万、上百单，未提供账本或平台后台"},
    "year_orders": {"value": 100, "unit": "orders", "source": "teaching_assumption", "note": "把「上百单」取整为100，仅用于单均价推演"},
    "course_price": {"value": 2980, "unit": "CNY", "source": "author_claim", "note": "自述第一门课定价2980"},
    "course_refund_rate": {"value": 0.10, "unit": "ratio", "source": "teaching_assumption", "note": "知识付费常见假设，不是作者给出的退款率"},
    "delivery_cost_ratio": {"value": 0.40, "unit": "ratio", "source": "teaching_assumption", "note": "协作交付成本占GMV的比例，作者未披露真实成本"},
    "ad_spend": {"value": 20000, "unit": "CNY", "source": "teaching_assumption", "note": "闲鱼投流花费未给出，这里只作敏感度起点"},
    "consult_from_ad": {"value": 200, "unit": "leads", "source": "teaching_assumption", "note": "假设广告带来的咨询数"},
    "close_rate": {"value": 0.10, "unit": "ratio", "source": "teaching_assumption", "note": "咨询到成交转化率"},
    "video_course_revenue": {"value": 100000, "unit": "CNY", "source": "author_claim", "note": "自述一条视频带来十几万课程收入，取10万作下限演示"},
    "investment": {"value": 10000000, "unit": "CNY", "source": "author_claim", "note": "自述千万投资，未见到投资协议或工商披露"},
}

def v(name):
    return INPUTS[name]["value"]

def derived():
    avg_order = v("year_gmv") / v("year_orders")
    photo_margin = v("photo_price")  # cost unknown; treat revenue only
    delivery = v("year_gmv") * v("delivery_cost_ratio")
    service_contrib = v("year_gmv") - delivery
    ad_orders = v("consult_from_ad") * v("close_rate")
    cac = v("ad_spend") / ad_orders if ad_orders else math.inf
    contrib_per_order = service_contrib / v("year_orders")
    # breakeven ad spend for this assumed close rate and contribution
    be_ad = contrib_per_order * ad_orders  # if CAC equals contribution, profit from ads is 0
    ad_profit = contrib_per_order * ad_orders - v("ad_spend")
    net_course = v("course_price") * (1 - v("course_refund_rate"))
    courses_to_match_gmv = v("year_gmv") / net_course
    return {
        "avg_order_if_100": {"value": round(avg_order, 2), "source": "derived", "uses": ["year_gmv", "year_orders"]},
        "service_delivery_cost": {"value": round(delivery, 2), "source": "derived", "uses": ["year_gmv", "delivery_cost_ratio"]},
        "service_contribution": {"value": round(service_contrib, 2), "source": "derived", "uses": ["year_gmv", "delivery_cost_ratio"]},
        "ad_orders": {"value": ad_orders, "source": "derived", "uses": ["consult_from_ad", "close_rate"]},
        "cac": {"value": round(cac, 2), "source": "derived", "uses": ["ad_spend", "consult_from_ad", "close_rate"]},
        "contrib_per_order": {"value": round(contrib_per_order, 2), "source": "derived", "uses": ["year_gmv", "delivery_cost_ratio", "year_orders"]},
        "ad_profit_under_assumptions": {"value": round(ad_profit, 2), "source": "derived", "uses": ["ad_spend", "consult_from_ad", "close_rate", "year_gmv", "delivery_cost_ratio", "year_orders"]},
        "net_course_revenue_per_seat": {"value": round(net_course, 2), "source": "derived", "uses": ["course_price", "course_refund_rate"]},
        "seats_to_match_claimed_gmv": {"value": round(courses_to_match_gmv, 1), "source": "derived", "uses": ["year_gmv", "course_price", "course_refund_rate"]},
        "photo_listing_is_not_a_profit_model": {"value": True, "source": "derived", "uses": ["photo_price"]},
        "investment_excluded_from_profit": {"value": True, "source": "derived", "note": "融资不是营业收入，模型利润不含投资额"},
    }

def sensitivity():
    rows = []
    base_close = v("close_rate")
    base_cost = v("delivery_cost_ratio")
    base_ad = v("ad_spend")
    for close in [0.05, 0.10, 0.20]:
        for cost in [0.20, 0.40, 0.60]:
            for ad in [10000, 20000, 50000]:
                orders = v("consult_from_ad") * close
                contrib = v("year_gmv") / v("year_orders") * (1 - cost)
                profit = contrib * orders - ad
                rows.append({
                    "close_rate": close,
                    "delivery_cost_ratio": cost,
                    "ad_spend": ad,
                    "orders": orders,
                    "contrib_per_order": round(contrib, 2),
                    "profit": round(profit, 2),
                    "is_base": close==base_close and cost==base_cost and ad==base_ad,
                    "all_inputs_are_assumptions_or_claims": True,
                })
    return rows

def verify(d, rows):
    checks = []
    def chk(name, ok, detail):
        checks.append((name, bool(ok), detail))
        print(("PASS" if ok else "FAIL"), name, detail)
    # every input has a source tag
    chk("inputs_tagged", all("source" in x and x["source"] in {"author_claim","teaching_assumption"} for x in INPUTS.values()), "all inputs tagged")
    chk("claims_not_measured", all(x["source"]!="measured" for x in INPUTS.values()), "no input marked measured")
    chk("investment_not_in_profit", d["investment_excluded_from_profit"]["value"] is True, "investment excluded")
    chk("photo_flag", d["photo_listing_is_not_a_profit_model"]["value"] is True, "5 yuan is process test")
    # arithmetic
    expect_avg = 500000/100
    chk("avg_order", d["avg_order_if_100"]["value"]==expect_avg, d["avg_order_if_100"]["value"])
    expect_contrib = 500000*0.6/100
    chk("contrib", d["contrib_per_order"]["value"]==expect_contrib, d["contrib_per_order"]["value"])
    chk("sensitivity_27", len(rows)==27, len(rows))
    # worse close rate should not secretly become more profitable if ad fixed and others fixed
    base = next(r for r in rows if r["is_base"])
    worse = next(r for r in rows if r["close_rate"]==0.05 and r["delivery_cost_ratio"]==0.40 and r["ad_spend"]==20000)
    chk("sensitivity_direction", worse["profit"] < base["profit"], (worse["profit"], base["profit"]))
    # high cost + high ad + low close should be negative under these numbers
    bad = next(r for r in rows if r["close_rate"]==0.05 and r["delivery_cost_ratio"]==0.60 and r["ad_spend"]==50000)
    chk("stress_negative", bad["profit"] < 0, bad["profit"])
    failed = [c for c in checks if not c[1]]
    print(f"assertions={len(checks)} failed={len(failed)}")
    if failed:
        sys.exit(1)

def main():
    d = derived()
    rows = sensitivity()
    payload = {"disclaimer": "作者融资、GMV、课程收入和场地均为自述，本模型只做带标签的算术敏感度，不是财务审计。", "inputs": INPUTS, "derived": d, "sensitivity": rows}
    (ROOT/"results.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    with (ROOT/"sensitivity.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print("derived", json.dumps({k:v["value"] for k,v in d.items()}, ensure_ascii=False, indent=2))
    print("wrote", ROOT/"results.json", ROOT/"sensitivity.csv", "rows", len(rows))
    verify(d, rows)

if __name__ == "__main__":
    main()
