---
tags: [项目笔记]
类别: 知识学习类（产品工作流）
来源项目: chatgpt_space_workflow
完成日期: 2026-11-22
---

# chatgpt_space_workflow：当前 Space 协作与静态快照边界

## 项目是什么

学习 ChatGPT Space 当前 Pages、Slides、表格、Sites 和协作权限，同时用自定义 viz/ref/file 块验证一个单向静态导出器。原截图中的交互可视化/@块不再称为当前官方文档确认。

## 来源核实

- https://learn.chatgpt.com/docs/space
- https://learn.chatgpt.com/docs/space/collaboration
- 原帖作者入口：https://x.com/gengdaJ

当前协作页列出 View/Comment/Edit、Slides View/Edit 和继承权限；链接来源保留原权限。总览明确分享页面不共享私人聊天或保存的记忆。Link access 不等于已定义匿名公开。

## 带来的概念

- [[快照契约与不可变只读]]：追加静态交付与源页面分离，不把所有导出绝对化为死快照。
- [[只读闸门三原则]]：分享角色、来源权限和敏感内容需分别检查，不能只复制链接。
- [[第二大脑LLMWiki]]：Pages 是产品化沉淀通道之一。

## 实验做了什么

初稿单向导出误称往返且路径会失败。修订后默认新增 `space-demo-export-v2.md`，6 块顺序与 viz/ref/file 降级标记明确，5 项 unittest 通过。它只验证自定义单向导出，不是 Space 真实导出器。

## 坑与结论

- 未创建 Space、分享或导出；真实交互、历史版本和原位文件编辑未验证。
- v2 指南逐页渲染审核，原 PDF 保留，manifest 指向 v2。
- 指南：`chatgpt_space_workflow/chatgpt-space-guide.html`；审核版：`chatgpt_space_workflow/ChatGPT-Space页面工作流-小白指南-v2.pdf`。
