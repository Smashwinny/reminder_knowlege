---
tags: [概念]
领域: AI 工具生态 / 认证协议
别名: [RFC 9728, Protected Resource Metadata, MCP免密接入]
首次来源: "[[项目笔记/agentkey]]"
---

# OAuth 资源发现

**一句话定义**：服务端对未认证请求返回 401，并在 `WWW-Authenticate` 头里给出元数据 URL，客户端据此自动发现 OAuth 授权服务器——全程免手工贴 API Key。

**属于领域**：MCP 远程服务器的标准接入认证方式（RFC 9728 Protected Resource Metadata）。

**通俗理解**：像到前台问路——你（Agent 客户端）没带工牌进门被拦（401），前台递给你一张指路条（`WWW-Authenticate: Bearer resource_metadata="…/.well-known/oauth-protected-resource"`），你照着条子找到发证处（authorization server）自动办证，之后凭证通行。讲完比喻落回术语：401 不是终点而是**引导**，配置里只需写 URL 不需写任何凭证。

**与已有概念的关联**：
- 相关：[[MCP协议]] 与 [[stdio与流式HTTP传输]]（远程 HTTP 传输的配套认证）、[[JSON-RPC与stdio传输]]（报文仍走 JSON-RPC）、[[统一数据网关]]（AgentKey 用它实现"一条命令接入 40+ Agent"）
- 坑：若客户端配置里写了静态 `Authorization` 头，Claude Code 会视为显式头认证，401 后**不再回退** OAuth 发现流程（AgentKey 仓库 CLAUDE.md 明示）

**首次接触于**：[[项目笔记/agentkey]]
