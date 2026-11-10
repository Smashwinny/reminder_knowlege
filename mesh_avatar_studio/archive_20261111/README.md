# Mesh Avatar Studio：一张图到分层网格底稿：2026-11-11 收尾归档

本页汇总机器人停止学习前已经产出的材料。归档检查不等于重新完成真实服务、硬件或生产环境验证；请以各项限制及原始实验日志为准。

原始交付包已在本地保留；公开目录仅收录经筛选的教材、原创练习、来源说明和必要结果。第三方完整源码、抓取全文及重复压缩包不随本次提交发布。

## 陈娇 · Mesh Avatar Studio：一张图到分层网格底稿

- 来源：[https://x.com/i/status/2106593371762651346](https://x.com/i/status/2106593371762651346)
- 归档状态：**待验证（离线实验材料）**
- 完整学习验收：本轮未新增完整学习验收，也未更改 Reminder 任务完成状态。

验证范围与缺项：

- 部分练习读取被排除的上游/来源快照；仅归档自写代码与日志，复跑需按sources和原README另取固定版本依赖，未声称清理版可直接完整复跑。
- ## 前置安装与夹具失败（真实记录） `npm install --prefix exercise/runtime --ignore-scripts --no-audit --no-fund mesh-avatar@0.7.2` 输出：added 2 packages in 405ms，exit=0。 首次 validateRig 返回 `[rig.view: margins must leave a positive viewport]`；将夹具 padTop/padSide 由误填 10 改为 .05 后，通过。上游代码未改。 
- ## 未验证边界 待验证：Studio 编辑器、WebGL 渲染、眼口自然度、Agent 自动生成、ImageGen、真实声音/摄像头和全链路体验。只完成上游文件与归档 API 实验，不冒称可视化运行。 
- 公开清理版的依赖恢复范围详见 ARCHIVE_DEPENDENCIES.md；原版 README 对自带源码/快照的说明仅适用于本机保留的原包。

阅读与实验入口：

- [demo.html](chenjiao_2_16/exercise/demo.html)
- [experiment-log.md](chenjiao_2_16/experiment-log.md)
- [guide.html](chenjiao_2_16/guide.html)
- [guide.pdf](chenjiao_2_16/guide.pdf)
- [knowledge-proposal.md](chenjiao_2_16/knowledge-proposal.md)
- [sources.md](chenjiao_2_16/sources.md)

其余原创练习文件见 [chenjiao_2_16](chenjiao_2_16/)。
原实验日志保留写作时的状态；补收媒体后的当前归档状态以本页和 media 索引为准。

## 整理说明

同一项目的不同机器人材料按子目录保留，来源与状态逐项记录；内容相近并不等于证据相同。需要原始网页快照或固定版本上游依赖的练习，在取得公开来源后才能重跑，本轮没有为补齐归档启动实验。
