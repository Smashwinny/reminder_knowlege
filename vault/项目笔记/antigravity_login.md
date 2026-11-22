---
tags: [项目笔记]
类别: 知识学习类（排查方法论+工具审计）
来源项目: antigravity_login
完成日期: 2026-11-22
---

# antigravity_login：当前访问政策与固定数据流标记

## 项目是什么

学习 Antigravity 登录失败的资格、授权网络、额度和 ToS 分层，并静态审计 Manager/Bridge 两类第三方工具。未登录或运行工具。

## 来源核实

- 当前 FAQ：https://antigravity.google/docs/faq/
- Terms：https://antigravity.google/terms
- Manager 固定 0067fe0；Bridge 固定 2c8c12d；原帖：https://x.com/Delroy715/status/2102267215819296905

当前官方禁止第三方访问，可暂停/终止 Antigravity 和/或 Gemini CLI 账户；FAQ 替代路径为 AI Studio/Gemini Enterprise。封禁潮、全 Google 影响和通用封号申诉均不冒充官方事实。资格含地区、年龄与账号类型。

## 带来的概念

- [[登录排查四层拆解]]：资格/授权网络/额度/服务限制分别取证。
- [[第三方工具数据流审计]]：端点、凭据路径、许可与当前授权分层。
- [[OAuth资源发现]]：标准认证不授予违反产品条款的访问权。

## 实验做了什么

固定 Manager 命中端点 9/10/3 文件、token 文件名 5 文件，LICENSE 为 CC-BY-NC-SA；6 项 unittest 通过。Bridge 的“不碰凭据”只保留为 README 自述，未全量验证。

## 坑与结论

- 静态标记不证明完整运行数据流；社区封禁和价格宣传未核实。
- v2 指南逐页渲染审核，原 PDF 保留，manifest 指向 v2。
- 指南：`antigravity_login/antigravity-login-guide.html`；审核版：`antigravity_login/Antigravity登录排查-小白指南-v2.pdf`。
