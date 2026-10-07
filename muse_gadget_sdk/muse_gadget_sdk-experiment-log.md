# 实验日志 · Muse Gadgets SDK（muse_gadget_sdk）

- 任务：92100bf6-10ff-4494-9625-4538006a1739
- worker：kimi-pool-20261007-w1
- 日期：2026-10-07
- 仓库：facebookincubator/muse-gadget-sdk（浅克隆，快照 b139b45）

## 实验设计

无 ESP32 硬件、无 Muse 账户/token、Windows 本机。选择可真实执行的实验面：仓库全量结构阅读 + Linux SDK（纯 Python）测试套件在 Windows 上真实运行，验证设备端协议栈纯逻辑层。

## 运行记录（全部真实执行，完整输出 exercise/experiment_run1.txt）

1. **第 1 轮** `python -m pytest tests/ -q`：10 个收集错误——包未安装（musegadget 不在路径）。
2. **第 2 轮** `PYTHONPATH=src`：8 个测试文件可收集；test_executor.py / test_service.py 收集失败，原因 `ModuleNotFoundError: No module named 'pwd'`（Unix-only 模块）。
3. **第 3 轮** 排除 2 个 Unix-only 文件后全量：**132 passed, 1 skipped, 11 errors in ~5s**。11 个 ERROR 经归因全部为 pytest 临时目录 PermissionError（WinError 5 拒绝访问 C:\Users\Windows\AppData\Local\Temp\pytest-of-Windows），属本机环境而非代码缺陷。
4. **复测说明**：计划以干净 basetemp 复测 11 个错误项，被权限分类器拒绝（外部克隆仓库执行类操作），结果如实保留第 3 轮原状。
5. **结构统计**（真实计数）：487 文件；ESP32 主程序 32 个 C/C++ 文件；26 个 sdkconfig 板级配置（16 个板文件）；Linux SDK 11 个测试文件；ESP32 侧 37 个 Python 测试；skills/ 43 个 gadget SKILL.md；Noise 纯 Python 实现 1833 行；官方配对测试向量 link_pairing_v5.json 8KB；版本 999.0.0。

## 132 项通过覆盖

配对握手（含 v5 官方向量）、Noise 会话与隧道、BLE 帧封装/生命周期、配置存储、身份持久化与损坏恢复、网络 SSID 报告、Muse API 调用、pebble-ring 桥示例等。

## 结论

- Linux SDK 的协议层（配对/加密/封帧）跨平台真实可用；执行层（executor/service）绑定 Unix。
- 仓库工程质量高：主机侧 fakes + harness 测试模式（esp32/tests/link_*_harness.c）让无硬件测试成为一等公民，UI 模拟器（SDL/LVGL）让无板改界面可行。
- 未验证（诚实声明）：固件编译与烧录（需 ESP-IDF + Linux/macOS）、云侧连接（需 token）、硬件在环。

## 产物

- `exercise/experiment_run1.txt`（三轮测试完整输出）
