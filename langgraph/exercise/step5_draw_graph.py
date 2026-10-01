# -*- coding: utf-8 -*-
# 步骤5：把图打印成 Mermaid 代码，粘到 mermaid.live 就能看见流程图
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    draft: str; feedback: str; score: int; attempts: int

def writer(state: State) -> dict: ...
def reviewer(state: State) -> dict: ...

g = StateGraph(State)
g.add_node("writer", writer); g.add_node("reviewer", reviewer)
g.add_edge(START, "writer"); g.add_edge("writer", "reviewer")
g.add_conditional_edges("reviewer", lambda s: "END" if s["score"] >= 80 else "writer",
                        {"writer": "writer", "END": END})
app = g.compile()
print(app.get_graph().draw_mermaid())
