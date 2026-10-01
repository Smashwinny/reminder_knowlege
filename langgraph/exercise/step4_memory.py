# -*- coding: utf-8 -*-
# 步骤4：Checkpointer 持久化 —— 同一个 thread_id，第二次调用能接着上次的白板继续
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    draft: str; feedback: str; score: int; attempts: int

def writer(state: State) -> dict:
    n = state["attempts"] + 1
    print(f"  [写手] 接到白板 attempts={state['attempts']}，开始第 {n} 次写稿")
    return {"draft": f"第{n}版草稿", "score": min(50 + 20 * n, 100), "attempts": n}

def reviewer(state: State) -> dict:
    s = state["score"]
    print(f"  [质检] 打分 {s}")
    return {"feedback": "" if s >= 80 else "内容太单薄，请扩充"}

def gate(state: State) -> str:
    return "END" if state["score"] >= 80 else "writer"

g = StateGraph(State)
g.add_node("writer", writer); g.add_node("reviewer", reviewer)
g.add_edge(START, "writer"); g.add_edge("writer", "reviewer")
g.add_conditional_edges("reviewer", gate, {"writer": "writer", "END": END})

# 关键：编译时挂一个"存档器"。每走一步，整张白板自动存档一次
app = g.compile(checkpointer=MemorySaver())

config_a = {"configurable": {"thread_id": "文章A"}}   # 文章A的专属存档槽
config_b = {"configurable": {"thread_id": "文章B"}}   # 文章B的专属存档槽

print("== 文章A：第一轮调用（新存档）==")
app.invoke({"draft": "", "feedback": "", "score": 0, "attempts": 0}, config_a)

print("== 文章A：第二轮调用（只传一个新烂稿，不传 attempts）==")
r = app.invoke({"draft": "", "score": 0, "feedback": ""}, config_a)
print("文章A 最终白板:", r)
print("attempts 没传却自己累加到:", r["attempts"], " <- 说明它记得上次存档")

print("== 文章B：独立存档槽，互不干扰 ==")
r2 = app.invoke({"draft": "", "feedback": "", "score": 0, "attempts": 0}, config_b)
print("文章B attempts:", r2["attempts"])
