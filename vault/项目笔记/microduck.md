---
tags: [项目]
类别: 开源项目类（机器人）
上游仓库: https://github.com/pollen-robotics/microduck (+ 姊妹训练仓库 microduck_rl)
完成日期: 2026-10-02
---

# microduck

**这是什么**（一句话）：Hugging Face 旗下 Pollen Robotics 的 25cm 双足开源机器鸭——$399 卖硬件，但"大脑"（Rust 守护进程栈 + MuJoCo/PPO 强化学习训练管线 + 策略分发契约）全开源；15 舵机、744g、50Hz 控制环，会走路/滑轮/叼东西/自己爬起来。源头是拾遗推文（Geek Lite "开源机器鸭，想要一个华强北版本"）。

**它给我什么能力**：
- 一套生产级机器人软件架构模板（7 daemon / 意图-安全层 / 恢复路径解耦）
- 无真机机器人实验室：MuJoCo + 官方物理模型（microduck_rl 的 scene.xml，86 STL + 14 位置伺服 + INIT/STAND/SIT/FOLD 关键帧）零成本做动力学实验
- sim2real 完整流水线代码可读可改；社区策略像 App 一样 `robotctl policy load` 装进鸭子
- Linux 下还有官方 `scripts/duck-sim`：仿真鸭子跑真守护进程

**引入的概念**：
- [[Sim2Real与MuJoCo仿真]]
- [[前向运动学FK与四元数链]]
- [[机器人守护进程架构]]
- [[发布交换与健康门回滚]]

**实验记录**（全部真实运行，Windows 11 + Python 3.14 + MuJoCo 3.14.0，脚本在 `microduck\exercise\`）：
1. 模型体检：kinematics 内嵌 MJCF = 纯运动链（15 关节/0 执行器/0 碰撞体/744.4g）；训练场景版 nu=14、ngeom=82
2. 无地板坠落：0.24s 掉 0.285m ≈ 精确自由落体——模型只描述鸭子，世界是场景给的
3. 位置伺服锁关节：INIT 姿态 0.38s、STAND 姿态 1.03s 后高度跌破 5cm 并瘫在 3.5~4.4cm——静态锁位站不稳，这就是必须用 RL 动态平衡的实证
4. 侧向 0.8m/s 冲量：roll 仅 1.8°（伺服扛住倾斜）但照样塌——平衡必须动态
5. 手写 Python FK（四元数链式折叠）vs mj_kinematics：64 姿态 × 4 site 最大误差 1.8×10⁻⁷ m（镜像上游 fk_against_mujoco.rs）
6. 官方模型渲染：STAND 站姿 vs 3s 后脸着地对比图（duck_stand.png / duck_collapsed.png）
- 坑：MuJoCo 3.14 移除了 `model.jnt_name2id` 便捷方法（改用 `mujoco.mj_name2id`）；默认离屏渲染帧缓冲 640×480，渲染大图要在 XML 里调 offwidth 或缩窗口
- 诚实限制：本机无 Rust 工具链未构建守护进程；未跑真实 ONNX 行走策略（需 microduck_rl 观测管线+权重）；硬件 BOM/CAD 官方不开源（社区 fanhao375 已从 47 个 STL 反推装配图）

**后续可深入的方向**：
- 读 microduck_rl 训练代码，本地训一个自己的步态策略导出 ONNX
- Linux 机器上跑 `scripts/duck-sim`（真守护进程 + 仿真身体）
- 关注华强北生态：ZeroTau 低成本复刻方案 / YIduck / 淘宝 openduck（¥7000+）
