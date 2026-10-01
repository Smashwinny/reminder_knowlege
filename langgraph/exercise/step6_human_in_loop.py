# -*- coding: utf-8 -*-
# 步骤6：interrupt —— 质检通过后先"暂停等人审批"，人点头了才发布
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command

class State(TypedDict):
    draft: str; score: int; attempts: int; approved: bool

def writer(state: State) -> dict:
    n = state["attempts"] + 1
    return {"draft": f"第{n}版草稿", "score": min(50 + 20 * n, 100), "attempts": n}

def reviewer(state: State) -> dict:
    s = state["score"]
    return {"score": s}

def publisher(state: State) -> dict:
    # interrupt(): 图在这里暂停，把问题抛给人；人的回答通过 Command(resume=...) 送回来
    answer = interrupt({"question": "文章质检通过，是否发布？", "draft": state["draft"]})
    return {"approved": answer == "yes"}

def gate(state: State) -> str:
    return "publisher" if state["score"] >= 80 else "writer"

g = StateGraph(State)
g.add_node("writer", writer); g.add_node("reviewer", reviewer); g.add_node("publisher", publisher)
g.add_edge(START, "writer"); g.add_edge("writer", "reviewer")
g.add_conditional_edges("reviewer", gate, {"publisher": "publisher", "writer": "writer"})
g.add_edge("publisher", END)
app = g.compile(checkpointer=MemorySaver())   # interrupt 必须有存档器才能"冻住"

cfg = {"configurable": {"thread_id": "demo"}}

print("== 第一次 invoke：跑到 interrupt 处暂停 ==")
r1 = app.invoke({"draft": "", "score": 0, "attempts": 0, "approved": False}, cfg)
print("返回:", r1["__interrupt__"][0].value)   # 人看到的问题

print("== 人审批：回复 yes，图从暂停点继续 ==")
r2 = app.invoke(Command(resume="yes"), cfg)
print("最终白板:", {k: r2[k] for k in ("draft", "score", "attempts", "approved")})
