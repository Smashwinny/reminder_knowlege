---
tags: [项目笔记]
项目: CMU 11-768 AI Agents 跟学
类别: 知识学习类（顶尖高校公开课程）
完成日期: 2026-10-03
来源: "https://x.com/Xudong07452910/status/2097846768323133559"
官网: "https://www.cmu-agents.com/"
---

# 项目笔记：CMU 11-768《AI Agents》

## 这是什么

CMU 2026 秋新开的研究生课（讲师 Daniel Fried & Graham Neubig，后者为 OpenHands 作者），26 讲四大板块：能力（工具/上下文/Skills/规划）→ 领域（Coding/GUI/Deep Research）→ 训练（SFT/RL×3）→ 安全·框架·交互·搜索。由拾遗推文（Xudong Han 推荐"Agent Engineering 进入高校课程体系"）触发学习。与 [[项目笔记/agent-harness]] 同源互补：那是工业界 harness 方法论，这是高校课程化的完整知识地图。

## 带来的概念

- 新建：[[Agent后训练SFT与RL]]（课程③板块 4 讲的浓缩：SFT 模仿专家轨迹 → RL 可验证奖励超越，rollout 是系统瓶颈）、[[程序化工具调用]]（Part 3 的 run_python：模型写代码沙箱一次执行多步策略）
- 强化互链：[[AgentHarness智能体挽具]]（作业 A1 就是它的教学版）、[[上下文预算与战略压缩]]（作业实现工作记忆压缩 2816→409 tok 实测）、[[AgentSkills技能包]]/[[分层按需加载]]（渐进披露：目录常驻+invoke_skill 取正文）、[[LLM裁判与自动评估]]（作业 A2 前置）、[[Agent循环]]（ReAct 域无关基类）

## 实验做了什么

对官方作业仓库 cmu-agents/assignment-1（commit 67498d8）实现了全部离线可测 TODO：
- base.py：域无关 ReAct 循环（build_prompt/run/load_skills/compact_context）
- code_agent.py：system_information 块 + 渐进披露 catalog + execute/send_message/invoke_skill 容错分发
- chess 三件套：3 个 strict 工具 schema + 4 个 `<chess_error>` 错误通道 helper + 分发器
- **结果：pytest 从基线 7 failed → 15 passed, 4 deselected（modal 计费测试按设计排除）**
- demo_react_loop.py：脚本化 LLM 零成本端到端演示（截断/压缩/渐进披露全触发）

## 坑与结论

- 环境：仓库要求 Python ≥3.11，swe-rex 隐性依赖 boto3（不装 import env 就炸）；pytest 的 tmp_path 在本机 Temp 目录权限拒绝，须 `--basetemp` 指到仓库内
- 作业真跑（Modal 沙箱 + DeepSeek API）是计费服务，离线测试完全免费——先离线全绿再考虑真跑
- 结论：**这门课的④板块（安全/框架/交互/搜索）与③板块（训练）是现有知识库最大增量**，后续可按跟学路线逐讲补 slides
