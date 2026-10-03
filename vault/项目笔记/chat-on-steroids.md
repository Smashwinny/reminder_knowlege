---
tags: [项目笔记]
类型: 开源项目类
仓库: https://github.com/totec448-spec/chat-on-steroids
学习日期: 2026-10-03
任务: 拾遗 44cb4699（X 推文 https://x.com/AI_DVD6/status/2100360685452492964）
---

# chat-on-steroids

## 这是什么
Electron 桌面应用 + Chrome MV3 扩展（MIT，v2.1.25 实测克隆，≈4.2k stars / 1144 commits）：给 ChatGPT 网页版接入本地 MCP 能力——读写文件、跑终端、浏览器/桌面自动化、多 Agent Workers、Goal/Loop 自动续跑、Compact & Resume 交接。架构三方接力：**ChatGPT 网页（脑）→ Chrome 扩展（神经，收发页面消息）→ 本地 Electron/MCP 服务器（手脚，127.0.0.1:8765-8769）**。

## 走红话术甄别（推文判断依据）
X 推文称"GPT-6 Astra 额度白嫖 100 倍"。查证结论：**不是破解额度**。README 明确声明功能"do not grant extra quota or model access, must not be used to evade rate limits"——真实含义是"用 ChatGPT 网页订阅的宽松对话额度跑 agent，代替 Codex 的 agent 用量额度"，属通道切换话术。真实风险：自动化 ChatGPT 网页 UI 非 OpenAI 官方 API，可能违反 ToS 有封号风险（README 自认）。**与判例 55e30d0a / df617fa1（无可克隆的薅额度偏方，判非学习类）不同**：本项目是真开源工程，判学习类。

## 带来的概念
- [[本地MCP端点安全四道门]] — token 路径/Host/Origin/体积上限，防 DNS 重绑定
- [[工具暴露单调性]] — 快照只增不减护客户端缓存，handler 实时校验返 TOOL_DISABLED；readOnlyHint 免确认
- [[Handoff交接简报续跑]] — 跨会话续命，id 本地 randomUUID 防模型伪造
- [[Realpath路径沙箱防逃逸]] — realpath 规范化后比对根目录，"约束在代码里不在提示词里"

## 实验做了什么（exercise\，零依赖 Node，全部真实运行）
- **E1 仓库测绘**：静态扫描 11 项断言全 PASS——四道门代码在位、8 个 Core 工具齐全（update_plan 在独立 plan-tool.ts，自 Codex Apache-2.0 改编）、readOnlyHint 7 处、扩展白名单 5 个 localhost 端口、docs/ 74 篇 worklog。
- **E2 安全四道门复现**：node:http 复刻四道门 + 5 攻击视角 1 合法请求实测 404/403/403/413/404/200 全按预期。**坑：undici fetch 剥离自定义 host 头**，伪造 Host 必须用原生 http request。
- **E3 工具暴露单调性模拟**：60 行模拟"快照只增不减 + handler 实时校验 + readOnlyHint"，7/7 PASS。

## 坑与结论
1. **update_plan 不在 tools-core.ts**——在 plan-tool.ts（E1 初版断言写错的真实教训：断言要跟着架构走）。
2. goal/agent 机制文件主要在 **src/shared/**（类型+策略）而非 src/main/session/（执行机器）。
3. 多 Agent 的工程重心在"收尸"：silent ceiling 恢复、身份认领（IdentityLost）、reply ledger 记账、allowUnattributedCalls。
4. code-mode（exec 工具）让模型在受限 JS 运行时里编排工具调用，中间结果不进上下文省 token（64k 源码/32MiB/2s CPU/60s/32 调用限额），合同对标 Codex code-mode 协议。
5. 学习其架构**无需登录任何账号**；真要用需自担 ToS 封号风险。

## 产出
- `chat-on-steroids/chat-on-steroids-小白指南.pdf`（12 问彩色图文，SVG 配图）
- `chat-on-steroids/exercise/`（e1/e2/e3 三个实验脚本 + guide HTML 源文件）
