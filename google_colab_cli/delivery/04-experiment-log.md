# Google Colab CLI 真实实验记录

实验日期：2026-10-05 UTC。以下为既有实验记录的公开副本；发布准备没有重新运行实验。独立审核另见第六份审核日志。

## 结论与范围

真实上游HistoryLogger/converter的本地历史导出实验：33/33测试用例通过，四种格式实际生成；最终ZIP新解压后创建全新venv并按全部五条展示命令成功复跑。

本地日志/产物流水线。11条事件完全虚构；代码字段未执行。未运行完整CLI、Google认证、远端Colab、GPU/TPU、CCU、H3或其他工作负载。

准备阶段联网下载官方 PyPI 依赖；第4步主实验进程离线。合成事件中的代码、会话、文件和输出不是远程实测数据。

固定上游提交：a84e094c67544e70d88649ba2d2a1d48511b3af7
来源：https://github.com/googlecolab/google-colab-cli/tree/a84e094c67544e70d88649ba2d2a1d48511b3af7

## 运行环境与输入

本次实跑：Linux，Python 3.12.14，nbformat 5.10.4；完整依赖版本在 requirements-tested-linux.txt。Windows 未实跑；官方完整 CLI 仅声明支持 Linux/macOS。

先解压 03-exercise.zip，进入 google_colab_cli_offline_experiment 目录；以下全部命令都在该目录运行。需要 Python 3.12 或更高版本。第 2 步从官方 PyPI 联网安装，之后运行的主实验离线。长命令末尾的反斜杠表示续行。

仅写入解压目录的 .venv、runtime、outputs。主脚本会设置本地 HOME/缓存/临时目录并阻断测试进程联网；这不是 OS 级沙箱。重跑会覆盖本练习生成的输出，保留旧结果时请先复制整个目录。

未更改上游源码；14份来源文件的 SHA-256 与固定清单相等。保留 Google LLC 版权标头与 Apache-2.0 全文。完整 CLI 没有安装、执行；只有相关文件供静态检查。

实测依赖版本：

```text
attrs==26.1.0
fastjsonschema==2.22.2
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
jupyter_core==5.9.1
nbformat==5.10.4
platformdirs==4.12.3
referencing==0.37.0
rpds-py==2026.9.1
traitlets==5.16.1
typing_extensions==4.16.0
```

## 五步实际命令与原始结果

工作目录：03-exercise.zip 解压后的 google_colab_cli_offline_experiment 根目录。下列命令无额外 HOME/PYTHONPATH 要求；run_experiment.py 在导入上游模块前配置自己的项目内路径。

第2步展示使用一条 shell 命令的反斜杠续行；参数与实跑单行命令一致。各步骤的原始 UTC 起止时间保留到微秒。复跑随机 notebook cell id 会变化，比较语义和来源指纹。

### 第1步 创建隔离环境

目的：在新解压目录创建项目专用虚拟环境

```sh
python3 -m venv .venv
```

开始 UTC：2026-10-05T05:33:41.644629+00:00
结束 UTC：2026-10-05T05:33:43.543256+00:00
退出码：0

实现结果：本地.venv创建成功
验收依据：退出码0；虚拟环境路径位于新解压目录

原始标准输出与标准错误：

```text
（此步骤无标准输出或标准错误；退出码0）
```

### 第2步 安装已验证依赖

目的：从官方PyPI安装本次Linux依赖版本；此准备步骤需要联网

```sh
.venv/bin/python -m pip --isolated install --no-cache-dir \
  --index-url https://pypi.org/simple \
  -r requirements-tested-linux.txt
```

开始 UTC：2026-10-05T05:33:43.543679+00:00
结束 UTC：2026-10-05T05:34:04.212501+00:00
退出码：0

实现结果：nbformat5.10.4和锁定版本依赖安装成功
验收依据：退出码0；完整安装输出已保留；无全局安装

原始标准输出与标准错误：

```text
Collecting attrs==26.1.0 (from -r requirements-tested-linux.txt (line 1))
  Downloading attrs-26.1.0-py3-none-any.whl.metadata (8.8 kB)
Collecting fastjsonschema==2.22.2 (from -r requirements-tested-linux.txt (line 2))
  Downloading fastjsonschema-2.22.2-py3-none-any.whl.metadata (2.1 kB)
Collecting jsonschema==4.26.0 (from -r requirements-tested-linux.txt (line 3))
  Downloading jsonschema-4.26.0-py3-none-any.whl.metadata (7.6 kB)
Collecting jsonschema-specifications==2025.9.1 (from -r requirements-tested-linux.txt (line 4))
  Downloading jsonschema_specifications-2025.9.1-py3-none-any.whl.metadata (2.9 kB)
Collecting jupyter_core==5.9.1 (from -r requirements-tested-linux.txt (line 5))
  Downloading jupyter_core-5.9.1-py3-none-any.whl.metadata (1.5 kB)
Collecting nbformat==5.10.4 (from -r requirements-tested-linux.txt (line 6))
  Downloading nbformat-5.10.4-py3-none-any.whl.metadata (3.6 kB)
Collecting platformdirs==4.12.3 (from -r requirements-tested-linux.txt (line 7))
  Downloading platformdirs-4.12.3-py3-none-any.whl.metadata (5.5 kB)
Collecting referencing==0.37.0 (from -r requirements-tested-linux.txt (line 8))
  Downloading referencing-0.37.0-py3-none-any.whl.metadata (2.8 kB)
Collecting rpds-py==2026.9.1 (from -r requirements-tested-linux.txt (line 9))
  Downloading rpds_py-2026.9.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.1 kB)
Collecting traitlets==5.16.1 (from -r requirements-tested-linux.txt (line 10))
  Downloading traitlets-5.16.1-py3-none-any.whl.metadata (10 kB)
Collecting typing_extensions==4.16.0 (from -r requirements-tested-linux.txt (line 11))
  Downloading typing_extensions-4.16.0-py3-none-any.whl.metadata (3.3 kB)
Downloading attrs-26.1.0-py3-none-any.whl (67 kB)
Downloading fastjsonschema-2.22.2-py3-none-any.whl (27 kB)
Downloading jsonschema-4.26.0-py3-none-any.whl (90 kB)
Downloading jsonschema_specifications-2025.9.1-py3-none-any.whl (18 kB)
Downloading jupyter_core-5.9.1-py3-none-any.whl (29 kB)
Downloading nbformat-5.10.4-py3-none-any.whl (78 kB)
Downloading platformdirs-4.12.3-py3-none-any.whl (32 kB)
Downloading referencing-0.37.0-py3-none-any.whl (26 kB)
Downloading rpds_py-2026.9.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (371 kB)
Downloading traitlets-5.16.1-py3-none-any.whl (86 kB)
Downloading typing_extensions-4.16.0-py3-none-any.whl (45 kB)
Installing collected packages: typing_extensions, traitlets, rpds-py, platformdirs, fastjsonschema, attrs, referencing, jupyter_core, jsonschema-specifications, jsonschema, nbformat
Successfully installed attrs-26.1.0 fastjsonschema-2.22.2 jsonschema-4.26.0 jsonschema-specifications-2025.9.1 jupyter_core-5.9.1 nbformat-5.10.4 platformdirs-4.12.3 referencing-0.37.0 rpds-py-2026.9.1 traitlets-5.16.1 typing_extensions-4.16.0

[notice] A new release of pip is available: 25.0.1 -> 26.2.1
[notice] To update, run: python -m pip install --upgrade pip
```

### 第3步 核验上游源码

目的：确认运行的是固定版本的真实上游模块

```sh
.venv/bin/python verify_sources.py
```

开始 UTC：2026-10-05T05:34:04.213101+00:00
结束 UTC：2026-10-05T05:34:04.241203+00:00
退出码：0

实现结果：14个上游文件SHA-256一致
验收依据：source_manifest.json与原始核验日志

原始标准输出与标准错误：

```text
OK vendor/colab_cli/history.py d1f1ef8a90195dd75dcc1cfb2c1a8a60326afa00b93370f6f1aab041e1ebadb4
OK vendor/colab_cli/converter.py 211143cbba34e770ef126c9106d08832b8221ff3a5e768fcfa851ddb0d4adcb2
OK upstream_tests/test_history.py c8b6bff6cb90998e04d92cb4f2bd18d259f9425208aa610b5bb056fc4ac1ecd9
OK LICENSE.upstream cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30
OK source_reference/README.md be2d812def6240ae023b8b99e330e7fffd98def5f819ea4a2ae79efac5645627
OK source_reference/pyproject.toml 8e6bcc892d11d7a46ebbcd6f191e750a098c5d5f7580eb2aaee73038185211da
OK source_reference/uv.lock 1f299e50a6a4f976aded9de6777555578a21ffd5502f8d3a4cffadc5e1cd94de
OK source_reference/cli.py 46918b27d3e8d0f7fa99c4e9861e600e36ed144fdb4f4a6743cb4884ce861cf7
OK source_reference/common.py 56cc48f56a8dbe223b04728d075b8c8382c801925ad6a508e8eaa2870b887276
OK source_reference/state.py 563232b3b0bc201245e9c35a79df052ead53b6b8c90348aebe3fe8d1d23c83d3
OK source_reference/auto_update.py aba759304fe24cb40d1bd18c67ee9c9c1f2414c05c14aa4eec049594c9ad0ac3
OK source_reference/commands/utility.py 3e8ac7c9a83713198e42e32a20e01b241ec1ba81a53be369afb4429be388437a
OK source_reference/commands/run.py 2595c0ec28b561ec3ad9a4d96b9a814df409c89db4ef22543fa39d6f24e248b5
OK source_reference/commands/execution.py ad82ab0798ca28b598c807d0490043d80751a25a61f0260ee5291575f2fee759
Verified 14 unchanged upstream files at a84e094c67544e70d88649ba2d2a1d48511b3af7
```

### 第4步 运行离线实验

目的：运行上游HistoryLogger/converter、边界和负对照并输出四种格式

```sh
.venv/bin/python run_experiment.py
```

开始 UTC：2026-10-05T05:34:04.241612+00:00
结束 UTC：2026-10-05T05:34:04.455246+00:00
退出码：0

实现结果：33/33通过；四种导出完成；无意外网络尝试
验收依据：outputs/summary.json、tests_raw.txt与四种导出文件

原始标准输出与标准错误：

```text
test_list_sessions (test_history.TestHistory.test_list_sessions) ... ok
test_log_and_get_history (test_history.TestHistory.test_log_and_get_history) ... ok
test_01_real_logger_roundtrip_order_unicode (__main__.PipelineTests.test_01_real_logger_roundtrip_order_unicode) ... ok
test_02_real_logger_lists_sessions (__main__.PipelineTests.test_02_real_logger_lists_sessions) ... ok
test_03_missing_session_is_empty (__main__.PipelineTests.test_03_missing_session_is_empty) ... ok
test_04_empty_file_and_blank_lines (__main__.PipelineTests.test_04_empty_file_and_blank_lines) ... ok
test_05_corrupt_history_raises_json_decode_error (__main__.PipelineTests.test_05_corrupt_history_raises_json_decode_error) ... ok
test_06_payload_can_override_event_metadata (__main__.PipelineTests.test_06_payload_can_override_event_metadata) ... ok
test_07_notebook_schema_and_code_count (__main__.PipelineTests.test_07_notebook_schema_and_code_count) ... ok
test_08_notebook_text_output_is_preserved (__main__.PipelineTests.test_08_notebook_text_output_is_preserved) ... ok
test_09_notebook_error_output_is_preserved (__main__.PipelineTests.test_09_notebook_error_output_is_preserved) ... ok
test_10_notebook_rich_output_is_preserved (__main__.PipelineTests.test_10_notebook_rich_output_is_preserved) ... ok
test_11_stderr_label_becomes_stdout_observed_limitation (__main__.PipelineTests.test_11_stderr_label_becomes_stdout_observed_limitation) ... ok
test_12_execute_result_loses_execution_count_observed_limitation (__main__.PipelineTests.test_12_execute_result_loses_execution_count_observed_limitation) ... ok
test_13_piped_shell_and_python_both_get_bash_magic (__main__.PipelineTests.test_13_piped_shell_and_python_both_get_bash_magic) ... ok
test_14_exclamation_shell_does_not_get_bash_magic (__main__.PipelineTests.test_14_exclamation_shell_does_not_get_bash_magic) ... ok
test_15_session_termination_absent_from_notebook (__main__.PipelineTests.test_15_session_termination_absent_from_notebook) ... ok
test_16_automation_and_input_are_retained_in_notebook (__main__.PipelineTests.test_16_automation_and_input_are_retained_in_notebook) ... ok
test_17_markdown_preserves_text_omits_error_rich_and_termination (__main__.PipelineTests.test_17_markdown_preserves_text_omits_error_rich_and_termination) ... ok
test_18_plain_text_does_not_export_execution_outputs (__main__.PipelineTests.test_18_plain_text_does_not_export_execution_outputs) ... ok
test_19_jsonl_export_exactly_preserves_event_records (__main__.PipelineTests.test_19_jsonl_export_exactly_preserves_event_records) ... ok
test_20_uppercase_extension_is_supported (__main__.PipelineTests.test_20_uppercase_extension_is_supported) ... ok
test_21_unsupported_format_prints_warning_without_file (__main__.PipelineTests.test_21_unsupported_format_prints_warning_without_file) ... ok
test_22_empty_notebook_contains_title_only (__main__.PipelineTests.test_22_empty_notebook_contains_title_only) ... ok
test_23_recorded_code_is_never_executed (__main__.PipelineTests.test_23_recorded_code_is_never_executed) ... ok
test_24_default_history_is_under_isolated_home (__main__.PipelineTests.test_24_default_history_is_under_isolated_home) ... ok
test_25_multiline_records_stay_one_jsonl_line (__main__.PipelineTests.test_25_multiline_records_stay_one_jsonl_line) ... ok
test_26_network_negative_control_is_blocked (__main__.SafetyAndSourceTests.test_26_network_negative_control_is_blocked) ... ok
test_27_upstream_copies_match_fixed_hash_manifest (__main__.SafetyAndSourceTests.test_27_upstream_copies_match_fixed_hash_manifest) ... ok
test_28_actual_cli_ast_default_is_oauth2 (__main__.SafetyAndSourceTests.test_28_actual_cli_ast_default_is_oauth2) ... ok
test_29_actual_cli_ast_suppresses_update_for_log (__main__.SafetyAndSourceTests.test_29_actual_cli_ast_suppresses_update_for_log) ... ok
test_30_actual_log_ast_filters_before_tailing (__main__.SafetyAndSourceTests.test_30_actual_log_ast_filters_before_tailing) ... ok
test_31_source_config_does_not_redirect_history (__main__.SafetyAndSourceTests.test_31_source_config_does_not_redirect_history) ... ok

----------------------------------------------------------------------
Ran 33 tests in 0.037s

OK
[colab] Exported history to '[EXERCISE_ROOT]/outputs/fictional-demo.ipynb'.
[colab] Exported history to '[EXERCISE_ROOT]/outputs/fictional-demo.md'.
[colab] Exported history to '[EXERCISE_ROOT]/outputs/fictional-demo.txt'.
[colab] Exported history to '[EXERCISE_ROOT]/outputs/fictional-demo.jsonl'.
{
  "tests_run": 33,
  "failures": 0,
  "errors": 0,
  "upstream_history_tests": 2,
  "harness_pipeline_tests": 25,
  "safety_and_static_source_tests": 6,
  "unexpected_network_guard_events": 0
}
```

### 第5步 核对落盘产物

目的：检查实际事件数、notebook结构、文件哈希和格式信息差异

```sh
.venv/bin/python inspect_results.py
```

开始 UTC：2026-10-05T05:34:04.455776+00:00
结束 UTC：2026-10-05T05:34:04.483569+00:00
退出码：0

实现结果：11事件；12单元/6代码；输出哈希一致；错误和富内容在Markdown缺失
验收依据：inspect_results.py打印的JSON与实际导出文件相互印证

原始标准输出与标准错误：

```text
{
  "test_cases_passed": 33,
  "test_cases_total": 33,
  "jsonl_event_count": 11,
  "notebook_cell_count": 12,
  "notebook_code_cell_count": 6,
  "all_recorded_output_hashes_match": true,
  "notebook_has_error_object": true,
  "notebook_has_rich_json": true,
  "markdown_has_error_object": false,
  "markdown_has_rich_json_type": false,
  "text_has_error_object": false,
  "jsonl_has_termination_event": true,
  "unexpected_network_guard_events": 0,
  "note": "All event data is fictional. Code stored in the log or notebook was not executed."
}
```

路径说明：原始输出中的实验目录规范为 [EXERCISE_ROOT]；错误、返回值与实验结果未改写。

## 怎样解释33项通过

2项未改动上游 HistoryLogger 用例 + 25项自建管线/边界用例 + 6项安全/静态源码用例 = 33项。此数不包含重复执行次数，不能把原始运行、解压重跑和独立复验相加。

没有运行全仓库测试、远程集成测试或完整 CLI。静态 AST 检查证明固定源码如何写，不证明 CLI 运行时行为。

## 实际发现

### 元数据可覆盖

test_06：data内timestamp/event_type覆盖log_event自动写入值。日志不是远端执行来源真实性证明。

### 损坏JSONL会报错

test_05：合法行后接损坏行，get_history抛JSONDecodeError。不能把损坏历史当成自动容错的已完成记录。

### JSONL保留完整事件

test_19逐记录相等；实际11事件；包括session_terminated。原始结构化记录应与人读导出一起保留。

### notebook有损投影

stderr改stdout；execute_result改display_data并丢execution_count；session_terminated未导出。通过案例是在确认现有限制，没有修复这些限制。

### piped不是可靠的语言类型

test_13中print(1)也被加%%bash；execution.py:347确认Python REPL同样使用source=piped。导出的Python单元可能被误分类，应先检查后执行。

### Markdown和纯文本更有损

实际Markdown未保留ZeroDivisionError与application/json；txt未保留执行输出。不能从简报反推所有执行细节。

### 文档与源码认证默认值冲突

cli.py:78为OAuth2；README/operator skill写adc；test_28静态AST核验。本次采用固定源码事实，未触发认证。

### --config隔离不完整

common.py的HistoryLogger无参数，settings/log也独立取HOME；test_31静态核验。仅改sessions.json路径不足以隔离整个CLI。

### README运行器能力需源码复核

run.py的主流程未发现任意产物下载步骤，不能把README的retrieve output files当作已验证自动行为。只作为静态边界，不运行远端验证。

## 实际导出结果

```json
{
  "test_cases_passed": 33,
  "test_cases_total": 33,
  "jsonl_event_count": 11,
  "notebook_cell_count": 12,
  "notebook_code_cell_count": 6,
  "all_recorded_output_hashes_match": true,
  "notebook_has_error_object": true,
  "notebook_has_rich_json": true,
  "markdown_has_error_object": false,
  "markdown_has_rich_json_type": false,
  "text_has_error_object": false,
  "jsonl_has_termination_event": true,
  "unexpected_network_guard_events": 0,
  "note": "All event data is fictional. Code stored in the log or notebook was not executed."
}
```

同一输入的JSONL保留逐事件结构；Notebook、Markdown和TXT是有损的不同视图。kernelspec 显示 Google Colab 也是导出器写入的标签，不是远端执行凭据。日志与Notebook可能保留代码、输入回答和输出；真实项目对外分享前须检查敏感内容，本次数据全为虚构。

## 交付ZIP与复跑验收

文件：03-exercise.zip
公开副本字节：120758
公开副本 SHA-256：2df4ed14cf06229e2a5d5e5ace8c73c8dd6e415df1d71d0e533d098ffd57e9a5

公开副本仅规范导出日志路径、更新对应输出指纹及公开说明，保留原实验代码与结果。以下复跑记录描述清理前已完成的历史复验，不表示公开副本已重新执行。

ZIP在新目录解压后，依次创建全新虚拟环境、联网安装固定依赖、核验来源、运行实验、核对产物，全部五步退出码0。首次工程验证和使用现有依赖的解压验证仅属额外审计历史，没有替代这次新环境复跑。

包内 outputs 保留制作者运行快照；自行复跑会刷新时间、随机cell id和相应输出哈希。inspect_results.py 校验当前快照中的文件哈希；不要求新Notebook与旧Notebook逐字节相同。

## 官方条件与来源

- [官方固定仓库](https://github.com/googlecolab/google-colab-cli/tree/a84e094c67544e70d88649ba2d2a1d48511b3af7)
- [Google AI Pro福利](https://support.google.com/googleone/answer/14534406?hl=en)：页面列200 CCUs；web-only、18+、家庭计划管理者、排除试用。没有核查用户实际权益，也不把页面文字扩展成每月额度或CLI授权。
- [Colab FAQ](https://research.google.com/colaboratory/faq.html)：资源和型号不保证；免费且无正CU余额的托管runtime限制SSH/远控及主要绕过notebook UI的使用。付费余额不取消全部禁止事项。

没有核验第三方定制技能，不把官方仓库的 colab-operator 等同于其他技能文件，也不声称复现远程工作负载。

## 停止条件与清理

未创建远端资源，没有 Google 登录或 token 创建；无需执行任何远端stop。本次仅保留项目本地venv、runtime、脚本与输出，没有全局安装或系统配置修改。遇到需要账号、额度、凭据或远端资源的步骤应另行确认，不能由本离线练习自动延伸。

知识连接与后续扩展不构成本离线实验的远程功能验收。
