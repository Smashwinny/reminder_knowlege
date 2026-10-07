---
tags: [概念]
领域: AI 工具生态 / 编程智能体
别名: ["Agent Skills", "技能包", "SKILL.md"]
首次来源: "[[项目笔记/awesome-llm-apps]]"
---

# AgentSkills技能包

**一句话定义**：给编程智能体（Claude Code / Codex / Cursor）"按需加载的方法论包"——一个带 frontmatter 的 SKILL.md + 可选脚本和参考资料，一条 `npx skills add <url>` 即可安装。

**属于领域**：AI 工具生态 / 编程智能体

**通俗理解**：Tool 是厨房里的锅（函数，程序执行）；Skill 是**菜谱卡片**（Markdown 方法论，LLM 读进上下文后照着做）。awesome-llm-apps 的 agent_skills 区 9 个技能均含 `SKILL.md`（name + description 说明"何时用"）+ `scripts/` + `references/`，且过安全+评测 CI 门禁。用户自己的 `/learn-project` skill 就是同一格式。

**与已有概念的关联**：
- 与 [[LLM工具调用]] 的对比：Tool=代码给程序跑，Skill=说明书给 LLM 读，[[MCP模型上下文协议]]=连接标准
- 加载进上下文后，LLM 常会转而调用工具/脚本——Skill 是把"知识"与"执行"粘起来的包装
- 家族化实战见 [[项目笔记/xxd_panels]]：56 个"士兵"共用一个家族运行时，内部治理靠 [[提示词权威边界]]（宪法管审美、军规管物流）
- 76k stars 标杆实例：[[项目笔记/archify]]——SKILL.md 教 AI 填 [[JSON-IR类型化中间表示]] 表格，本地 CLI finalize 门禁当终审法官

**首次接触于**：[[项目笔记/awesome-llm-apps]]

## 方法与实际效果分开（2026-10-05）

[[项目笔记/ponytail]] 的核心方法、紧凑规则和会话 hook 是不同载体。文件存在、宿主载入、行为改变与结果通过测试是四层证据；[[最小实现决策阶梯]] 是方法，参数化 SQL 和输入校验才是程序机制。
