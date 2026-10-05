# Easel：内容产物契约与发布证据的知识入库提案

原学习日期：2026-10-05 UTC。本稿保留当时知识查重、源码观察和本地组件实验的历史范围。公开副本于2026-10-05清理与更新；本次整理不新增学习实验，也不把当时查重结论扩展为全库结论。当前合并由云端协调者按最新公开库复核并处理，具体提交状态以发布记录为准。

## 1 查重范围与证据等级

原学习采用的公开知识索引固定于Smashwinny/reminder_knowlege@1f61909da967cea8bc68dbfaffc642a4331b3352；原学习方法与公开正文固定于1043e9d6080bff7af9724162e2c44559fab63e40。复用三份参考文件前重验字节数、SHA-256和Git blob SHA-1，原方法全文阅读并与索引指纹相符。

索引共394条元数据，原学习全文读取并按索引字节数与SHA-256核验9篇相关正文，其余385篇只有元数据检索。原学习另检查有限补充资料并核验完整性。历史公开快照查重加有限补充资料不代表全库查重；本次最新公开vault查重须另述。对全部重建正文做名称/相关词检索，重点复读Skill、产物、配置、身份、授权与证据相关段落，没有逐项重验所有历史陈述。

Easel、ZJU-REAL/Easel在原学习的上述元数据与已读正文范围内无名称命中。原学习范围不含当时未核验的本地知识库、未提交修改、其他未公开笔记或385篇未读正文，不能写成“全库无重复”或“从未学过”。笔记存在不等于本人已掌握；哈希一致不证明所有事实正确。历史星标、价格、平台规则、默认值及旧项目实验表现不作为本轮Easel事实。

来源：[固定知识索引](https://github.com/Smashwinny/reminder_knowlege/blob/1f61909da967cea8bc68dbfaffc642a4331b3352/reminder-dot/cloud-reference/knowledge-index.json)、[原学习方法](https://github.com/Smashwinny/reminder_knowlege/blob/1043e9d6080bff7af9724162e2c44559fab63e40/.claude/skills/learn-project/SKILL.md)。

## 2 优先复用已有知识

- [[AgentSkills技能包]]、[[技能路由器与授权硬门]]已解释方法包、路由、执行与行动许可；Easel补实际入口和消费契约，不重新发明“Skill”概念，也不把目录清单视为全技能已掌握
- [[分镜表驱动生成]]、[[产物留痕与状态外置]]已解释结构化中间表示与文件接力；Easel补薄索引、创作意图文件、两类状态及消费者验证
- [[ai-video-pipeline]]已有“选题门/事实门由人把关”的内容流水线方法；仅作方法关联，不借用其历史战绩、TTS或视频渲染结果为Easel背书
- [[沙箱与审批正交]]、[[证据状态机]]、[[证据优先质检ProofOverClaims]]、[[接缝与桩实现StubSeam]]已有充分的权限和验收基础；不另造同义“离线不是端到端”笔记

## 3 优先增补：薄索引传位置，简报传意图

一句话定义：跨工序索引只记录产物位置、步骤状态与简短摘要，完整内容和不能从成品反推的创作意图分别保存在文件中，由下游明确读取。

领域：内容工程、Agent工作流、产物契约。

固定Easel规范采用outputs/主题目录：最终成品放根目录，中间素材放assets/；.easel.json同时承载展示头和steps历史。规范明确manifest是薄索引，不把全文塞入summary；受众、基调、钩子、do/don't等意图落到brief.md并登记为outputs。这样下游可以区分“去哪里读”和“为什么这样做”。

自写例子：一篇虚构校园科学社的短文，note.md保存正文，brief.md保存“面向初学者、每次只解释一个实验、不含真实学生信息”，.easel.json登记路径。仅一行摘要无法代替正文或这些限制。这里是教学设计，不代表模型已经创作或平台已经发布。

源码中的record只是追加调用方提供的路径、摘要和状态，没有自动检查这些文件是否存在、内容是否正确或媒体能否打开。因此应把“索引登记成功”与“产物有效”分开验证。原[[分镜表驱动生成]]中“表填满的那一刻，片子就成立了”宜收窄为“结构化字段为后续工序提供输入”；文件存在、解码、渲染、声画同步和质量需要另行验收。

合并建议：首先增补[[产物留痕与状态外置]]，与[[分镜表驱动生成]]互链。Easel使用项目级索引，Storyboard使用镜头级媒体字段，不把两者说成同一schema。

来源：[产物接口规范](https://github.com/ZJU-REAL/Easel/blob/6c049ceb73b1b74a73448664dcd4dbc7e051442a/docs/SKILL-SPEC.md)、[manifest读写实现](https://github.com/ZJU-REAL/Easel/blob/6c049ceb73b1b74a73448664dcd4dbc7e051442a/skills/shared/scripts/manifest.py)。证据等级：源码观察。

## 4 优先增补：项目展示状态与工序结果分开

一句话定义：项目给人的生命周期标签、某个工序的记录结果，以及外部服务确实发生的效果，是三个不能互相替代的对象。

领域：状态建模、软件验收、发布流程。

Easel展示头status接受draft/ready/published；steps中的status接受done/failed。meta只改本次传入字段，保留其余字段；record追加步骤；latest按可选layer过滤后返回最后一条登记记录，没有自动筛除failed。两个status域不构成强制发布状态机：把展示头登记为published，没有证明某平台收到内容；返回最近一步，也没有保证它成功。

自写例子：最近制作步骤为failed，下游应检查该状态和文件，不能因为latest返回found=true就继续发布。另一个项目即使标签写ready，也仍要独立确认正文、素材、用户授权和目标账号。这个例子只解释状态含义，不宣称已实测上述负样本。

路径约束也有独立执行位置：output_paths.py验证产物目录布局、越界路径和系统目录许可；manifest自己的路径选择函数没有自动调用这个验证器。因此“规范要求所有新脚本调用”与“每个已有入口已接入”需要分开，不宣称本次已审完所有写入路径或建立OS沙箱。

合并建议：优先为[[证据状态机]]和[[产物留痕与状态外置]]增加内容生产案例。云端协调者核对最新公开库没有同义条目后，才考虑独立“内容产物状态契约”。

来源：[manifest实现](https://github.com/ZJU-REAL/Easel/blob/6c049ceb73b1b74a73448664dcd4dbc7e051442a/skills/shared/scripts/manifest.py)、[输出路径检查](https://github.com/ZJU-REAL/Easel/blob/6c049ceb73b1b74a73448664dcd4dbc7e051442a/skills/shared/scripts/output_paths.py)。证据等级：源码观察。

## 5 项目案例：创作者画像不是平台登录身份

一句话定义：创作者画像描述内容该怎样写；登录账号标识哪个平台主体；发布授权决定当次是否可以代为行动，三者要分别取证。

领域：内容个性化、配置管理、身份与授权。

persona.py按identity、style、audience、platforms、preferences、memory六个文件的顺序读取非空Markdown，再附加其他Markdown文件。profile_exists只检查目录是否存在；persona_prefix把画像名和账号记忆范围作为消息前缀交给宿主。它本身没有登录平台，也不证明六份画像完整、事实准确、模型遵守风格或记忆隔离得到强制执行。

自写例子：虚构“校园科学社”画像写着“科普风格、面向初学者、目标小红书”，只提供创作上下文。它不是小红书登录凭据，也不批准发帖。若实验仅加载这几个文件，只能报告读取/拼接/前缀行为，不能报告账号接入或模型内容质量。

合并建议：保留为Easel项目案例，与[[技能路由器与授权硬门]]互链，依据本节源码区分画像上下文、平台身份和发布许可，不新建泛化“账号安全”同义笔记。

来源：[画像共享助手](https://github.com/ZJU-REAL/Easel/blob/6c049ceb73b1b74a73448664dcd4dbc7e051442a/easel/persona.py)、[Skill宿主入口](https://github.com/ZJU-REAL/Easel/blob/6c049ceb73b1b74a73448664dcd4dbc7e051442a/easel/commands/skill.py)。证据等级：源码观察。

## 6 项目案例：发布前检查必须写清检查了什么

一句话定义：规则扫描、完整性检查、内容质量判断、事实/版权核对、用户批准与外部发布回执，各回答不同问题，不能用一个“通过”覆盖全部。

领域：内容安全、验收设计、行动授权。

content_guard.py用模式和可选环境字面值查疑似泄露，分类区分BLOCK与WARN；AI措辞和模型名仅提醒。guard_or_die在exec_mode且没有allow_unsafe时才对BLOCK命中退出7；dry-run或显式放行分支只告警。CLI scan对BLOCK命中返回7。描述时必须指出实际调用入口与参数，不能泛称所有入口都不可绕过。

扫描没有命中，只说明指定规则和输入范围内没有检出阻塞项，不证明事实准确、版权成立、平台接受、用户批准或发布成功。公开内容应按实际规则保留必要的AI标识；不能把代码中的AI措辞提醒解读为应隐瞒生成方式。

publish-checklist与quality-gate主要是要求OpenClaw执行的SKILL文档。前者关注完整性，后者要求合规/质量分析。easel skill入口把消息交给OpenClaw agent；仅阅读文档或运行本地扫描器，不等于执行了这两个Skill。固定版本中publish-checklist仍提meta.json，而总规范使用.easel.json，说明文档与消费者要逐项对照，不能靠相似名称假定契约一致。文档列的平台限制也注明是历史参考值，不能当最新规则。

合并建议：追加到[[技能路由器与授权硬门]]、[[证据优先质检ProofOverClaims]]和Easel项目笔记，明确提示规则与真正执行检查的接缝。

来源：[内容扫描与执行闸门](https://github.com/ZJU-REAL/Easel/blob/6c049ceb73b1b74a73448664dcd4dbc7e051442a/skills/shared/scripts/content_guard.py)、[完整性检查Skill](https://github.com/ZJU-REAL/Easel/blob/6c049ceb73b1b74a73448664dcd4dbc7e051442a/skills/openclaw/skill-publish-checklist/SKILL.md)、[质量检查Skill](https://github.com/ZJU-REAL/Easel/blob/6c049ceb73b1b74a73448664dcd4dbc7e051442a/skills/openclaw/skill-quality-gate/SKILL.md)。证据等级：源码观察。

## 7 真实本地组件实验与项目结论

固定源码ZJU-REAL/Easel@6c049ceb73b1b74a73448664dcd4dbc7e051442a；pyproject版本0.2.1、包内版本0.1.1、git describe为v0.2.1-79-g6c049ce，完整SHA为准。Linux x86_64、Python3.12.14标准库。原始实跑UTC 2026-10-05T13:46:00.680168至13:46:00.810746。未改动上游模块，仅自建harness将persona目录指向练习夹具，并用runpy按记录argv运行组件。根许可Apache-2.0，所有第三方技能参考资料的许可未全面认证；ZIP仅带最小模块和根许可，不带这些技能参考资料。

主实验有六个内部阶段：建立并修改六文件虚构画像；显式验证路径并保存草稿；观察初稿拒绝；人工修订并重查；建立索引、改标签并找回正文；运行三项上游自测入口并核对源码副本未变。共有15/15自写命名检查、3/3未改动上游selftest入口、20次组件调用，三种单位不能相加，未运行全量pytest。

虚构画像“纸页角落”仅style.md改变，其他五维指纹不变；画像前缀明确该目录的memory.md，未验证模型实际遵循。四个不合规输出路径被拒绝。manifest未内置调用路径校验器，是harness显式调用；不能称作上游统一安全保护。

本地自写中文初稿social_count为365，超出自选140±5%（133–147），字数校验退出1。合成私网IP触发1处proxy-ip发现，content_guard CLI scan退出7；7是退出码。删除冗余段落和合成串后的人工修订稿计数143，两项检查退出0。这个目标仅为练习阈值，不是最新微博官方规则。没有模型生成、个人秘密或真实账号输入。

manifest latest实际返回过failed记录；修订后历史依次为done、failed、done，但项目展示状态保持draft。非法kind输入退出2且文件字节不变。assets索引有3项，包括隐藏.easel.json；以weibo及两标签筛选只找到1篇成品。平台来自路径规则，并非自动读取manifest的平台字段。archive/--apply未执行。

原始尝试1在执行上游前被自建进程内审计hook拦住：环境描述platform.platform()试图访问子进程/devnull。仅将harness改为os.uname后尝试2成功，两次记录保留。审计hook是进程内测试守卫，不是OS级沙箱；没有安装全局hook。原manifest自测故意产生非法kind的argparse stderr，整体退出0，不能把它误记为本轮失败。

指南的6条学习命令已在全新解包目录逐条原样执行：首条运行完整六阶段，后5条读取并验证画像、拒绝、修订、索引与源码/自测证据。所有命令、UTC时间、原始输出、退出码和失败判据见实验日志；原始上游manifest时间使用UTC+8，原素材索引使用主机当地UTC-7，不能不换时区就比较字符串。重放时间戳和绝对路径会变化。

未测：OpenClaw宿主、Easel主CLI、Web服务、模型推理、生图/TTS/视频、真实账号登录、平台审批、外部发布、数据归因与营销效果。扫描通过不是完整质量/事实/版权审查，也不是发布授权。原始社媒材料访问返回HTTP 403，未读取全文。

## 8 当前公开库合并安排

由云端协调者核对最新公开库与同义内容，保留已有编辑；优先增补已有概念并双向链接，再整理Easel项目笔记、实际实验与未知项，最后更新总览。知识合并、文件发布和提交状态分别核验，以对应发布记录为准。原学习只形成提案的历史事实不改写为当时已完成合并。

## 9 实际全文核验的公开知识正文

AgentSkills技能包；技能路由器与授权硬门；分镜表驱动生成；ai-video-pipeline；产物留痕与状态外置；证据优先质检ProofOverClaims；证据状态机；接缝与桩实现StubSeam；沙箱与审批正交。它们均固定于公开正文提交1043e9d6080bff7af9724162e2c44559fab63e40；精确来源、字节数和散列列在配套公开知识清单。

- [AgentSkills技能包](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/AgentSkills%E6%8A%80%E8%83%BD%E5%8C%85.md)；UTF-8 1536字节；SHA-256：bb055a1f106f721c5c71a3a2b359c16d11190fbc261c772d63a7bbc3782f011b
- [技能路由器与授权硬门](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%8A%80%E8%83%BD%E8%B7%AF%E7%94%B1%E5%99%A8%E4%B8%8E%E6%8E%88%E6%9D%83%E7%A1%AC%E9%97%A8.md)；UTF-8 2140字节；SHA-256：8e122f9a4d1cb581bbc11303a0952f46b81b8d8251c938067e38db926f90ff4e
- [产物留痕与状态外置](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E4%BA%A7%E7%89%A9%E7%95%99%E7%97%95%E4%B8%8E%E7%8A%B6%E6%80%81%E5%A4%96%E7%BD%AE.md)；UTF-8 2389字节；SHA-256：6aba36f09afc580c08a669663e1ddaef6fa2c99067fcfedb65f56ba81a5ecceb
- [证据优先质检ProofOverClaims](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%AF%81%E6%8D%AE%E4%BC%98%E5%85%88%E8%B4%A8%E6%A3%80ProofOverClaims.md)；UTF-8 3593字节；SHA-256：c54ea2f3bcfe830556942d04c502ba84472a7382c45b76dd07401861e44c2fac
- [证据状态机](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%AF%81%E6%8D%AE%E7%8A%B6%E6%80%81%E6%9C%BA.md)；UTF-8 2488字节；SHA-256：4ac12b197891357591ebd092a9120bd67fa6fa1a09a407ed9c0fea3bc9b97328
- [接缝与桩实现StubSeam](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%8E%A5%E7%BC%9D%E4%B8%8E%E6%A1%A9%E5%AE%9E%E7%8E%B0StubSeam.md)；UTF-8 1752字节；SHA-256：83decb2724ea3ac736e0f9c4c89e17e043504be4733162e6ee44d7988c976804
- [沙箱与审批正交](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%B2%99%E7%AE%B1%E4%B8%8E%E5%AE%A1%E6%89%B9%E6%AD%A3%E4%BA%A4.md)；UTF-8 3248字节；SHA-256：a9e65c39d85a821884b50e6e2a4a1a1944cd18c4fd7961cb8a6c9f65cd645a41
- [分镜表驱动生成](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%88%86%E9%95%9C%E8%A1%A8%E9%A9%B1%E5%8A%A8%E7%94%9F%E6%88%90.md)；UTF-8 1574字节；SHA-256：2641bc7f44c9543b6084932b7716291a4e69fde074ac1d25fa313118d10240e5
- [ai-video-pipeline](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/ai-video-pipeline.md)；UTF-8 3596字节；SHA-256：511447ea68b28960a3af7efdaf38667d3a7bbd87f2f92eff9d3eab31933a1d7e
