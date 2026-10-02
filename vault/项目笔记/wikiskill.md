---
tags: [项目笔记]
类别: 知识学习类（论文方法精读 + 方法层 toy 复现）
完成日期: 2026-10-03
来源: X 推文 @mylifcc（拾遗队列 task a3fffd3b-6e12-40d2-bdfe-e9766bce088f）
---

# wikiskill — WikiSkill 论文方法精读

## 这是什么
Google Research 论文《WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution》（arXiv:2608.27454，2026-08-27，作者 Liyan Tang 等 6 人）。技能演化框架：wiki（理解，只增不删）+ skills（可执行，门控验收）双层共演化，不改权重提升智能体能力。官方无代码（网上仅第三方复现），本批次走方法层轻量验证。

## 带来的概念
- [[WikiSkill共演化循环]] — 三层工作区 + 四角色循环 + 关键数字（9B+技能 47.4% > 27B 裸考 39.4%；Proposer 读 wiki +15.0；负迁移 50.5→18.1）
- [[知识层永不回滚原则]] — 门控只回滚 skills、wiki 永续、skill-impact 程序化审计

## 实验做了什么（F:\reminder\wikiskill\exercise\wikiskill_toy.py，零 API 纯标准库，全跑通）
1. **ex1 演化循环**：stub 模型 A（权重冻结）基线 12.5% → 3 轮演化 87.5%；leap 题仍错世纪年=论文"低层 workaround"活标本
2. **ex2 污染测试**：坏技能 62.5%<87.5% 被门控拒绝回滚 skills；wiki 只增不删；审计拦重复提案
3. **ex3 跨模型迁移**：B 裸考 50%→87.5% 正迁移；A 的闰年简化规则把全对的 B 带错（leap 2/2→1/2）负迁移实证
4. **ex4 复杂度记账**：N=40→80，Maintainer/Proposer 调用均 3→3 不变，rollout 120→240（优化器侧与数据量无关）

## 坑与结论
- x.com 抓不到正文 → fxtwitter API 拿全文；arXiv PDF 直读渲染失败（无 poppler）→ 改用 arXiv HTML 版全文
- 论文附录 C/D.2/E.2 在 HTML 版中被截断：复杂度精确公式、采样预算细节不可达，实验只验证正文可推断的结构，PDF 中如实标注
- 初读曾误记"merge/append/prune 三操作、Top-k 检索"——精读纠正：补丁式增量编辑（无 prune=局限之一）、ReAct 式自主 read_file 检索。教训：二手摘要必须对原文核对数字
- 诚实验证边界：stub 替代真实 LLM，验证的是机制（门控/永续/审计/调用结构），不是论文分数

## 产出
- PDF：`F:\reminder\wikiskill\WikiSkill-小白指南.pdf`（12 问彩色 + 4 实验记录）
- HTML 源：`F:\reminder\wikiskill\wikiskill_guide.html`
