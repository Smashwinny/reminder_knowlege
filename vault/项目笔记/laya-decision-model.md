---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/NandhaKishorM/laya (Apache-2.0, 30k+★)
完成日期: 2026-10-03
---

# laya-decision-model

**这是什么**（一句话）：Jev 的开源平替——非自回归 System 1 决策引擎，单次前向输出带校准概率的 choice/score/noul 结构化决策，421M 参数 CPU 就能本地跑（暖态 ~250ms/题，官方 GPU 33ms）。

**它给我什么能力**：本地毫秒级判断层（路由/分诊/审核/护栏），数据不出机器；自建带标准答案考卷的"本地 vs 云端"评测范式；决策模型版提示词工程（criteria 措辞）；置信度门控与弃权阈值拟合工具链。

**引入的概念**：
- [[非自回归决策模型]]（单次前向 vs 逐 token 生成；checkpoint 路由；英文 checkpoint 非英语塌方）
- [[RLCD与严格合规评分规则]]（严格合规评分规则=撒谎不划算的打分表，逼出诚实概率）
- [[概率校准与温度缩放]]（ECE；校准≠准确：温度修复 ECE 0.733→0.571 而准确率不动）
- [[置信度门控与弃权]]（覆盖率换准确率；前提是校准真的好）

**实验记录**（2026-10-03，全部真实运行，Windows 11 + RTX 4070 CPU 路线，venv 隔离装 laya 0.3.24）：
1. `lab01_quickstart.py` 冒烟：billing 工单三问全中（choice 0.9865 / score 1.77 / noul 0.879）；中文工单自动路由 multilingual 且 0.9955 正确；技术故障工单换 technical 0.92。坑：首调 51s（下载 checkpoint）+ 温度超区间 RuntimeWarning
2. `lab02_laya_benchmark.py` 主实验：自建 24 题双语工单考卷（12 英+12 中），dept 75% / urgency 54.2% / churn 91.7% / 三问全对 37.5%；暖态中位 676ms 冷首调 10.3s
3. `lab02b_zh_criteria.py` 对照：中文题 urgency 全饱和在 2（连"不着急"都判停摆）是英文 criteria 与中文输入错配所致——换中文措辞 urgency 4/12→7/12、dept 8/12→10/12、不再饱和（决策模型也吃提示词工程）
4. `lab03_llm_benchmark.py` 云端同卷对比（claude CLI/kimi-for-coding）：见指南 Q10 表；单题中位 ~10s vs Laya 本地 0.25-0.7s
5. 置信门控实测：conf≥0.8 只剩 11 题，子集准确率 72.7% 反而低于全量 75%——校准差时门控无效
- 坑：① Windows `pip install` 全局装被权限拦 → 项目 venv 隔离；② subprocess 调 claude CLI：list+shell=True 引号损坏 / 无 shell 找不到 .cmd / 多行 prompt 被命令行换行截断——终解=.cmd 全路径+单行 prompt；③ venv 里 pip 装 torch 是 CPU 版（要 CUDA 得另装 cu 轮子，本实验 CPU 足够）
- 判例注：拾遗任务 1a45286b（小墨同学推文）判学习类——推文含可复现的本地部署+对比评测方法，且对应开源载体 NandhaKishorM/laya 可 clone 可跑；与 604727ff（Jev 闭源本体非学习类）互补
- 评测口径分析：推主"Jev 准确率完胜（100% vs 57%）"是自建 100 场景考卷（Laya 仅英文跑）；仓库官方基准微调后 0.766 vs Jev 公开值 0.727（Jev 数字第三方发表未实测）；零样本 vs 微调差一倍（0.362→0.766）——不同考卷不可直接比，厂商数字一律打折
- 顺带纠正推文口径："Laya 只支持英文"不准确——english checkpoint 离英语塌方（印地语 0.100 vs 乱猜 0.050），但 Router 会切 multilingual（100+ 语言，本机中文实测 0.9955）

**后续可深入的方向**：laya-server TypeSafe 兼容 API 指向 jev-router 的 TYPESAFE_BASE_URL 接缝=全本地逐轮路由；typed-decisions 微调 loop（Kaggle 2xT4 notebook）；laya-mlx/laya.cpp 部署路线；宽选项（11+）桶温度重校准。

源头：https://x.com/xiaomovps/status/2101111530313933182（小墨同学对比评测帖）
产出：`laya-decision-model/laya-decision-model-小白指南.pdf`（12 问 + 6 步实验，Edge 无头打印）
