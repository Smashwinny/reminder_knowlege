---
tags: [概念]
领域: 实时渲染 / 频谱海洋
别名: [FFT Ocean Cascades, Stockham IFFT]
首次来源: "[[项目笔记/ultra_water]]"
---

# FFT海面级联

**一句话定义**：把不同空间尺度的波谱分到多个网格，分别做二维逆 FFT 得到位移与斜率，再按世界尺度采样叠加，构造实时海面。

**通俗理解**：远处长涌浪和眼前细碎波纹需要不同的“尺子”。级联让每张纹理拥有自己的世界长度；它不是把同一张波浪图复制四次。FFT 网格尺寸、世界覆盖范围、屏幕像素分辨率是三个不同量。

## 固定实现：Ultra-Water

- 每级 `N=256`，世界长度 `[600,85,12,2.1]` 米；频谱沿纵向组成 `256×1024` 图集。每级纹素尺寸约 `2.34375、0.33203125、0.046875、0.008203125` 米。
- JONSWAP 风浪与 swell 参数生成复频谱；相位演化后，横向和纵向各做8个 Stockham radix-2 pass，共16个 IFFT pass。两个渲染目标交替读写，MRT 同时输出多个附件。
- `pack2(a,b)=a+i·b` 将两路实场打包到复变换。最终装配乘 `(-1)^(x+y)`，撤销居中波数的频移；遗漏这一步会让独立 DFT 对拍出现棋盘符号差异。
- 该项目把色散频率量化为 `2π/300` 的整数倍，频谱相位可300秒循环；这不意味着泡沫历史、浮体或整个场景也严格循环。
- 前三级位移参与表面形状，第四级主要提供毛细细节斜率；这是当前源码的实现选择，不能推广成所有 FFT 海洋的通则。

## 本次证据与边界

实际执行了上游导出的 JS 参数，并用 CPU 翻译的 Stockham 算术与独立朴素 DFT 对照。`N=4/8` 的最大复数误差分别约 `3.95e-15 / 1.72e-14`。这不覆盖真实 `256×1024` 图集隔离、GPU shader、MRT 或半精度数值误差；14项检查中还有源码字符串检查，不是14个完整 GPU 用例。

浏览器水面确实出图，说明当前环境能运行该场景；不能据此证明每个频域采样都数值正确。它仍是实时高度场近似，不是完整流体求解器。

**与已有概念的关联**：
- [[Three.js与场景图]]：场景图组织网格与相机，逐帧纹理提供可见几何的数据源。
- [[泡沫压缩与恢复]]：水平位移导数继续用于判断波面压缩。
- [[先量后优化性能法]]：分别测量 `sim.evolve / sim.fft / sim.assemble / water`，不能把任意分辨率调整都归因于同一种成本。
- [[证据优先质检ProofOverClaims]]：构建、CPU对拍、浏览器视觉各证明不同层。

**固定源码**：[布局与参数](https://github.com/Humpalumps/Ultra-Water/blob/30ea65ecb0a66b137aa200d099965634bdd84d51/src/water/OceanSim.js#L4-L30)、[频谱与打包](https://github.com/Humpalumps/Ultra-Water/blob/30ea65ecb0a66b137aa200d099965634bdd84d51/src/water/OceanSim.js#L50-L141)、[Stockham与装配](https://github.com/Humpalumps/Ultra-Water/blob/30ea65ecb0a66b137aa200d099965634bdd84d51/src/water/OceanSim.js#L143-L195)、[更新循环](https://github.com/Humpalumps/Ultra-Water/blob/30ea65ecb0a66b137aa200d099965634bdd84d51/src/water/OceanSim.js#L304-L347)。

**实验原件**：[数值输出](../../ultra_water/exercise/verification-output.txt)、[可重放脚本](../../ultra_water/exercise/verify-ocean.mjs)。
