# Codex 进阶独立审核与公开副本检查

历史实验与独立复跑日期：2026-10-05 UTC。公开副本审核日期：2026-10-06 UTC。

结论：通过本次限定范围的内容、证据、公开副本和知识合并检查。本次没有重跑实验，也没有新增在线集成或模型验收。以下历史命令与结果均明确属于原日期；文件整理和审核通过不代表读者已经掌握，也不证明原视频、真实账户或运行时行为。

## 1. 独立性与本次检查范围

本次审查者没有编写或改动作者的前五份公开交付物，也没有编写知识库的五份候选修改；只编写本审核日志。检查时按最终文件字节固定对象，独立核对历史执行记录、全部样例指纹、来源、许可、归档成员、文字和链接，并实际查看最终 PDF 的全部 12 页。

2026-10-05 的历史独立审核曾把原始 ZIP 放到独立目录，按指南执行六步。保存记录显示六步退出码均为 0、stderr 均为空，两份 Draft-07 schema 与四份来源文件核对通过。25 个样例全部匹配预期：8 个结构接受、14 个 schema 拒绝、3 个解析错误。本次读取并逐例对比原作者结果与历史独立结果，结果、错误、输入指纹、运行器指纹、样例清单及来源完全一致。没有把阅读旧记录写成新一次复跑。

历史复跑的外部时钟观察边界为 2026-10-05T10:38:32Z 至 2026-10-05T10:39:14Z。下面每步时间来自当时运行主机，不能当作分别读取外部时钟的结果。实际运行对象是 Python 3.12.14、jsonschema 4.26.0 与 referencing 0.37.0；安装清单 0.159.2 未执行，也未证明与固定源码等价。

## 2. 当前公开交付物指纹

以下五份是本次实际检查的公开副本。本审核日志是第六份，自己的最终指纹由配套发布清单记录，避免在正文内制造自指哈希。
- codex-advanced-guide.pdf：52095 字节；SHA-256 f7174f2a7f54de4ed61edd82db6fd9921bfe698888aa2a431dd9a2050ee932dd
- codex-advanced-guide.html：42693 字节；SHA-256 687f4c51243e387466ab90dd1b5670aa611d422ba857288b841788b2db47668f
- codex-advanced-exercise.zip：85148 字节；SHA-256 13fdf7c4425839ad0cc174c7a3ef6d21dee9ecc149b174eb883a02b9d801397c
- codex-advanced-experiment-log.md：20950 字节；SHA-256 2cf22557d26f23fb39717e62feb412a1143d87cba8c1e73964d3729b213fbf7c
- codex-advanced-knowledge-notes.md：18389 字节；SHA-256 bffd851cc4b8a04c1eae4b79b4bc30cf7ba3e5993641a0bc210277d74992f3eb

六份公开交付物按各自原始字节相加低于 1,000,000 字节；不是把二次压缩后的大小当作原文件总量。原始历史六份的合计为 231110 字节，公开整理前指纹如下，仅作历史来源对照，不冒充当前文件指纹。
- codex-advanced-guide.pdf：历史原始 52161 字节；SHA-256 1ebd56f57e6d65b303cbbe680c396ce9edae69e6254686b6c9b09b512f1225e5
- codex-advanced-guide.html：历史原始 42652 字节；SHA-256 30d8c7cd7fe0528a6828a853230bb578034bb8c19ec54492149d04503a04bdf8
- codex-advanced-exercise.zip：历史原始 83496 字节；SHA-256 254179e9cb6d911387f72c4def2a382ecf03ced7600f73f92f5404d50d8fc7b6
- codex-advanced-experiment-log.md：历史原始 19923 字节；SHA-256 1b0223153c6ca1bb63bdbcbd9a6c1b2ba9dc1dd2cb4b39d07177164f7fa4891f
- codex-advanced-knowledge-notes.md：历史原始 18869 字节；SHA-256 44d03a3f46664021f2351c0d56d9418f435002fe8cd116e4a0d7f818708453f2
- codex-advanced-review-log.md：历史原始 14009 字节；SHA-256 4f706849245e9eaf9de4226687ad1a25d3b31023338a22bbefc34a798b317a86

## 3. 2026-10-05 六步独立复跑原始记录

### 第 1 步

开始 2026-10-05T10:39:00.463230+00:00；结束 2026-10-05T10:39:00.583985+00:00；耗时 0.120739 秒；退出码 0

```bash
python3 -m zipfile -e codex-advanced-exercise.zip replay
cd replay
python3 -I -c "import sys;print(sys.version)"
python3 -I -c "import importlib.metadata as m;print(m.version('jsonschema'))"
```

标准输出：
```text
3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]
4.26.0
```

标准错误：
```text
(empty)
```

### 第 2 步

开始 2026-10-05T10:39:00.584142+00:00；结束 2026-10-05T10:39:00.825335+00:00；耗时 0.241185 秒；退出码 0

```bash
python3 -I validate_offline.py --verify-only
```

标准输出：
```text
{"actual_outcomes": {}, "cases_run": 0, "failed": 0, "passed": 0, "schemas_checked": 2, "source_files_verified": 4, "suite": "verify-only"}
```

标准错误：
```text
(empty)
```

### 第 3 步

开始 2026-10-05T10:39:00.825526+00:00；结束 2026-10-05T10:39:01.066167+00:00；耗时 0.240631 秒；退出码 0

```bash
python3 -I validate_offline.py --suite config --output evidence/recheck_config.json
```

标准输出：
```text
PASS config_valid_read_only: accept
PASS config_valid_provider_shape: accept
PASS config_valid_empty: accept
PASS config_invalid_model_type: reject
PASS config_invalid_auth_boolean: reject
PASS config_invalid_wire_api: reject
PASS config_unknown_top_level: reject
PASS config_unknown_provider_field: reject
PASS config_invalid_retry_count: reject
{"actual_outcomes": {"accept": 3, "reject": 6}, "cases_run": 9, "failed": 0, "passed": 9, "schemas_checked": 2, "source_files_verified": 4, "suite": "config"}
Saved: evidence/recheck_config.json
```

标准错误：
```text
(empty)
```

### 第 4 步

开始 2026-10-05T10:39:01.066318+00:00；结束 2026-10-05T10:39:01.391228+00:00；耗时 0.324904 秒；退出码 0

```bash
python3 -I validate_offline.py --suite protocol --output evidence/recheck_protocol.json
```

标准输出：
```text
PASS protocol_valid_initialize: accept
PASS protocol_valid_capabilities: accept
PASS protocol_unknown_fields_allowed: accept
PASS protocol_synthetic_model_accepted: accept
PASS protocol_valid_turn_shape: accept
PASS protocol_missing_id: reject
PASS protocol_invalid_id_type: reject
PASS protocol_missing_client_version: reject
PASS protocol_invalid_client_name: reject
PASS protocol_invalid_capability_type: reject
PASS protocol_unknown_method: reject
PASS protocol_turn_missing_thread: reject
PASS protocol_turn_invalid_text: reject
{"actual_outcomes": {"accept": 5, "reject": 8}, "cases_run": 13, "failed": 0, "passed": 13, "schemas_checked": 2, "source_files_verified": 4, "suite": "protocol"}
Saved: evidence/recheck_protocol.json
```

标准错误：
```text
(empty)
```

### 第 5 步

开始 2026-10-05T10:39:01.391373+00:00；结束 2026-10-05T10:39:01.678120+00:00；耗时 0.286740 秒；退出码 0

```bash
python3 -I validate_offline.py --suite malformed --output evidence/recheck_malformed.json
```

标准输出：
```text
PASS malformed_json_missing_brace: parse_error
PASS malformed_toml_unclosed_string: parse_error
PASS malformed_toml_duplicate_key: parse_error
{"actual_outcomes": {"parse_error": 3}, "cases_run": 3, "failed": 0, "passed": 3, "schemas_checked": 2, "source_files_verified": 4, "suite": "malformed"}
Saved: evidence/recheck_malformed.json
```

标准错误：
```text
(empty)
```

### 第 6 步

开始 2026-10-05T10:39:01.678375+00:00；结束 2026-10-05T10:39:02.046630+00:00；耗时 0.368245 秒；退出码 0

```bash
python3 -I validate_offline.py --suite all --output evidence/recheck_all.json
```

标准输出：
```text
PASS config_valid_read_only: accept
PASS config_valid_provider_shape: accept
PASS config_valid_empty: accept
PASS config_invalid_model_type: reject
PASS config_invalid_auth_boolean: reject
PASS config_invalid_wire_api: reject
PASS config_unknown_top_level: reject
PASS config_unknown_provider_field: reject
PASS config_invalid_retry_count: reject
PASS protocol_valid_initialize: accept
PASS protocol_valid_capabilities: accept
PASS protocol_unknown_fields_allowed: accept
PASS protocol_synthetic_model_accepted: accept
PASS protocol_valid_turn_shape: accept
PASS protocol_missing_id: reject
PASS protocol_invalid_id_type: reject
PASS protocol_missing_client_version: reject
PASS protocol_invalid_client_name: reject
PASS protocol_invalid_capability_type: reject
PASS protocol_unknown_method: reject
PASS protocol_turn_missing_thread: reject
PASS protocol_turn_invalid_text: reject
PASS malformed_json_missing_brace: parse_error
PASS malformed_toml_unclosed_string: parse_error
PASS malformed_toml_duplicate_key: parse_error
{"actual_outcomes": {"accept": 8, "parse_error": 3, "reject": 14}, "cases_run": 25, "failed": 0, "passed": 25, "schemas_checked": 2, "source_files_verified": 4, "suite": "all"}
Saved: evidence/recheck_all.json
```

标准错误：
```text
(empty)
```

## 4. 历史错误分层与测试含义

逐项核对所有 25 条结果。以下错误直接取自 2026-10-05 的独立复跑，不是推测的服务端回复：

- config_invalid_model_type → reject；type；42 is not of type 'string'
- config_invalid_auth_boolean → reject；type；'false' is not of type 'boolean'
- config_unknown_top_level → reject；additionalProperties；Additional properties are not allowed ('made_up_setting' was unexpected)
- protocol_missing_client_version → reject；required；'version' is a required property
- protocol_turn_missing_thread → reject；required；'threadId' is a required property
- malformed_json_missing_brace → parse_error；JSONDecodeError；Expecting value: line 2 column 1 (char 40)
- malformed_toml_unclosed_string → parse_error；TOMLDecodeError；Illegal character '\n' (at line 1, column 20)
- malformed_toml_duplicate_key → parse_error；TOMLDecodeError；Cannot overwrite a value (at line 2, column 17)

未知配置根键及 Provider 键被所测 schema 拒绝；所测请求 envelope/ClientInfo 的额外字段被接受。合成的不存在模型名和 threadId 也被接受。这些正例只证明字段结构合规，没有证明资源存在、协议时序、配置层已采用、账户授权或模型调用成功。

运行器使用真正的 jsonschema Draft7Validator；读取的是两份未经改写的公开官方 schema。外部 schema 引用检索被显式阻止，路径被限制在实验目录，输出限定到 evidence。执行代码没有调用 Codex CLI、启动 App Server、传输协议、读取账户/凭证/真实配置或发起模型请求。审核未做操作系统级网络抓包，不能把源码约束说成完整网络审计。

## 5. 固定来源、许可与公开 ZIP

固定源码为 openai/codex@823ea830c0fd418b09ff02d36cad9a1fff66465b。本次审查者通过公开 GitHub 只读接口，独立重新取得该提交下的两份 schema、LICENSE 和 NOTICE，逐字节对比历史原文件与公开 ZIP 内文件。四份原文、字节数、SHA-256 与 Git blob SHA-1 全部一致；两份 schema 均声明 Draft-07。

- [schemas/upstream/ConfigToml.json](https://github.com/openai/codex/blob/823ea830c0fd418b09ff02d36cad9a1fff66465b/codex-rs/core/config.schema.json)：235174 字节；SHA-256 8cc41c549fda67a807ab44e7447a3c851d4d86f3cfd45ba30cc4fb426f596db8；Git blob SHA-1 b832da2f807b1ad588207d1ece4c88e8b9b641a1
- [schemas/upstream/ClientRequest.json](https://github.com/openai/codex/blob/823ea830c0fd418b09ff02d36cad9a1fff66465b/codex-rs/app-server-protocol/schema/json/ClientRequest.json)：210425 字节；SHA-256 8af27fa887f2fed9c7b52f5f06476e969fa48d92aa3fd038e4db048ea87f7fef；Git blob SHA-1 02dde191f7b85079ff39913b8f8e517097fff928
- [schemas/upstream/LICENSE](https://github.com/openai/codex/blob/823ea830c0fd418b09ff02d36cad9a1fff66465b/LICENSE)：10926 字节；SHA-256 d17f227e4df5da1600391338865ce0f3055211760a36688f816941d58232d8dc；Git blob SHA-1 4606e72e042564097e8780d66c1d4dcb611869bd
- [schemas/upstream/NOTICE](https://github.com/openai/codex/blob/823ea830c0fd418b09ff02d36cad9a1fff66465b/NOTICE)：242 字节；SHA-256 9d71575ecfd9a843fc1677b0efb08053c6ba9fd686a0de1a6f5382fd3c220915；Git blob SHA-1 2805899d56d0332d175cfc613c67d45d6f006db7

Apache-2.0 LICENSE 与上游 NOTICE 原样保留。来源许可和文件指纹不证明模型服务权益、软件质量或在线行为。

公开 ZIP 有 35 个唯一成员，无绝对路径、父目录逃逸或符号链接；CRC 检查无错误。SHA256SUMS 覆盖其余 34 个文件，逐项重算全部匹配。与历史 ZIP 对比，仅三处改变：README 增加公开整理说明；历史 original_results.json 的命令首项由环境专属解释器绝对路径规范为 python3；SHA256SUMS 相应更新。JSON 的其他命令参数、历史时间、依赖版本、汇总、全部 25 条结果与错误完全保留。25 个样例、清单、验证器和四份上游原文没有改变。

六步命令在 PDF、HTML 与实验日志中一致。实验日志所有代码块和历史命令、stdout、stderr、退出码、时间及耗时保持不变；原 ZIP 哈希明确标成历史原始值，另列当前公开 ZIP 哈希。范围内没有安装依赖、执行 Codex CLI/App Server、启动模型或发出协议请求。

## 6. 最终 PDF 逐页与 HTML 结构检查

本次最终 PDF 由 ReportLab 直接生成，为 12 页 A4。审查者独立用 pdftoppm 将该精确文件渲染为 110 DPI PNG，逐页实际查看第 1 至 12 页，而非只检查页数或抽取文本。

- 第 1 页：范围、历史日期、未复跑声明和十二问目录清楚
- 第 2 至 7 页：十二个问题、图示、解释与依据可读，没有裁切、重叠或缺字
- 第 8 页：五项能力与五个用途完整，未把学习等同于在线操作许可
- 第 9 至 10 页：六步命令、历史观察与时间可读，命令没有越界
- 第 11 页：8/14/3 结果和历史公开知识读取边界相符
- 第 12 页：固定来源、动态文档日期、未测项和排版限制清楚，长链接没有越界

PDF 没有附件、表单或 JavaScript；文本与元数据没有发现环境专属路径或非公开标识。Poppler 报出 fontconfig 缓存不可写警告，但渲染成功，全部页图中的文字与图形正常；未改系统设置来消除警告。

HTML 仅作静态结构检查：12 个问题卡片、12 个可解析内联 SVG、6 步命令、12 个有效目录锚点，无重复 id、脚本、表单或外部资源加载。中文 lang、UTF-8、viewport 与 SVG 标题保留。HTML 浏览器视觉与 HTML 转 PDF 的原路线受环境限制，本次未重试；PDF 的直接生成和逐页检查不替代这两项验收。

## 7. 知识合并与历史保留

本次候选知识合并基于公开仓库 main 的 ad4242e88337434fe8a784fd51717ca4a4fd753c，树为 4762a1e881bf9a729837c9abe3b4fba758dbed8b。准备期间 main 曾前进；审查者独立核对两提交差异，只新增五个无关工具文件。候选重新以新树为基线，未改这些工具文件。25 份已读正文在新基线重新取得，字节保持一致，全部与基线 blob、SHA-256 和长度记录相符。

本次阅读范围为 MOC、学习方法、仓库说明、两份模板、12 篇概念和 8 篇项目，共 25 份正文。基线有 306 篇概念和 107 篇项目；其余 294 篇概念、99 篇项目只筛查路径或标题，未宣称全库全文查重。原学习阶段的 394 条公开元数据、24 篇实际公开正文、370 篇未读正文另行保留，不能混作本次较新快照计数。

合并恰有五份知识文件：新增项目 codex_advanced；向 Agent输出协议契约、单一馈送与schema冻结、接缝与桩实现StubSeam 三篇已有概念追加 Codex 案例；在 MOC 增加领域入口与项目索引行。没有新建同义概念。

独立逐字节复核表明：三篇概念的完整旧正文仍是新文件前缀；MOC 恰有两块插入，没有删除或替换。去掉这些插入可精确恢复旧字节、长度和 SHA-256，原历史标签、累计计数和已有项目索引都未改写。全部既有项目文件在修改白名单之外。新加的双链按基线文件路径唯一解析，配套材料相对链接指向本组实际文件。固定上游外链对应本次实际取得的四份公开原文。

## 8. 公开内容边界与结论

检查覆盖六份公开交付的文本、PDF 提取文本和元数据、全部 ZIP 文本，以及知识文件的新增内容。未发现非公开账号或对象标识、环境专属路径、原视频帖子、私人笔记原文、凭证或个人配置。原本已公开的历史知识正文按原字节保留；新增内容没有引入这类信息。上游 schema 的通用 Reminder 类型名属于已核对原文，不是个人记录。

教材、历史日志与知识案例都保留以下边界：25/25 是预期与观察一致，不是 25 次模型调用成功；合成模型名和线程标识可以通过结构检查，不证明它们存在；配置与请求的未知字段政策只适用于所测对象。身份、授权、资格、费用、配置实际采用、协议生命周期和完成结果，需要各自的运行证据。

原视频仍未观看、未核验；没有 CLI/App Server 运行、真实模型或计费验收。本次只确认上述精确公开候选的内容、完整性、视觉、结构和合并边界；Git 发布是否成功须以随后的实际发布回读另行确认，不能从本日志推断。
