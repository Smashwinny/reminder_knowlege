# 七个 AI 信息入口：发现、原文与评测分工：2026-11-11 收尾归档

本页汇总机器人停止学习前已经产出的材料。归档检查不等于重新完成真实服务、硬件或生产环境验证；请以各项限制及原始实验日志为准。

原始交付包已在本地保留；公开目录仅收录经筛选的教材、原创练习、来源说明和必要结果。第三方完整源码、抓取全文及重复压缩包不随本次提交发布。

## 陈娇 · 七个 AI 信息入口：发现、原文与评测分工

- 来源：[https://x.com/i/status/2106520924631744599](https://x.com/i/status/2106520924631744599)
- 归档状态：**待验证（离线实验材料）**
- 完整学习验收：本轮未新增完整学习验收，也未更改 Reminder 任务完成状态。

验证范围与缺项：

- 部分练习读取被排除的上游/来源快照；仅归档自写代码与日志，复跑需按sources和原README另取固定版本依赖，未声称清理版可直接完整复跑。
- ## 步骤 4：检查阅读覆盖和证据边界 目的：检查阅读覆盖和证据边界  ```bash cd /workspace/chen-jiao-batch2-20261111/item12 python3 exercise/lab.py audit ``` 真实结果 exit=0： ```text sources_with_paper_ids= ['HF-Papers.html', 'alphaXiv.html', 'arXiv.html', 'paper-2611.12865.html'] HTTP 200 != paper reviewed; rankings != universal quality; no schedule created  ``` 验证：输出实际含论文 ID 的来源集合 
- ## 未验证边界 待验证：论文 PDF 全文、代码与方法复现；Arena/AA 完整方法和实测；页面动态数据未全面读取。没有建立监控或登录账号。 
- 公开清理版的依赖恢复范围详见 ARCHIVE_DEPENDENCIES.md；原版 README 对自带源码/快照的说明仅适用于本机保留的原包。

阅读与实验入口：

- [experiment-log.md](chenjiao_2_12/experiment-log.md)
- [guide.html](chenjiao_2_12/guide.html)
- [guide.pdf](chenjiao_2_12/guide.pdf)
- [knowledge-proposal.md](chenjiao_2_12/knowledge-proposal.md)
- [sources.md](chenjiao_2_12/sources.md)

其余原创练习文件见 [chenjiao_2_12](chenjiao_2_12/)。
原实验日志保留写作时的状态；补收媒体后的当前归档状态以本页和 media 索引为准。

## 悠咪 · 七类AI信源与可追溯选型

- 来源：[https://x.com/i/status/2110271890967130252](https://x.com/i/status/2110271890967130252)
- 归档状态：**待验证**
- 完整学习验收：本轮未新增完整学习验收，也未更改 Reminder 任务完成状态。

验证范围与缺项：

- 普通HTTP6页403；真实模型选型、API评测及论文性能未验证。
- 原exercise.zip含原帖/完整网页/上游源码，禁止原样公开；已重包仅所列原创练习与必要结果。
- 部分练习读取已剔除的原始来源/上游文件；公开清理包是成果归档，不保证离线即跑。应按sources取得对应公开版本，本轮不下载补齐或重跑。

阅读与实验入口：

- [guide.html](youmi_20261111-final-existing-output_item07/guide.html)
- [guide.pdf](youmi_20261111-final-existing-output_item07/guide.pdf)
- [experiment-log.md](youmi_20261111-final-existing-output_item07/experiment-log.md)
- [knowledge-proposal.md](youmi_20261111-final-existing-output_item07/knowledge-proposal.md)
- [sources.md](youmi_20261111-final-existing-output_item07/sources.md)

其余原创练习文件见 [youmi_20261111-final-existing-output_item07](youmi_20261111-final-existing-output_item07/)。
原实验日志保留写作时的状态；补收媒体后的当前归档状态以本页和 media 索引为准。

## 整理说明

同一项目的不同机器人材料按子目录保留，来源与状态逐项记录；内容相近并不等于证据相同。需要原始网页快照或固定版本上游依赖的练习，在取得公开来源后才能重跑，本轮没有为补齐归档启动实验。
