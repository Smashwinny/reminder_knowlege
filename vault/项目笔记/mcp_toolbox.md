# MCP Toolbox：数据库执行权限与工具提示

学习审核日期：2026-10-05；任务完成由本人点击。

## 实际项目与证据

Toolbox 将数据库 source、tool 和 toolset/group 连接到 MCP 客户端。观察源码固定 a24e5e68567fa014a42fc6cc711faa82b964d4c0，实际执行 v1.13.1/e14cda6b4f483e6b5e5ec23e342f9f232a6ce60f Linux 发布程序。作者与独立审核者分别实际通过同一组 MCP 26 项，另有独立 CLI 5 项。

预制工具列出 execute_sql/list_tables，合成主库两行 apples=4、pears=7；通过 mode=ro 拒绝 INSERT、UPDATE、DELETE、CREATE TABLE 及 query_only 重置后的 INSERT，数据及主库文件 SHA256 不变。可写独立负对照即使 readOnlyHint=true 仍实际写入第三行。

固定 name=? 语句使 SQL 外观输入保持普通值；整数触发参数类型错误。未配置工具返回 -32602 是注册范围的证据，不能解释为用户身份鉴权通过。SQLite 的 readOnly:true 字段被程序拒绝，源码 IsReadOnly=false；支持 SQLite 连接不等于支持 Toolbox 的同名只读配置。

## 合并已有概念

- [[MCP协议]] 与 [[代码管边界提示词管判断]]：工具注解描述预期，不是强制权限；客户端看到的提示和数据库实际拒绝分别验证。
- [[只读闸门三原则]]：按引擎、适配器、版本、连接模式和工具验证。mode=ro 本次保护打开的主库，未验证附加库、临时库、扩展或整个进程。
- [[本地MCP端点安全四道门]]：stdio、未知工具、身份鉴权、HTTP 入口属于不同层，未借用旧项目验收本次 HTTP/OAuth。
- [[关系型数据库与NoSQL]]：同属 SQL 数据库不能推导支持相同只读字段。文档矩阵四类云源只做阅读，未实际连接；BigQuery protected 允许会话临时写入。

Windows 六原件校验、全部 13 页 PDF 及五项离线命令检查通过，85 个包内文件和 23 份固定源码指纹一致。Windows 未运行固定 Linux 程序；云端独立复跑证据不混成本机实验数量。

## 成果与后续

[彩色指南](../../mcp_toolbox/MCP-Toolbox-小白指南.pdf)、[练习入口](../../mcp_toolbox/exercise/START_HERE.md)、[真实云端实验日志](../../mcp_toolbox/experiment_log.txt)、[审核说明](../../mcp_toolbox/independent-review.md)。

后续部署先用授权的脱敏数据库、最小权限账号，补租户越权、返回字段、超时、审计、HTTP/OAuth 等测试。本次未验证全部 SQL 副作用或生产安全；HTML 浏览器视觉未验收，原 PDF 由 ReportLab 直接生成。

固定来源：[SQLite 实现](https://github.com/googleapis/mcp-toolbox/blob/e14cda6b4f483e6b5e5ec23e342f9f232a6ce60f/internal/sources/sqlite/sqlite.go)、[只读文档](https://mcp-toolbox.dev/documentation/configuration/security/read-only/)、[MCP 注解](https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations)。
