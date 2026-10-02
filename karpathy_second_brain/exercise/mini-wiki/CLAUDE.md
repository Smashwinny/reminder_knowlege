# CLAUDE.md — mini-wiki 规约（schema 层）

这是给 LLM agent（或 lint 工具）看的"宪法"：结构、约定、工作流。

## 1. 目录结构

- `raw/` — 只读原始素材。**任何情况下不许修改、重命名、删除**。这是审计线（audit trail）。
- `wiki/sources/` — 每份 raw 源对应一张"源摘要页"（type: source-summary）。
- `wiki/concepts/` — 原子概念页，一页一个概念（type: concept）。
- `wiki/index.md` — 内容目录：每页一行 `[[链接]] — 一句话摘要`。
- `wiki/log.md` — 追加式时间线。每条必须以 `## [YYYY-MM-DD] 操作 | 说明` 开头（grep 可解析）。

## 2. 页面约定

- 每张 wiki 页开头必须有 YAML frontmatter，字段：`title`、`type`（concept | source-summary）、`sources`（指向 raw/ 的路径）、`related`（[[双链]] 列表）、`created`。
- 页面互链一律用 `[[双链]]`，目标是文件名（不含 .md）。
- **原子性**：一页只讲一个概念。一页里出现两个概念就拆页。

## 3. 操作

- **Ingest**：`python tools/mini_ingest.py raw/<file>.md` → 生成源摘要页 + 概念页 + 更新 index.md + 追加 log。（真实场景这一步由 LLM 完成，这里用确定性脚本演示簿记。）
- **Query**：`python tools/wiki_query.py <关键词>` → 先读 index.md，再给页面排名。
- **Lint**：`python tools/wiki_lint.py` → 体检：断链、孤儿页、frontmatter 缺字段、index 覆盖率、log 格式、sources 指向是否存在。
