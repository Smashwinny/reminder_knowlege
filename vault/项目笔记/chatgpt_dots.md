---
tags: [项目笔记]
类别: 知识学习类（常驻Agent产品机制）
来源项目: chatgpt_dots
完成日期: 2026-11-22
---

# chatgpt_dots：多模型常驻与本地持久交接协议

## 项目是什么

学习 Dots 云端常驻、授权本机、派生任务和 takeover/return control。2026-11-22 当前文档已是多模型，支持连接多台电脑且每线程一次一台；旧“只用 Astra/只能一台”口径已纠正。

## 来源核实

- https://learn.chatgpt.com/docs/dots
- https://learn.chatgpt.com/docs/dots/computers-and-apps
- 原引用帖作者入口：https://x.com/LiuweijiaVip

本机使用时需在线和 ChatGPT 应用开启，云浏览器不继承本机登录；渠道/插件/电脑权限分别管理。当前未文档化快照创建/恢复。首月扩展额度不是全免，Edu/Healthcare 合格工作区条件已更新。

## 带来的概念

- [[常驻任务执行位置三分法]]：云端/本机/派生任务的条件、权限和计费分开。
- [[显式控制权交接协议]]：显式转换、真实快照、持久审计和 fail-closed。
- [[共享环境非隔离原则]]：每线程一台不是安全隔离证明。

## 实验做了什么

初稿仅内存 history 却声称快照/落盘。修订后每次转换原子写 JSON，完整交接后重载状态/历史/快照一致，红线 STOPPED 也可重载；8 项 unittest 全部通过。快照和红线是本地协议，不是官方功能证明。

## 坑与结论

- 未连接真实电脑、验证 Dots、Blender、账单或硬件配置。
- v2 指南逐页渲染审核，原 PDF 保留，manifest 指向 v2。
- 指南：`chatgpt_dots/chatgpt-dots-guide.html`；审核版：`chatgpt_dots/ChatGPT-Dots-小白指南-v2.pdf`。
