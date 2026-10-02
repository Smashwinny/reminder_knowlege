---
tags: [项目]
类别: 知识学习类（推文复刻）
上游仓库: 无（作者 Dilum Sanjaya 未开源；本复刻为原创实现）
完成日期: 2026-10-02
---

# blueprint_to_3d（2D 工程图纸 → 3D 模型自然过渡）

**这是什么**（一句话）：复刻 X 推文 https://x.com/DilumSanjaya/status/2092293934844346660 中 Dilum Sanjaya 用 Kimi K3 制作的应用——左侧 2D 工程图纸（代码生成、含尺寸标注）自然过渡到右侧 Three.js 代码生成的 3D 坦克，模型可一键替换为机器人。

**它给我什么能力**：
- "2D→3D 自然过渡"三件套：SVG stroke-dashoffset 图纸重绘 + 3D 零件错峰挤出 + easeOutBack 回弹
- 数据驱动双视图：一份零件数据同时投影成 SVG 工程图纸和 3D 场景，换模型 = 换数据条目
- 无头验收 WebGL：Edge `--headless=new --screenshot` + 页面内置统计钩子（PARTS/DRAWCALLS）

**引入的概念**：
- [[补间动画与缓动函数]]（新概念，本批入库）
- 复用了 [[程序化建模]]、[[Three.js与场景图]]（vault 已有，未重建）
- 关联 [[双时钟模型]]：状态由时间函数导出，不逐帧存

**实验记录**（做了什么、结果、坑）：
- 实验材料：`F:\reminder\blueprint-to-3d\exercise\`（index.html + app.js + vendor/ 本地化 three@0.160.0）
- 坦克 14 零件（履带×2、轮×8、车体、炮塔、炮管、天线），炮塔组挂 turretNode 展示场景图父子层级；机器人 8 零件
- 实测：http.server 8977 服务，Edge 无头截图 3 张全部成功（图纸态 PARTS=14 DRAWCALLS=15；坦克 3D；机器人 PARTS=8）
- 坑1：ES module 在 file:// 下被 CORS 拦截，双击 html 白屏——必须本地 http 服务
- 坑2：Edge 无头 `--disable-gpu` 下 WebGL 走 SwiftShader 软渲染，可用，无需真实显卡
- 产出 PDF：`blueprint-to-3d/图纸到3D过渡-小白指南.pdf`（10 页，含 5 张 SVG 示意图 + 3 张实验截图）

**后续可深入的方向**：
- 让 AI 输出零件 JSON（"AI 生成准确的机器人设计图纸"的落地路径）：LLM → 结构化清单 → 本复刻的渲染器
- 真 morph：图纸 SVG 路径顶点与 3D 线框顶点一一插值（本项目用的是"重绘+挤出"的观感等价方案）
- 三视图图纸（主视/俯视/侧视）+ 爆炸图动画

**来源链接**：https://x.com/DilumSanjaya/status/2092293934844346660（x.com 无法直接抓取，内容经 WebSearch + LinkedIn 同文帖子交叉确认）
