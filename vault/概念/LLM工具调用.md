---
tags: [概念]
领域: AI / LLM 应用
别名: [Tool Calling, Function Calling, 工具调用, bind_tools]
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

**首次接触于**：[[项目笔记/langchain]]
