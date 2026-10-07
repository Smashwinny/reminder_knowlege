---
tags: [学习方法, 开源书籍, 人生方法论]
status: worker 提案待协调者 review 定稿
owner: kimi-pool-20261007-w1
task: 327aa7d1-1301-4062-8a95-218024e2e967
---
# 上海交通大学生存手册（SurviveSJTU Manual）

> 本文件为 worker 按协调者 2026-10-07 裁定新建的**提案笔记**（manifest.vault_note 指向）。
> 概念笔记提案见项目目录 `sjtu_survival_manual/sjtu_survival_manual-knowledge-proposal.md`，由协调者查重合并进 `vault/概念/`。

## 是什么

开源人生方法论手册：2008 年由上海交大校友（主要作者之一为 AI 专家侯晓迪）撰写初版，2022 年起翻新为 GitBook 开源仓库（GitHub `SurviveSJTU/SurviveSJTUManual`，5890+ stars，快照 commit fd64d6c）。主张流水线化大学教育下学生必须自我负责，核心是"怎么选"而不是"怎么考"。

## 结构

- 序（旧版序 + 新版序）：为什么写这本书
- 立志篇 ★核心：你想要做什么 / 失败的思维方式（高考思维、被动思维）/ 反对 PUA / 悲壮的学习方式 / 你的身价是多少 / 正确地浪费剩下的时间 / 总有更值得做的事情 / 认识信息素养 / 做研究的兴趣 / 关于工作
- 访谈集：为了留学而出国（含警惕出国中介）/ 做真正的研究 / 管理者的智慧 / 小心项目的陷阱 / 保研者说 / 破解留沪政策
- 生存技巧：转专业 / 选课 / 突击备考 / 正确解读成绩算法（GPA）/ 旁门左道（含善用 GPT）
- 附录：各专业学长学姐分享（TODO 持续更新）

## 核心思想（概念提案，待协调者建/并）

- **高考思维**：把量化评分当至高追求 = 政策的牺牲品；分数是指标不是证据
- **被动思维**：凡事等外部给理由；心悦诚服的理由只应是求知欲
- **时间价值四档**：终身受益/中期影响/短期满足/负向消耗，按时间尺度效率给任务定价
- **信息素养**：搜索→辨别→使用→安全呈现；信息差 = 信息素养差距

## 实验

一周时间投资审计器（`sjtu_survival_manual/exercise/time_invest_audit.py`，纯标准库）：
CSV 时间日志 → 四档分类 → 评分 + 彩色 HTML 报告。示例数据评分 34.2，调参 + 增补记录后 44.4。详见项目内实验日志。

## 坑与结论

- 部分章节为 TODO 占位，注意时效（考研/转专业等）
- 身价数据更新于 2024 年，仅作量级参照
- 全书是观点型写作，需批判阅读（这恰是手册倡导的独立思考）
- 指南 PDF：`sjtu_survival_manual/上海交通大学生存手册-小白指南.pdf`（14 页，疑问式目录 Q1–Q10）

## 来源

- 触发记录：https://x.com/NFTCPS/status/2107396492721897729
- 上游：https://github.com/SurviveSJTU/SurviveSJTUManual · https://survivesjtu.gitbook.io/survivesjtumanual/
