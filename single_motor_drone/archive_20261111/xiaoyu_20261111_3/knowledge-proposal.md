# 知识入库提案（仅候选，不改 vault）

协调者决定是否合入。本 worker 不提交 Git、不改 `vault/`、不勾任务。

## 查重

- 仓库：https://github.com/Smashwinny/reminder_knowlege
- 分支 / SHA：`main` / `a8674777e18302b8804b137212b1396cbfe5a747`
- 提交时间：2026-11-04T09:42:58Z → 2026-11-04 17:42:58 Asia/Shanghai
- 已读：`vault/00-总览.md` 及树中路径关键词（bird, joshua, drone, 旋翼, 周期, paulos, hinge, cyclic, TPU, PPA, swashplate, underactuat）
- 已有相关条目：仅 `fly-brain-drone`（果蝇全脑 + 四旋翼仿真，2026-10-03），主题不同
- 结论：**无重复，本包为新增**

## 建议条目

| 字段 | 建议 |
| --- | --- |
| slug | `single-propeller-drone` 或 `bird-hinged-rotor` |
| 类型 | 开源项目类 + 概念（周期调速 / 滞后-变距耦合） |
| 一句话 | Joshua Bird 用 45° 斜铰链把电机一次谐波加减速变成周期变距，6 英寸桨约 2 万转、开源 CAD 与 moteus/ArduPilot fork；源头是 Paulos & Yim 2013，不是「第一次单电机起飞」 |
| 要点 | θ=ζ tan(α)，45° 为 1:1；反电势电调在约 50 Hz 失步；周期正弦必须在电调 ISR 用编码器计算（0.2 ms≈24°）；160 Hz 更接近结构模态而非锁死的 333 Hz 1/rev；PULSAR 面积比验算为 6.087；机身仍慢转，航向靠红外信标；MCOUT 文档协议号 50 对 51 未决 |
| 来源 SHA | 飞机仓库 `efc9176`；moteus `704a0dd`；ardupilot `455b266` |
| 附件 | `单电机铰链桨无人机-增量学习指南.html/.pdf`、`exercise.zip`、`experiment-log.md`、`sources.md` |
| 状态标签 | 学习与数值实验真实完成；打印/台架/试飞/频闪待验证 |

## 不要写入的内容

- 把 16.978 N 推力或 1.36 N 侧向力写成实测
- 把 2 ms = 20° 的自动字幕错误当成作者数据
- 把 moteus 文档示例 40 rev/s 当成飞行转速
