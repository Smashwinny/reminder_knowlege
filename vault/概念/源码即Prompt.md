---
tags: [概念]
领域: AI 工程 / Prompt 工程
别名: [prompt as product, thin runtime, 发布期渲染]
首次来源: "[[项目笔记/godogen]]"
---

# 源码即 Prompt

**一句话定义**：仓库的价值不在可执行代码，而在几篇精心措辞的 Markdown 说明书——发布（publish）给 AI 智能体后，由它现场把游戏/软件重建出来；GitHub 7k 星的 Godogen 整个仓库里没有一行游戏代码。

**属于领域**：AI 原生软件工程（AI-native development）。

**通俗理解**：驾校不发车，但发的教材能让学员自己开走一辆车。Godogen 的产品是"说明书三件套"：① 运行时清单（CLAUDE.md，十几行章程：状态写 README、花钱先确认、验收看运行）；② 单页引擎指南（Godot/Bevy/Babylon 各一份，专收静默失败陷阱）；③ asset-gen 技能包（AI 画美术的工艺，见 [[AgentSkills技能包]]）。项目脚手架、截图工具全由 AI 到场后按指南重建——**薄运行时（thin runtime）**：发布出来的仓库只有文档，没有脚手架。

**发布期渲染（publish-time render）**：Markdown 里挖 `${VAR}` 占位符，发布脚本按"引擎 × 宿主"填变量——一套模板渲染出 3 引擎 × 2 宿主 = 6 种口味（CLAUDE.md vs AGENTS.md、/asset-gen vs $asset-gen、不同引擎的资产目录与 .gitignore）。没有 6 份源码树，只有 1 份模板 + 1 个渲染器，本质是[[提示词模板]]的工程化多目标版。

**为什么有效**：固定住不可妥协的原则（状态存哪、怎么验收、怎么花钱），把架构设计、任务分解全留给强模型现场发挥——给"聪明员工"的手写便条，不是给流水线工人的 SOP。模型越强这套说明越有效。

**与已有概念的关联**：
- 思想近亲：[[PromptAsCode提示词即代码]]——都把 prompt 当工程产物对待；区别是 PromptAsCode 参数化"一张图"的生成，源码即 Prompt 参数化"一整个项目"的生成
- 验收配套：[[证据优先质检ProofOverClaims]]——薄运行时钉死的第一原则就是它
- 技能载体：[[AgentSkills技能包]]；状态机制：[[Checkpoint存档与持久执行]]（README.md 就是人可读存档点）

**首次接触于**：[[项目笔记/godogen]]
