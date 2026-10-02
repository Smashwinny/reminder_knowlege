---
tags: [概念]
领域: 音乐技术 / 函数式编程
别名: [pattern as function of time, Hap, queryArc]
首次来源: "[[项目笔记/strudel]]"
---

# Pattern时间函数与Hap事件

**一句话定义**：Strudel/Tidal 的核心抽象——pattern 不是音频数据，而是"时间区间 → 事件列表"的函数：`queryArc(b, e)` 返回该区间内的 Hap（事件 = 起止时间 + 内容），时间用分数保证二分/三分节奏永不丢精度。

**属于领域**：函数式响应式编程、音乐信息学。

**通俗理解**：把 pattern 想成"乐谱查询机"——你问它"第 3 到第 4 小节有什么"，它吐出一张精确到毫厘的演出时刻表，声音引擎照单发货。因为 pattern 是函数，`fast(2)`/`rev()`/`add(3)` 这些变换就是函数组合：不修改原谱，而是派生新谱。讲完落回术语：Tidal 论文标题即 "pattern as a function of time"，Strudel 用 JavaScript 复刻了这一模型（`@strudel/core/pattern.mjs` 约 1300 行）。

**实测要点**（来自 strudel 实验）：
- `sequence('a',['b','c']).queryArc(0,1)` → `a: 0-1/2, b: 1/2-3/4, c: 3/4-1`（嵌套自动均分）
- `.fast(2)` 事件数翻倍坐标减半；`.slow(2)` 反之；`.rev()` 坐标倒序；`.add(3)` 音符整体移调
- 事件坐标是 Fraction 对象，画图前要 `Number()` 转换
- **headless 可跑**：谱面→事件是纯计算，无声卡也能在 Node 验证，再自写合成器渲染成 wav

**与已有概念的关联**：
- 相关：[[Mini-notation节奏语言]]（pattern 的文本来源）、[[LiveCoding现场编程]]（表演场景）
- 与 [[确定性脚本]] 同源：同输入必同输出，可写单元测试断言"歌对不对"

**首次接触于**：[[项目笔记/strudel]]
