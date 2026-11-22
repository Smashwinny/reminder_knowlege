# UI 设计四资源 · 实验日志（task b7a65371-8ba1-44a0-9f05-d0c1a728061f）

实验日期：2026-10-27
上游：pbakaus/impeccable @ d34c87e（浅克隆静态阅读）；getdesign.md / libraries.dev / open-design 经分类阶段核读
边界：构建外部 Rust 引擎被权限层合理拒绝 → 改用自写迷你检测器复刻"确定性规则"概念。

## 四资源分工（核实后）

| 资源 | 角色 | 关键点 |
|---|---|---|
| getdesign.md | 视觉规范参考 | 设计参考站 |
| libraries.dev | 局部组件 | 复制 prompt 接入组件，主要面向 React |
| pbakaus/impeccable | 审查修改 | 1 skill/24 命令/**62 条确定性规则**；PRODUCT.md（产品事实）与 DESIGN.md（视觉方向）分离 |
| nexu-io/open-design | 持续设计工作流 | 设计工作空间，可接现有 agent |

## 步骤与真实输出

### 步骤 1：impeccable 源码静态核实（克隆 @ d34c87e，4422 文件）

- README 宣称：1 skill、24 命令、62 条确定性 detector 规则、免 LLM 免 Key 可跑
- 规则源码 crates/core/src/checks/rules.rs（2969 行）静态阅读，规则 ID 真实存在：
  `ai-color-palette`（紫色标题/紫渐变检测，含 Tailwind `from-purple` 模式）、
  `low-contrast`（低对比度）、`gradient-text`（bg-clip-text+gradient）、
  `gray-on-color`、`side-tab`（边框伪 tab）等
- PRODUCT.md 带 schema 注释（`<!-- impeccable:product-schema 1 -->`），实测含 Platform/Users/Product Purpose/Positioning——"产品事实与视觉方向分离"在自家仓库落实
- 引擎为 Rust workspace（crates/core 规则引擎 + crates/wasm 编译到浏览器扩展），二进制不随仓库分发（`cargo build --release -p impeccable` 构建被拒，如实记录）

### 步骤 2：迷你检测器复刻（自写代码，非 impeccable 二进制）

`exercise/mini_ai_detector.py`（原创练习）按 impeccable 规则思想检测 5 类 AI 味，
对故意堆满 AI 味的示例页 `exercise/ai-tells-sample.html`（Inter/紫蓝渐变/#999 灰字/嵌套卡片/图标砖）实测：

```
检测完成：6 条 AI 味命中
 - Inter 万能字体 / 紫蓝紫渐变 / 灰色辅助文字 #999
 - 卡片套卡片 / 圆角图标砖+渐变底
 - 低对比度正文 #999（2.85:1 < 4.5:1 WCAG AA）   ← 真实 WCAG 对比度公式计算
exit=1（有命中即非零，fail-closed 设计）
```

## 结论

- impeccable 的"62 条确定性规则"真实存在且规则逻辑可读（紫色色相 260-310° 判定等细节专业）；
- "确定性检测器"概念本机复刻成功：6/6 命中示例页全部 AI 味，低对比度用 WCAG 公式算出 2.85:1；
- PRODUCT.md/DESIGN.md 分离 = [[DESIGN.md规范文档]] + [[事实与判断分离]] 的产品化；
- 未验证：impeccable 完整引擎行为（构建被拒）、getdesign.md/libraries.dev/open-design 的实操效果。

## 产物

- `exercise/mini_ai_detector.py` — 迷你 AI 味检测器（自写）
- `exercise/ai-tells-sample.html` — 示例待检页
- `exercise/experiment-log.md`（本文件）
