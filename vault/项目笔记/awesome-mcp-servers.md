---
tags: [项目]
类别: 知识学习类
上游仓库: https://github.com/punkpeye/awesome-mcp-servers
完成日期: 2026-10-01
---

# awesome-mcp-servers

**这是什么**（一句话）：GitHub 上最全的 MCP 服务器精选清单——4086 个条目按约 60 个领域分类，是"给 AI 装手脚"的生态黄页。

**它给我什么能力**：
- 按分类检索现成的 AI 工具集成（文件/数据库/浏览器/智能家居…），不造轮子
- 挑选有据：🎖️ 官方 → 🪟 Windows 支持 → 语言徽章 → glama 评分徽章的四步漏斗
- Frameworks 区是自写服务器的入口（Python FastMCP：一个装饰器 `@mcp.tool` + docstring 即一台服务器）
- 60 个分类本身就是"AI agent 能力边界"地图

**引入的概念**：
- [[MCP模型上下文协议]]
- [[JSON-RPC与stdio传输]]
- [[工具调用生命周期]]
- [[M×N集成问题]]
- [[提示注入]]

**实验记录**（做了什么、结果、坑）：
- `exercise/mcp_handshake.py`：用 Python subprocess 拉起官方 `@modelcontextprotocol/server-filesystem`（npx -y），裸发 JSON-RPC 完成 initialize → tools/list（14 个工具）→ tools/call(write_file)，磁盘验证 sandbox/hello.txt 内容正确，全部通过 ✅。全程无需任何大模型 API key。
- 坑：① npx 首次运行要下载包，十几秒属正常；② stdio 服务器的 stdout 是协议通道，调试信息必须走 stderr；③ 握手 protocolVersion（2024-11-05）双方须一致；④ 只授权 sandbox 目录时，越界写入返回 isError=True——最小授权围栏真实有效。
- 延伸：同样的命令可写进 Claude Desktop 的 claude_desktop_config.json，用自然语言驱动今天亲手发过的那些 JSON 消息。

**后续可深入的方向**：
- 用 FastMCP 把已有脚本（如 langchain 练习里的工具）包成 MCP 服务器，接入 Claude Code
- 试 awesome-remote-mcp-servers 的 URL 型服务器，对比 stdio 与 HTTP 传输
- 阅读 MCP 规范的 resources/prompts 能力（本清单聚焦 tools）
