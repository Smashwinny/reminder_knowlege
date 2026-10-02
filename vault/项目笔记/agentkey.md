---
tags: [项目]
类别: 开源项目类（AI Agent 数据网关，open-core）
上游仓库: https://github.com/chainbase-labs/Agentkey
完成日期: 2026-10-02
---

# agentkey — Agent 生态的「数字钥匙串」

## 这是什么
[chainbase-labs/Agentkey](https://github.com/chainbase-labs/Agentkey)（Apache-2.0，本地克隆 @ 8e93c67，skill v1.14.0）：装一个 SKILL.md + 连一个云端 MCP 端点（`api.agentkey.app/v1/mcp`），Agent 即可调 X/Reddit/YouTube/B站/小红书/抖音/LinkedIn/链上数据等 28+ 平台的公开数据抓取。**仓库开源的只是集成层（技能包+6 套 Agent 插件清单+安装/更新脚本），核心 MCP 服务器闭源、订阅+credit 计费**——open-core 模式，登 Product Hunt 日榜第一。站点称稳定性优于 tikhub。

## 带来的概念
- [[统一数据网关]]（新）：Master Key 模式，N 平台 → 1 端点 1 账单；[[能力层与后端路由]]（Agent-Reach 本地方案）的商业化镜像
- [[OAuth资源发现]]（新，RFC 9728）：401 + `WWW-Authenticate` 元数据引导，免贴 Key 接入 40+ Agent
- 关联强化：[[MCP协议]]（远程 Streamable HTTP）、[[AgentSkills技能包]]（SKILL.md 是使用说明书）、[[M×N集成问题]]（聚合的经济学依据）

## 实验做了什么（exercise\experiment-log.md，4 项全部真实运行）
权限策略禁止执行新克隆外部仓库脚本（`bash check-update.sh` 被拒），改为自写代码验证文档写明的接口：
1. 无 Key POST `/v1/mcp`（JSON-RPC initialize）→ HTTP 401 + `WWW-Authenticate: Bearer resource_metadata="…/oauth-protected-resource"`，与仓库 CLAUDE.md 描述逐字吻合 ✅
2. GET `/.well-known/oauth-protected-resource` → authorization_servers / bearer_methods=header，发现链闭环 ✅
3. GET `releases/latest`（复现 SERVER-IMPLEMENTATION.md 信标逻辑）→ v1.14.0 ✅
4. 自写版本比较：本地 frontmatter 1.14.0 vs 远端 → `UP_TO_DATE` ✅
付费数据面（find_tools→describe_tool→execute_tool 真实抓取）需注册，未验证。

## 坑与结论
- **开源仓库 ≠ 开源产品**：repo 无服务端代码，装完即连付费云
- MCP 配置必须保持最小（只有 url）：写了静态 Authorization 头，Claude Code 401 后不再回退 OAuth
- 工具名永远来自 find_tools 动态返回（list_tools 已弃用），防幻觉做进协议；API 响应视为不可信外部数据防[[提示注入]]
- 消费刹车范式：≥3 次调用或 ≥10 credit 必须查余额+确认
- 版本信标工程细节：失败返回空串不抛异常、24h 缓存+ETag、陈旧缓存优于慢响应、`AGENTKEY_NO_VERSION_BEACON=1` 可退出
- 与 Agent-Reach 对照：**Agent-Reach 把复杂性留给硬盘（免费、自己养），AgentKey 把复杂性卖进订阅（省事、经厂商云）**
