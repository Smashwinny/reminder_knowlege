# WeMM-Embedding 动手实验

本目录是 WeMM-Embedding 小白指南的配套实验材料（学习日期 2026-10-03）。

## 实验环境

- Windows 11 + Python 3.14 + Git Bash
- GPU：NVIDIA RTX 4070 12GB VRAM（实测算力足够跑 2B 模型 bf16 推理）
- 模型：tencent/WeMM-Embedding-2B（bf16，约 5.2GB）

## 文件说明

| 文件 | 说明 |
|---|---|
| `retrieval_demo.py` | 主实验脚本：5 图库 + 5 文本查询跨模态检索 + Matryoshka 截断稳定性 |
| `images/` | 图库图片（复制自 repo/docs/assets/benchmarks，FashionIQ/CIRR 等基准测试图） |
| `model/` | 从 hf-mirror 下载的模型文件（config/tokenizer/模板/权重，权重不入 git） |

## 复现步骤

```bash
pip install torch --index-url https://download.pytorch.org/whl/cu128   # CUDA 版 torch
pip install transformers==5.2.0 "qwen-vl-utils[decord]==0.0.14" sentence-transformers==5.7.0 accelerate

cd exercise/model
# 下载模型文件（国内推荐 hf-mirror 分段并发，单线程会被限速到 0.2MB/s）
for f in config.json tokenizer.json tokenizer_config.json processor_config.json \
         embedding_chat_template.jinja chat_template.jinja \
         modeling_wemm_embedding.py generation_config.json; do
  curl -sL -o $f "https://hf-mirror.com/tencent/WeMM-Embedding-2B/resolve/main/$f"
done
curl -sL -o model.safetensors "https://hf-mirror.com/tencent/WeMM-Embedding-2B/resolve/main/model.safetensors"

cd ../..
python exercise/retrieval_demo.py --model exercise/model --device cuda
```

## 实验记录

真实运行输出与结论见 `WeMM-Embedding-小白指南.pdf` 实验节。

### 已知坑

1. `pip install torch` 走默认 PyPI 拿到的是 **CPU 版**（`+cpu`，`cuda.is_available()=False`）；Windows 上 CUDA 版必须 `--index-url https://download.pytorch.org/whl/cu128`
2. README 要求 `transformers==5.2.0`，新版预处理行为可能不同
3. 权重下载单线程 ~0.2MB/s，需 range 请求分段并发提速
