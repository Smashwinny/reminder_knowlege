# NCE 播放器工程知识笔记

历史学习日期：2026-10-05 UTC。范围：时间标记文本解析、媒体时间轴、句段边界与资源加载；例子只使用自写短句。公开整理未重跑实验；本文保留固定来源、公开知识关联、历史结果和适用边界。

## 1. 查重范围

固定公开索引包含 394 条元数据。本轮实际全文读取并核验 19 篇相关概念/项目笔记，其余 375 篇只查元数据。公开索引固定于 Smashwinny/reminder_knowlege@1f61909da967cea8bc68dbfaffc642a4331b3352；相关公开正文固定于 1043e9d6080bff7af9724162e2c44559fab63e40。

在固定公开索引标题/路径和上述 19 篇公开正文中，没有找到 NCE 的既有完整学习记录。名称检查覆盖 NCE、nce_reading、New Concept English、新概念英语、相关繁体/播放器写法、ichochy 与 nce.ichochy.com。这个结论只针对历史快照的实际阅读范围，不覆盖其他版本或其余 375 篇未读正文；不能写成“从未学过”或“全库无重复”，也不代表读者已掌握。

## 2. 先复用已有概念

- [[hypit]]、[[词锚定语义时间]]、[[声明式视频源语言]]：只建立相关链接。既有 Hypit 笔记的实验是源码分析和固定语速模拟，没有实际执行词级音频对齐或成片渲染。NCE 的 LRC 时间标签与 Hypit 的语义词锚并非同一机制
- [[双时钟模型]]：复用内容时间与观看过程时间的区分；用媒体 currentTime 解释字幕定位，用播放速率解释相同媒体区间需要多少实际等待时间。旧项目的动画策略不自动成为所有播放器的规则
- [[Pattern时间函数与Hap事件]]、[[React逐帧视频渲染]]：关联“时间输入决定事件或画面”。不要把节拍分数、视频帧号和音频秒数混用，或宣称这三个项目共享相同实现
- [[缓存]]、[[npm包即CDN源]]、[[分层按需加载]]：作为相关背景。目录配置、资源地址、下载成功、解码成功与实际播放分别需要证据。分层 Skill 加载与媒体预取只属于思路类比
- [[共享状态与Reducer]]、[[可逆派生状态]]：复用显式状态、过时信息不能覆盖当前事实的思想；播放器并不是 LangGraph Reducer，本项目状态应按实际源码解释
- [[事实与判断分离]]、[[证据状态机]]、[[产物留痕与状态外置]]、[[证据优先质检ProofOverClaims]]：已有充分的方法基础，只补 NCE 案例，不新建同义“证据分层”概念
- [[接缝与桩实现StubSeam]]、[[确定性快进与真渲染取证]]：受控时间和替身可帮助检查真实上游代码，但函数结果、替身调用记录、浏览器像素、音频播放和用户效果是不同证据
- [[开源验货三查]]、[[文档渲染与XSS净化]]：代码许可不自动覆盖外部教材/音频/译文；解析成功不自动证明所有显示位置安全。具体许可与安全判断仍须核对本项目当前来源

## 3. 候选概念：媒体时间轴与字幕区间查询

一句话定义：将字幕的时间标签解释为媒体内部坐标，并按明确的区间和边界规则，计算给定播放位置对应的字幕及句段终点。

领域：媒体软件、数据解析、时序查询。

自写例子：两条提示分别标为 1.200 秒的“Blue cube”和 2.500 秒的“Green circle”。播放器到媒体时间 2.499 秒时仍处于第一段，达到 2.500 秒后选择第二段。两条标签定义的媒体间隔为 1.300 秒；若媒体按 2 倍速连续推进，理想等待时间约为 0.650 秒。这只是算例，不是实测音频播放延迟。

重要区别：词锚先选语义位置，再由具体音频对齐给出时间；LRC 直接携带数值时间。调节 playbackRate 并不改写同一音源的时间坐标；更换录音、剪掉片头或插入停顿则可能需要重新对齐字幕。因此不能一概说“绝对秒数在变速后必然失准”。

固定 NCE 源码的静态观察：LRCParser 读取一个行首时间标签，支持 1–2 位分钟、两位秒和 2–3 位小数；秒数达到 60 的行被跳过。它减去传入 timeOffset，再保留三位小数，按时间排序。正偏移使标签前移，不是后移；配置默认 0.3 秒只是本项目选择，不是音频系统通用延迟。注释中出现单小数位的示意不改变正则只接受两或三位的事实。

查找函数从末项反向扫描，返回最后一个满足 time≤currentTime 的索引；句段终点使用下一项时间，最后一项取 audioDuration 与 startTime+0.1 的较大值。这是该实现的边界策略，不是 LRC 格式天然提供的结束标记。相同时间戳、负时间、最后一句、缺失时长与无效输入都值得逐项检查；看到源码分支不等于已经执行覆盖它。

关联：[[双时钟模型]]、[[词锚定语义时间]]、[[Pattern时间函数与Hap事件]]。

合并建议：先在目标知识库查找“字幕时间轴、cue、媒体时钟、区间查询、LRC”等同义内容。有同义项则增补本项目；只有相关项时互链，确认独立价值后才建立新概念。

来源：[LRCParser.js](https://github.com/ichochy/nce/blob/0a92ab5af50e2898a104f15eac7adb00f17bd96b/js/utils/LRCParser.js)、[config.js](https://github.com/ichochy/nce/blob/0a92ab5af50e2898a104f15eac7adb00f17bd96b/js/config.js)。上述为静态源码核对；实际执行覆盖须以本次实验日志为准。

## 4. 候选概念：异步资源加载的过期结果隔离

一句话定义：当用户的当前选择已改变，较早请求即使较晚返回，也不能再覆盖新选择的状态。

领域：前端异步编程、状态一致性、资源生命周期。

自写例子：先选择合成资源 A，再立即选择 B。A 的字幕较晚返回时，不应将 B 的画面替换成 A。取消请求可以减少不再需要的工作；检查请求代次则决定一个结果还有没有资格更新状态。两者作用不同，不能因为调用过 abort 就省略所有过期结果检查。

固定源码的静态观察：ReadingSystem.loadUnitByIndex 在切换时中止旧请求、递增 unitLoadId，重置句段状态，并在 await 加载字幕后及设置音源前检查代次。PrefetchService 则负责字幕缓存和音频预取。缓存命中、取得文本和建立 Audio 对象都不能单独证明用户已经听到声音。

关联：[[共享状态与Reducer]]、[[可逆派生状态]]、[[缓存]]、[[产物留痕与状态外置]]。这些概念相关而非同义，不能把 Reducer、任务终态或缓存 TTL 的旧实现直接移植为 NCE 事实。

合并建议：优先作为 NCE 的项目案例，复用时查询“竞态、过期响应、请求代次、取消、latest request wins”等现有内容。发现同义项则合并，不只换名另建。

来源：[ReadingSystem.js](https://github.com/ichochy/nce/blob/0a92ab5af50e2898a104f15eac7adb00f17bd96b/js/ReadingSystem.js)、[PrefetchService.js](https://github.com/ichochy/nce/blob/0a92ab5af50e2898a104f15eac7adb00f17bd96b/js/services/PrefetchService.js)。上述是源码审阅，不声称完整浏览器竞态测试已经通过。

## 5. 项目案例：解析、控制和播放分层验证

可分别记录：文本能否解析成字段、字段是否符合业务约束、区间选择是否符合约定、模式是否产生预期控制动作、浏览器是否真正加载解码和播放，以及使用者是否获得学习效果。

真实上游函数处理自写合成输入，属于函数级执行证据。假音频对象记录 seek/pause，只能证明代码按测试契约发出了对应操作；不会证明浏览器自动播放政策、音频设备、CORS、听感、字幕真实准确性或英语学习效果。故意构造的异常如果准确暴露当前行为，也可以使“行为检查通过”，但不等于缺陷已经修复。

这部分优先增补既有 [[证据优先质检ProofOverClaims]] 与 [[接缝与桩实现StubSeam]]，不重复创造新的证据原则。保留固定上游、合成输入标识、命令、时间、原始结果及未执行范围；不要搬用任何旧项目的测试数量或成绩。

## 6. 复用建议与边界

先核对目标知识库的同义条目与已有编辑，再决定概念合并、互链与项目索引更新。保留固定来源、输入、命令、历史结果和未验证范围；不要以保存笔记代替实际掌握或产品验收。

本文范围是播放器工程学习，不复制教材、外部翻译或原版音频，不证明真实浏览器播放或英语学习效果。实验结论应与历史日志逐项对应；不能把此处的源码审阅自动升级为已执行结果。

## 7. 实际全文核验的公开知识来源

以下来源均固定在公开正文提交 1043e9d6080bff7af9724162e2c44559fab63e40，仅用于查重与概念关联。历史价格、服务条件、许可简写、性能及他项目实验没有在本轮逐项重验。

1. [Pattern时间函数与Hap事件](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/Pattern%E6%97%B6%E9%97%B4%E5%87%BD%E6%95%B0%E4%B8%8EHap%E4%BA%8B%E4%BB%B6.md)
   UTF-8 1762 字节；SHA-256 6b400b1d9d511cf2acfa423607fa6e28d5be2b9b3de291501170b6f32912fb6f

2. [React逐帧视频渲染](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/React%E9%80%90%E5%B8%A7%E8%A7%86%E9%A2%91%E6%B8%B2%E6%9F%93.md)
   UTF-8 1997 字节；SHA-256 c8f87b4b218b9910149ac18c5e8fa29ccedddc1265fb13d81c5a78b5ef0b0e29

3. [hypit](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/hypit.md)
   UTF-8 3959 字节；SHA-256 954994020f39c1f088c74b16c4544e8d6d5061f12431815aac867285c1bf142e

4. [npm包即CDN源](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/npm%E5%8C%85%E5%8D%B3CDN%E6%BA%90.md)
   UTF-8 1928 字节；SHA-256 4606e7ee371afaee7d1841bd8cf0b2a4d7ad51bb70324b1c27d0d2d5680ce6c4

5. [事实与判断分离](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E4%BA%8B%E5%AE%9E%E4%B8%8E%E5%88%A4%E6%96%AD%E5%88%86%E7%A6%BB.md)
   UTF-8 1653 字节；SHA-256 53f5643580c0ab2e2860c6d2b25e3ea7eeb80cf806c1fdf4d989cab59319427b

6. [产物留痕与状态外置](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E4%BA%A7%E7%89%A9%E7%95%99%E7%97%95%E4%B8%8E%E7%8A%B6%E6%80%81%E5%A4%96%E7%BD%AE.md)
   UTF-8 2389 字节；SHA-256 6aba36f09afc580c08a669663e1ddaef6fa2c99067fcfedb65f56ba81a5ecceb

7. [共享状态与Reducer](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%85%B1%E4%BA%AB%E7%8A%B6%E6%80%81%E4%B8%8EReducer.md)
   UTF-8 1438 字节；SHA-256 a09fb5e07eba8ee88fe6c917c45cf04ecda284fb73cf0326a9b9233a8af79da9

8. [分层按需加载](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%88%86%E5%B1%82%E6%8C%89%E9%9C%80%E5%8A%A0%E8%BD%BD.md)
   UTF-8 1586 字节；SHA-256 835f5fd1ef083c5dae702918b5da3e33edca7105342b95e44c275701feff3d14

9. [双时钟模型](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%8F%8C%E6%97%B6%E9%92%9F%E6%A8%A1%E5%9E%8B.md)
   UTF-8 1677 字节；SHA-256 ab74a0126c149cad5251df1f8863882a0ff262b83472c37fc0c04b746e023b29

10. [可逆派生状态](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%8F%AF%E9%80%86%E6%B4%BE%E7%94%9F%E7%8A%B6%E6%80%81.md)
   UTF-8 2076 字节；SHA-256 f08c023413927f01deab7be39889ea0c8539f1f389b6f25506c9395f72430d37

11. [声明式视频源语言](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%A3%B0%E6%98%8E%E5%BC%8F%E8%A7%86%E9%A2%91%E6%BA%90%E8%AF%AD%E8%A8%80.md)
   UTF-8 2367 字节；SHA-256 f96518339a233d646cd0652b4e9e5b80872370a1c13c3d086f8c1f6a6ac985f0

12. [开源验货三查](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%BC%80%E6%BA%90%E9%AA%8C%E8%B4%A7%E4%B8%89%E6%9F%A5.md)
   UTF-8 1815 字节；SHA-256 836585db83f85f393815551357aad9b894567c5e57bc7c4623e088040c50b0ce

13. [接缝与桩实现StubSeam](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%8E%A5%E7%BC%9D%E4%B8%8E%E6%A1%A9%E5%AE%9E%E7%8E%B0StubSeam.md)
   UTF-8 1752 字节；SHA-256 83decb2724ea3ac736e0f9c4c89e17e043504be4733162e6ee44d7988c976804

14. [文档渲染与XSS净化](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%96%87%E6%A1%A3%E6%B8%B2%E6%9F%93%E4%B8%8EXSS%E5%87%80%E5%8C%96.md)
   UTF-8 1386 字节；SHA-256 c6386db4fd0d42c4ae0de236ffe1dc4367eb011e97f6a1a001968fc31c95a248

15. [确定性快进与真渲染取证](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E7%A1%AE%E5%AE%9A%E6%80%A7%E5%BF%AB%E8%BF%9B%E4%B8%8E%E7%9C%9F%E6%B8%B2%E6%9F%93%E5%8F%96%E8%AF%81.md)
   UTF-8 1902 字节；SHA-256 29854a02e9a9a472da6e921019fae7fbeccf6cb912cfbdb73392a742bb86fcf4

16. [缓存](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E7%BC%93%E5%AD%98.md)
   UTF-8 1116 字节；SHA-256 cdbb3ace706c0e5210ae08a4b85ddc4878ef3c9548c6f56ced46a0d9789d6fe0

17. [证据优先质检ProofOverClaims](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%AF%81%E6%8D%AE%E4%BC%98%E5%85%88%E8%B4%A8%E6%A3%80ProofOverClaims.md)
   UTF-8 3593 字节；SHA-256 c54ea2f3bcfe830556942d04c502ba84472a7382c45b76dd07401861e44c2fac

18. [证据状态机](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%AF%81%E6%8D%AE%E7%8A%B6%E6%80%81%E6%9C%BA.md)
   UTF-8 2488 字节；SHA-256 4ac12b197891357591ebd092a9120bd67fa6fa1a09a407ed9c0fea3bc9b97328

19. [词锚定语义时间](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%AF%8D%E9%94%9A%E5%AE%9A%E8%AF%AD%E4%B9%89%E6%97%B6%E9%97%B4.md)
   UTF-8 2101 字节；SHA-256 4e1028a2d41e0811ad7d2a1d46674399cfc8ef08539d3c04039ca7bee14069f4

## 8. 历史组件实验补充

实验直接加载固定提交中的 14 个 JavaScript 模块，保留原始字节与 MIT 许可；自建脚本不重写 LRC 算法。只有实验子类的 init() 被覆盖以停止自动目录启动，DOM、音频、存储和时钟使用受控替身。原始输入为六条原创双语短句，不含课文、录音或外部翻译。

- 默认解析不减偏移时，排序结果为 [0.1, 1.25, 2.5, 2.5, 4.125, 6]；按应用配置减去 0.3 后变成 [-0.2, 0.95, 2.2, 2.2, 3.825, 5.7]
- 当前时刻为 2.2 秒时命中索引 3；索引 2 的句界为 [2.2, 2.2]，形成零长度区间。检查通过表示观察与当前实现一致，不表示数据歧义已经修复
- 时长已知为 8 秒时，seek(-0.2) 写入 0，seek(99) 写入 8。未知或零时长分支以请求值作为上限，替身观察到负值可被写入；真实 HTMLMediaElement 对该输入的处理未测
- 替身点击触发真实 LyricsView → ReadingSystem → AudioController 方法链；timeupdate 触发回调和 active 类更新。直接 seek 先更新进度，高亮直到下一次 tick 才同步
- 选中索引 1 后到达句尾 2.2 秒，click 模式回到 0.95 秒并暂停；one 模式回到 0.95 秒但继续播放。点击重复时间的第一条会在同时间 tick 上立即暂停
- 最后一句使用已知时长 8 秒作为终点；无时长时的兜底结果为 5.8 秒。恢复进度超过时长时，当前实现放到 7.95 秒

完整断言与执行时间见配套实验日志，原始 JSON 留在练习 ZIP 的 results 中。组件模拟没有验证音频解码、听感、真实布局、浏览器自动播放、CORS、网络竞态或学习效果。句界实验结论可补到媒体时间轴概念；过期异步结果隔离仍只是本轮源码审阅，不应升级为已执行覆盖。
