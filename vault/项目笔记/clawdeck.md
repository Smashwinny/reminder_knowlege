---
tags: [项目笔记]
类别: 开源项目类（Agent 遥测硬件，无硬件轻量实验）
学习日期: 2026-10-03
上游仓库: https://github.com/Dixie-sketch/Clawdeck（镜像 SideCrab 原仓库，MIT）
本地克隆: F:\reminder\clawdeck\repo
来源: 拾遗 task daf9577d（X 病毒帖 "physical touchscreen dashboard for Claude agents"）
---

# clawdeck（SideCrab / Claw'deck）

## 这是什么
把 Corsair Xeneon Edge 触屏（2560×720，约 $250）变成 Claude Code 集群状态实体仪表盘的开源项目（MIT）。像素螃蟹的心情就是状态：calm/alert/worried。三件套：**crabd** 伴飞服务（Python 单文件约一万行，只听 127.0.0.1:2722，读 hooks 事件 + ~/.claude 转录 + OAuth 用量，服务 /v1/state 与 /panel/）、**SideCrab.Panel**（.NET 10 + WebView2，无边框不夺焦钉在 Edge 屏）、**toast 通知器**（Windows 原生通知带 Acknowledge/Snooze 回传）。Windows only。2026-09 经 X/LinkedIn 病毒传播（"THIS GUY BUILT A PHYSICAL TOUCHSCREEN DASHBOARD JUST TO MANAGE HIS CLAUDE AGENTS"）。

## 带来的概念
- [[ClaudeCodeHooks与fail-open]] — hooks 推模式采集 + 观测者挂掉不连累会话
- [[单一馈送与schema冻结]] — 一份 /v1/state 快照 + schema 钉 5 + 字段存在性探测
- [[环境显示与触屏Agent面板]] — ambient display 范式 + Python/C#/Web 混合栈分工

关联已有：[[人机协同Interrupt]]、[[JSONL事件日志与折叠模型]]、[[零依赖编程]]、[[健康探测三态]]、[[提示注入]]、[[发布交换与健康门回滚]]

## 实验做了什么（exercise\mini_crabd.py，全部真实运行）
约 180 行纯标准库复刻软件主链路 hooks→状态机→/v1/state→/panel/，跑在 :2799：
1. hook 事件逐条 curl 驱动：session-start→idle、prompt→working、notification→needs_input、stop→done、stop-failure→failed、session-end→gone，排序与老化规则与上游一致；
2. JSONL 转录真实解析：sample_transcript.jsonl 4 行 → outputTokens 440；
3. mood 随 waiting 会话 calm↔alert 切换；
4. 无头 Edge 截图自证面板：🦀⚠️"有会话在等你" + 橙色 needs_input 卡片 + 中文问题 + 燃烧 440 tok（4 行）；
5. 加分：直接跑上游 hooks/sidecrab_statusline.py（crabd 未运行）→ 静默降级输出 "🦀 sidecrab · Opus · clawdeck"，退出码 0，fail-open 实证。

## 坑与结论
- **Git Bash 内联中文 JSON 会以错误编码发出**（curl 报 000），必须 `--data-binary @utf8文件`；
- 上游 crabd 声明 Python 3.13，本机 3.14 跑实验件无碍（标准库而已）；
- 原组织 github.com/sidecrab 现已 0 公开仓库（删库/转私），Dixie-sketch/Clawdeck 为完整功能镜像（35 stars，2026-10-01 仍在更新），引用时注意注明；
- SC-01 教训：localhost ≠ 信任边界，能写进模型输入的通道按最高信任设防；
- 状态枚举按 open set 消费（v0.36 新增 failed 就是先例），switch 别写死。

## 产出
- PDF：F:\reminder\clawdeck\clawdeck-SideCrab小白指南.pdf（10 问卡片 + SVG 架构图/状态机 + 实验 5 步 + 截图）
- HTML 源：F:\reminder\clawdeck\clawdeck_guide.html
- 实验件：F:\reminder\clawdeck\exercise\（mini_crabd.py、sample_transcript.jsonl、notif.json、panel_screenshot.png）
