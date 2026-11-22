---
tags: [项目笔记]
类别: 知识学习类（集成契约）
来源项目: higgsfield_codex_workflow
完成日期: 2026-11-22
---

# higgsfield_codex_workflow：三通路契约与本地预算实验

## 项目是什么

学习 Higgsfield CLI/MCP/Computer Use 三种接入及账号、积分、责任与 Skills 边界。官方当前说明异步轮询和 Assets，但没有公开具体任务状态枚举或任务查询命令。

## 来源核实

- https://higgsfield.ai/cli
- https://higgsfield.ai/creator-hub/help-center/integrations/how-do-i-access-higgsfield-via-cli
- 官方公告：https://x.com/higgsfield/status/2105354097788412063

CLI/MCP 账号登录，Higgsfield API 是另一 key 制产品；同账号同积分率，Unlimited/免费生成不适用；Developer Terms 要求保护会话并承担生成责任；两种 Skills 不同。

## 带来的概念

- [[能力层与后端路由]]：追加 CLI/MCP/GUI 的证据不可互换，不另建“三通路分工”同义条目。
- [[异步任务五态契约]]：官方有轮询但无状态枚举，本地五态只作参考。
- [[付费调用回执与预算熔断]]：账号会话、积分与生成责任一起入账。

## 实验做了什么

初稿只有决策表。新增本地 `route_contract.py` 与 8 项测试：三通路证据、Unlimited/未知通路拒绝、预算 500→260 后拒绝 300、通用终态验收和非法迁移。全部通过，未连接平台。

## 坑与结论

- 未真实安装、登录、生成、扣费或验证 Assets/Computer Use。
- 阈值和批量大小是示例，不是官方建议。
- v2 指南逐页渲染审核，原 PDF 保留，manifest 指向 v2。
- 指南：`higgsfield_codex_workflow/higgsfield-guide.html`；审核版：`higgsfield_codex_workflow/Higgsfield-Codex工作流-小白指南-v2.pdf`。
