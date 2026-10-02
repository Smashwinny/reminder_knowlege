---
tags: [概念]
领域: 语音/实时交互
来源项目: s2s-voice-agent
创建日期: 2026-10-03
---

# Realtime 协议兼容层

**一句话定义**：把自研后端包装成"讲 OpenAI Realtime 方言"的服务端——暴露同一套 WebSocket/WebRTC 事件集（`input_audio_buffer.speech_started`、`response.output_audio.delta`、`response.done` 等，源码可提取 31 种），让全世界已认该协议的客户端**零改造**切换到自托管全开源栈。

**属于哪个领域**：语音交互 / API 协议设计（huggingface/speech-to-speech 的对外接口层）。

**展开**：
- 机关：协议面标准化 = 生态位免费继承。官方 demo 把网页客户端端点地址从托管 OpenAI 改成本机地址，一行业务代码不改即完成"端点互换"。
- 事件流一轮完整对话：`session.created` → `input_audio_buffer.append`（音频块流入）→ `speech_started/stopped`（VAD 判定）→ `committed` → `input_audio_transcription.completed`（STT）→ `response.create/created` → `output_audio_transcript.delta` + `output_audio.delta`（文本/音频双流）→ `response.done`（携带 ≤512 字符延迟账本 metadata）。收尾顺序固定 transcript.done < audio.done < response.done。
- 工具调用（如查天气）穿插方式：response 中出 `function_call_arguments.done` → 客户端 `conversation.item.create` 塞回工具结果 → 再 `response.create`——与文本侧工具调用同构。
- 通用规律：**任何"被广泛山寨的协议"都是架构资产**——兼容它的成本远低于自造协议再教育生态。

**与已有概念的关联**：与 [[MCP协议]]/[[M×N集成问题]] 同一经济学（M×N 定制 → M+N 标准接口）；与 [[LLM工具调用]] 互为语音侧/文本侧；管线本体见 [[级联语音管线]]，判定事件来源见 [[VAD与轮末判断]]。
