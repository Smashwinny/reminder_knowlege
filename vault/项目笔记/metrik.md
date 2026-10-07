---
tags: [项目笔记, 开源项目, 用量计量]
学习日期: 2026-10-05
固定上游: 637444bdc8d91475f66f5319a15dda0e4be1c652
版本: v0.21.1
许可: AGPL-3.0-or-later
验证范围: 离线 JavaScript 额度选择、托盘决策与格式化组件
---

# Metrik

## 是什么，能学到什么

[keros68/metrik](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/README.md) 是聚合多个 AI 编程工具官方额度、本地用量与参考费用的 Tauri 桌面仪表盘。理解它的关键是先拆开数据口径，再理解主读数怎么被选择。固定版本为 v0.21.1、AGPL-3.0-or-later；练习包保留所需上游原模块、原测试、完整许可证与文件指纹。

可以用这次材料学习：判断读数来源与单位；分辨未知、真零、陈旧与旧周期失效；写可复现的边界场景；用源码对照 README 简写；给解析、去重、账单和界面验收分别记证据。项目没有自有云服务不等于所有路径都不联网，配额查询、可选仪表盘与更新检查不属于本次执行范围。

## 概念查重与合并

- 新增 [[用量、额度与估算费用的计量分层]]：来源、单位与时间范围的独立建模；与网关归因、账户分工和预算执行各自分工
- 新增 [[多窗口额度的展示选择规则]]：有效性、单位、15% 阈值与稳定顺序；与跨源归一化、LLM 确定性选择器相关而非同义
- 增补 [[meta新鲜度声明]]、[[单一馈送与schema冻结]]：未知与真零分开；stale 不等于 resetExpired，格式化不能吞掉可用性与金额单位
- 增补 [[JSONL事件日志与折叠模型]]：累计差分、事件身份与来源观察；只保留源码审阅结论，不借 JS 测试证明后端去重
- 增补 [[BYOK模型网关与用量归因]]、[[付费调用回执与预算熔断]]：观察、归属、估价、结算与硬停分别取证
- [[缓存]]、[[缓存有效期与发布边界]]、[[双时钟模型]] 只建立时效相关链接，不移植 TTL 或把不同时间模型当同义词
- [[双数据源适配器隔离]]、[[数据源降级链]]、[[本地优先与文件监听]]、[[Tauri桌面应用框架]]、[[派生会话ID与结构脱敏]] 用作架构对照，不把其他项目的行为当成 Metrik 实测

## 实验做了什么

已有学习实验在 Linux x64 / Bash / Node.js v24.19.0 中直接执行固定版本 quotaWindows.js、trayBadge.js、tokenFormat.js，未安装依赖。五步是：确认运行时、核对上游文件与许可、运行上游测试、运行合成场景、重放核对。原学习 ZIP 已在全新目录按教材打印命令独立复现。

- 23 项未修改的上游 JavaScript 测试通过，失败与跳过均为 0
- 27 个另列的合成 JavaScript 场景通过，逐场景重放两次，输入记录与实际输出一致
- 四个后端阅读例子明确未执行，不计入实测通过数；这不是 50 项上游测试

本次公开整理复用上述已完成实验与审核记录，没有重新执行学习实验。Node 文件权限参数不是网络隔离证明；已审阅的实验执行路径没有网络调用，输入全部为合成数据。

## 关键结论与坑

1. 正常取预排序有效首项，非余额窗口 ≤15% 才由告急项中的最小值接管；README 的“最低余量”简写不能替代完整规则
2. 不可用不是零，stale 不是旧周期失效；跨重置点只排除旧读数，不证明新周期已查到 100%
3. 余额的 remainingPercent 字段实际承载金额，8.4 不是 8.4%，168.5 也不是需要钳制的百分比
4. trayBadgeSpec 取第一个 Agent；金额保护在 App.jsx 调用层，该层仅源码审阅；原生托盘画布未执行
5. compactTokens(null) 返回字符串 0，不能据此判断完整 UI 误报，也不能把它当数据完整性的证据
6. 重复窗口输入保留不变只证明选择器未改输入，不证明 Rust 解析或数据库去重；Token 归一化与账本合并均为静态源码观察
7. 固定引擎使用 182 天解析视界和约 1500 毫秒文件间预算；界面查询周期不同于解析覆盖。旧架构说明的按界面周期扩扫不可直接当当前行为，这部分未执行

## 验证边界

没有运行 Rust/Cargo、完整 npm/build、真实 Agent 日志、Token 后端归一化、SQLite 事务与事件去重、真实提供方配额/余额、认证、实际账单、预算硬停、多设备同步、Tauri 全应用、Windows/macOS/Linux 原生 UI 或托盘画布。未验证 Windows/PowerShell、其他 Node 主版本及原推文正文。不能由组件通过外推完整应用或跨平台正确。

原 PDF 使用 ReportLab 直接生成并逐页渲染检查；HTML 只有结构、锚点、文本与来源检查，没有浏览器视觉或浏览器打印验收。公开副本的整理与原学习审核应分别阅读，见下方材料。

## 最新公开知识库读取范围

本次合并基于 GitHub main 快照 eef57f1408874be6db8b7f82dfe727c6b79265e7，完整读取 MOC、学习方法、仓库说明、两份模板、18 篇相关概念与三篇相关项目笔记，并逐文件核对 Git blob SHA、UTF-8 字节数和 SHA-256。该树有 302 篇概念，其余 284 篇只做路径/标题层筛查，不能称作全库正文查重，也不代表其他副本或未发布笔记已经核对。

18 篇概念为：[[BYOK模型网关与用量归因]]、[[JSONL事件日志与折叠模型]]、[[meta新鲜度声明]]、[[缓存]]、[[缓存有效期与发布边界]]、[[付费调用回执与预算熔断]]、[[双数据源适配器隔离]]、[[数据源降级链]]、[[双时钟模型]]、[[本地优先与文件监听]]、[[Tauri桌面应用框架]]、[[派生会话ID与结构脱敏]]、[[可逆派生状态]]、[[证据状态机]]、[[单一馈送与schema冻结]]、[[跨源评分归一化]]、[[规划执行分账]]、[[确定性选择器模式]]。项目对照为 [[项目笔记/codex-claude-resets]]、[[项目笔记/codex_quota_mcp]]、[[项目笔记/google_colab_cli]]；不迁移其历史套餐、价格、政策、测试数量或平台验证。Easel 与 Colab 的已有公开内容原样保留。

本次新增两篇概念、增补五篇已有概念，不重写 MOC 的历史累计计数；学习材料与知识整理完成不等于本人已掌握全部内容。

## 六类学习材料

- [彩色 PDF 指南](../../metrik/delivery/01-guide.pdf)
- [HTML 指南](../../metrik/delivery/02-guide.html)
- [离线练习包](../../metrik/delivery/03-exercise.zip)
- [实验日志](../../metrik/delivery/04-experiment-log.md)
- [知识笔记](../../metrik/delivery/05-knowledge-notes.md)
- [审核日志](../../metrik/delivery/06-review-log.md)

## 固定来源

- [README](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/README.md)、[开发说明](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/docs/development.md)、[LICENSE](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/LICENSE)
- [窗口规则](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src/quotaWindows.js)、[上游窗口测试](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src/quotaWindows.test.js)
- [托盘决策](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src/trayBadge.js)、[Token 格式化](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src/tokenFormat.js)、[App 调用层](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src/App.jsx)
- [TokenVector](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src-tauri/src/domain.rs#L59-L120)、[定价实现](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src-tauri/src/pricing.rs)
- [Codex 适配器](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src-tauri/src/adapters/codex.rs#L250-L390)、[Claude 适配器](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src-tauri/src/adapters/claude.rs#L114-L195)、[账本](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src-tauri/src/storage.rs#L157-L460)
- [引擎](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src-tauri/src/engine.rs)、[配额刷新](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src-tauri/src/quota.rs)
