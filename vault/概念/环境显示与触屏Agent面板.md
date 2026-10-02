---
tags: [概念]
领域: 人机交互 / Agent 遥测硬件
别名: [ambient display, 环境计算, 触屏仪表盘, Claw'deck, SideCrab]
首次来源: "[[项目笔记/clawdeck]]"
---

# 环境显示与触屏Agent面板

**一句话定义**：ambient display（环境显示）指信息**不等你去找它、而是一直在你余光里**的呈现范式——SideCrab/Claw'deck 把它用到 Agent 运维上：一块约 $250 的 Corsair Xeneon Edge 触屏（2560×720）摆在显示器下面，用一只像素螃蟹的心情汇总所有 Claude Code 会话状态（calm=安好 / alert=有会话等你 / worried=馈送失联），还能隔着桌子点一下回答会话。

**属于领域**：人机交互 / Agent 遥测硬件（桌面实体仪表盘）

**通俗理解**：多开 3~5 个 Claude 会话后，"谁跑完了、谁在等批准、谁被限流挂了"成为高频焦虑，Alt+Tab 轮询终端既累又滞后。环境显示把这套状态从"按需查询"升级成"房间级信号"：从房间另一头一眼看到 ⚠️，走过去点屏幕即可应答。混合栈是标准答案：**数据面 Python**（crabd 伴飞服务，hooks 采集 + 单一馈送）、**显示壳 C#/.NET 10 + WebView2**（无边框、置顶、从不夺焦、按显示器 PnP id 钉屏、休眠唤醒自动回钉——浏览器 F11 全屏做不到）、**界面本身 Web**（迭代最便宜）。2026-09 这波同赛道还有 Stream Deck 按键版（ClawDeck）、ESP32 小圆屏用量表（ChibiDeck/Clawdmeter），SideCrab 赢在"看"升级成了"顺手答"。

**与已有概念的关联**：
- 数据从 [[ClaudeCodeHooks与fail-open]] 来，状态经 [[单一馈送与schema冻结]] 的 /v1/state 分发
- "点屏回答会话"是 [[人机协同Interrupt]] 的物理外设化：Interrupt 信号获得房间级可见性
- 面板审批默认关闭的教训见 [[提示注入]]（SC-01：本机任意进程可经 /v1/config 把指令写进下一次 Stop hook 的 continue 词表）
- 升级走 staging→last-good→原子换名→回滚，见 [[发布交换与健康门回滚]]
- 想自己复刻：mini-crabd 实验证明纯标准库即可跑通软件主链路，换 ESP32/旧手机当屏即可零硬件门槛入场

**首次接触于**：[[项目笔记/clawdeck]]（2026-09 X/LinkedIn 病毒传播的开源项目，MIT）
