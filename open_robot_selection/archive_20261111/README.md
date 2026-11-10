# 开源机器人筛选：2026-11-11 收尾归档

本页汇总机器人停止学习前已经产出的材料。归档检查不等于重新完成真实服务、硬件或生产环境验证；请以各项限制及原始实验日志为准。

原始交付包已在本地保留；公开目录仅收录经筛选的教材、原创练习、来源说明和必要结果。第三方完整源码、抓取全文及重复压缩包不随本次提交发布。

## 小钰 · 开源机器人筛选

- 来源：[https://x.com/techniahqrobot/status/2113982788407787894](https://x.com/techniahqrobot/status/2113982788407787894)
- 归档状态：**待验证（模拟/组件实验，真实硬件或服务未验证）**
- 完整学习验收：本轮未新增完整学习验收，也未更改 Reminder 任务完成状态。

验证范围与缺项：

- 部分练习读取被排除的上游/来源快照；仅归档自写代码与日志，复跑需按sources和原README另取固定版本依赖，未声称清理版可直接完整复跑。
- ## 执行边界 - survey/licenses 使用 exercise/data/repos-slim.json（公开 API 精简缓存）与已读 LICENSE 笔记，不在每次运行时重新打 GitHub API。 - agibot 读取 sources/hf 下已落盘文件。98 个 info.json 的类型统计在 info-scan-stats.json：第一次 urllib 扫描有 9 个 SSL 中断，随后用 `curl -fL --retry 5` 全部找回。最终 98/98，Success 8259 + Error 2 + Intervention 2。Intervention Frame 出现在重试文件中。 - completions.json 的 8146 条 isResultSucceed=false 被解释为占位，不当失败率。 - FK 为纯解析，跳过没有 parent/child 的占位关节；未加载网格，未运行 MuJoCo/PyBullet。 - verify 的 9 组是同一作者自写检查，不能称独立审核或上游测试套件通过。 
- ## 证据等级与限制 原帖=作者陈述；LICENSE/URDF/info.json=固定公开文件；本批输出=API 元数据、标注计数与解析 FK。四层不混用。无真机、无带网格仿真、无完整视频核验，无独立审核。 
- 公开清理版的依赖恢复范围详见 ARCHIVE_DEPENDENCIES.md；原版 README 对自带源码/快照的说明仅适用于本机保留的原包。

阅读与实验入口：

- [experiment-log.md](xiaoyu_20261111_4/experiment-log.md)
- [knowledge-proposal.md](xiaoyu_20261111_4/knowledge-proposal.md)
- [sources.md](xiaoyu_20261111_4/sources.md)
- [开源机器人筛选-增量学习指南.html](xiaoyu_20261111_4/%E5%BC%80%E6%BA%90%E6%9C%BA%E5%99%A8%E4%BA%BA%E7%AD%9B%E9%80%89-%E5%A2%9E%E9%87%8F%E5%AD%A6%E4%B9%A0%E6%8C%87%E5%8D%97.html)
- [开源机器人筛选-增量学习指南.pdf](xiaoyu_20261111_4/%E5%BC%80%E6%BA%90%E6%9C%BA%E5%99%A8%E4%BA%BA%E7%AD%9B%E9%80%89-%E5%A2%9E%E9%87%8F%E5%AD%A6%E4%B9%A0%E6%8C%87%E5%8D%97.pdf)

其余原创练习文件见 [xiaoyu_20261111_4](xiaoyu_20261111_4/)。
原实验日志保留写作时的状态；补收媒体后的当前归档状态以本页和 media 索引为准。

## 整理说明

同一项目的不同机器人材料按子目录保留，来源与状态逐项记录；内容相近并不等于证据相同。需要原始网页快照或固定版本上游依赖的练习，在取得公开来源后才能重跑，本轮没有为补齐归档启动实验。
