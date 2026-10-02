---
tags: [项目]
类别: 开源项目类（知识学习，轻量复刻路线）
上游仓库: graphdeco-inria/gaussian-splatting（commit 54c035f，depth1，submodules 未拉）
完成日期: 2026-10-02
---

# gaussian-splatting

**这是什么**（一句话）：SIGGRAPH 2023 最佳论文"3D Gaussian Splatting"的官方开源实现——用百万级显式彩色椭球 + 可微光栅化，实现照片级场景的实时新视角渲染。

**学习缘起**：抖音"元游镜相"的灵隐寺高斯孪生作品展示帖（作品闭源、无教程），判定 3DGS 技术本身值得独立开讲，以官方仓库为学习对象，因本机无 GPU 走**轻量复刻路线**（论文要点 + 仓库结构 + 纯 CPU 数学复刻）。

**它给我什么能力**：
- 看懂 3DGS 生态全家桶并选型（官方/NVIDIA gsplat/压缩分支/网页播放器）
- 算清算力账：训练要 CUDA（论文级 24GB 显存，可降到 ~8GB）；查看渲染要求低
- 读懂 .ply 资产（62 float32/高斯 = 248 字节）并能写解析器批处理
- 判断商业红线：官方代码 INRIA 非商业许可
- 与 Three.js 技能树合流（GaussianSplats3D 网页播放）

**引入的概念**：
- [[高斯泼溅3DGS]]（核心）
- [[新视角合成]]（问题域）
- [[球面谐波视角色]]（外观建模）

**实验记录**（exercise\，全部 Python 3.14 + numpy + Pillow 实测跑通，无 GPU）：
1. `make_synthetic_ply.py`：手工构造 1500 高斯（红蓝渐变球壳 + 绿色散射盘）按 62 字段写二进制 PLY → 372000 字节 = 1500×248 ✅
2. `parse_ply.py`：零依赖手写二进制 PLY 解析器，验证"一高斯=62 float32"，log/logit/SH-DC 全部正确还原 ✅
3. `mini_splat.py`（主实验）：纯 numpy 复刻渲染四步（Σ=R S Sᵀ Rᵀ → 雅可比投影 2D 协方差 → 深度排序 → 前向 α 混合）→ render.png 出图正确（球壳+散射盘可见），与官方 gaussian_model.py:33-47 激活函数逐行对应 ✅
4. 概念→源码定位：train.py:167-171 密度化循环；gaussian_model.py:409/435/452 split/clone/prune；renderer/__init__.py:91 光栅化入口 ✅

**坑与结论**：
- 克隆要 `--recursive`（含 diff-gaussian-rasterization / simple-knn 子模块），轻量读结构时 depth1 够用
- 训练环境强绑 CUDA 11.8 + VS2019（不支持 Clang），非 12 的 CUDA 12 实测也有兼容路径但默认环境是 Python 3.8 + 旧 PyTorch
- 3DGS 文件大的根因 = 248 字节/高斯 × 百万级；压缩是落地第一工程问题

**后续可深入的方向**：
- 有 GPU 时：手机环拍小物件 → convert.py（COLMAP）→ train.py → Three.js 网页播放
- 3DGS 压缩/流式传输（SOG、quantization）
- 4DGS 动态场景 / 3DGS-SLAM
