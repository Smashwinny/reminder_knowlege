---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/langchain-ai/langgraph
完成日期: 2026-10-01
---

# langgraph

**这是什么**（一句话）：构建有状态 Agent 的底层编排框架——共享白板（State）+ 节点路线图（Graph）+ 每步存档机（Checkpointer）。

**它给我什么能力**：有状态多节点编排、条件分支与循环、每步持久化与断点恢复（Durable Execution）、人机协同暂停点（interrupt）、并行分支 + Reducer 合并、流式输出、draw_mermaid 一键流程图、子图嵌套、prebuilt 的 create_react_agent 快速配方。

**引入的概念**：
- [[状态图编排]]
- [[共享状态与Reducer]]
- [[Checkpoint存档与持久执行]]
- [[人机协同Interrupt]]
- 强化：[[质检Gate与自我纠错循环]]（条件边 = Gate 的工业化实现）、[[构建流水线与Pass]]（流水线是状态图的特例）、[[确定性脚本]]（条件边裁判函数可直接单测）

**实验记录**（做了什么、结果、坑）：
- 实验：`exercise\` 里 6 步纯 Python 实验（零 API key）：①State+两节点最简图 ②条件边"70 分打回→90 分过审"循环 ③stream() 分步直播 ④MemorySaver + thread_id 跨调用记忆（第二轮不传 attempts，从存档补齐后累加到 3）⑤draw_mermaid 出图 ⑥interrupt 冻结→Command(resume) 唤醒审批。全部命令实际执行验证，输出见 PDF《LangGraph-小白指南.pdf》。
- 坑 1：`invoke` 的输入 dict 键名打错（多了个空格），报 `KeyError: 'attempts'` 且栈很深——白板字段名建议集中定义避免手写两遍。
- 坑 2：实验初版写手第一稿就 80 分过审，循环没发生；把初始分调低到 70 才让"打回重写"可见。**设计实验要让关键机制真实触发**。
- 坑 3：`interrupt` 必须在 compile 时挂 checkpointer，否则无法冻结。

**后续可深入的方向**：
- 用 langchain-openai 接真 LLM，把 writer/reviewer 换成真实模型 + create_react_agent
- subgraph 子图嵌套、Send API 并行 fan-out
- SqliteSaver/PostgresSaver 落盘存档
- 给 img2threejs 的生成流水线换 LangGraph 引擎重写
- LangSmith 观测 trace
