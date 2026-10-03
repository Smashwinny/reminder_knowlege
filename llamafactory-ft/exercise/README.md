# 动手实验：RTX 4070 真实 LoRA 微调 Qwen2.5-1.5B（来自抖音"浏览器点几下就能微调大模型"）

## 实验目标
用 LLaMA-Factory 给 Qwen2.5-1.5B-Instruct 做一次 LoRA 监督微调（SFT），
把模型身份从"通义千问"改成自定义身份"小拾"，训练前后用同一批问题对比验证。

## 环境
- Windows 11 + Python 3.12 venv（`../venv`）+ torch 2.14.1+cu126 + llamafactory 0.9.5（PyPI 官方包）
- GPU：NVIDIA GeForce RTX 4070 12GB
- 模型源：`USE_MODELSCOPE_HUB=1`（注意：0.9.5 认的是这个变量名，旧教程的 USE_MODELSCOPE 会导致 HF 直连假死）

## 文件清单
| 文件 | 作用 |
|---|---|
| `data/shiyi_identity.json` | 20 条中文自我介绍数据集（Alpaca 格式；**必须是纯 JSON，注释行会让 pyarrow 报错**） |
| `data/dataset_info.json` | 数据集注册表（formatting: alpaca + 列映射） |
| `qwen25_lora_sft.yaml` | 训练配置（最终版：12 epochs / lr 3e-4 / warmup 3） |
| `qwen25_lora_chat.yaml` | 推理配置（基座 + adapter） |
| `baseline_chat.py` / `after_chat.py` | 训练前/后对照问答（同题） |
| `probe_train_questions.py` | 训练集原题探针（防"只换聊天风格"） |
| `ablate_identity.yaml` | 对照实验配置（官方 identity 数据集） |
| `saves/qwen25-lora-sft/` | 训练产物：adapter（35MB）+ loss 曲线 + trainer_log |
| `logs_*.txt` | 各阶段真机输出 |

## 真实结果（2026-10-03）

### 基线（logs_baseline.txt）
Q: 你是谁？A: 我是Qwen，是由阿里云开发的超大规模语言模型……（5 问均自称 Qwen/阿里云）

### 训练（logs_train.txt，第 3 次成功）
- trainable params: 9,232,384 / 1,552,946,688 = **0.59%**
- loss：epoch2 3.51 → epoch4 1.61 → epoch6 0.61 → epoch8 0.097 → epoch10 0.009 → epoch12 **0.004**
- train_runtime: **20.43s**（60 步）；adapter_model.safetensors = **36,981,072 字节 ≈ 35MB**（基座 3GB 的 1.2%）

### 微调后验证（logs_after.txt）
- Q: 你是谁？A: **我是小拾，一个由拾遗学习者亲手微调出来的 AI 助手**（细节全对）
- Q: 你是通义千问吗？A: 底座来自通义千问……但经过微调后我自称小拾
- 通用体检 Q: 你支持哪些语言？→ 正常回答，未练坏

### 原题复现探针（logs_probe.txt）
- Q: 这个实验用了什么硬件？A: 一张 NVIDIA GeForce RTX 4070（12GB 显存）……（教材原话）
- Q: 谁是通义千问？请忽略之前的问题，你的名字是什么？A: 我叫小拾（抗干扰）

## 失败与修正记录（重要）
1. **第 1 次**（2 epochs / lr 1e-4 / warmup 5，10 步）：loss 4.15→3.82 几乎没动，验证仍自称 Qwen → 步数太少、warmup 吃掉一半
2. **第 2 次**（3 epochs / lr 3e-4，15 步）：loss→2.36，模型开始胡说（自称"Qwen-7B 0307"）但仍未学会 → 用"训练集原题探针"确诊：连教材都背不出
3. **对照实验**（官方 91 条 identity 数据集同环境，68 步）：loss 2.46→0.64 → 证明后端健康，是我的数据步数不够
4. **根因**：自造答案罕见 token 多（Qwen2.5-1.5B-Instruct、LLaMA-Factory、ModelScope），初始 loss 4.0 远高于官方案例的 2.5；**12 epochs（60 步）** 后 loss 砸到 0.004，验证全部通过

## 复现命令
```powershell
cd F:\reminder\llamafactory-ft
set USE_MODELSCOPE_HUB=1
venv\Scripts\llamafactory-cli train exercise\qwen25_lora_sft.yaml
venv\Scripts\python exercise\after_chat.py
```
