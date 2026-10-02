---
tags: [项目]
类别: 知识学习类（清华 SLAMFormer-∞，无 GPU 轻量实验）
上游仓库: https://github.com/Tsinghua-MARS-Lab/SLAM-Former
完成日期: 2026-10-03
---

# slamformer（SLAM-Former / SLAMFormer-∞）

**这是什么**：清华赵行团队（MARS Lab）的几何 Transformer SLAM。前作 SLAM-Former（ECCV 2026，arXiv 2509.16909）把 SLAM 前端+后端+记账全塞进一个 36 层 Transformer（Pi3/DINOv2 底座，BSD-3 开源 521★，权重在 HuggingFace）；后续作 SLAMFormer-∞（arXiv 2608.03429，2026-08）用内存条件动态坐标系取消距离上限——17 公里 45 分钟城市驾驶 RGB-only 在线稠密重建，KITTI 全序列 ATE 23.0 m（VGGT-Long 26.4 m）。抖音"深蓝前沿"短视频宣传的就是 ∞ 版。

**它给我什么能力**：
- 读懂"几何基础模型"赛道 DUSt3R→VGGT→SLAM-Former→∞ 的演化主线
- 一套无 GPU 学习法：源码契约对拍 + 复杂度账本仿真，零显卡验证重量级论文的核心主张
- KV 剪枝通用套路（只剪 K/V 保 Query）、"后端=全注意力"的思想实验
- 有 GPU 时的升级路线：README 四条命令复现 TUM/KITTI 推理

**引入的概念**：
- [[首帧锚定与内存条件坐标系]]
- [[KV剪枝与多样性保留]]
- [[注意力即优化器]]

**实验记录**（无 GPU，全部真实运行）：
1. `exercise/contract_check.py` —— 论文承诺 vs 源码实现逐条对拍，**18/18 PASS**（retention_ratio=0.5、DivPrune、_prune_idx_cache、ConvHead、bn_every=10、local_points/conf/camera_poses、Pi3-DINOv2、BSD-3、HF 权重、∞ 链接…）。坑：论文术语 pointmap ≠ 代码变量名 local_points，首跑 17/18，修正术语后全过——"论文语言≠代码语言"是读研代码第一课。
2. `exercise/kv_ledger_sim.py` —— KV 内存账本仿真（numpy+matplotlib）：12,000 帧（≈17km）不剪枝 31.0 GiB / γ=0.5 15.5 GiB / 动态 log 池 36.2 MiB（879x）；100,000 帧 260.9 GiB vs 44.4 MiB（6021x）。结论：恒定 γ 只折斜率，动态 log 池才是"无距离上限"的数学前提。图：exercise/kv_ledger_sim.png。

**坑与结论**：
- SLAMFormer-∞ 官方仓库是**占位仓库**（仅 README+BibTeX，2 commits，65★），代码未放；能跑的开源载体是前作 SLAM-Former
- SLAM-Former 推理强依赖 CUDA（demo.py 直接 .to('cuda')），本机无 GPU 不硬跑；评测需 `--retention_ratio 1`（issue #15）
- 训练只用 12 帧/批（32×A100 训 11 小时），测试 1.2 万帧——训练/使用分布差三个数量级是这条技术路线的普遍痛点

**产出**：SLAMFormer-Inf-小白指南.pdf（8 页彩色）+ slamformer_guide.html + exercise/
