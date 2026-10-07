---
tags: [项目笔记, 接口测试, 资源生命周期]
学习审核日期: 2026-10-05
上游仓库: https://github.com/whaleyxbt/patchright-enhanced
固定版本: e38ab7ab9448db6f093f72ee097c18ca9905e84c
验证范围: 三个TypeScript模块的配置与生命周期特征化测试
---

# Patchright Enhanced：包装层配置与资源清理

## 是什么，能学到什么

Patchright Enhanced 是 TypeScript 编写的 Patchright 包装层，组织配置、会话与 BrowserManager 资源管理。固定版仓库名为 patchright-enhanced，package.json 的包名为 ghostprobe。学习范围是接口封装、配置输入、资源关闭与失败诊断；上游宣传的浏览器能力没有在本项目得到验证。

可以借此学习：对照文档与实际默认值；检查字符串到数值的宽松转换；区分真实包装层与替身依赖；核对成功、失败和重复调用的资源状态；给源码观察、特征化测试和完整集成分别记证据。20/20 表示当前行为与断言相符，其中包括缺陷，不能理解为 20 项质量验收或生产可用证明。

## 与已有知识的合并

- [[接缝与桩实现StubSeam]]：追加真实包装层、惰性依赖与真实浏览器三者的覆盖边界，不再新建 mock 测试同义概念
- [[失败反馈具体化]]：追加关闭失败时的步骤、残留引用、未发生的清理与手动再调用；不把局部幂等写成完整恢复机制
- [[开源验货三查]]：追加无明确许可声明、只提供来源引用而不打包上游源码的案例，关联 [[内容型开源与双许可]]
- [[Provider适配层与错误契约]]、[[健康探测三态]]：提供错误传播和依赖诊断的相关视角；其特定实现不是本包装层已经实现的功能
- [[固定版本中的跨文件时间漂移]]：文档默认值与函数默认值应分别呈现，版本固定不能保证两者一致
- [[证据优先质检ProofOverClaims]]、[[证据状态机]]、[[产物留痕与状态外置]]：检索到文本、执行脚本、渲染画面和完成交互需要不同证据，不单设重复概念页

[[工具调用生命周期]] 讲 MCP 调用循环，本页讲对象引用与资源清理，不能同义合并；[[托管Harness与会话即资源]] 的持久会话也不是浏览器 context。[[确定性选择器模式]] 是 LLM 特征到决定信号的组合，与 DOM selector/locator 不同。[[GUIAgent与多模态定位]] 与 [[确定性快进与真渲染取证]] 仅为真实设备或画面验收的背景，此次没有相关运行证据。

[[能力层与后端路由]] 与 [[项目笔记/agent-reach]] 是工具安装、体检与路由视角，不把本包装层当作相同能力平台，也不重复该项目实验。[[能力运行时]]、[[能力地板选型]] 与 [[数据源降级链]] 仅用于架构/选型对照。[[沙箱与审批正交]]、[[代码管边界提示词管判断]]、[[沙箱三态与Executor]]、[[只读闸门三原则]] 与 [[缓存有效期与发布边界]] 的边界不能由工具能力或缓存记录替代。

## 已有六步实验与计数

原学习在 Node v24.19.0 中，用 stripTypeScriptTypes 去除类型语法，再经白名单导入载入 VM。只执行固定且未修改的三个源码模块：src/config/browser.config.ts、src/config/index.ts、src/browser/browser-manager.ts。fs.existsSync/mkdirSync、代理标记、context.close、cleanupTempDir 是惰性替身；path.resolve 是纯路径运算，没有真实会话目录创建或清理。

六步为检查 Node/Git、读取固定来源并执行单元代码、查看默认值、查看数值矩阵、查看生命周期、核对来源与未测范围。初次运行记录为 2026-10-05 08:13:42 UTC；历史独立审核从新解压包重取指定版本，于 08:28:54–08:29:04 UTC 重放六步，全部退出 0。本次公开知识整理复核已有证据，没有重新执行学习实验或浏览器。

- 20 个自写的上游源码当前行为断言：4 个浏览器配置、9 个应用配置、7 个生命周期；20/20 匹配，0 个断言失败
- 自写结果查看器另有 10 个用例：1 个完整证据正例被接受、9 个合成错误证据被拒；不加成 30 个上游测试
- 同一组 20 个用例的历史独立重放不另加成 40 个；耗时不是性能基准
- 类型去除与 VM modules 的 ExperimentalWarning 保留，未当成语义类型检查或构建成功

## 关键结论与缺陷

1. B01–B04：headless 固定为 false；浏览器路径和时区的显式输入及空字符串回退按实际输出记录；传入未实现的 HEADLESS 环境变量没有效果。得到配置对象不代表浏览器接受配置或产生目标效果
2. A01/A09：MAX_PARALLEL 缺失或为空字符串时返回 2，README/.env.example 示例为 1。五个输入 0、-1、oops、2junk、2.9 分别得到 0、-1、NaN、2、2，未被拒绝；这表明校验缺口，而非这些值合法
3. A02/A03：目录缺失仅向惰性 fs 发出递归 mkdir 请求，目录已存在则不发出创建请求；它们不证明真实文件系统变化
4. L01–L05：空管理器无外部效果；setContext 保留对象身份；close 成功后清空 context，cleanup 另行处理；closeAndCleanup 先关闭后清理。首次成功后的顺序重复调用无额外替身效果，只是局部幂等证据
5. L06：合成 close 拒绝向上传播，context 引用仍在，cleanup 调用数为 0；不保证“所有异常最终都会清理”
6. L07：测试代码主动第二次调用关闭，替身这次成功后才继续清理；没有实现自动重试、退避或崩溃恢复
7. START_PAGE_URL 空值回退、locale 类型声明与实际返回不一致、package 与 lock 的依赖条目不一致，仅为原学习静态源码观察；没有运行编译、安装或导航来验证后续影响

历史审核曾发现 scope 查看器对空 sourceChecks 使用 every() 会误报“三个来源散列”。修正版要求恰好三个唯一预期路径、正确提交/执行模块、合法且匹配的散列及严格 true 标记；9 个负例验证错误记录被拒绝。记录内部一致不替代独立执行，也不能证明记录防篡改。

## 没有验证的部分

未安装上游依赖，未运行语义类型检查、完整 tsc/build、官方测试套件、入口 main、SessionRunner、context-factory、proxy.config、start/default 或真实文件清理实现。没有导入外部浏览器依赖、启动浏览器、导航、执行网页脚本、真实代理、DOM/视觉/交互、站点任务或性能验证。被测三个模块没有网络请求；历史来源获取使用普通公共 Git 读取，不能把全过程写成零网络。

没有进行反自动化、WAF 通行、挑战处理或规避访问限制的测试，也不提供这类方法。cleanup 自身抛错、初始化中途遗留、SessionRunner finally 传播、并发关闭、资源所有权转移与真实崩溃恢复均未覆盖。VM 只是本次夹具的依赖隔离，不是任意未知代码的强安全沙箱；安全边界来自有限已审阅源码、逐文件指纹、白名单导入与不接入外部能力。

固定提交的 22 个跟踪文件中未找到 LICENSE/COPYING 或许可声明；没有据此推断分发或商业授权。练习 ZIP 的六个自写文件为 harness.mjs、inspect.mjs、viewer-tests.mjs、reproduce.sh、source-manifest.json、README.md，不含上游源码、node_modules 或浏览器。指南与图示是独立教学总结，来源以固定链接定位。

原 PDF 由 ReportLab 直接生成，共 12 页；历史审核查看全部页面。HTML 仅结构、锚点与来源检查，没有浏览器视觉或打印验收。教材中的示意图不是浏览器任务截图。

## 最新公开知识读取范围

本次合并基于 GitHub main 快照 bcd08c5d817a348838f538e34d30e603c0c042f8。连接器完整读取并核对 Git blob SHA、UTF-8 字节数与 SHA-256：MOC、学习方法、仓库说明、两份模板、26 篇相关概念及 8 篇相关项目，共 39 份正文。26 篇概念包括上方“与已有知识的合并”中的 24 篇，以及 [[控制面与数据面]]、[[Agent输出协议契约]]；后二者用于区分调用分层与输出契约，并不声称本包装层实现相同协议。

该快照有 304 篇概念、104 篇项目笔记；另 278 篇概念与 96 篇项目仅做路径/标题筛查，未全文阅读，不称为全库正文查重或其他设备副本核验。8 篇项目为 agent-reach、how_to_live_better、ponytail、mcp_toolbox、google_colab_cli、metrik、qwen_image_2_1、ai_native_handbook。

[[项目笔记/how_to_live_better]] 与 [[项目笔记/ponytail]] 提供来源分层和负对照方法；[[项目笔记/mcp_toolbox]] 强调声明与执行强制分别验证；[[项目笔记/google_colab_cli]]、[[项目笔记/metrik]]、[[项目笔记/qwen_image_2_1]]、[[项目笔记/ai_native_handbook]] 分别提供记录、计量、契约与委托的相关证据纪律。旧项目的测试数量、版本、许可或平台能力不迁移成本项目事实。

此次新增本项目笔记，向三篇已有概念追加案例，并在 MOC 增加入口；不新增同义概念，不改写历史累计计数或已有正文。早期学习的 394 条元数据/20 篇正文范围仍保留在配套知识笔记，与本次较新公开快照的查重范围分开。

## 六份配套材料

- [彩色 PDF 指南](../../patchright_enhanced/delivery/patchright-enhanced-guide.pdf)
- [HTML 指南](../../patchright_enhanced/delivery/patchright-enhanced-guide.html)
- [练习包](../../patchright_enhanced/delivery/patchright-enhanced-exercise.zip)
- [历史实验日志](../../patchright_enhanced/delivery/patchright-enhanced-experiment.log)
- [知识笔记](../../patchright_enhanced/delivery/patchright-enhanced-knowledge-notes.md)
- [发布审核及历史证据复核](../../patchright_enhanced/delivery/patchright-enhanced-review.log)

## 固定来源

- [README](https://github.com/whaleyxbt/patchright-enhanced/blob/e38ab7ab9448db6f093f72ee097c18ca9905e84c/readme.md)、[环境示例](https://github.com/whaleyxbt/patchright-enhanced/blob/e38ab7ab9448db6f093f72ee097c18ca9905e84c/.env.example)、[包信息](https://github.com/whaleyxbt/patchright-enhanced/blob/e38ab7ab9448db6f093f72ee097c18ca9905e84c/package.json)
- [浏览器配置](https://github.com/whaleyxbt/patchright-enhanced/blob/e38ab7ab9448db6f093f72ee097c18ca9905e84c/src/config/browser.config.ts)、[应用配置](https://github.com/whaleyxbt/patchright-enhanced/blob/e38ab7ab9448db6f093f72ee097c18ca9905e84c/src/config/index.ts)、[管理器](https://github.com/whaleyxbt/patchright-enhanced/blob/e38ab7ab9448db6f093f72ee097c18ca9905e84c/src/browser/browser-manager.ts)
- [本次查重的学习方法](https://github.com/Smashwinny/reminder_knowlege/blob/bcd08c5d817a348838f538e34d30e603c0c042f8/.claude/skills/learn-project/SKILL.md)

返回 [[00-总览|知识库总览]]。
