---
tags: [概念]
领域: CLI 工具 / 开发环境
别名: [Codex双开, 家目录隔离, CODEX_HOME]
首次来源: "[[项目笔记/codex-dual-home]]"
---

# CODEX_HOME多实例隔离

**一句话定义**：`CODEX_HOME` 是 Codex CLI 的家目录环境变量（默认 `~/.codex`，收纳 auth.json 凭证、config.toml 配置、history/sessions 历史、memories 记忆），启动前把它指到另一个目录，同一个 codex.exe 就变成一个互不相干的新实例。

**属于领域**：CLI 工具 / 开发环境隔离

**通俗理解**：家目录就是 AI 助手的"户口本+私人物品箱"——登录凭证是身份证、config.toml 是生活习惯、历史和记忆是个人经历。换一个箱子（目录）再启动，它就是一个新"人"；换回去，又变回原来那个。注意坑：**目标目录必须先建好，Codex 不会自动创建、直接拒绝启动**（实测 `Error loading configuration: ... but that path does not exist`）。

**与已有概念的关联**：
- 正交互补：[[GitWorktree并行隔离]] 隔离"在哪干活"（代码工作目录），CODEX_HOME 隔离"以谁的身份干活"（凭证/配置/记忆），可叠加成双层并行
- 额度澄清：双开不产生新额度，额度跟 ChatGPT 账号走不跟实例走；省额度走 [[规划执行分账]]（[[上下文接力]] 同项目族）
- 同族边界：config.toml profiles 只是同一家里的"换穿搭"（共享 auth.json/历史），要换身份必须换 CODEX_HOME；单次覆盖用 `-c key=value`
- 通用模式："换家目录=换身份"是 CLI 界通用解，Claude Code 用 `CLAUDE_CONFIG_DIR`、Docker 用 `DOCKER_CONFIG`、SSH 用 `-F`；与 [[沙箱与审批正交]] 同属"把边界划清"的工程思想

**首次接触于**：[[项目笔记/codex-dual-home]]
