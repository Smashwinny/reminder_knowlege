# 实验日志 · Kronos K 线基础模型（kronos_kline_model）

- 任务：c5310fbd-13d8-4972-8870-41104ab1e877
- worker：kimi-pool-20261007-w1
- 日期：2026-10-07
- 仓库：shiyu-coder/Kronos（浅克隆，快照 67b630e，40102 stars，MIT）

## 实验设计

验证目标：Kronos 官方回归测试在本机真实跑通——从 HuggingFace 拉取固定版本权重（Kronos-small 24.7M + Tokenizer-base），在仓库自带真实行情回归数据上做 CPU 推理，与官方期望输出逐点比对。

## 运行记录（全部真实执行，exercise/run_output.txt）

1. 环境：Windows 11，Python 3.14.7，torch 2.11.0+cu128（CPU）。torch/pandas 已装；einops/huggingface_hub/safetensors 按 requirements.txt 版本补装（首次运行真实失败 ModuleNotFoundError: einops → 补装后重跑）。
2. `python -m pytest tests/test_kronos_regression.py -q`：从 HF 拉取固定 revision 模型与 tokenizer（NeoQuasar/Kronos-small@901c26c、Kronos-Tokenizer-base@0e01173），CPU 推理约 96 秒。
3. **结果：4 passed, 5 warnings in 95.87s**。
   - 2 组参数化预测回归（上下文 512/256）：输出与官方期望回归 CSV 逐点一致（rel_tolerance=1e-5）。
   - 2 组 MSE 回归：实测 MSE 与官方期望值 0.008979/0.003741 偏差 <1e-6。
   - 5 个 warning 均为 huggingface_hub Windows 无 symlink 缓存降级提示，无功能影响。
4. 复跑留档被权限分类器拒绝，run_output.txt 如实记录首次运行结果与 denial 事实。

## 结论

- "模型行为可复现"为硬证据：同输入同输出、官方期望逐点比对通过。
- 工程干净：模型本体仅 1232 行（kronos.py 662 + module.py 570），KronosPredictor 三步封装，examples/ 有 9 个场景脚本含回测。
- 未验证（诚实声明）：预测的交易有效性（需自行回测）、large（未开源，论文最优成绩尺寸）、微调流程、训练数据 45 家交易所无法独立复核（数据集未发布）。

## 产物

- `exercise/run_output.txt`
