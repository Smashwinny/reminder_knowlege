---
tags: [项目笔记]
项目: codex-dual-home
类别: 知识学习类（X 文章教程）
完成日期: 2026-10-03
---

# codex-dual-home — Codex 双开（CODEX_HOME 多实例隔离）

## 这是什么
X 文章《Codex双开配置教程》（Hardy Chen @Chchenhao0129，2026-09-18，97 赞/218 书签/8.5 万浏览），经诺鸭船长3 @noahduck283 以"信息差"钩子帖引用传播。文章本体：针对 Plus 额度不够/Pro 太贵，教你在同一台电脑上把 Codex 分成两个独立实例（原文面向 macOS 桌面版：`open -n -a Codex` + `CODEX_ELECTRON_USER_DATA_PATH` + AppleScript 启动器；含更新回滚流程）。本批将其核心原理迁移到 Windows CLI 实测，CLI 双开只需一个 `CODEX_HOME`。

## 带来的概念
- [[CODEX_HOME多实例隔离]] — 换家目录即换身份；profiles 换穿搭不换人；与 [[GitWorktree并行隔离]] 正交叠加

## 实验做了什么（Windows 11 + codex-cli 0.160.0 全部真跑通）
1. 基线：老家 `codex login status` → Logged in using ChatGPT；config.toml model=gpt-6.1-sol
2. 换家：`CODEX_HOME=~/.codex-work` → **坑实锤：目录不存在直接拒绝启动**（不自动创建）；建目录后 → Not logged in，新家仅 tmp/
3. 配置隔离：新家写独立 config.toml（reasoning_effort=high vs 老家 low），`codex doctor` 两家对比分别报出各自的 config.toml / auth.json 路径
4. 启动器：exercise\codex-work.ps1 / codex-work.cmd（set 变量 + mkdir 兜底 + codex @args），实跑 doctor 指向新家

## 坑与结论
- **CODEX_HOME 指向不存在目录 → 拒绝启动**，启动器必须带 mkdir 兜底
- doctor 退出码非零 ≠ 失败：未登录时 doctor/login status 也非零，按输出内容判断
- 额度跟账号不跟实例：双开的收益是隔离与并行，不是白嫖额度
- 程序（npm 全局 exe）全机共享一份，升级回滚影响两个实例；家当（配置/凭证）不随程序走
- Windows 桌面版 Codex App 双开（open -n 等价法）社区反馈新版本不可靠——CLI 双开是跨平台稳路线
