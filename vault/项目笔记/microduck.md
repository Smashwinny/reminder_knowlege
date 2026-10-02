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

**硬件拆解补充篇**（拾遗 task 6083ef55，同日第二帖，PDF：`microduck/Microduck硬件架构拆解.pdf`，实验在 `microduck/exercise/hardware/`）：
- 15-DOF 硬件地图从仓库内嵌 MJCF 复算：头3 + 颈1 + 双腿各5 + 喙1（喙在行走 MJCF 外，由 theremin/chorale 驱动）；主控 RK3566 / Radxa Zero 3（soc.rs 双热区坐实），ToF = ST VL53L8CX 8×8（vendor 驱动进仓库，源码明言 "no reprojection"——不是扫描式激光雷达）
- 总线：15 舵机 + IMU 共一根 UART 菊花链；fast sync read(0x8A) 一次接力应答省 15 个帧头（bus.rs 注释原话）；XL330 固件 v46+ 才支持（robotd-params）
- 实验三段全 PASS（duck_hardware_lab.py，纯标准库）：MJCF 解析 15-DOF 地图；Dynamixel Protocol 2.0 CRC-16 双实现交叉验证命中标准向量 0xFEE8 + SyncWrite 构造/回读/篡改检测；BOM 三情景（零售 15 只舵机 $412.35 > 整机 $399，批量才回成本线下）
- 新概念：[[智能舵机与菊花链总线]]（与 [[舵机与PWM角度控制]] 哑巴舵机对照）；诚实记录：无实机，实验 2 仅协议层正确性验证

**复刻教程补充篇**（拾遗 task f3ccf5fa，yishan(@tspy) 的 X 长文《如何从零 DIY 复刻一只可爱的 Microduck》15 章，PDF：`microduck/Microduck DIY复刻教程补充篇.pdf`，实验 `microduck/exercise/contract_check.py`）：
- 完整复刻路线图：机械重建（第三方 fanhao375/microduck-replica 已把 47 网格归并成 15 装配件，总质量 ~737g）→ 电气（HAT 原理图开源于 elec_RPI_Robot_HAT，KiCad+Gerber）→ 契约对齐 → ONNX 导出 → 十级调试（单舵机→单腿→15 舵机→IMU→吊架回 home→离地跑策略→扶持站→独立站 5-10s→扶持走→0.2m 自由走）
- **主实验 contract_check.py 27/27 PASS**：复刻契约对拍——解析两仓库真实源码交叉验证 15 关节线序+ID 表（左腿 20-24/头颈 30-33/嘴 34/右腿 10-14/IMU 200/1Mbps）、训练端 HOME_FRAME vs 运行端 DEFAULT_POSITION 14 关节逐值全等、61 维观测拼装（含 body 块 z,roll,pitch 顺序与 x/y/yaw 恒零两个暗坑）、**index-9 陷阱复现**（14 维动作直拷会把 +28.6° 右髋命令送进嘴部舵机）、XL330 raw→rad 编码、ONNX 契约常量（OBS_LEN=61/ACTION_LEN=14/50Hz/policy.onnx 固定名）
- 新概念：[[策略观测向量与动作契约]]（61 维布局/四道锁/重训触发清单）；[[Sim2Real与MuJoCo仿真]] 补充电压随机化实证 vin_range=(6.5,8.2)
- 关键警示（文章原话）：结构若从 ~800g 涨到 1.2kg 就是另一套动力学，必须更新 MJCF 重训，不能只调 action_scale；官方 XL330 电压适配（标称 5V vs 训练 6.5-8.2V 随机）作者自认未经实物验证

**后续可深入的方向**：
- 读 microduck_rl 训练代码，本地训一个自己的步态策略导出 ONNX
- Linux 机器上跑 `scripts/duck-sim`（真守护进程 + 仿真身体）
- 关注华强北生态：ZeroTau 低成本复刻方案 / YIduck / 淘宝 openduck（¥7000+）
