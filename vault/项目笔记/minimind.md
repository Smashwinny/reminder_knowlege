---
tags: [项目笔记]
项目: minimind
链接: "https://github.com/jingyaogong/minimind"
类别: 开源项目类
状态: 已学完（2026-10-03）
---

# minimind —— 3 块钱 2 小时从零训出自己的大模型

**这是什么**：jingyaogong/minimind，56,800+ Star、Apache 2.0 的「最小白 LLM 训练全链路」开源教程+代码库。把 GPT 全套核心算法（分词器、Transformer、预训练、SFT、LoRA、DPO/PPO/GRPO/CISPO、蒸馏、MoE）用纯 PyTorch 手写一遍，模型仅 64M 参数（GPT-3 的 1/2700），单张消费级显卡几小时可从头训完。核心理念："用乐高自己拼飞机，远比坐头等舱（调 API）更让人兴奋"。

**带来的概念**：
- [[从零预训练CausalLM]] —— 主实验真实验证的管线（next-token prediction + 交叉熵）
- [[BPE分词器]] —— 6400 词表 minimind_tokenizer，实测中文整词成 token
- [[RoPE旋转位置编码]] —— `precompute_freqs_cis` 手写实现，YaRN 外推 32768
- [[MoE混合专家]] —— `--use_moe 1` 一键切换，198M-A64M
- [[知识蒸馏]] —— 软标签暗知识；项目还反向用大模型合成 SFT 数据
- [[RLHF偏好对齐]] —— DPO/PPO/GRPO/CISPO 手写全套

**实验做了什么**（本机 RTX 4070 12G，全程真实运行）：
1. 魔搭流式采样 `pretrain_t2t_mini.jsonl` 前 2 万条（15MB，源文件 1.2GB）→ `exercise/dataset/pretrain_sample.jsonl`
2. Tokenizer 实测：`'人工智能正在改变世界。MiniMind is tiny!'` → 中文整词 5 token + 英文 BPE 子词 10 token
3. **真实预训练 1 epoch / 625 步 / 约 4 分钟**（batch 32，cosine lr 5e-4，显存峰值 10.2GB）
   - loss 曲线（每 20 步一个点，完整见 exercise/pretrain_log.txt）：7.3609(20) → 6.1104(100) → 5.2609(200) → 4.8012(300) → 4.4536(400) → 4.2041(500) → **3.9138(625)**；随机瞎猜起点 ln(6400)≈8.77
   - 曲线形态健康：快速下降后趋缓，抖动正常
4. 生成验收（`eval_llm.py --weight pretrain`）：连续输出真实中文 token、不崩溃；语义"神智不清"但符合 625 步小样本预期，完整数据+多 epoch 即 README 演示水平

**坑与结论**：
- transformers 5.x 已兼容（作者代码内置 meta-device 下重算 RoPE 缓冲区的适配），无需降级 4.57
- Windows 输出重定向块缓冲：日志要等进程退出才完整落盘，耐心等 exit
- **并发教训**：并行 worker 的 `git add -A` 曾把本任务未提交文件卷入它的提交（b737955），137MB 权重 .pth 被误提交——已 `git rm --cached` 并在 .gitignore 补 `minimind/exercise/out/`、`minimind/exercise/dataset/`
- 训练成本公式 ≈ 6×参数量×token 数：64M 小模型个人可训的根源，也是理解大模型训练费的钥匙

**产出**：`minimind/MiniMind-小白指南.pdf`（13 问彩色指南 + 6 步真实实验，23 页）
