---
tags: [概念]
领域: AI Agent / Harness 工程
别名: ["Harness as a Service", "Agents API", "Session as a Resource", "会话即资源", "托管智能体挽具"]
首次来源: "[[项目笔记/openai-agents-api]]"
---

# 托管Harness与会话即资源

**一句话定义**：把开源 harness 整体搬上云端变成 API——你的应用只发任务、收事件，模型循环/上下文压缩/断点恢复/subagent 调度/沙箱运维全由厂商代管；核心资源是 **Session**（`sess_` id 的持久对象，可 create/retrieve/update/delete，像管数据库记录一样管一个"在岗的 agent"）。

**属于领域**：AI Agent / Harness 工程（[[AgentHarness智能体挽具]] 的云服务形态）

**通俗理解**：已学的 LangGraph/checkpointer 是"买机器回家自己开车间"；Agents API 是"租一条现成生产线"——2026-09-10 OpenAI 把自家 Codex 背后的 harness（[[AgentHarness智能体挽具]] 七职责的全部实现，开源在 openai/codex，131 crates / 200 万行 Rust）托管成 `POST /v1/agents/sessions`。代价：锁 OpenAI 生态、数据仅美国驻留且不支持 ZDR、沙箱容器按时长计费（真正的账单放大器）。

**三层运行时怎么选**（官方口径）：要代驾→Agents API（OpenAI runs a managed Codex harness）；要方向盘→Agents SDK（循环在你的进程，即 [[智能体框架]] 的 OpenAI 版）；只要发动机→Responses API。注意 `openai-agents` pip 包（2025-03 的 SDK）和新 Agents API 是两代东西，SDK≥3.x 才有 `client.beta.agents` 命名空间（实测 2.54.0 没有、3.24.0 有 161 个 agent 类型）。

**四概念咬合**：Agent（模型+指令+工具+MCP 的配置包）· Environment（工位，见 [[沙箱三态与Executor]]）· Session（在册员工，跨轮次持久）· Events & Items（工作日志，subagent 的创建/打断/关闭也是 item）。压缩恢复侧官方托管化了 [[上下文预算与战略压缩]] 与 [[Checkpoint存档与持久执行]]（源码坐标 core/src/compact.rs，CompactionReason/CompactionSummary 一等公民）；编排侧 harness 自主拆解 subagent（对照 [[工单任务图与前沿调度]]：你画 DAG vs 它自己招临时工）。

**与已有概念的关联**：
- [[AgentHarness智能体挽具]]：本概念是它的 SaaS 化；"改环境胜过改形容词"被 OpenAI 直接做成了商业模式
- [[程序化工具调用]]：CodeAct 被产品化为一个开关 `{"type": "programmatic_tool_calling"}`
- [[Checkpoint存档与持久执行]]：服务端替你存档续跑（流断了 retrieve session/items 续传）
- [[多Agent协作乱序竞态]]：并行 subagent 的完成序≠依赖序，汇总仍要防
- [[控制面与数据面]]：无 key 请求 401 "A valid actor biscuit is required"（内部鉴权术语），认证在控制面前置

**首次接触于**：[[项目笔记/openai-agents-api]]
