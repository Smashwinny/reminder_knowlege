---
tags: [概念]
领域: AI / 大语言模型
别名: ["MoE", "Mixture of Experts", "混合专家模型"]
首次来源: "[[项目笔记/minimind]]"
---

# MoE混合专家

**一句话定义**：把 Transformer 前馈网络从"全体 token 共用一个网络"换成"N 个并行专家 + 一个路由器"，每个 token 只被路由给最相关的 top-k 个专家处理——总参数量（容量）大涨，但每个 token 的激活参数（算力）不变。

**属于领域**：AI / 大语言模型（架构稀疏化；DeepSeek-V3、Mixtral、Qwen3-MoE 同款思想）

**通俗理解**：综合医院 vs 全科医生。Dense 模型是全科医生，什么病都看同一个脑子；MoE 是医院，挂号处（路由器 gate）按病情分诊到心内科/骨科…（专家）。医院总专家很多（参数大），但每个病人只看一两个科室（激活少）。

**关键事实**（MiniMind `--use_moe 1` 实测源码）：
- MiniMind-3-MoE：198M 总参 / 仅 64M 激活（≈Dense 版算力，3 倍容量）
- 路由：softmax 打分 → top-k 选专家 → 加权合并；k=1 时权重恒为 1（straight-through 技巧传梯度）
- 负载均衡损失（aux_loss）：防止所有 token 挤去同一个专家，loss 里加 `router_aux_loss_coef × Σ(load × prob)`；预训练日志里的 aux_loss 字段就是它（Dense 时为 0）
- 代价：显存装全部专家、推理批量小时专家利用率低、训练稳定性更挑超参

**与已有概念的关联**：
- [[从零预训练CausalLM]]：前馈层是它的可替换部件；[[RLHF偏好对齐]]：MoE 模型同样要做对齐训练

**首次接触于**：[[项目笔记/minimind]]（jingyaogong/minimind 一键 MoE 切换）
