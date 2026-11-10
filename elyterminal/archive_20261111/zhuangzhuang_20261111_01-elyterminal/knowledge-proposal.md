# ELYTerminal 候选知识提案（未合入）

## 查重与来源
知识库 main：`a8674777e18302b8804b137212b1396cbfe5a747`。已读总览、设计令牌DesignToken、可逆派生状态、开源验货三查、证据优先质检ProofOverClaims；vault 严格关键词未发现 ELYTerminal 专项成果。旧式宽匹配 PTY 曾误中 empty 的 pty，保留但不计相关成果。
上游：`https://github.com/ELY-Open-Source/ELYTerminal/tree/9504b5382f3b47b0377063fa3b78cb706f44ed08`；访问 2026-11-11（Asia/Shanghai）。原帖 `https://x.com/i/status/2113499695586721857` 全文及三图已读，无引用帖字段；原图 v0.1.8，当前 main 包版本 0.2.4，不混作同一版本。

## 建议新增概念：终端语义标记与光标输入路由
定义：终端经 PTY 接收字节，以 OSC 133 的 A/B/C/D 区分提示符、输入、输出和退出，再按 shell 所报告的点击模式把有效输入区点击转换为方向键或 SGR 鼠标事件。
领域：桌面终端 / 交互协议。关联 [[可逆派生状态]]、[[Agent输出协议契约]]、[[证据优先质检ProofOverClaims]]。
具体案例：上游 marks.rs 接受 A/N、B/I、C、D；Click 包含 Arrows/Absolute/Relative。click.rs 仅在 Reading 且程序没有鼠标跟踪时尝试定位；备用屏幕与输入区外拒绝；宽字符占位格不计为一次额外移动。
证据：真实运行上游 Bash 集成四场景，捕获 18 标记；未改动 marks.rs 的 3 个上游测试通过，并解析真实捕获。没有执行 click.rs 的 GUI 路由或其网格测试，不能宣称全路径通过。

## 对已有概念仅追加案例
- [[设计令牌DesignToken]]：透明度叠加后的相邻颜色才是对比度对象。九个合成场景淡高亮 1.020013–1.298294:1；深色边也在一个深壁纸/低不透明度场景跌到 2.234323:1。不是 Ely Light 实机色值，不证明 macOS bug；WCAG 3:1 仅作为必要非文本指示参考。
- [[可逆派生状态]]：当前 status.rs 显示优先级 blocked > error > working > done > idle；程序报告 done 不是独立业务验收。这里只读源码，不称实跑状态机。
- [[开源验货三查]]：本次 MIT LICENSE 实读，两个再分发组件附完整许可；整体产品另含字体和第三方通知，主代码 MIT 不替代组件核查。
- [[证据优先质检ProofOverClaims]]：分开“作者主观体验”“文档能力”“组件实跑”“数值模型”“原生产品效果”；3 个测试不是 3 条断言，更不是完整项目测试。

## 项目笔记建议：vault/项目笔记/elyterminal.md
定位：Rust/GPUI 原生终端；左会话、中终端、右 Git/Files；shell/PTY 与窗口分层。
实验：六步组件主实验，详见 experiment-log.md。完整应用要求 Rust 1.95，而云端 1.85.1，仅独立 parser crate 编译；GUI、多会话、宠物、macOS 27 透明高亮、中文/折行点击及性能均待验证。
产物：中文 12 问内联 SVG 单文件 HTML、A4 PDF（实际状态见 pdf-review.md）、练习 ZIP、日志及 sources 清单。
本提案不修改总览累计计数、不自动合入、不提交/发布、不勾选用户任务。建议由总协调者复核后处理。
