---
tags: [概念]
领域: AI 工具生态
别名: ["MCP Server"]
首次来源: "[[项目笔记/mcp_servers]]"
---

# MCP服务器

**一句话定义**：按 MCP 协议把某种能力（文件、API、数据库…）暴露给 AI 应用的独立程序，可提供 Tools（可执行动作）、Resources（只读数据）、Prompts（提示模板）三种能力。

**属于领域**：AI 工具生态。

**通俗理解**（比喻/例子，讲完落回术语）：按 USB-C 标准造出来的"外设"。能力判断口诀：会"做事"的是 **Tool**（模型决定何时调，如查库、发邮件），只是"被看"的是 **Resource**（URI 标识的只读数据），给人"点选"的话术模板是 **Prompt**。装进宿主：Claude Code 用 `claude mcp add 名字 -- 命令 参数`，Claude Desktop 改 claude_desktop_config.json。自己写：官方 Python SDK 三步——`MCPServer("名")` 建实例 → `@mcp.tool()` 挂函数（函数签名+docstring 自动变成给模型看的说明书）→ `mcp.run()`。安全红线：服务器以你的身份在跑，装第三方 ≈ 发钥匙给陌生人，优先官方实现、最小权限、敏感操作留人工确认（见 [[质检Gate与自我纠错循环]]）。

**与已有概念的关联**：
- [[MCP协议]]：它遵循的协议
- [[stdio与流式HTTP传输]]：它与客户端通信的两种方式
- 与 LangChain/CrewAI 框架内工具是分层关系：框架管思考编排，MCP 管工具的标准化复用

**首次接触于**：[[项目笔记/mcp_servers]]

**同义/相关笔记（并行批次合并）**：[[工具调用生命周期]]（tools/call 全流程详解）、[[MCP模型上下文协议]]。
