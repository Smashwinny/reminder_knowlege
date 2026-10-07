---
tags: [项目笔记, 设计系统, 词法检索]
学习审核日期: 2026-10-05
上游仓库: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
固定版本: 477bcb28c9812b385cb51a4605ddf30d7b2266e2
许可: MIT
验证范围: 本地Python与CSV检索、规则推荐和选定测试
---

# UI UX Pro Max：词法检索与设计建议来源

## 是什么，能学到什么

UI UX Pro Max 将设计相关 CSV 语料、Python 搜索与规则组装、Agent Skill 使用说明放在同一项目中。本页只整理该固定版本已完成的单项目学习；本地脚本能返回设计建议，不代表宿主已加载技能、模型已执行设计任务或最终界面已经实现。

可以学习：用 [[BM25词法相关性排序]] 理解召回；区分查询域、参与匹配的字段与返回字段；追踪产品、规则和设计值的来源；分别检查拒答与回退；把建议、实现、交互和用户效果分层验收。

## 与已有知识的合并

- 新增 [[BM25词法相关性排序]]：词频饱和、逆文档频率与长度归一化；它与 [[混合检索与RRF融合]] 的多通道融合、[[BPE分词器]] 的子词编码不同
- 增补 [[混合检索与RRF融合]]：单通道词法排序与多域顺序调用的边界，不把它写成向量检索或完整 [[RAG检索增强生成]]
- 增补 [[设计令牌DesignToken]]：原始配色、派生值与实际组件消费分别取证；关联 [[DESIGN.md规范文档]]，不假设两种文档格式自动兼容
- 增补 [[证据优先质检ProofOverClaims]]：推荐文字、有限函数检查和真实 UI 验收分层，不新建同义“设计验收分层”页
- [[AgentSkills技能包]]、[[技能路由器与授权硬门]]、[[分层按需加载]]：关联技能说明与宿主使用，不声称已安装或建立执行硬门
- [[事实与判断分离]]、[[证据状态机]]、[[产物留痕与状态外置]]、[[AI味模式库与信号非证据]]：沿用证据纪律，排序分数或完整文档不代表质量与效果

[[项目笔记/awesome-design-md]] 提供设计规范背景，[[项目笔记/six_skills]] 提供技能与检测信号背景；[[项目笔记/agent-reach]]、[[项目笔记/archify]] 只作已有关联，本次没有重复它们的学习、安装或实验。

## 已有六步实验

原学习在 Python 3.12.14 中依次运行 snapshot → search → rank → design → tests → verify，2026-10-05 08:54:41–08:54:47 UTC 六步退出码均为 0。历史独立审核于 08:59:45–08:59:50 UTC 从新解压练习包逐条重放。此次公开整理和知识合并复核已有材料，没有重新执行实验或上游脚本。

- 61/61 项自建证据检查：2+18+5+32+0+4
- 73/73 个选定上游 unittest 测试方法，来自 13 个类；失败、错误、跳过均为 0。两组分开计，subTest 循环不额外计数；不是完整上游 CI
- 重复调用、冷/热缓存与 3 个新进程散列种子的有限一致性检查通过；不泛化为任意输入、版本或平台的确定性
- 历史审核另核查 29 个来源追溯对象的文件散列、行散列、逻辑数据行、物理行范围和整行内容；这不是 29 个新增测试方法，也不代表全部语料逐项审查

## 核心发现与容易误判的地方

1. **BM25 公式对拍有固定口径。** 对真实 products.csv 的 192 行、查询“SaaS dashboard”，按同一分词契约另写公式重算，全部分数与次序匹配，最大绝对差 0.0。前三项为 SaaS (General)、Micro SaaS、Analytics Dashboard。这证明该次实现与公式一致，不是独立相关性、审美或可用性基准。
2. **搜索契约不止一个分数。** search_cols 决定参与匹配的列，output_cols 决定返回列；返回 Accessibility 不等于按这个字段检索。域路由、身份匹配、阈值、建议词与回退还会影响最终结果。缓存签名使用 mtime_ns/size；材料中的 SHA-256 是额外取证，不是引擎缓存键。
3. **多域不是多模型并行。** 历史调用追踪顺序为 product、product、style、color、landing、typography，共六次搜索调用，其中五个不同域。被测 Python 路径是顺序循环与确定性规则，没有五路并行 AI 推理。
4. **查询含 dark 不等于独立模式参数。** “SaaS dashboard accessible”命中 SaaS (General)、Minimalism & Swiss Style、Friendly SaaS，并命中 if_ux_focused 规则；加入“dark mode”后产品类别变成 Smart Home/IoT Dashboard。整个查询和多个召回项一起改变，该入口没有显式 color-mode 参数，不能当作只改变颜色模式的受控对照。
5. **helper 派生值仍要保留身份。** 独立固定 SaaS (General) 颜色行时，light helper 返回原行，dark helper 改变 7 个颜色字段并增加 derived-dark 标记；这是派生配色，不是 CSV 中另有一条官方暗色原行。该例 ring/background 对比度约 3.454 只属于所测组合，未证明页面或整站无障碍通过。
6. **拒答与回退使用不同输入。** 直接 UX 检索“zzqqxx totally made up gibberish”拒答；设计生成器对“zzqqxx flarble blorpt”仍产出回退建议，reasoning_default=true，product/reasoning 来源身份为空。这是分层观察，不能当作同输入 A/B 或产品识别成功。

## 未验证边界与材料许可

没有运行全量测试、安装器、hooks、全局技能写入、持久化入口、完整宿主/模型/API 集成、浏览器建站、部署、真实用户任务、转换率或实际 UI 可访问性验收。选定测试不含 TestPersistence、四项 light 输出格式测试、landing/stack 与 generated catalog 契约类及其余模块。进程内 socket 审计拒绝网络事件不等于 OS 沙箱或任意代码安全保证。

练习包保留 49 个固定来源文件的原始字节、完整 MIT 许可与 Copyright (c) 2024 Next Level Builder；README 仅改交付文件名为 README.upstream.md。字体/图标数据是元数据，没有打包字体二进制；MIT 不重新许可这些元数据引用的第三方资产。

公开 PDF 仍为 ReportLab 直接生成的 13 页，历史实验与本次公开副本审核分别留证；当前逐页检查见独立审核日志。HTML 只做结构、锚点与来源检查，浏览器视觉与 HTML→PDF 路径仍受限、未经验证，本次没有重试。图示和合成 brief 不是实际 UI 成果；学习材料完成不代表读者已掌握或真实产品通过验收。

## 最新公开知识读取范围

此次合并基于 GitHub main 快照 10cbcbc6f15227aa2c5c7a16f2141f99a039948f。完整读取并核对 Git blob SHA、UTF-8 字节数与 SHA-256：MOC、学习方法、仓库说明、两份模板、20 篇相关概念和 11 篇相关项目，共 36 份正文。

20 篇概念为 [[AgentSkills技能包]]、[[技能路由器与授权硬门]]、[[DESIGN.md规范文档]]、[[设计令牌DesignToken]]、[[RAG检索增强生成]]、[[RAG架构谱系]]、[[混合检索与RRF融合]]、[[事实与判断分离]]、[[证据状态机]]、[[证据优先质检ProofOverClaims]]、[[产物留痕与状态外置]]、[[AI味模式库与信号非证据]]、[[代码管边界提示词管判断]]、[[修改与约束分离]]、[[开源验货三查]]、[[分层按需加载]]、[[接缝与桩实现StubSeam]]、[[固定版本中的跨文件时间漂移]]、[[BPE分词器]]、[[向量与Embedding]]；BM25 是此次新增，不计入已读旧概念。11 篇项目为 awesome-design-md、six_skills、agent-reach、archify、memmy、vector_database_qdrant、google_colab_cli、metrik、qwen_image_2_1、ai_native_handbook、patchright_enhanced。检索对照中的 [[项目笔记/memmy]]、[[项目笔记/vector_database_qdrant]] 没有与本项目做效果竞赛，其他项目的数量、许可和平台结论也不迁移为本次事实。

该快照有 304 篇概念、105 篇项目笔记；另 284 篇概念与 94 篇项目只做路径/标题层筛查，未全文阅读。BM25 与已读的融合、向量与分词笔记相关而非同义，因此独立成篇；不能由此宣称全库正文无重复、其他副本已核验或“从未学过”。此次仅新增本项目与 BM25，向三篇旧概念追加案例并在 MOC 加入口，不改写历史计数或既有正文。早期学习的 394 条元数据/24 篇正文范围另留在配套知识笔记。

## 六份配套材料

- [彩色 PDF 指南](../../github_tools_increment/delivery/UIUX增量学习_彩色指南.pdf)
- [HTML 指南](../../github_tools_increment/delivery/UIUX增量学习_彩色指南.html)
- [练习包](../../github_tools_increment/delivery/UIUX增量学习_练习包.zip)
- [历史实验日志](../../github_tools_increment/delivery/UIUX增量学习_实验日志.txt)
- [知识笔记](../../github_tools_increment/delivery/UIUX增量学习_知识笔记.md)
- [发布审核及历史证据复核](../../github_tools_increment/delivery/UIUX增量学习_独立复核日志.txt)

## 固定来源

- [README](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/477bcb28c9812b385cb51a4605ddf30d7b2266e2/README.md)、[MIT LICENSE](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/477bcb28c9812b385cb51a4605ddf30d7b2266e2/LICENSE)
- [检索核心](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/477bcb28c9812b385cb51a4605ddf30d7b2266e2/src/ui-ux-pro-max/scripts/core.py)、[设计建议组装](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/477bcb28c9812b385cb51a4605ddf30d7b2266e2/src/ui-ux-pro-max/scripts/design_system.py)、[命令行入口](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/477bcb28c9812b385cb51a4605ddf30d7b2266e2/src/ui-ux-pro-max/scripts/search.py)
- [产品语料](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/477bcb28c9812b385cb51a4605ddf30d7b2266e2/src/ui-ux-pro-max/data/products.csv)

返回 [[00-总览|知识库总览]]。
