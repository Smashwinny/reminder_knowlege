<!-- vault/概念/FFT海面级联.md -->
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


---

<!-- vault/概念/异步GPU读回与计时.md -->
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


---

<!-- vault/概念/泡沫压缩与恢复.md -->
---
tags: [概念]
领域: 实时海洋 / 泡沫生成
别名: [Jacobian Foam, Wave Compression Foam]
首次来源: "[[项目笔记/ultra_water]]"
---

# 泡沫压缩与恢复

**一句话定义**：利用水平位移映射的面积压缩量产生泡沫记忆，再按时间步恢复，使泡沫不只是由波峰高度阈值触发。

**通俗理解**：把有网格的橡皮纸往中间挤，格子面积缩小。Jacobian行列式 `J` 衡量这种局部面积变化；实时海面用它近似判断哪里容易形成白沫，并保留一点时间上的记忆。

## 从导数到可见泡沫

固定源码先将水平位移导数乘以choppiness系数，再计算：

```text
J = (1 + dxx) * (1 + dzz) - dxz * dxz
turb = min(J, previous + dt * recovery / max(J, 0.5))
```

`J=1` 为无水平面积形变参考，较小值表示压缩；负值意味着局部映射翻转风险。`min` 让压缩时的下降立即跟随，恢复时只能按dt逐步上升，并在J处封顶。这里的`turb`是后续着色的中间量，不是直接测到的气泡体积或泡沫覆盖率。

固定J且没有封顶时，公式的恢复项对累计时间呈线性。实际海面J会变，且含纹理采样与着色，因此不能由这个代数性质宣布整个泡沫系统帧率无关。

本次CPU用例比较6步与60步，最终都饱和到 `J=0.8`；它验证固定J示例的截断结果，不是动态泡沫验证。开发时曾把期望误写0.86，核查公式后修为0.8，失败与修订保留在[实验日志](../../ultra_water/exercise/experiment-log.txt)。

海面另有近岸白浪、接触泡沫与纹理。`foamScale`是后续映射参数，`caustics`控制水下聚光；关掉焦散后的沙底变化不能当作泡沫公式被验证的证据。

**与已有概念的关联**：
- [[FFT海面级联]] 提供位移导数，Jacobian是频谱计算到视觉效果的中间量。
- [[先量后优化性能法]]：先分清风浪、压缩系数和着色覆盖，再决定调整哪项参数。
- [[证据优先质检ProofOverClaims]]：数值样例、动态纹理与最终画面要分别验收。

**边界**：高度场泡沫是实时近似，不模拟气泡体积、两相流或卷浪管道；本轮未验证GPU泡沫纹理的数值正确性。

**固定源码**：[Jacobian与恢复公式](https://github.com/Humpalumps/Ultra-Water/blob/30ea65ecb0a66b137aa200d099965634bdd84d51/src/water/OceanSim.js#L169-L195)、[海面泡沫组合](https://github.com/Humpalumps/Ultra-Water/blob/30ea65ecb0a66b137aa200d099965634bdd84d51/src/water/OceanSurface.js#L647-L710)。


---

<!-- vault/项目笔记/ultra_water.md -->
---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/Humpalumps/Ultra-Water
学习日期: 2026-11-11
上游版本: 30ea65ecb0a66b137aa200d099965634bdd84d51
---

# Ultra-Water：从频谱海面到浏览器证据

**这是什么**：基于Three.js/WebGL2的实时海洋示例，把频谱风浪、近岸浪、泡沫、反射、折射、焦散、水下合成与浮体查询接成一条渲染管线。包名为 `gelatin-game-engine`，不应据此认错上游项目。

**它给我什么能力**：搭建海面视觉原型；理解频域到空间域的海浪计算；隔离水体光学通道；研究延迟水高驱动浮体；学习分层取证和GPU计时口径。它不是完整流体物理或跨设备性能保证。

## 新知识与已有知识

- [[FFT海面级联]]：四种世界尺度、16个Stockham pass、复场打包与居中频移复原。
- [[异步GPU读回与计时]]：在途上限、结果时间/tag、fence和query的不同含义。
- [[泡沫压缩与恢复]]：Jacobian驱动的压缩记忆及dt恢复。
- 关联 [[Three.js与场景图]]、[[先量后优化性能法]]、[[证据优先质检ProofOverClaims]]；不再新建同义的“GPU Timer Query”或“构建不等于通过”笔记。

查重基线是知识仓库main `a8674777e18302b8804b137212b1396cbfe5a747`，只读相关三篇旧概念与总览，结合完整非截断文件树确认三个新名称及本项目笔记不存在。网站知识快照共35篇/193块的重构校验已通过；关键词未命中本专题不等于精读全vault或断言用户没学过。

## 一次五步主实验：真实结果分层记录

1. **冻结输入**：Node `v24.21.0`、npm `11.19.0`，上游固定 `30ea65ecb0a66b137aa200d099965634bdd84d51`。研究与练习均绑定此版本。
2. **安装并构建**：`npm ci --ignore-scripts --no-audit --no-fund` 与 `npm run build` 实际退出0；锁定three0.186.1、lil-gui0.21.0、Vite8.3.5。主包751.48kB触发chunk大小警告，未阻断。
3. **检查上游JS与参数边界**：练习直接执行上游导出的常量/函数及提取的JONSWAP函数；零/负风速、fetch可产生非有限参数，JSON中的null不等于有效数值0。
4. **CPU数值对照**：最终输出 `SUMMARY checks=14 status=PASS gpu=NOT_TESTED`。`N=4/8` Stockham与独立DFT最大误差约 `3.95e-15 / 1.72e-14`。其中含源码字符串检查；不覆盖GPU、真实大图集隔离、MRT或fp16。泡沫固定J用例两路均饱和到0.8，不是动态泡沫验证。
5. **浏览器实际操作**：本机启动Vite，Chrome显示Lagoon水面；Water/caustics从1置0后沙底网状亮纹消失，恢复1并切Underwater后可见水下雾与底部焦散。时间继续流动，所以是可见单参数对照，不是同一模拟帧的像素差分。新标签受控日志无warn/error，先前标签出现过精度警告，不能宣称所有运行均无警告。

基准补充：RTX4070、1660×1053、4×MSAA、Lagoon的内置按钮返回一次 `2.38 ms/frame = 420 fps (GPU 2.34 ms)`。源码暂停常规循环但连续推进模拟帧；`drain()`未检查disjoint。本轮没有独立复测热态、disjoint或稳定分布，只保留UI观察值。普通后台HUD约1FPS不能代表GPU吞吐。

## 实验中踩到的坑

- 首版恢复期望误写0.86，实际被J=0.8截断；修正oracle并保留失败记录。
- 首版二维DFT参考漏掉 `(-1)^(x+y)`，造成棋盘符号差异；核对固定上游后补齐，不放宽误差阈值。
- `nearSurface`在源码中包括所有水下位置及高于水面不足约1.2m的位置，不是只包含狭窄水线带。反射跳过判定另用相机低于查询水面约0.3m。
- 构建、CPU、画面和计时是四层证据；其中任一层通过都不能包办其它层。

## 学习材料与可重放原件

- [彩色小白指南PDF](../../ultra_water/Ultra-Water-小白指南.pdf)、[单文件HTML](../../ultra_water/Ultra-Water-小白指南.html)：12问、12张机制SVG、5用途、5步主实验。最终页数和文件字节由交付审核记录，不在笔记中先行猜测。
- [练习说明](../../ultra_water/exercise/README.md)、[数值脚本](../../ultra_water/exercise/verify-ocean.mjs)、[输出](../../ultra_water/exercise/verification-output.txt)。
- [本地实验日志](../../ultra_water/exercise/experiment-log.txt)、[协调者浏览器观察](../../ultra_water/exercise/browser-experiment-evidence.txt)。浏览器截图在本轮工具记录中已查看，本链接不冒称包含本地截图文件。

后续可深入：真实GPU图集隔离和误差采样；异步水高的新鲜度/tag验证；固定时间、固定输入的图像对照；有效disjoint检查与重复基准。任务完成勾选由本人决定；这份知识笔记不证明网站标签或Git发布状态已经改变。

**一手来源**：[固定上游README](https://github.com/Humpalumps/Ultra-Water/blob/30ea65ecb0a66b137aa200d099965634bdd84d51/README.md#L1-L156)、[渲染入口](https://github.com/Humpalumps/Ultra-Water/blob/30ea65ecb0a66b137aa200d099965634bdd84d51/src/main.js#L371-L435)、[基准实现](https://github.com/Humpalumps/Ultra-Water/blob/30ea65ecb0a66b137aa200d099965634bdd84d51/src/main.js#L443-L475)、[MIT许可](https://github.com/Humpalumps/Ultra-Water/blob/30ea65ecb0a66b137aa200d099965634bdd84d51/LICENSE#L1-L21)、[第三方声明](https://github.com/Humpalumps/Ultra-Water/blob/30ea65ecb0a66b137aa200d099965634bdd84d51/THIRD_PARTY_NOTICES.md#L1-L46)。公开交付仅包含学习成果与练习，不包含克隆的repo、缓存、凭据或私有原记录。
