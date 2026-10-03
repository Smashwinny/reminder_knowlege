# -*- coding: utf-8 -*-
"""toy_rrsi.py —— 40 行思想版的迷你 RRSI 进化环（离线、确定性、零 API）。

复现推文核心主张的三件事：
  1. 失败的检查 = 下一个修复任务（failing check -> next repair job）
  2. 回归套件盯着每次修复破坏了什么（held-out regression watch）
  3. 评分集作弊的"泄漏"提案被 Critic 拦下；关掉 Critic 就是论文里的过拟合翻车

一个"harness"= 系统提示词规则清单；"策略"按已有规则解题（规则缺席就答错）。
三种运行模式：
  python toy_rrsi.py                          # 诚实 proposer + Critic 开（默认）
  python toy_rrsi.py --proposer leaky         # 泄漏 proposer + Critic 开 -> 全被拦截
  python toy_rrsi.py --proposer leaky --critic off   # 关掉 Critic -> ID 满分 / OOD 归零
"""
from __future__ import annotations
import argparse
import re

# ---------------------------------------------------------------- 任务集 ---
# 进化集（evolve set）：proposer 看得见的失败检查
EVOLVE = [
    ("E1", "3 件商品每件 5 元，总价多少？", 15),
    ("E2", "4 件商品每件 6 元，总价多少？", 24),
    ("E3", "2 件商品每件 9 元，打 8 折总价多少？", 14.4),
    ("E4", "5 件商品每件 4 元，打 7 折总价多少？", 14.0),
    ("E6", "总价 100 元，用优惠券减 20 元，实付多少？", 80),
    ("E7", "总价 90 元，用优惠券减 15 元，实付多少？", 75),
    ("E8", "总价 60 元，用优惠券减 10 元，实付多少？", 50),
]
# 留出集（held-out / OOD 回归套件）：进化时看不见，组合了两种机制
HELDOUT = [
    ("H1", "总价 100 元打 8 折，再用优惠券减 20 元，实付多少？", 60),
    ("H2", "总价 80 元打 5 折，再用优惠券减 10 元，实付多少？", 30),
    ("H3", "总价 200 元打 9 折，再用优惠券减 50 元，实付多少？", 130),
    ("H4", "总价 50 元打 6 折，再用优惠券减 5 元，实付多少？", 25),
]

# ------------------------------------------------------------ 系统提示词 ---
RULES = {
    "BASE":     "你按用户要求计算商品总价。",
    "DISCOUNT": "规则一：题目出现'打 X 折'，先把单价总价乘以 X/10。",
    "COUPON":   "规则二：题目出现'优惠券减 Y 元'，从金额中减去 Y。",
    "ORDER":    "规则三：同时出现打折与优惠券时，先打折再减券。",
}
RULE_COST = {k: len(k) + 6 for k in RULES}      # 每条规则的推理 token 成本（示意）
HARDCODED = {tid: (text, want) for tid, text, want in EVOLVE}


def policy_answer(text: str, harness: list[str]) -> float:
    """确定性'策略'：只使用 harness 里已启用的机制。缺机制就照旧算法答错。"""
    # 泄漏机制：硬编码的"特例规则"优先命中（评分集作弊的实现方式）
    for entry in harness:
        m = re.match(r"HARDCODE_(E\d+)$", entry)
        if m and HARDCODED[m.group(1)][0] == text:
            return HARDCODED[m.group(1)][1]
    nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", text)]
    has = set(harness)
    if "优惠券" in text:
        if "COUPON" not in has:
            return -1.0                          # 不会处理优惠券
        pay = nums[0]
        cut = nums[-1]
        if "打" in text:
            if "DISCOUNT" not in has:
                return -1.0
            rate = nums[1] / 10 if "ORDER" in has else nums[1] / 10
            pay = nums[0] * rate
        return round(pay - cut, 4)
    if "打" in text:
        if "DISCOUNT" not in has:
            return nums[0] * nums[1]             # 缺机制：直接漏打折（经典回归）
        return round(nums[0] * nums[1] * nums[2] / 10, 4)
    return nums[0] * nums[1]


# --------------------------------------------------------------- 评估器 ---
def evaluate(harness, tasks) -> dict:
    per = {}
    for tid, text, want in tasks:
        got = policy_answer(text, harness)
        per[tid] = 1.0 if abs(got - want) < 1e-6 else 0.0
    S = sum(per.values()) / len(per)
    C = sum(RULE_COST.get(r, len(r) + 6) for r in harness)
    return {"S": S, "C": C, "per": per}


# -------------------------------------------------------------- 分析器 ---
def analyze(per) -> list[str]:
    """失败检查 -> 失败模式（推文：failed check becomes the next repair job）。"""
    modes = []
    for tid, text, _ in EVOLVE:
        if per[tid] == 0.0:
            if "打" in text and "优惠券" not in text and "折扣机制缺失" not in modes:
                modes.append("折扣机制缺失")
            if "优惠券" in text and "优惠券机制缺失" not in modes:
                modes.append("优惠券机制缺失")
    return modes


# ------------------------------------------------------------- 提案者 ---
def propose_honest(modes, harness):
    """诚实提案：每个失败模式映射成一条通用机制规则（不是特例补丁）。"""
    if "折扣机制缺失" in modes and "DISCOUNT" not in harness:
        return {"id": "DISCOUNT", "diff": f"+ {RULES['DISCOUNT']}"}
    if "优惠券机制缺失" in modes and "COUPON" not in harness:
        return {"id": "COUPON", "diff": f"+ {RULES['COUPON']}"}
    return None


def propose_leaky(per):
    """泄漏提案：把某道失败题的答案直接写死进系统提示词（评分集作弊）。"""
    for tid, text, want in EVOLVE:
        if per[tid] == 0.0:
            return {"id": f"HARDCODE_{tid}",
                    "diff": f"+ 特例：若题目编号为 {tid}（原文：{text}），直接输出 {want}"}
    return None


# ---------------------------------------------------------------- Critic ---
LEAK_PATTERNS = [
    (r"题目编号为\s*E\d+|原文：", "把进化集任务的特征（编号/原文）写进了提示词"),
    (r"直接输出\s*-?\d", "硬编码期望答案"),
]


def critic(diff) -> tuple[bool, list[str]]:
    hits = [why for pat, why in LEAK_PATTERNS if re.search(pat, diff)]
    return (len(hits) == 0, hits)


# --------------------------------------------------------------- 选择器 ---
DELTA = 0.05          # 噪声地板
BETA0, BETA1 = 0.10, 40.0   # 成本规则预算


def select(cands, inc, S_star, held_S):
    """Algorithm 2 缩水版：地板 + 成本规则 + OOD 守卫 + argmax。"""
    ok = []
    for c in cands:
        dS = c["S"] - inc["S"]
        dC = (c["C"] - inc["C"]) / inc["C"]
        if c["S"] < S_star - DELTA:
            c["why"] = f"低于噪声地板 {S_star - DELTA:.2f}"
        elif dS > DELTA and dC > BETA0 + BETA1 * dS:
            c["why"] = f"成本超预算 {dC:.2f} > {BETA0}+{BETA1}*dS"
        elif c["held"] < held_S - DELTA:
            c["why"] = "留出集回归！修复破坏了别的题"
        else:
            c["why"] = "admissible"
            ok.append(c)
    return max(ok, key=lambda c: c["S"]) if ok else None


# ------------------------------------------------------------------ 主环 ---
def run(proposer: str, use_critic: bool, T: int = 8) -> dict:
    harness = ["BASE"]
    inc = evaluate(harness, EVOLVE)
    inc_held = evaluate(harness, HELDOUT)
    S_star = inc["S"]
    print(f"\n=== 模式: proposer={proposer} critic={'开' if use_critic else '关'} ===")
    print(f"t=base  harness={harness}  S_id={inc['S']:.3f}  S_ood={inc_held['S']:.3f}  C={inc['C']}")
    streak = 0
    for t in range(T):
        cands = []
        cand = (propose_leaky(inc["per"]) if proposer == "leaky"
                else propose_honest(analyze(inc["per"]), harness))
        if cand is None:
            print(f"t={t}  提案者报告：没有可修的失败检查，进化收敛。")
            break
        new_harness = harness + [cand["id"]]
        ev_new = evaluate(new_harness, EVOLVE)
        cand.update(harness=new_harness, S=ev_new["S"], C=ev_new["C"],
                    held=evaluate(new_harness, HELDOUT)["S"])
        accepted, why = True, ""
        if use_critic:
            ok, hits = critic(cand["diff"])
            if not ok:
                accepted, why = False, f"Critic 拒绝：{hits}"
                streak = streak + 1 if cand["id"].startswith("HARDCODE") else 0
            else:
                streak = 0
        if accepted:
            win = select([cand], inc, S_star, inc_held["S"])
            if win is None:
                accepted, why = False, cand["why"]
            else:
                why = win["why"]
        tag = "ACCEPT" if accepted else "REJECT"
        print(f"t={t}  提案[{cand['id']}] diff=《{cand['diff']}」")
        print(f"      -> S_id={cand['S']:.3f}  S_ood={cand['held']:.3f}  C={cand['C']}  {tag}: {why}")
        if use_critic and streak >= 3:
            print("      提案者连续 3 轮交不出能过审的修复，进化终止（bounded repair 思想）。")
            break
        if accepted:
            harness, inc = cand["harness"], {"S": cand["S"], "C": cand["C"],
                                             "per": ev_new["per"]}
            S_star = max(S_star, cand["S"])
            inc_held = evaluate(harness, HELDOUT)
    fin_held = evaluate(harness, HELDOUT)
    print(f"--- 终态: harness={harness}")
    print(f"    S_id(进化集)={inc['S']:.3f}   S_ood(留出回归套件)={fin_held['S']:.3f}   "
          f"成本 C={inc['C']}")
    return {"S_id": inc["S"], "S_ood": fin_held["S"]}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--proposer", choices=["honest", "leaky"], default="honest")
    ap.add_argument("--critic", choices=["on", "off"], default="on")
    a = ap.parse_args()
    run(a.proposer, a.critic == "on")
