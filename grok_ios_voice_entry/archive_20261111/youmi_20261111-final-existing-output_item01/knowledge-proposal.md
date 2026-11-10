# 知识合入候选：iOS 人声入口

不修改现有仓库、不变更概念总数。

## 查重
已读 vault/00-总览.md、项目笔记/s2s-voice-agent.md、概念/第二大脑LLMWiki.md，参考 karpathy_second_brain_guide.html 的暖白底/彩色卡片/大号序号。未找到人声快捷指令专条。

## 建议增量
向 [[项目笔记/s2s-voice-agent]] 追加“会话前的系统入口链”旁注：人声识别→快捷指令→App语音动作，不等于 STT/LLM/TTS 管线全部本地，更不等于替换 Siri。
向 [[证据优先质检ProofOverClaims]] 追加“三层观察门”：触发、会话打开、可辨认回复分开；未知记录为 null。
可选项目笔记 ios_vocal_bot_entry：记录原帖及 Apple 文档，但不把作者锁屏体验当兼容性保证。

## 证据
五步自写 Python 实验退出码均 0；5 个护栏单测通过。八格设备矩阵全部未测。没有 iPhone、声音准确率、锁屏行为或端到端延迟实测；状态只能为“部分待验证”。
