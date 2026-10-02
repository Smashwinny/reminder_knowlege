---
tags: [项目笔记]
项目: agentic-design-patterns
类别: 知识学习类（开源书）
完成日期: 2026-10-03
来源: "拾遗任务 f5b25c7d（x.com 推文）"
---

# Agentic Design Patterns 开源书

## 项目是什么
Antonio Gulli（Google 高级工程师）2025-09 开源的书《Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems》：424 页（实际 PDF 482 页）+ 全套 Jupyter notebooks，把 Agent 开发反复出现的 21 种结构解法逐一命名讲解，LangChain/LangGraph、CrewAI、Google ADK 三画布对照。GitHub 镜像 `DanieleSalatti/AgenticDesignPatterns`（851 star，fork 自 AnkunHuang）。已克隆到 `F:\reminder\agentic-design-patterns\repo\`。

## 带来的概念（全部已入库）
- [[Agent设计模式目录]] — 21 模式四层地图 + Level 0-3 复杂度分级（总纲）
- [[提示链PromptChaining]] — 固定流水线，站间 JSON 契约（模式 1）
- [[并行化编排Parallelization]] — Sectioning/Voting/Governing 三形态（模式 3）
- [[反思模式Reflection]] — 生成-批评循环 + 双停止条件（模式 4）
- [[护栏模式Guardrails]] — 输入输出双重安检门（模式 18）
- [[LLM裁判与自动评估]] — rubric + LLM-as-a-Judge（模式 19）
- [[A2A智能体互通信]] — AgentCard 名片协议（模式 15，与 [[MCP协议]] 互补）
- 互链更新：[[质检Gate与自我纠错循环]]、[[评分契约与护栏]]（未合并，互链）

## 实验做了什么
`exercise\patterns_playground.py`：确定性 FakeLLM 离线复现 5 个代表性模式——提示链三站 JSON 契约接力、路由工单分诊、ThreadPoolExecutor 三 Critic 并行+总裁合成、反思循环 4→7→9 分 early-stop、pydantic 协议门拒收越权工具名/越界置信度后放行合法调用。**5/5 PASS，重复运行输出一致**，完整输出存 `exercise\run_output.txt`。

## 坑与结论
- **notebook 全依赖外部 API**：61 个文件全要 OPENAI_API_KEY 或 GOOGLE_API_KEY，本机无 Key 未真跑原版；改用 FakeLLM 复现模式骨架（换真模型客户端即原版做法）。
- **notebook 多为无扩展名 ipynb**：Colab 导出导致，`file` 命令确认是 JSON，用 `json.load` 按 `cells[].source` 抽代码阅读。
- **PDF 无书签目录**：`get_toc()` 返回空；章标题靠 notebooks 目录名 + 附录页扫描还原。
- **最大收获**：模式一旦命名即可跨项目复用；"能用提示链别上循环"、"护栏里代码永远包住 LLM"、"反思循环双停止条件"三条工程判据直接可落地。
