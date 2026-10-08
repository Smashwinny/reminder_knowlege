# 实验日志 · magpie 本地模型网关（magpie_gateway）

- 任务：3fee3059-7297-47f6-9ba8-e0ba5fb8b635
- worker：kimi-pool-20261007-w1
- 日期：2026-10-09
- 仓库：yetone/magpie（浅克隆 023f5aa，3836 文件，MIT，~4.3k stars）

## 实验设计

Go 工具链本机未装（`go: command not found`），1425 个测试文件无法执行。实验目标退为宣称结构校验（纯标准库文件级断言）+ 三大核心机制（协议翻译/订阅共享/配置手术）源码阅读。

## 运行记录（全部真实执行，exercise/run_output.txt）

`python validate_magpie.py` → **6/6 通过（exit=0）**：

- T1 四协议处理器 4/4：internal/gateway/{chat,responses,anthropic,gemini}.go 均存在且 >2KB。
- T2 端口 3425 在 18 个 agent 适配器文件中被引用（127.0.0.1:3425 网关地址属实）。
- T3 订阅共享：claude_subscription.go + claudebridge/mcp.go（5923B，MCP 桥接）存在。
- T4 供应商 host 识别：balance.go 按 api.deepseek.com / api.moonshot.cn / api.siliconflow.cn 等 host 识别 ≥3 家。
- T5 Agent 适配器 80 个非测试文件（原子化配置手术实现面）。
- T6 测试文件 1425 个（工程密度宣称属实）。
- 工程统计：Go 2162 / 测试 1425 / internal 包 44。

## 结构阅读实证（纯读取）

- 网关归一化架构：四协议处理器入 internal/gateway/，M×N 压成 M+N。
- 订阅凭证化：驱动真实 claude 二进制 + MCP 桥接（claudebridge/mcp.go），多账号配额故障转移（account_cap/account_rank 测试面）。
- 配置手术：internal/agent/ 80 适配器，改配置保注释保格式可回滚。
- 风险阅读：订阅共享的 ToS 灰区（社区讨论中）、凭证集中风险。

## 结论

- 全部宣称结构属实；magpie 是 vault [[BYOK模型网关与用量归因]] 概念的旗舰实现+能力超集（BYOK→BYSOL 订阅凭证化→四协议翻译）。
- 未验证（诚实声明）：Go 测试未执行（无工具链）；网关未真实运行（系统级变更+需真实凭证）；订阅共享 ToS 合规未评估；~4.3k stars 为搜索时点数会变动。

## 产物

- `exercise/validate_magpie.py`、`exercise/run_output.txt`
