---
tags: [项目笔记]
项目: deeptutor
类别: 开源项目类
完成日期: 2026-10-01
上游: https://github.com/HKUDS/DeepTutor
版本: v1.6.12
---

# DeepTutor（港大 HKUDS · AI 家教学习系统）

## 这是什么

Agent-native 的本机学习系统：讲题/出题/研究/画图/精读/视频学习跑在**同一个 Agent 循环**（能力运行时）上，配三层长期记忆和五引擎可插拔 RAG；最有特色的是能把本机 Claude Code 等 10 种编程智能体 CLI 当工具调用。40k★，Python(FastAPI):8001 + Next.js:3782，全部数据在本机 `data/`。

## 带来的新概念

- [[三层记忆]] — L1 jsonl 轨迹 → L2 界面摘要 → L3 用户画像（4 档案），LLM 压缩，Memory Graph 可回溯
- [[能力运行时]] — 一个循环 + 可插拔能力插件包
- [[子智能体咨询]] — consult_subagent 工具：发现本机 CLI → 无头运行 → 咨询预算

强化的旧概念：[[RAG检索增强生成]]（引擎可插拔 + 索引版本化）、[[Agent循环]]（工业化实例）、[[质检Gate与自我纠错循环]]（doctor 体检/连接探测/嵌入失配检测）。

## 实验做了什么（全部本机验证通过）

1. `pip install deeptutor` + 配置中转站 Anthropic（claude-haiku-4-5）→ `run chat` 端到端对话（cost $0.0016/次）
2. Ollama 手动装 nomic-embed-text（768 维）→ `kb create python-basics` 建库 → `kb search` 精确命中笔记段落
3. `run chat --tool subagent` 实测 Claude Code 被咨询（tools=1），并亲眼看到工作区权限边界拦住 F 盘路径访问
4. `deeptutor doctor` 全项 PASS；L1 轨迹确认落盘 `data/memory/trace/kb/日期.jsonl`

产出：`deeptutor/DeepTutor-小白指南.pdf`（12 页，HTML 同目录）。

## 坑与结论

| 坑 | 解法 |
|---|---|
| Clash 代理把 localhost 劫成 502 | 命令前加 `NO_PROXY=localhost,127.0.0.1` |
| init 向导对中转站 `GET /models` 无超时卡死 | Ctrl+C 后手改 `model_catalog.json` |
| Ollama 拉模型被 fake-ip DNS 拒（198.18.x.x） | 手动从 registry.ollama.ai 下 blob 放 `~\.ollama\models\blobs` |
| `deeptutor` exe 不在 PATH（用户目录 pip） | 统一 `python -m deeptutor` |

**结论**：读生产级开源项目的价值 = 看自己 langchain 实验里的最小循环在每个环节被如何加固（轮次预算、崩溃恢复、索引版本化、密钥隔离）。性价比最高的源码入口：`capabilities/subagent/tools.py`、`services/memory/paths.py`、`services/rag/pipelines/` 目录名。
