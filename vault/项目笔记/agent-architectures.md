---
tags: [项目笔记]
项目: agent-architectures
类别: 开源项目类
状态: 已学完（2026-10-03）
来源链接: "https://x.com/miles_mazy/status/2097154216267837847"
---

# agent-architectures（Agent 架构三项目推荐帖）

## 这是什么

X 帖子（Miles Ma）推荐的"从零学 Agent 架构"三个 GitHub 项目，本笔记深挖第 1 个、盘点后 2 个：

1. **FareedKhan-dev/all-agentic-architectures**（深挖，4.5k star，MIT）：35 种文献级 Agent 架构的标准化 Python 库（基于 LangGraph），每个架构统一 `build()/run()/diagram()` 合同 + 35 份真跑 Notebook + 17 题 benchmark 排行榜（最近 33/42=78% @ Llama-3.3-70B）。7 大族：推理反思/采样搜索/RAG/记忆/工具行动/多智能体/安全路由。工程纪律核心=[[确定性选择器模式]]（13/35 架构使用）。
2. **pguso/ai-agents-from-scratch**（盘点，4.8k star）：JS + node-llama-cpp 本地模型，15 章零框架徒手搭 Agent（工具调用→ReAct→思维树→工具路由），另有 Python 姊妹版。
3. **wquguru/harness-books**（盘点，3.2k star）：两本免费书，Claude Code / Codex 的挽具工程分析（提示词即控制面、查询循环、上下文治理、错误恢复），是 vault 已学 [[AgentHarness智能体挽具]] 概念的原著级展开。

## 带来的概念

- [[确定性选择器模式]]（本库最独特贡献）
- [[推理反思架构族]]（Reflection/Reflexion/CoVe/Self-Discover/Constitutional AI）
- [[采样搜索架构族]]（Self-Consistency/ToT/LATS/Ensemble）
- [[RAG架构谱系]]（Agentic/CRAG/Self-RAG/Adaptive/GraphRAG）
- [[记忆架构谱系]]（MemGPT/Voyager/Graph Memory）
- [[多智能体架构谱系]]（Blackboard/Debate/STORM/Meta-Controller）

## 实验做了什么（F:\reminder\agent-architectures\exercise\）

本机 Ollama 跑 Qwen2.5-3B-Instruct（Q4_K_M，从 hf-mirror 下 GGUF 后 `ollama create`），exercise/arch_compare.py 实测三架构：
- Reflection：科普写作首稿 8/10 一次达标，4.7s 收敛；
- ReAct：农夫卖奶题经 calculator 工具 3 次调用算出 504（正确），但小模型反复"确认"不收尾，max_rounds=5 强制结束（护栏生效的实例）；
- Self-Consistency：应用题翻车——5 条高温采样集体偷懒输出同一个占位符 "x"，0/3；补做两轮乘法实验（arch_voting_mul.py）——简单乘法直答 5/5 但 num_predict 截断废掉答案提取；边界乘法直答 0/5、表决 0/5（ollama 结构化输出回退失控，采样混入乱码还能赢多数票）。总教训：架构救不了模型能力地板，provider 能力矩阵（ollama structured_output=False）是硬约束。

## 坑与结论

- ollama 官方拉模型在 Clash fake-ip 代理下报 "redirect target not allowed"（CDN 域名被污染成 198.18.x.x）；解法=hf-mirror.com curl 下载 GGUF + `ollama create`。
- `architectures/__init__.py` 全量导入 35 个架构，缺 networkx 会整体 ImportError，需补装 networkx json-repair。
- **结论：架构选型要匹配模型能力**——3B 模型上 Self-Consistency 救不了"长推理链集体偷懒"；benchmark 显示的能力边界以 70B 为基准，本地小模型复现实验适合学机制、不适合追分数。

## 产出

- `F:\reminder\agent-architectures\agent-architectures-小白指南.pdf`
- 学习路线：先用 ai-agents-from-scratch 徒手搭 → 本库试驾 35 架构 → harness-books 读工程化。
