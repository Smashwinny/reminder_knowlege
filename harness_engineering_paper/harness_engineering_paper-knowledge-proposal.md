# 知识入库提案 · harness_engineering_paper

- 任务：2791589d-5cee-48df-8e6d-54881aef5a1d
- worker：kimi-pool-20261007-w1（2026-10-09，主控模式）
- 查重范围：`vault/概念/`、`vault/项目笔记/`（队列 arXiv:2609.00006 零命中；vault 有同域概念但本论文为新实证工件）

## 提案 1：新建项目笔记（按 2026-10-09 新边界，放提案文件待协调者合并）

`harness_engineering_paper-vault-note-proposal.md` 已另存在本目录（内容同下），请协调者合入 `vault/项目笔记/harness_engineering_paper.md`：

论文定位（harness 工程首个系统性实证：11 系统+Omnigent+七子系统+双缺席）、Table 1 光谱、扩展标准平局已破、平台转向、五轴权衡、7/7 原句级核对、与 [[AgentHarness智能体挽具]] 等概念的系统升级关系。

## 提案 2：概念更新建议（请协调者终审，非新建）

**更新 `vault/概念/AgentHarness智能体挽具.md`**：追加"Harness Engineering 论文（arXiv:2609.00006）体系化框架"一节——

- 七子系统解剖：Agent loop / LLM 集成 / 工具与动作 / 记忆与上下文 / 安全与权限 / 编排 / 扩展（+接口层与会话基底两个横切面）；每部件存在最小↔最大实现光谱，缺位也是位置。
- 双缺席实证：400 万行零 agentic 框架导入、零向量代码检索（确定性检索 ripgrep/tree-sitter/glob）。
- 100 行地板：Mini-SWE-Agent 七子系统全实现，差距在安全/恢复/成本/扩展/平台面。
- 平台转向：harness 吞并框架之问（SKILL.md 9/11 vs MCP 8/11，ACP 6 系统 harness 托管）。
- 链接：`[[项目笔记/harness_engineering_paper]]`、`[[工具目录膨胀]]`、`[[Compaction上下文压缩算法]]`、`[[工具调用三段式流水线]]`。

## 总览/索引更新

请协调者在 `vault/00-总览.md` 项目清单补一行 harness_engineering_paper。
