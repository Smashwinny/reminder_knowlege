---
tags: [概念]
领域: AI / Agent 编排
别名: [Checkpointer, 持久执行, Durable Execution, 断点恢复]
首次来源: "[[项目笔记/langgraph]]"
---

# Checkpoint 存档与持久执行

**一句话定义**：图每执行完一个节点，自动把整块共享状态拍快照存档；进程崩溃或任务暂停后，可从最近快照原样恢复继续执行，已完成的节点不重跑。

**属于领域**：分布式系统 / Agent 编排（LangGraph 术语：Durable Execution 持久执行）

**通俗理解**：像游戏通关前的存档点——打到第三关崩了，重开时从第三关门口继续，而不是从头打。在 LLM 应用里这直接省钱：重跑 = 重新花钱调 API。存档器可插拔：学习用 MemorySaver（内存），生产换 SqliteSaver / PostgresSaver，业务代码一行不改。存档按 thread_id 分槽（见下），一个编译好的图靠不同 thread_id 同时服务无数用户，"服务记得你"的底层就是这个。

**与已有概念的关联**：
- 属于：[[LangGraph与Agent编排]]（引擎的第三大件）
- 前置：[[确定性脚本]]（快照能恢复的前提是节点行为可复现）
- 支撑：[[人机协同Interrupt]]（"暂停等人"就是存档+退出）

**首次接触于**：[[项目笔记/langgraph]]
