---
tags: [概念]
领域: AI 工具生态 / 个人 Agent
别名: [Hermes, OpenClaw, 小龙虾, ClawBot, 消息通道]
首次来源: "[[项目笔记/wechat_hermes_notebot]]"
---

# Agent网关与消息通道

**一句话定义**：跑在自己常驻主机上的开源个人 AI 智能体（Hermes、OpenClaw 等），把微信/Telegram 等 IM 消息通道接入 Agent 循环——聊天软件变成随时遥控"住家数字员工"的遥控器。

**属于领域**：AI 工具生态 / 个人 Agent 基础设施。

**通俗理解**（比喻/例子，讲完落回术语）：像给家里请了一个 7×24 在岗的秘书，微信 ClawBot 就是他的"工位电话"——你发条消息，他收单干活再回话。落回术语：Hermes/OpenClaw 是**网关+运行时**（收消息→按 profile 分诊→调模型→执行工具→回消息），微信 ClawBot/iLink Bot API 是**通道**（把个人微信扫码绑定到网关），channel 绑到哪个 profile，哪个 Agent 接单。

**关键事实**：
- Hermes Agent：开源自托管（GitHub 4.7万+ Star），带记忆系统与闭合学习循环，`hermes claw migrate` 可从 OpenClaw 一键迁移配置/记忆/技能/Key
- OpenClaw（小龙虾）：同类前身，轻量、渠道多（20+）
- 常驻是前提：主机睡眠/断网期间消息不会被及时处理
- 微信 ClawBot 入口：手机微信 → 我 → 设置 → 插件，扫码绑定；默认会把短时间连续消息**合并**处理，"一条消息一条结果"的场景必须关掉合并

**与已有概念的关联**：
- 相关：[[Agent循环]]（网关背后的执行引擎）、[[LLM工具调用]]、[[提示注入]]（IM 消息是不可信输入，专用 profile + 最小工具授权是根本防线）、[[统一数据网关]]（同样"一处接入多源"思路，对象是平台数据而非 IM 消息）
- 相关：[[技能路由器与授权硬门]]（多 Agent 时"谁接单"的分流问题，网关用 channel→profile 绑定静态解决）

**首次接触于**：[[项目笔记/wechat_hermes_notebot]]
