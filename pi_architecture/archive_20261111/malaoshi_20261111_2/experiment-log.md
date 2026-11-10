# Pi 架构：真实主实验日志
时间均为 Asia/Shanghai UTC+8。未启动 Pi 主 CLI，未调用模型；步骤 1 仅公共 npm 下载。
## 1 准备精确发布物

时间：2026-11-11T00:56:39.917917+08:00（Asia/Shanghai）

工作目录：`/workspace/reminder-batch/item-2-pi-architecture/exercise/lab`

```bash
node --version && npm --version && npm pack @earendil-works/pi-coding-agent@0.84.2 --ignore-scripts --json > pack.json && tar -xzf earendil-works-pi-coding-agent-0.84.2.tgz && node -e "const p=require('./package/package.json'); console.log(p.name+'@'+p.version)"
```

真实输出：
```text
v24.22.1
11.21.1
@earendil-works/pi-coding-agent@0.84.2

```

退出码：0

## 2 发布物身份与旧功能边界

时间：2026-11-11T00:56:40.556678+08:00（Asia/Shanghai）

工作目录：`/workspace/reminder-batch/item-2-pi-architecture/exercise/lab`

```bash
node manifest.mjs
```

真实输出：
```text
@earendil-works/pi-coding-agent@0.84.2
own deps: @earendil-works/pi-agent-core,@earendil-works/pi-ai,@earendil-works/pi-client,@earendil-works/pi-protocol,@earendil-works/pi-tui
PASS: version/dependencies/exports; not a runtime MCP conformance test

```

退出码：0

## 3 四快照生产依赖闭包

时间：2026-11-11T00:56:40.587519+08:00（Asia/Shanghai）

工作目录：`/workspace/reminder-batch/item-2-pi-architecture/exercise`

```bash
python3 graph.py
```

真实输出：
```text
{"sha": "914cf1472e715297caa30db4b9535d534a9eb718", "workspaces": 9, "non_private": 8, "product": "0.84.2", "direct": ["pi-agent-core", "pi-ai", "pi-client", "pi-protocol", "pi-tui"], "closure": ["pi-agent-core", "pi-ai", "pi-client", "pi-coding-agent", "pi-protocol", "pi-telemetry", "pi-tui"]}
{"sha": "06a466935536f8c9bcacb2d5efc0fc021be1bdff", "workspaces": 11, "non_private": 10, "product": "1.2.0", "direct": ["pi-agent-core", "pi-ai", "pi-codemode", "pi-mcp", "pi-tui"], "closure": ["pi-agent-core", "pi-ai", "pi-codemode", "pi-coding-agent", "pi-mcp", "pi-telemetry", "pi-tui"]}
{"sha": "65c43bb520edf53f11923f7a927aefd05475c6af", "workspaces": 12, "non_private": 11, "product": "1.5.2", "direct": ["pi-agent-core", "pi-ai", "pi-codemode", "pi-mcp", "pi-tui"], "closure": ["pi-agent-core", "pi-ai", "pi-codemode", "pi-coding-agent", "pi-mcp", "pi-schema", "pi-telemetry", "pi-tui"]}
{"sha": "b30d54b8aebe6408e02d1473446d25f8083da68f", "workspaces": 12, "non_private": 11, "product": "1.5.2", "direct": ["pi-agent-core", "pi-ai", "pi-codemode", "pi-mcp", "pi-tui"], "closure": ["pi-agent-core", "pi-ai", "pi-codemode", "pi-coding-agent", "pi-mcp", "pi-schema", "pi-telemetry", "pi-tui"]}
PASS: 4 pinned snapshots; manifest hashes and production-closure assertions

```

退出码：0

## 4 真实开关函数十用例

时间：2026-11-11T00:56:40.620810+08:00（Asia/Shanghai）

工作目录：`/workspace/reminder-batch/item-2-pi-architecture/exercise/lab`

```bash
node switch.mjs
```

真实输出：
```text
{"env":"<unset>","setting":true,"got":true}
{"env":"<unset>","setting":false,"got":false}
{"env":"0","setting":true,"got":false}
{"env":"false","setting":true,"got":false}
{"env":"no","setting":true,"got":false}
{"env":"","setting":true,"got":false}
{"env":"garbage","setting":true,"got":false}
{"env":"1","setting":false,"got":true}
{"env":"TRUE","setting":false,"got":true}
{"env":"yes","setting":false,"got":true}
PASS: 10 telemetry-switch cases; no fetch or model invocation

```

退出码：0

## 5 真实编译方法+mock请求五分支

时间：2026-11-11T00:56:40.652287+08:00（Asia/Shanghai）

工作目录：`/workspace/reminder-batch/item-2-pi-architecture/exercise/lab`

```bash
node ping-mock.mjs
```

真实输出：
```text
{"url":"https://pi.dev/api/report-install?version=0.84.2","opts":{"headers":{"User-Agent":"pi/0.84.2 (linux; node/v24.22.1; x64)"},"signal":{"mockTimeoutMs":5000}}}
branch {"setting":true,"count":1} mock requests 1
branch {"flag":"0","setting":true,"count":0} mock requests 0
branch {"offline":"1","setting":true,"count":0} mock requests 0
branch {"offline":"0","setting":true,"count":0} mock requests 0
branch {"setting":false,"count":0} mock requests 0
PASS: 5 mocked branches; no real fetch or model invocation

```

退出码：0

## 6 输入完整性及范围复核

时间：2026-11-11T00:56:40.689685+08:00（Asia/Shanghai）

工作目录：`/workspace/reminder-batch/item-2-pi-architecture/exercise`

```bash
python3 final-check.py
```

真实输出：
```text
PASS: tarball SHA1 e4d4c1e769963c816959f5cea02a0a10ccc0495a; 4 snapshots present
LIMIT: no CLI session, provider, MCP interop, server privacy, or user machine tested

```

退出码：0
