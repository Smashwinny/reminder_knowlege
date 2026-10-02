---
tags: [项目笔记]
项目: abot-recon
类别: 开源项目类（流式3D重建模型，无GPU轻量实验）
完成日期: 2026-10-03
仓库: https://github.com/amap-cvlab/ABot-Recon
---

# ABot-Recon（高德万帧级流式 3D 重建）

## 这是什么

阿里巴巴高德 CV Lab 2026-08 开源的流式 3D 重建模型（arXiv 2608.27529）：**仅凭固定的 12 帧局部上下文**（当前帧 + 11 帧 KV 缓存）实时重建超长视频流——无需 COLMAP、无需相机内参、无需深度传感器，KITTI-02 上 24.45 FPS / 6.71 GiB，最大 22000 帧。代码 Apache-2.0，权重在 HF（acvlab/ABot-Recon）与魔搭。标志性 demo：北京三环一万帧"一镜到底"重建。

## 架构一句话

Pi3 点图骨架（DINOv2 编码 + 因果窗口解码，[[点图与前馈重建]]）+ 钉死 12 帧的滑动 KV 窗口（[[流式滑窗与O(1)状态]]）+ 相对位姿头（quat + 运动-视觉旋转精修器，≤2° 因果修正）+ 可选回环（DINOv2-SALAD 检索重访帧 → 稀疏位姿图优化，[[漂移与回环闭合]]）。

## 引入的概念

- [[点图与前馈重建]] — DUSt3R→Pi3 一脉：一次前向出 3D，内参焊进权重
- [[漂移与回环闭合]] — 接力估计误差无界累积，回环硬约束清账
- [[流式滑窗与O(1)状态]] — O(N)→O(1) 的显存账本（22000帧 KV：1631.5 GiB → 911 MiB）

## 实验做了什么（本机 Windows 11 纯 CPU 实测）

1. **环境**：Python 3.12 venv + torch 2.5.1 CPU + `pip install -e .`，`import abot_recon` 通过
2. **官方测试套件**：`pytest -q` → **49 passed, 7 skipped**（跳过项全是 CUDA/真实权重集成；坑：pytest 临时目录权限，加 `--basetemp` 解决）
3. **绕三环漂移仿真**（exercise/exp1_pose_drift.py，纯 numpy）：每帧航向误差 0.05° 随机游走，1 万帧终点漂 203 m、5 万帧 735 m；每圈回环清账后终点恒 3 m——误差无界 vs 有界
4. **显存账本**（exercise/exp2_kv_memory.py）：按仓库真实参数（720 token/帧×36层×bf16）实算，全局注意力 22000 帧 KV 1631.5 GiB vs 12 帧滑窗 911.2 MiB，省 1833 倍；实测 `local_window_frames=11` 被 config 校验拒绝

## 坑与结论

- 官方推理环境 Linux + CUDA 12.1；CPU 跑不动网络前向，但测试/仿真/代码走读全程无 GPU 可做
- pytest 在 Windows 沙箱下默认 basetemp 会权限报错
- 输出是点云+位姿，不是高斯——可与 [[高斯泼溅3DGS]] 管线衔接（PLY 当高斯初始化）
- 评测协议在 `eval` 分支、训练代码在 `train` 分支（2026-09-25，18 数据源混合训练）
- 无 GPU 体验入口：HF Space 与魔搭在线 Demo；社区已移植 Axera AX650N NPU

## 产出

- 指南：`abot-recon/ABot-Recon小白指南.pdf`（+ abot_recon_guide.html 源文件）
- 实验：`abot-recon/exercise/`（exp1_pose_drift.py、exp2_kv_memory.py、.venv）

**首次接触**：抖音"未来注释员"视频（拾遗 task c5d1b7b6），文案"只用12帧画面重建1万帧3D场景"
