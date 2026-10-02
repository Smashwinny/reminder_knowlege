---
tags: [项目]
类别: 知识学习类（开源硬件主题，无硬件轻量实验）
上游仓库: https://github.com/grablab/Yale-OpenHand-Workshop-2018
完成日期: 2026-10-02
---

# bionic_hand_diy（百元仿生机械手）

**这是什么**：抖音 @了不起的绿豆冰「不到100块手搓仿生机械手」引出的主题学习——百元内"舵机+绳驱+欠驱动"机械手的结构原理与控制链路。原作者教程渠道（抖音私域）公开不可验证，学习基于公开开源项目：B站小楚君百元机械手（BV19Dgy6GEeJ，网盘全套开源）、MakerWorld 五指灵巧手（ESP32-C3+PCA9685）、Yale OpenHand（repo\ 克隆其 Workshop 仓 @ ac11e5c）。

**它给我什么能力**：讲清欠驱动自适应抓握原理；PWM↔角度、闭合量↔关节角、关节角↔指尖三条换算链；四流派开源选型（入门小楚君/进阶 MakerWorld/读码 Yale/整机体 InMoov）；≤￥100 BOM 与避坑表（供电共地、绳张力、扭矩上限 40%）。

**引入的概念**：
- [[舵机与PWM角度控制]]
- [[绳驱欠驱动]]
- [[正运动学向量接力]]
- [[比例量控制接口]]

**实验记录**（无硬件，纯软件仿真，全部实跑）：
- `exercise\bionic_hand_sim.py` 5 步全 PASS：Step1 PWM 映射（1500µs→90° 断言过）；Step2 比例耦合 5:3:2（c=1→90°/60°/28°，绳行程 6.21mm 单调）；Step3 正运动学（伸直 (0,84)=指长和；握拢 (53.6,−40.5)）；Step4 出 fig_hand_poses.png + fig_finger_trajectory.png（目检过）；Step5 抓取序列状态机（张开→闭合→保持→释放断言过）
- 坑①：grablab/openhand-firmware 仓库名不存在，固件实际在 Workshop/openhand_node 仓
- 坑②：运动学初始方向写反（−90°），指尖跑到 (0,−84)，改 +90° 弯向掌心
- 坑③：比例耦合下 c=1 只有近端关节满角（90/60/28），断言先写错后按模型修正

**产出**：`F:\reminder\bionic_hand_diy\百元仿生机械手-小白指南.pdf`（11 疑问卡片+SVG+实验章节）；HTML 源 `guide_bionic_hand.html`；拾遗任务 6e3cb007 已标完成。

**升级路径**：体感手套（弯曲传感器/MediaPipe）→ 肌电（MyoWare）→ 力控（FSR 主动柔顺）→ Dynamixel 数字舵机闭环。
