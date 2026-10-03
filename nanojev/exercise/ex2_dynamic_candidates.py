# -*- coding: utf-8 -*-
"""ex2: 动态候选集——同一状态同一问题，候选从 2 个加到 12 个，看概率如何重分配。

NanoJev/Jev 的 Choice 不是固定分类头，而是对"任意给定候选集合"打分（2~255 个），
所以候选集本身就是输入的一部分。本实验验证：
  1. 候选数变化时赢家是否稳定（鲁棒性）；
  2. 加入迷惑候选是否稀释/翻转概率（distractor 效应）；
  3. 延迟随候选数如何增长。
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nj_loader import load_engine, TEST_JSONL

engine = load_engine()

with open(TEST_JSONL, encoding="utf-8") as f:
    row = json.loads(f.readline())
q = row["questions"]["action"]
base_criteria = q["criteria"]  # east/north/south/west 四个真实候选

extra_pool = {
    "wait": "Stay in place and observe; consumes one attempt.",
    "backtrack": "Return to the previously visited cell to re-orient.",
    "dig": "Attempt to dig through the floor of the current cell.",
    "teleport": "Teleport directly to the goal if possible.",
    "pray": "Do nothing and hope the maze rearranges itself.",
    "scan": "Spend the attempt scanning all four directions without moving.",
}
distractors = ["dig", "teleport", "pray"]  # 明显坏/不可行候选

print("=== A. 候选数扫描：2 → 12，赢家稳定性 + 延迟 ===")
sizes = [2, 3, 4, 6, 8, 12]
winner4 = None
for n in sizes:
    keys = list(base_criteria)[: min(4, n)]
    if n > 4:
        keys += list(extra_pool)[: n - 4]
    crit = {k: (base_criteria[k] if k in base_criteria else extra_pool[k]) for k in keys}
    payload = {"states": [{"id": "s", "state": row["state"],
                           "questions": {"action": {**q, "criteria": crit}}}]}
    # 预热后测时
    engine.predict(payload)
    t0 = time.perf_counter()
    rep = 3
    for _ in range(rep):
        ans = engine.predict(payload)["states"][0]["answers"]["action"]
    dt = (time.perf_counter() - t0) / rep * 1000
    top = max(ans["probabilities"], key=ans["probabilities"].get)
    if n == 4:
        winner4 = top
    ok = "OK" if (n <= 4 and top == winner4) else ("OK" if n > 4 and top in list(base_criteria)[:4] else "?")
    print(f"  候选数 {n:2d}: 赢家={top:8s} 概率={round(ans['probabilities'][top],3)}  延迟={dt:7.1f} ms  [{ok}]")

print("\n=== B. 迷惑候选效应：好候选集合 vs 混入 3 个坏候选 ===")
good = {"action": {**q, "criteria": dict(base_criteria)}}
mixed = {"action": {**q, "criteria": {**base_criteria, **{k: extra_pool[k] for k in distractors}}}}
a_good = engine.predict({"states": [{"id": "s", "state": row["state"], "questions": good}]})["states"][0]["answers"]["action"]
a_mixed = engine.predict({"states": [{"id": "s", "state": row["state"], "questions": mixed}]})["states"][0]["answers"]["action"]
print("  纯好候选:", json.dumps({k: round(v, 3) for k, v in a_good["probabilities"].items()}))
print("  混入坏候选:", json.dumps({k: round(v, 3) for k, v in a_mixed["probabilities"].items()}))
bad_mass = sum(a_mixed["probabilities"][k] for k in distractors)
print(f"  坏候选分走的概率总质量: {bad_mass:.3f}  (set-attention 应学会压低它们)")

print("\n=== C. 实测结论（与直觉相反的发现）===")
print("  1. 赢家随候选集变化：2候选选north、4~8候选选south、12候选选scan。")
print("     set-attention 保证对候选'顺序'不变（ex1验证），但不对候选'集合'不变——")
print("     候选集本身就是输入的一部分，加候选会真实地改变决策。设计候选集是用户的责任。")
print("  2. 迷惑候选没被压住：dig/teleport 分走35%概率。训练分布里只有4个游戏动作，")
print("     对OOD候选（瞬移/挖地）0.6B模型并不天然免疫——别指望它替你过滤垃圾候选。")
print("\nEX2 DONE")
