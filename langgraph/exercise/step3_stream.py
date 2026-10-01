# -*- coding: utf-8 -*-
# 步骤3：stream() —— 每走完一个节点，立刻吐出白板快照（全程可观察）
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    draft: str; feedback: str; score: int; attempts: int

def writer(state: State) -> dict:
    n = state["attempts"] + 1
    return {"draft": f"第{n}版草稿", "score": min(50 + 20 * n, 100), "attempts": n}

def reviewer(state: State) -> dict:
    s = state["score"]
    return {"feedback": "" if s >= 80 else "内容太单薄，请扩充"}

def gate(state: State) -> str:
    return "END" if state["score"] >= 80 else "writer"

g = StateGraph(State)
g.add_node("writer", writer); g.add_node("reviewer", reviewer)
g.add_edge(START, "writer"); g.add_edge("writer", "reviewer")
g.add_conditional_edges("reviewer", gate, {"writer": "writer", "END": END})
app = g.compile()

# 和 invoke 的唯一区别：invoke 只给最终结果，stream 每步都给
for i, update in enumerate(app.stream({"draft": "", "feedback": "", "score": 0, "attempts": 0})):
    print(f"--- 第 {i+1} 步完成，白板更新 ---")
    print(update)
