---
tags: [概念]
领域: AI Agent / 本地服务安全
别名: ["localhost hardening", "本地端点加固", "DNS rebinding 防护", "四道安全门"]
首次来源: "[[项目笔记/chat-on-steroids]]"
---

# 本地MCP端点安全四道门

**一句话定义**：本机回环（127.0.0.1）上的 MCP/HTTP 服务在处理任何请求前依次执行的四道独立检查——秘密令牌路径、Host 环回校验、Origin 环回校验、body 体积上限——用于挡住扫描器、DNS 重绑定、浏览器跨域驱动和恶意巨型包。

**属于领域**：AI Agent / 本地服务安全（[[MCP服务器]] 的暴露面安全；[[沙箱与审批正交]] 管的是"进来之后能碰什么"，本笔记管"谁有资格进来"）

**通俗理解**（比喻/例子，讲完落回术语）：只监听 127.0.0.1 像"家门只朝院内开"，但**浏览器是院里最不可信的访客**。DNS 重绑定（DNS rebinding）攻击：恶意网页让你访问 evil.com，其 DNS 先解析到攻击者服务器，随后把记录切到 127.0.0.1——你的浏览器仍以为在跟 evil.com 通信，请求却打进了本机服务；**同源策略管不住它，因为脚本眼里这还是"自己的源"**。chat-on-steroids 的 server.ts 对策四道门：① URL 路径携带每次会话随机生成的 token 段，用 `timingSafeEqual` 恒时比对（防时序侧信道猜 token）；② Host 头必须是 loopback（DNS 重绑定后 Host 是 evil.com，直接拦）；③ 若请求带 Origin 头（说明是浏览器发起），Origin 也必须是 loopback（挡任意网页跨域 fetch）；④ body ≤ 8MB。绑定时用 ephemeral port 且永不 0.0.0.0（局域网不可达）。

**与已有概念的关联**：
- [[MCP服务器]] / [[MCP协议]]：本模式是任何本地 MCP 端点的通用安全前置层
- [[OAuth资源发现]]：chat-on-steroids 的隧道端还做 RFC 9728 protected-resource metadata，与四道门同层协作
- [[GUI自动化下单]]：同样是"本地服务+浏览器"形态，若暴露本地端口同样适用四道门
- [[沙箱与审批正交]]：门（谁能连）与沙箱（连上后能干什么）是正交的两层防线

**实测坑**：用 Node 内置 fetch 模拟"伪造 Host"会失败——undici 把自定义 `host` 头当 forbidden header 剥掉，导致攻击永远打不中；测安全逻辑要用 `node:http` 原生 request。实验 E2 实测 6 请求：404/403/403/413/404/200 全部按预期。

**首次接触于**：[[项目笔记/chat-on-steroids]]（src/main/mcp/server.ts 注释写明设计动机）

## Toolbox 实证增补（2026-10-05）

[[项目笔记/mcp_toolbox]] 只验证 stdio 及数据库主库连接；未配置工具返回 -32602 不证明身份鉴权。HTTP、Host/Origin、OAuth、命名端点和租户隔离未在本项目验收。
