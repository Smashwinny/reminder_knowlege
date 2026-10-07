# Patchright Enhanced 知识笔记

历史学习日期：2026-10-05 UTC。公开整理未重跑实验；以下实测数据保留原学习时点。主题限于 whaleyxbt/patchright-enhanced 的接口封装、配置、生命周期和失败诊断。

固定来源为 whaleyxbt/patchright-enhanced@e38ab7ab9448db6f093f72ee097c18ca9905e84c。已完成知识查重、源码检查与真实包装层单元实验；20 个当前行为断言匹配，包含已确认的缺陷。本稿不声称已启动浏览器、访问目标网页或完成浏览器任务。

## 1. 查重范围

固定公开知识索引共394条元数据；本次实际全文读取并核验20篇相关公开概念/项目笔记，其余374篇只有元数据检索。公开索引固定于 Smashwinny/reminder_knowlege@1f61909da967cea8bc68dbfaffc642a4331b3352，相关公开正文固定于1043e9d6080bff7af9724162e2c44559fab63e40。

以上范围只描述固定公开快照的实际阅读范围，不是全库全文覆盖；相关笔记存在也不代表读者已经掌握。复用时先检查同义项，保留版本和证据范围。

## 2. 复用已有概念，避免重复

- [[能力层与后端路由]] 与 [[agent-reach]] 已讲安装、体检与路由。这里只用来定位wrapper所在层，不重复Agent-Reach项目或实验
- [[健康探测三态]] 已区分依赖缺失、存在却损坏、超时/错误。增补浏览器链路诊断时，应保留各失败阶段，不把它简化成单一可用布尔值
- [[接缝与桩实现StubSeam]] 已讲隔离外部服务。增补真实wrapper与fake后端的证据边界，不把fake结果当作真实浏览器结果
- [[Provider适配层与错误契约]] 提供检查错误传播的架构视角；其特定LLM接口的异常规则不能直接套到浏览器API
- [[工具调用生命周期]] 与浏览器资源生命周期仅相关。前者是MCP调用循环，后者关注进程、上下文与页面等对象的创建和清理，不做同义合并
- [[确定性选择器模式]] 是LLM特征与确定性决策组合，和DOM selector/locator并非同一事物，不能误合并
- [[能力运行时]] 关注能力插件共享Agent循环；wrapper存在本身并不能证明有这套能力注册架构
- [[沙箱与审批正交]]、[[代码管边界提示词管判断]] 保留环境能力和行动授权的区分；不会因为依赖可运行而取得新目标、新身份或新访问方式的权限

## 3. 候选增量：检索、执行与渲染证据分层

一句话定义：拿到页面文本、浏览器执行脚本、形成可见画面和完成预期操作是不同层的结果，各自需要对应证据。

领域：浏览器自动化、信息检索、软件测试。

普通例子：程序读到了一个网页标题，只能支持标题获取成功；不能据此确认页面按钮可点击。即使页面截图存在，也还应核对实际显示了什么、交互是否发生，以及结果是否满足任务。

知识关联：[[控制面与数据面]] 提供分层检查的类比；[[证据状态机]] 防止把计划或声明展示成已完成；[[证据优先质检ProofOverClaims]] 要求相应运行证据。

合并建议：优先在Patchright Enhanced项目笔记中作证据分层小节。固定索引没有明确同名条目，但未读正文仍可能已有相关内容；先查重，再决定是否独立成篇。

边界：这是本轮教学综合，不冒充上游自带术语，也不表示本次已经进行了浏览器渲染。

## 4. 优先增补：wrapper契约与后端集成分开验收

一句话定义：wrapper对参数、调用顺序、返回值和清理职责的处理，可以与真实后端是否可启动、可连接、可完成任务分别测试。

领域：接口设计、可测试性、软件验收。

普通例子：fake后端记录收到的参数并按约定返回对象，可以验证wrapper有没有遗漏参数；fake记录了close调用，可以验证调用是否发出。它们不能证明操作系统中的浏览器进程真的退出，更不能证明目标站点交互成功。

知识关联：[[接缝与桩实现StubSeam]]、[[证据优先质检ProofOverClaims]]、[[产物留痕与状态外置]]。

合并建议：优先给StubSeam增补“真实wrapper、合成后端、真实浏览器三者标明”的案例，不再新建“mock测试”同义笔记。

设计时应记录：未修改的上游函数和文件指纹、被替换的接缝、fake行为、正常/异常用例、断言和未测项。实际通过数量只能取本轮日志；不复制旧项目成绩。

## 5. 候选增量：浏览器资源的生命周期与所有权

一句话定义：为每个资源明确谁创建、谁使用、谁负责正常或异常路径的清理，避免对象返回成功却留下后台资源。

领域：资源管理、同步/异步编程、故障恢复。

普通例子：wrapper新建的资源是否应由它清理，与调用方传入的既有资源是否归调用方所有，需要看接口契约；不能只见一个close方法就猜所有权。初始化中途失败也要检查已创建的部分资源。

知识关联：[[工具调用生命周期]] 只提供流程分段类比；[[托管Harness与会话即资源]] 提供资源状态视角，但其云会话机制不等于本项目浏览器机制；[[失败反馈具体化]] 支持记录哪一步、缺什么、允许怎样修复。

合并建议：先作为项目案例；按实际源码确认对象与清理顺序后，再决定与现有资源管理概念合并或互链。实际 L05 仅确认管理器成功关闭清理后的局部幂等行为；不扩展为所有权系统、取消传播或完整崩溃恢复。

## 6. 优先增补：配置生效与故障阶段分别取证

一句话定义：配置被解析或被转发，与下游接受它并产生预期效果，是不同事实；故障信息应包含具体阶段。

领域：配置管理、适配层、可观测性。

普通例子：记录到了一个timeout参数，只能说明调用链上出现了这个值；不能据此确认导航、定位器和整体任务都受相同上限控制。需要核对参数属于哪个API，再按实际行为测试。

知识关联：[[Provider适配层与错误契约]]、[[健康探测三态]]、[[失败反馈具体化]]、[[证据状态机]]。

合并建议：配置优先级和故障定位作为项目案例增补。不要在没有实现依据时写“自动重试”“自动降级”“所有异常保证清理”等能力。

## 7. 方法复用：证据分层

- 有来源与断言已验证分开
- 共同契约、有限覆盖与负对照分别说明
- 声明或注解不等于实际强制执行
- 本地模块执行不证明远端资源与任务成功
- 数值保留状态、单位、时点；源码审阅不冒充运行证据
- 解析成功、契约满足和任务正确分层；合成输入保持明确标识
- 发现、授权与执行分层；访问或运行限制不能被工具能力覆盖

这些是可复用的方法，不把其他项目的版本、默认配置、政策、许可、测试数量或性能移植到本项目。

## 8. 复用范围

仅讨论已核对的 Patchright Enhanced 固定版本及相关公开知识。学习内容不提供规避反自动化检查、代理轮换、挑战处理、身份伪装或浏览器政策限制的方法。依赖失败或访问拒绝时按已授权范围停止、诊断和记录，不把换后端当成绕过许可。

复用时先核对同义概念；同义合并、相关互链，并保留本轮固定版本、实验日志和未测范围。索引没有同名项，不代表未读正文没有相关内容。

## 9. 本轮实际全文读取的20篇公开知识

以下正文都固定在1043e9d6080bff7af9724162e2c44559fab63e40，仅列来源和指纹，不批量转载。

1. [产物留痕与状态外置](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E4%BA%A7%E7%89%A9%E7%95%99%E7%97%95%E4%B8%8E%E7%8A%B6%E6%80%81%E5%A4%96%E7%BD%AE.md)
   - UTF-8：2389 字节；SHA-256：6aba36f09afc580c08a669663e1ddaef6fa2c99067fcfedb65f56ba81a5ecceb

2. [代码管边界提示词管判断](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E4%BB%A3%E7%A0%81%E7%AE%A1%E8%BE%B9%E7%95%8C%E6%8F%90%E7%A4%BA%E8%AF%8D%E7%AE%A1%E5%88%A4%E6%96%AD.md)
   - UTF-8：1427 字节；SHA-256：82baf8f30c908b3ea424d15f82b6d3124e40b3c1b023961bfd0c8abd1eb8b86d

3. [工具调用生命周期](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8%E7%94%9F%E5%91%BD%E5%91%A8%E6%9C%9F.md)
   - UTF-8：1411 字节；SHA-256：9f8e203fdc45687ecf8625edc7fe4fc3c766850385879f97623333710d2c5481

4. [开源验货三查](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%BC%80%E6%BA%90%E9%AA%8C%E8%B4%A7%E4%B8%89%E6%9F%A5.md)
   - UTF-8：1815 字节；SHA-256：836585db83f85f393815551357aad9b894567c5e57bc7c4623e088040c50b0ce

5. [托管Harness与会话即资源](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%89%98%E7%AE%A1Harness%E4%B8%8E%E4%BC%9A%E8%AF%9D%E5%8D%B3%E8%B5%84%E6%BA%90.md)
   - UTF-8：2905 字节；SHA-256：596bf0d1e5d38c769bf4b5fd6baa8201a7c442bd23c237fc2338218bac8d49fa

6. [接缝与桩实现StubSeam](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%8E%A5%E7%BC%9D%E4%B8%8E%E6%A1%A9%E5%AE%9E%E7%8E%B0StubSeam.md)
   - UTF-8：1752 字节；SHA-256：83decb2724ea3ac736e0f9c4c89e17e043504be4733162e6ee44d7988c976804

7. [控制面与数据面](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%8E%A7%E5%88%B6%E9%9D%A2%E4%B8%8E%E6%95%B0%E6%8D%AE%E9%9D%A2.md)
   - UTF-8：1575 字节；SHA-256：90267f9bf8041185daf02ce384e1367c4c8e3ed32beccf4dc6ae7ae9c7ef7409

8. [数据源降级链](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%95%B0%E6%8D%AE%E6%BA%90%E9%99%8D%E7%BA%A7%E9%93%BE.md)
   - UTF-8：1789 字节；SHA-256：7b4229977ca35e94e59a1547b3adc21ef9551be4fc6e96ee0e9a0ec5e403ed7f

9. [沙箱三态与Executor](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%B2%99%E7%AE%B1%E4%B8%89%E6%80%81%E4%B8%8EExecutor.md)
   - UTF-8：2157 字节；SHA-256：4d1113c17b1c8a8568ad3b44e73c7393ff7f7b4a6be44c3cd5bc3e620b1107a1

10. [沙箱与审批正交](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%B2%99%E7%AE%B1%E4%B8%8E%E5%AE%A1%E6%89%B9%E6%AD%A3%E4%BA%A4.md)
   - UTF-8：3248 字节；SHA-256：a9e65c39d85a821884b50e6e2a4a1a1944cd18c4fd7961cb8a6c9f65cd645a41

11. [能力运行时](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%83%BD%E5%8A%9B%E8%BF%90%E8%A1%8C%E6%97%B6.md)
   - UTF-8：1411 字节；SHA-256：1341c5c402b01ed0cc6641b8b4ba4b9be0024c03ec443b2300e0453bbe121678

12. [证据优先质检ProofOverClaims](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%AF%81%E6%8D%AE%E4%BC%98%E5%85%88%E8%B4%A8%E6%A3%80ProofOverClaims.md)
   - UTF-8：3593 字节；SHA-256：c54ea2f3bcfe830556942d04c502ba84472a7382c45b76dd07401861e44c2fac

13. [证据状态机](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%AF%81%E6%8D%AE%E7%8A%B6%E6%80%81%E6%9C%BA.md)
   - UTF-8：2488 字节；SHA-256：4ac12b197891357591ebd092a9120bd67fa6fa1a09a407ed9c0fea3bc9b97328

14. [Provider适配层与错误契约](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/Provider%E9%80%82%E9%85%8D%E5%B1%82%E4%B8%8E%E9%94%99%E8%AF%AF%E5%A5%91%E7%BA%A6.md)
   - UTF-8：3175 字节；SHA-256：6747c71d9ab9e007e5dd35330e4c733613e111498b987fdca973828259503986

15. [健康探测三态](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%81%A5%E5%BA%B7%E6%8E%A2%E6%B5%8B%E4%B8%89%E6%80%81.md)
   - UTF-8：1724 字节；SHA-256：e87a03d9cd6cf94292a456273b522baa891cb6e7121d65dfaa773726eeaf03bb

16. [失败反馈具体化](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%A4%B1%E8%B4%A5%E5%8F%8D%E9%A6%88%E5%85%B7%E4%BD%93%E5%8C%96.md)
   - UTF-8：1506 字节；SHA-256：2c74f5f7df56c688c8b338d5e4204deb5680f561babedee33e648edee00f6a6c

17. [确定性选择器模式](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E7%A1%AE%E5%AE%9A%E6%80%A7%E9%80%89%E6%8B%A9%E5%99%A8%E6%A8%A1%E5%BC%8F.md)
   - UTF-8：1380 字节；SHA-256：dd94627a200fc3874f675869c31a6eded52fc4a732bedd7ddfb1ea8324881fcc

18. [能力地板选型](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%83%BD%E5%8A%9B%E5%9C%B0%E6%9D%BF%E9%80%89%E5%9E%8B.md)
   - UTF-8：1580 字节；SHA-256：04ae0bad7425fe6daa783116a2dac8c83e6db62be03d258db18e4e1009377d6c

19. [能力层与后端路由](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%83%BD%E5%8A%9B%E5%B1%82%E4%B8%8E%E5%90%8E%E7%AB%AF%E8%B7%AF%E7%94%B1.md)
   - UTF-8：2320 字节；SHA-256：8a1462b22f56cc8171ba017b5498ac501e8ed3dfade9291971371e7dfbcd0828

20. [agent-reach](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/agent-reach.md)
   - UTF-8：2831 字节；SHA-256：8e4b2ab724b77ccf948dd8e01b6d9274fa066639418cb38a79ccf2d37e13468f


## 10. 项目笔记与实测结论

### 项目是什么

TypeScript 编写的 Patchright 包装层，负责配置、会话组织及 BrowserManager 资源管理。仓库名称为 patchright-enhanced；package.json 内包名为 ghostprobe。底层浏览器不在本次运行范围。

### 本轮主实验

现有 Node v24.19.0 通过 stripTypeScriptTypes 去除类型语法，将固定源码放入 VM。只执行 src/config/browser.config.ts、src/config/index.ts、src/browser/browser-manager.ts。fs 存在/建目录、代理标记、context.close、cleanupTempDir 是惰性替身；path.resolve 为纯路径运算。VM 不是处理任意恶意代码的强安全沙箱；安全边界来自已审阅的固定源码、白名单导入、逐文件 SHA-256 和不接入外部能力。

初次实际运行时间 2026-10-05 08:13:42 UTC，20/20 断言匹配，0 个断言失败：4 个浏览器配置、9 个应用配置、7 个生命周期用例。这里的 PASS 指与当前源码行为一致，包括缺陷；不等于 20 项健康验收。

- B01-B04：默认 headless=false；显式浏览器路径/时区生效；空字符串回退；未实现的 HEADLESS 环境变量无效果
- A01/A09：MAX_PARALLEL 未设置或为空字符串时为 2
- A02/A03：缺失目录只向惰性 fs 发出递归创建请求；已有目录不发出创建请求；未实际创建会话目录
- A04-A08：0、-1、oops、2junk、2.9 分别得到 0、-1、NaN、2、2，未拒绝这些输入
- L01-L05：空管理器无外部效果；setContext 保留对象引用；关闭与清理可分开；组合调用先 close 后 cleanup；成功后重复调用无额外效果
- L06：context.close 合成拒绝后错误向上传播、context 保留、cleanupCalls=0
- L07：第一次关闭合成失败、第二次成功后，才继续清理；这不是自动重试机制，也不是实测浏览器崩溃恢复

### 仅源码观察

- README/.env.example 的并发值 1 与函数空环境默认值 2 不同；.env 路径与空环境路径不能混用
- getStartPageUrl 空环境回退为空字符串，与 README/示例 URL 不同；该函数没有在本轮 VM 中执行
- BrowserConfig.locale 为必填而实现中的 locale 行被注释；没有运行 tsc，不写编译失败结论
- package.json 与 pnpm-lock.yaml 的依赖条目不一致；没有安装依赖，不写实际安装失败结论
- 当前提交 22 个跟踪文件中未找到 LICENSE/COPYING 或许可声明；许可待核实，练习 ZIP 不复制上游模块

### 未测和未完成

未执行上游测试、完整 TypeScript 构建、Patchright 导入、真实工厂、真实代理、真实文件清理、浏览器、导航、页面截图、性能基准或业务任务。cleanup 自身抛错、初始化中途资源遗留、SessionRunner finally 的完整传播路径也没有运行覆盖。不能据此断言任何目标站点可用。

主实验六步完整命令位于 PDF 第 9-11 页、HTML 实验部分及练习 ZIP README。来源和首次运行原始结果见实验日志；原学习 ZIP 解压/获取/六步复现记录与当前副本核验分别见独立审核日志。当前 PDF 是 ReportLab 直接生成的 A4，经 Poppler 全页渲染；HTML 浏览器视觉预览及 HTML 转 PDF 原路线受阻，本次未重试。

### 合并安排

项目笔记关联 [[接缝与桩实现StubSeam]]、[[证据优先质检ProofOverClaims]]、[[失败反馈具体化]]、[[开源验货三查]]。优先给已有概念增补固定版本案例，确无同义项时再考虑新增概念。

### 固定源码入口

https://github.com/whaleyxbt/patchright-enhanced/tree/e38ab7ab9448db6f093f72ee097c18ca9905e84c
