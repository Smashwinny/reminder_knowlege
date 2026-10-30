---
tags: [项目笔记, 论文解读, harness工程, Agent架构]
created: 2026-10-09
---

# Harness Engineering 论文（arXiv:2609.00006）

- 论文：https://arxiv.org/abs/2609.00006（CC BY 4.0，Wavestone AI Lab，v1 2026-07-15；全文已存本仓库 exercise/paper.html）
- 来源：@程序员鱼皮 推文 https://x.com/yupi996/status/2106760754997203304

## 是什么

harness 工程（2026 年初命名的学科）的首个系统性实证：对 11 个生产级 coding harness（Claude Code/Codex CLI/Gemini CLI/Mistral Vibe/OpenHands/Aider/Mini-SWE-Agent/Hermes/Pi/OpenCode/OpenClaw）+ Omnigent 元对照做源码解剖。约 400 万行 Python/TS/Rust。方法纪律：不 benchmark 不排名，只描述比较。产出：七子系统解剖 + 13 横切观察 + 29 设计模式 + 五轴权衡。

## 七子系统（每部件最小↔最大光谱，缺位也是位置）

Agent loop（Mini-SWE 线性 while ↔ OpenHands 事件溯源）/ LLM 集成（一次 LiteLLM 调用 ↔ Hermes 5 传输 29 供应商档）/ 工具与动作（只有 bash ↔ Claude Code 43 工具延迟加载）/ 记忆与上下文（无界线性 ↔ Codex 跨会话记忆管线）/ 安全与权限（两限 ↔ Codex 四层栈含 LLM 审批员+三平台沙箱）/ 编排（Aider 无 ↔ Claude Code 递归组合）/ 扩展（结构化类型 ↔ Codex 市场插件）。

## 双缺席（三次语料扩充后仍成立）

① 400 万行零通用 agentic 框架导入（LangChain/LangGraph/AutoGen…；Gemini CLI 连自家都不用）——全手写 async 循环。② 零向量代码检索——全靠 ripgrep/tree-sitter/glob/MD 上下文文件的确定性检索。

## 其他要点

- 100 行地板：Mini-SWE-Agent 七子系统全实现，SWE-bench 同区间；差距在安全/恢复/成本/扩展/平台面。
- 扩展标准平局已破：SKILL.md 9/11 vs MCP 8/11；ACP 6 系统新增 harness 托管角色。
- 平台转向：harness 正在吞并"用哪个框架"之问（技能=声明式程序、hooks 基底、工具≈工作流、harness=服务面）。

## 本机实证

verify_claims.py 对全文存档做原句级断言 7/7（含双缺席/SKILL.md 平局/100 行证明原句命中）；T2 HTML 实体修正实录保留。未复算 400 万行语料统计（需 clone 11 仓库）。

## 关联

- [[AgentHarness智能体挽具]]（概念更新提案：追加论文体系化框架，见 knowledge-proposal.md）
- [[工具目录膨胀]]、[[Compaction上下文压缩算法]]、[[工具调用三段式流水线]]、[[上下文工程四操作]]、[[项目笔记/agent-harness]]
