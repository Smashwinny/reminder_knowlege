---
tags: [项目]
类别: 开源项目类（全开源 7-DOF 人形双臂平台，无硬件轻量仿真/协议实验）
上游仓库: https://github.com/enactic/openarm（门户）+ 9 子仓库
完成日期: 2026-10-03
---

# openarm（OpenArm）

**这是什么**（一句话）：日本东京 enactic 公司全开源的 7 自由度人形双臂平台——CAD 图纸（CERN-OHL-S v2）+ BOM + 达妙 QDD 电机 CAN 固件协议 + 全套控制/遥操作/仿真/数据代码（Apache-2.0），整机 $6,500，被称为具身智能的"Linux 时刻"。来源：X @AYi_AInotes 推文（拾遗 task 78392ef6）。

**它给我什么能力**：
- 机器人工程的完整分层范式模板：描述层（MJCF/URDF/Isaac 同源）→ 通信层（CAN/MIT 帧）→ 控制层（重力补偿/单边双边遥操作 500Hz）→ 数据层（LeRobot 250Hz）
- 无硬件也能玩的完整学习路径：MuJoCo 模型 + 官方采样数据集 + 浏览器 WASM 版全免费
- 与 microduck（腿）、reachy-mini（脸）互补成"具身智能身·脸·手"三件套

**引入的概念**：
- [[QDD准直驱与反驱力控]]
- [[主从遥操作与双边力反馈]]
- [[CAN总线与MIT电机帧]]

**实验记录**（exercise/，全部真跑通）：
1. ex1 仓库盘点：1 门户（Docusaurus 站）+6 子仓库体积/许可表；关键发现 openarm_hardware 本体只有指针，CAD 实体在 Google Drive（GitHub Releases 仅镜像）
2. ex2 MuJoCo（mujoco 3.14.0 加载 v1/openarm.xml）：nq=9（7 hinge+2 slide）nu=8 质量 5.39kg；FK 全零位末端 z=0.6736m；断电 2s joint2 塌 100.1°（高反驱实证）；竖直伸展保持 3s 纯 PD 残差 0.135° → 加 mj_inverse 重力补偿前馈 7 关节误差全 0（改善 100%）；MjSpec 注入灯光离屏渲染剪影
3. ex3 MIT 帧协议 Python 复刻：q16|dq12|kp12|kd12|tau12=64bit 满排，手算 0x8A3D 一致，1000 组 roundtrip 误差 ≤ 半分辨率，4/4 PASS；错误码 D0 高 4 位解剖
4. ex4 官方数据集（pip openarm_dataset 读 fixture，LeRobot v3.0）：2 episodes（含失败样本）、观测含 qtorque、8 列=7 关节+夹爪、帧间隔 4ms=250Hz

**坑与结论**：
- MuJoCo jnt_type 枚举 hinge=3（不是 0）；nu=8（两指 equality 耦合只占 1 执行器）
- 命令帧与反馈帧位排布不同，混用会出 18.97 N·m 假误差
- openarm_dataset 本版 load_obs 需传 episode dict（README 是旧签名）
- 金属 OBJ 材质无环境贴图渲染偏暗，只作剪影
- 未接触真实硬件：反驱手感/CAN 时序/噪声均未验证（诚实记录）

**后续可深入的方向**：
- 用 dora-openarm 把键盘/手柄接成"伪主臂"替代 $6,500 Leader
- openarm_isaac_lab 跑强化学习抓取任务
- openarm_ros2 + MoveIt2 逆运动学规划（衔接 [[逆运动学IK与CCD迭代]]）
