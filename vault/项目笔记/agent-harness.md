---
tags: [项目笔记]
类型: 开源项目类
项目: affaan-m/ECC (Everything Claude Code)
日期: 2026-10-03
来源: 拾遗队列 https://x.com/0xwhrrari/status/2095134652688220236
---

# agent-harness — Agent Harness 工程（以 ECC 为样本）

## 这是什么

源起是一条病毒式营销推文："Anthropic 以 $250K-$750K 年薪聘请了这位会构建 harness 的工程师"（不点名）。查证后：
- **"this engineer"** 最可能指 **Affaan Mustafa**（github.com/affaan-m）：Anthropic x Forum Ventures 黑客松冠军（zenith.chat），开源 **ECC (Everything Claude Code)**——GitHub 实测 **271,019 stars**，自称 "The Agent Harness Operating System"。其 LinkedIn 显示 2026-06 起与 Anthropic 关联（Claude Community Ambassador）；"$250K-$750K"大概率是把 Anthropic 公开职位薪资带和他的故事混在一起的 engagement bait。
- 推文附带的《Harness Engineering: How to Build AI Agents That Don't Fall Apart》长文（rari@0xwhrrari）主体是真技术内容：**问题不在模型智能，在 harness 环境**；引用 Dario Amodei "you need a harness to use them" 与 OpenAI《Harness engineering: leveraging Codex in an agent-first world》。

## 核心知识（带走了哪些概念）

- **[[AgentHarness智能体挽具]]**（新）：模型是推理引擎，harness 决定它"能看什么、能碰什么、什么存活、什么算证据、何时必须停"。七职责：契约→地图→工具最小权限→验证与证据→上下文工程→失败廉价→停止条件。
- **[[本能学习与置信度评分]]**（新）：ECC 的 continuous-learning-v2.1——PreToolUse/PostToolUse hook 观察会话→后台小模型提炼原子 instinct（置信度 0.3~0.9）→项目作用域隔离→聚类进化成 skill。
- **[[上下文预算与战略压缩]]**（新）：sonnet 打底 opus 攻坚（~60% 降本）、MAX_THINKING_TOKENS 10000、50% 早压缩、MCP<10 个。
- 关联旧概念：[[Agent循环]]、[[AgentSkills技能包]]、[[Agent中间件]]、[[分层按需加载]]、[[质检Gate与自我纠错循环]]、[[工具目录膨胀]]、[[KV缓存与上下文]]

## ECC 结构速记

293 skills（按需加载的工作流，主表面）/ 68 agents（frontmatter 定义 name/tools/model 的子代理）/ 94 commands（斜杠兼容层）/ 23 rules（常驻规范）/ hooks（PreToolUse/PostToolUse/Stop 等事件自动化）/ contexts（动态系统提示注入）/ 跨平台适配（.codex/.opencode/.cursor）。装法：Claude Code 插件 `ecc@ecc`（官方渠道唯一，谨防第三方镜像投毒）。

## 动手实验（exercise/mini_harness.py，全部真实跑通）

30 行核心逻辑从零搭迷你 harness：**契约 → 日志(JSONL) → 重试 → 验证门 → 记忆注入**，驱动无头 `claude -p`（haiku）。
- task_a：20.2s / $0.0413 / 2 turns ✅；`learn` 写入 memory.md；task_b：46.7s / $0.0542 ✅，**产出标题自动带 [HARNESS] 前缀**（记忆注入生效，模型没被告知）——"harness 越用越聪明"实证
- **四个真实的坑**（每坑对应一职责）：①多行 prompt 经 cmd.exe 断行→全灭（日志审计）②模型谎报 DONE 但没写文件→验证门拦截 ③无头模式默认拒绝 Write（permission_denials 里躺着完整被拒内容；`--allowedTools` 是变长参数还会吞掉后面的 prompt）→`--permission-mode acceptEdits` ④learn 写入的记忆带尾换行→脏记忆打破 harness→注入前必须清洗

## 坑与结论

- 营销钩子（不点名+$ salary+空泛"15分钟工作坊"）底下可以藏真项目——判断学习类与否要看实质指向，不看话术
- ECC 是"把 harness 当操作系统做"的极端样本：个人日常用不必全装（装满会吃光上下文，见[[上下文预算与战略压缩]]），挑 2~3 个职责自己实现 mini 版反而最有效
- `claude -p` 无头模式是穷人版 Claude Agent SDK：JSON 输出+权限模式+审计字段(permission_denials/modelUsage)，本实验全用它
