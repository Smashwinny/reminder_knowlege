#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""单位收益核算器：验证"知道低价货源 ≠ 获得利润"
口径：净单价 = 售价 − 进货/交付成本 − 平台扣点 − 获客分摊 − 退款损耗 − 时间成本
四场景数字均为示例假设（明确标注），非原帖真实数据。
"""
def unit(sale, cost, platform_pct, cac, refund_pct, time_hours, hourly):
    platform = sale * platform_pct
    refund_loss = sale * refund_pct
    time_cost = time_hours * hourly
    net = sale - cost - platform - cac - refund_loss - time_cost
    return {
        "售价": sale, "平台扣点": round(platform,2), "获客分摊": cac,
        "退款损耗": round(refund_loss,2), "时间成本": round(time_cost,2),
        "净单价": round(net,2), "净利率": f"{net/sale*100:.1f}%",
    }

scenarios = {
  "①商品转售(无货源)":  dict(sale=99,  cost=45, platform_pct=0.05, cac=25, refund_pct=0.10, time_hours=0.5, hourly=30),
  "②服务转售(外包交付)": dict(sale=800, cost=400, platform_pct=0.0, cac=120, refund_pct=0.05, time_hours=2, hourly=30),
  "③内容转售(翻译合集)": dict(sale=39,  cost=3,  platform_pct=0.30, cac=8,  refund_pct=0.05, time_hours=1.5, hourly=30),
  "④能力转售(代运营)":   dict(sale=3000,cost=0,  platform_pct=0.0, cac=500, refund_pct=0.0, time_hours=25, hourly=30),
}
for name, p in scenarios.items():
    r = unit(**p)
    print(f"\n{name}")
    for k,v in r.items(): print(f"  {k}: {v}")
    if r["净单价"] <= 0:
        print("  ⚠️ 净单价≤0：该口径下不成立（原帖式宣称需打问号）")
