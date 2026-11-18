---
tags: [项目笔记, SEO, 内容发布, 差异闸门]
created: 2026-10-27
---
# ChatSEO 六技能 SEO 工作流

X 长文《My chief of SEO, claude code opus 5.5》所述工作流：Claude Code 做主管，ChatSEO MCP 做情报层，人审批上线。ChatSEO 有 38 工具，Pro+ €49/月起，OAuth 2.1+RFC 9728；技能文件免费不代表数据服务免费。

## 核心概念
- [[上线前差异闸门（DIFF GATE）]]：发布前机械列出旧版有而新版丢的元素，丢失即拦截。
- [[政策到纪律翻译]]：把平台政策转成 Agent 可执行的具体纪律。

## 实测
本地 `diff_gate.py` 三轮：丢表格 exit=7 拦截、同页 exit=0 无误报、修复后 exit=0 放行。六技能规则完整提取：money-keywords/page-brief/ship-page/geo-rankings/pattern-drip/weekly-seo。Google 垃圾政策核对完成。

未接入付费 ChatSEO/GSC、未编辑真实页面，排名提升未验证。
