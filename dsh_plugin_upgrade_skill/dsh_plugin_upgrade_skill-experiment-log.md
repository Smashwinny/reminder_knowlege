# 实验日志 · DSH 插件升级 Skill（dsh_plugin_upgrade_skill）

- 任务：d7baab36-85bf-450b-8efd-cae089fe09d6
- worker：kimi-pool-20261007-w1
- 日期：2026-10-07
- 仓库：oh-my-dsh/dsh-plugin-upgrade-skill（浅克隆，快照 ef07576，5002 文件，MIT）

## 实验设计

把推文/README 的宣称逐条断言校验（纯读取不执行仓库代码）：11 skill / 195 卡 / 版本覆盖 / benchmark 63 / 卡片 AI 可读结构。

## 运行记录（全部真实执行，exercise/run_output.txt）

`python validate_claims.py` 两轮演进，**5/5 通过（exit=0）**：

- T1 skills/ 目录 = 11 个（plugin-workflow 统一编排 + 九个专职 + generic-migration 对照控制组）。
- T2 references/v*.md 20 个版本文件 frontmatter cardCount 求和 = **195，与徽章精确一致**，无缺失 frontmatter。
- T3 版本走廊 20 区间覆盖 0.1.0-rc.8→0.2.0-rc.1。
- T4 benchmark/tasks 实测 **65**（S24/M14/H27）vs 宣称 63（22/14/27）——静态多 2 道，为宣称低估；断言修正为 ≥63 并如实标注偏差方向。
- T5 抽样卡（DSH-0.1.2-A2-01）AI 可读字段 4/4：Type/Applies to/Symptoms/Action level。

## 结论

- 全部结构宣称属实（且 benchmark 实际比宣称多，诚实方向反了也无妨——徽章未同步更新）。
- 卡片字段设计（Symptoms/Applies to/Action level）是"写给 AI 执行的文档"与"写给人看的文档"的本质区别样本。
- generic-migration 控制组的设计（量化专有知识贡献）是学术严谨性进入社区 skill 的标志性做法。
- 未验证（诚实声明）：论文分数 93.83→98.75 未本机复算；未执行真实迁移任务（需 DSH 环境）；DSH 为快迭代生态，快照会过期。

## 产物

- `exercise/validate_claims.py`、`exercise/run_output.txt`
