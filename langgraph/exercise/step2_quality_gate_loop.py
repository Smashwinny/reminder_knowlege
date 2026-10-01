# -*- coding: utf-8 -*-
# 步骤2：条件边做"质检 Gate"——分数不够就打回重写，形成循环
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    draft: str
    feedback: str
    score: int
    attempts: int   # 防止死循环的计数器

def writer(state: State) -> dict:
    n = state["attempts"] + 1
    print(f"  [写手] 第 {n} 次写稿，参考上一轮反馈: {state['feedback'] or '（首次，无反馈）'}")
    # 模拟：每重写一次，文章质量提高 20 分
    return {"draft": f"第{n}版草稿", "score": min(50 + 20 * n, 100), "attempts": n}

def reviewer(state: State) -> dict:
    s = state["score"]
    passed = s >= 80
    print(f"  [质检] 打分 {s} 分 -> {'通过' if passed else '打回重写'}")
    return {"feedback": "" if passed else "内容太单薄，请扩充"}

def gate(state: State) -> str:          # 条件边：看分数决定下一站
    return "END" if state["score"] >= 80 else "writer"

g = StateGraph(State)
g.add_node("writer", writer)
g.add_node("reviewer", reviewer)
g.add_edge(START, "writer")
g.add_edge("writer", "reviewer")
g.add_conditional_edges("reviewer", gate, {"writer": "writer", "END": END})
app = g.compile()

result = app.invoke({"draft": "", "feedback": "", "score": 0, "attempts": 0})
print("最终白板:", result)
