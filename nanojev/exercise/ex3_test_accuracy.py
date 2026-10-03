# -*- coding: utf-8 -*-
"""ex3: 官方测试集推理——本机复现 NanoJev 的测试集表现。

数据: unified/hard/test.jsonl（2496 题 = shooting 2169 + maze 211 + snake 116）
目标: shooting → 专家动作 conditioned_action（hard label）
      maze/snake → Jev API 策略分布 argmax（api_policy_distribution）
指标: 题目级 top-1 一致率，按任务/子任务分组。

采样: 全量 2496 题在 fp32/no-TF32 下本机需 >40 分钟，故分层抽样——
      maze/snake 全量（327）+ basic/predict_position 各 300，共 927 题。
运行: python -u ex3_test_accuracy.py
"""
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nj_loader import load_engine, TEST_JSONL, question_target, shooting_subtask

SAMPLE_CAPS = {("shooting", "basic"): 300, ("shooting", "predict_position"): 300}
BATCH_QUESTIONS = 12

engine = load_engine()
print("模型加载完成，开始测试集推理（分层抽样）...", flush=True)

all_rows = []
with open(TEST_JSONL, encoding="utf-8") as f:
    for line in f:
        all_rows.append(json.loads(line))

rows = []
counts = defaultdict(int)
for r in all_rows:
    if r["metadata"]["task"] == "shooting":
        key = ("shooting", shooting_subtask(r))
    else:
        key = (r["metadata"]["task"], "")
    if counts[key] < SAMPLE_CAPS.get(key, 10**9):
        counts[key] += 1
        rows.append(r)
print(f"抽样完成: maze={counts[('maze','')]} snake={counts[('snake','')]} "
      f"basic={counts[('shooting','basic')]} predict_pos={counts[('shooting','predict_position')]} "
      f"总计 {len(rows)} 题", flush=True)

# 分批推理，逐批打印进度（全量跑会因 fp32/no-TF32 超时，这里可见进度）
stats = defaultdict(lambda: [0, 0])
t_start = time.perf_counter()
for i in range(0, len(rows), BATCH_QUESTIONS):
    chunk = rows[i:i + BATCH_QUESTIONS]
    payload = {"states": []}
    for r in chunk:
        qid = next(iter(r["questions"]))
        payload["states"].append({"id": r["id"], "state": r["state"], "questions": {qid: r["questions"][qid]}})
    result = engine.predict(payload, batch_questions=BATCH_QUESTIONS)
    answers = {s["id"]: s["answers"] for s in result["states"]}
    for r in chunk:
        qid = next(iter(r["questions"]))
        a = answers[r["id"]][qid]
        pred = a["choice"] if a["type"] == "choice" else a["value"]
        tgt, _ = question_target(r)
        sub = shooting_subtask(r) if r["metadata"]["task"] == "shooting" else r["metadata"]["task"]
        stats[sub][1] += 1
        if pred == tgt:
            stats[sub][0] += 1
    done = i + len(chunk)
    el = time.perf_counter() - t_start
    print(f"  进度 {done}/{len(rows)}  已用 {el:.0f}s  预计总时长 {el/done*len(rows):.0f}s", flush=True)

dt = time.perf_counter() - t_start
print(f"\n推理完成: {dt:.1f}s, decode_steps=0（全程零自回归解码）\n")

print(f"{'任务':<22s} {'一致':>6s} {'总数':>6s} {'top-1一致率':>10s}")
total_c = total_n = 0
for sub in ["maze", "snake", "basic", "predict_position"]:
    c, n = stats[sub]
    total_c += c
    total_n += n
    print(f"{sub:<22s} {c:>6d} {n:>6d} {c/n*100:>9.1f}%")
print(f"{'TOTAL':<22s} {total_c:>6d} {total_n:>6d} {total_c/total_n*100:>9.1f}%")

out = Path(__file__).resolve().parent / "ex3_test_accuracy_result.json"
out.write_text(json.dumps({
    "sampled": True, "seconds": round(dt, 1), "total": total_n, "correct": total_c,
    "per_task": {k: {"correct": v[0], "total": v[1]} for k, v in stats.items()},
}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\n结果已存 {out.name}")
print("对照 README 口径：其报告的是整局游戏成功率（Basic 128/128 等），")
print("本实验是题目级动作一致率（927 题分层抽样），两者指标不同不能直接比。")
print("\nEX3 DONE")
