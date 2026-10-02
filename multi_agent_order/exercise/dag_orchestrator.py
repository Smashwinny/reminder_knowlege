# -*- coding: utf-8 -*-
"""
多 Agent 协作乱序问题：复现与治理（动手实验）
来源：抖音视频《两年大模型开发，被一个多 Agent 协作乱序问题干沉默了》技术主线还原

场景：一个"行业周报编辑部"由 4 个 Agent 组成
  A 抓数据(0.8s)  ->  C 写摘要(依赖 A+B)
  B 查新闻(0.2s)  ->  D 排版(依赖 C)

子命令：
  python dag_orchestrator.py race      步骤1  复现：全员并发、完成即合流 -> 报告乱序 + 摘要拿到空数据
  python dag_orchestrator.py cycle     步骤2  循环依赖：C依赖A且A依赖C -> 计划阶段就报错
  python dag_orchestrator.py dag       步骤3  修复：DAG拓扑 + 前沿调度 -> 顺序正确、摘要有数据
  python dag_orchestrator.py heal      步骤4  故障自愈：B前两次故意失败，重试后周报照常完成
  python dag_orchestrator.py protocol  步骤5  输出协议：schema校验拒绝坏结果 + 双源数据冲突消解
"""
import sys
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

random.seed(42)  # 固定随机种子，结果可复现

# ---------------------------------------------------------------- 公共部分
AGENTS = {
    "A_抓数据": {"sleep": 0.8, "deps": []},
    "B_查新闻": {"sleep": 0.2, "deps": []},
    "C_写摘要": {"sleep": 0.1, "deps": ["A_抓数据", "B_查新闻"]},
    "D_排版":   {"sleep": 0.05, "deps": ["C_写摘要"]},
}

DATA_SOURCE = {"rows": 42}  # A 抓数据后才知道的"真相"

def run_agent(name, shared):
    """模拟一个 Agent 干活：睡 sleep 秒后把自己的产出写进 shared（共享上下文）"""
    spec = AGENTS[name]
    time.sleep(spec["sleep"])
    if name == "A_抓数据":
        shared["data_rows"] = DATA_SOURCE["rows"]
        return f"[数据] 本周共采集 {shared['data_rows']} 条行业数据"
    if name == "B_查新闻":
        return "[新闻] 本周 3 条要闻：模型降价 / 新框架发布 / 融资"
    if name == "C_写摘要":
        rows = shared.get("data_rows")  # 关键：摘要依赖 A 的数据
        return f"[摘要] 综合数据({rows} 条)与新闻，本周行业平稳向好"
    if name == "D_排版":
        return "[排版] 周报已生成 PDF"
    raise ValueError(name)

# ---------------------------------------------------------------- 步骤1：复现乱序
def race():
    print("== 步骤1 复现：全员并发、完成即合流（天真写法）==")
    shared, sections, order = {}, [], []
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(run_agent, n, shared): n for n in AGENTS}
        for fut in as_completed(futures):          # 谁先完成就先收谁的
            name = futures[fut]
            sections.append(fut.result())
            order.append((name, round(time.perf_counter() - t0, 2)))
    print("完成顺序（时间秒）:", order)
    print("\n最终周报（按完成顺序拼接）:")
    for s in sections:
        print("  " + s)
    print("\n[坑] 完成顺序 = %s，而不是依赖顺序 A→B→C→D" % "→".join(n for n, _ in order))
    print("[坑] 摘要里 'data_rows' 在 C 运行时还没被 A 写入 -> 摘要拿到 None（空数据定稿）")

# ---------------------------------------------------------------- 步骤2：循环依赖检测
def cycle():
    print("== 步骤2 循环依赖：计划阶段就该被拦下 ==")
    bad = {n: list(s["deps"]) for n, s in AGENTS.items()}
    bad["A_抓数据"] = ["C_写摘要"]                 # 人为加一条：A 依赖 C -> A↔C 成环
    try:
        topo_sort(bad)
        print("未检测到环？不应该走到这里")
    except ValueError as e:
        print("ValueError:", e)
        print("[结论] 环必须在规划期发现，否则调度器运行时会死等，谁也开不了工")

def topo_sort(deps):
    """Kahn 拓扑排序；有环则抛 ValueError（cycle 成员也一并报出）"""
    indeg = {n: 0 for n in deps}
    dependents = {n: [] for n in deps}
    for n, ds in deps.items():
        for d in ds:
            indeg[n] += 1
            dependents[d].append(n)
    queue = [n for n, k in indeg.items() if k == 0]
    order = []
    while queue:
        n = queue.pop()
        order.append(n)
        for m in dependents[n]:
            indeg[m] -= 1
            if indeg[m] == 0:
                queue.append(m)
    if len(order) != len(deps):
        stuck = sorted(n for n, k in indeg.items() if k > 0)
        raise ValueError(f"循环依赖！这些节点永远入不了队: {stuck}")
    return order

# ---------------------------------------------------------------- 步骤3：DAG 前沿调度（修复版）
def dag():
    print("== 步骤3 修复：DAG 拓扑 + 前沿(frontier)调度 ==")
    print("拓扑序检查:", " → ".join(topo_sort({n: s["deps"] for n, s in AGENTS.items()})))
    deps = {n: list(s["deps"]) for n, s in AGENTS.items()}
    dependents = {n: [] for n in AGENTS}
    for n, ds in deps.items():
        for d in ds:
            dependents[d].append(n)
    remaining = {n: len(ds) for n, ds in deps.items()}
    ready = [n for n, k in remaining.items() if k == 0]
    shared, sections, done_order = {}, {}, {}
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as pool:
        pending = {pool.submit(run_agent, n, shared): n for n in ready}
        print("初始前沿(入度0，可立即并发):", [pending[f] for f in pending])
        while pending:
            fut = next(as_completed(pending))
            name = pending.pop(fut)
            sections[name] = fut.result()
            done_order[name] = round(time.perf_counter() - t0, 2)
            for m in dependents[name]:              # 完工一张工单，前沿推进一格
                remaining[m] -= 1
                if remaining[m] == 0:
                    pending[pool.submit(run_agent, m, shared)] = m
                    print(f"  [{done_order[name]}s] {name} 完工 -> {m} 入前沿")
    print("完成时间:", done_order)
    print("\n最终周报（严格按依赖顺序拼接）:")
    for n in topo_sort(deps):
        print("  " + sections[n])
    print("\n[验证] 摘要拿到的是 42 条（A 先于 C 完成才允许 C 开工）——乱序问题消失")

# ---------------------------------------------------------------- 步骤4：故障自愈
def run_agent_flaky(name, shared, fail_times):
    """B 前两次故意抛异常，模拟真实世界的执行失败"""
    if name == "B_查新闻" and fail_times["B_查新闻"] < 2:
        fail_times["B_查新闻"] += 1
        raise ConnectionError(f"{name} 第{fail_times['B_查新闻']}次调用超时")
    return run_agent(name, shared)

def heal():
    print("== 步骤4 故障自愈：失败自动重试，周报照常交付 ==")
    fail_times = {"B_查新闻": 0}
    deps = {n: list(s["deps"]) for n, s in AGENTS.items()}
    dependents = {n: [] for n in AGENTS}
    for n, ds in deps.items():
        for d in ds:
            dependents[d].append(n)
    remaining = {n: len(ds) for n, ds in deps.items()}
    ready = [n for n, k in remaining.items() if k == 0]
    shared, sections = {}, {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        pending = {pool.submit(run_agent_flaky, n, shared, fail_times): (n, 1) for n in ready}
        while pending:
            fut = next(as_completed(pending))
            name, attempt = pending.pop(fut)
            try:
                sections[name] = fut.result()
                print(f"  OK  {name}（第{attempt}次尝试）")
                for m in dependents[name]:
                    remaining[m] -= 1
                    if remaining[m] == 0:
                        pending[pool.submit(run_agent_flaky, m, shared, fail_times)] = (m, 1)
            except (ConnectionError, TimeoutError) as e:
                print(f"  FAIL {name}（第{attempt}次）: {e}")
                if attempt < 3:
                    pending[pool.submit(run_agent_flaky, name, shared, fail_times)] = (name, attempt + 1)
                else:
                    sections[name] = f"[降级] {name} 三次失败，用缓存旧新闻占位"
                    print(f"  降级 {name}")
    print("\n最终周报:")
    for n in topo_sort(deps):
        print("  " + sections[n])
    print("\n[验证] B 失败 2 次被自动重试救回，全链路无人工介入完成交付")

# ---------------------------------------------------------------- 步骤5：输出协议 + 冲突消解
PROTOCOL = {"agent": str, "section": str, "content": str, "confidence": (int, float)}

def validate(msg):
    """标准化输出协议校验：字段齐、类型对，才算合格交付物"""
    if not isinstance(msg, dict):
        return f"拒绝：不是 dict，是 {type(msg).__name__}"
    for k, t in PROTOCOL.items():
        if k not in msg:
            return f"拒绝：缺字段 {k}"
        if not isinstance(msg[k], t):
            return f"拒绝：字段 {k} 类型应为 {t}，实际 {type(msg[k]).__name__}"
    return None

def protocol():
    print("== 步骤5 输出协议校验 + 双源数据冲突消解 ==")
    inbox = [
        {"agent": "数据源1", "section": "数据", "content": "本周 40 条数据", "confidence": 0.6},
        {"agent": "数据源2", "section": "数据", "content": "本周 42 条数据", "confidence": 0.95},
        {"agent": "摘要员", "content": "本周行业平稳向好"},                 # 缺 section/confidence
        "本周数据 99 条",                                                # 根本不是 dict
    ]
    merged = {}
    for msg in inbox:
        err = validate(msg)
        if err:
            print(f"  校验: {err}  <- 来自 {msg if isinstance(msg, str) else msg.get('agent')}")
            continue
        prev = merged.get(msg["section"])
        if prev and prev["content"] != msg["content"]:   # 口径不一 -> 冲突消解：信 confidence 高的
            winner = max(prev, msg, key=lambda m: m["confidence"])
            print(f"  冲突: {prev['agent']}({prev['confidence']}) vs {msg['agent']}({msg['confidence']}) -> 采信 {winner['agent']}")
            merged[msg["section"]] = winner
        else:
            merged[msg["section"]] = msg
    print("\n合流后的周报素材（口径已统一）:")
    for sec, m in merged.items():
        print(f"  [{sec}] {m['content']}  (来源: {m['agent']})")
    print("\n[验证] 坏格式 2 条被协议门拦下；两份数据冲突按置信度统一为 42 条")

if __name__ == "__main__":
    cmds = {"race": race, "cycle": cycle, "dag": dag, "heal": heal, "protocol": protocol}
    if len(sys.argv) != 2 or sys.argv[1] not in cmds:
        print(__doc__)
        sys.exit(1)
    cmds[sys.argv[1]]()
