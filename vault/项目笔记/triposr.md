---
tags: [项目笔记]
项目: triposr
类别: 开源项目类
完成日期: 2026-10-03
来源: "https://x.com/xetgepete/status/2097664117733490964"
---

# TripoSR — 单图秒生 3D 模型（Tripo 开源生态）

## 是什么
Stability AI × Tripo（VAST）2024-03 联合开源的单图前馈 3D 重建模型（MIT，7000+ 星）：一张照片 → 2~3 秒 → 水密网格 + 顶点色，可直接导 GLB。学术底座是 LRM，表示是三平面。拾遗入口是一条葡萄牙语推文（Tripo 的 488 条 3D 提示词库营销帖），按"能不能动手"查证后判定学习类：背后有 TripoSR（本地免费）+ tripo-mcp（207★ MIT，Claude 直连云 3D 生成）+ tripo-python-sdk 完整开源链路。

## 带来的概念
- [[LRM大型重建模型]] — 前馈 3D 生成范式
- [[Triplane三平面表示]] — Transformer 友好的 3D 表示
- 互链：[[点图与前馈重建]]（同门前兄弟：点图 vs 三平面，测绘员 vs 雕塑家）、[[Three.js与场景图]]、[[glTF与GLB资产管线]]、[[MCP服务器]]（tripo-mcp 路线）

## 实验做了什么（RTX 4070，全真跑通）
1. 官方 chair.png：加载 4.6s → 抠图 8.1s → 前向 2.27s → 256³ marching cubes 1.79s → mesh.glb（42,076 顶点/84,156 面/水密）
2. 自选玻璃碗小黄鸭照片：86,480 面水密网格，环绕渲染帧黄身红嘴正确
3. mc-resolution 扫参：128→20,420 面/0.27s；256→84,156/1.79s；384→191,164/5.77s（面数立方增长）
4. 烘焙贴图：实锤上游 bug（positions_to_colors 漏 .to(device)），exercise/run_bake.py 一行修复后 1024² 贴图 32.4s 烘焙成功
5. Three.js 查看器（viewer.html 内嵌双 GLB），Edge 无头截图验证渲染成功

## 坑与结论
- torchmcubes 需编译 CUDA 扩展 → skimage 垫片（exercise/torchmcubes.py）零编译顶替
- transformers 4.35 连环版本套：tokenizers 0.14 要 hub<0.18，钉 hub==0.17.3
- trimesh 4.0.5 的 ndarray.ptp() 被 numpy2 移除 → 升 4.4.9
- xatlas 0.0.9 无 py3.12 wheel → 0.0.11；rembg 要显式装 onnxruntime
- 结论：TripoSR 定位"游戏 demo 灰模/网页素材/想法验证"，背面靠先验想象非测绘级；透明材质与多物体场景翻车
