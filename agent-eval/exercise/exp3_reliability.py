# -*- coding: utf-8 -*-
"""实验3：可靠性 —— pass@k vs pass^k、3/n 法则、Wilson 置信区间、重复运行"""
import sys, os, math, random, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from framework import build_cases, run_agent, evaluate

cases = [c for c in build_cases() if c["slice"] == "common"]  # 12 条 common
print("== 1) pass@k vs pass^k：单次成功率 p=0.8 时的数学现实 ==")
p = 0.8
for k in (2, 3, 5):
    print(f"  k={k}: pass@k(至少1次成功) = {1-(1-p)**k:.1%}   pass^k(连续{k}次全成功) = {p**k:.1%}")

print("\n== 2) 真实重复运行：v1 在 12 条 common 上各跑 5 次（attempt=0..4）==")
per_case = {}
for c in cases:
    runs = []
    for att in range(5):
        run = run_agent(c, "v1", attempt=att)
        run["version_"] = "v1"
        runs.append(evaluate(c, run)["success"])
    per_case[c["id"]] = runs
flaky = {cid: r for cid, r in per_case.items() if 0 < sum(r) < 5}
always, never = [cid for cid, r in per_case.items() if sum(r) == 5], [cid for cid, r in per_case.items() if sum(r) == 0]
print(f"  5/5 全过: {len(always)} 条   时好时坏(flaky): {len(flaky)} 条 {list(flaky)}   全挂: {len(never)} 条")
single = sum(sum(r) for r in per_case.values()) / (12*5)
pass3 = sum(1 for r in per_case.values() if all(r[:3])) / 12
pass5 = sum(1 for r in per_case.values() if all(r)) / 12
print(f"  单次成功率(single) = {single:.1%}   pass^3 = {pass3:.1%}   pass^5 = {pass5:.1%}")
print("  -> 单次看起来不错，pass^k 才暴露 flaky（文章：企业要的是 pass^k）")

print("\n== 3) 3/n 法则：零失败观察不等于零失败率 ==")
for n in (30, 100, 300):
    print(f"  {n} 次运行 0 次越权 -> 95% 置信真实越权率上界 ≈ 3/{n} = {3/n:.1%}")

print("\n== 4) Wilson 95% 置信区间：'80% 涨到 83%' 能说明 v2 更好吗 ==")
def wilson(k, n, z=1.96):
    ph = k/n; d = 1 + z*z/n
    c = (ph + z*z/(2*n)) / d
    h = z*math.sqrt(ph*(1-ph)/n + z*z/(4*n*n)) / d
    return c-h, c+h
for label, k, n in [("v1: 80/100", 80, 100), ("v2: 83/100", 83, 100)]:
    lo, hi = wilson(k, n)
    print(f"  {label}: {k/n:.0%}  CI95=[{lo:.1%}, {hi:.1%}]")
print("  -> 两个区间几乎完全重叠：样本 100 时 3pp 的差距不构成证据，诚实结论是'未发现重大回归'")

print("\n== 5) 对照组：多少样本才能分清 80% vs 90% ==")
for n in (100, 400, 1000):
    lo1, hi1 = wilson(80*n//100, n); lo2, hi2 = wilson(90*n//100, n)
    overlap = "重叠" if lo2 < hi1 else "分离"
    print(f"  n={n}: v1 CI 上界 {hi1:.1%} vs v2 CI 下界 {lo2:.1%} -> {overlap}")
print("✅ 预期：pass^k 明显低于单次成功率；80/100 与 83/100 的 CI 重叠；n>=1000 才可能分离 10pp 差距")
