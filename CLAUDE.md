# F:\reminder — 400+ 子项目学习总仓库

本仓库是一个**学习知识管理总仓**：用户有 400+ 个小项目要逐个学习了解，学习成果（PDF 指南、笔记）和知识库都在这里维护，并同步到 GitHub（Smashwinny/reminder_knowlege）。

## 核心规则

- **协作与调度优先规则（2026-10-04）**：Codex 和 Claude 均须先读根目录 `AGENTS.md`、`tools/shiyi_worker_guide.md`，用 `tools/reminder_pipeline.py` 领取。最新用户授权（2026-10-04）：新记录自动分类，核实的学习项目也自动执行完整学习；完整产物与独立审核后只写分析标签，任务完成由用户本人点击。worker 只写任务所属产物，知识库合并、网站状态、纲要和 Git 由唯一协调者维护；本规则覆盖下述 skill 中让每个 worker 独立入库/提交的调度方式，学习质量要求仍全部保留。禁止 worker 使用 `git add -A` 或直接执行旧脚本 `done/viewed`。

- **学习方法**：使用项目级 skill `/learn-project`（`.claude/skills/learn-project/SKILL.md`）。对知识学习类、开源项目类子项目，严格按该流程执行：疑问清单 → 图文解答 → 能力清单 → 动手实验 → 彩色 PDF → 知识入库 → git 同步。
- **默认执行与备份**（2026-10-06）：本人 Dot 为唯一云端协调者，按原 skill 第 8/9 步合并最新 GitHub vault、真实独立审核并直接通过自己已授权的 GitHub 连接提交/推送学习成果。Ubuntu 仅维护网站授权、私有报告和处理状态；不等待服务器发布器或新增 delivery OAuth。Dot 实际写权限、二进制提交与端到端回读尚在核验，不因规则已更新就宣称已运行。Windows 上线备份及同步已核验成果，直连 Git 回执消费未验收前保留待同步。保留现有目录、vault 和旧 owner，不重跑已学项目；公开仓库只收学习成果，私密报告仅留网站/本机，任务完成由本人点击。worker 不操作共享 vault/Git，Dot 协调者承担这两步。
- **注意**：该 skill 同时部署了一份用户级副本 `C:\Users\Windows\.claude\skills\learn-project\SKILL.md`（保证在任何目录开的窗口都能用）。**修改 skill 时必须同步更新两份**。
- **目录布局**：每个子项目一个目录；克隆的上游代码放在 `<子项目名>\repo\`（被 .gitignore 排除，**不要提交**）；学习成果放子项目根目录和 `exercise\`。
- **知识库**：`vault\` 是唯一的 Obsidian 知识库，覆盖所有项目。新概念先查重（合并/关联），再写入；每学完一个项目必须更新 `vault\00-总览.md`。
- **PDF 偏好**：报告类产出一律彩色鲜艳、图文并茂、重点夸张的 PDF（HTML → Edge 无头打印），中文文件名需先 ASCII 临时名再改名（见 skill 第 7 步）。

## 当前项目清单

| 子项目 | 类别 | 状态 |
|---|---|---|
| img2threejs | 开源项目类 | 指南+实验已产出（2026-10-01），知识入库待补 |
| changeheadanddance | 一次性报告类 | 报告已产出 |
