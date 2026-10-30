---
tags: [项目笔记, 开源项目, 人机协作, 2D动画, VTuber]
created: 2026-10-09
---

# Mesh Avatar Studio（插画变动头像）

- 仓库：https://github.com/shinshin86/mesh-avatar-studio（MIT 代码/样例角色保留，快照 39d1625，v0.1.0，2026-10-09 浅克隆实测 540★）
- 来源：子 agent（kimi-sub-20261009-s1）分类上报 06ac032d，主控批复后主控完整学习

## 是什么

一张插画 → 会眨眼/说话/转头/呼吸/摆发的 Live2D 风格 2D 网格头像。四步人机管线：①Agent 备料（读图定位/摆骨架/切层/自检）→ ②人在编辑器 Pose test/口型检查 → ③人拖拽修关键点 → ④Agent 固定姿势自检评审。机器做 1/4+1/4 且强制自检，人是审核员不是操作工。

## 两个最值得学的设计

- **能力前置验证**：tools/vision-check.py 生成标定图让 agent 读坐标评分，不达标主动停下告知"可能不达标"——返工成本压缩成 10 秒标定（harness 七子系统之外的新增子系统位置）。
- **agent 作业书体裁**：docs/agent-guide.md 201 行，顺序+每步检查+资质声明制（模型不在推荐清单就明说）。与 SKILL.md（路由型）构成 agent 指令文件两种体裁。

## 本机实证

npm install 成功；vitest 107 用例 → **102 passed / 5 failed**（失败全为 Windows symlink EPERM 权限族——测试用符号链接构造路径逃逸攻击样本测自家 API）。e2e 与端到端头像生成未做（如实声明）。

## 许可分层

代码 MIT；样例角色 Miko 作者保留；vendor/mediapipe 面部关键点模型 Apache 2.0。

## 关联

- [[bead_pattern]]、[[sprite_gen]]（"单图→可用资产"三部曲）
- [[项目笔记/huashu_art_motion]]（一帧先行同族）、[[人机协同Interrupt]]（能力前置验证提案）
- [[AgentSkills技能包]]（指令文件两种体裁注记）
