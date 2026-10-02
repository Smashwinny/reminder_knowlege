---
tags: [概念]
领域: 语音/实时交互
来源项目: s2s-voice-agent
创建日期: 2026-10-03
---

# VAD 与轮末判断

**一句话定义**：VAD（Voice Activity Detection，语音活动检测）是给每小段音频打"是不是人声"分数的守门员小模型；轮末判断（如 Smart Turn）则在 VAD 发现停顿后裁决"话说完了没"——两级配合才能让机器"该接话时接话，不该时闭嘴"。

**属于哪个领域**：语音交互 / 实时对话系统（huggingface/speech-to-speech 管线的第一段）。

**展开**：
- VAD 只回答"声音停了"，回答不了"话说完了没"。"帮我订明天去**（想两秒）**上海的高铁"——纯静音计时会把犹豫停顿当句尾，把话拦腰提交，机器人开始回复，**用户被自己的机器人打断**。
- 上游分层设计：**Silero VAD 管"快"**（~2MB 小神经网络，每 32ms 判一次，发现语音段起止）；**Smart Turn v3.2 管"准"**（pipecat-ai 开源 ONNX 模型，只在停顿边界被触发时听整句的声学+语义特征判 complete/incomplete，incomplete 则 hold 继续听，最长等 2s 强制提交）。代价是确认延迟 +0.3~0.4s。
- 实验（s2s-voice-agent/exp2，numpy 合成信号复刻状态机）：犹豫句纯 VAD 提交 2 次且过早打断=是，加轮末判断后恰好 1 次完整提交；结束句两者均 1 次。坑：提交后必须"等新语音再武装"（Silero triggered 状态机），否则静音期重复提交。
- 可换后端：silero（默认）/ firered（FireRed 流式 VAD）。

**与已有概念的关联**：整条链路见 [[级联语音管线]]；协议事件 `input_audio_buffer.speech_started/stopped` 见 [[Realtime协议兼容层]]；是 Reachy Mini 机器人"耳朵"的实现（[[WebRTC机器人应用]]、项目笔记 reachy-mini）。
