# -*- coding: utf-8 -*-
"""
WikiSkill 方法层 toy 复现（零 API、零依赖、全确定性）
论文: WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution
      (arXiv:2608.27454, Google Research, 2026-08-27)

说明（诚实边界）：
- 论文用真实 LLM（Gemini-3.5-Flash / Qwen 系列）；本实验没有 API key，
  用两个"确定性 stub 模型"（ModelA/ModelB，各自带系统性错误模式）替代 LLM。
- Wiki Maintainer / Skill Proposer / Gating 的控制逻辑按论文 Algorithm 1
  用确定性脚本实现——验证的是**方法机制**（三层工作区、wiki 永不回滚、
  门控只动技能、skill-impact 审计、全批模式优化器调用数与数据量无关），
  不是论文的绝对分数。模型权重（stub 的错误模式）全程不变——
  提升只来自持久知识层，这正是论文标题的主张。
"""
from __future__ import annotations
import datetime as dt
import json, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.join(HERE, "workspace")          # 三层工作区根目录
TOL = 0.05                                     # 数值题容忍误差（绝对值）

# ---------------------------------------------------------------- 任务层
def gen_tasks(n_per_type=5):
    """固定任务集（种子隐含在硬编码列表里，完全可复现）"""
    miles = [12, 5, 33, 8, 21, 40, 17, 3, 27, 46][:n_per_type]
    fahr  = [98, 32, 212, 68, 104, 50, 176, 86, 14, 230][:n_per_type]
    days  = [(2026, 1, 3, 40), (2025, 3, 15, 50), (2026, 2, 20, 15),
             (2024, 12, 1, 70), (2026, 5, 5, 90), (2025, 8, 9, 25),
             (2026, 7, 4, 60), (2024, 2, 28, 2), (2026, 10, 1, 45),
             (2025, 11, 20, 100)][:n_per_type]
    leap  = [1900, 2000, 2024, 2023, 2100, 1996, 2016, 2019, 2028, 1800][:n_per_type]
    pools = []
    pools.append([dict(ttype="miles", q=f"将 {m} 英里换算为公里", ans=float(m)) for m in miles])
    pools.append([dict(ttype="f2c", q=f"将 {f}°F 换算为 °C", ans=float(f)) for f in fahr])
    pools.append([dict(ttype="adddays", q=f"{y}-{mo:02d}-{d:02d} 加 {k} 天", ans=(y, mo, d, k)) for (y, mo, d, k) in days])
    pools.append([dict(ttype="leap", q=f"{y} 是闰年吗(1/0)", ans=y) for y in leap])
    # 轮转交错，保证 train/val 切分后题型均衡
    tasks = [t for i in range(n_per_type) for p in pools for t in [p[i]]]
    return tasks

def truth(t):
    """真值"""
    if t["ttype"] == "miles": return t["ans"] * 1.609344
    if t["ttype"] == "f2c":   return (t["ans"] - 32.0) * 5.0 / 9.0
    if t["ttype"] == "adddays":
        y, mo, d, k = t["ans"]
        return (dt.date(y, mo, d) + dt.timedelta(days=k)).isoformat()
    if t["ttype"] == "leap":  # 完整格里高利规则（含世纪年规则）
        y = t["ans"]
        return 1 if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else 0

def correct(t, pred) -> bool:
    exp = truth(t)
    if t["ttype"] == "miles": return abs(pred - exp) <= TOL
    if t["ttype"] == "f2c":   return abs(pred - exp) <= TOL
    if t["ttype"] == "adddays": return pred == exp
    if t["ttype"] == "leap":  return pred == exp
    raise ValueError(t["ttype"])

# ---------------------------------------------------------------- 两个"模型"（权重=错误模式，全程冻结）
def model_a_naive(t):
    """ModelA：像小模型——系统性近似错误"""
    if t["ttype"] == "miles":   return t["ans"] * 1.5            # 粗略系数
    if t["ttype"] == "f2c":     return t["ans"] * 5.0 / 9.0      # 忘了减 32
    if t["ttype"] == "adddays":                                 # 每月按 30 天、不闰
        y, mo, d, k = t["ans"]; tot = d + k; mo2 = mo
        while tot > 30: tot -= 30; mo2 += 1
        return f"{y}-{mo2:02d}-{tot:02d}"
    if t["ttype"] == "leap":    return 1 if t["ans"] % 4 == 0 else 0  # 无世纪年规则

def model_b_naive(t):
    """ModelB：另一个"家族"——错误模式与 A 不同，部分题型本来就对"""
    if t["ttype"] == "miles":   return t["ans"] * 1.6            # 精度不够(1.6 vs 1.609344)
    if t["ttype"] == "f2c":     return (t["ans"] - 32.0) * 5.0 / 9.0   # 本来就对
    if t["ttype"] == "adddays":                                 # 日历精确但每月按 30 天跨月
        y, mo, d, k = t["ans"]
        if k + d <= 30 or mo == 12:
            return (dt.date(y, mo, d) + dt.timedelta(days=k)).isoformat()
        return f"{y}-{mo+1:02d}-{d+k-30:02d}"                   # 跨月即错
    if t["ttype"] == "leap":                                    # 本来就对（含世纪规则）
        y = t["ans"]; return 1 if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else 0

# ---------------------------------------------------------------- 三层工作区
class Workspace:
    def __init__(self, root):
        self.root = root
        for sub in ("raw", "wiki/patterns", "skills"):
            os.makedirs(os.path.join(root, sub), exist_ok=True)
        self.wiki_index = {}      # page -> 一句话索引（对应 wiki/index.md）
        self.wiki_pages = {}      # page -> 内容字符串（对应 wiki/patterns/*.md）
        self.logs = []            # wiki/logs.md
        self.impact = []          # wiki/skill-impact.md：提案审计
        self.skills = {}          # name -> dict(applies, rule)（对应 skills/SKILL.md）
    # --- raw 层：只追加、不可变（论文：不可变执行轨迹）
    def log_raw(self, task, pred, ok):
        with open(os.path.join(self.root, "raw", "traces.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(dict(ttype=task["ttype"], q=task["q"], pred=str(pred), ok=ok),
                               ensure_ascii=False) + "\n")
    # --- wiki 层：补丁式增量编辑（append/replace/insert）
    def wiki_upsert(self, page, content):
        if page in self.wiki_pages:
            self.wiki_pages[page] += "\n[patch] " + content   # 增量补丁
        else:
            self.wiki_pages[page] = content                   # 新建模式页
            self.wiki_index[page] = content.splitlines()[0]
    def wiki_append_log(self, line):
        self.logs.append(line)
    # --- skill-impact.md：外层 harness 程序化追加（论文原文机制）
    def impact_append(self, entry):
        self.impact.append(entry)
    def rejected_names(self):
        return {e["skill"] for e in self.impact if e["result"] == "Rejected"}
    # --- skills 层：可整体回滚
    def snapshot_skills(self):
        return dict(self.skills)
    def restore_skills(self, snap):
        self.skills = dict(snap)

# ---------------------------------------------------------------- 确定性 stub "LLM" 组件
def signature(fails):
    """失败签名 = 题型（确定性 Wiki Maintainer 的分组键）"""
    return sorted({f[0]["ttype"] for f in fails})

PATTERN_RULES = {
    # Wiki Maintainer 从失败轨迹"归纳"出的规则页内容（stub 版知识蒸馏）
    "miles":   "规则：英里→公里必须用精确系数 1.609344，近似 1.5/1.6 在大数值全错。",
    "f2c":     "规则：华氏→摄氏必须先减 32 再乘 5/9，即 (F-32)*5/9。",
    "adddays": "规则：日期加天数必须用真实日历（每月天数不同、含闰年），勿按 30 天估算。",
    "leap":    "规则：闰年=能被4整除，但世纪年须再被400整除（1900/2100 不是闰年）。",
}
# Skill Proposer 的"提案"：由模式页生成可执行校正（stub 版 LLM 写技能）
def propose_skill_for(ptype):
    if ptype == "miles":
        def fn(t, naive): return t["ans"] * 1.609344
    elif ptype == "f2c":
        def fn(t, naive): return (t["ans"] - 32.0) * 5.0 / 9.0
    elif ptype == "adddays":
        def fn(t, naive):
            y, mo, d, k = t["ans"]
            return (dt.date(y, mo, d) + dt.timedelta(days=k)).isoformat()
    elif ptype == "leap":
        def fn(t, naive):     # 注意：技能按论文由弱模型经验归纳——可能带"低层 workaround"缺陷
            y = t["ans"]; return 1 if y % 4 == 0 else 0   # 简化规则：缺世纪年判断
    return dict(applies=ptype, fn=fn,
                desc=f"[skill:{ptype}-fix] {PATTERN_RULES[ptype]}")

# 推理 agent（训练时禁读 wiki；技能全量注入系统提示——论文 full-injection 设定）
def infer(model, task, skills):
    if task["ttype"] in skills:
        return skills[task["ttype"]]["fn"](task, model(task))
    return model(task)

def evaluate(model, tasks, skills):
    oks, per_type = 0, {}
    for t in tasks:
        ok = correct(t, infer(model, t, skills))
        oks += ok
        per_type.setdefault(t["ttype"], [0, 0])
        per_type[t["ttype"]][0] += ok; per_type[t["ttype"]][1] += 1
    return oks / len(tasks), per_type

def rollout(model, tasks, skills, ws):
    """训练 rollout：记录轨迹进 raw 层（推理 agent 禁读 wiki）"""
    results = []
    for t in tasks:
        pred = infer(model, t, skills)
        ok = correct(t, pred)
        ws.log_raw(t, pred, ok)
        results.append((t, pred, ok))
    return results

# ---------------------------------------------------------------- Algorithm 1 主循环
COUNTER = {"maintainer": 0, "proposer": 0, "rollout": 0}   # 优化器调用记账

def evolve(model, train, val, ws, iters=3, verbose=True):
    best_score, best_skills = -1.0, {}
    hist = []
    for k in range(1, iters + 1):
        if best_score == 1.0: break                      # 提前终止：验证满分
        # (1) 训练 rollout（推理 agent 不读 wiki，技能全量注入）
        tr = rollout(model, train, ws.skills, ws); COUNTER["rollout"] += len(train)
        # (2) Wiki 维护：吃采样子集（全批=全部失败+通过轨迹），补丁式更新
        COUNTER["maintainer"] += 1
        fails = [r for r in tr if not r[2]]
        for ptype in signature(fails):
            ws.wiki_upsert(f"patterns/{ptype}.md", PATTERN_RULES[ptype])
        ws.wiki_append_log(f"iter{k}: 失败题型 {signature(fails)}，模式页已更新")
        # (3) Skill Proposer：ReAct 式按需检索——先看索引+skill-impact，再读页，原子提案
        COUNTER["proposer"] += 1
        proposals, rejected = [], ws.rejected_names()
        for ptype in signature(fails):
            name = f"{ptype}-fix"
            if name in ws.skills or name in rejected:    # 审计记录防重复提案
                continue
            proposals.append(propose_skill_for(ptype))
        # (4) Gating：候选技能集上验证集，严格提升才接受；wiki 永不回滚
        snap = ws.snapshot_skills()
        for p in proposals: ws.skills[p["applies"]] = p
        score, per = evaluate(model, val, ws.skills)
        accepted = score > best_score
        if accepted:
            best_score, best_skills = score, ws.snapshot_skills()
        else:
            ws.restore_skills(snap)                      # 只回滚 skills
        for p in proposals:
            ws.impact_append(dict(iter=k, skill=f"{p['applies']}-fix",
                                  score=round(score, 4),
                                  result="Accepted" if accepted else "Rejected"))
        hist.append((k, score, [p["applies"] for p in proposals], accepted))
        if verbose:
            print(f"  iter{k}: 提案={[p['applies'] for p in proposals]} "
                  f"val={score:.3f} {'接受' if accepted else '回滚(技能)'} wiki页数={len(ws.wiki_pages)}(不动)")
    return best_score, best_skills, hist

def fresh_ws(name):
    p = os.path.join(WS, name)
    shutil.rmtree(p, ignore_errors=True)
    return Workspace(p)

def pct(x): return f"{x*100:.1f}%"

# ---------------------------------------------------------------- 四个实验
def main():
    tasks = gen_tasks(10)                        # 40 题：4 题型 × 10，轮转交错
    train, val = tasks[:32], tasks[32:]          # 全批模式；val 每题型 2 题
    COUNTER.update(maintainer=0, proposer=0, rollout=0)

    print("=" * 72)
    print("ex1 演化循环：能力来自持久知识层，模型权重全程冻结")
    a = lambda t: model_a_naive(t)
    ws = fresh_ws("ex1")
    s0, _ = evaluate(a, val, {});  print(f"  ModelA 基线 val = {pct(s0)}")
    s1, skills, hist = evolve(a, train, val, ws)
    s1_again, _ = evaluate(a, val, skills)
    print(f"  3 轮演化后 val = {pct(s1_again)}（模型函数未改一行，技能数={len(skills)}）")
    assert s1_again > s0 + 0.3, "演化应显著提升"
    s1b, per = evaluate(a, val, skills)
    print(f"  分题型: " + ", ".join(f"{k}={v[0]}/{v[1]}" for k, v in sorted(per.items())))
    print("  ✅ 预期：miles/f2c/adddays 全修好；leap 因技能自带简化规则仍错世纪年（论文'低层workaround'镜像）")

    print("=" * 72)
    print("ex2 污染测试：坏技能被门控拒绝回滚，wiki 层不回滚、审计防重复提案")
    ws = fresh_ws("ex2")
    _, good_skills, _ = evolve(a, train, val, ws, iters=2, verbose=False)
    n_wiki_before, n_logs_before = len(ws.wiki_pages), len(ws.logs)
    # Phase B：坏提案进入候选集（模拟 Proposer 被污染轨迹带偏）
    snap = ws.snapshot_skills()
    bad = dict(applies="miles", fn=lambda t, naive: t["ans"] * 2.0, desc="[bad] 故意错误的系数")
    ws.skills["miles"] = bad
    s_cand, _ = evaluate(a, val, ws.skills)
    rejected_by_gate = not (s_cand > 0.875)
    if rejected_by_gate: ws.restore_skills(snap)     # 门控：严格提升才接受，否则回滚 skills
    ws.impact_append(dict(iter=3, skill="miles-fix(bad)", score=round(s_cand, 4),
                          result="Rejected" if rejected_by_gate else "Accepted"))
    assert rejected_by_gate and ws.skills == snap
    print(f"  坏技能候选 val={pct(s_cand)} < 最优 {pct(0.875)} → 门控拒绝，skills 回滚成功"
          f"（miles 技能恢复为正确版）")
    print(f"  wiki 页数 {n_wiki_before}→{len(ws.wiki_pages)}、logs {n_logs_before}→{len(ws.logs)}：wiki 层只增不删")
    # Phase C：审计防重复提案——删掉 adddays 技能并留下"已拒"审计，Proposer 应跳过它
    del ws.skills["adddays"]
    ws.impact_append(dict(iter=4, skill="adddays-fix", score=0.875, result="Rejected"))
    s_after, skills_after, hist = evolve(a, train, val, ws, iters=1, verbose=False)
    proposed = hist[0][2]
    print(f"  删除 adddays 技能后重演化：本轮提案={proposed or '空'}（adddays-fix 被审计拦下，不再重复提案）")
    print(f"  但 wiki/patterns/adddays.md 仍在：知识活着，下轮换个'diff'仍可再提案（严格门控排除中性提案=论文局限2镜像）")
    assert "adddays-fix" not in proposed and len(ws.wiki_pages) >= n_wiki_before
    print("  ✅ 预期：门控只回滚 skills；wiki 单调增长；skill-impact.md 审计被 Proposer 消费")

    print("=" * 72)
    print("ex3 跨模型迁移：A 的技能给 B——正迁移与负迁移并存（论文 Table 2 镜像）")
    b = lambda t: model_b_naive(t)
    wsA = fresh_ws("ex3a")
    _, skillsA, _ = evolve(a, train, val, wsA, iters=3, verbose=False)
    b0, _ = evaluate(b, val, {})
    bA, perA = evaluate(b, val, skillsA)           # 全量迁移
    # 只迁 leap 技能 = 用 A 的低层 workaround 约束本来更强的 B（负迁移子集）
    b_leap, perL = evaluate(b, val, {"leap": skillsA["leap"]} if "leap" in skillsA else {})
    print(f"  ModelB 无技能 val={pct(b0)}；全量迁移A技能 val={pct(bA)}")
    print(f"  分题型(全量迁移): " + ", ".join(f"{k}={v[0]}/{v[1]}" for k, v in sorted(perA.items())))
    print(f"  仅迁 leap 技能: leap 题 {perL.get('leap', [0,0])[0]}/{perL.get('leap', [0,1])[1]}"
          f"（B 原本全对，被 A 的简化规则带错世纪年 → 负迁移实证）")
    assert bA > b0 and perL["leap"][0] < perL["leap"][1]
    print("  ✅ 预期：共享弱点题型(miles/adddays)大幅正迁移；f2c 不变(B本来就对)；leap 子集负迁移")

    print("=" * 72)
    print("ex4 复杂度记账：全批模式下优化器组件调用数与训练集大小无关")
    t20 = tasks[:40]; t40 = tasks + gen_tasks(10)  # 造 80 题
    COUNTER.update(maintainer=0, proposer=0, rollout=0)
    w1 = fresh_ws("ex4a"); evolve(a, t20, val, w1, iters=3, verbose=False)
    m1, p1, r1 = COUNTER["maintainer"], COUNTER["proposer"], COUNTER["rollout"]
    COUNTER.update(maintainer=0, proposer=0, rollout=0)
    w2 = fresh_ws("ex4b"); evolve(a, t40, val, w2, iters=3, verbose=False)
    m2, p2, r2 = COUNTER["maintainer"], COUNTER["proposer"], COUNTER["rollout"]
    print(f"  N=40 : Wiki Maintainer 调用={m1}, Proposer 调用={p1}, rollout(推理)={r1}")
    print(f"  N=80 : Wiki Maintainer 调用={m2}, Proposer 调用={p2}, rollout(推理)={r2}")
    assert m1 == m2 and p1 == p2 and r2 > r1
    print("  ✅ 预期：维护/提案(优化器侧)调用数不随 N 翻倍；翻倍的只有推理 rollout（论文全批模式主张）")
    print("=" * 72)
    print("ALL 4 EXPERIMENTS PASSED")

if __name__ == "__main__":
    main()
