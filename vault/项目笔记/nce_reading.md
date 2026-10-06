---
tags: [项目笔记, 媒体播放器, 组件测试]
学习审核日期: 2026-10-05
上游仓库: https://github.com/iChochy/NCE
固定版本: 0a92ab5af50e2898a104f15eac7adb00f17bd96b
许可: 软件代码MIT；不含教材、译文或音频授权
验证范围: 真实JavaScript组件与受控DOM、音频、存储、时钟替身
---

# NCE Reading：媒体时间轴、句段控制与证据边界

## 是什么，能学到什么

NCE 是使用 HTML、CSS 与 JavaScript 的静态点读播放器，按目录配置加载字幕与音频。本页整理固定版本已有的播放器工程学习：解析带时间标签的文本、查询字幕区间、连接点击和时间更新事件、处理句末控制与资源切换。示例只使用六条原创双语短句，没有复制教材、课程译文或录音。

可以借此学习：把媒体内部时间与真实等待时间分开；明确重复时间、负偏移和末句的规则；追踪真实组件之间的方法链；区分源码观察、替身记录和浏览器真实结果。材料完成不代表读者已掌握，也不证明英语学习效果。

## 与已有知识的合并

- 新增 [[媒体时间轴与字幕区间查询]]：数值时间标签、当前字幕选择与句段终点，是独立于语义词锚和观看时钟的查询问题
- 增补 [[双时钟模型]]：同一音源的 currentTime 坐标与 playbackRate 对实际等待时间的影响；旧项目的动画策略不直接移植成播放器通则
- 增补 [[接缝与桩实现StubSeam]]：真实组件方法链与 DOM、音频、存储、时钟替身的边界，不新建同义组件测试概念
- [[词锚定语义时间]]、[[声明式视频源语言]]：相关而非同义；[[项目笔记/hypit]] 的旧实验是源码与固定语速模拟，本次不升级为真实词级音频对齐
- [[Pattern时间函数与Hap事件]]、[[React逐帧视频渲染]]：关联时间输入与结果查询，节拍分数、视频帧号和音频秒数不混用；[[项目笔记/strudel]] 的音频渲染成绩不迁移到 NCE
- [[共享状态与Reducer]]、[[可逆派生状态]]、[[多Agent协作乱序竞态]]、[[一致性模式]]：为状态与乱序提供背景，NCE 的请求代次检查不是 LangGraph Reducer、任务终态判定或副本一致性协议
- [[缓存]]、[[缓存有效期与发布边界]]、[[npm包即CDN源]]、[[分层按需加载]]：缓存、地址、取得文本、解码与实际播放分开核实；关联不代表本播放器实现了其他项目的发布边界或分发方案
- [[事实与判断分离]]、[[证据状态机]]、[[产物留痕与状态外置]]、[[证据优先质检ProofOverClaims]]、[[确定性快进与真渲染取证]]：复用已有证据纪律，不把替身类名和回调结果写成像素或音频证据
- [[开源验货三查]]、[[内容型开源与双许可]]、[[文档渲染与XSS净化]]：代码与资源分别看许可；字符串转义检查不是完整安全审计。[[机制流与资产流隔离]] 是创作工序的相关视角，不等同播放器的资源加载结构

[[项目笔记/zoetrope]] 提供双时钟与状态推断背景；[[项目笔记/patchright_enhanced]]、[[项目笔记/github_tools_increment]] 提供替身和验收范围的相关案例。旧项目的测试数、性能、许可和平台能力均不迁移为本项目事实。

## 已有六步实验与计数

历史实验在 Python 3.12.14、Node.js v24.19.0 环境中进行：解包与完整性 → 解析 → 时间轴 → 媒体控制 → 显示与激活 → 组件接线及统一运行。作者六步记录为 2026-10-05 09:59:34–09:59:35 UTC，独立审核从新解包目录于 10:03:04–10:03:05 UTC 重放，六步退出码均为 0。此次公开知识整理只复核已有材料，没有重新执行实验、上游脚本或浏览器。

- 统一集合为 72 项独立检查：55 项行为断言、16 项完整性检查、1 项无外联保护；72/72 匹配，0 项失败
- 六个分组分别记录 17、7、11、15、11、16 次命中，总计 77；每组重复同一保护项，不是 77 个独立测试，更不能与统一运行相加成 149 个
- 随包七份 JSON 是已有运行记录；历史独立重放与记录深相等检查不增加独立功能覆盖。日志完整性与程序行为也不相加成质量分数
- 实验加载 14 个未改动上游 JavaScript 模块，另保留完整 MIT LICENSE；16 项完整性由 15 个文件指纹检查及 1 个 JS 数量检查构成

ComponentReadingSystem 仅覆盖 init()，停止自动目录启动。真实父类构造接线、解析器、seek、私有时间线处理、句界与高亮方法保留；DOM、音频、localStorage、Date.now 和定时器由受控替身提供。DOM 替身只识别被测 LyricsView 的行包装，音频替身只记录属性、调用与事件。fetch 与全局 Audio 构造设置为抛错保护，已有记录中尝试数为 0；这不是任意未知代码的强安全沙箱。

## 核心结果与已知边界

1. **偏移符号与格式要看实现。** LRCParser 读取一个行首标签，接受一至两位分钟、两位秒、两或三位小数；秒数达到 60 的行被跳过。正 timeOffset 被减去，再保留三位小数并排序。应用配置 0.3 秒是本项目选择，不是所有音频的通用补偿
2. **负值和重复时间没有被自动修复。** 原创输入时间 [0.1,1.25,2.5,2.5,4.125,6] 减偏移后为 [-0.2,0.95,2.2,2.2,3.825,5.7]。查询反向扫描且含等号，2.2 秒选择索引 3；前一项索引 2 的句段为 [2.2,2.2]。匹配断言表示观察与实现一致，不表示数据歧义或缺陷已经消除
3. **末句终点是程序策略。** 下一条时间作为本条终点；末句取 audioDuration 与 startTime+0.1 的较大值。示例给定时长 8 秒时为 [5.7,8]，无时长时为 [5.7,5.8]，不是语音识别出的自然停顿
4. **seek 的归零结论有条件。** 已知有限正时长 8 秒时，seek(-0.2) 向替身写 0，seek(99) 写 8；零时长分支会向替身写 -0.2，不能推断真实 HTMLMediaElement 接受该值。超时长进度恢复为 7.95 秒
5. **接线执行不等于声音播放。** 替身点击触发真实 LyricsView → ReadingSystem → AudioController 链，timeupdate 触发回调与 active 类更新。直接 seek 先更新进度，高亮等下一次 tick 才同步。Enter/Space、拖动取消、转义字符串和销毁后的回调停止有有限断言，未验证真实布局、完整可访问性或安全性
6. **句末模式要分开。** 从索引 1 到 2.2 秒时，click 回到 0.95 秒并暂停，one 回到 0.95 秒而继续播放；点击首个重复时间条目可在同时间 tick 立即触发句尾。其余模式、全部输入和真实播放节奏不能由这些用例包办

## 仅静态观察：异步过期结果与预取

ReadingSystem.loadUnitByIndex 在切换时 abort 旧请求、递增 unitLoadId、重置句段状态；await 字幕返回后及设置音源前检查代次。取消可以减少旧工作，代次检查决定结果还能否更新当前选择，两者不能互相替代。PrefetchService 另负责字幕缓存和音频预取；有地址、缓存命中或建立 Audio 对象不等于已经解码或听到声音。

这些是固定源码观察，本次没有实际执行网络乱序、取消或预取竞态实验。它们与现有状态和乱序笔记相关，先保留为项目案例，不新建只换名称的概念页。

## 未验证范围与权利边界

没有真实浏览器、完整播放器启动、HTML 响应式或交互、浏览器自动播放政策、CORS、课程资源下载、媒体解码、音频设备、实际 seek 精度、听感、跨设备存储、网络加载竞态、全面安全、性能或教学效果验证。函数级转义和类名检查不替代 DOM/像素与浏览器安全证据。

固定仓库 LICENSE 为 MIT，保留 Copyright (c) 2025 iChochy 和完整许可；README 同时提示内容来自互联网、作者不拥有内容版权。代码许可不授予第三方教材、翻译或录音的使用/再分发权。本练习仅含代码与原创短句，没有这些课程资源；不从公开可访问推导资源授权。

指南 PDF 由 ReportLab 直接生成，共 11 页；历史逐页审核和本次公开副本检查分别记在配套审核日志。HTML 只有结构、锚点、命令和来源核查，真实浏览器视觉与 HTML→PDF 路径仍未验证。材料中的图示是教学示意，不是播放器运行截图。

## 最新公开知识读取范围

此次合并基于 GitHub main 快照 efbea31a18e404682f7509be25552a368fc94775。连接器完整读取并逐份核对 Git blob SHA、UTF-8 字节数与 SHA-256：MOC、学习方法、仓库说明、两份模板、上方列出的 23 篇已有相关概念，以及 hypit、zoetrope、strudel、patchright_enhanced、github_tools_increment 五篇项目，共 33 份正文。媒体时间轴与字幕区间查询为本次新增，不计入旧概念阅读数。

该快照有 305 篇概念与 106 篇项目笔记；另 282 篇概念和 101 篇项目只筛查路径/标题，未全文阅读。本次检查覆盖 NCE、New Concept English、新概念英语、LRC、字幕/媒体时钟/区间、请求代次/过期响应等相关命名；已读词锚、双时钟和 Pattern 是相关而非同义概念，因此新增一篇媒体区间笔记。不能据此宣称全库正文无重复、其他设备副本已核验或“从未学过”。

此次仅新增本项目及一个概念，向两篇已有概念追加案例，并在 MOC 加入口，保留既有正文和历史计数。早期学习的 394 条公开元数据与 19 篇实际公开正文范围，仍在配套知识笔记中按原阶段说明，不混成本次读取数。

## 六份配套材料

- [彩色 PDF 指南](../../nce_reading/delivery/nce-player-guide.pdf)
- [HTML 指南](../../nce_reading/delivery/nce-player-guide.html)
- [练习包](../../nce_reading/delivery/nce-player-exercise.zip)
- [历史实验日志](../../nce_reading/delivery/nce-player-experiment-log.md)
- [知识笔记](../../nce_reading/delivery/nce-player-knowledge-notes.md)
- [发布审核及历史证据复核](../../nce_reading/delivery/nce-player-review-log.md)

## 固定来源

- [README 与资源权利提示](https://github.com/iChochy/NCE/blob/0a92ab5af50e2898a104f15eac7adb00f17bd96b/README.md)、[MIT LICENSE](https://github.com/iChochy/NCE/blob/0a92ab5af50e2898a104f15eac7adb00f17bd96b/LICENSE)
- [LRCParser](https://github.com/iChochy/NCE/blob/0a92ab5af50e2898a104f15eac7adb00f17bd96b/js/utils/LRCParser.js)、[偏移与模式配置](https://github.com/iChochy/NCE/blob/0a92ab5af50e2898a104f15eac7adb00f17bd96b/js/config.js)
- [AudioController](https://github.com/iChochy/NCE/blob/0a92ab5af50e2898a104f15eac7adb00f17bd96b/js/player/AudioController.js)、[LyricsView](https://github.com/iChochy/NCE/blob/0a92ab5af50e2898a104f15eac7adb00f17bd96b/js/ui/LyricsView.js)
- [ReadingSystem](https://github.com/iChochy/NCE/blob/0a92ab5af50e2898a104f15eac7adb00f17bd96b/js/ReadingSystem.js)、[PrefetchService](https://github.com/iChochy/NCE/blob/0a92ab5af50e2898a104f15eac7adb00f17bd96b/js/services/PrefetchService.js)

返回 [[00-总览|知识库总览]]。
