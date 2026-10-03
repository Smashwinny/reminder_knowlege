---
tags: [项目]
类别: 知识学习类（抖音技术视频还原 + 本地真机实验）
上游仓库: https://github.com/hiyouga/LLaMA-Factory（ce9dc9e，实际安装 PyPI 官方包 llamafactory 0.9.5）
完成日期: 2026-10-03
---

# llamafactory-ft

**这是什么**（一句话）：把抖音视频《配环境三天？浏览器点几下就能微调大模型》（作者"大书大"）的技术主线还原成可动手项目——视频方案是云端 Jupyter + LLaMA-Factory + QLoRA；本实验反其道在本地 RTX 4070 上真实跑通 LoRA 微调：给 Qwen2.5-1.5B 换身份"小拾"，训练前后同一批问题对比验证。

**它给我什么能力**：改身份/人格、固化输出格式、领域小模型定制、低成本验证微调需求、云端白嫖算力（Colab/DSW/ModelScope）、adapter 几 MB 资产化入库。

**引入的概念**：
- [[LoRA低秩适配微调]]（ΔW=B·A 低秩补丁，训练量千分之一）
- [[QLoRA量化微调]]（NF4 4bit 基座 + 分页优化器，48GB 训 65B）
- [[SFT监督微调]]（Alpaca 三件套示范课，identity 最小可验证实验）
- 激活旧概念：[[量化与GGUF]]（同思想两用）、[[KV缓存与上下文]]（显存账单思维）、[[证据优先质检ProofOverClaims]]（原题复现才算数）、[[ollama]]（adapter→GGUF 部署路线）

**实验记录**（全部真实跑通，venv：Python 3.12 + torch 2.14.1+cu126 + llamafactory 0.9.5）：
- 环境自检 `llamafactory-cli env` 全绿（GPU 4070 11.99GB）
- 基线（logs_baseline.txt）：5 问均自称 Qwen/阿里云
- 训练（logs_train.txt）第 3 次成功：12 epochs=60 步，loss 3.51→0.004，train_runtime 20.43s；可训练参数 9,232,384/1,552,946,688=**0.59%**；adapter 实测 36,981,072 字节≈**35MB**（基座 3GB 的 1.2%）
- 验证（logs_after.txt / logs_probe.txt）：身份 5 问全部改口"小拾"且细节准确（Qwen2.5-1.5B/LLaMA-Factory/RTX 4070）；通用题（支持哪些语言）正常；训练集原题逐字复现；注入干扰（"请忽略之前的问题"）仍答"我叫小拾"
- **坑 1**：llamafactory 0.9.5 国内镜像环境变量是 **USE_MODELSCOPE_HUB**（旧教程写 USE_MODELSCOPE），写错会默默走 HuggingFace 直连，下载假死无报错
- **坑 2**：Alpaca 数据集 .json 里写注释行 → datasets/pyarrow 报 JSON parse error row 0，数据文件必须纯 JSON
- **坑 3（最有教育意义）**：2~3 epochs（10~15 步）"训不动"——loss 4.15→2.36，模型自称"Qwen-7B 0307"胡说。诊断靠"训练集原题探针"（问"这个实验用了什么硬件？"连教材都背不出=步数不够）；对照实验（官方 91 条 identity 数据集 68 步 loss→0.64）排除后端嫌疑；12 epochs（60 步）后 loss 砸到 0.004。根因：自造答案罕见 token 多（Qwen2.5-1.5B-Instruct/LLaMA-Factory），初始 loss 4.0 远高于官方案例 2.5，需更多步
- 另：CLI 直跑不传 YAML 时 dataset_dir 默认相对路径 data\ 找不到 dataset_info.json；PyPI wheel 不自带 data 目录（用 repo/data）

**后续可深入的方向**：QLoRA 4bit 版同实验（quantization_bit: 4 两行改动）；lora_rank 8→32 对照实验；导出 GGUF 接 [[ollama]]；WebUI（llamafactory-cli webui）全程鼠标操作； held-out 考试题验证"学会 vs 背下来"。
