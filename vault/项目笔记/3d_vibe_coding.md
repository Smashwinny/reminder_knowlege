---
tags: [项目笔记]
项目: 3d_vibe_coding
类别: 知识学习类（开源橙皮书精读）
完成日期: 2026-10-03
来源: "https://x.com/AlchainHust/status/2099823153199591775"
---

# 《3D Vibe Coding》橙皮书 — 386 页开源手册盘点 + 三章深挖

## 是什么
花叔（@alchaincyf）2026-09-15 宣布开源的《3D Vibe Coding 手册》配套仓库（github.com/alchaincyf/3d-vibe-coding-handbook，269★，CC BY-NC-SA 4.0）：386 页 / 25.6 万字 / 260 图 / 6 个可玩 demo，是"用 Codex + Tripo 两天造一座能开车逛的巴黎"的全程实测记录。book/ 全书 HTML、demos/ 三个 demo 源码、scripts/ 11 个工具脚本、manifest/ 56 件资产逐件对账表。查证：fxtwitter 拿全文解析出仓库链接 + GitHub API 确认真实（描述/创建时间/许可与推文口径一致）。

## 学法（照 Agentic Design Patterns 开源书先例）
不逐章学：全书目录盘点（§00–§22 + 附录 A–D，27 行）+ 深挖 3 章（§01 图生3D 第一次 / §04 减面与重拓扑 / §12 Three.js 接入）+ 简挖 §11（五条接入路）/§17（清洗流水线）+ 附录 B 踩坑索引与 D 术语表。

## 带来的概念
- [[图生3D资产管线]] — 研究模型（[[LRM大型重建模型]]）之外的商业化后处理全链
- [[面数口径与减面下限]] — 同一个 8000 不是同一个 8000；下限由几何光滑度决定
- [[先量后优化性能法]] — GPU timer query / vsync 陷阱 / "量不出回归"
- 补强：[[Three.js与场景图]]（环境贴图死黑 / SkeletonUtils / vendor 钉版本）、[[证据优先质检ProofOverClaims]]（口径学 / 哈希锁输入 / 多通道互证）
- 互链：[[glTF与GLB资产管线]]、[[程序化建模]]、[[混合模型分工流水线]]、[[机制流与资产流隔离]]、[[MCP协议]]、[[Triplane三平面表示]]、[[内容型开源与双许可]]

## 实验做了什么（exercise\，全离线真跑通）
1. **零依赖手写 GLB + 减面极限复现**：make_glb.py 造光滑球（720 三角，笔算 2×24×16−48 吻合）+ 格构塔（1152=8 层×144）；自写 count_faces（indices.count/3 口径）与书 repo 的 measure_glb.py 双通道对账一致；@gltf-transform/cli@4.5.1 复现 E1：球砍到 4.9% 触底、塔 29.2% 触底（ratio 0.1/0.05/0.02 输出逐位相同）——"格构结构几乎砍不动"亲手复现；optimize quantize 14,560→8,472 字节
2. **PBR 白底死黑 A/B**：three@0.160.0 vendor 精选 5 文件 + 书 §12 最小壳 + ?env 开关，headless Edge（--use-angle=swiftshader）截图：env=0 铬球死黑 vs env=1 canvas 渐变环境贴图修复；Python 解 PNG 量化球中心区亮度 72.9 → 206.7（2.8×）。附带发现：铬材质格构塔在白底上近乎隐形（死黑坑的镜像）

## 坑与结论
- 塔按 Z-up 建，measure_glb.py 按 glTF Y-up 读"高度"= 1.0008——资产轴向/朝向不能想当然，亲手撞上书里同款坑
- 书中最贵的教训：默认价 50 里 35 分是导出时要降掉的 8K 贴图；面数框两种模式数的不是同一种面（换算系数 1+四边形占比≈1.75）；卡顿真凶常是贴图显存（31 张 8K=5.0 GiB→0.22 GiB，23×）而非三角面；Studio 订阅与 API 钱包两套账不互通（CLI/Codex 插件/MCP 三条 Agent 路共享 API 钱包）；响应式输入框改 DOM 不改状态（65 积分废件，ArrowRight 硬验证法）
- 结论：这本书 3D 部分教"从一张设计图到一座能开的城"，方法论部分（口径标注/哈希锁输入/多通道互证/空格不抄数）比技巧更值钱

## 产出
- PDF：3d_vibe_coding/3D_Vibe_Coding-小白指南.pdf（16 页 A4，12 问 + 目录盘点 + 2 实验 + 2 实拍图）
- HTML 源：3d_vibe_coding/guide.html；实验：3d_vibe_coding/exercise/（make_glb.py、three_shell/、decim/、截图、章节摘录 notes/）
