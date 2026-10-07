# 知识入库提案 · dsh_plugin_upgrade_skill

- 任务：d7baab36-85bf-450b-8efd-cae089fe09d6
- worker：kimi-pool-20261007-w1（2026-10-07）
- 查重范围：`vault/概念/`、`vault/项目笔记/`（无 DSH/DeepSeek/版本迁移条目）

## 提案 1：新建项目笔记（worker 已按裁定直接新建）

`vault/项目笔记/dsh_plugin_upgrade_skill.md` —— 已写入：定位（DSH 插件版本迁移的 skill 集合）、195 卡结构（版本走廊/frontmatter/覆盖表诚实标注）、11 skill 分工（含 generic-migration 控制组）、benchmark+论文（可复算证据链）、5/5 校验、边界（适用面窄/会过期）。

## 提案 2：新建概念（请协调者终审合并）

**文件名**：`vault/概念/经验卡知识库.md`

**一句话**：把专家踩坑经验结构化成"症状→适用条件→动作分级→修复"的标准卡片库，让 agent 按需检索执行，并用对照 benchmark 证明卡片贡献——经验从文档升级为可执行知识资产。

**正文要点**：
- 卡片三要素：Symptoms（怎么识别）/ Applies to（命中判断）/ Action level（执行分级）；字段设计即人机分工设计。
- 组织法：按版本走廊/风格谱系等"跳变轴"归档，覆盖表诚实标注完成度。
- 有效性证明：控制组对照 + 可复算证据链，拒绝"skill 有用"口号化。
- 与 huashu 配方卡同构（风格卡/升级卡 = 同一范式的领域实例）；经验回流闭环（新坑→考题→基准更新）。
- 反模式：卡片不设命中条件（AI 乱执行）；宣称覆盖大于实际；知识库无过期机制。
- 链接：`[[项目笔记/dsh_plugin_upgrade_skill]]`、`[[项目笔记/huashu_art_motion]]`、`[[AgentHarness智能体挽具]]`、`[[证据优先质检ProofOverClaims]]`

## 总览/索引更新

请协调者在 `vault/00-总览.md` 项目清单补一行 dsh_plugin_upgrade_skill（worker 不动总览）。
