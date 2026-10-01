---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/Shubhamsaboo/awesome-llm-apps
完成日期: 2026-10-01
---

# awesome-llm-apps

**这是什么**（一句话）：140k+ Star 的 AI 智能体示例合集——88 个（2026-10 实测）能直接跑的智能体应用模板,分 14 大区（入门/进阶/多智能体/Skills/常驻/语音/生成式 UI/MCP/RAG/记忆/微调/框架速成）,Apache-2.0 可商用。

**它给我什么能力**：
- 做智能体应用时"改模板"而非"从零写":挑最接近的 starter → 换 model → 换/加 tools → 改 instructions
- 四大件（Agent 工具循环 / RAG / 多智能体 / MCP）都有从 30 行到生产级的渐进示例
- `npx skills add` 给 Claude Code 装技能;9 个技能与用户自建 skill 同格式
- 支持 OpenAI 兼容 / Anthropic 兼容 / Ollama 本地三条接入路线（国产模型实测可跑）

**引入的概念**：
- [[AI智能体Agent]]（总纲）
- [[LLM工具调用]]（已合并:agno 视角 + Tool/Skill/MCP 对比）
- [[多智能体协作]]（已合并:agno Team 60 行实例）
- [[RAG检索增强生成]]（已合并:Agentic RAG）
- [[MCP模型上下文协议]]（已有笔记,本仓库提供 6 个 mcp_ai_agents 实例）
- [[AgentSkills技能包]]（新增）
- [[智能体框架]]（新增,agno 为实例）

**实验记录**（做了什么、结果、坑）：
- 环境:Windows 11 + Python 3.14 + venv(agno 3.0.11 / anthropic 1.11.0 / streamlit / icalendar)
- 冒烟:agno Agent + GLM-4.6(Anthropic 兼容端点)一句话问答 ✅,RunMetrics 可见 token 消耗
- 主实验:双工具智能体(计算器+时钟),日志出现 Thinking/Tool Calls/Response 三框,`calculator(expression=3e5 * 365 * 24 * 3600)` 与 `now_time()` 均被正确调用 ✅
- 改造:自定义 `roll_dice(sides, times)` 工具,一次消息并发两个工具调用(六面骰×2 + 二十面骰),随机数真实 ✅
- 坑:① agno 3.x 移除 `base_url` 直传,要用 `client_params={"base_url": ...}`(仓库示例还是 2.x 写法);② GLM 接入点限流约 1 次/分钟,连续调用需 `sleep 65`,否则 429/1302;③ 中文 Windows 先 `setx PYTHONUTF8 1`

**后续可深入的方向**：
- 跑通一个真正的 RAG 教程(建议 rag_chain 或本地 RAG,配合 Qdrant)
- 用 starter 模板改一个自己领域的助手(如 CSV 报表问答)
- 深入 mcp_ai_agents,给 Claude Code 配一个 MCP server
- 两个框架速成课(Google ADK / OpenAI Agents SDK)对照 agno 读
