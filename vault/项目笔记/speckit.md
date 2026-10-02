---
tags: [项目笔记]
类别: 开源项目类
完成日期: 2026-10-03
来源: "https://x.com/txbrraa/status/2097955506891469272 → github/spec-kit"
---

# speckit（GitHub Spec Kit）

## 这是什么
GitHub 官方开源的**规格驱动开发（SDD）工具包**（139.8★ · MIT · v1.1.x）。核心是 `specify` CLI（Python+typer）：一条 `specify init` 给项目装上 `.specify/` 项目舱（宪法、四大模板、确定性脚本、工作流）+ `.claude/skills/speckit-*` 10 个代理技能，支持 25+ AI 编码代理。纲领是"权力反转"：**规格书是源头，代码是规格的表达产物**。

## 流程
- 宪法一次：`/speckit-constitution`
- 每个功能一轮：`specify → (clarify) → plan → tasks → (analyze/checklist) → implement ⇄ converge` 循环直到报告 **Converged**
- 三条独立流程：SDD 造功能（core）/ Bug 修复 `extension add bug`（assess→fix→test，verified/partial/failed）/ 点子评估 `extension add assess`（go/needs-clarification/kill）

## 带来的新概念
- [[项目宪法Constitution]] —— 项目级根本法，一次写、全功能守
- [[规格收敛循环Converge]] —— implement⇄converge 对账循环，验收锁
- 补记 [[规格书先行SpecDriven]]：spec-kit 即其官方工业版（权力反转）
- 互链：[[工单任务图与前沿调度]]（tasks 环节同思想）、[[提示词权威边界]]（宪法/军规分层）、[[AgentSkills技能包]]、[[团队Harness的Git原生分发]]（.specify/ 是可评审可分发的团队资产）

## 实验做了什么（F:\reminder\speckit\exercise\）
1. `pip install` 本地克隆 → specify 1.1.1.dev0 ✅
2. `specify init demo-todo --integration claude --non-interactive` 真跑 → 生成 .specify/ + 10 个 SKILL.md ✅
3. `specify check` → 扫 30+ 代理集成，"ready to use" ✅
4. 手写真实规格书 specs/001-photo-albums/spec.md（照片整理器，3 用户故事 P1/P2/P3 各带 Given/When/Then，59 行）✅
5. `specify extension list` → "No extensions installed"，扩展机制验证 ✅

## 坑与结论
- 老教程的 `--no-git` 选项已不存在（实测报错）；命令已从推文中的 `/constitution` 等旧名升级为 `/speckit-*` 技能形态
- 官方脚本 create-new-feature.ps1 被本机安全策略拦截（外部代码），用等价手动法（mkdir + cp 模板）达成同一产物
- 推文数字过时：实测 139.8K stars（推文写 95K/126K），流程多了 converge
- 结论：Spec Kit = 把"规格先行 + 工单拆解 + 技能化 + 确定性脚本门禁"四件套打包成的官方产品，与仓库自建的 implement-spec/six_skills 思路高度同源，可直接用其模板反哺日常 AI 施工纪律

## 产出
- PDF：`speckit/spec-kit-小白指南.pdf`（HTML 源同目录）
- 实验：`speckit/exercise/demo-todo/`（SDD 骨架 + 真实规格书）
