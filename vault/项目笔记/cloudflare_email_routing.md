---
tags: [项目笔记, 基础设施, 邮箱, Cloudflare]
created: 2026-10-07
---

# Cloudflare Email Routing（邮件路由）

- 来源：@太阳 taiyanghere 推文 https://x.com/taiyanghere/status/2107119143577436176（466 赞）及其引用推文（Northwest .com 促销，时效背景）
- 核实依据：Cloudflare 官方文档 email-service 文档体系（2026-10-07 逐页读取）+ 本地模拟器实验 13/13 断言

## 是什么

Cloudflare 免费入站邮件转发器：MX 接住发往自有域名的邮件 → 按路由规则匹配 → 转发到已验证的目标邮箱，或交给 Workers `email()` 函数处理，或 drop。免费/付费计划均可用；向已验证目标地址发送免费。

## 核心机制（实验验证）

- **匹配优先级**：完整 local part 精确规则 > RFC 5233 subaddressing 回退（`user+tag@` 匹配 `user@`，+tag 保留在 message.to）> catch-all（接拼错地址）。同 pattern 多条规则仅列表首条生效。
- **动作三选一**：Send to email（转发）/ Send to Worker（编程处理）/ Drop（删除不路由）。每规则 1 个 action，多目标要 Worker 循环 forward。
- **destination address**：先发验证邮件，点击后才生效；未验证则所有用它规则禁用。每账户 200 个，跨域名复用。
- **DNS**：MX×3（route1/2/3.mx.cloudflare.net）+ SPF `v=spf1 include:_spf.mx.cloudflare.net ~all`（已有 SPF 要合并，查询≤10）+ DKIM（cf2024-1._domainkey）。
- **上限**：200 规则/域名、200 目标/账户、入站 25 MiB、收件人 50、主题 998 字符。

## 边界与坑

- 转发 ≠ 托管：只能收不能发；对外发信需 Gmail"其他地址发送"或别的 SMTP。出站 Email Sending 是另一项 Beta（Workers 付费）。
- 不能与外部邮件服务器共存（MX 必须指向 CF）；迁移需先解锁再并行切换。
- 原帖".com 权重高"无可核对证据，待证；Northwest 促销是时效性第三方主张。

## 用法

每个网站一个别名（`github@域名`/`taobao@域名`）→ 全部汇入真实邮箱；泄露的别名直接 drop；catch-all 保证不丢邮件；进阶用 Worker 把邮箱变成 webhook（自动回复/工单/入库）。

## 关联

- [[负载均衡与反向代理]]、[[缓存有效期与发布边界]]（CF 基础设施品味区）
- [[证据优先质检ProofOverClaims]]（对"权重高"口号的态度）
- 概念提案：邮件路由与无限别名（见项目目录 knowledge-proposal.md，协调者终审）
