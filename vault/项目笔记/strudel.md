---
tags: [项目]
类别: 开源项目类
上游仓库: github.com/felixroos/strudel（开发主力已迁 codeberg.org/uzu/strudel，AGPL-3.0）
完成日期: 2026-10-02
---

# strudel

**这是什么**：浏览器端 live coding 音乐环境——TidalCycles（Haskell 模式作曲语言）的 JavaScript 移植。打开 strudel.cc 写一行 `s("bd sd hh cp")` 即出声，改一个字符当场变奏，零安装。热点来源：X 热帖"其实你可以直接用 Claude 做音乐"（[推文](https://x.com/ozzyxs1a/status/2091917895689273843)）。

**它给我什么能力**：零安装作曲 / 算法作曲（欧几里得节奏、随机信号）/ live coding 表演 / pattern 逻辑 headless 单元测试 / 离线渲染音频 / Web Audio 与 DSP 入门。

**引入的概念**：
- [[LiveCoding现场编程]] — 表演艺术与文化场景（algorave）
- [[Mini-notation节奏语言]] — 一行字符串写节奏的 DSL
- [[Pattern时间函数与Hap事件]] — 核心抽象：pattern 是时间的函数，queryArc 查 Hap 事件

**实验记录**（F:\reminder\strudel\exercise\，全部真实运行）：
1. `smoke.mjs` — Node 冒烟：sequence/mini → queryArc 输出分数时间戳事件 ✅
2. `01_mini_notation.mjs` — 8 种 mini-notation 符号逐一实测（`*`压缩、`<>`交替、`bd(3,8)`欧几里得→0/0.38/0.75）✅
3. `02_transforms.mjs` — fast/slow/rev/add/stack 函数式变换实证（fast(2) 事件 8→16）✅
4. `03_render_wav.mjs` — **主实验**：stack(鼓/镲/琶音/贝斯) 100 事件 → 纯 Node 自制合成器渲染 `strudel_jam.wav`（516.8KB/6s/44.1kHz/16bit），Python wave 模块独立验证非静音 ✅ 真实可听
5. Edge 无头截图 strudel.cc 文档页验证在线可用（strudel_repl.png）

**坑与结论**：
- **npm 发布包失修**：@strudel/core@1.2.x dist 依赖 @kabelsalat/web 的 `SalatRepl` 导出，0.3.x/0.4.x 均无 → import 即 SyntaxError；解法=直接 vendor 仓库源码（packages/core+mini，仅依赖 fraction.js）
- 上游已迁 Codeberg；Node 端 "cannot use window" 警告无害
- 音高→频率按 A4=440 换算（c3≈130.8Hz），自制渲染器阈值分类别搞错

**后续可深入的方向**：浏览器 REPL 里让 Claude 生成 pattern 并现场改奏；读 pattern.mjs 源码研究分数时间引擎；试 superdough 合成器与 dirt-samples 采样库；结合 perlin/sine 信号做参数自动化。
