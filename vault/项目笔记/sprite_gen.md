---
tags: [项目笔记, 开源项目, 程序化美术, 游戏资产, 精灵生成]
created: 2026-10-07
---

# sprite-gen（程序化 2D 精灵生成）

- 仓库：https://github.com/aldegad/sprite-gen（Apache-2.0，快照 ece1ac8=包版本 2.39.0，2026-10-07 克隆实测 2575 stars，当日仍在推送）
- 来源：@darkest_alex（韩文）推文 https://x.com/AldegadWildKim/status/2106805154788090010（Star 2.4k / v2.24.0 / 行走强化 / 和服 8 方向）

## 是什么

一张角色立绘 → 游戏引擎可消费的精灵图集/透明循环动画。Python CLI（≥3.11，pillow+numpy）+ Codex/Claude skill（SKILL.md）。核心价值在生成后处理：逐行生成锁身份 → chroma 背景转真 alpha → 逐姿态提取透明帧 → 烘焙带 manifest.json.frame_layout 的机器可读图集。

## 双管线

- A 图集行式：prepare→gen/gen-set→extract→compose-atlas，curation webview 人工筛选回路（对比/否决/微调/实时看循环）。
- B 视频→循环：视频模型出动作片段→帧门→自动循环点选择；`--facing right|left` 画布+提示词一致；方向检测默认 record-only（--facing-fix none），纠错 opt-in（mirror/regen）并明示"提示词不保证方向"。

## 本机实证

pytest 全量 9741 collected → **8210 passed** / 6 failed / 1507 errors in 426s。归因：1507=pytest 临时目录 PermissionError（本机环境）；6 failed 全平台相关（POSIX 路径/字节冻结）。有效通过率 99.93%。compose-atlas 对自带 fixture 实跑被权限分类器拦截（跑测试允许、执行仓库脚本需用户点名授权），未绕过。生成侧需外部模型 API 未调用。

## 工程亮点

pyproject 记录 setuptools 77 版本坑与 NEP 50 pinning 理由（chroma 提取字节契约）；9741 项测试；Wanted AI Championship 2026 参赛项目。

## 像素艺术族谱

[[bead_pattern]]（照片→像素图纸）/ [[huashu_art_motion]]（代码画风格动画）/ sprite-gen（AI 生图→引擎资产）——三条同族记录都保留一处"人必须把关"的回路（换色校对/独立审片/curation 筛选）。

## 关联

- [[像素化渲染管线]]、[[程序化建模]]、[[项目笔记/bead_pattern]]、[[项目笔记/huashu_art_motion]]
- 概念提案：生成后处理管线（见项目目录 knowledge-proposal.md，协调者终审）
