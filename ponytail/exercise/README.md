# Ponytail sql-user 教学实验

本包是基于真实上游任务的自写工程对比，不是 Ponytail 插件安装包，也不是 Haiku 4.5 agentic benchmark 复现。上游所有内容仅静态阅读；脚本不导入、不执行上游参考片段。无付费 API、第三方 Python 依赖或外部网络请求。

## 来源及改编

DietrichGebert/ponytail 固定提交 e15862bb04d04285233a164460ced063941d9ef5：
https://github.com/DietrichGebert/ponytail/blob/e15862bb04d04285233a164460ced063941d9ef5/benchmarks/agentic/tasks.py

upstream-sql-user-reference.txt 原样摘取 sql-user 一节，含原始 seed、评分器和 good/bad 参考字符串。其 alice/bob 假数据及注入载荷用于追踪本次任务来源；保留 LICENSE-upstream.txt。其余 Python 文件是本次自写实现和测试，未运行上游参考实现或评分器。

## 同一契约

get_user(conn, username) 返回 (id, username, email) 元组或 None。conn 是调用者创建并拥有的 sqlite3.Connection；users 表具有 id、username、email 三列，username 唯一。没有唯一约束时，重名结果不保证顺序，这不在契约内。

在上游简短 seed 之上，本实验明确补充：username 必须为 str，长度 1..64 个 Unicode 字符且不含 NUL；错误类型分别 TypeError/ValueError。不会剥除空格或改变大小写。SQLite 操作错误继续抛出，不把故障伪装成“用户不存在”。返回值在默认 row_factory 和 sqlite3.Row 下均为 tuple。函数不提交、回滚或关闭调用者连接。自定义 row_factory 和并发访问不在范围内。

minimal.py 直接验证再参数化查询；layered.py 使用 5 类、7 个函数/方法承担同一工作。复杂版故意展示此单一需求下多余的层次，不代表所有 Repository 模式都不合理。两个实现安全机制相同。

## 六步复做

解压后进入 ponytail-exercise 文件夹，用 Python 3.12（仅标准库）执行以下真实验证过的命令：

1. python3 inspect_source.py
   目的：静态核对真实任务和版本。成功：打印 PASS、固定提交和片段 SHA-256；上游代码未执行。
2. python3 demo.py minimal alice
   目的：最小版跑通正常查询。成功：(1, 'alice', 'a@x.com')。
3. python3 demo.py layered alice
   目的：检查复杂版提供同样入口和结果。成功：与第二步完全一致。
4. python3 demo.py minimal "x' OR '1'='1"
   目的：看危险字符串被当作普通值。成功：None，而不是 alice。
5. python3 test_lookup.py
   目的：两版执行完全同一契约检查及负对照。成功：21 项/版，共 42 项通过，另抓住 1 个故意不安全的负对照。
6. python3 audit_sources.py
   目的：把结构差异和功能证据分开。成功：minimal 10 行/0 类/1 函数；layered 38 行/5 类/7 函数。行数为非空非注释物理行，包含 docstring，不是 git diff 新增行。

test_lookup.py 中 unsafe_negative_control 仅为验证测试敏感度，在一次性内存数据库和假数据上执行。故意拼接 SQL 会泄露假记录，不能复制到真实项目。

## 结果范围

只证明两份特定实现通过这批有限检查、该负对照可被识别。没有运行模型、上游 hook、服务器、浏览器、权限系统、真实业务数据库、付费 API、并发/延迟测试或全部上游任务。不推断节省 token、费用或时间，更不能宣称完整安全。

## 自查题

- 为什么 TypeError 与 SQLite OperationalError 不应都变成 None？
- 如果增加第二种数据库，哪一层可能开始有真实价值？先写需求再决定保留。
- 为什么带引号的合法姓名应当成功，而 OR 注入载荷不应返回别人？
- 10 行比 38 行小，为什么仍不能证明 Ponytail 对所有模型有效？

中文建议使用 UTF-8；本次没有更改全局环境变量、安装依赖或写生产数据。
