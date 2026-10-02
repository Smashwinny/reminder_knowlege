---
tags: [概念]
领域: 三维图形
别名: [glTF, GLB, GLTFLoader]
首次来源: "[[项目笔记/robot-web-anatomy]]"
---

# glTF 与 GLB 资产管线

**一句话定义**：glTF 是三维界的"JPEG"——轻量级 3D 传输格式；GLB 是它的单文件二进制版，把网格、贴图、材质打包成一个自包含文件，浏览器 `GLTFLoader` 一次加载。

**属于领域**：三维图形资产 / Web 3D。

**通俗理解**：GLB 像"真空压缩袋装好的整套乐高"：形状（mesh 几何体）、皮肤（贴图）、说明书（材质）全在一袋；但**怎么拼（关节层级/装配关系）不在袋子里**。Microduck Anatomy 的关键手法正是"几何与装配分离"：GLB 只当零件库（按名字建 `geometryByName` 索引），装配图另用 MuJoCo MJCF 导出的 `kinematics.json`（body 树/位置/四元数/铰链轴），网页端自己总装。好处：同一份官方仿真模型既训机器人又喂官网，不重建模。

**与已有概念的关联**：
- 装配载体：[[Three.js与场景图]]（Group 树挂几何体）
- 上游来源：[[Sim2Real与MuJoCo仿真]]（MJCF 仿真模型导出 GLB + kinematics.json）
- 对比：[[程序化建模]]（代码生成几何；GLB 管线是"拿来主义"路线）
- 坐标系坑：MJCF z-up → three.js y-up 需 `root.rotation.x = -π/2`

**首次接触于**：[[项目笔记/robot-web-anatomy]]
