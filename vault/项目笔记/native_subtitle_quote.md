---
tags: [项目笔记, 开源项目, AgentSkill, 视频处理, 社交内容]
created: 2026-10-07
---

# native-subtitle-quote-image（视频字幕长图 Skill）

- 仓库：https://github.com/chengyi-ai/native-subtitle-quote-image（MIT，快照 08d6990，2026-10-07 克隆实测 1832 stars，当天推送）
- 来源：@ChengYi3629 推文 https://x.com/ChengYi3629/status/2107427874731155490（用户案例 12 天 0→3000 粉=单方案例主张）

## 是什么

本地视频/YouTube 链接 → 找金句 → 精确取帧 → 拼 3:4 社交长图（保留原生字幕或绘制审核过的后期字幕）。Agent Skill 形态（SKILL.md 路由 + references/ 三文档）+ Python 脚本独立可跑。原生/脚本双模式从不混用（"原生不重绘 · 脚本不冒充"伦理红线）。

## 管线与版式

找句子（字幕时间轴）→ sample 精确取帧（句子时间点±窗口）→ 字幕条 extent 裁剪 → stitch 紧凑拼图 → 逐张质检可否决。版式三细节：先拼源像素再统一缩放（防首句变形）/脚本主图 70% 起（句多降 48%）/字幕条零间隙。

## 本机实证

39 项测试全绿（9.12s，含 17 subtests），关键端到端用例：ffmpeg lavfi 合成视频 → sample 取帧 → stitch 渲染真实跑通。无系统 ffmpeg，imageio-ffmpeg 捆绑二进制兜底（:20）。成品目检（examples/gallery 陈数案例，已复制 exercise/example_output.jpg）：版式承诺兑现。未实测 yt-dlp YouTube 路径与真实视频出图。

## 与生成后处理管线的关系

[[sprite_gen]] 概念（生成后处理管线）的社交内容域实例：取帧=切分/字幕条裁剪=清洗/紧凑拼图=排版/3:4+质检=契约。差异：sprite-gen 交付机器（游戏引擎），本条交付流量（平台+人眼）。

## 关联

- 概念提案：内容工厂管线（见项目目录 knowledge-proposal.md，协调者终审）
- [[项目笔记/sprite_gen]]、[[项目笔记/huashu_art_motion]]（第三个 Agent Skill 样本：导演型/迁移型/内容工厂型）、[[ai-video-pipeline]]、[[证据优先质检ProofOverClaims]]
