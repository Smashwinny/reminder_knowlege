---
tags: [项目笔记, 开源项目, 模型网关, BYOK, Agent基础设施]
created: 2026-10-09
---

# magpie（本地模型网关）

- 仓库：https://github.com/yetone/magpie（MIT，快照 023f5aa，2026-10-09 浅克隆；~4.3k stars 搜索时点）
- 来源：@MindfulReturn 推文 https://x.com/MindfulReturn/status/2106599213379309749
- 官网：https://usemagpie.ai

## 是什么

跑在本机 127.0.0.1:3425 的模型网关 + 菜单栏换模型面板：40+ Agent（Claude Code/Codex/Gemini CLI/Cursor…）接到同一网关，任一 Agent 用任一模型，菜单一键切换。四协议互译（OpenAI Chat Completions/Responses+Anthropic Messages+Gemini，含流式/工具调用/推理过程）；26+ 供应商预设；路由分组/用量/会话/插件；限流自动故障转移。

## 三个核心机制

1. **协议翻译**：internal/gateway/{chat,responses,anthropic,gemini}.go 四处理器归一化互译——M×N 压成 M+N。
2. **订阅凭证化（BYSOL）**：登录过的 Claude/Codex/Copilot/Gemini 订阅成为 provider——驱动真实 claude 二进制 + MCP 桥接（claudebridge/mcp.go），多账号配额尽自动切下一个。
3. **配置手术**：internal/agent/ 80 个适配器原子化修改各家配置，保注释保格式可回滚。

## 本机实证

validate_magpie.py 6/6：四协议处理器全在/端口 3425 十八处引用/订阅 MCP 桥存在/供应商 host 识别≥3/80 适配器/1425 测试文件。Go 工具链未装测试未执行（结构校验替代）；网关未真实运行（系统级+需凭证）；Go 2162/测试 1425/internal 44 包。

## 与 BYOK 概念关系

[[BYOK模型网关与用量归因]] 的旗舰实现+能力超集：BYOK→BYSOL→四协议翻译三段进阶。对照 LiteLLM（Python 系）、One-API/New-API（国内流行）。

## 风险

订阅共享 ToS 灰区（订阅条款大概率禁止账号共享/自动化，封号风险自担）；凭证集中（网关被入侵=全部失守）；单一作者依赖。

## 关联

- [[BYOK模型网关与用量归因]]（概念更新提案见 knowledge-proposal.md，协调者终审）
- [[能力层与后端路由]]、[[Provider适配层与错误契约]]、[[用量额度与估算费用的计量分层]]
