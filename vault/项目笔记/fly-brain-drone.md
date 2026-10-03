---
tags: [项目]
类别: 开源项目类（连接组仿真 / 科研复刻，抖音视频溯源）
上游仓库: philshiu/Drosophila_brain_model + ClutchMedia775/fly-brain-drone
完成日期: 2026-10-03
---

# fly-brain-drone（果蝇大脑开无人机）

**这是什么**：把 FlyWire v783 果蝇全脑连接组（138,639 神经元）按 Shiu et al. 2024 的 LIF 模型跑成脉冲网络，接到仿真四旋翼上——零训练、零飞行代码，大脑自己会躲障碍。抖音"阿博粒"视频的海外源头是开发者 @c10ned 的 FPV 无人机仿真实验（The Neuron 2026-09-15 报道）。

**它给我什么能力**：
- 复现/操作一个 Nature 级全脑仿真（参数、动力学、驱动方式全开源）
- pandas 处理 1500 万行级连接组数据的实战（查通路、算度分布、BFS 可达性）
- 一套机制归因对照实验模板（real/shuffle/rand/nobrain × n=20 × CI × 消融）
- 从短视频溯源到论文+官方代码的完整查证路线

**引入的概念**：
- [[FlyWire全脑连接组]]
- [[LIF全脑仿真]]
- [[布线特异性与零训练涌现]]

**实验记录**（exercise/，全部真机运行）：
- ex1 连接组解剖：v783=138,639 神经元/15,091,983 边；糖→MN9 直接突触 0 条，2 跳可达；shuffle 后 2 跳可达仍 20/20 → 特异性在强度不在可达性
- ex2 numpy 手写全脑 LIF（127,400 神经元，23s/次）：基线 0Hz / 真实布线 MN9 102Hz / 打乱布线 0Hz。坑：t_mbr(20ms) 与 tau(5ms) 混用整脑静默；PoissonInput 直打 v 非打 g；CSR 出边索引按 presynaptic 排序（接错则传导全断）
- ex3 飞行日志取证：有脑避障 1.98/1.80m vs 无脑 0m 撞毁；首次响应 0.12s；官方 n=20：real 100% vs shuffle 0~50%；消融显示单 DN 冗余、全摘转向读出才失效
- 边界：本机无 conda，Brian2 完整复刻留 WSL2；"91% 上传大脑"说法不实，91% 是神经响应吻合率

**后续可深入的方向**：WSL2 + Brian2+Cython 完整复刻全脑飞行（3.5s≈20s 墙钟）；MaleCNS 雄蝇连接组跨数据集验证；erojasoficial-byte/fly-brain 的 MuJoCo 具身行为（走/理毛/逃逸）；把 ex2 扩展成 looming 输入的迷你避障。
