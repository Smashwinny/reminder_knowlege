---
tags: [概念]
领域: 协议基础
别名: [JSON-RPC, stdio 传输]
首次来源: "[[项目笔记/awesome-mcp-servers]]"
---

# JSON-RPC 与 stdio 传输

**一句话定义**：JSON-RPC 2.0 是用 JSON 文本表示"远程函数调用"的极简协议；stdio 传输指两个进程通过标准输入/输出一行一行互发这些 JSON。

**属于领域**：协议基础，是 [[MCP模型上下文协议]] 的底层载体。

**通俗理解**（比喻/例子，讲完落回术语）：
就像两个程序之间传纸条：一张纸条写"请帮我算 add(1,2)，编号 1"（请求），对方回一张"编号 1 的结果是 3"（响应），还有不需要回条的通知（notification）。MCP 服务器本质就是一个"会说 JSON-RPC 的普通命令行程序"——宿主把它作为子进程启动，往它的 stdin 写请求、从 stdout 读响应，没有任何魔法。注意：**stdio 服务器的 stdout 是协议通道，调试信息必须走 stderr**，往 stdout 随意 print 会破坏协议。

**与已有概念的关联**：
- 承载：[[MCP模型上下文协议]]
- 相关：[[工具调用生命周期]]

**首次接触于**：[[项目笔记/awesome-mcp-servers]]（实验：用 Python subprocess 裸发 JSON 与官方 filesystem 服务器握手成功）

**同义/相关笔记（并行批次合并）**：[[stdio与流式HTTP传输]]（同一主题的另一篇，补齐 Streamable HTTP 云端侧）。
