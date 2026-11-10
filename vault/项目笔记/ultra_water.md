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
