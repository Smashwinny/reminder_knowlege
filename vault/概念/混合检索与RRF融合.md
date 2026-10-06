---
tags: [概念]
领域: AI / 检索
别名: [混合检索, Hybrid Search, RRF, 倒数排名融合, MMR, 多通道召回]
首次来源: "[[项目笔记/memmy]]"
---

# 混合检索与RRF融合

**一句话定义**：用向量、全文（FTS5）、字面 pattern、结构化片段多条通道并行召回，再把"各通道最好分 + 层质量加成 + 倒数排名融合（RRF）共识加成"合成一个 relevance 分，最后过相对阈值、MMR 去冗余、LLM 终筛的检索架构。

**属于领域**：信息检索 / RAG 工程

**通俗理解**：像"**招人既看简历关键词又看面试印象**"。纯向量检索是"只看面试印象"——换词能懂但精确标识符（PYTHONUTF8、错误码）抓瞎；纯关键词是"只筛简历字面"——换个说法就漏。混合检索让两类考官各自打分，<span style="background:#FFD600;font-weight:bold">RRF 给"多位考官都点名"的候选人加分</span>（公式 `0.4×Σ1/(60+名次+1)`），MMR 再按 `0.7×相关性−0.3×冗余` 选人，避免录取十个一模一样的。Memmy 的实测漏斗：raw 24 条 → 融合 ranked 6 → 阈值砍 18 → LLM 终筛留 4。**坑**：终筛 LLM 太弱（qwen2.5:0.5b）会误杀正确结果，宁可不设或换强模型。

**与已有概念的关联**：
- 相关：[[RAG检索增强生成]]（混合检索是 RAG 召回环节的主流强化）
- 相关：[[向量数据库]] / [[HNSW近似最近邻索引]]（向量通道的底层；Memmy 用轻量 sqlite-vec 而非独立向量库）
- 相关：[[余弦相似度]]（向量通道的打分基础）
- 同构：[[数据源降级链]]（LLM 终筛失败自动回退机械 top6——单通道故障不致命）

**首次接触于**：[[项目笔记/memmy]]

## UI UX Pro Max：词法排序与多域调用分别识别（2026-10-05）

[[项目笔记/github_tools_increment]] 的 [[BM25词法相关性排序]] 是单语料词法打分部件；设计建议生成路径按 product、product、style、color、landing、typography 顺序做六次搜索调用。五个不同域不等于五路并行 AI，也没有因此实现本笔记中的向量通道、RRF、MMR 或 LLM 终筛。

已有 192 行公式对拍只验证固定输入下的 BM25 分数与次序；最终入口还受域路由、字段选择、身份匹配、阈值和回退影响。它与 [[RAG检索增强生成]] 相关，但本次检索后是规则组装，不是调用大模型生成。Memmy 原有漏斗与测试数量保持原项目口径，不用于为此项目背书。

来源：[固定检索实现](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/477bcb28c9812b385cb51a4605ddf30d7b2266e2/src/ui-ux-pro-max/scripts/core.py)、[设计组装实现](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/477bcb28c9812b385cb51a4605ddf30d7b2266e2/src/ui-ux-pro-max/scripts/design_system.py)；[历史实验日志](../../github_tools_increment/delivery/UIUX增量学习_实验日志.txt)。
