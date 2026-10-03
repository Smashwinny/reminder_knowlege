---
tags: [概念]
领域: AI / 大语言模型
别名: ["Tokenizer", "分词器", "BPE", "Byte Pair Encoding", "ByteLevel BPE"]
首次来源: "[[项目笔记/minimind]]"
---

# BPE分词器

**一句话定义**：LLM 的"词典+翻译官"——把自然语言文本切成离散 token 并映射为整数 id（编码），模型输出 id 后再查表换回文本（解码）；BPE（字节对编码）是其主流训练算法：从单字符出发，反复合并最高频相邻片段，直到词表达到目标大小。

**属于领域**：AI / 大语言模型（所有 NLP/LLM 的输入输出层）

**通俗理解**：模型只会做矩阵运算，不认识汉字。分词器在"文字 ↔ 数字"之间当翻译：英文按"子词块"切（unbelievable → un/believ/able），中文常整词成 token（"人工智能" = 1 个 token）。词表就是一本有固定页数的词典，6400 页 vs 15 万页是设计取舍。

**关键事实**（MiniMind 实测）：
- MiniMind 词表仅 6400（vs Qwen2 15 万、Llama3 12.8 万）：嵌入层参数 = 词表 × 隐藏维度，小词表让小模型不"虚胖"；代价是编码效率略低
- 特殊标记：BOS（句首）/ EOS（句尾）/ PAD（填充对齐），训练标签里 PAD 位置用 -100 屏蔽
- 词表大小决定随机瞎猜的 loss 起点 = ln(词表)（6400 → 8.77）
- 跨 tokenizer 比较模型质量时 PPL 失真，BPB（Bits Per Byte）更公平
- 实测分词：`人工智能正在改变世界。` → `[2225, 3593, 2886, 1950, 302]`，整词成 token；`MiniMind` → `M/in/i/M/ind`，BPE 子词

**与已有概念的关联**：
- [[从零预训练CausalLM]]：预训练前必经的切词步骤；[[向量与Embedding]]：id 查表变成向量的下一步
- [[KV缓存与上下文]]：token 数是上下文预算的单位

**首次接触于**：[[项目笔记/minimind]]（minimind 自带 6400 词表 minimind_tokenizer）
