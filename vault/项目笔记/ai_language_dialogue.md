---
tags: [项目笔记]
类别: 知识学习类（学习方法）
来源项目: ai_language_dialogue
完成日期: 2026-11-22
---

# ai_language_dialogue：真人测试效应与参数模型分离

## 项目是什么

拆解 @RealHanyaHu 的 AI 外语对话练习：场景对话、母语补位、目标语重试与隔天提取。具体 Muse 产品身份无法绑定，方法与品牌解耦。

## 来源核实

- 原帖：https://x.com/RealHanyaHu
- K&R 2008：https://learninglab.psych.purdue.edu/downloads/2008/2008_Karpicke_Roediger_Science.pdf

原文 40 个词对，一周后重复测试 80%、无重复测试 36%（跨后续学习条件平均）。这是真人实验；玩具模型不证明该效应。

## 带来的概念

- [[测试效应与延迟提取]]：真人证据与模型参数分开。
- [[母语补位重试纪律]]：补位维持交流，目标语重试才处理缺口。
- 关联 [[可回收训练闭环]]、[[两层重复与场景迁移]]，不另建“记忆升级条件”绝对规则。

## 实验做了什么

初版把测试加固预设得更高又称方向稳健，属于循环论证。修订后默认玩具输出 21.7%/33.0%，反向参数输出测试 8.3%，8 项 unittest 通过。练习指标不再称唯一，产品效果未验证。

## 坑与结论

- v2 指南逐页渲染审核，原 PDF 保留，manifest 指向 v2。
- 指南：`ai_language_dialogue/ai-language-dialogue-guide.html`；审核版：`ai_language_dialogue/AI辅助外语对话-小白指南-v2.pdf`。
