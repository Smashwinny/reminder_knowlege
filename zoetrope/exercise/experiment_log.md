# zoetrope 动手实验真实记录（2026-10-02）

环境：Windows 11 中文版，Git Bash + PowerShell，无 Rust 工具链。
zoe 二进制：F:\reminder\zoetrope\bin\zoe.exe（v0.2.0 官方预编译 x86_64-pc-windows-msvc）。

## 实验 1：验证安装

```
$ ./bin/zoe.exe --version
zoe 0.2.0
```

## 实验 2：回放仓库自带演示会话（headless 会话树）

```
$ ./bin/zoe.exe inspect repo/assets/claude/demo.jsonl
session demo — Add a dark mode toggle to settings
  mode: normal
  permission: acceptEdits
  last prompt: Also respect the OS system preference when no choice has been saved yet.
  8 agent(s), 20 tool call(s) · 3 file edits · 1 queued

  ◌ [main] claude  (idle) — id=main
      model: claude-opus-4-8
      tools: 9 (9✓ 0✗ 0⏳)   tokens: 1420
    ✓ [subagent] Explore  (done) — id=a1000000000000001
        Map the theme system
        tools: 2 (2✓ 0✗ 0⏳)   tokens: 220
    ✓ [subagent] general-purpose  (done) — id=a2000000000000002
        Implement the toggle component
    ✓ [subagent] general-purpose  (done) — id=a3000000000000003
        Write tests for the toggle
        tools: 4 (3✓ 1✗ 0⏳)   tokens: 820
    ✓ [subagent] claude-code-guide  (done) — id=a4000000000000004
    ✓ [group] code-review  (done) — id=wf_demo01
      ✓ [subagent] workflow-subagent  (done) — id=w1000000000000001
      ✓ [subagent] workflow-subagent  (done) — id=w2000000000000002
（后略）
```

要点：main 下面挂着 4 个子 agent 和一个 workflow group（组内还有 2 个子 agent），
注意 a300 有 `1✗`——一个失败的工具调用也会被如实画出来。

## 实验 3：按会话 id 前缀回放自己的真实历史会话

```
$ ./bin/zoe.exe inspect a3ffe5cf
session a3ffe5cf-0024-4250-8bce-8ff9e64366a3 — reminder_knowlege 学习方法 skill
  mode: normal
  permission: auto
  1 agent(s), 56 tool call(s) · 6 file edits · 1 queued

  ◌ [main] claude  (idle) — id=main
      model: claude-opus-5-5
      tools: 56 (50✓ 6✗ 0⏳)   tokens: 84484
```

要点：不用记完整 UUID，唯一前缀即可；数据来自本机
`C:\Users\Windows\.claude\projects\F--reminder\a3ffe5cf-....jsonl`。

## 实验 4：TUI 回放真实渲染（无终端环境下验证能跑）

```
$ timeout 4 ./bin/zoe.exe repo/assets/claude/demo.jsonl --speed 20 > tui_raw.bin
（4 秒输出 91~94 KB 的 ANSI 转义帧序列 —— TUI 确实在持续重绘）
```

用 Python 剥掉 ANSI 转义序列后可辨认出真实画面内容：
agent 卡片（`● claude ⚒ 5 · Workflow active 520 tok`）、子 agent 卡片
（`● Explore / Map the theme system / running`）、工具 chip（`⚒ Grep 5.0s ✓`、
`⚒ Bash 10s ✗`）、卡片之间的连线（`│ ╭─┴─`）和右侧时间线刻度。
完整一帧见 exercise/tui_frame.txt。

在真实终端（Windows Terminal / PowerShell）里运行即可交互观看：
`F:\reminder\zoetrope\bin\zoe.exe F:\reminder\zoetrope\repo\assets\claude\demo.jsonl`
按键：space 暂停/播放，[ ] 上/下一个提示词时代，g 跳到直播边缘，
s 切换空档压缩，f 跟随镜头，? 帮助，q 退出。

## 实验 5：Codex 格式自动识别

```
$ ./bin/zoe.exe inspect repo/assets/codex/cli-0.149.1/2026/08/26/rollout-...jsonl
session 01a03eb1-... — (untitled)
  app: codex-tui
  version: 0.149.1
  cwd: /Users/demo/personal/projects/zoetrope
  4 agent(s), 46 tool call(s)
  ◌ [main] codex  (idle) — id=main
      model: gpt-5.6-terra
```

要点：不用 `--provider codex` 也自动按内容识别了格式（provider 按文件内容、
不按路径判断）。

## 实验 6（云上）：浏览器版

https://zoetrope.furkankly.dev —— 同一 Rust 核心编译成 WASM，文件在本地解析不上传。
