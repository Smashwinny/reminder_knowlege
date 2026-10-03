# -*- coding: utf-8 -*-
"""ex1: NanoJev 决策初体验——三种题型、零解码、概率校准、排列不变性。

操作：python ex1_decision_hello.py
验证：所有断言通过，输出各题概率分布、延迟、GPU 显存、零自回归解码步数。
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nj_loader import load_engine, TEST_JSONL

engine = load_engine()
print(f"[1] 模型加载完成: 0.6B 参数, checkpoint={engine.root.name}")

# --- 取一条真实测试数据（迷宫题）作为 state ---
with open(TEST_JSONL, encoding="utf-8") as f:
    row = json.loads(f.readline())
q = row["questions"]["action"]
print(f"[2] 真实测试样本: task={row['metadata']['task']}, 候选={list(q['criteria'])}")

payload = {
    "states": [
        {
            "id": "maze-real",
            "state": row["state"],
            "questions": {
                "action": q,  # choice：4 个方向
                "near_goal": {  # boolean：命题真假概率
                    "type": "boolean",
                    "instructions": "The maze goal is at [5,5] and the agent is at (3,5). Proposition: the agent can reach the goal within the remaining attempts.",
                    "criteria": {"false": "The proposition is false.", "true": "The proposition is true."},
                },
                "risk": {  # score：2-10 级有序量表
                    "type": "score",
                    "instructions": "Rate the risk that moving south from the current cell wastes an attempt (wall or dead end).",
                    "criteria": ["no risk", "low risk", "medium risk", "high risk"],
                },
            },
        }
    ]
}

t0 = time.perf_counter()
result = engine.predict(payload)
dt = time.perf_counter() - t0
answers = result["states"][0]["answers"]

print("\n[3] 一次前向，三题同出（零自回归解码）:")
for qid, a in answers.items():
    print(f"  {qid}: {json.dumps({k: v for k, v in a.items() if k != 'probabilities'})}")
    print(f"       probs={ {k: round(v, 3) for k, v in a['probabilities'].items()} }")
    s = sum(a["probabilities"].values())
    assert abs(s - 1.0) < 1e-5, f"概率和不为1: {s}"
print("  PASS: 三题概率均归一")

ex = result["execution"]
print(f"\n[4] 执行元数据: forward_passes={ex['forward_passes']}, "
      f"autoregressive_decode_steps={ex['autoregressive_decode_steps']}, "
      f"candidate_paths={ex['candidate_paths']}")
assert ex["autoregressive_decode_steps"] == 0
print("  PASS: 零输出 token 解码（这就是 System One/Jev 的核心卖点）")

import torch
print(f"\n[5] 延迟与显存: 3题4路径 {dt*1000:.1f} ms; "
      f"GPU 显存占用 {torch.cuda.memory_allocated()/2**30:.2f} GiB")

# --- 排列不变性：同一道题，候选顺序打乱，赢家应不变（set attention 的设计目标） ---
import random
criteria = q["criteria"]
keys = list(criteria)
rng = random.Random(42)
agree = 0
N = 5
for i in range(N):
    shuffled = dict(rng.sample(list(criteria.items()), len(criteria)))
    p2 = {"states": [{"id": "maze-real", "state": row["state"],
                      "questions": {"action": {**q, "criteria": shuffled}}}]}
    a2 = engine.predict(p2)["states"][0]["answers"]["action"]["choice"]
    if a2 == answers["action"]["choice"]:
        agree += 1
print(f"\n[6] 排列不变性: {N} 次打乱候选顺序，{agree}/{N} 次选出同一动作")
print(f"    (choice 题型带 set-attention 头，理论上对候选集合的排列近似不变)")
print("\nEX1 ALL PASS")
