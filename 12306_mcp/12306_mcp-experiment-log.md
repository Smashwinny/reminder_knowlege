# 实验日志 · 12306-mcp

- 实验：MCP stdio 客户端五步真实查询（exercise/mcp_client.mjs）
- 环境：Windows 11 Pro，Node v24.21.0 / npm 11.19.0，PYTHONUTF8=1
- 日期：2026-10-07
- 上游：github.com/Joooook/12306-mcp @ ff6439d（浅克隆）

## 实验设计

1. `repo/`：`npm i --ignore-scripts`（跳过生命周期脚本）+ `npx tsc` 手动编译出 build/index.js。
2. `exercise/mcp_client.mjs`：用 @modelcontextprotocol/sdk 的 Client + StdioClientTransport，把服务器当子进程拉起，依次调用 listTools → get-current-date → get-station-code-of-citys → get-tickets → get-train-route-stations。
3. 每步打印真实返回；完整输出存 exercise/run_output.txt。

## 真实执行记录

### 运行 1（失败，路径 bug）

`import.meta.url.pathname` 在 Windows 下产生 `/F:/...`，拼出 `F:\F:\...` → MODULE_NOT_FOUND。
修复：改用 `fileURLToPath`。

### 运行 2（失败，参数名不符）

按文档猜的参数名 `cityNames` 被 zod 拒绝：`Required at citys`。
教训：参数名以源码 zod schema 为准——get-station-code-of-citys 用 `citys`；get-train-route-stations 用 `trainCode`+`departDate`（不是 trainNo/fromStation/toStation）。

### 运行 3（成功，exit=0）

- 服务器启动后打印 "12306 MCP Server running on stdio"，listTools 返回 8 个工具。
- get-current-date → `2026-10-07`（上海时区正确）。
- get-station-code-of-citys("北京|上海") → `{"北京":{"station_code":"BJP"},"上海":{"station_code":"SHH"}}`。
- get-tickets(2026-10-08, 北京, 上海, G) → 真实余票表 6521 字符，含 G1 北京南→上海虹桥 04:54 历时、二等座 661 元剩余 1 张等。**中文城市名直接被接受**（内部自动翻译为 telecode）。
- get-train-route-stations(G531, 2026-10-08) → 13 个经停站到发时刻（北京南 06:08 发 → 上海虹桥 12:04 到）。
- 最后打印 "✅ 全部调用成功"。

## 结论与坑

- ✅ 端到端链路真实打通：MCP 握手 → 工具发现 → 中文翻译 → 12306 实时余票 → 经停表。
- ✅ 分层设计实证：基础工具（城市→代码）确实被核心工具依赖，LLM 无需知道 BJP/SHH。
- 坑 1（Windows）：ESM 的 `import.meta.url.pathname` 带前导斜杠，取文件路径必须 `fileURLToPath`。
- 坑 2（接口契约）：文档与 schema 可能不一致，以 zod schema 为准（citys / trainCode / departDate）。
- 坑 3（安全执行）：克隆仓库的 `npm i` 会触发生命周期脚本，本实验用 `--ignore-scripts` + 手动 `npx tsc` 规避。
- 局限：未测中转工具（get-interline-tickets，源码注明只回前 10 条）；未测 HTTP/SSE 模式；余票为查询时刻快照，12306 接口改版可能导致失效。
