# MCP Toolbox：实际知识查重与增量判断

日期：2026-10-05 UTC。项目：googleapis/genai-toolbox（当前源码模块与文档使用 MCP Toolbox）。本次源码固定到 a24e5e68567fa014a42fc6cc711faa82b964d4c0；实际运行结果另见主实验日志，本文件不先行填写实验成功。

## 结论

已有知识已经包含 MCP 的连接协议、驱动层只读、工具与表白名单、审计，以及“代码承担硬边界”的原则。此次不应重建这些同义概念。真正值得补充的是：在 Toolbox 的具体源、工具和工具组中，分别找出真正拒绝写入的执行机制、缩小暴露面的目录机制和只负责描述行为的注解；三者不能互相冒充。

## 1. 已实际读取与验证的范围

- 公开索引固定为 Smashwinny/reminder_knowlege@1f61909da967cea8bc68dbfaffc642a4331b3352 的 reminder-dot/cloud-reference/knowledge-index.json。复用已取得的固定快照，复制前核对字节和 SHA-256；共检索394条题名、路径等元数据
- 正文只按索引中的真实路径和 URL 读取，固定在索引所指定的1043e9d6080bff7af9724162e2c44559fab63e40。本轮完整读取下列5篇并核对原始字节数与SHA-256。其余389条只检索元数据，不算全文已读
- 网站既有知识完整读取2篇、9个分块；协调者本轮实际取回2页，末页 nextCursor 为 null。本执行者按每篇的 chunkIndex 合并，检查连续性与总块数，再核对正文与提供的内容指纹
- Ponytail：5块，8797字节，SHA-256为2301ded97ac4d265103ce5c453ad58148453eac2bb292794c78da352ede73663
- HowToLiveBetter：4块，6202字节，SHA-256为12eb84e8e59202e18feb892416f4a345895b863ea5a9ce06c30d90ecbc86b3c9
- 合并正文不插入分隔符，也不增删换行；两篇均精确匹配。公开笔记保存时补丁工具加入的额外末尾LF已去除，再精确匹配索引。分发清单仅保留项目名、块数、字节、时间和内容哈希，不保留网站内部路由标识

这不是最新 Windows vault 全量扫描，也未读取私密、未提交笔记。已有笔记不代表用户已经掌握；本次只证明所列快照确实读取、复制准确，不能证明“全库从未出现此概念”。

## 2. 五篇既有概念：复用与新增边界

### MCP协议

旧笔记已有：MCP作为统一连接协议；Host、Client、Server角色；JSON-RPC消息；initialize、tools/list、tools/call 的工具调用链。旧笔记也已互链同义条目《MCP模型上下文协议》。

复用：不再另建“MCP是什么”。

本次补充：MCP工具的声明、工具实际注册、一次调用返回，以及数据库最终允许的行为是不同观察层。工具清单里写着 readOnlyHint，不会自动修改数据库权限。旧笔记中版本相关的 Python SDK 迁移断言未在本轮核实，不转述为当前事实。

来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/MCP%E5%8D%8F%E8%AE%AE.md

字节数1720；SHA-256：f241531981004f1580b331a37b9e38ca96875e368ac03d687aab199daac284d6。

### 只读闸门三原则

旧笔记已有：驱动层只读与SQL白名单、工具及表白名单、对成功和拒绝请求都留审计证据。其历史例子是另一个项目的 SQLite mode=ro；历史实验数字不计入此次 Toolbox 实验。

复用：沿用“只读、最小权限、可审计”的分层方法。不能把新项目又包装成首次发现“提示词不是安全边界”。

本次补充：逐个核对 Toolbox 的适配器，而非把一个数据库的机制推广到所有数据库。固定文档 read-only 支持矩阵只列 Cloud SQL PostgreSQL、AlloyDB PostgreSQL、Cloud SQL MySQL 和 BigQuery 四类，不能把 SQLite 加进矩阵。SQLite URI 的 mode=ro 是驱动路径，与 Toolbox 源配置层的 readOnly 开关、自动写工具抑制是不同机制。旧笔记“焊死、绕不过”的比喻不作为本轮证明：本轮若验证mode=ro，应限定为该连接对指定样例数据库的写入被拒，不能扩大到任意SQL、ATTACH目标、扩展加载或所有文件与数据库都不可变。只读保护也不自动限定能读哪些表、返回多少数据或是否泄露数据；仍需审计和最小权限。

来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%8F%AA%E8%AF%BB%E9%97%B8%E9%97%A8%E4%B8%89%E5%8E%9F%E5%88%99.md

字节数1994；SHA-256：23952485062d0da330ebe343b0216eb755f8340c1290526c26001d8af760817a。

### 本地MCP端点安全四道门

旧笔记已有：本地HTTP/MCP服务的入口限制，讨论令牌路径、Host、Origin与请求体大小；明确区分“谁能进来”和“进来后能做什么”。这是其来源项目的具体设计，不是所有MCP实现必须照抄的协议条款。

复用：保留网络入口控制与执行权限正交的认识。

本次补充：绑定127.0.0.1、使用stdio或限定工具组，都不能独自证明数据库只读。本轮若只测试stdio与合成数据库，就不能写成已经测试HTTP认证、DNS重绑定或生产网络防护。未认证的回环测试也不构成OAuth或用户身份授权验证。

来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%9C%AC%E5%9C%B0MCP%E7%AB%AF%E7%82%B9%E5%AE%89%E5%85%A8%E5%9B%9B%E9%81%93%E9%97%A8.md

字节数2558；SHA-256：1f7cfcb79846015e78c94fcb6391e09ffc9f4b1e236c29ac391dd20fda686cff。

### 代码管边界提示词管判断

旧笔记已有：数据访问、文件权限等不能靠模型自觉的限制，应落在模型不能说服或修改的强制执行层。

复用：readOnlyHint是描述，安全边界必须找执行器。

本次补充：安全字段的名字不是证据，要追到代码分支。固定源码 ShouldSuppress 先要求 source.IsReadOnly() 为真；明确 false 的 readOnlyHint 才触发这一通用抑制逻辑，未标注工具只警告而不抑制。不能把“自动剪枝写工具”缩写成“所有未证明只读的工具都会被删除”。SQLite源的 IsReadOnly() 返回false，不具备此源级联动。

来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E4%BB%A3%E7%A0%81%E7%AE%A1%E8%BE%B9%E7%95%8C%E6%8F%90%E7%A4%BA%E8%AF%8D%E7%AE%A1%E5%88%A4%E6%96%AD.md

字节数1427；SHA-256：82baf8f30c908b3ea424d15f82b6d3124e40b3c1b023961bfd0c8abd1eb8b86d。

### 关系型数据库与NoSQL

旧笔记已有：关系型、键值、文档等数据库类别与基本存储选型词汇。本轮只借用这个分类入口，不把旧文中的概括式一致性或扩展性比较当作所有产品的严格保证。

复用：不因 Toolbox 同时连接多类数据库而重建“数据库类型”笔记。

本次补充：同属SQL数据库，不代表只读配置、驱动参数或工具默认行为相同。Toolbox的来源适配器是行为单位，应按引擎、适配器、模式和固定版本记录验证，而非按“SQL/NoSQL”两大类直接推断安全性。

来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%85%B3%E7%B3%BB%E5%9E%8B%E6%95%B0%E6%8D%AE%E5%BA%93%E4%B8%8ENoSQL.md

字节数1085；SHA-256：a1521ce3393b63310f6e22c9f20bc3eca593928dcb342b56e40f2b31991ccce9。

## 3. 网站已有两篇：跨项目重复与此次新增

### Ponytail

已经有的：提示文本不能替代程序约束；证据按来源声明、静态源码、实际实验分开；在自写SQLite样例上做了参数化SQL与字符串拼接负对照。

此次增量：直接观察实际Toolbox进程的MCP调用与数据库驱动行为。参数化解决值如何进入SQL语句，只读机制解决写权限，两者不等价。不能拿Ponytail的旧SQLite样例证明Toolbox已经运行，更不能将旧42项检查计入此次结果。

### HowToLiveBetter

已经有的：来源可定位不等于断言已验证；缺数弃权；真实输入指纹和日志；区分来源可读层级和作者判断。

此次增量：安全文档也必须拆分为文档宣称、固定源码观察和本轮真实执行。读到四类云数据库矩阵，不等于已对四类云数据库逐一运行；一个SQLite写入被拒，也不等于所有引擎、所有文件或所有副作用都已阻断。

## 4. 建议合并而非重复新建的条目

### 工具注解与强制执行分离

一句话定义：readOnlyHint等注解用于描述工具行为；数据操作是否真正被阻断，取决于实际的权限、数据库连接或服务端执行机制。

领域：AI工具安全。优先补充《代码管边界提示词管判断》与《MCP协议》，互链《只读闸门三原则》。MCP官方2025-06-18规范明确注解不保证忠实描述行为，不能依赖不可信服务器的注解决定工具使用。Toolbox文档某些“可安全自动执行、零副作用”措辞不能脱离该信任条件。

来源：https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations

### 适配器级只读能力矩阵

一句话定义：只读能力必须按引擎、来源适配器、连接模式、工具类型和版本逐项验证，不能从统一字段名推断一致实现。

领域：数据库接入与安全验证。优先补充《只读闸门三原则》，关联《关系型数据库与NoSQL》。特别注意BigQuery protected模式允许会话临时数据集写入，同时仍被Toolbox层分类为只读并展示readOnlyHint；这与“绝无任何副作用”不同。

### 工具暴露范围与数据权限分层

一句话定义：工具组控制加载或暴露给某条调用路径的能力集合，数据库账号、数据过滤和执行约束控制实际能接触的数据与操作；选了较小工具组不能单独证明后者已限制。

领域：最小权限。优先补充《只读闸门三原则》。固定Toolsets文档还明确：未指定名称加载toolset时会加载服务器上的全部工具。因此课程应明确工具集合和端点范围，并实际检查能否绕到其他调用路径，不能只看选出的清单较短。

以上名称是本报告的归纳提案，不是已确认全库不存在的新概念。回迁前仍要在最新本机知识中做同义检索、合并、互链和索引更新。

## 5. 本次所用 Toolbox 静态证据

下列文件的相关证据段落均已实际读取；固定提交为a24e5e68567fa014a42fc6cc711faa82b964d4c0。来源文件使用googleapis/mcp-toolbox模块名；仓库入口保留googleapis/genai-toolbox的已知地址。

- 只读四类支持矩阵、各引擎机制与BigQuery模式：https://github.com/googleapis/genai-toolbox/blob/a24e5e68567fa014a42fc6cc711faa82b964d4c0/docs/en/documentation/configuration/security/read-only.md
- 工具注解与ShouldSuppress分支：https://github.com/googleapis/genai-toolbox/blob/a24e5e68567fa014a42fc6cc711faa82b964d4c0/internal/tools/tools.go
- SQLite源无readOnly字段且IsReadOnly返回false：https://github.com/googleapis/genai-toolbox/blob/a24e5e68567fa014a42fc6cc711faa82b964d4c0/internal/sources/sqlite/sqlite.go
- Toolsets逻辑分组与默认加载全部工具：https://github.com/googleapis/genai-toolbox/blob/a24e5e68567fa014a42fc6cc711faa82b964d4c0/docs/en/documentation/configuration/toolsets/_index.md
- BigQuery protected模式与工具适用限制：https://github.com/googleapis/genai-toolbox/blob/a24e5e68567fa014a42fc6cc711faa82b964d4c0/docs/en/integrations/bigquery/source.md

这里的静态观察不是云数据库实测。实验结论须由真实运行日志、输入输出及独立审核支持；本文件不宣称用户掌握、不宣称全库新知、不修改本机vault，不执行Git提交或推送，也不代用户标记学习完成。

逐文件可复核数据见read_manifest.json；离线校验命令为python verify_knowledge.py。该清单与分块合并副本不含网站内部任务或报告标识。
