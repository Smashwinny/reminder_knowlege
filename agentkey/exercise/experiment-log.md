# AgentKey 动手实验日志（全部真实运行，2026-10-02，Windows 11 / Python 3.13 / Git Bash）

> 权限说明：与 agent-reach 一样，本机权限策略禁止直接执行新克隆的外部仓库脚本
> （`bash check-update.sh` 被拒绝）。因此实验全部改为**自写代码验证架构里写明的接口**，
> 逐条与仓库源码（SKILL.md / SERVER-IMPLEMENTATION.md / .claude/CLAUDE.md）核对。

## 实验1：无认证探测 MCP 远程端点（验证 RFC 9728 OAuth 发现链）
- 命令：Python urllib POST `https://api.agentkey.app/v1/mcp`，JSON-RPC `initialize`
  （protocolVersion 2025-06-18，clientInfo=probe-script），无 Authorization 头
- 真实输出：
  ```
  HTTP 401
  www-authenticate: Bearer resource_metadata="https://api.agentkey.app/.well-known/oauth-protected-resource"
  {"code":401,"error":"missing authorization header"}
  ```
- 结论：与仓库 .claude/CLAUDE.md 描述逐字吻合——不带静态 header 的 MCP entry 收到 401 后，
  客户端按 RFC 9728 从 `WWW-Authenticate` 拿到元数据 URL 走原生 OAuth 流程。
  **这就是"一条命令装好 40+ Agent、免贴 Key"的底层机制。**

## 实验2：读取受保护资源元数据（401 引导出的下一跳）
- 命令：GET `https://api.agentkey.app/.well-known/oauth-protected-resource`
- 真实输出：
  ```json
  {"authorization_servers":["https://api.agentkey.app"],
   "bearer_methods_supported":["header"],
   "resource":"https://api.agentkey.app",
   "resource_documentation":"https://console.agentkey.app"}
  ```
- 结论：OAuth 服务器 = api.agentkey.app（Clerk，见 CLAUDE.md 对 RFC 6749 重复参数的描述），
  Bearer 走 header，控制台入口在 resource_documentation。发现链完整验证。

## 实验3：复现 SERVER-IMPLEMENTATION.md 的版本信标拉取逻辑
- 命令：GET `https://api.github.com/repos/chainbase-labs/agentkey/releases/latest`
  （User-Agent: AgentKey-Server，与文档代码一致）
- 真实输出：`latest skill release tag: v1.14.0`
- 结论：`agentkey_skill_meta` 工具背后的数据源真实存在，skill-meta-v1 协议可行。

## 实验4：自写代码复现 SKILL.md 预检（本地版本 vs 最新 release）
- 命令：Python 正则读 SKILL.md frontmatter `version:`，与实验3的 tag 比较
- 真实输出：`local=1.14.0 latest=1.14.0` → `UP_TO_DATE`
- 结论：check-update.sh / skill-meta 信标"本地=远端→静默继续"的判定逻辑验证通过。

## 总结论
四项实验都在**不注册、不付费、不执行外部代码**的前提下，验证了 AgentKey 架构文档中
写明的三条关键链路：①401+RFC9728 免贴 Key 接入；②OAuth 发现元数据；
③GitHub Release 版本信标。付费数据面（find_tools/describe_tool/execute_tool 实际调用）
需要账号与信用点，不在本机验证范围。
