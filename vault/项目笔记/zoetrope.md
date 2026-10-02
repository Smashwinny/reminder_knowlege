---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/furkankly/zoetrope
完成日期: 2026-10-02
---

# zoetrope

**这是什么**（一句话）：只读的终端/浏览器可视化工具，把 Claude Code 或 Codex 会话的 JSONL 转录实时画成"流动图"——主 agent、子 agent、工具调用一目了然，支持直播跟随和"时间旅行"回放。Rust + ratatui，MIT，v0.2.0，约 979★。

**它给我什么能力**：① 实时监督长任务（哪个子 agent 卡住、哪个工具失败）；② `zoe inspect <id前缀>` 秒出历史会话树（agent 数/工具成败/token）；③ 回放会话录像学习 agent 编排；④ 脚本友好的无界面输出；⑤ 零网络、文件不上传。

**引入的概念**：
- [[JSONL事件日志与折叠模型]] — 转录=append-only 事件日志，状态=fold 事件的纯函数（顺序无关）
- [[双时钟模型]] — 状态读内容时钟、动画走呈现时钟，才有可 scrub 的时间旅行
- [[可逆派生状态]] — spawn ack≠完成；pending 工具调用是"还活着"的铁证；启发式必须可逆

**实验记录**（做了什么、结果、坑）：
1. 本机无 Rust 工具链 → 用 Releases 预编译 zip（x86_64-pc-windows-msvc），`zoe.exe --version` → `zoe 0.2.0` ✅
2. `zoe inspect repo/assets/claude/demo.jsonl` → 打印完整会话树（main + 4 subagent + workflow group，含每 agent 工具成败统计）✅
3. `zoe inspect a3ffe5cf` → 按 id 前缀回放本机真实历史会话："reminder_knowlege 学习方法 skill"，56 次调用 (50✓ 6✗)，84484 tokens ✅
4. 无 tty 环境跑 `zoe demo.jsonl --speed 20` 4 秒 → 输出 91KB ANSI 帧，Python 剥转义后确认渲染内容（agent 卡片、⚒ chip、连线），帧存 exercise/tui_frame.txt ✅
5. Codex rollout 文件自动识别格式（无需 --provider）→ `gpt-5.6-terra, 4 agents, 46 tool calls` ✅
坑：① 非 inspect 命令在非交互环境会向 stdout 狂吐 ANSI 帧，交互观看必须在真实终端；② Windows 下别硬上 cargo，直接用预编译二进制。

**后续可深入的方向**：读 docs/ARCHITECTURE.md 的顺序无关 fold 与 snapshot ladder 实现（imbl 持久化集合）；ratatui/rataflow 自研图布局；给其他 agent CLI 写一个新 provider。
