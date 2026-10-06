# Codex 进阶离线契约历史实验日志

公开副本说明：本次整理未重跑实验。以下六步完整命令、stdout、stderr、退出码、时间与耗时均来自 2026-10-05 的历史实测；25 项样例结果与错误路径保持不变。

日期：2026-10-05 UTC。主实验从独立 ZIP 新解包开始。以下命令、stdout、stderr、退出码和单调计时器耗时由程序直接记录。时间为运行主机 UTC；本轮已与外部时钟核对。

## 实验边界

只校验固定公开 schema 与无敏感信息的合成输入。没有 Codex CLI/App Server 进程、协议发包、账户/凭证/真实配置读取、模型列表或推理、计费验证。原视频未观看、未核验。运行器只允许本地 schema 引用；没有做操作系统级网络审计。

## 来源与环境

源码提交：823ea830c0fd418b09ff02d36cad9a1fff66465b
运行环境：{"python": "3.12.14", "jsonschema": "4.26.0", "referencing": "0.37.0"}
历史原始练习 ZIP SHA-256（公开整理前）：254179e9cb6d911387f72c4def2a382ecf03ced7600f73f92f5404d50d8fc7b6
上游 LICENSE 与 NOTICE 原样保留，许可为 Apache 2.0。安装清单 0.159.2 只读过，不是本次被执行的运行时。

## 第 1 步 解包并核对环境

目的：从独立 ZIP 开始，确认不是依赖原工作目录
开始：2026-10-05T10:36:45.649934+00:00；结束：2026-10-05T10:36:45.792137+00:00；耗时：0.1422 秒；退出码：0

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

观察：Python 3.12.14；jsonschema 4.26.0；ZIP 独立解包成功
验证：两个版本命令正常打印，进入 replay 后再做下面步骤

## 第 2 步 核对上游文件与 schema

目的：验证来源指纹，确认两份 Draft-07 契约可加载
开始：2026-10-05T10:36:45.792185+00:00；结束：2026-10-05T10:36:46.072958+00:00；耗时：0.2808 秒；退出码：0

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

观察：4 份上游文件指纹匹配；2 份 schema 检查通过
验证：输出 source_files_verified=4、schemas_checked=2、failed=0

## 第 3 步 让配置正例和反例一起跑

目的：比较类型、枚举、未知字段的不同结果
开始：2026-10-05T10:36:46.072996+00:00；结束：2026-10-05T10:36:46.351888+00:00；耗时：0.2789 秒；退出码：0

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

观察：9/9 符合预期：3 接受、6 结构拒绝
验证：查看 recheck_config.json：model=42 的错误为 not of type string

## 第 4 步 观察协议形状与语义陷阱

目的：区分请求形状和真实握手、资源与模型资格
开始：2026-10-05T10:36:46.351926+00:00；结束：2026-10-05T10:36:46.682010+00:00；耗时：0.3301 秒；退出码：0

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

观察：13/13 符合预期：5 接受、8 结构拒绝
验证：不存在的模型名和 threadId 仍可合规；不代表服务成功

## 第 5 步 把解析错误单独识别出来

目的：确认坏 JSON/TOML 在结构校验之前就会失败
开始：2026-10-05T10:36:46.682047+00:00；结束：2026-10-05T10:36:46.894597+00:00；耗时：0.2125 秒；退出码：0

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

观察：3/3 符合预期，均由解析器报错
验证：查看 recheck_malformed.json：JSONDecodeError 或 TOMLDecodeError

## 第 6 步 全量回归并保存证据

目的：核对总数，生成可供另一人检查的完整结果
开始：2026-10-05T10:36:46.894640+00:00；结束：2026-10-05T10:36:47.173658+00:00；耗时：0.279 秒；退出码：0

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

观察：25/25 符合预期：8 接受、14 结构拒绝、3 解析错误
验证：recheck_all.json 中 passed=25、failed=0；保留完整错误路径

## 样例级真实错误与结果

PASS 只表示实际结果符合预期。所有 reject/parse_error 样例都是刻意构造的反例，不是被掩盖的运行失败。

### config_valid_read_only
输入：fixtures/config/config_valid_read_only.toml
预期：accept；观察：accept；符合预期：True
输入 SHA-256：a7339608e9170068c335888695a88083a24021274ff84299fa2078b495a9d335
无校验错误；不是服务端接受或执行凭证。

### config_valid_provider_shape
输入：fixtures/config/config_valid_provider_shape.toml
预期：accept；观察：accept；符合预期：True
输入 SHA-256：95b356c40fb8e703a87a211e12c216879bfab7a7af7cf40700363e2984edc811
无校验错误；不是服务端接受或执行凭证。

### config_valid_empty
输入：fixtures/config/config_valid_empty.json
预期：accept；观察：accept；符合预期：True
输入 SHA-256：ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356
无校验错误；不是服务端接受或执行凭证。

### config_invalid_model_type
输入：fixtures/config/config_invalid_model_type.toml
预期：reject；观察：reject；符合预期：True
输入 SHA-256：dd21aa9e304593bb29400dccbe968a3b4b767bfae9420a88d352232b82d5ace0
```json
[
  {
    "message": "42 is not of type 'string'",
    "validator": "type",
    "instance_path": [
      "model"
    ],
    "schema_path": [
      "properties",
      "model",
      "type"
    ]
  }
]
```

### config_invalid_auth_boolean
输入：fixtures/config/config_invalid_auth_boolean.toml
预期：reject；观察：reject；符合预期：True
输入 SHA-256：27b64a03a432dfe397723c2e067cdf9269ba84bef001857c4cec03da7d564c96
```json
[
  {
    "message": "'false' is not of type 'boolean'",
    "validator": "type",
    "instance_path": [
      "model_providers",
      "fixture_provider",
      "requires_openai_auth"
    ],
    "schema_path": [
      "properties",
      "model_providers",
      "additionalProperties",
      "properties",
      "requires_openai_auth",
      "type"
    ]
  }
]
```

### config_invalid_wire_api
输入：fixtures/config/config_invalid_wire_api.toml
预期：reject；观察：reject；符合预期：True
输入 SHA-256：d589770e8db9d64000f9c73402b4eca534a59ad8ed8b8d4b63c627a8dfdb8f3b
```json
[
  {
    "message": "'made_up_wire_api' is not valid under any of the given schemas",
    "validator": "oneOf",
    "instance_path": [
      "model_providers",
      "fixture_provider",
      "wire_api"
    ],
    "schema_path": [
      "properties",
      "model_providers",
      "additionalProperties",
      "properties",
      "wire_api",
      "allOf",
      0,
      "oneOf"
    ]
  }
]
```

### config_unknown_top_level
输入：fixtures/config/config_unknown_top_level.toml
预期：reject；观察：reject；符合预期：True
输入 SHA-256：4cede7bee1761dba5295eb0f244749029dc114d5e8fce3e6441310780533d087
```json
[
  {
    "message": "Additional properties are not allowed ('made_up_setting' was unexpected)",
    "validator": "additionalProperties",
    "instance_path": [],
    "schema_path": [
      "additionalProperties"
    ]
  }
]
```

### config_unknown_provider_field
输入：fixtures/config/config_unknown_provider_field.toml
预期：reject；观察：reject；符合预期：True
输入 SHA-256：8701932638707f7fe96ba03886dec8ba216ece69b748f114b238a2c0dfae00a7
```json
[
  {
    "message": "Additional properties are not allowed ('made_up_provider_field' was unexpected)",
    "validator": "additionalProperties",
    "instance_path": [
      "model_providers",
      "fixture_provider"
    ],
    "schema_path": [
      "properties",
      "model_providers",
      "additionalProperties",
      "additionalProperties"
    ]
  }
]
```

### config_invalid_retry_count
输入：fixtures/config/config_invalid_retry_count.toml
预期：reject；观察：reject；符合预期：True
输入 SHA-256：88f09037fdcb5e741f5d06b93a2a6ff5b97751eafc9b50d539b259c69caecfee
```json
[
  {
    "message": "-1 is less than the minimum of 0.0",
    "validator": "minimum",
    "instance_path": [
      "model_providers",
      "fixture_provider",
      "request_max_retries"
    ],
    "schema_path": [
      "properties",
      "model_providers",
      "additionalProperties",
      "properties",
      "request_max_retries",
      "minimum"
    ]
  }
]
```

### protocol_valid_initialize
输入：fixtures/protocol/protocol_valid_initialize.json
预期：accept；观察：accept；符合预期：True
输入 SHA-256：679bf0be73e251c6ec5083de32b5cfd2252648832e7815d2a0ebccee43d249dc
无校验错误；不是服务端接受或执行凭证。

### protocol_valid_capabilities
输入：fixtures/protocol/protocol_valid_capabilities.json
预期：accept；观察：accept；符合预期：True
输入 SHA-256：d3c66176f1028141c7ed469032630dd5ffe58ab9fa0bddc5553ef9a4c6a73d85
无校验错误；不是服务端接受或执行凭证。

### protocol_unknown_fields_allowed
输入：fixtures/protocol/protocol_unknown_fields_allowed.json
预期：accept；观察：accept；符合预期：True
输入 SHA-256：32fea710af2b7c8698766c6d73bf0bdd02220edd5078d16aa976bea26df97f58
无校验错误；不是服务端接受或执行凭证。

### protocol_synthetic_model_accepted
输入：fixtures/protocol/protocol_synthetic_model_accepted.json
预期：accept；观察：accept；符合预期：True
输入 SHA-256：68c8d01051f7eb4f2ca5dca79117eda896829e29a1ff78e2c6c94d5521f69d92
无校验错误；不是服务端接受或执行凭证。

### protocol_valid_turn_shape
输入：fixtures/protocol/protocol_valid_turn_shape.json
预期：accept；观察：accept；符合预期：True
输入 SHA-256：f72cbf35f51838048669eb40bf6ef54765451f4f7846b17bc6e124abaff41a39
无校验错误；不是服务端接受或执行凭证。

### protocol_missing_id
输入：fixtures/protocol/protocol_missing_id.json
预期：reject；观察：reject；符合预期：True
输入 SHA-256：6e9cdc65ca1c3738abaed5bfa4eb50b1ef79f27de5983801dcce58f86328c549
```json
[
  {
    "message": "'id' is a required property",
    "validator": "required",
    "instance_path": [],
    "schema_path": [
      "oneOf",
      0,
      "required"
    ]
  }
]
```

### protocol_invalid_id_type
输入：fixtures/protocol/protocol_invalid_id_type.json
预期：reject；观察：reject；符合预期：True
输入 SHA-256：cb97c8e4fa31d956a3663d93a2c0d31e87e0f88100c93455b405f36dfbb799b7
```json
[
  {
    "message": "[] is not valid under any of the given schemas",
    "validator": "anyOf",
    "instance_path": [
      "id"
    ],
    "schema_path": [
      "oneOf",
      0,
      "properties",
      "id",
      "anyOf"
    ]
  }
]
```

### protocol_missing_client_version
输入：fixtures/protocol/protocol_missing_client_version.json
预期：reject；观察：reject；符合预期：True
输入 SHA-256：46fec799b9ef2cf2ad0e985e30e49aae6c3bd2ae2819fed02f3a76c6113026bb
```json
[
  {
    "message": "'version' is a required property",
    "validator": "required",
    "instance_path": [
      "params",
      "clientInfo"
    ],
    "schema_path": [
      "oneOf",
      0,
      "properties",
      "params",
      "properties",
      "clientInfo",
      "required"
    ]
  }
]
```

### protocol_invalid_client_name
输入：fixtures/protocol/protocol_invalid_client_name.json
预期：reject；观察：reject；符合预期：True
输入 SHA-256：2c4ef3d3cc1a31597635ce326632ebf6f9c683df09d1b2c37567eace5671a306
```json
[
  {
    "message": "42 is not of type 'string'",
    "validator": "type",
    "instance_path": [
      "params",
      "clientInfo",
      "name"
    ],
    "schema_path": [
      "oneOf",
      0,
      "properties",
      "params",
      "properties",
      "clientInfo",
      "properties",
      "name",
      "type"
    ]
  }
]
```

### protocol_invalid_capability_type
输入：fixtures/protocol/protocol_invalid_capability_type.json
预期：reject；观察：reject；符合预期：True
输入 SHA-256：5d23195e5313717a067c54477d7f29ac222eec431ada5c3fc14f581d1f888bbe
```json
[
  {
    "message": "{'experimentalApi': 'false'} is not valid under any of the given schemas",
    "validator": "anyOf",
    "instance_path": [
      "params",
      "capabilities"
    ],
    "schema_path": [
      "oneOf",
      0,
      "properties",
      "params",
      "properties",
      "capabilities",
      "anyOf"
    ]
  }
]
```

### protocol_unknown_method
输入：fixtures/protocol/protocol_unknown_method.json
预期：reject；观察：reject；符合预期：True
输入 SHA-256：30ee79e1286b8973ec47fdec84eba2945d7c18f686e34ab431e1ad23481f780f
```json
[
  {
    "message": "{'id': 1, 'method': 'made/up/method', 'params': {'clientInfo': {'name': 'offline_fixture', 'version': '1.0.0'}}} is not valid under any of the given schemas",
    "validator": "oneOf",
    "instance_path": [],
    "schema_path": [
      "oneOf"
    ]
  }
]
```

### protocol_turn_missing_thread
输入：fixtures/protocol/protocol_turn_missing_thread.json
预期：reject；观察：reject；符合预期：True
输入 SHA-256：a269fe9db7a5dcbd7fd0a3bcb7dcce71f5aedaae540641aec4ef0cc84bb37ab0
```json
[
  {
    "message": "'threadId' is a required property",
    "validator": "required",
    "instance_path": [
      "params"
    ],
    "schema_path": [
      "oneOf",
      63,
      "properties",
      "params",
      "required"
    ]
  }
]
```

### protocol_turn_invalid_text
输入：fixtures/protocol/protocol_turn_invalid_text.json
预期：reject；观察：reject；符合预期：True
输入 SHA-256：d979168acf8a56e2ee5f0ee88105d672d1358c18a9be0be716ac150bb148d3e9
```json
[
  {
    "message": "{'type': 'text', 'text': 42} is not valid under any of the given schemas",
    "validator": "oneOf",
    "instance_path": [
      "params",
      "input",
      0
    ],
    "schema_path": [
      "oneOf",
      63,
      "properties",
      "params",
      "properties",
      "input",
      "items",
      "oneOf"
    ]
  }
]
```

### malformed_json_missing_brace
输入：fixtures/malformed/malformed_json_missing_brace.json
预期：parse_error；观察：parse_error；符合预期：True
输入 SHA-256：bbfea7f65cad18730110001ff56e2e01a1337bdf2f3da2f563a0b40097398e30
```json
[
  {
    "type": "JSONDecodeError",
    "message": "Expecting value: line 2 column 1 (char 40)"
  }
]
```

### malformed_toml_unclosed_string
输入：fixtures/malformed/malformed_toml_unclosed_string.toml
预期：parse_error；观察：parse_error；符合预期：True
输入 SHA-256：eb3f4d1ace3578deda7be74872d260cbe1fb99451486e40c28fffaa4cdf653c8
```json
[
  {
    "type": "TOMLDecodeError",
    "message": "Illegal character '\\n' (at line 1, column 20)"
  }
]
```

### malformed_toml_duplicate_key
输入：fixtures/malformed/malformed_toml_duplicate_key.toml
预期：parse_error；观察：parse_error；符合预期：True
输入 SHA-256：03132a7d96a4f5ce3f589f1c1d1d66562f1275d418f07fb355f763a6a78a37d0
```json
[
  {
    "type": "TOMLDecodeError",
    "message": "Cannot overwrite a value (at line 2, column 17)"
  }
]
```

## 全量摘要
```json
{
  "suite": "all",
  "source_files_verified": 4,
  "schemas_checked": 2,
  "cases_run": 25,
  "passed": 25,
  "failed": 0,
  "actual_outcomes": {
    "accept": 8,
    "reject": 14,
    "parse_error": 3
  }
}
```

## 可追溯上游原文

- schemas/upstream/ConfigToml.json: https://github.com/openai/codex/blob/823ea830c0fd418b09ff02d36cad9a1fff66465b/codex-rs/core/config.schema.json
  SHA-256 8cc41c549fda67a807ab44e7447a3c851d4d86f3cfd45ba30cc4fb426f596db8；Git blob SHA-1 b832da2f807b1ad588207d1ece4c88e8b9b641a1
- schemas/upstream/ClientRequest.json: https://github.com/openai/codex/blob/823ea830c0fd418b09ff02d36cad9a1fff66465b/codex-rs/app-server-protocol/schema/json/ClientRequest.json
  SHA-256 8af27fa887f2fed9c7b52f5f06476e969fa48d92aa3fd038e4db048ea87f7fef；Git blob SHA-1 02dde191f7b85079ff39913b8f8e517097fff928
- schemas/upstream/LICENSE: https://github.com/openai/codex/blob/823ea830c0fd418b09ff02d36cad9a1fff66465b/LICENSE
  SHA-256 d17f227e4df5da1600391338865ce0f3055211760a36688f816941d58232d8dc；Git blob SHA-1 4606e72e042564097e8780d66c1d4dcb611869bd
- schemas/upstream/NOTICE: https://github.com/openai/codex/blob/823ea830c0fd418b09ff02d36cad9a1fff66465b/NOTICE
  SHA-256 9d71575ecfd9a843fc1677b0efb08053c6ba9fd686a0de1a6f5382fd3c220915；Git blob SHA-1 2805899d56d0332d175cfc613c67d45d6f006db7

## 历史成果验收范围

HTML 只做结构检查，没有浏览器视觉验收。PDF 使用 ReportLab 直接生成并渲染；逐页检查及独立复验另有记录。


## 当前公开副本说明

本次只整理公开副本，没有重新执行离线实验，也没有新增 CLI、App Server、认证、模型或计费验收。PDF 由 ReportLab 直接重新生成并逐页渲染检查；HTML 仅结构检查。HTML 浏览器视觉与 HTML 转 PDF 原路线受环境限制，本次未重试。当前独立审核另见审查日志。

ZIP 的 25 个样例、运行器、两份 schema、LICENSE 与 NOTICE 均保留原字节；README 新增公开说明，历史 JSON 的解释器绝对路径规范为 python3，SHA256SUMS 随之重算。JSON 的时间、版本、其余命令参数、逐项结果、错误和汇总没有改变。

当前公开 ZIP：85148 字节；SHA-256 13fdf7c4425839ad0cc174c7a3ef6d21dee9ecc149b174eb883a02b9d801397c
