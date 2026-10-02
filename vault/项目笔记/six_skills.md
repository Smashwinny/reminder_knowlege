---
tags: [项目]
类别: 知识学习类（X 推文 skills 盘点，6 个真实开源仓库）
上游仓库: zhaoxuya520/reverse-skill, conorbronsdon/avoid-ai-writing, mattpocock/skills, anthropics/skills, JimLiu/baoyu-design, justinjohnson25600/hermes_skills
完成日期: 2026-10-03
---

# six_skills（陈成六 Skill 盘点）

**这是什么**：陈成（@chenchengpro）2026-09 推文盘点的 6 个值得关注的 Claude skills，全部有真实开源仓库。本篇按"2 个深挖动手 + 1 个架构精读 + 3 个盘点介绍"处理。

**六个 skill 与定位**：
| # | Skill | 仓库 | 一句话定位 | 处理 |
|---|---|---|---|---|
| 1 | reverse-skill | zhaoxuya520/reverse-skill（39.3k★） | 逆向/渗透安全技能**路由器**：44 条路由规则+授权硬门+经验库 | 架构精读 |
| 2 | dev-pair | justinjohnson25600/hermes_skills/dev-pair | 跨模型**第二意见**：另一个 LLM 挑刺，daily_cap 硬预算+审计台账 | 盘点+概念吸收 |
| 3 | claude-api | anthropics/skills/skills/claude-api | 官方 API 参考技能：防模型凭旧记忆写错 API | 盘点 |
| 4 | gen-pptx | JimLiu/baoyu-design/skills/baoyu-design/agents/gen-pptx | 宝玉系 HTML→PPTX 生成管线（截图/可编辑捕获双路） | 盘点 |
| 5 | implement-spec | mattpocock/skills/skills/engineering/implement-spec | spec→工单任务图→worktree 并行施工→integration 合并 | **主学+实验** |
| 6 | avoid-ai-writing | conorbronsdon/avoid-ai-writing（4.8k★） | 74 类 AI 味模式库+零依赖检测器，signals not proof | **主学+实验** |

**它给我什么能力**：
- 用 implement-spec 的任务图/frontier 模式拆解任何多步开发任务并行派工
- 用 avoid-ai-writing 检测器（node 一条命令）给自己写的指南/文档"体检验 AI 味"，也可当 pre-commit 门槛
- 借 reverse-skill 的"路由+授权门+经验库"三件套组织自己日益增多的技能包
- claude-api 提醒：涉及 API 的代码先查权威参考，别信训练记忆

**引入的概念**：
- [[工单任务图与前沿调度]]
- [[AI味模式库与信号非证据]]
- [[技能路由器与授权硬门]]

**实验记录**：
1. avoid-ai-writing detector 实测：克隆 repo（bdeb726），自写 AI 味英文样本 → 9 处命中、得分 44（Moderate AI signals）；按 SKILL.md 规则改写 → 0 分 Clean。命令 `node repo/bin/avoid-ai-writing.js <file>`，JSON 输出存 exercise/detector_*.json。
2. implement-spec 微型演练（exercise/implement-spec-lab）：git 仓库内按 to-spec 模板写 spec.md + tickets.md（T1 tokenize / T2 report 依赖T1 / T3 cli 依赖T1T2），三张工单各自分支实现+断言测试全绿后逐个 merge 回 main，端到端 `python topwords.py sample.txt -n 3` 真实输出 `5 the / 2 dog / 2 fox`，git log 6 commits 全程可查。
3. 坑：Windows Python 3.14 无 pytest（实验改用 stdlib 断言脚本，反而更符合"零依赖"精神）；mattpocock/skills 里 implement-spec 实际路径在 skills/engineering/ 下（推文写的 in-progress 已过时）。

**后续可深入的方向**：
- reverse-skill 装进 Claude Code 实测一次真实路由（需授权语境，单独安排）
- gen-pptx 跑一次 HTML→PPTX，与本仓库"HTML→Edge 无头打印 PDF"管线对比
- 把 avoid-ai-writing 的 gate 接到本仓库 PDF 前置 HTML 的自检
