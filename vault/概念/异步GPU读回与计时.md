---
tags: [概念]
领域: WebGL2 / GPU-CPU同步
别名: [Async GPU Readback, PBO Fence]
首次来源: "[[项目笔记/ultra_water]]"
---

# 异步GPU读回与计时

**一句话定义**：把 GPU 工作的提交和结果消费分开，避免即时等待；数据读回回答“算出了什么”，计时查询回答“这段工作花多久”，二者不能互相替代。

**通俗理解**：寄出检验样本后先做别的事，等回执到达再使用结果。异步只改变等待方式，不保证结果新鲜或调用永不出错。用于物理的水高还要附带采样时间和布局标记。

## 水面查询：迟到的数据必须能识别

Ultra-Water 的 `WaterQuery` 在一个窄渲染目标中计算水高和水平位移，调用 Three.js `readRenderTargetPixelsAsync()`。最多允许两个请求在途；完成后写入 `resultCount / resultTag / resultTime`。容量是256的构造默认值，主程序实例化为512。源码注释称通常滞后1–3帧，该数字是作者描述，本轮未实测延迟分布。

GPU结果由稍后的浮体积分使用。240Hz物理子步不等于每个子步都取到了新的GPU水高。错误处理的 `.catch(() => {})` 会吞掉异常；仅看“没报错”不够，应检查结果时间与计数是否持续变化，并拒用旧布局的tag。

底层PBO/fence属于读回实现机制；本轮只核查应用层调用与注释，没有以此代替 Three.js 依赖源码审计或驱动级证明。

## 计时：普通帧循环与批量基准不同

- 普通HUD帧间隔受显示同步、页面后台调度和CPU工作影响，不等于GPU执行时间。
- `GpuTimer.endFrame()` 用 `EXT_disjoint_timer_query_webgl2` 延迟读取每个pass的query结果，并在disjoint时跳过；队列过长会丢弃积压。
- 内置基准暂停常规渲染循环，先预热20帧，再连续调用 `renderFrame(1/200)` 300次并等待GPU fence。模拟仍在推进，不能称为同一静止帧的重复渲染。
- 基准以墙钟总耗时除以300得到 `ms/frame`，另汇总各pass query。`drain()` 路径未检查disjoint，因此不能把普通路径的过滤保证直接套到基准结果上。

本机UI曾报告 `2.38 ms/frame` 与 `GPU 2.34 ms`（RTX4070、1660×1053、4×MSAA、Lagoon）。它只是一次内置基准观察；没有独立验证disjoint状态、热态与重复性，不构成优化结论或跨设备承诺。详见[浏览器实测记录](../../ultra_water/exercise/browser-experiment-evidence.txt)。

**与已有概念的关联**：[[先量后优化性能法]] 已包含测量纪律，本笔记只补充读回协议、结果新鲜度和具体计时路径；[[证据优先质检ProofOverClaims]] 要求把观察值与测量有效性分开记录。

**固定源码**：[WaterQuery](https://github.com/Humpalumps/Ultra-Water/blob/30ea65ecb0a66b137aa200d099965634bdd84d51/src/water/WaterQuery.js#L5-L58)、[实例化与消费者](https://github.com/Humpalumps/Ultra-Water/blob/30ea65ecb0a66b137aa200d099965634bdd84d51/src/main.js#L83-L88)、[GPU计时器](https://github.com/Humpalumps/Ultra-Water/blob/30ea65ecb0a66b137aa200d099965634bdd84d51/src/engine/gpuTimer.js#L1-L69)、[fence与基准](https://github.com/Humpalumps/Ultra-Water/blob/30ea65ecb0a66b137aa200d099965634bdd84d51/src/main.js#L443-L475)。
