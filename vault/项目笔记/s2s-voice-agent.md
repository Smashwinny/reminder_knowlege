---
tags: [项目]
类别: 开源项目类（Hugging Face 官方开源语音智能体管线，无声卡文本管道级轻量实验）
上游仓库: https://github.com/huggingface/speech-to-speech
完成日期: 2026-10-03
---

# s2s-voice-agent

**这是什么**（一句话）：Hugging Face 官方的低延迟全模块化语音智能体管线——VAD→STT→LLM→TTS 四段级联、8 队列 4 线程流式接力，经 WebSocket/WebRTC 暴露 OpenAI Realtime GA 事件集（源码可提取 31 种事件名），组件全可换（2×12×4×8=768 种配置），Apache-2.0，v1.0.0 Production/Stable，**已投产为数千台 Reachy Mini 机器人的对话后端**（正是 [[项目笔记/reachy-mini]] 里"官方对话 App"的本体）。

**它给我什么能力**：
- 全本地不上云的语音助手（Mac 16GB 或 NVIDIA 24GB，`pip install speech-to-speech` 三条命令起服务）
- 中文全家桶换装：STT 槽 paraformer/sensevoice，LLM 槽任意 OpenAI 兼容 API（国产模型可接），TTS 换中文音色
- 给机器人/智能硬件装"嘴和耳朵"（Reachy Mini 同款后端，WebRTC 送声）
- 已有 OpenAI Realtime 客户端的产品改个端点即切自托管，零改造
- 生产级 Python 流水线活教材：队列解耦/BaseHandler 模板方法/注册表模式/全链路延迟埋点

**引入的概念**：
- [[VAD与轮末判断]] —— Silero 管快、Smart Turn 管准，"说完没完"的两段式裁决
- [[级联语音管线]] —— 8 队列流式接力、ttfa、barge-in 打断、延迟账本
- [[Realtime协议兼容层]] —— 假装成 OpenAI，协议面标准化=生态位免费继承

**实验记录**（全部在 exercise/，本机 Windows 无声卡，语音端到端如实未验证）：
- exp1 mini_s2s.py：4 线程 5 队列复刻级联架构（文本块模拟音频），实测 ttfa=0.892s vs e2e=1.614s，用户提前 722ms 听到声音；坑：TTS handler 忘写 q_out.put 导致主线程收零块
- exp2 vad_smart_turn.py：numpy 合成"犹豫句/结束句"，流式状态机复刻 VADHandler 两段式判断；犹豫句纯 VAD 提交 2 次且过早打断，加轮末判断后恰好 1 次；坑①提交后需"等新语音再武装"否则静音期重复提交②过早判定基准应为最后一帧语音时刻
- exp3 realtime_protocol_check.py：正则扫源码提取 31 种事件名冻结集，重放含工具调用的 24 事件全过校验，延迟账本 metadata 190/512 字符合规
- exp4 组件矩阵盘点：直接数源码 VAD 2 × STT 12 × LLM 4 × TTS 8 = 768 种管线配置
- 秒级实测数字（stt=0.18s/llm=1.24s/tts_ttfa=0.12s/e2e=2.01s）引用自上游 docs/response-latency.md

**坑与结论**：Python 3.14 + numpy/scipy 即可跑全部实验，不必装 torch 全家桶；全双工打断怕扬声器回声可 `--local_audio_block_mic_during_playback`（播放时暂停收音）；级联 vs 端到端选型口诀——要"听懂语气"选端到端，要"可控可换可私有"选级联。

**后续可深入的方向**：真机（有声卡设备）跑 pip 版测真实延迟；接国产 LLM + paraformer 组中文语音助手；把 demo 网页客户端部署到 HF Spaces 配合 Reachy Mini 仿真；精读 diarization（说话人分离）模块。
