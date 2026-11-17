---
tags: [项目笔记, 动效编目, 证据分级, 提示词管理]
created: 2026-10-27
---
# Awesome AI Motion 动效编目库

guanmo-ai/awesome-ai-motion（main@8733ddf）：AI 动效作品与制作资料的编目系统，不只是链接集合。

## 核心概念
- [[四级验证编目法]]：附件确认→主张核对→独立复现→完整复核，低级状态也如实记录。
- [[提示词三态标注]]：original/brief/unknown，简介级不能冒充原配方。

## 实测
`data/cases.json` 共 1728 条，README 的 441 已严重滞后；附件确认 100%、作者主张核对 98.1%、独立复现 0、完整复核 0。stage 为 discovery 1635、catalogued 61、None 32。提示词 original 244、brief 233、unknown 1251。

其价值在于把“编目完成”和“验证完成”拆开。未逐项核实 25 个附源码案例，未复现任何案例生成过程；链接存在不等于转载授权。
