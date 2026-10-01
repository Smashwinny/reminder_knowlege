---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/qdrant/qdrant
完成日期: 2026-10-01
---

# vector_database_qdrant

**这是什么**（一句话）：Qdrant（读作 quadrant）是 Rust 写的生产级向量数据库——按"语义相似"而非"字面精确"来检索数据的服务。

**它给我什么能力**：
- 本地向量数据库服务（单二进制 30MB，REST :6333 / gRPC :6334，免 Docker）
- 中文文本 → 512 维向量（fastembed + BAAI/bge-small-zh-v1.5，本地 CPU，无需 API key）
- 建集合 / upsert / 语义搜索 / payload 过滤搜索完整链路
- RAG 知识库的存储层（官方有 langchain-qdrant 集成包）

**引入的概念**：
- [[向量与Embedding]]
- [[余弦相似度]]
- [[向量数据库]]（Collection / Point / Payload 概念体系 + 选型对比）
- [[HNSW近似最近邻索引]]
- [[RAG检索增强生成]]
- [[向量量化]]

**实验记录**（exercise\ 目录，全部已验证）：
- exp1_ingest.py：16 部电影简介 → 向量入库，集合状态 green
- exp2_search.py：语义 vs 关键词对比——3 个"字面零重合"的查询，关键词搜索 0 命中，语义搜索 Top1 全对（黑客帝国 0.67 / 星际穿越 0.63 / 阿甘正传 0.46）
- exp3_filter.py：过滤搜索——加 genre=动画 后盗梦空间出榜换你的名字；科幻+year≥2015 只剩流浪地球2
- 产出：`Qdrant向量数据库-小白指南.pdf`（17 页，12 疑问 + 6 步实验）

**坑与结论**：
- Clash 代理劫持 localhost → qdrant-client 报 502；`setx NO_PROXY "localhost,127.0.0.1"` 解决
- ollama 拉 nomic-embed-text 被 Clash fake-IP 劫持 DNS（198.18.x.x 非公网）拉不下来；改用 fastembed
- 官方 Windows 二进制不带 Web UI（/dashboard 404），Docker 版才有；用 REST API 替代
- qdrant-client 1.19 重构了内置 embedder API（无 set_model），直接用 fastembed 库更稳
- Git Bash 里 curl 走代理对 localhost 返回空；验证用 PowerShell / Python

**后续可深入的方向**：
- langchain-qdrant 接入：把今天的 movies 集合变成 langchain RAG 的 retriever
- 混合搜索（dense + BM25 sparse + RRF 融合）
- 给 crewai/langgraph 的 agent 加向量长期记忆
- 以文搜图（CLIP embedding）相册
