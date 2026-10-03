# -*- coding: utf-8 -*-
"""RRSI 仓库核心模块离线演示：不动一行 repo 代码，只用它的公开函数。
演示三件事：余弦退火预算 / 选择侧三闸门 / 组件标签防谎报。
运行：python rrsi_core_demo.py   （需先 pip install -e F:/reminder/rrsi/repo）
"""
import math
import sys

from rrsi.schedule import budget_table, edit_budget
from rrsi.selection import Candidate, cost_rule, select_round
from rrsi.config import RRSIConfig
from rrsi.components import normalize, novelty
from rrsi.evaluate import EvalResult, TaskResult, aggregate


def ev(job, rewards_by_task, k=2, tokens=1000.0):
    per = {t: TaskResult(rewards=list(r), tokens=[tokens] * len(r))
           for t, r in rewards_by_task.items()}
    return aggregate(job, k, per)


def demo_anneal():
    print("=" * 60)
    print("[1] 余弦退火编辑预算 b_t = ceil(b_min+(b_max-b_min)*(1+cos(pi t/T))/2)")
    T, bmin, bmax = 10, 1, 4
    tab = budget_table(T, bmin, bmax)
    print(f"    T={T} 轮, b_min={bmin}, b_max={bmax}")
    for t, b in enumerate(tab):
        bar = "#" * b
        print(f"    round t={t:2d}: b_t={b} {bar}")
    assert tab[0] == bmax and tab == sorted(tab, reverse=True)
    assert edit_budget(T, T, bmin, bmax) == bmin   # t=T 收到下界（与官方单测一致）
    print("    -> 早期允许捆绑多个协同编辑，后期每轮最多改 1 处（可归因）")


def demo_gates():
    print("=" * 60)
    print("[2] 选择侧三闸门（Algorithm 2）：噪声地板 / 成本规则 / argmax")
    cfg = RRSIConfig(beta0=0.1, beta1=40.0, w_s=100.0, w_c=15.0, w_n=0.5)
    inc = ev("inc", {f"t{i}": [1, 1] if i < 5 else [0, 0] for i in range(10)})   # S=0.50
    S_star, delta = 0.55, 0.05
    cands = [
        Candidate("A", [{"id": "e1", "component": "prompt"}],
                  ev=ev("A", {f"t{i}": [1, 1] if i < 7 else [0, 0] for i in range(10)})),  # S=0.70 实涨
        Candidate("B", [{"id": "e2", "component": "prompt"}],
                  ev=ev("B", {f"t{i}": ([1, 1] if i < 5 else ([0.5, 0] if i == 5 else [0, 0]))
                              for i in range(10)})),  # S=0.525 带内噪声级微涨
        Candidate("C", [{"id": "e3", "component": "prompt"}],
                  ev=ev("C", {f"t{i}": [1, 1] if i < 3 else [0, 0] for i in range(10)})),  # S=0.30 倒退
        Candidate("D", [], gate_failure="critic_reject"),                                 # 被 Critic 拦下
        Candidate("E", [{"id": "e4", "component": "prompt"}],
                  ev=ev("E", {f"t{i}": [1, 1] if i < 7 else [0, 0] for i in range(10)},
                        tokens=1000.0 * (1 + 0.1 + 40 * 0.2 + 0.5))),                # S=0.70 但太贵
    ]
    win, decs = select_round(cands, inc, S_star, delta, cfg, {})
    for d in decs:
        s = "未评估" if d.S is None else f"S={d.S:.4f}"
        ds = "  -  " if d.delta_S is None else f"dS={d.delta_S:+.4f}"
        dc = "  -  " if d.delta_C is None else f"dC={d.delta_C:+.3f}"
        print(f"    候选{d.variant}: {s} {ds} {dc} admissible={d.admissible}")
        print(f"        理由: {d.reason}")
    print(f"    -> 本轮赢家: {win.variant if win else '无（H_{t+1}=H_t）'}")
    assert win is not None and win.variant == "A"


def demo_leak_precheck():
    print("=" * 60)
    print("[3] 组件标签防谎报（normalize）+ 结构新颖度（novelty）")
    print("    例1: 申报 'skill'，但 diff 为空        ->",
          normalize("skill", "", []))
    print("    例2: 申报 'skill'，diff 新增 skills/x  ->",
          normalize("skill", "+++ b/harness/skills/x/SKILL.md", []))
    print("    例3: 申报 'bogus'（不在 K 里），diff 有 skills/ ->",
          normalize("bogus", "+++ b/harness/skills/x/SKILL.md", []))
    print("    例4: 纯文本改动（prompt）谎报 control_flow ->",
          normalize("control_flow", "+ print('hello world')", []))
    counts = {"skill": 2, "prompt": 5}
    print("    例5: novelty(['client_tool','prompt'], {'skill':2,'prompt':5}) =",
          novelty(["client_tool", "prompt"], counts),
          "（client_tool 是 incumbent 从未采纳过的结构组件）")
    assert normalize("skill", "", []) == "prompt"
    assert normalize("bogus", "+++ b/harness/skills/x/SKILL.md", []) == "skill"
    assert normalize("control_flow", "+ print('hello world')", []) == "prompt"


if __name__ == "__main__":
    demo_anneal()
    demo_gates()
    demo_leak_precheck()
    print("=" * 60)
    print("全部断言通过：三段演示与论文 Algorithm 1/2 及单测一致。")
    sys.exit(0)
