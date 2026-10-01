---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/langchain-ai/langchain
完成日期: 2026-10-01
---

# LangChain

**这是什么**（一句话）：AI Agent 工程平台——把"大语言模型 + 工具 + 数据"组装成能自动干活的 AI 应用的框架；v1 起核心是 `create_agent`（底层由 LangGraph 状态图引擎驱动）。

**它给我什么能力**：
1. 统一模型接口（`init_chat_model` 一行换供应商）
2. `@tool` + `create_agent` 组装能自己决定调什么工具的智能体
3. RAG 组件（embeddings / vectorstores / text-splitters）做文档问答
4. 结构化输出做信息抽取
5. middleware + checkpointer 做人工审批、记忆压缩、断点续跑
6. LangGraph 图编排做多 Agent 协作

**引入的概念**：
- [[ChatModel与消息类型]]
- [[LLM工具调用]]
- [[Agent循环]]
- [[RAG检索增强生成]]
- [[提示词模板]]
- [[LangGraph与Agent编排]]
- [[Agent中间件]]

**实验记录**（做了什么、结果、坑）：
- 主实验《零成本拆解一个 AI Agent》5 步全部离线跑通（`exercise\exp1~5.py`，langchain 1.4.3 + Python 3.14.7，无需 API Key）：
  - exp1 FakeListChatModel 基本对话；exp2 @tool 生成 JSON Schema 说明书；exp3 create_agent 消息循环实测 4 条消息；exp4 模型传错参数（b="zero"）→ 校验错误 ToolMessage 回流 → 模型自动改对；exp5 stream 逐片段输出。
- **坑 1**：`GenericFakeChatModel` 没实现 `bind_tools`，直接喂给 `create_agent` 会 `NotImplementedError`——需子类补一个 `def bind_tools(self, tools, **kwargs): return self`。
- **坑 2**：工具内主动 raise 自定义异常（如 ValueError）默认**不会**被兜底成 ToolMessage，会直接炸掉 Agent 循环；默认只兜参数校验错误（包装为 ToolInvocationError）。想自纠错：要么靠参数类型校验，要么工具内部 try/catch 返回错误文字。
- **坑 3**：中文 Windows 先 `setx PYTHONUTF8 1`。
- 仓库结构：`libs/core`（langchain_core 协议地基）/ `libs/langchain_v1`（主包）/ `libs/partners`（各家模型集成）/ LangGraph（独立仓库，v1 的引擎）。

**后续可深入的方向**：
- 接真模型重跑实验（ollama 本地免费 或 langchain-openai）
- RAG 实战：把自己笔记库做成问答机器人
- middleware 源码：`libs/langchain_v1/langchain/agents/middleware/`
- LangSmith 可观测性（商业产品）
