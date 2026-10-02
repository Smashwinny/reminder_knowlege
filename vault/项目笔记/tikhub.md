---
tags: [项目]
类别: 商业 SaaS（社交数据 API 平台 + 托管 MCP，核心闭源）
上游: https://tikhub.io · https://mcp.tikhub.io
完成日期: 2026-10-02
---

# tikhub — 一个 Key 买通 17 个社交平台的数据超市

## 这是什么
[TikHub](https://tikhub.io)（核心闭源，GitHub 仅开源 Python/Java SDK 与 .exe 分发）：社交数据采集商业平台，**1003 个 REST 端点 / 1007 个 MCP 工具覆盖 17 个平台**（抖音 319、TikTok 162、Instagram 93…中文平台最深），MCP 托管在 `mcp.tikhub.io/{platform}/mcp`，三种传输（Streamable HTTP / SSE / Stdio 桥接），静态 Bearer 认证。定价：注册赠 ~50 次请求 + $0.05，按量 $0.001-0.01/次，日用量阶梯折扣最高 -50%，失败不计费；另有 10 亿+ 条预采集数据集（量大每千条 $0.40）与 Marketplace（佣金 10%）。

## 带来的概念
- [[工具目录膨胀]]（新）：工具目录是上下文里最大的隐形账单，实测单平台 162 工具 ≈ 24,846 tokens；解法谱系=按域拆分 / 分层按需加载 / 动态工具发现
- [[控制面与数据面]]（新）：认证闸门装在哪是架构决策——TikHub 控制面全开放（假 Key 实测通过 initialize+tools/list），数据面才验 Key；401 有网关层/工具结果内嵌两种形态
- 关联强化：[[统一数据网关]]（三部曲正主收编）、[[MCP协议]]、[[stdio与流式HTTP传输]]（三种传输全配齐）、[[分层按需加载]]、[[KV缓存与上下文]]、[[OAuth资源发现]]（对照：TikHub 不走发现路线）

## 实验做了什么（exercise\experiment-log.md，11 项全部真实运行，零注册协议级探测）
1. GET /health（免认证）→ `{"status":"healthy","version":"2.0.0","platforms":17,"total_endpoints":1003}` ✅
2. GET /platforms → 17 平台端点数全清单（douyin 319…）✅
3. 无 Key initialize → HTTP 401 + `www-authenticate: Bearer realm="TikHub MCP"`（无 resource_metadata，非 OAuth 发现）+ JSON-RPC -32001 ✅
4. 假 Key `tk_fake_key_123` initialize → **HTTP 200 放行**，serverInfo "TikHub TikTok MCP" v1.20.0 ✅
5. 假 Key tools/list（带 Mcp-Session-Id）→ 完整工具目录放行 ✅
6. 目录量化：162 工具 / 99KB / ≈24,846 tokens（与 endpoint_count 精确一致）✅
7. 假 Key tools/call → MCP 200 成功信封内嵌 `{"error":"unauthorized","status":401}`（协议成功、业务失败）✅
8-11. SSE 入口无 Key 401 / 不存在平台 401（认证先于路由）/ 会话头对比 / 响应恒为 SSE 封装 ✅

## 坑与结论
- **工具目录=免费橱窗，闸门在数据面**：目录公开是获客策略，掏钱时刻=真实取数
- **响应永远 SSE 封装**（`event: message`+`data:`），解析记得剥壳；`Mcp-Session-Id` 必须全程携带
- **部分接口仅限付费**：免费额度可能被跳过、直接扣付费余额
- **合规灰色地带**："公开可见"≠"允许程序化采集"，ToS 风险自担，当原型/研究加速器最稳
- **三部曲终局**：Agent Reach 把复杂性留给硬盘（免费自养）→ AgentKey 卖进订阅（open-core）→ TikHub 卖进按次账单（纯商业）。选型本质是选择支付复杂性的货币：**时间 / 月费 / 单价**
