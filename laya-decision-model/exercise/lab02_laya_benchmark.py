# -*- coding: utf-8 -*-
"""实验 2（主实验·Laya 侧）：复现推主"本地部署 + 系统性测试"的评测范式。

自建 24 题双语工单分诊测试集（12 英 + 12 中，人工标注标准答案），
Laya 本地推理（Router 自动挑 checkpoint），统计：
  - 三个维度准确率（department choice / urgency 分档 / churn 真假）
  - 暖态延迟（median / p95）
跑法：PYTHONUTF8=1 HF_HOME=<缓存> python lab02_laya_benchmark.py
"""
import json
import statistics
import time

from laya import Router

# label: dept ∈ {billing, technical, other}; urgency ∈ {0,1,2}; churn: 1=有退订威胁
TESTSET = [
    ("Hi, we were billed twice for March. Please refund the duplicate today or we will cancel our plan.", "billing", 2, 1),
    ("The app crashes every time I open the settings page since this morning.", "technical", 1, 0),
    ("I can't find the invoice PDF for June anywhere, could you resend it?", "billing", 0, 0),
    ("Our whole production instance is down and every user is blocked from working.", "technical", 2, 0),
    ("How do I upgrade to the enterprise plan? No rush at all.", "other", 0, 0),
    ("The refund amount is still wrong after two weeks of waiting. Fix it this week or we move to a competitor.", "billing", 2, 1),
    ("The password reset email never arrives, I've checked spam.", "technical", 1, 0),
    ("Just wondering, do you support SSO login?", "other", 0, 0),
    ("My annual renewal was charged twice, please check.", "billing", 1, 0),
    ("Feature request whenever you have time: it would be nice to have a dark mode.", "other", 0, 0),
    ("The checkout page returns a 500 error and no customer can pay right now.", "technical", 2, 0),
    ("I signed up in EUR but was charged in USD, I want the correct currency.", "billing", 1, 0),
    ("我三月被扣了两次款，今天不退款我就退订。", "billing", 2, 1),
    ("设置页面一打开就闪退，根本进不去。", "technical", 1, 0),
    ("我想要六月的发票，麻烦补发一份，谢谢。", "billing", 0, 0),
    ("系统全挂了，所有人都登录不了，业务停摆。", "technical", 2, 0),
    ("请问你们支持微信支付吗？", "other", 0, 0),
    ("这个问题报错两周没人管，我们打算换供应商了。", "technical", 2, 1),
    ("忘记密码了，重置邮件一直收不到。", "technical", 1, 0),
    ("随口问问：学生用户有折扣吗？", "other", 0, 0),
    ("年费续订好像被重复扣费了，希望核实一下。", "billing", 1, 0),
    ("不着急，希望以后能加个深色模式。", "other", 0, 0),
    ("支付页面报错 500，客户都付不了款。", "technical", 2, 0),
    ("账单币种错了，我是欧元签约却被扣了美元。", "billing", 1, 0),
]

QUESTIONS = {
    "department": {"type": "choice", "instructions": "Which department should handle this?",
                   "criteria": {"billing": "invoices, payments, refunds, charges",
                                "technical": "bugs, crashes, outages, errors, access problems",
                                "other": "general questions, sales, feature requests, everything else"}},
    "urgency": {"type": "score", "instructions": "How urgent is this?",
                "criteria": ["not urgent", "soon", "blocking or business stops"]},
    "churn_risk": {"type": "noul", "instructions": "Does the user threaten to cancel, unsubscribe, or switch to a competitor?"},
}

def urgency_bucket(score: float) -> int:
    if score < 0.67:
        return 0
    if score < 1.33:
        return 1
    return 2

def main():
    router = Router()
    rows, lat = [], []
    for i, (state, d, u, c) in enumerate(TESTSET):
        t0 = time.perf_counter()
        r = router.predict(state, QUESTIONS)
        ms = (time.perf_counter() - t0) * 1000
        lat.append(ms)
        a = r["answers"]
        got_d = a["department"]["choice"]
        got_u = urgency_bucket(a["urgency"]["score"])
        got_c = 1 if a["churn_risk"]["noul"] >= 0.5 else 0
        rows.append({
            "id": i + 1, "lang": "en" if i < 12 else "zh",
            "state": state[:40],
            "dept": [got_d == d, d, got_d],
            "urg": [got_u == u, u, got_u],
            "churn": [got_c == c, c, got_c],
            "conf_d": a["department"]["confidence"],
            "ms": round(ms),
            "route": r["routing"]["model"],
        })
        print(f"[{i+1:02d}/{len(TESTSET)}] {rows[-1]['route'][:12]:<12} {ms:7.0f}ms  "
              f"dept={'Y' if got_d == d else 'N('+got_d+')'}  urg={got_u}({'Y' if got_u == u else 'N,' + str(u)})  "
              f"churn={'Y' if got_c == c else 'N'}  conf={a['department']['confidence']:.2f}")

    n = len(TESTSET)
    acc = {
        "dept": sum(r["dept"][0] for r in rows) / n,
        "urg": sum(r["urg"][0] for r in rows) / n,
        "churn": sum(r["churn"][0] for r in rows) / n,
    }
    acc["all3"] = sum(r["dept"][0] and r["urg"][0] and r["churn"][0] for r in rows) / n
    print("\n==== Laya 本地（RTX4070 机器 CPU 推理）====")
    print(f"dept 准确率    : {acc['dept']:.2%}  ({sum(r['dept'][0] for r in rows)}/{n})")
    print(f"urgency 分档   : {acc['urg']:.2%}  ({sum(r['urg'][0] for r in rows)}/{n})")
    print(f"churn 真假     : {acc['churn']:.2%}  ({sum(r['churn'][0] for r in rows)}/{n})")
    print(f"三题全对比例   : {acc['all3']:.2%}")
    s = sorted(lat)
    print(f"延迟 median={statistics.median(lat):.0f}ms  p95={s[int(len(s)*0.95)-1]:.0f}ms  max={max(lat):.0f}ms")
    # 弃权空间：如果只在 confidence>=0.8 时作答，覆盖率 vs 准确率
    gated = [r for r in rows if r["conf_d"] >= 0.8]
    if gated:
        print(f"置信门控 conf>=0.8: 覆盖 {len(gated)}/{n}，此子集 dept 准确率 {sum(r['dept'][0] for r in gated)/len(gated):.2%}")
    with open("laya_results.json", "w", encoding="utf-8") as f:
        json.dump({"acc": acc, "rows": rows}, f, ensure_ascii=False, indent=1)
    print("已写 laya_results.json")

if __name__ == "__main__":
    main()
