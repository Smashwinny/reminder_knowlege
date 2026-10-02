---
tags: [项目]
类别: 开源项目类（Agent Skill 家族）
上游仓库: https://github.com/nevertoday/xxd-panel-116 （及 273 个 xxd-panel-NNN 系列）
完成日期: 2026-10-02
---

# xxd_panels

**这是什么**（一句话）：小小东（nevertoday）开源的 56 个 AI 生图 Agent Skills——把 54 种"转绘"风格提示词各装成一个标准 SKILL.md 仓库（xxd-panel-NNN），配一份家族运行时契约，由"将军"中控角色统一管理，形成风格多变、行为统一的 Skill 军团。

**它给我什么能力**：
- 56 种开箱转绘风格（粉彩涂鸦/瓷器碎片/点刻版画/刺绣章/糖霜浮雕……），一句话把照片变高级海报
- 四种交付模式：top-bottom / left-right 严格 50:50 对照、design-only 纯设计、wallpaper-pack 四端壁纸
- 目录批量转绘、交付偏好记忆、确定性缝线审计
- 可照抄的架构范式：宪法（original-prompt）/军规（soldier-runtime）分离 + 士兵/将军编制

**引入的概念**：
- [[转绘]]
- [[提示词权威边界]]（含消毒输出纪律）
- 复用已有：[[AgentSkills技能包]]、[[分层按需加载]]、[[质检Gate与自我纠错循环]]、[[确定性脚本]]、[[角色提示]]

**实验记录**（做了什么、结果、坑）：
- 克隆 xxd-panel-116/133/224 到 repo\；通读 3 个脚本全文确认安全后真实运行
- compose_panel.py：--plan 三种布局全部跑通；合成 poster-top-bottom.png（1536x2048, split exactly 1024/1024）与 poster-left-right.png（3072x2048）
- --audit 缝线审计：好图 offset 0.00% 判 OK；故意做的 45:55 坏图被检出 OFF（45.0%/55.0%），脚本建议分两张生成再拼
- panel_preferences.py：save→load→clear 全流程通过（XXD_PANEL_PREFS_DIR 重定向到 exercise\prefs 避免污染真实配置）
- configured_imagegen.py probe：本机无图像路由，返回 {"ok":false,"reason":"route_not_configured"} exit=2，如实记录；生图环节需用户自备路由
- 安装 skill 到 ~/.claude/skills 被权限策略拒绝，未执行，安装命令写进指南 Q13
- 许可注意：PolyForm Noncommercial 1.0，个人随便用，商用需作者书面授权

**后续可深入的方向**：
- 配好图像路由后跑一次真实转绘并按验收门禁逐条自检
- 仿照宪法/军规二分法把自己常用的输出（周报排版、PPT 配色）Skill 化
- 对比 224（材质型）与 133（版式型）宪法原文的写法差异
