# TikHub 动手实验日志（全部真实运行，2026-10-02）

环境：Windows 11 + curl (Git Bash) + python 3。无注册账号（无法收邮件），采用**协议级探测**路线：无认证元端点 + 假 Key 行为分析（与 agentkey 实验同模式）。

| # | 实验 | 命令要点 | 真实结果 |
|---|---|---|---|
| 1 | 健康检查（无认证） | `curl https://mcp.tikhub.io/health` | `{"status":"healthy","version":"2.0.0","platforms":17,"total_endpoints":1003}` ✅ |
| 2 | 平台清单（无认证） | `curl https://mcp.tikhub.io/platforms` | 17 平台全列表，每平台 endpoint_count（douyin 319 / tiktok 162 / instagram 93…）+ 各自 mcp_url/sse_url ✅ |
| 3 | 无 Key initialize | POST `/tiktok/mcp` JSON-RPC initialize | HTTP 401 + `www-authenticate: Bearer realm="TikHub MCP"`（**无 resource_metadata**，非 OAuth 发现）+ JSON-RPC 错误信封 code -32001 ✅ |
| 4 | 无 Key tools/list | POST 同上 tools/list | HTTP 401 ✅ |
| 5 | 假 Key initialize | `Authorization: Bearer tk_fake_key_123` | **HTTP 200 通过！** SSE 事件流格式返回 `serverInfo: "TikHub TikTok MCP" v1.20.0` + instructions ✅ |
| 6 | SSE 端点 GET 无 Key | GET `/tiktok/sse` | HTTP 401（SSE 入口在网关层就挡） |
| 7 | 不存在平台 | GET `/nonexistent/mcp` | 401（认证先于路由，不泄露平台存在性） |
| 8 | 抓会话头 | initialize 响应头 `Mcp-Session-Id` | `4f76c3aa5eb649d5baa2d6302dd7e39f`（无 Key 时无此头） |
| 9 | 假 Key tools/list 带会话 | POST + `Mcp-Session-Id` | **200 放行**，返回完整工具目录（name/description/inputSchema/outputSchema）✅ |
| 10 | 假 Key tools/call（数据面） | 调 `tiktok_web_fetch_post_detail` | MCP 协议 200 成功信封，**业务错误藏在 content[0].text**：`{"error":"unauthorized","status":401,...}` ✅ |
| 11 | 工具目录体积实测 | tools/list 全量落盘 + python 统计 | TikTok 平台 **162 个工具**（与 /platforms endpoint_count 精确一致）；目录 JSON 99,386 字符 ≈ **24,846 tokens** ✅ |

## 核心结论

1. **控制面开放、数据面计费**：initialize / tools/list 不验 Key（网关只挡"完全没有 Authorization 头"），Key 真正校验发生在 tools/call 上游调用时。工具目录对任何人可见 = 免费的产品橱窗，付费点在数据。
2. **401 两种形态**：网关层 401（HTTP 状态码 + www-authenticate）vs 数据层 401（HTTP 200 + 工具结果内嵌 error JSON）——后者让 LLM 能读到错误原因并自我纠正，是 MCP 错误设计的常见取向。
3. **上下文膨胀量化**：单平台 162 工具 ≈ 2.5 万 token 的目录开销，占了常见 128k 上下文的 ~20%。所以 TikHub 按 17 平台拆 MCP 服务器并建议"只添加你用的平台"——这就是它对 1000+ 工具问题的唯一解法（无工具搜索/分页机制）。
4. **协议版本**：serverInfo v1.20.0 / 平台服务 version 2.0.0；响应走 SSE 事件流封装（`event: message` + `data:`），即使 Accept 已含 application/json。
