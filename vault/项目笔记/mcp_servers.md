---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/punkpeye/awesome-mcp-servers
完成日期: 2026-10-01
---

# mcp_servers

**这是什么**（一句话）：MCP 服务器的精选目录（4086 个条目、59 个分类、378 个官方实现），学习它的真正目的是掌握 **MCP 协议** 本身与生态全貌。

**它给我什么能力**：
- 给 Claude（Code/Desktop）一条命令装新技能（查库、控浏览器、读文件…）
- 把自己写的工具升级为跨应用、跨框架的通用 MCP 服务器
- 用图例系统（🎖️官方 / 语言 / 🏠☁️ / 系统）精准淘服务器；配 glama.ai 可搜索

**引入的概念**：
- [[MCP协议]]
- [[MCP服务器]]
- [[stdio与流式HTTP传输]]

**实验记录**（做了什么、结果、坑）：
实验《给你的 AI 装上第一个自造 MCP 服务器》，代码在 `mcp_servers\exercise\`，全部实跑验证：
1. venv 安装官方 SDK mcp 2.2.0；
2. server.py：MCPServer 建实例 + add / count_servers 两个工具 + greeting 资源（约 40 行）；
3. client.py 最小客户端：initialize（协商版本 2025-11-25）→ tools/list → tools/call（add(20,22)=42；清单统计 4086 条/59 类/378 官方）→ read_resource 全通；
4. `claude mcp add awesome-lab` 注册进 Claude Code → ✔ Connected；
5. `claude -p` 端到端：真实模型调用两个工具并正确报告结果 ✅。

坑（都已解决并记入概念笔记）：
- 客户端用系统 python 启动子进程 → 依赖缺失 → Connection closed（改用 sys.executable）
- mcp 2.x 把 FastMCP 改名 MCPServer、属性 snake_case（老教程失效）
- bash 里反斜杠路径要单引号包住，否则注册的命令面目全非

**后续可深入的方向**：
- Aggregators 聚合器（一个服务器转发 N 个应用）
- 用 npx @modelcontextprotocol/inspector 可视化调试消息流
- 给 search_category 加工具：按关键词搜清单分类
- 学完 LangChain/LangGraph/CrewAI 后把 MCP 工具接进 agent 循环做综合练习
