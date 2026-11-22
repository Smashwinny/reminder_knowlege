#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""家教中介 P&L 示例：首月与续费月分账；不是经营数据或法律建议。"""


def pnl(students, price_per_class, classes_per_month, teacher_share,
        commission_classes, rent=3000, cac=80, refund=0.05,
        hours_admin=40, hourly=30, month="first"):
    if month not in {"first", "renewal"}:
        raise ValueError("month 必须是 first 或 renewal")
    if students < 0:
        raise ValueError("students 不得为负")
    gross = students * classes_per_month * price_per_class * (1 - refund)
    teacher_pay = gross * teacher_share
    commission = (students * commission_classes * price_per_class * 1.5
                  if month == "first" else 0)
    acquisition = cac * students if month == "first" else 0
    fixed = rent + hours_admin * hourly
    net = gross - teacher_pay + commission - acquisition - fixed
    return {"月份": month, "毛收款": round(gross), "教师报酬": round(teacher_pay),
            "中介费": round(commission), "获客": round(acquisition),
            "固定": round(fixed), "月净利": round(net)}


SCENARIOS = {
    "A 有场地": dict(students=10, price_per_class=120, classes_per_month=8,
                   teacher_share=0.7, commission_classes=4),
    "B 有场地翻倍": dict(students=20, price_per_class=120, classes_per_month=8,
                     teacher_share=0.7, commission_classes=4),
    "C 无场地": dict(students=10, price_per_class=120, classes_per_month=8,
                   teacher_share=0.7, commission_classes=4,
                   rent=0, hours_admin=25),
}


def break_even(month):
    for students in range(0, 1000):
        result = pnl(students=students, price_per_class=120, classes_per_month=8,
                     teacher_share=0.7, commission_classes=4, month=month)
        if result["月净利"] > 0:
            return students
    return None


def main():
    for name, kwargs in SCENARIOS.items():
        print(f"\n{name}")
        for month in ["first", "renewal"]:
            result = pnl(month=month, **kwargs)
            print(f"  {month}: 净利 {result['月净利']}；中介费 {result['中介费']}；获客 {result['获客']}；固定 {result['固定']}")
    assert pnl(month="first", **SCENARIOS["A 有场地"])["月净利"] == 4936
    assert pnl(month="renewal", **SCENARIOS["A 有场地"])["月净利"] == -1464
    assert pnl(month="renewal", **SCENARIOS["B 有场地翻倍"])["月净利"] == 1272
    assert pnl(month="renewal", **SCENARIOS["C 无场地"])["月净利"] == 1986
    assert break_even("first") == 5
    assert break_even("renewal") == 16
    print("\nA 口径盈亏平衡：首月 5 人；续费月 16 人")
    print("PASS：首月一次性中介费/获客没有计入续费月")


if __name__ == "__main__":
    main()
