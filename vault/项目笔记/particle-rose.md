---
tags: [项目]
类别: 知识学习类（Creative Coding）
上游仓库: 无（X 推文作品，作者未开源；实验代码全部自研）
完成日期: 2026-10-02
---

# particle-rose（粒子玫瑰）

**这是什么**：复现关智博（@guanzhiboisme）2026-08 在 X 上爆火的"粒子玫瑰"视频作品（5.6万+浏览，评论区求教程未开源）。本质 = 参数曲面（玫瑰目标点云）+ 粒子系统（从混沌星云缓动汇聚），两套实现全部自研实测：Python/matplotlib 静态验证版 + Three.js 交互动画版。

**它给我什么能力**：
- 一套可复用的"粒子汇聚"动画管线：起点/目标双缓冲 + 每粒子随机延迟 + easeInOutCubic + GPU uniform 驱动
- 一组可调的玫瑰参数方程（四层弧线花瓣：a0→a1 角度谱 35°→93° 的包心结构、瓣宽自适应、横折、尖卷）
- 无头浏览器给 WebGL 页面拍"确定性证件照"的验收手法（SwiftShader + virtual-time-budget）

**引入的概念**：
- [[粒子系统]]
- [[参数曲面采样]]
- 关联已有：[[Three.js与场景图]]（动画绕过场景图发生在着色器）、[[程序化建模]]、[[确定性脚本]]（固定种子 mulberry32(42) 可复现）、[[证据优先质检ProofOverClaims]]

**实验记录**（exercise\，全部真实运行）：
1. `rose_mpl.py` → `rose_mpl.png`：34,400 粒子静态玫瑰，matplotlib 3.11.2 实测出图。迭代 4 轮：平盘→直立弧线→瓣宽自适应→瓣尖上卷，花型逐版收敛
2. `rose.html`（three.min.js r128 UMD + 精简 OrbitControls + 自定义 ShaderMaterial）→ 无头截图 `rose_final.png`（100% 成品）、`rose_morph.png`（21% 混沌态，virtual-time-budget=3200）
3. 参数实验：`?k=0.55`（瓣数 4/7/10/14→2/4/6/8，`rose_k06.png`）、`?blue=1`（蓝色变体 `rose_blue.png`），固定种子保证可对比
4. 坑：① 加法混合首版全图过曝成白饼——uSize 3.2→0.62、alpha×0.55、辉光核 0.35→0.10 解决；② ES Module 在 file:// 被 CORS 拦——必须用 UMD 版 three.min.js（r128）

**后续可深入的方向**：心形/文字目标点（Canvas 像素采样）、粒子烟花（加重力）、对数螺旋星系、把 aTarget 换成数据做"数据雕塑"
