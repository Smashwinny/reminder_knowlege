---
tags: [项目笔记, 开源项目, 程序化动画, AgentSkill, Canvas]
created: 2026-10-07
---

# huashu-art-motion（花叔艺术动画 Skill）

- 仓库：https://github.com/alchaincyf/huashu-art-motion（MIT，快照 26dba25，396 文件；总目录 alchaincyf/huashu-skills 52 skills）
- 来源：@花叔 AlchainHust 推文 https://x.com/AlchainHust/status/2107018546194882678（Opus5.5 + 本 skill 的 SpaceX 白板视频）

## 是什么

给 coding agent 的"用代码画画并做成动画"职业技能包：35 种艺术风格配方卡（渲染器手法+母题动作+签名转场+质量星级+当前短板）+ 9 种解说视频语法（8 种带 JSON spec 可参数化渲染时长精确片段）+ 完整 Canvas 引擎工程（35 场景/转场库/绘画库/render.py）。源自 2026-10-04 复刻 15 秒"艺术史速通"（16 个艺术时代）的经验固化。

## 核心方法

- 五层机制：固定场景骨架 × 每幕都是活的画 × 签名转场 × 节拍网格 × 叙事锚。
- 窄桥硬规则：画面必须动（量帧差自检）；代码画场景、AI 生帧做人；种子确定性（mulberry32，全引擎 53 处 rng(seed)）；独立审片 agent。
- 质量分布（INDEX 自述）：★★★ 20 / ★★ 14 / ★ 1（伦勃朗最该重做）；普遍短板=角色。

## 本机实测

结构校验 6/6：35 卡 35 场景文件 / 9 语法 / 引擎骨架 9 项 / 种子实现 / 8 JSON spec 合法（exercise/validate_structure.py）。引擎实渲染被权限分类器拦截未执行（Chromium 已装，授权后 render.py --solo <id> --stills 可补）；本机无 ffmpeg 未出 mp4。

## 依赖与入口

`npx skills add alchaincyf/huashu-art-motion`；渲染需 uv + Playwright Chromium + ffmpeg。开新片：复制 scripts/engine 到项目，改 eras.js 段落表、写 scenes/<id>.js。

## 关联

- [[AgentSkills技能包]]（skill 形态标准结构：SKILL.md 路由表+参考文档+代码工程）
- [[vibecoding_motion]]、[[ai-video-pipeline]]、[[三帧关键帧插画法]]、[[动效描述词表]]、[[分镜表驱动生成]]、[[程序化建模]]
- [[证据优先质检ProofOverClaims]]（质量星级+短板的诚实标注法）
- 概念提案：风格即渲染器（见项目目录 knowledge-proposal.md，协调者终审）
