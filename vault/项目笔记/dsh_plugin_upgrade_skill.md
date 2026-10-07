---
tags: [项目笔记, 开源项目, AgentSkill, 版本迁移, DeepSeek生态]
created: 2026-10-07
---

# dsh-plugin-upgrade-skill（DSH 插件升级 Skill）

- 仓库：https://github.com/oh-my-dsh/dsh-plugin-upgrade-skill（MIT，快照 ef07576，5002 文件；2026-10-07 克隆实测 239 stars）
- 来源：@SuSu_酥酥 推文 https://x.com/NFT_Chen/status/2107040867202855211（崔神推荐插件第五弹）
- 论文：arXiv:2609.30120《Evaluating Agent Skills for Version-Specific Plugin Migration》

## 是什么

教 AI 升级 DSH（DeepSeek Harness，"所有功能都以插件形式存在"的 AI 运行框架）插件的 skill 集合。痛点：DSH 每次发新版老插件可能启动不了。解法：已知坑→195 张 AI 可读的升级卡（按版本走廊 0.1.0-rc.8→0.2.0-rc.1 组织，20 个文件）+ 11 个 skill（workflow 编排 + 九个专职 + generic-migration 对照控制组）+ 63 道 benchmark 题 + 论文可复算证据链。社区共建，与 DeepSeek 无隶属。

## 卡片设计（AI 可读性三要素）

Symptoms（坏了长什么样）/ Applies to（哪些插件会踩）/ Action level（required-if-hit 等执行分级），溯源到上游 compare 与 release notes。README 覆盖表诚实标注 ✅完成/📝草稿段。

## 本机实证

validate_claims.py 5/5：11 skill 精确 / 195 卡 cardCount 求和精确 / 20 区间覆盖 / benchmark 实测 65（比宣称 63 多 2 道静态，宣称低估已标注）/ 抽样卡 4/4 字段。论文分数（93.83→98.75）未复算；未执行真实迁移（需 DSH 环境）。

## 同构与区分

与 [[huashu_art_motion]] 配方卡同构（风格卡/升级卡 = 经验卡知识库范式的两个领域实例）；与 vault [[AgentHarness智能体挽具]] 概念同域但 DSH≠agent-harness 子项目，注意区分。

## 边界

适用面窄（只覆盖 DSH 版本走廊）；知识随上游发版过期需社区回流；长期解是上游少破坏性变更+兼容层（README 自述）。

## 关联

- 概念提案：经验卡知识库（见项目目录 knowledge-proposal.md，协调者终审）
- [[AgentHarness智能体挽具]]、[[证据优先质检ProofOverClaims]]、[[Handoff交接简报续跑]]
