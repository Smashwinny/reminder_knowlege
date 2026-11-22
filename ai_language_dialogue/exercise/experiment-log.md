# AI 辅助外语对话 · 实验日志（task a23f16a3-5f81-43e0-8ec2-b96a28d7d04a）

初跑：2026-10-27；审核修订：2026-11-22。
性质：学习方法与论文证据 + 参数玩具模型。未验证 Muse 产品身份、语音识别或发音评分。

## 来源核实

- 原帖 @RealHanyaHu 的 AI 外语对话方法：日常场景、对话练习与母语补位。具体每天 10 对话+1 电影是个人安排，不是最佳练习量结论。
- 同名候选 introducing.mue.ai 无法绑定作者所用产品，继续品牌悬置。
- Karpicke & Roediger 2008 原文：https://learninglab.psych.purdue.edu/downloads/2008/2008_Karpicke_Roediger_Science.pdf

原文 pp.966–967：被试学习 40 个斯瓦希里语—英语词对，首次成功回忆后进入不同后续测试/学习条件；一周后重复测试 80%，无重复测试 36%（跨后续学习条件平均）。额外重复学习几乎没有收益，优势来自持续提取。该真人实验支持长期保持效果，但不证明所有间隔或所有学习任务都同样有效。

## 初稿模型问题

初版预设测试成功加固 1.45、重学 1.25，再说“测试效应方向稳健”。这是把待证明方向写进参数后的循环论证。21.7%/33.0% 和 +11.3pp 只能叫参数输出，不是 K&R 复现或真人证据。

## 修订后的真实复跑

新版使用局部随机数生成器，论文与模型输出分开打印；支持加固和衰减参数，8 项 unittest 验证确定性、概率范围、参数敏感性、方向可反转、零衰减和非法输入。

实际命令：

```bash
python -I ai_language_dialogue/exercise/testing_effect_sim.py
python -I ai_language_dialogue/exercise/test_testing_effect_sim.py
python -I ai_language_dialogue/exercise/testing_effect_sim.py --test-success-gain 1 --test-failure-gain 0.5
```

默认共享随机序列仍输出重学 21.7%、测试 33.0%；反向参数输出测试 8.3%，明确推翻“方向稳健”。独立调用 test 的 seed=7 输出 35.0%，初次测试误写成共享序列的 33.0% 导致 1 项失败，已按实际种子语义修正测试并复跑，最终 8 项全通过。

## 方法边界

- 母语补位可维持交流，但补位后应回到目标语言重试；流利感不是掌握证明。
- 隔天 recall 是指标之一，还需目标语准确性、流利度与迁移任务，不是“唯一诚实指标”。
- 困难应与反馈匹配，不是越大越好；任何产品都可尝试方法，但语言覆盖与识别质量不能预设。

## PDF

修订 HTML 后新增 v2 PDF，共 7 页；Windows.Data.Pdf 全部逐页渲染联系表审核：封面/Q1→Q2…Q10→总结→来源，无裁切或空白页。原 PDF 保留，manifest 指向 v2；SHA-256 `248861abb3fc10713d76fcde2f5cef9d1bd45d575cb621d184602018f3e835a1`。
