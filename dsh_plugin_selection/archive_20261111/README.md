# 不是装满插件  而是补上一个痛点：2026-11-11 收尾归档

本页汇总机器人停止学习前已经产出的材料。归档检查不等于重新完成真实服务、硬件或生产环境验证；请以各项限制及原始实验日志为准。

原始交付包已在本地保留；公开目录仅收录经筛选的教材、原创练习、来源说明和必要结果。第三方完整源码、抓取全文及重复压缩包不随本次提交发布。

## 马老师 · 不是装满插件  而是补上一个痛点

- 来源：[https://x.com/i/status/2112791503278125329](https://x.com/i/status/2112791503278125329)
- 归档状态：**离线/组件实验已交付，真实集成待验证**
- 完整学习验收：本轮未新增完整学习验收，也未更改 Reminder 任务完成状态。

验证范围与缺项：

- 部分练习读取被排除的上游/来源快照；仅归档自写代码与日志，复跑需按sources和原README另取固定版本依赖，未声称清理版可直接完整复跑。
- ## 3 长上下文边界与聚合反例  时间：2026-11-11T01:05:07.983499+08:00（Asia/Shanghai UTC+8） 工作目录：`/workspace/reminder-batch/item-4-dsh-plugin-picks/exercise`  ```bash node --import ./network-guard.mjs threshold.mjs ```  真实输出： ```text {"label":"exactly threshold","got":0.4,"want":0.4} {"label":"one above","got":0.800004,"want":0.800004} {"label":"cache participates","got":0.600002,"want":0.600002} {"label":"output excluded from threshold","got":2.400002,"want":2.400002} {"counterexample":"sum two per-call charges, not aggregate tokens then charge","separate":0.5,"aggregated":1} PASS: 4 boundaries + aggregation counterexample; network attempts=0  ``` 退出码：0 
- ## 准备阶段失败（未隐藏） 首次依赖扫描正则误匹配注释中的 from 字样，manifest未生成，正式首步退出1；原样保留 evidence/experiment-first-failure.md。改成只匹配 import 行后，复制21文件，六步重新执行全部退出0。此日志上方为成功复跑真实输出。 
- 真实完成：HTML（12问各SVG、5用途）、15页A4 PDF实际打印且逐页Read检查、六步离线组件实验全退出0、exercise.zip/experiment-log/knowledge-proposal/sources/交付ZIP已保存；待验证：真实DSH安装兼容、会话恢复、模型审查质量、实际账单、原生桌面与用户本机。
- 公开清理版的依赖恢复范围详见 ARCHIVE_DEPENDENCIES.md；原版 README 对自带源码/快照的说明仅适用于本机保留的原包。

阅读与实验入口：

- [dsh-plugin-picks.pdf](malaoshi_20261111_4/dsh-plugin-picks.pdf)
- [experiment-log.md](malaoshi_20261111_4/experiment-log.md)
- [index.html](malaoshi_20261111_4/index.html)
- [knowledge-proposal.md](malaoshi_20261111_4/knowledge-proposal.md)
- [sources.md](malaoshi_20261111_4/sources.md)

其余原创练习文件见 [malaoshi_20261111_4](malaoshi_20261111_4/)。
原实验日志保留写作时的状态；补收媒体后的当前归档状态以本页和 media 索引为准。

## 整理说明

同一项目的不同机器人材料按子目录保留，来源与状态逐项记录；内容相近并不等于证据相同。需要原始网页快照或固定版本上游依赖的练习，在取得公开来源后才能重跑，本轮没有为补齐归档启动实验。
