---
tags: [概念]
领域: 三维图形
别名: [Three.js, 场景图, Scene Graph]
首次来源: "[[项目笔记/img2threejs]]"
---

# Three.js 与场景图

**一句话定义**：Three.js 是浏览器里最常用的 JavaScript 三维渲染库；它组织三维世界的核心结构叫"场景图"（Scene Graph）——一棵把所有物体按父子关系挂起来的树。

**属于领域**：三维图形 / Web 前端

**通俗理解**：场景图像"家族树"：场景(Scene)是祖宗，下面的网格(Mesh)、灯光、相机都是子孙。**父节点动，全体子孙跟着动**——把车门挂到车身上，旋转车身时车门自然跟着转，不用单独算车门的位置。这就是为什么层级组织方式本身就是建模的一部分。

**与已有概念的关联**：
- 相关：[[程序化建模]]（Three.js 是程序化建模最常用的执行环境）
- 相关：[[构建流水线与Pass]]（img2threejs 的产物就是一段在浏览器里构建场景图的 TypeScript 代码）
- 接第三方 GLB 资产三坑（2026-10-03 来自 [[项目笔记/3d_vibe_coding]] 花叔书 §12，亲手复现坑一）：
  ① **PBR 死黑**——metalness 高的材质没有 `scene.environment` 时在白底上渲成一团黑（漫反射被抑制只剩直射光），修法 = canvas 画渐变当 equirect → PMREMGenerator 转环境光照（渐变必须有暗部 #403c35 当"黑旗"，金属才有明暗对比）；不要金属质感就把 metalness 摁 0
  ② **带骨骼的模型不能用普通 clone()**——所有实例共享同一副骨骼会"同手同脚"；用 `SkeletonUtils.clone()` + 每实例一个 AnimationMixer + 相位按坐标错开 `(x*0.37+z*0.11)%duration`，并切掉动画位移轨（位移归游戏代码）
  ③ **vendor 精选钉版本**——`npm i three@0.160.0` 后只拷 5 个文件（three.module/GLTFLoader/OrbitControls/BufferGeometryUtils/SkeletonUtils），5 个必须同一版本；BufferGeometryUtils 不是可选的（GLTFLoader 自己 import，缺了的表现是页面全白而非报错）；WebGL 页面必须走 http，file:// 被 CORS 挡

**首次接触于**：[[项目笔记/img2threejs]]
