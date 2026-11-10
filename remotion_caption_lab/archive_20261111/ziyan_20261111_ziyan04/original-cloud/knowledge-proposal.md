---
tags: [项目, 候选增量, Remotion]
类别: 学习增量（尚未合入）
日期: 2026-11-11 Asia/Shanghai
---
# Remotion 无口播中文字幕：把导演提示词改成验收合同

## 查重依据
main SHA a8674777e18302b8804b137212b1396cbfe5a747；实读 vault/00-总览.md、vault/概念/React逐帧视频渲染.md、vault/项目笔记/ai-video-pipeline.md、vault/概念/动效描述词表.md、vault/概念/声明式视频源语言.md，以及项目笔记 huashu_art_motion、vibecoding_motion。样式参照 ai-video-pipeline/AI视频流水线-小白指南.html 与 vibecoding_motion/m_desc_guide.html。

已有：Remotion逐帧渲染、TTS时长驱动、props形状陷阱、动效四要素和缓动。不要新建同义概念笔记，不重复宣称发现Remotion。

## 仅建议新增
1. 给 [[React逐帧视频渲染]] 增补“静音字幕主导”的验收分支：本次4镜头×90帧=360帧，1920×1080、30fps；不需要TTS测时，字幕阅读时间直接成为镜头时长约束。3秒阅读只是本例设计，不是经用户实验验证的通用阈值。
2. 在 [[动效描述词表]] 增补“frame确定性”：Scene中useCurrentFrame相对于Sequence.from；错峰7帧≈233ms；spring由局部帧计算，避免依赖实际播放时钟。
3. 为项目笔记补“验收合同”：技术规格靠ffprobe；画面语义靠关键帧；字体与边界靠目视；渲染命令退出0并不证明内容准确。本例源码由worker直接编写，未验证“一句话让某模型导演”的效果。
4. 原帖模型与API推广不作为技术证据；LICENSE固定SHA后确认个人/非商业评估适用免费许可，不等同于所有组织均免费。
5. 版本边界：npm Remotion/CLI固定4.0.542，main固定e3a1be5c8b29c07ec3d36efe16cbc69b6170cb5d。main Sequence文档已不建议直接用Sequence，本例为4.x兼容实验；不据此声称验证新API或升级路径。

## 交付状态
候选成果只保存在item04隔离目录；未合入共享vault，未发布Git，未修改任务完成状态。实测字段以experiment-log.md与ffprobe.json为准。画面检查是同一worker自检，不是独立审核。
