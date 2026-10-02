---
tags: [概念]
领域: AI工程/团队协作
别名: [Team Harness Distribution, PR审核分发, 团队资产同步]
首次来源: "[[项目笔记/teamai-cli]]"
---

# 团队Harness的Git原生分发

**一句话定义**：把团队的 skills/rules/hooks/MCP 等 AI 资产放进一个共享 Git 仓库，用"push → 建分支+MR → reviewer 合并 → 各成员 SessionStart hook 自动 pull → 落入各工具原生目录"的流水线，把一个人的调教经验变成全员资产。

**属于领域**：AI 工程 / 团队协作工具链（teamai-cli 的核心机制）

**通俗理解**（比喻/例子，讲完落回术语）：就像团队的 npm 私服：没有人把 `.js` 文件用 U 盘拷来拷去，大家都 `npm install` 同一个 registry。teamai-cli 的 registry 就是一个普通 Git 仓库——管理员 push 一份 `SKILL.md`，成员开会话时 SessionStart hook 静默 `teamai pull`，skill 就出现在 `~/.claude/skills/`、`.codex/` 等各工具的原生目录里。**代码 review 流程第一次被搬到了 AI 资源上**：一份团队规则想进所有人的 AI，得先过 MR 这一关。

**关键机制**（teamai-cli 实测）：
- `teamai init <git仓库>` 把任意 Git 托管（GitHub/GitLab/私有）变成团队资源库；URL 强制 https/ssh 格式，push 走"建分支+MR"而非直推 main
- 分发内容八类：skills / rules / docs / env / agents / hooks / mcp / models，hooks.yaml 与 mcp.yaml 按各工具**原生格式**下发（密钥只声明 `${VAR}` 名，不写值入库）
- 接入即自动向 `~/.claude/settings.json` 注入 SessionStart/Stop/PostToolUse/UserPromptSubmit 四类 hook（命令带 `|| true`，正是 [[ClaudeCodeHooks与fail-open]] 的 fail-open 模式）
- 分发策略四件套：Roles（角色→namespace 映射）、Tags（标签订阅）、Sources（订阅其他团队的 skill 仓库）、Projects（与角色正交的项目维度）

**与已有概念的关联**：
- 基础资产格式：[[AgentSkills技能包]]（SKILL.md 目录是分发的主要货物）
- 自动同步的执行者：[[ClaudeCodeHooks与fail-open]]（SessionStart hook 是分发链最后一环）
- 单人版对应物：[[跨工具个人记忆层]]（Memmy 统一"一个人的多工具记忆"，teamai 统一"一群人的多工具 harness"）
- 资产即代码思想：[[PromptAsCode提示词即代码]]（提示词/规则可版本化、可评审、可回滚）
- 分发的择路问题：[[技能路由器与授权硬门]]（多了资产之后"谁能用哪个"）
- 总纲：[[AgentHarness智能体挽具]]（分发的正是 harness 组件）

**首次接触于**：[[项目笔记/teamai-cli]]
