---
tags: [概念]
领域: AI Agent / 设计模式
别名: [Agentic Design Patterns, 21模式, Gulli设计模式, Agent模式地图]
首次来源: "[[项目笔记/agentic_design_patterns]]"
---

# Agent 设计模式目录

**一句话定义**：Antonio Gulli（Google）开源书《Agentic Design Patterns》把构建 AI Agent 时反复出现的 21 种结构解法逐一命名（424 页 + 全套 notebooks，LangChain/LangGraph·CrewAI·ADK 三画布对照），是 Agent 时代的 GoF 设计模式。

**属于领域**：AI Agent 架构 / 软件设计模式

**通俗理解**：像 1994 年 GoF 给面向对象编程的"单例/观察者/工厂"命名一样，把 Agent 开发里大家反复在写的结构起名字——起名之后才能跨项目复用、才能"对号入座"地诊断系统。Google Cloud 官方架构文档已直接引用其分类。

**21 模式四层地图**（记忆口诀：单兵 → 团队 → 安全带 → 教练）：
1. **基础编排**（单 Agent）：1 提示链 [[提示链PromptChaining]] · 2 路由 · 3 并行化 [[并行化编排Parallelization]] · 4 反思 [[反思模式Reflection]] · 5 工具使用 · 6 规划
2. **协作通信**：7 多智能体协作（见 [[多智能体协作]]）· 8 记忆管理（见 [[三层记忆]]）· 9 自适应 · 10 MCP（见 [[MCP协议]]）· 15 A2A（[[A2A智能体互通信]]）
3. **可靠性安全**：11 目标监控 · 12 异常恢复 · 13 人在回路（见 [[人机协同Interrupt]]）· 14 RAG（见 [[RAG检索增强生成]]）· 18 护栏 [[护栏模式Guardrails]]
4. **元能力**：16 资源感知 · 17 推理技术 · 19 评估 [[LLM裁判与自动评估]] · 20 优先级 · 21 探索发现

**Level 0-3 复杂度分级**（书的升级路线图）：L0 裸 LLM → L1 接工具/RAG（连接者）→ L2 规划+反思+记忆（战略家）→ L3 多 Agent 协作系统。想升级就补对应层的模式。

**与已有概念的关联**：
- [[Agent循环]]：模式 4/5/6 的组合体；提示链是其反面（不给自主权）
- [[AgentHarness智能体挽具]]：harness 是跨模式的总装车间；本书是零件目录
- [[技能路由器与授权硬门]] / [[能力层与后端路由]]：路由模式的领域特例

**首次接触于**：[[项目笔记/agentic_design_patterns]]
