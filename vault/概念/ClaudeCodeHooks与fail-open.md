---
tags: [概念]
领域: AI 原生开发 / Agent 遥测
别名: [hooks, UserPromptSubmit, Stop hook, Notification hook, 失败放行]
首次来源: "[[项目笔记/clawdeck]]"
---

# ClaudeCodeHooks与fail-open

**一句话定义**：Claude Code 在会话生命周期的关键节点（SessionStart、UserPromptSubmit、Notification、Stop、StopFailure、SubagentStart/Stop、PermissionRequest、SessionEnd、PreCompact）按 `~/.claude/settings.json` 里的注册表**主动把事件 JSON 推给你指定的 HTTP 端点或命令**，而"fail-open（失败放行）"指 hook 端点拒连/超时/非 2xx 时会话照常继续——观测者挂掉绝不连累被观测者。

**属于领域**：AI 原生开发 / Agent 遥测（Agent 生命周期事件采集）

**通俗理解**：hooks 就像给会话装了门磁和摄像头：不装，想知道"谁在干活、谁卡住了"只能挨个开终端轮询（拉模式，又累又滞后）；装了，每个事件发生瞬间就有一条 JSON 推到你的仪表盘（推模式，实时且零轮询）。SideCrab（Claw'deck）的伴飞服务 crabd 就是靠 10 个 hook 喂出来的：prompt 事件→working，Notification→needs_input，Stop→done，StopFailure→failed。其中 9 个用 `"type":"http"` 由 CLI 本体直发（不落 shell、不起子进程），只有 SessionStart 因 CLI 不对它跑 http hook 而保留 command 型 curl 条目。超时设 2~3 秒上限（PermissionRequest 因长轮询例外给 60s），保证仪表盘永不拖慢 prompt。

**与已有概念的关联**：
- 是 [[人机协同Interrupt]] 的"传感层"：Interrupt 处理"怎么把问题交还给人"，hooks 解决"系统怎么知道有会话在等人"
- 事件流形态同 [[JSONL事件日志与折叠模型]]：一个推（hooks 实时）、一个落盘（转录持久），crabd 两者都吃
- fail-open 与 [[健康探测三态]] 同一价值观：观测失效必须被"诚实呈现"（worried 螃蟹 + 数据截至横幅），而不是伪装成正常或拦死业务
- 反例对子： [[提示注入]]（SC-01 漏洞——能写进模型输入的通道要按最高信任设防，即使只听 127.0.0.1）

**首次接触于**：[[项目笔记/clawdeck]]（mini-crabd 实验：204 无正文 hook 入口 + curl 逐事件驱动状态机）
