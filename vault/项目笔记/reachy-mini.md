---
tags: [项目]
类别: 开源项目类（Hugging Face 开源桌面机器人，无硬件 MuJoCo 仿真实验）
上游仓库: https://github.com/pollen-robotics/reachy_mini
完成日期: 2026-10-03
---

# reachy-mini

**这是什么**（一句话）：Hugging Face（旗下 Pollen Robotics）的开源表情桌面机器人——28cm/1.5kg、头部 6 自由度 Stewart 并联平台 + 2 根可当天线的舵机，Lite 版 $299 / Wireless 版 $449；2025-07 开卖 24 小时预售近 50 万美元、5 天破 100 万美元（本次拾遗抖音视频的新闻本体）。软硬件全开源：软件 Apache-2.0、硬件图纸 CC BY-SA-NC，可无硬件 MuJoCo 仿真运行。

**它给我什么能力**：
- 零硬件入门具身 AI：一台电脑跑仿真，行为与真机一致
- 给 LLM 一具身体：官方对话 App = VAD + LLM 工具调用 + TTS 驱动实体运动
- 表情机器人编程：关键姿态 + 时长 + 插值的三元组序列（[[情感运动序列]]）
- 零安装分享：Web 应用经 WebRTC 一个链接远程玩（[[WebRTC机器人应用]]）

**引入的概念**：
- [[Stewart并联平台]] —— 6 推杆并联出头部 6 自由度
- [[情感运动序列]] —— 表情 = keyframe + 插值性格（[[补间动画与缓动函数]] 的物理版）
- [[WebRTC机器人应用]] —— 静态网页直连机器人的应用生态

**实验记录**（做了什么、结果、坑）：
- 环境：Python 3.14 装 mujoco 无预编译轮子 → 退回 Python 3.12 重建 venv，mujoco 3.3.0 + reachy_mini 1.11.0
- `reachy-mini-daemon --sim --headless` 后台起仿真（localhost:8000），exp1 连接成功：头部 7 关节（6 推杆+1 身体轴）+ 天线 2 关节，点头/摇天线/回休息位全部通过
- exp2 四种插值 100Hz 真实采样对比：cartoon 唯一过冲（+1.09mm，峰值 21.09）且起步先反向沉 0.56mm 蓄力，峰值速度 228.9mm/s ≈ linear(57.4) 的 4 倍；轨迹存 trace_*.npy，图 exp2_traces.png
- exp3 手写 4 段表情序列（好奇/害羞/开心/回正）跑通；坑：枚举名是 MIN_JERK 不是 MINJERK
- 其它坑：仿真模式无音频硬件 → SDK 带 `media_backend="no_media"`；pitch/roll 软限位 ±40°
- 全部实验脚本与日志在 `reachy-mini/exercise/`，指南 PDF：`reachy-mini/ReachyMini-小白指南.pdf`

**后续可深入的方向**：JS/WebRTC 应用发布到 HF Spaces；对话 App 接入国产 LLM；情感库微调（把 exp3 的序列参数化）；与 LeRobot 数据格式打通做模仿学习。
