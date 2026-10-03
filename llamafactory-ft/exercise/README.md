# 动手实验：RTX 4070 真实 LoRA 微调 Qwen2.5-1.5B（来自抖音"浏览器点几下就能微调大模型"）

## 实验目标
用 LLaMA-Factory 给 Qwen2.5-1.5B-Instruct 做一次 LoRA 监督微调（SFT），
把模型身份从"通义千问"改成自定义身份"小拾"，训练前后用同一批问题对比验证。

## 文件清单
| 文件 | 作用 |
|---|---|
| `data/shiyi_identity.json` | 20 条中文自我介绍数据集（Alpaca 格式：instruction/input/output） |
| `data/dataset_info.json` | 数据集注册表（告诉 LLaMA-Factory 去哪读、什么格式） |
| `qwen25_lora_sft.yaml` | 训练配置：LoRA + bf16 + 2 epochs |
| `qwen25_lora_chat.yaml` | 推理配置：基座 + LoRA adapter |
| `saves/qwen25-lora-sft/` | 训练产物（LoRA adapter + loss 曲线图） |
| `logs_baseline.txt` / `logs_train.txt` / `logs_after.txt` | 三个阶段的真机输出 |

## 实验步骤

### 0. 环境
- Windows 11 + Python 3.12 venv + torch 2.14.1+cu126 + 官方 PyPI `llamafactory[torch,metrics]`
- GPU：NVIDIA GeForce RTX 4070 12GB
- 模型下载：`set USE_MODELSCOPE=1`（走 ModelScope 国内镜像，免 HF 访问问题）

### 1. 基线测试（训练前）
```powershell
./venv/Scripts/python.exe -c "from llamafactory.chat import ChatModel; ..."
```
问"你是谁"，记录原始回答（预期：自称通义千问）。

### 2. 训练
```powershell
./venv/Scripts/llamafactory-cli train exercise/qwen25_lora_sft.yaml
```

### 3. 微调后测试
加载 adapter 再问"你是谁"，对比回答是否变成"小拾"。

## 真实输出记录
（本文件在实验全部跑完后由 worker 回填真实结果）
