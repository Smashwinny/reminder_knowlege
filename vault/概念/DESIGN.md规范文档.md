---
tags: [概念]
领域: AI 原生开发 / 设计系统
别名: ["DESIGN.md", "设计规范文档"]
首次来源: "[[项目笔记/awesome-design-md]]"
---

# DESIGN.md 规范文档

**一句话定义**：Google Stitch 提出的纯文本设计系统文档——YAML frontmatter 存精确 token、Markdown 正文写设计原则与组件规范，放在项目根目录供 AI 编程工具读取，使其生成的 UI 保持一致的大厂级气质。

**属于领域**：AI 原生开发 / 设计系统。

**通俗理解**：`AGENTS.md` 告诉 AI"怎么施工"，DESIGN.md 告诉 AI"装修成什么风格"——一份**装修样板间说明书**。为什么偏偏是 Markdown？因为 LLM 的母语是文本：零解析成本、diff 友好、人机共读（对比 Figma 导出 / JSON token 工具链的重装备）。它是[[设计令牌DesignToken]]的"平民化载体"：过去只有大厂设计团队养得起 token 体系，现在拷贝一个文件就继承 Vercel/Linear 级规范。

**与已有概念的关联**：
- 相关：[[规格书先行SpecDriven]]（审美版规格书：主观感受→客观合同）、[[提示词权威边界]]（防 AI 风格漂移的结构方案）、[[源码即Prompt]]（Markdown 说明书驱动 AI 干活，同一家族）
- 项目对照：[[项目笔记/ai-website-cloner]] 复刻"结构与代码"，DESIGN.md 复刻"视觉规则"，两条互补路线

**首次接触于**：[[项目笔记/awesome-design-md]]
