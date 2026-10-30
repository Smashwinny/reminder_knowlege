# 实验日志 · Harness Engineering 论文（harness_engineering_paper）

- 任务：2791589d-5cee-48df-8e6d-54881aef5a1d
- worker：kimi-pool-20261007-w1（主控模式）
- 日期：2026-10-09
- 对象：arXiv:2609.00006v1《Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents》（CC BY 4.0，Wavestone AI Lab）

## 实验设计

论文本体无代码可跑（400 万行语料的源码解剖研究）。实验面：全文存档 + 宣称原句级核对——把推文与论文的核心宣称逐条变成对已存档全文（exercise/paper.html，1.4MB HTML）的原句断言。

## 运行记录（全部真实执行，exercise/run_output.txt）

`python verify_claims.py` 两轮演进，**7/7 通过（exit=0）**：

- T1 十一系统 11/11 全名命中 + Omnigent 元对照。
- T2 七子系统 7/7 + Table 1 最小/最大实现原句（Mini-SWE-Agent 线性 while / OpenHands 事件溯源）。
- T3 双缺席 1：`no agent runtime imports a general-purpose agentic framework` 原句命中（含 Gemini CLI 不用 Google 自家框架）。
- T4 双缺席 2：`none retrieves code with vector embeddings` 原句命中（确定性检索 ripgrep/tree-sitter/glob）。
- T5 `SKILL.md skills lead MCP in adoption (9/11 vs. 8/11)` + `ACP ships in six systems` 原句命中。
- T6 `implements all seven subsystems in roughly 100 lines` + SWE-bench Verified 原句命中。
- T7 `It does not benchmark or rank` + `13 cross-cutting observations` + `29 recurring design patterns` 原句命中。

**排查实录**：T2 首跑 6/7——"Memory & context" 被 HTML 实体 `&amp;` 挡住 → 实体解码一行修正后 7/7，过程保留在 run_output.txt。

## 内容要点（供指南）

- 七子系统 + 每部件最小/最大实现光谱（Table 1 全文映射，指南已整表收录）。
- 双缺席 + 100 行存在证明（Mini-SWE-Agent，SWE-bench 同区间——论文自加方法论警示）。
- 扩展标准平局已破（SKILL.md 9/11 vs MCP 8/11；ACP 6 系统新增 harness 托管角色）。
- 平台转向四信号 + harness-framework 合并论题 + 市场经济学。
- 五轴权衡：简单↔能力、安全↔自主、供应商耦合↔无关性、单体↔模块、脚手架复杂度↔模型能力。

## 结论

- 帖内宣称与论文原文一致性 100%；论文是 harness 工程的首个系统性实证，vault harness 品味区获整体"正名"。
- 未验证（诚实声明）：400 万行语料统计本身未复算（需 clone 11 个仓库逐行验证）；SWE-bench 成绩为论文转述自报数字。

## 产物

- `exercise/paper.html`（全文存档）、`exercise/verify_claims.py`、`exercise/run_output.txt`
