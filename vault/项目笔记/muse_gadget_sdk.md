---
tags: [项目笔记, 开源项目, ESP32, 智能硬件, Noise协议]
created: 2026-10-07
---

# Muse Gadgets SDK（Meta 开源硬件 SDK）

- 仓库：https://github.com/facebookincubator/muse-gadget-sdk（Apache-2.0，快照 b139b45，2026-10-07 克隆实测 1589 stars）
- 来源：@Roland.W 推文 https://x.com/rwayne/status/2106743937398682089（2026-10-02 发布，社区 24h 登顶 GitHub Trending）

## 是什么

给 Meta 个人 AI 智能体 Muse 自制硬件外设的开源 SDK：ESP32 刷开源固件（C/ESP-IDF）或树莓派装 musegadget 服务（Python），Muse 即可驱动屏幕、按钮、传感器、执行器。**AI 推理全在 Meta 云端，设备只做 I/O**，所以 $3 的 ESP32 就够。每个设备配对需 SDK token（gadgets.muse.ai），手机 Muse App 是配对与授权入口。

## 结构实测（487 文件）

- ESP32 SDK：main/ 下 32 个 C/C++ 文件（noise_tunnel、link_pairing、voice_*、ota、wifi_mgr、stack_monitor 等）；16 个板文件（M5Stack 全家桶/Waveshare/SenseCAP/乐鑫 Box-3）；26 个 sdkconfig；SDL/LVGL 桌面 UI 模拟器；37 个 Python 测试。
- Linux SDK：纯 Python，自带 Noise 协议实现（1833 行：noise_xx/envelope/framing/transport）；executor/fileops 让 Muse 获得安装账户同等机器权限（装 systemd 服务）。
- skills/：43 份 gadget-*/SKILL.md 设备说明书（Google Home/Sonos/Hue/扫地机/电视/3D 打印机…），CATALOG.md 索引。

## 连接架构

BLE 配对（transcript 存证 + 签名策略防中间人）→ Wi-Fi 上云建 Noise XX 加密隧道 → 语音/指令/图片走隧道。局域网存量设备由 Home Link（ESP32-C5 棒）发现代理。

## 实验（Windows 本机真实运行）

Linux SDK 测试三轮：包路径修正后 132 passed / 1 skipped / 11 errors（全部为 pytest 临时目录 PermissionError 本机环境问题；executor/service 因 Unix-only pwd 模块不可收集）。覆盖配对握手（官方 v5 向量）、Noise 会话/隧道、BLE 帧、配置、身份、网络报告。未做：固件编译（需 Linux/macOS ESP-IDF）、云连接（需 token）、硬件在环。

## 与 OpenMuse 的关系

**同名异质**：vault 的 [[openmuse]] 是 CopilotKit 的任务引擎（持久任务/浏览器接管/审批），与 Meta 本生态无关，注意区分。队列内 muse_tutorial_index / muse_tailscale / awesome-muse-connectors 是 Muse 产品家族的其他组件（在学/过期租约），互链不重复。

## 关联

- 概念提案：硬件AI分工范式、设备技能即提示词（见项目目录 knowledge-proposal.md，协调者终审）
- [[AgentHarness智能体挽具]]、[[AgentSkills技能包]]、[[护栏模式Guardrails]]、[[Zigbee与网状网络]]（智能家居设备群）
