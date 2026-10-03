---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/TianyuCodings/NanoJev (MIT)
完成日期: 2026-10-03
---

# nanojev

**这是什么**（一句话）：0.6B 开源 Jev/System One 决策模型复刻——Qwen3-0.6B 基座拆掉 LM head 换标量决策头，state+question+candidates 进、完整概率分布出，零输出 token 解码；权重/数据/训练管线全开源（HuggingFace C-Tianyu/NanoJev，unified-games-v1）。

**它给我什么能力**：本机毫秒~百毫秒级判断裁判（隐私不出机、零 API 费）；2~255 动态候选 Choice + Boolean + Score 三题型；一条可照抄的"蒸馏 Jev API 分布 + RL 专家硬标签 → 混合 SFT"训练管线；给 jev-router 换真本地裁判的完整件。

**引入的概念**：
- [[决策头与非生成式读出]]（拆 LM head、候选路径 hidden→标量→softmax，60 行 DecisionModel）
- [[动态候选与集合敏感]]（set-attention + log K；顺序不变集合敏感；OOD 候选不免疫）
- 关联已有：[[SystemOne决策模型Jev]]（本体，闭源）、[[逐轮模型路由与哨兵代理]]（合体路线）、[[知识蒸馏]]（迷宫/蛇目标=Jev 分布蒸馏）

**实验记录**（2026-10-03，RTX 4070 12G，全部真实运行）：
1. `ex1_decision_hello.py`：官方 test.jsonl 第一条迷宫状态，一次前向三题型（Choice/Bool/Score）同出；概率归一断言过；autoregressive_decode_steps=0；显存 2.23 GiB；候选顺序打乱 5/5 同一赢家（排列不变）。Choice 选 south(0.368)，p_true=0.944，风险期望 1.98
2. `ex2_dynamic_candidates.py`：候选 2→12 扫描，赢家随集合变化（2→north 0.90 / 4~8→south / 12→scan 反超）——集合敏感实证；混入 dig/teleport/pray 坏候选分走 35% 概率——OOD 不免疫实证（与直觉相反，如实记录）
3. `ex3_test_accuracy.py`：官方 unified/hard/test.jsonl 分层抽样 927 题（迷宫 211 全量 + 蛇 116 全量 + Basic 300 + Predict Position 300）本机推理 894.6s，decode_steps=0；题目级 top-1 一致率：迷宫 72.5% / 蛇 88.8% / Basic 78.7% / PP 74.3% / 总计 77.1%（对照目标：射击=专家动作硬标签，迷宫蛇=Jev API 分布 argmax）。注：全量 2496 题首跑因 fp32/no-TF32 超 40 分钟被后台时限杀，改分层抽样重跑成功；长序列行（50×50 迷宫/Predict Position）吃掉约 86% 时间
4. 仓库自带 `test_question_contract.py` 17/17 全过（无需 GPU：id 不进输入/问题隔离/分词锁定等契约）

**坑**：
- torch 2.11 无 `torch._native.triton_utils`（2.14 新增），DecisionPredictor 的 `--disable-native-triton` 直接 ModuleNotFoundError → exercise/nj_loader.py 用 sys.modules 打桩（deregister 本为空操作，语义安全）
- 官方推理入口硬要求 CUDA（`device.type != "cuda"` 直接 ValueError），推文"2GB RAM 可跑"需自改 CPU 路径
- fp32 加载 + allow_tf32=False，全量推理慢（2496 题数十分钟）；显存峰值 11.8 GiB 贴近 12G 卡上限
- README"Basic 128/128 超 Jev 56/128"为作者自报口径，勿当独立验证事实引用

**后续可深入的方向**：照 build_toy_decisions.py 造自己的路由/审稿判断数据集微调；把 serve_decisions.py 接进 jev-router 替换 mock 裁判（需 sitecustomize 打桩 triton 坑）；CPU 推理改造验证"2GB RAM"；FlexAttention/共享前缀推理（repo 路线图）。

源头：https://x.com/yulmu_coffee/status/2100920275475042443（韩语推文，율무커피："고작 0.6B짜리 판단 모델 NanoJev…2GB RAM만 있어도 돌"）
产出：`nanojev/nanojev-小白指南.pdf`（12 问 8 SVG 3 实验）
