# MCP Toolbox × SQLite：真实运行的六步实验

这不是数据库服务器的自写替身：Python 只负责造两份合成 SQLite 数据、启动官方 Toolbox 子进程、发送标准 JSON-RPC/MCP 消息与断言结果。数据库工具由官方二进制实际执行。

## 环境与运行

- Linux x86_64、Python 3 标准库，无 Python 包安装
- 官方 Toolbox v1.13.1，实际版本：1.13.1+binary.linux.amd64.e14cda6
- 源码 tag：e14cda6b4f483e6b5e5ec23e342f9f232a6ce60f
- 测量所得二进制 SHA-256：d8e0df24b5ce9934c8f7ae8466f64ff5512857c5a7e47640301750ee82f92db3
- 校验值证明复跑使用同一字节版本；这不是独立发布的签名校验

在解压后的 exercise 目录运行。ZIP 不含约 300 MiB 的二进制。首次准备需要联网下载官方文件，实验运行只使用本地合成数据库。

```bash
mkdir -p vendor
curl -fL --connect-timeout 15 --max-time 120 -o vendor/toolbox https://storage.googleapis.com/mcp-toolbox-for-databases/v1.13.1/linux/amd64/toolbox
printf '%s  %s\n' d8e0df24b5ce9934c8f7ae8466f64ff5512857c5a7e47640301750ee82f92db3 vendor/toolbox | sha256sum -c -
chmod u+x vendor/toolbox
PYTHONDONTWRITEBYTECODE=1 python3 run.py --output evidence/my-fresh-run
```

`--output` 必须是新目录，脚本拒绝覆盖旧证据。已有官方二进制可用 `--binary /absolute/path/to/toolbox` 指定；脚本先验证精确 SHA-256。该版本仅演示本次固定实验，不代表未来最新版。

## 六步目的、操作与验证

整套六步由上面的 `run.py` 单命令串行执行。每个 Toolbox 命令的真实 argv、时间、请求与响应保存在输出目录。

1. 核对版本并建立两份合成数据库
   - 执行 `toolbox --version` 与 SHA-256 校验
   - Python sqlite3 建 inventory(id,name,qty)，写入 apples=4、pears=7
   - 一份以 `file:///.../readonly.db?mode=ro` 打开，一份为独立 writable.db
   - 验证：版本/字节匹配，记录只读主库起始 hash
2. 发现官方预制工具并读数据
   - `toolbox --prebuilt sqlite/sqlite_database_tools --stdio --disable-version-check --disable-reload --log-level ERROR`
   - 仅对该子进程设置 `SQLITE_DATABASE=file:///.../readonly.db?mode=ro`
   - MCP initialize → notifications/initialized → tools/list → tools/call
   - 验证：只有 execute_sql/list_tables；列出 inventory；SELECT 返回两行；execute_sql 的 readOnlyHint 仍为 false
3. 检验原生只读主库边界
   - 依次 tools/call execute_sql：INSERT、UPDATE、DELETE、CREATE TABLE、`PRAGMA query_only=OFF; INSERT ...`
   - 验证：五次均返回 `attempt to write a readonly database (8)` 工具错误；后续 SELECT 仍为2行、总 qty=11；主库 SHA-256 不变
4. 测试参数绑定与错误审计
   - `toolbox --config <output>/custom.yaml --stdio --disable-version-check --disable-reload --log-level ERROR`
   - 固定查询 `WHERE name = ?`；普通 name=apples 返回一行，`apples' OR 1=1 --` 是普通值并返回空
   - name=123 返回类型错误；调用未配置 execute_sql 返回 -32602 unknown-tool 错误
   - 验证：错误不当成功；清单仅含 lookup_item
5. 加入可写负对照，识破错误提示标签
   - `toolbox --config <output>/hint-control.yaml --stdio --disable-version-check --disable-reload --log-level ERROR`
   - 此合成测试故意给动态 SQL 工具标注 readOnlyHint=true，却连接独立 mode=rw 库
   - INSERT 实际成功；另一连接确认第三行已持久化
   - 验证：提示标签本身不会禁止写入。该错误标签配置仅供测试，不能抄为生产配置
6. 核查 SQLite 不支持的 Toolbox 字段并归档
   - `toolbox --config <output>/unsupported-readonly.yaml --stdio --disable-version-check --disable-reload`
   - SQLite source 上加入 readOnly:true，实际启动以 unknown field "readOnly" 拒绝
   - 验证：最终只读主库 hash 仍不变；输出 results.json、commands.json、mcp-transcript.jsonl 与各子进程 stderr

## 已观察结果

作者第一次运行：2026-10-05 UTC，26/26 检查通过；精确时间见 evidence/run-01/results.json。日志保存原始响应，既区分顶层 JSON-RPC error，也区分 result.isError=true。可写控制 INSERT 的成功不是“错误漏报”：实验用独立 Python 连接确认行数确实从2变3。

## 必须保留的边界

- SQLite 的 mode=ro 是数据库驱动/引擎针对这次打开的主库的边界，不是 Toolbox readOnly 配置支持，也不是全进程沙箱
- 没有测试临时/附加数据库的所有行为；不可声称任意 SQL 绝对无副作用或所有文件都受保护
- 没有用 SQL 关键词/正则黑名单做安全控制
- 固定语句使用普通参数绑定。templateParameters 会改写 SQL 文本，不等于值绑定
- 预制 toolset 筛选被实际执行；stdio 的默认清单含全部已配置工具。错误案例是调用未配置工具，不是完整用户鉴权或命名 HTTP 分组端点的授权证明
- 未使用真实数据库、用户私有数据、凭据、OAuth、云账号、付费 API、外部网络监听或全局 MCP 配置；未修改 OS 网络/安全设置
- 未配置遥测 exporter，禁用启动版本检查；没有声称安装了 OS 网络隔离
- cloud-sql-postgres、cloud-sql-mysql、alloydb-postgres、bigquery 的 readOnly 机制只做源码/文档学习，本次没有云端实测
- BigQuery protected 模式允许会话临时数据写入；不能把 readOnlyHint 解释成普遍“零副作用”

## 来源与许可证

- 官方 README/下载说明：https://github.com/googleapis/mcp-toolbox/blob/e14cda6b4f483e6b5e5ec23e342f9f232a6ce60f/README.md
- SQLite source：https://github.com/googleapis/mcp-toolbox/blob/e14cda6b4f483e6b5e5ec23e342f9f232a6ce60f/internal/sources/sqlite/sqlite.go
- 官方只读文档：https://mcp-toolbox.dev/documentation/configuration/security/read-only/
- SQLite URI：https://www.sqlite.org/uri.html
- MCP 注解：https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations

run.py 是本次自写测试驱动。Toolbox 是 Google LLC 的 Apache-2.0 开源项目，许可全文保存在 LICENSE.toolbox；上游源码及官方二进制的既有版权归原作者。没有修改官方二进制或上游源码。
