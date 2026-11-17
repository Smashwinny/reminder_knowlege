# awesome-ai-motion 实验日志（task 96550ce7-aea2-4c8d-93a4-c7386d7fcb0d）

实验日期：2026-10-27
上游：guanmo-ai/awesome-ai-motion，main @ 8733ddf（浅克隆，5381 文件）
目标：核实 README 宣称（441 作品/69 提示词/25 源码）并评估其证据分级体系的真实性。

## 步骤与真实输出

### 步骤 1：克隆与结构摸底

- 最新 commit：`8733ddf 补充 311 个 Opus 5.5 动效案例与制作资料`
- 结构：`data/cases.json`（主数据）+ `cases/`（1728 个单条 md，中英双语）+ `prompts/`（112 个提示词 txt）+ `browse/`（分类浏览页）

### 步骤 2：主数据实测（data/cases.json）

```
python 解析：1728 条案例（README 的 441 已严重滞后——仓库仍在快速膨胀）
stage 分布：discovery 1635 / catalogued 61 / None 32
```

### 步骤 3：证据分级字段全量统计（核心发现）

每条案例带结构化 verification 字段，1728 条全量统计：

| 验证项 | 命中 | 比例 |
|---|---|---|
| videoAttachmentConfirmed（视频附件确认） | 1728 | 100% |
| authorClaimConfirmed（作者主张经原文核对） | 1696 | 98.1% |
| **independentlyReproduced（独立复现）** | **0** | **0%** |
| **fullReview（完整复核）** | **0** | **0%** |

prompt 状态机三态分布：original（原帖公开提示词）244 / brief（简介级）233 / unknown 1251。

### 步骤 4：与宣称对照

| README 宣称 | 实测 | 结论 |
|---|---|---|
| 441 个作品 | 1728 条 | 宣称滞后，实际远超 |
| 69 份公开提示词 | 244 original（另 233 brief） | 口径不同，量级增长 |
| 25 个案例附源码 | 未逐项核 | 保留 |
| "已编目 36 条" | catalogued stage 61 条 | 宣称滞后 |

## 结论

- 这是一个**证据分级编目系统**而非代码库：每条案例有 verification 四字段（作者主张/视频附件/独立复现/完整复核），
  诚实到"独立复现 0 条"也照写——与知识库 [[证据状态机]]、[[中继交叉印证]] 完全同构；
- README 数字严重滞后于数据（441 vs 1728），引用其数字前必须查 data/cases.json 真源；
- prompt 三态（original/brief/unknown）是务实的中间状态设计——"简介级"不等于"原提示词"；
- 学习价值：如何给"AI 作品展示区"做可信编目（发现池→编目→复核的 stage 流水线）。

## 产物

- `exercise/experiment-log.md`（本文件）
- `repo/` 上游克隆（.gitignore 排除）
