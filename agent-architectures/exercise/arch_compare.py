"""动手实验：用同一道任务对比 3 种 Agent 架构（all-agentic-architectures 库）。

架构对比演示：
  1. Reflection   —— 生成 -> 评审打分 -> 改写，直到分数达标
  2. ReAct        —— Thought/Action 交替，调用真实工具（计算器）
  3. SelfConsistency —— 高温采样多条推理路径 + 多数表决，对比单次直答

全部跑在本机 Ollama 的 Qwen2.5-3B 上，输出保存到 results.txt。
"""

from __future__ import annotations

import io
import sys
import time

# Windows 中文控制台 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

OUT = io.open("results.txt", "w", encoding="utf-8")


def log(msg: str = "") -> None:
    print(msg)
    OUT.write(msg + "\n")
    OUT.flush()


from langchain_core.tools import tool

from agentic_architectures.architectures import (
    Reflection,
    ReAct,
    SelfConsistency,
)
from agentic_architectures.llm.factory import get_llm


@tool
def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression, e.g. '12*(3+4)'."""
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        return "ERROR: only arithmetic characters allowed"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:  # noqa: BLE001
        return f"ERROR: {e}"


MATH_TASKS = [
    ("A baker makes 24 muffins each tray and bakes 7 trays. After selling 30, a friend takes 12. How many remain?", "126"),
    ("A train travels 60 km/h for 2.5 hours, then 45 km/h for 40 minutes. Total distance in km?", "180"),
    ("Shop A sells pens at 3 for $5. Shop B sells at $1.9 each. How much cheaper is buying 12 pens at A vs B? Answer in $.", "2.8"),
]


def demo_reflection() -> None:
    log("=" * 72)
    log("架构 1/3  Reflection（生成-评审-改写循环）")
    log("=" * 72)
    arch = Reflection(max_iterations=2, target_score=8)
    t0 = time.time()
    res = arch.run("Explain in 3-4 sentences why the sky is blue, for a curious 10-year-old.")
    log(f"[耗时 {time.time()-t0:.1f}s]")
    for h in res.state.get("history", []):
        log(f"\n--- 第 {h['iteration']+1} 稿 | 评委打分 {h['score']}/10 ---")
        log(f"草稿: {h['draft'][:200]}")
        log(f"评语: {h['critique'][:200]}")
    log(f"\n[最终输出] {res.output[:300]}")
    log("")


def demo_react() -> None:
    log("=" * 72)
    log("架构 2/3  ReAct（Thought 与 Action 显式分节点）")
    log("=" * 72)
    arch = ReAct(tools=[calculator], max_rounds=5)
    t0 = time.time()
    res = arch.run(
        "A farmer has 15 cows. Each cow produces 4 liters of milk per day. "
        "Milk sells at $1.2 per liter. How much money per week (7 days)? "
        "Use the calculator tool for every arithmetic step."
    )
    log(f"[耗时 {time.time()-t0:.1f}s]")
    for i, step in enumerate(res.trace, 1):
        role = step.get("role", "?")
        content = str(step.get("content", ""))[:250].replace("\n", " ")
        tool_calls = step.get("tool_calls")
        log(f"  步{i:02d} [{role}] {content}")
        if tool_calls:
            for tc in tool_calls:
                fn = tc.get("function", tc)
                log(f"        -> 调用工具 {fn.get('name')}(args={fn.get('arguments')})")
    log(f"\n[最终输出] {res.output[:300]}")
    log("")


def demo_self_consistency() -> None:
    log("=" * 72)
    log("架构 3/3  SelfConsistency（5 条高温采样 + 多数表决） vs 单次直答")
    log("=" * 72)
    llm = get_llm()
    arch = SelfConsistency(n_samples=5, sample_temperature=0.8)
    correct_arch = correct_naive = 0
    for task, answer in MATH_TASKS:
        t0 = time.time()
        res = arch.run(task)
        naive = llm.invoke(
            "Answer with ONLY the final number, nothing else.\n" + task
        ).content.strip()
        ok_arch = answer in res.output.replace(",", "")
        ok_naive = answer in naive.replace(",", "")
        correct_arch += ok_arch
        correct_naive += ok_naive
        log(f"\n[题] {task}")
        log(f"    标准答案={answer} | 单次直答={naive[:40]!r} {'✓' if ok_naive else '✗'}"
            f" | 多数表决={res.output[:40]!r} {'✓' if ok_arch else '✗'} [{time.time()-t0:.1f}s]")
        log(f"    元信息(各路径答案分布): {res.metadata.get('answer_votes') or res.metadata}")
    log(f"\n[汇总] 单次直答正确 {correct_naive}/{len(MATH_TASKS)}，"
        f"SelfConsistency 正确 {correct_arch}/{len(MATH_TASKS)}")
    log("")


if __name__ == "__main__":
    log("实验环境: Ollama 本地 Qwen2.5-3B-Instruct (Q4_K_M)")
    log("")
    demo_reflection()
    demo_react()
    demo_self_consistency()
    log("全部演示完成，结果已写入 results.txt")
    OUT.close()
