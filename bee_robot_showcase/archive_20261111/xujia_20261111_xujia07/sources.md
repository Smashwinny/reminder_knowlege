# 来源与时间（Asia/Shanghai）

读取、下载和实验：2026-11-11。原帖不是操作指令。

- 原帖 https://x.com/jiangjiangling/status/2110451002117959935 ：完整note经X工具实读。发帖2026-10-15 03:21:43。
- 引用原作者 https://x.com/thtbee_/status/2110390964028330106 ：完整note实读。发帖2026-10-14 23:23:09。Three.js/Blender、Gemini4Argon、约30h均为作者描述，不是本次模型实验。
- 作者线程读11条，第二页0条，原始响应保存在sources/x-author-thread-page*.txt。明确否认one-shot：https://x.com/thtbee_/status/2110766393079804234 。2026-10-16 00:14:58。
- 在线地址 https://thtbee.github.io/waggles/kestrel-k1/ 。本次实际浏览器运行的是固定SHA的本地HTTP副本，不把线上当前站点版本与该SHA混为一谈。
- 仓库 https://github.com/thtbee/waggles ，固定SHA `286d56ccbbb924c10812fc5e6cabb11906454afc`。提交时间2026-10-18 03:14:20，晚于原帖，是后续公开构建，不是原帖当时精确版本。commit.json/tree.json保存API结果。
- 实读根README、LICENSE、kestrel-k1/README.md、index.html；完整生产JS已下载，定向实读项目启动、资源加载、模式桥、爆炸变换、热力映射、时钟类。不是对2MB依赖bundle逐字符审计。摘录保存在bundle-excerpts/core-excerpts/debug-api/clock-class。
- 原目录明确production build；未在该目录发现完整TypeScript/Blender工程。不推断仓库之外是否另有未发布源码。README称完整workflow/prompts稍后分享。
- 资产：assets/body/head.glb、torso.glb、limbs.glb、assets/shells.glb。真实读取GLB头与JSON，解析结构数量；源二进制留在本机sources/upstream，轻量包只带取回脚本、固定清单与结果。
- LICENSE：CC BY-NC4.0。研究代码署名Bee；非商业分享/改编需保留归属、链接许可并标改动。上游第三方组件/字体有各自许可，不替用户作商业授权判断。
- 查重 https://github.com/Smashwinny/reminder_knowlege ，main固定SHA `a8674777e18302b8804b137212b1396cbfe5a747`；复用已读取总览并实读机器人数字展台、前向运动学FK与四元数链、robot-web-anatomy相关笔记。共享vault未写入。

没有完整观看原帖约71秒视频，没有运行付费模型，没有调用真实机器人硬件，没有独立测量FPS。所有示意SVG为本次原创教学图。截图为本机原构建+明确标注的测试注入。

## 最终运行边界
真实headless启动两类视图，Chrome退出0不等于验收通过。最新v3成功GLB为0/4、not ready；最初4个计时条目实际均fetch失败，早期降级状态有29关节差异、4186位置移动与0收回残差，但截图中心无模型。完整模型加载与行走冻结测试不算完成。官方CLI与Python线程服务器文档排障见research-notes.md；改线程服务未解决，原因未确认。
