---
tags: [概念]
领域: AI / LLM 应用
别名: [Tool Calling, Function Calling, 工具调用, bind_tools, 工具调用FunctionCalling]
首次来源: "[[项目笔记/langchain]]"
---

# LLM 工具调用

**一句话定义**：让 LLM"使用工具"的机制——实际上 LLM 只输出一段结构化文字（"我要调 add，参数 128 和 64"），**真正执行函数的是你机器上的框架**，执行结果再作为 ToolMessage 回填给模型。

**属于领域**：LLM 应用开发

**通俗理解**：像**餐厅点菜**——LLM 是只会说话、不能进厨房的顾客：看到菜单（工具说明书 = 函数名 + docstring + 参数 JSON Schema）后写下"点单"（tool_calls JSON）；服务员（LangGraph 工具节点）拿单子去厨房（你的 Python 函数）真正炒菜，再把菜端回来（ToolMessage 回填）。⚠️ 最大误解纠正：**LLM 从头到尾没有执行任何代码，它只是"点了菜"**。安全推论：工具=把执行权交给模型决策，危险操作必须在函数内部加限制。

**与已有概念的关联**：
- 相关：[[ChatModel与消息类型]]（bind_tools 发菜单，ToolMessage 上菜）
- 相关：[[Agent循环]]（工具调用是循环的驱动事件）
- 相关：[[质检Gate与自我纠错循环]]（参数校验失败回传错误，模型自纠）
- crewAI 视角：继承 `BaseTool` 实现 `_run` 即发一件工具；实测日志 "Tool Output: 红烧肉 12元…"，模型推荐的价格只能来自工具——调用生效的铁证
- agno 视角（awesome-llm-apps 实测）：把**普通 Python 函数**直接塞进 `Agent(tools=[now_time, calculator])` 即可，框架自动读函数签名+docstring 生成"菜单"；GLM-4.6 为数学题主动调 `calculator(expression=3e5 * 365 * 24 * 3600)`、为时间问题调 `now_time()`，不心算不编造——菜单机制生效
- 三个易混物对比：**Tool**=函数代码（给程序执行）｜**[[AgentSkills技能包]]**=方法论文档+脚本（给 LLM 读）｜**[[MCP模型上下文协议]]**=跨应用连接标准（M×N 变 M+N，见 [[M×N集成问题]]）

**首次接触于**：[[项目笔记/langchain]]（另见 [[项目笔记/crewai]]、[[项目笔记/awesome-llm-apps]]）
