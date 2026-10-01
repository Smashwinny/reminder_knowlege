# -*- coding: utf-8 -*-
# 步骤1：定义共享状态(State) + 两个节点(Node)，连成最简单的图
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. 共享状态：整张图流转的"一块白板"，每个节点读写它
class State(TypedDict):
    draft: str      # 当前文章草稿
    score: int      # 质检分数

# 2. 节点：就是一个普通的 Python 函数，读状态 -> 干活 -> 写回状态
def writer(state: State) -> dict:
    print("  [写手] 根据白板内容写文章...")
    return {"draft": "LangGraph 是一个状态图编排框架。"}  # 写回白板

def reviewer(state: State) -> dict:
    print("  [质检] 给文章打分...")
    return {"score": 85}                                  # 写回白板

# 3. 连图：白板 -> 写手 -> 质检 -> 结束
g = StateGraph(State)
g.add_node("writer", writer)
g.add_node("reviewer", reviewer)
g.add_edge(START, "writer")
g.add_edge("writer", "reviewer")
g.add_edge("reviewer", END)
app = g.compile()

# 4. 运行：一块空白白板进去，写满的白板出来
result = app.invoke({"draft": "", "score": 0})
print("最终白板:", result)
