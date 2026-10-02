---
tags: [项目]
类别: 开源项目类（Web 3D 方法论）
上游仓库: https://huggingface.co/spaces/mishig/microduck-anatomy（HF Space，源码公开）
完成日期: 2026-10-03
---

# robot-web-anatomy（交互式机器人官网 / Microduck Anatomy）

**这是什么**：Microduck 机器鸭的"全息解剖"官网——官方 GLB 模型 + 官方 RL 步态数据在浏览器里实时驱动的可交互数字展台；本项目学的是它的**方法论**（与 [[项目笔记/microduck|microduck]] 学的机器人本体互为姊妹篇）。

**它给我什么能力**：任何机器人/机械产品都能照五层配方（资产→骨架→动作→交互→分镜）做出会走路、能解剖、可拖拽的交互官网；见[[机器人数字展台]]。

**引入的概念**：
- [[逆运动学IK与CCD迭代]]（补上 FK 笔记"下一站"）
- [[glTF与GLB资产管线]]
- [[机器人数字展台]]

**实验记录**（2026-10-03，全部实测）：`exercise\mini-duck-site\` 单 HTML 复刻四大能力——GLB+kinematics.json 关节树装配、32帧×18通道策略步态回放、图层聚焦、爆炸滑杆。无头 Edge 截图自证：整机行走（遥测 步态相位/髋角/躯干滚转 实时刷新，70 零件·14 关节）、`?layer=MOTORS&explode=0.65` 舵机炸开、`?layer=SENSORS` 镜头高亮。**坑**：① CommonJS `module.exports` 在浏览器 ESM 报错，改 `export{}`；② MJCF z-up → three y-up 必须 `root.rotation.x=-π/2` 且躯干步态偏移写在旋转前坐标系，否则模型躺倒错位。

**后续可深入的方向**：把 CCD 拖拽交互也复刻进 mini 版；试 URDF 格式机器人（另见 urdf-loaders）；用同配方给自己产品做官网。
