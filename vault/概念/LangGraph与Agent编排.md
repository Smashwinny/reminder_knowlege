---
tags: [概念]
领域: AI / LLM 应用
别名: [LangGraph, 状态图, 状态图编排, StateGraph, Agent 编排, 图编排]
首次来源: "[[项目笔记/langchain]]"
---

# LangGraph 与 Agent 编排

**一句话定义**：LangGraph 是 Agent 运行时引擎——用"状态图"（节点=干活的步骤，边=跳转规则，全局 State=所有节点共读共写的数据如消息列表）来编排 LLM 应用；LangChain v1 的 `create_agent` 返回的就是一张编译后的 LangGraph 图（CompiledStateGraph）。

**属于领域**：LLM 应用 / 工作流编排

**通俗理解**：普通 while 循环只能"模型↔工具转到天荒地老"；状态图是**带路由的地铁图**——可以在某些站点要求人工审批（human-in-the-loop）、某条线故障退回上一站（错误回退）、中途出站次日刷卡再进站继续坐（checkpointer 持久化断点续跑）、多条线路协作（多 Agent）。基础的 Agent 循环就是这张图上最简单的"两站环线"。

**核心构件**（langgraph 项目亲手实验后的补全）：Node（普通 Python 函数，读白板快照、返回增量 dict，节点里想调 LLM 就调、不调也行）、State（共享白板，见 [[共享状态与Reducer]]）、Conditional Edge（裁判函数读白板返回字符串决定下一站，循环就是一条画回上游的边）、Checkpointer（每步快照存档，见 [[Checkpoint存档与持久执行]]）、interrupt/Command(resume)（见 [[人机协同Interrupt]]）。手写 while+if 的四大痛点——状态散落、循环写死、断掉全完、流程不可视——全被图结构解决。

**与已有概念的关联**：
- 思想同源：[[构建流水线与Pass]]（复杂工作拆成顺序阶段，但图允许分叉/回路/暂停；流水线是"只进不退"的状态图特例）
- 是 Gate 的工业化实现：[[质检Gate与自我纠错循环]]（条件边="打回重写"只是一条普通的边）
- 承载：[[Agent循环]]
- 相关联动：[[LLM工具调用]]
- 支撑件：[[共享状态与Reducer]]、[[Checkpoint存档与持久执行]]、[[人机协同Interrupt]]

**首次接触于**：[[项目笔记/langchain]]，深化于 [[项目笔记/langgraph]]
