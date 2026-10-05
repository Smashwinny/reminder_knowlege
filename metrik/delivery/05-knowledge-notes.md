# Metrik 知识笔记与公开概念关联

日期：2026-10-05 UTC。固定上游：keros68/metrik，v0.21.1，提交 637444bdc8d91475f66f5319a15dda0e4be1c652；许可 AGPL-3.0-or-later。

这是 2026-10-05 历史学习成果的公开整理。执行结论限于原 JavaScript 实验；公开整理未重新学习或新增实测。知识关联限于列出的已读公开来源。

## 当前公开整理结果

以下历史正文保留原学习时的概念提案和知识关联。此次按公开知识库较新的正文完成同义查重后，采用了以下整理结果；历史段落中的“候选”“入库建议”不表示这些决定仍未落实。

- 新建两个概念：[用量、额度与估算费用的计量分层](../../vault/概念/用量、额度与估算费用的计量分层.md)、[多窗口额度的展示选择规则](../../vault/概念/多窗口额度的展示选择规则.md)
- 在五篇既有概念末尾增补 Metrik 案例，保留原文：[JSONL事件日志与折叠模型](../../vault/概念/JSONL事件日志与折叠模型.md)、[meta新鲜度声明](../../vault/概念/meta新鲜度声明.md)、[BYOK模型网关与用量归因](../../vault/概念/BYOK模型网关与用量归因.md)、[付费调用回执与预算熔断](../../vault/概念/付费调用回执与预算熔断.md)、[单一馈送与schema冻结](../../vault/概念/单一馈送与schema冻结.md)
- 新建 [Metrik 项目笔记](../../vault/项目笔记/metrik.md)，并向知识索引增加入口
- 只整理与互链已有证据，没有新增实验；后端 Rust、真实配额、账本去重、账单和原生界面的未验证边界保持不变

## 历史学习正文

## 1. 查重范围与证据等级

- 固定公开索引包含 394 条元数据；本次全文读取并核对 14 篇相关正文，其他 380 篇只有元数据检索，不能宣称全库全文查重
- 公开正文固定于 1043e9d6080bff7af9724162e2c44559fab63e40；公开知识索引固定于 1f61909da967cea8bc68dbfaffc642a4331b3352
- Metrik 执行证据只覆盖真实 JavaScript 函数；Rust 架构结论标为源码审阅，不能借旧项目测试或本轮 JS 测试替它背书

## 2. 先复用，避免同义笔记越堆越多

1. [[JSONL事件日志与折叠模型]]：不重新定义 JSONL；增补“累计量先差分、事件身份与来源观察分离”的计量案例。JSONL 格式本身不会自动带来幂等、容错或完整性
2. [[meta新鲜度声明]]、[[缓存]]、[[缓存有效期与发布边界]]：增补陈旧、未知与跨重置点的区别。旧项目缓存时长不能当 Metrik 刷新周期
3. [[双时钟模型]]：只建立相关链接。旧概念的内容回放/呈现时钟，与采样时间/当前时间/额度重置时刻并非同一术语，不做同义合并
4. [[BYOK模型网关与用量归因]]、[[付费调用回执与预算熔断]]：关联计费路由、估算和账单；显示配额不是预算硬熔断，不能保证停止推理或不超支
5. [[双数据源适配器隔离]]、[[数据源降级链]]：关联不同 Agent 的来源边界。回退来源成功不等于同一账户、同一时间范围或完整统计
6. [[本地优先与文件监听]]、[[Tauri桌面应用框架]]：只回顾架构。Metrik 的“没有自有云服务”不代表不联网；配额、Cursor 可选仪表盘和更新检查仍有网络路径
7. [[派生会话ID与结构脱敏]]：关联同步字段最小化；哈希标识不等于匿名，也不自动是去重身份
8. [[codex-claude-resets]]、[[codex_quota_mcp]]：只复用证据分级和计量口径辨别方法；历史价格、政策、次数或账户额度未经本轮复核，不搬成当前事实

## 3. 候选概念：用量、额度与估算费用的计量分层

一句话定义：本地处理量、官方窗口余量、按公开价格折算的参考费用与实际结算账单，具有不同来源、单位和时间范围，不能互相替代。

领域：软件可观测性、AI 用量计量、数据建模。

四种事实：
- 本地处理量来自日志或特定来源的用量事件，单位是 Token
- 官方额度来自提供方的窗口快照，常是百分比或 Credits；余额窗口则是货币金额
- API 估算费用按模型和 Token 组成计价，缺少价格时应保留未计价状态
- 真实账单涉及实际套餐、价格、折扣和结算；本实验没有读取或验证

Metrik 的处理量口径：未缓存输入 + 缓存读 + 缓存写 + 输出。推理输出是输出子项，不重复加总。不同来源的 input 口径必须经适配器归一。以上后端口径为源码审阅，未执行 Rust。

例：100 未缓存输入 + 200 缓存读 + 50 缓存写 + 30 输出（其中推理 10）= 380，而不是 390。该式是教学算例，不能说它是本次后端测试结果。

关联：[[BYOK模型网关与用量归因]]、[[付费调用回执与预算熔断]]、[[codex_quota_mcp]]。

入库建议：先在所用知识库查找同义概念；已有同义项就增补 Metrik 案例，不另建同名变体。

来源：
- https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/docs/guide.md
- https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src-tauri/src/domain.rs#L59-L120
- https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src-tauri/src/pricing.rs

## 4. 候选概念：多窗口额度的展示选择规则

一句话定义：多个周期同时约束使用时，显示哪个余量是一条包含可用性、单位、阈值和稳定排序的策略，不等同于无条件求最小值。

领域：交互信息压缩、状态选择、可观测性界面。

固定版本的真实规则：
1. 去掉 available=false 或 resetExpired=true 的窗口
2. 不因 stale=true 单独排除；函数也不自行推导新鲜度或对窗口排序
3. 若非余额型窗口中存在 remainingPercent≤15，选这些告急窗口中数值最小的；同值保留输入顺序
4. 否则返回有效列表第一项，依赖后端预排序契约
5. 余额通过 key.startsWith("balance") 识别；金额不参加百分比告急筛选，但仍可作为有效首项正常选中

实测：短窗 80% / 周窗 40% 选 80%；周窗 15% 选 15%；周窗 15.01% 又选 80%。余额 8.4 不因数值小就接管百分比窗口；余额 168.5 不在选择器中被钳为 100。

对照资料：README 与 guide 的“取余量最低”是简写，不能代替函数规则。此函数也不验证整个输入 schema，更不是账户额度查询或预算执行器。

关联：[[meta新鲜度声明]]、[[codex-claude-resets]]、[[数据源降级链]]。与“额度是什么”相关，但这里专指显示选择策略。

入库建议：经同义查重后再决定独立概念或作为计量分层的子节。

来源：
- https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src/quotaWindows.js
- https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src/quotaWindows.test.js

## 5. 优先增补：读数新鲜度与周期有效性

一句话定义：一次读数被观察到多久，以及它所属的额度周期是否已经结束，是两条独立判断。

领域：缓存一致性、时序状态、信息可信度。

增补到 [[meta新鲜度声明]]，链接 [[缓存]]，不要把它与 [[双时钟模型]] 当同义概念合并。

Metrik 案例：
- 不可用是未知，不是 0%；有效的 0 才表示零余量
- stale 但尚未跨重置点的窗口仍可选择，并保留陈旧提示
- resetExpired 表示记录的重置点已过，选择器排除旧周期读数；这不证明新周期已经查询到 100%
- trayBadge 对 null 输出 --，对 0 输出 0；tooltip 和状态指纹均保留陈旧位
- compactTokens(null) 却输出 "0"，因此必须保留调用层可用性信息，不能让格式化文本替代状态证据。此次没有测试完整 UI，不能由此断言产品误报

实际执行范围：已有状态位进入 JavaScript 后的行为。后端如何计算 age、stale、resetExpired，配额 TTL、重试、鉴权与刷新仅源码审阅。

来源：
- https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src/quotaWindows.js
- https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src/trayBadge.js
- https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src/tokenFormat.js
- https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src-tauri/src/engine.rs#L1343-L1372

## 6. 在既有 JSONL/折叠笔记里增补的项目案例

不要把“日志行数”当“用量事件数”。Codex 累计快照要差分，分叉继承的历史不能新算；Claude 的同一 provider message ID 可渐进补齐 Token 组成，按组成最大值合并。事件身份与来源观察分离，同一事实出现在两个文件不应算两遍。

边界：这些是对固定版本 Rust 实现的静态核对，没有 Rust/Cargo 运行证据。本轮 exact_duplicate_window 只证明选择器没有改动输入，不能证明数据库去重。

覆盖也不能混淆：当前引擎固定 182 天解析视界，界面周期只是查询范围；约 1500 毫秒解析预算在文件间检查，未处理来源等待回填。旧 ARCHITECTURE 中按 Today/7/30 天扩扫的描述已滞后。没有实测这套回填流程。

来源：
- https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src-tauri/src/adapters/codex.rs#L250-L390
- https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src-tauri/src/adapters/claude.rs#L114-L195
- https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src-tauri/src/storage.rs#L157-L460
- https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src-tauri/src/engine.rs#L30-L44

## 7. 项目笔记提案：Metrik

是什么：将多个 AI 编程工具的官方额度与本地用量放进桌面仪表盘，以统一事件账本支撑统计；参考成本单列。

关联概念：[[用量、额度与估算费用的计量分层]]、[[多窗口额度的展示选择规则]]（以上两个名称仍是候选）、[[JSONL事件日志与折叠模型]]、[[meta新鲜度声明]]、[[BYOK模型网关与用量归因]]、[[Tauri桌面应用框架]]。

本次做了什么：Linux x64、Node.js v24.19.0，直接执行固定版本的 quotaWindows.js、trayBadge.js、tokenFormat.js。五步是检查运行时、核验源文件、上游测试、合成场景、双重重放。23 个上游测试与 27 个合成场景分别全部通过；四个后端阅读例子标为未执行。最终 ZIP 全新解压后按打印命令复跑成功。

最重要结论：正常选预排序有效首项，≤15% 才由百分比告急窗中的最小值接管；类型、时间、可用性必须与数值一起传递。

坑：源码比 README 的简写更精确；格式化的 0 可能丢失缺失语义；选择器不负责排序与输入验证；一份重复窗口输入不是账本去重实验。App.jsx 调用层会屏蔽余额进入百分比徽标，trayBadgeSpec 本身并不识别余额类型；这段调用链仅源码审阅。

未验证：Rust 日志解析/去重/SQLite/Token 归一化、真实账号额度与账单、配额时效计算、同步、整套 Tauri、原生平台显示及托盘画布。没有执行实际安装或修改个人电脑。

许可：固定版本为 AGPL-3.0-or-later，练习包保留完整许可证、完整所需原模块/测试与来源指纹，不沿用更旧版本许可。

## 8. 知识组织建议

1. 在项目索引中增加 Metrik，链接上述概念与本次实验结论
2. 先将新鲜度案例并入原概念；计量分层与显示策略做同义查重后再决定新增
3. 日志差分与去重只做项目案例，保留“源码审阅、未执行”的边界
4. 复用本报告时检查已有笔记与关联，保留原文，避免同义概念重复或把源码审阅升级为实测

## 9. 本次实际全文读取的公开知识来源

以下是已读正文的标题、固定 URL 与 SHA-256；未附正文。不以目录索引冒充实际阅读。

1. BYOK模型网关与用量归因；1697 UTF-8 字节
   来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/BYOK%E6%A8%A1%E5%9E%8B%E7%BD%91%E5%85%B3%E4%B8%8E%E7%94%A8%E9%87%8F%E5%BD%92%E5%9B%A0.md
   SHA-256：27d76f60753171c92bdd2c12a8cb33e74dbe266bbd90537e716bdb760ef69dd3

2. JSONL事件日志与折叠模型；1776 UTF-8 字节
   来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/JSONL%E4%BA%8B%E4%BB%B6%E6%97%A5%E5%BF%97%E4%B8%8E%E6%8A%98%E5%8F%A0%E6%A8%A1%E5%9E%8B.md
   SHA-256：8346f3ddd229a2fb8fe929ee0a4916f44ecf17700818581ef3f57c4c7495a5ea

3. Tauri桌面应用框架；1832 UTF-8 字节
   来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/Tauri%E6%A1%8C%E9%9D%A2%E5%BA%94%E7%94%A8%E6%A1%86%E6%9E%B6.md
   SHA-256：2ddc620badf0aaa04ebdb10bc50f11e422939ffd2254cc082c20af4fea84b44f

4. codex-claude-resets；3316 UTF-8 字节
   来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/codex-claude-resets.md
   SHA-256：515198a3054222a95894759eba570680f28a09d66442c7c866e9e20ff5169e22

5. codex_quota_mcp；2699 UTF-8 字节
   来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/codex_quota_mcp.md
   SHA-256：664c96a58fcbd5e6f32a71ab98fa344c400f1e22ae11d85f67ea0af5f9225d74

6. meta新鲜度声明；1591 UTF-8 字节
   来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/meta%E6%96%B0%E9%B2%9C%E5%BA%A6%E5%A3%B0%E6%98%8E.md
   SHA-256：09a94888f7296ecc39979fda2f685b96cbe64cd10b4d7379b429e1a8c74f4067

7. 付费调用回执与预算熔断；1332 UTF-8 字节
   来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E4%BB%98%E8%B4%B9%E8%B0%83%E7%94%A8%E5%9B%9E%E6%89%A7%E4%B8%8E%E9%A2%84%E7%AE%97%E7%86%94%E6%96%AD.md
   SHA-256：b39da3ad301951246ab91c6100991097d7c7782cd04d1ae1b671958f930ae5a4

8. 双数据源适配器隔离；1907 UTF-8 字节
   来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%8F%8C%E6%95%B0%E6%8D%AE%E6%BA%90%E9%80%82%E9%85%8D%E5%99%A8%E9%9A%94%E7%A6%BB.md
   SHA-256：13a11174f17551914da7a5bb232dbc6099281b02ae57225a029bdeaa67cf5535

9. 双时钟模型；1677 UTF-8 字节
   来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%8F%8C%E6%97%B6%E9%92%9F%E6%A8%A1%E5%9E%8B.md
   SHA-256：ab74a0126c149cad5251df1f8863882a0ff262b83472c37fc0c04b746e023b29

10. 数据源降级链；1789 UTF-8 字节
   来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%95%B0%E6%8D%AE%E6%BA%90%E9%99%8D%E7%BA%A7%E9%93%BE.md
   SHA-256：7b4229977ca35e94e59a1547b3adc21ef9551be4fc6e96ee0e9a0ec5e403ed7f

11. 本地优先与文件监听；1824 UTF-8 字节
   来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%9C%AC%E5%9C%B0%E4%BC%98%E5%85%88%E4%B8%8E%E6%96%87%E4%BB%B6%E7%9B%91%E5%90%AC.md
   SHA-256：83b7595bbd0040ab9cd9e3b53778a4372540745072dbba18aa1f004af651d358

12. 派生会话ID与结构脱敏；2355 UTF-8 字节
   来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%B4%BE%E7%94%9F%E4%BC%9A%E8%AF%9DID%E4%B8%8E%E7%BB%93%E6%9E%84%E8%84%B1%E6%95%8F.md
   SHA-256：d6fded6e6d9805bddf64c847fa3872479d8c45be8ff5476f7491f71f8bc5490c

13. 缓存；1116 UTF-8 字节
   来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E7%BC%93%E5%AD%98.md
   SHA-256：cdbb3ace706c0e5210ae08a4b85ddc4878ef3c9548c6f56ced46a0d9789d6fe0

14. 缓存有效期与发布边界；1296 UTF-8 字节
   来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E7%BC%93%E5%AD%98%E6%9C%89%E6%95%88%E6%9C%9F%E4%B8%8E%E5%8F%91%E5%B8%83%E8%BE%B9%E7%95%8C.md
   SHA-256：b4a5b6b1f2d226f05cf58217743f221b1473cc445774ecf1941228f6d9cabf4a

## 10. 证据使用原则

- 来源材料存在与断言正确分开；页面质量与数量不是结论证明
- 有限同契约测试只证明其输入范围；声明只读或本地不等于实际具备隔离
- 真实上游函数、合成输入、历史日志、负对照和未执行项应同时记录
- 不把其他项目的性能、政策、价格、测试数量或许可转移给 Metrik
