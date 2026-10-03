# -*- coding: utf-8 -*-
"""实验 1：Laya 最小冒烟——三原语（choice/score/noul）各来一发。
按项目 README 的公开 API（laya.Router.predict）自己组织的练习脚本。
目的：验证安装可用 + 亲眼看到三种决策原语的输出长什么样。
"""
import sys, time
from laya import Router

router = Router()

# 场景 1：Choice——客服工单该派给哪个部门
state = "Hi, we were billed twice for March. Please refund the duplicate today or we will cancel our plan."
questions = {
    "department": {"type": "choice", "instructions": "Which department should handle this?",
                   "criteria": {"billing": "invoices, payments, refunds",
                                "technical": "bugs, outages, system errors",
                                "other": "everything else"}},
    "urgency": {"type": "score", "instructions": "How urgent is this?",
                "criteria": ["not urgent", "soon", "blocking"]},
    "churn_risk": {"type": "noul", "instructions": "Does the user threaten to cancel or leave?"},
}
t0 = time.perf_counter()
r1 = router.predict(state, questions)
dt = (time.perf_counter() - t0) * 1000
print(f"[scene1 billing ticket] {dt:.0f} ms  routing={r1['routing']['model']}")
for k in questions:
    print(" ", k, "->", r1["answers"][k])

# 场景 2：中文输入（考多语言路由：中文应被送去 multilingual checkpoint）
state2 = "我三月被扣了两次款，今天不退就退订。"
q2 = {"department": questions["department"]}
t0 = time.perf_counter()
r2 = router.predict(state2, q2)
dt = (time.perf_counter() - t0) * 1000
print(f"[scene2 Chinese ticket] {dt:.0f} ms  routing={r2['routing']['model']}")
print("  department ->", r2["answers"]["department"])

# 场景 3：明显技术故障（对照：choice 应换答案）
state3 = "The app crashes every time I open the settings page since this morning."
t0 = time.perf_counter()
r3 = router.predict(state3, q2)
dt = (time.perf_counter() - t0) * 1000
print(f"[scene3 crash ticket] {dt:.0f} ms  routing={r3['routing']['model']}")
print("  department ->", r3["answers"]["department"])
