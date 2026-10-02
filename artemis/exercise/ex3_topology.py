# -*- coding: utf-8 -*-
"""ex3: 仓库拓扑静态分析——用代码量证明架构描述不是吹的。

从源码里直接提取三类事实：
  A. Pro 模式 LangGraph 图的节点与边（graph.py 源码级提取）
  B. 设备动作集（action_specs.py 声明的动作名）
  C. 各 Agent 角色的代码规模（agents/ 目录行数）

运行（在 repo 目录下）：
    uv run python ../exercise/ex3_topology.py
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent / "repo"


def extract_graph() -> dict:
    """从 graph.py 提取 add_node / add_edge / add_conditional_edges。"""
    src = (REPO / "artemis" / "graph" / "graph.py").read_text(encoding="utf-8")
    nodes = re.findall(r'add_node\("([\w_]+)"', src)
    edges = re.findall(r'add_edge\("([\w_]+)",\s*"([\w_]+)"\)', src)
    cond = re.findall(
        r'add_conditional_edges\(\s*"([\w_]+)"', src
    )
    return {"nodes": nodes, "edges": [f"{a} -> {b}" for a, b in edges],
            "conditional_from": cond}


def extract_actions() -> list[str]:
    """从 action_specs.py 提取声明的设备动作名。"""
    src = (REPO / "artemis" / "mcp" / "action_specs.py").read_text(encoding="utf-8")
    return re.findall(r'name="(\w+)"', src)


def agent_sizes() -> list[tuple[str, int]]:
    """统计 agents/ 下每个角色的 .py 总行数。"""
    base = REPO / "artemis" / "agents"
    out = []
    for d in sorted(base.iterdir()):
        if d.is_dir():
            n = sum(len(p.read_text(encoding="utf-8").splitlines())
                    for p in d.rglob("*.py"))
            out.append((d.name, n))
        elif d.suffix == ".py":
            out.append((d.stem, len(d.read_text(encoding="utf-8").splitlines())))
    return sorted(out, key=lambda x: -x[1])


def main() -> None:
    g = extract_graph()
    print("== A. Pro 模式 LangGraph 拓扑（源码提取）==")
    print(f"节点 {len(g['nodes'])} 个: {g['nodes']}")
    print(f"固定边 {len(g['edges'])} 条:")
    for e in g["edges"]:
        print(f"    {e}")
    print(f"条件边从 {len(g['conditional_from'])} 个节点出发: {g['conditional_from']}")

    acts = extract_actions()
    print(f"\n== B. 设备动作集：{len(acts)} 个 ==")
    print("    " + ", ".join(acts))

    print("\n== C. Agent 角色代码规模（.py 行数，降序）==")
    for name, n in agent_sizes():
        print(f"    {name:<20} {n:>6} 行")

    # 断言：架构文档说的关键角色必须真实存在
    assert set(["planner", "operator", "validator", "summarizer",
                "execution_check", "perception", "exit_settlement"]) <= set(g["nodes"])
    assert {"click", "swipe", "input_text", "press_key"} <= set(acts)
    print("\n✅ 断言通过：Pro 图 7 节点 + 设备动作集与文档描述一致，拓扑提取已存 exercise/pro_graph.json")
    (Path(__file__).parent / "pro_graph.json").write_text(
        json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
