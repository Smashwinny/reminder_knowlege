# -*- coding: utf-8 -*-
"""实验 2b：中文题换中文 criteria——决策模型的"提示词工程"对照。
假设：实验 2 中中文工单 urgency 全饱和在 2，是 criteria 英文措辞与中文输入错配所致。
"""
from lab02_laya_benchmark import TESTSET, urgency_bucket
import time, statistics
from laya import Router

ZH_QUESTIONS = {
    "department": {"type": "choice", "instructions": "这条请求应该由哪个部门处理？",
                   "criteria": {"billing": "发票、付款、退款、扣费问题",
                                "technical": "故障、闪退、报错、无法登录等系统问题",
                                "other": "一般咨询、销售、功能建议，以及其他所有情况"}},
    "urgency": {"type": "score", "instructions": "这件事有多紧急？",
                "criteria": ["不紧急", "需要尽快处理", "阻塞业务或业务停摆"]},
    "churn_risk": {"type": "noul", "instructions": "用户是否威胁要退订或转向竞争对手？"},
}

zh_items = [(s, d, u, c) for s, d, u, c in TESTSET[12:]]

router = Router()
ok = {"dept": 0, "urg": 0, "churn": 0}
lat = []
for i, (state, d, u, c) in enumerate(zh_items):
    t0 = time.perf_counter()
    r = router.predict(state, ZH_QUESTIONS, model="multilingual")
    ms = (time.perf_counter() - t0) * 1000
    lat.append(ms)
    a = r["answers"]
    gd = a["department"]["choice"]
    gu = urgency_bucket(a["urgency"]["score"])
    gc = 1 if a["churn_risk"]["noul"] >= 0.5 else 0
    ok["dept"] += gd == d; ok["urg"] += gu == u; ok["churn"] += gc == c
    print(f"[zh{i+1:02d}] {ms:5.0f}ms dept={gd}({'Y' if gd==d else 'N'}) urg_score={a['urgency']['score']:.2f}->{gu}({'Y' if gu==u else 'N,want '+str(u)}) churn={gc}({'Y' if gc==c else 'N'})")
n = len(zh_items)
print(f"\n==== 中文 criteria 对照（12 题）====")
print(f"dept {ok['dept']}/{n}  urgency {ok['urg']}/{n}  churn {ok['churn']}/{n}  median={statistics.median(lat):.0f}ms")
