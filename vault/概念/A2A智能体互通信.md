---
tags: [概念]
领域: AI Agent / 通信协议
别名: [A2A, Agent-to-Agent, AgentCard, 智能体名片]
首次来源: "[[项目笔记/agentic_design_patterns]]"
---

# A2A 智能体互通信

**一句话定义**：Agent 与 Agent 之间互相发现、互相调用的开放协议——每个 Agent 发布一张 AgentCard"名片"（JSON：我能干什么/怎么调我/要什么参数），对方读了名片就能直接委派任务，《Agentic Design Patterns》模式 15。

**属于领域**：AI Agent 通信协议

**通俗理解**：[[MCP协议]] 是"Agent ↔ 工具"的USB接口，A2A 是"Agent ↔ Agent"的名片交换。前台 WeatherBot 在名片里写明"我报天气，给我城市名返回 JSON"，你的 Agent 读了名片就能把天气查询整单外包，不必知道对方内部用什么框架。

**书中三块内容**：AgentCard 定义、同步与流式请求、完整 A2A 交互示例。

**与已有概念的关联**：
- [[MCP协议]]：互补不重叠——MCP 连工具（能力复用），A2A 连 Agent（任务委派）；两者共同解 [[M×N集成问题]]
- [[多智能体协作]] / [[Agent输出协议契约]]：A2A 是协作的通信底座，交付物协议在 A2A 之上
- [[Agent设计模式目录]]：模式 15

**首次接触于**：[[项目笔记/agentic_design_patterns]]
