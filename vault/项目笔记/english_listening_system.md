---
tags: [项目笔记]
类别: 知识学习类（英语听力训练方法）
来源项目: english_listening_system
原始作者: momoai_daily
原文文章ID: 2104111173943828480
完成日期: 2026-11-22
---

# english_listening_system：可回收的英语听力训练闭环

## 项目是什么

[@momoai_daily](https://x.com/momoai_daily) 的公开 X Article《听力练了很久，为什么还是听不懂？ChatGPT + Obsidian 搭一套可回收的英语听力训练系统》提出一套方法：用两遍盲听与文本校准处理输入，用跟读、半句预测、脱稿复述和新场景提取检验理解，再由 Obsidian 保存误听、语块、复述和复习题，让旧内容进入后续训练。ChatGPT 负责降低材料组织与反馈成本，Obsidian 负责留下可检索的个人语料。

## 来源核实

- 主帖：https://x.com/momoai_daily/status/2105541217975247073
- 同作者原始文章状态：https://x.com/momoai_daily/status/2104136225120772358
- X Article：https://x.com/i/article/2104111173943828480
- 本次实际读取通道：https://api.fxtwitter.com/momoai_daily/status/2104136225120772358
- 转载交叉印证：https://www.jxxy.net/ai/articles/chatgpt-obsidian-listening-training/

主帖两张公开图片已实际下载并读取，第一张提供目标文章标题，第二张仅为可选插件截图。直接读取 X 在本环境返回 HTTP 402，因此正文通过公共镜像取得，转载页用于署名与原文链接交叉印证。没有采用传播人数作为已核实事实，也没有用 Compass 或 Penny777 的另一套口语系统替代本项目。

## 带来的概念

- **声音—意义双层拆解**：把“听清”与“听懂”分开观察，错误可进一步标为声音边界、连读弱读、生词、熟词反应、句法、篇章和短期记忆；标签是训练假设而非诊断。
- **两层重复与场景迁移**：同材重复建立声音熟悉度，同主题换材料与新场景提取帮助语块迁移；避免只背一篇或每天全新材料。
- **可回收训练闭环**：练习留下误听、语块、复述和复习题，后续再次提取并更新状态；笔记保存本身不等于回收完成。
- [[原子笔记与双链]]：复盘可成为个人语料节点，但本系统还要求复习问题回流训练，不只是静态双链。
- [[固定间隔重复排程]]：可辅助安排复习，但原文没有指定 +1/+2/+4/+7/+15 等固定日程，不能把两者等同。
- [[确定性脚本]] 与 [[证据优先质检ProofOverClaims]]：本地实验把词面指标交给确定性代码，同时把代理指标与真人效果严格分开。

## 能力清单

1. 用三遍测试筛选材料；2. 把模糊“听不懂”拆成可训练错误；3. 用 AI 组织盲听、预测、复述与新场景；4. 保存自己的误听和真实表达；5. 把旧错误转成后续复习任务；6. 迁移到日常、工作、播客和雅思精听。

## 实验做了什么

- 在 `english_listening_system/exercise/` 用 Windows SAPI 实际生成 669,410 字节、非静音的英语 WAV；材料为自编 31 词项目进度更新。
- 用 Python 3.14.7 `-I` 运行确定性反馈工具，输入为明确标注的合成学习者夹具，不是真人练习。
- baseline：2 个词替换，WER 6.45%，词面准确率代理 93.55%，复述关键点覆盖 66.67%，新场景语块命中 0%。
- replay：修改合成输入后，WER 0%、复述覆盖 100%、新场景语块命中 33.33%；生成两份 Obsidian 风格 Markdown 与机器 JSON。
- 首次测试因 Python 3.14 移除 `audioop` 出现 1 项 ERROR；改用 `array + math` 计算 PCM RMS，并修复复习题错误耦合。最终 6 项检查全部通过，原始输出为 `exercise/test-output.txt` 和 `exercise/experiment-log.txt`。

## 坑与结论

- 原文 60% 首听、80% 复听是作者选材经验，不是统一科学分数线；词面准确率、关键点命中也不等于理解率或 CEFR。
- 提示词可以要求“不要提前显示文本、不要编造链接和进步”，但真实音频、文本、学习记录仍需独立核对。
- 主帖截图列出 Claudian、Language Learner、RSS Dashboard、Smart Media Notes、Spaced Repetition；原训练文章不要求这些插件，本次未安装或核验。
- 未验证 ChatGPT Live、自动联网选材、真实 Obsidian 写入、真人盲听、发音质量、长期记忆或训练效果。
- 指南：`english_listening_system/guide.html` 与 `english_listening_system/english_listening_system-小白指南.pdf`（23 页，938,256 字节；结构检查通过，当前环境缺少 pdftoppm，未宣称逐页视觉审核）。
