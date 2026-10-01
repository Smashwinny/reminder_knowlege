---
tags: [概念]
领域: AI 工具生态 / 进程通信
别名: ["stdio transport", "Streamable HTTP"]
首次来源: "[[项目笔记/mcp_servers]]"
---

# stdio与流式HTTP传输

**一句话定义**：MCP 客户端与服务器之间的两种通信管道——stdio 把服务器当本地子进程、用标准输入/输出收发 JSON-RPC；Streamable HTTP 通过 URL 连远程云服务（老的 HTTP+SSE 方式已淘汰）。

**属于领域**：AI 工具生态 / 进程间通信。

**通俗理解**（比喻/例子，讲完落回术语）：stdio 像"雇佣贴身工人"——宿主亲手启动服务器进程，数据不出你的机器，私密但要在本地装环境；Streamable HTTP 像"打电话叫外卖"——连个 URL 就用，省事可共享，但数据走网络。这对应 awesome 清单里每个条目的 🏠 Local / ☁️ Cloud 标记：管本地软件的多为 🏠，调远程 API 的多为 ☁️。

**与已有概念的关联**：
- [[MCP协议]]：传输层只是协议的一部分，握手和消息格式不变
- [[MCP服务器]]：选择服务器时先看它是什么传输类型

**首次接触于**：[[项目笔记/mcp_servers]]

**踩坑备忘**：stdio 模式下客户端用 PATH 里的系统 python 启动子进程而依赖装在 venv → "Connection closed"；要用 sys.executable 或 venv 绝对路径。
