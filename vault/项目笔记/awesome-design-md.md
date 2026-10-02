---
tags: [项目]
类别: 开源项目类（资料合集，纯 Markdown 无运行时）
上游仓库: https://github.com/VoltAgent/awesome-design-md
完成日期: 2026-10-02
---

# awesome-design-md

**这是什么**：VoltAgent 维护的 73+ 套大厂 DESIGN.md 设计规范合集（GitHub 119k stars）——把 Vercel/Notion/Linear/Stripe 等 74 个网站的视觉基因提炼成 AI 可读的 Markdown，拷进项目根目录即可让 AI 生成风格一致的大厂级 UI。抖音"一键复刻大厂UI"梗的本尊。

**它给我什么能力**：
1. 给 Cursor/Claude Code 等 AI 工具"装审美"（拷文件 + 一句话）
2. 74 份大厂设计系统当免费教材（色阶/字阶/组件纪律）
3. 个人项目套大厂规范，原型可信度暴涨
4. 当模板做自己的品牌 DESIGN.md

**引入的概念**：
- [[设计令牌DesignToken]]
- [[DESIGN.md规范文档]]

**实验记录**（exercise\，Windows 11 全部实跑）：
- `exp1_parse_tokens.py`：正则解析全部 frontmatter → **64/74（86%）结构化可解析，1491 个精确色值 token，平均 14.2 个字号层级**；10 份（tesla/spotify/kraken/lamborghini/mastercard/runwayml/sanity/starbucks/theverge/lovable）是无 frontmatter 的散文老格式，解析不了
- 同一产品文案分别按 Linear / Notion 规范手写 `page_linear.html` / `page_notion.html`，Edge 无头截图实拍：近黑克制单紫强调 vs 深蓝主视觉带+粉彩卡，"规范决定气质"成立
- 坑：规范里的商业字体（Linear Display / Airbnb Cereal）本地没有，会回退 Inter/系统字体——复刻的是规则不是字体文件
- 产出：`awesome-design-md-小白指南.pdf`（6 页彩色，含双页实拍对照）

**后续可深入的方向**：
- 把此规范接进 Claude Code 实战生成一个完整多页站点，验证长页面一致性
- 仿写一份自己的 DESIGN.md 品牌规范
- 对比 awesome-claude-design（同作者姊妹仓库）
