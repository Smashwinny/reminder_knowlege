---
tags: [项目笔记]
项目: pixel3dworld
类别: 知识学习类（推文技术思路复现）
完成日期: 2026-10-03
---

# pixel3dworld — Three.js 像素风 3D 世界复刻

## 项目是什么
拾遗队列任务（task 01f50401）：X 用户 @ErwinWu000 的复刻思路帖——某像素风 3D 网站爆火后，作者给五点复刻框架：①Three.js/WebGL 引擎 ②Gameplay（行走/对话/场景切换）③2D+3D 资产 ④自写日式 RPG 风 shader ⑤多人位置同步（"idk"）。被引的原网站（17MB、0 加载）具体身份未查实（推文回复区拿不到，WebSearch 未命中），但五点自含、不依赖原仓库 → 判学习类做独立复现。

## 产出
- `pixel3dworld/Three.js像素风3D世界复刻-小白指南.pdf`（12 问，9 页，含 4 张实拍渲染图）
- `pixel3dworld/exercise/`：复现 demo《像素村》（index.html + js/logic.js + js/main.js + server.mjs）+ logic_test.mjs + verify.mjs + analyze_ab.py + verification/（5 张冻结帧截图 + report.json）
- 运行：`node server.mjs` → `http://127.0.0.1:4175/exercise/index.html`；验证：`node logic_test.mjs`、`node verify.mjs`

## 带来的概念
- [[像素化渲染管线]] — 低分辨率 RT + 最近邻放大 + CSS pixelated，缺一就露馅
- [[Cel量化着色与反转壳描边]] — MeshToonMaterial 三档梯度图 + BackSide 放大黑壳
- [[轴分离贴墙滑行碰撞]] — 每轴扫掠钳位，相切留 EPS
- [[确定性快进与真渲染取证]] — ?t= 时间机器 + 无头 Edge HUD 断言 + 截图物证

## 实验做了什么
1. **Node 逻辑测试**（logic_test.mjs）：四逻辑件 23 断言全过。首跑 8 fail：advance 跳打字未转 waiting（真 bug）、碰撞 all-or-nothing 无滑到贴墙（设计缺陷）→ 重写为扫掠钳位（又修扫描轴交换、相切边界两轮）。
2. **无头真渲染取证**（verify.mjs）：确定性 `?demo=1&t=` 快进 5 关键帧，14 断言全过——行走折返 x=3.80、打字机中态、第二句等待态、踩门进屋 scene=house、ghost 延迟插值 (5.84,8.00) 与理论值逐字吻合、4 张 GPU 截图。
3. **像素化 A/B**（analyze_ab.py）：pixel=1 vs 0 均值差 45.42/255，块状度 0.9475>0.9442。

## 坑与结论
- **step() 把场景对象当 grid 传入碰撞**：静止帧 d=0 早退掩盖 60 帧，一移动就炸——错误堆栈进 HUD 才定位。
- **相机方向向量 y 写负**：钻到地下，地板背面剔除"消失"，症状（蓝屏+黑块）与病因风马牛不相及；靠改红背景截图取色破案（蓝天经 sRGB→linear 变换 (62,157,212) 实锤"看到的是天空"）。
- **场景忘加灯**：MeshToonMaterial 受光驱动，无灯全黑；MeshBasicMaterial 不受光所以地板/贴图正常——"有的东西黑有的东西正常"正是灯的指纹。
- **出门传送在门格上** → 村/屋无限横跳；传离门 1.6 格。
- 无头 Edge --screenshot 相对路径"拒绝访问"，必须绝对路径；.edgeprofile 磁盘缓存吃到旧 JS 造成一次 pos=1.80 幽灵 flake，清缓存后连续 5 次稳定 3.80。

## 与已有知识的关系
[[Three.js与场景图]]（img2threejs 学的）直接复用：场景子树挂/摘就是场景切换；[[程序化建模]]、[[纯函数游戏引擎与种子复放]]（deadrun：固定时间步+种子）是本项目的确定性地基；验证方法论挂到 [[证据优先质检ProofOverClaims]] 和 [[质检Gate与自我纠错循环]]。
