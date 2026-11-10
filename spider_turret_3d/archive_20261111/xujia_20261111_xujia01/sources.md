# 第1项来源清单

读取时间：2026-11-11 00:54—01:02（Asia/Shanghai，UTC+8）；后续文件生成时间以本目录mtime/日志为准。

## 原帖与作者线程（MCP 公共 x 读取）
- 原帖：https://x.com/thebuggeddev/status/2115425928503550344
- 发布：2026-10-28 20:50:18（Asia/Shanghai）。正文宣称单张概念图、Gemini 4 Argon、程序化3D、rigging、机械运动与发射；不验证模型身份、生成次数或实际物理真实性。
- 原帖 referenced_tweets 未出现，没有引用帖需递归读取；附51秒视频元数据已读取，视频未完整观看，不将画面细节当本次直接观察。
- 作者线程搜索：`conversation_id:2115425928503550344 from:thebuggeddev`，第一批25条、第二批7条、终页0条（无next_token）。搜索结果是当前可返回范围，不保证已删除/搜索未收录内容。
- 首次续页遇共享X HTTP429，要求到2026-11-11 00:59:32（Asia/Shanghai）再读；本次于01:00后原参数重试成功。未绕过限制。
- 源码入口：https://x.com/i/status/2115644254190236018 → https://github.com/thebuggeddev/spider-turret
- one-shot的限定：https://x.com/i/status/2115646545416831015 ——作者说模型/转动one-shot，同时微调细节与UI。不能简写成“成品完全一次生成”。
- bpy生成路线：https://x.com/i/status/2115430260334534776 ——作者说写整套Python脚本，通过Blender bpy执行，而非直接UI操作。仓库缺该脚本，不能复现此生成链。
- 发热效果归因：https://x.com/i/status/2115641354814738837 ——“Argon自行加上”；仅为作者陈述。
- 工具入口回复：https://x.com/i/status/2116013451776872532 → https://antigravity.google/ 、https://aistudio.google.com/apps （仅记录作者链接，未登录、未付费、未调用）。
- 读取回执：sources/x-post.txt、x-thread-page1.txt、x-thread-page2.txt、x-thread-end.txt、x-links.txt。保留数据包装，不将包装内建议当执行指令。

## 一手仓库
- URL：https://github.com/thebuggeddev/spider-turret
- 固定提交：`e5f92a8b99f2cbeef6a87ad12c142b0ccf34a99b`，提交时间2026-10-29 18:59:44（Asia/Shanghai），不是原帖当日精确构建。
- commit与完整tree回执：sources/commit.json、sources/tree.json。该树无README、LICENSE、原始概念图、生成prompt、Blender .py生成脚本；这是本固定树的观察，不推断作者从未拥有。
- 下载了index.html与全部11个JS模块；实读聚焦下列位置（保存不等于通读每一行）：
  - index.html:1009–1037：React18.3.1 / three0.174.0 / Fiber8.17.10 importmap与GLB入口。
  - src/components/SpiderTurretApp.js:760–876、1225–1249：资源初始化、useFrame、dt截断、WebGPURenderer、像素比上限。
  - src/spider/RobotRig.js:1–200、470–633：命名节点契约、材质转换、爆炸图、GLB加载。
  - src/spider/LegIKSolver.js:1–156：完整解析IK。
  - src/spider/QuadrupedGaitController.js:1–269：完整步态/悬挂/IK调用。
  - src/spider/AnimationStateMachine.js:1–122：完整状态机。
  - src/spider/TurretController.js:1–230、250–319：转动、发热、事件触发、换装。
  - src/spider/RobotController.js:480–636：主调用顺序、uniform、遥测/伪温度映射。
  - src/spider/tslMaterials.js:1–153：TSL、发光与恒0地形。
  - spider_turret.glb：Python标准库解析头与JSON；7,719,160字节，SHA256 `b3c28c34e609e430911207a9aaf3b2adef47b2893017503f01176482d833d22f`。
- 固定链接格式：https://github.com/thebuggeddev/spider-turret/blob/e5f92a8b99f2cbeef6a87ad12c142b0ccf34a99b/src/spider/LegIKSolver.js#L55 。HTML各问已附固定链接。

## 官方文档 / 依赖
- Blender官方Python API Quickstart：https://docs.blender.org/api/current/info_quickstart.html ，2026-11-11读取。支持bpy可读写场景/网格/材质并执行脚本的一般机制；current页面可能更新，没有把当前API版当作作者生成环境。
- 实验依赖three@0.174.0，来源由npm registry与exercise/package-lock.json的resolved/integrity锁定；上游浏览器把three映射至该版three.webgpu.js，Node实验默认three入口仅用共享数学类，不验证后端。
- 没有引用论文，没有模型API调用，没有作者性能替代本次实测。

## 知识库查重 / 风格
- https://github.com/Smashwinny/reminder_knowlege ，当前main查询固定 `a8674777e18302b8804b137212b1396cbfe5a747`。
- commit时间2026-11-04 17:42:58（Asia/Shanghai）；完整树truncated=false。没有clone、没有写仓库，仅公开raw/API只读快照至reference/。
- 实读 vault/00-总览.md；项目 img2threejs、3d_vibe_coding、blueprint_to_3d；概念 程序化建模、Three.js与场景图、图生3D资产管线、逆运动学IK与CCD迭代。
- 未发现spider-turret/Argon专属主题；通用程序化建模、场景图、图生3D管线与性能方法已覆盖。因此只提案增量：刚性命名节点契约、解析IK/触限残差、世界坐标支撑目标、离散事件计数。
- 风格样本：agent_desktop/agent_desktop-小白指南.html（大号问答卡、蓝青橙、SVG、notice边界、证据/实验分列）。本HTML为原创结构/图示，不复制整篇内容。

## 文件指纹
见 sources/file-hashes.json；实验JSON与log给出真实观察，qa为作者自身排版检查，绝不是独立审核。
