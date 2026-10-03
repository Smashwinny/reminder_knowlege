# MiniMind 动手实验记录（本机 RTX 4070 12G 真实运行，2026-10-03）

## 实验目标
验证 jingyaogong/minimind 的**从零预训练管线**在本机真实跑通：采样子集 → 预训练小步数 → 生成验收。不求训出好用模型，只求管线每个环节真实可用 + 诚实记录损失曲线。

## 环境
- Windows 11 + Python 3.14.7 + torch 2.11.0+cu128 + transformers 5.2.0 + datasets 5.0.1
- GPU：NVIDIA RTX 4070 12GB（训练显存峰值 10.2GB）
- 上游仓库：`repo/`（git clone --depth 1，f659b55）

## 实验步骤与真实结果

### 1. 数据采样子集（免下 1.2GB 全量）
`python download_sample.py`：从魔搭 ModelScope 流式下载 `pretrain_t2t_mini.jsonl`，取前 20000 条，仅传输 15MB。
```
DONE: 20000 samples -> dataset/pretrain_sample.jsonl, total streamed 15.0 MB
```

### 2. Tokenizer 实测（repo 自带 6400 词表）
```
原文: 人工智能正在改变世界。MiniMind is tiny!
token ids: [2225, 3593, 2886, 1950, 302, 80, 301, 108, 80, 916, 395, 297, 301, 124, 36]
逐token还原: ['人工智能', '正在', '改变', '世界', '。', 'M', 'in', 'i', 'M', 'ind', ' is', ' t', 'in', 'y', '!']
vocab_size: 6400   BOS: 1   EOS: 2   PAD: 0
```
中文整词成 token，英文 BPE 子词块。

### 3. 真实预训练（核心）
```bash
cd repo/trainer && python train_pretrain.py \
  --data_path ../../exercise/dataset/pretrain_sample.jsonl \
  --save_dir ../../exercise/out --epochs 1 --batch_size 32 \
  --accumulation_steps 1 --log_interval 20 --save_interval 200 --num_workers 4
```
- 模型：**63.91M 参数**（hidden 768 × 8 层，Dense）
- 20000 条 ÷ batch 32 = **625 步，全程约 4 分钟**

**诚实损失曲线**（每 20 步一个点，完整日志见 pretrain_log.txt）：

| step | 20 | 100 | 200 | 300 | 400 | 500 | 625 |
|---|---|---|---|---|---|---|---|
| loss | 7.3609 | 6.1104 | 5.2609 | 4.8012 | 4.4536 | 4.2041 | **3.9138** |

- 随机瞎猜 6400 词表的 loss 起点 = ln(6400) ≈ 8.77，实测从 7.36（第 20 步）一路降到 3.91
- 曲线形态：快速下降后趋缓，中段正常抖动，lr 按 cosine 从 5e-4 衰减——教科书式健康曲线

### 4. 生成验收（`eval_llm.py --weight pretrain`）
```
💬: 解释一下"光合作用"的基本过程
🧠: 是将光的重点进行说明。天空通常由风雨、水来时空调，导致气中升起着光的光线...

💬: 比较一下猫和狗作为宠物的优缺点
🧠: 。狗是猫，它们属于哺乳动物，它们有羽毛，有不同的动物，有很多动物...
```
输出是连贯的真实中文 token，格式整齐、不崩溃、不吐乱码 id——**管线全通**。语义上"神智不清"完全符合预期（625 步 × 2 万条样本仅为官方完整训练的零头，官方完整数据 + 多 epoch 即 README 演示的流畅对话水平）。

## 结论
- MiniMind 预训练管线在本机真实跑通，loss 曲线健康（7.36 → 3.91）
- 个人显卡训 LLM 的核心账：成本 ≈ 6 × 参数量 × token 数，64M 参数让小步数验证成本趋近于零
- transformers 5.x 无需降级（作者已适配）

## 坑
- Windows 输出重定向块缓冲：pretrain_log.txt 要等进程退出才完整落盘
- 大文件别进 git：`out/*.pth`（137MB）与采样数据集已在 .gitignore 排除

## 文件清单
- `download_sample.py` — 魔搭流式采样子集脚本
- `dataset/pretrain_sample.jsonl` — 2 万条预训练子集（15MB，git 忽略）
- `pretrain_log.txt` — 625 步完整训练日志
- `out/pretrain_768.pth` — 训练产物权重 137MB（git 忽略，可复训重现）
