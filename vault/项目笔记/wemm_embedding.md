---
tags: [项目笔记]
项目: wemm_embedding
类别: 开源模型类
日期: 2026-10-03
状态: 已学完
---

# wemm_embedding

## 这是什么

腾讯微信视觉组开源的通用多模态 embedding 模型系列（WeMM-Embedding 2B/4B/9B，arXiv:2608.24053，Apache 2.0），基于 Qwen3.5 单塔多模态架构，把文/图/视频/视觉文档/交错输入统一编码进共享向量空间。已大规模部署于微信视频号、公众号、朋友圈搜索与电商推荐，日调用量 10 亿量级。9B 登顶 MMEB-v2（80.6），2B（77.9）超过此前领先的 8B 开源模型。

- 仓库：https://github.com/Tencent/WeMM-Embedding
- 权重：HuggingFace `tencent/WeMM-Embedding-{2B,4B,9B}`（国内用 hf-mirror 加速）

## 带来的概念

- [[多模态嵌入模型]] — 本项目主角：单塔 VLM + `<embedding>` token 抽向量
- [[Matryoshka套娃嵌入]] — 64~4096 维自由截断，normalize(emb[:d]) 两行降维
- [[对比学习]] — 拉正推负 + in-batch negatives + 跨尺度知识蒸馏
- [[混合线性注意力]] — 3 线性 + 1 全注意力循环，config.json layer_types 实证
- 关联已有：[[向量与Embedding]]、[[余弦相似度]]、[[向量数据库]]、[[RAG检索增强生成]]

## 实验做了什么

本机 RTX 4070 12GB + Python 3.14 真实推理 2B 模型（bf16，5.2GB）：
1. 分析 config/tokenizer/chat template（混合注意力 3:1、GQA 8/2、词表 248078、Matryoshka 维度表）
2. `exercise/retrieval_demo.py`：5 张图库 + 5 条文本查询做跨模态检索，余弦相似度排序
3. Matryoshka 截断稳定性：同一查询在 64→2048 维下 Top-1 对比
脚本与真实输出：[[../wemm-embedding/exercise/retrieval_demo.py]]（详见 PDF 指南实验节）

## 坑与结论

- **下载坑**：huggingface.co 直连与 hf-mirror 单线程均被限速到 ~0.2MB/s，分段并发（range 请求 + 多线程）有效；ModelScope 无此模型
- **版本坑**：README 明确要求 transformers==5.2.0，新版预处理行为可能不同；modeling 代码注释提到 <5.15 有 rope_deltas 缓存 bug
- **铁律**：入库与查询必须同一模型同一 chat template，`<embedding>` 位置错位 = 坐标系歪
- **诚实限制**：MMEB 分数为作者自评；音频不支持；5 图小实验只验证排序方向，不复现榜单
- **选型结论**：个人/小团队用 2B（消费级显卡可跑），Apache 2.0 可商用，可平替闭源 embedding API
