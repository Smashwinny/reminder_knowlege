# 实验日志 · ODS 私有 AI 服务器（ods_local_ai_server）

- 任务：71a6fc99-229b-4299-acd2-7ccb36fd2b06
- worker：kimi-pool-20261007-w1
- 日期：2026-10-07
- 仓库：Osmantic/ODS（浅克隆 ac1fd24，5460 文件，Apache-2.0，7107 stars，V3 预发布）

## 实验设计

真实安装会拉 Docker 全家桶并做系统级变更，超出 worker 实验范围。实验目标：核心测试套件实跑 + 结构阅读 + 模型选择逻辑定位。

## 运行记录（全部真实执行，exercise/run_output.txt）

1. `python -m pytest ods/tests -q --continue-on-collection-errors --basetemp=<干净临时目录>`：1046 collected → **2500 passed, 187 failed, 627 skipped, 1018 errors in 189s**。
2. 归因（--tb=line 异常类型统计）：1018 errors ≈980 FileNotFoundError/WinError（缺 docker/ollama 二进制、Unix 路径）+ 35 ModuleNotFoundError（pwd 等 Unix-only）；187 failed 集中在 bats/docker/launchd 集成语义——**macOS/Linux-first 项目实证**（install.ps1 存在但 Windows 支持以 WSL 为前提）。
3. 模型选择/硬件探测专项（dashboard-api/tests，-k "model or select or hardware"）：437 passed / 77 failed / 929 errors，同平台归因；硬件→模型推荐纯函数逻辑可跑部分真实通过。
4. 结构定位：硬件探测在 ods/extensions/services/dashboard-api/model_selection.py；7+ 服务组件各自带独立 tests/；项目自带 CLAUDE.md + ARCHITECTURE.md。

## 结论

- ODS 是"编排层"而非新组件：组件集成/服务发现/硬件-模型映射/云端回退的 know-how 是增量价值。
- "一行命令"省的是集成工序，运维本身（模型下载/驱动/升级兼容）不被消灭；V3 预发布期生产慎用。
- 未验证（诚实声明）：真实安装（Docker 全家桶+系统服务变更）；macOS/Linux 完整体验；Windows+WSL 路径。

## 产物

- `exercise/run_output.txt`
