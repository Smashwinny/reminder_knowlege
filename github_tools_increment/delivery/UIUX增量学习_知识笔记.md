# UI UX Pro Max 知识笔记

历史学习日期：2026-10-05 UTC。范围限于 UI UX Pro Max 的本地 Python/CSV 检索与设计系统推荐。公开整理未重跑实验；本文保留固定来源、公开知识关联、历史结果和适用边界。

## 1. 目录与完整学习分开计

背景资料是一份 11 项工具目录。本轮只选 UI UX Pro Max 做一个完整增量，不把一个链接、一段介绍或目录收录计为完整学习。Agent-Reach 与 Archify 已有项目笔记，本轮仅链接既有成果；其余项目没有因此获得完整学习结论。

UI UX Pro Max 固定来源：nextlevelbuilder/ui-ux-pro-max-skill@477bcb28c9812b385cb51a4605ddf30d7b2266e2。其本地搜索与规则组装代码、Agent Skill 使用说明、实际宿主调用和最终界面是不同层，需要分别验证。

## 2. 查重范围

固定公开知识索引共 394 条元数据，本轮实际全文读取并核验 24 篇相关概念/项目笔记，其余 370 篇只有元数据检索。公开索引固定于 Smashwinny/reminder_knowlege@1f61909da967cea8bc68dbfaffc642a4331b3352，相关公开正文固定于 1043e9d6080bff7af9724162e2c44559fab63e40。

在固定公开索引的标题/路径和已读 24 篇公开正文中，没有找到 UI UX Pro Max 的既有完整学习记录。名称检查覆盖 UI UX Pro、UI/UX Pro、ui-ux-pro、ui_ux_pro、uipro、nextlevelbuilder 与 uupm.cc 等变体。此结论仅针对该历史快照的实际阅读范围，不覆盖其他版本或其余未读正文；不能写成“从未学过”或“全库无重复”。笔记存在也不等于读者已掌握。

## 3. 已有概念只补新案例

- [[AgentSkills技能包]]：继续区分方法说明、执行脚本与宿主加载。可用代码存在，不代表某个编程助手已经安装、加载或成功使用它
- [[DESIGN.md规范文档]]、[[设计令牌DesignToken]]、[[awesome-design-md]]：设计决策命名与文字规范已有基础。当前新增是如何从语料和规则生成候选规范；输出文件存在不证明组件正在引用它，也不保证格式与既有 DESIGN.md 完全兼容
- [[RAG检索增强生成]]、[[RAG架构谱系]]、[[混合检索与RRF融合]]：仅作关联。当前本地词法检索/规则组装不是向量搜索，不是 RRF 融合，也不能单独算成“检索后调用大模型”的完整 RAG
- [[图像提示八要素]]、[[提示词模板]]、[[修改与约束分离]]、[[角色一致性锚定]]：复用“用途明确、变量分离、保留约束可检查”的写法。图像生成/编辑与 UI 设计任务不同，不重新展开旧图像教程；旧 Lint 分数不证明当前设计质量
- [[事实与判断分离]]、[[证据状态机]]、[[证据优先质检ProofOverClaims]]：区分数据记录、排序结果、规则推荐、实现和用户效果。不将历史星标、商业收入、节省时长、转换率或旧项目实验数值带入本轮
- [[agent-reach]]、[[archify]]：仅作已经读过的相关项目链接。本轮没有重复安装、实验或增加完成数

## 4. 候选新概念：BM25 词法相关性排序

一句话定义：根据查询词在每条记录中的出现情况、这些词在整个语料中的稀有程度，以及记录长度归一化，对记录进行词法相关性排序。

领域：信息检索、搜索系统。

普通例子：想找面向咖啡店的简洁页面，把需求中的产品、风格和用途词送入本地语料检索。某词在少数条目出现时通常更有区分力；把同一个词塞很多遍也不应无限加分；长记录不该只靠文字多而占优势。这是排序机制，不是模型理解用户全部意图的证明。

本项目静态实现：core.py 的 BM25 类先做小写、同义词归一化、标点处理、按空白切分、短词和停用词过滤，再建立词频、文档频率与平均长度，按 k1、b 参数计算排序。项目搜索还叠加域选择、身份匹配、阈值、建议词或回退等逻辑，因此“最终搜索结果”不等于裸 BM25 公式的直接输出。非空字符串也可能经过分词后缺少有效词；中文字符能够保留，不等于实现了中文分词或跨语言语义理解。

与已有概念的关联：[[混合检索与RRF融合]] 已讲关键词与向量通道各自的长短处；本条只补其中词法排序部件。[[RAG检索增强生成]] 可使用检索部件，但检索本身不等于生成流程。

合并建议：固定索引没有独立 BM25 同名条目，先作为候选。在目标知识库确认同义内容后，再决定独立成篇或并入已有检索笔记。不把 BM25 分数写成审美分、质量百分比、可信度概率或可用性成绩。

## 5. 项目增量：查询域、可检索列与返回列

一句话定义：搜索行为同时受选中语料域、参与匹配的字段、输入归一化及返回字段控制；用户看见的字段不一定参与搜索。

领域：检索工程、数据契约、可解释性。

普通例子：某条设计风格记录返回 Accessibility 字段，并不自动意味着搜索时会匹配这个字段；需要核对该域的 search_cols。想查交互建议时，明确 UX 域与让自动路由猜测可能得到不同结果，应先记录实际选中的域。

与已有概念的关联：[[事实与判断分离]] 提醒先记录实际域、实际语料和真实返回值；[[证据状态机]] 提醒区分零命中、过滤后为空、回退命中和读取失败。

合并建议：先放进本项目笔记的“检索契约”小节，不为每个 CSV 新建一个概念。保存精确查询、域、上限参数、数据与脚本指纹、原始结果；换语料后不能照搬旧排序和旧命中数。

## 6. 项目增量：推荐组装与逐字段来源

一句话定义：最终设计系统建议由多个检索结果、规则、优先级与默认值共同组装，需要追踪各字段来自哪里，不能仅看最后文档是否好看。

领域：规则系统、设计工具、数据溯源。

本项目静态链路：先查 product 得到类别，再匹配类别规则、多域搜索，选择风格、颜色、字体与落地页模式，最后生成结构化对象及可读文本。某些字段可能使用回退值；CSV 的一行、规则的优先级与最终选择不应被混成同一条事实。

普通例子：给同一 brief 加上 dark 或 light，会改变查询文本；新词可能同时改变产品类别或其他召回项。因此完整输出的差异只能说明“改了这段查询后，结果变了”，不能宣称只隔离了颜色模式。若另做固定类别的 palette helper 对照，需单独标明其函数级测试范围。

与已有概念的关联：[[设计令牌DesignToken]] 管规范中的值如何命名与复用；本项目案例补充值如何被选出来。[[产物留痕与状态外置]] 管查询、结果与来源指纹如何保留。

合并建议：增补已有设计规范项目的“来源与生成”章节并互链 UI UX Pro Max；不要把规则输出自动称为设计专家评审结论。

## 7. 优先补充：设计建议与界面验收分层

一句话定义：检索到建议、生成设计规范、实现界面、验证交互和验证用户效果，是逐层增加要求的不同结果，前一层成功不保证后一层。

领域：前端工程、质量保证、可访问性、实验方法。

普通例子：CSV 提醒文字要有足够对比度，只说明检索到了建议。只有在实际前景/背景颜色、字体大小与状态下测量，才有对应组合的证据；即便对比度满足要求，也不能替代键盘、焦点、名称角色、错误反馈、缩放、动效偏好等其他检查。若本轮未做这些检查，就不能写“无障碍通过”。

关联：[[证据优先质检ProofOverClaims]] 已讲运行证据；[[AI味模式库与信号非证据]] 已讲信号不能越级为证明；既有 Patchright Enhanced 学习已强调检索、执行与渲染分层。本轮优先增补设计任务的案例，不新建同义“证据分层”条目。

历史实验支持的结论：真实本地上游 Python 代码处理固定 CSV 与普通合成 brief，返回记录或设计系统文本，并保留实际运行输出。实验不是真实用户研究，没有验证生产转化率，没有部署网站，没有调用付费模型，也没有证明任何最终界面通过可访问性验收。本轮实际结果如下；不复制旧项目数字。

### 7.1 本轮实际实验结论

2026-10-05 08:54:41–08:54:47 UTC，在 Python 3.12.14 中执行 snapshot → search → rank → design → tests → verify 六步，六步返回码均为 0。61 项自建证据检查匹配预期，另有 73 个选定上游 unittest 测试方法通过，失败/错误/跳过均为 0；subTest 循环未额外计数，也没有运行完整上游 CI。自建检查与上游测试是不同口径，不相加冒充一种覆盖率。

- 真实搜索：对产品、风格、颜色与 UX 域查询，返回记录能定位到固定 CSV 的具体行和行内容指纹；重复、冷缓存及三个新进程散列种子下，本轮输出一致
- BM25 对照：对实际 products.csv 的 192 行，在查询“SaaS dashboard”下，按相同分词契约另写公式重算，全部分数与顺序匹配，最大绝对差为 0.0。前三项为 SaaS (General)、Micro SaaS、Analytics Dashboard；这只验证该实现与公式的一致性，不是独立的检索相关性基准
- 设计系统：普通合成 brief“SaaS dashboard accessible”得到 SaaS (General)、Minimalism & Swiss Style 与 Friendly SaaS 字体配对，命中 if_ux_focused 规则；保留了产品、规则、风格、颜色、字体与落地页来源身份
- 查询敏感性：改成“SaaS dashboard accessible dark mode”后类别变为 Smart Home/IoT Dashboard，风格等也改变。没有使用显式 color-mode 参数，因为该入口没有这个参数；此结果不是孤立颜色模式的对照
- 独立颜色函数检查：固定 SaaS (General) 颜色行，light helper 返回原行，dark helper 保留产品身份、派生 7 个颜色字段并附 derived-dark 标记。测到的单项 ring/background 对比度与 helper 阈值检查只属于该函数，不等于整站无障碍验收
- 不同负样本：直接 UX 检索“zzqqxx totally made up gibberish”拒答；设计生成器处理另一条无意义输入“zzqqxx flarble blorpt”仍生成回退建议，同时 reasoning_default=true，product/reasoning 来源身份为空。这是两个不同输入的分层观察，不是同一输入的受控 A/B；文档有内容不等于产品已被识别
- 未测边界：未安装到用户宿主、未生成或渲染网站、未测真实用户任务/可用性/转换率，未调用付费模型；没有把有限检查升级为全功能正确

详细证据在六步实验结果、命令日志和练习包中。源文件运行前后指纹一致，旧学习项目的测试数量没有进入本轮计数。

## 8. 复用与合并建议

1. 先核对目标知识库的同义条目与已有编辑，再决定 BM25 等候选是否独立成篇
2. 设计令牌、规范文档、技能包与证据分层优先补充案例，不重复建立同义概念
3. 保留项目与概念的双向关联，明确哪一条证据支持哪一个结论
4. 一同保存固定源码版本、精确合成输入、完整命令、历史结果和审核范围
5. 不以索引未命中推断未读正文没有相关内容，也不以保存笔记替代实际掌握或产品验收

## 9. 本轮实际全文读取的公开知识来源

以下 24 篇均固定于 1043e9d6080bff7af9724162e2c44559fab63e40。这里只列可复核来源与指纹，不批量转载正文。

1. [AgentSkills技能包](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/AgentSkills%E6%8A%80%E8%83%BD%E5%8C%85.md)
   - UTF-8：1536 字节；SHA-256：bb055a1f106f721c5c71a3a2b359c16d11190fbc261c772d63a7bbc3782f011b；Git blob：3c99fde537d041344e59ab38d8e7180a066b59d7

2. [技能路由器与授权硬门](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%8A%80%E8%83%BD%E8%B7%AF%E7%94%B1%E5%99%A8%E4%B8%8E%E6%8E%88%E6%9D%83%E7%A1%AC%E9%97%A8.md)
   - UTF-8：2140 字节；SHA-256：8e122f9a4d1cb581bbc11303a0952f46b81b8d8251c938067e38db926f90ff4e；Git blob：25536eb2cee811c77b0c174e21a230294e552bc1

3. [DESIGN.md规范文档](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/DESIGN.md%E8%A7%84%E8%8C%83%E6%96%87%E6%A1%A3.md)
   - UTF-8：1446 字节；SHA-256：a6cd9ef692f0b1e3bc38641db9ab5bc78c4a897b8d53652a71fa121b5ee72e4b；Git blob：b85ae4b9d7be0bbe94cae6ba58df945ba818e30c

4. [设计令牌DesignToken](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%AE%BE%E8%AE%A1%E4%BB%A4%E7%89%8CDesignToken.md)
   - UTF-8：1236 字节；SHA-256：ab060471ced8e989239f2b3cea5515fbc2ecc7ea26f133e45b571214ef15f55d；Git blob：760e1938981abee674ceec431c48594b34600bb3

5. [awesome-design-md](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/awesome-design-md.md)
   - UTF-8：1947 字节；SHA-256：aac029cc22967244e2c24cecc8f10ee1dd7087dc308ee7a473070a05861e72c2；Git blob：adfb1193a65f69a0d8d1804b6d78dcd0dff2147c

6. [six_skills](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/six_skills.md)
   - UTF-8：3368 字节；SHA-256：04d4b2eb80d9fb1fb82e7c88ad465850045395f2d9112938d85b2d55e5670ecf；Git blob：933defbc740e2d17fff656c1546704d600996624

7. [RAG检索增强生成](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/RAG%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BA%E7%94%9F%E6%88%90.md)
   - UTF-8：1846 字节；SHA-256：d647bda0a1f1d95136313716a10ca07653d90366aa7fdfcb0678eb77be2393e1；Git blob：70adb54840b2ae314009084e346e66ff11941e58

8. [混合检索与RRF融合](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%B7%B7%E5%90%88%E6%A3%80%E7%B4%A2%E4%B8%8ERRF%E8%9E%8D%E5%90%88.md)
   - UTF-8：1739 字节；SHA-256：2cdad497ae76c834be48f7104df5fd3c605b57785b0ff955c9c3bf1d8ef2d58c；Git blob：89be05f727be50f5c115b8e002fe9f69d4762065

9. [图像提示八要素](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%9B%BE%E5%83%8F%E6%8F%90%E7%A4%BA%E5%85%AB%E8%A6%81%E7%B4%A0.md)
   - UTF-8：2408 字节；SHA-256：652f097bd319294e764558409bd2975d10fc4d94e251d9afe203eeb7e5bf12d1；Git blob：4a359182d0a58d14f7bc5ca3a2738bb2529e4428

10. [提示词模板](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%8F%90%E7%A4%BA%E8%AF%8D%E6%A8%A1%E6%9D%BF.md)
   - UTF-8：1147 字节；SHA-256：96f7b18a973e2f4d5fd2a86ea967011c6e12ced0ab50ce8029232bdf8098ea21；Git blob：7511ae54bfd05fa62c097687bd8d5f1ff12859fc

11. [修改与约束分离](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E4%BF%AE%E6%94%B9%E4%B8%8E%E7%BA%A6%E6%9D%9F%E5%88%86%E7%A6%BB.md)
   - UTF-8：2625 字节；SHA-256：e4fcd8e5b32997c473240296081e74f1923cfbfa87cb0a4e5da3e37ea46d6494；Git blob：0eee151eb1eedea66e8772a64548dc4b83d3d820

12. [角色一致性锚定](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%A7%92%E8%89%B2%E4%B8%80%E8%87%B4%E6%80%A7%E9%94%9A%E5%AE%9A.md)
   - UTF-8：1514 字节；SHA-256：72b2873b3439bbcda7855fa5209c6217aecb172ad6ce7acd0106fd9974fa7521；Git blob：1b48c49048df5db89eb94ea771904580e6bd77c4

13. [gpt_image_prompting](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/gpt_image_prompting.md)
   - UTF-8：5392 字节；SHA-256：ff9cd7c86487e45dc3467de0d55113c0a8285e48e9061c59f613b63e543edae6；Git blob：c63700aa0b232882ab5cf2592540ef3ea766b3fe

14. [awesome_gpt_image_2](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/awesome_gpt_image_2.md)
   - UTF-8：2242 字节；SHA-256：f1e72ebd4437ef406afc437f00742394b4ea8425010cb2f0b8680ee63340e452；Git blob：bd15db6b0783a1d4a00f572d84433ceb853697a5

15. [证据优先质检ProofOverClaims](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%AF%81%E6%8D%AE%E4%BC%98%E5%85%88%E8%B4%A8%E6%A3%80ProofOverClaims.md)
   - UTF-8：3593 字节；SHA-256：c54ea2f3bcfe830556942d04c502ba84472a7382c45b76dd07401861e44c2fac；Git blob：34acc9927d33b25c7177554ccecf898dee090d53

16. [证据状态机](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%AF%81%E6%8D%AE%E7%8A%B6%E6%80%81%E6%9C%BA.md)
   - UTF-8：2488 字节；SHA-256：4ac12b197891357591ebd092a9120bd67fa6fa1a09a407ed9c0fea3bc9b97328；Git blob：ac9073f0704c00fa5d3f97b797753de60785f9bf

17. [事实与判断分离](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E4%BA%8B%E5%AE%9E%E4%B8%8E%E5%88%A4%E6%96%AD%E5%88%86%E7%A6%BB.md)
   - UTF-8：1653 字节；SHA-256：53f5643580c0ab2e2860c6d2b25e3ea7eeb80cf806c1fdf4d989cab59319427b；Git blob：dbae8a2ec18840326d27617c25d4ad4481302628

18. [代码管边界提示词管判断](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E4%BB%A3%E7%A0%81%E7%AE%A1%E8%BE%B9%E7%95%8C%E6%8F%90%E7%A4%BA%E8%AF%8D%E7%AE%A1%E5%88%A4%E6%96%AD.md)
   - UTF-8：1427 字节；SHA-256：82baf8f30c908b3ea424d15f82b6d3124e40b3c1b023961bfd0c8abd1eb8b86d；Git blob：fc833147506c77d23ced4c6fff79e50fdab5347f

19. [agent-reach](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/agent-reach.md)
   - UTF-8：2831 字节；SHA-256：8e4b2ab724b77ccf948dd8e01b6d9274fa066639418cb38a79ccf2d37e13468f；Git blob：d6f97bb4f6fa5c1ad53599414064b6c0f06b8ee1

20. [archify](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/archify.md)
   - UTF-8：2504 字节；SHA-256：ef8bb1077867c603405823368668b8a7a5cf7072001f82b1553b2e7f41cb575c；Git blob：c17d5444f89dcb3846b6b79585659322da09c865

21. [开源验货三查](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%BC%80%E6%BA%90%E9%AA%8C%E8%B4%A7%E4%B8%89%E6%9F%A5.md)
   - UTF-8：1815 字节；SHA-256：836585db83f85f393815551357aad9b894567c5e57bc7c4623e088040c50b0ce；Git blob：c20d06f6c477b96a6f55cd6422102081debb40af

22. [产物留痕与状态外置](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E4%BA%A7%E7%89%A9%E7%95%99%E7%97%95%E4%B8%8E%E7%8A%B6%E6%80%81%E5%A4%96%E7%BD%AE.md)
   - UTF-8：2389 字节；SHA-256：6aba36f09afc580c08a669663e1ddaef6fa2c99067fcfedb65f56ba81a5ecceb；Git blob：cb5ec501b62bbfb0ca2def6e6b828041e240da36

23. [RAG架构谱系](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/RAG%E6%9E%B6%E6%9E%84%E8%B0%B1%E7%B3%BB.md)
   - UTF-8：1543 字节；SHA-256：786a39c72a7a802adb0825ff988c916aa8ba76e5325132fb32aecdd7dbfac603；Git blob：d9d077374eb6511b45174444891b3bf3285c8e4f

24. [AI味模式库与信号非证据](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/AI%E5%91%B3%E6%A8%A1%E5%BC%8F%E5%BA%93%E4%B8%8E%E4%BF%A1%E5%8F%B7%E9%9D%9E%E8%AF%81%E6%8D%AE.md)
   - UTF-8：2177 字节；SHA-256：294ec3ddd248e8db25c76f17c8747993b98a9a324f4a3b0502eb67c72bc352ef；Git blob：9d08df434163cc6128c2bfcc7c141177877260b2

## 10. 本轮项目机制来源

- [core.py：CSV 配置、分词与 BM25、搜索流程](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/477bcb28c9812b385cb51a4605ddf30d7b2266e2/src/ui-ux-pro-max/scripts/core.py)
- [design_system.py：类别规则、多域选择与设计系统组装](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/477bcb28c9812b385cb51a4605ddf30d7b2266e2/src/ui-ux-pro-max/scripts/design_system.py)
- [search.py：命令行参数与输出入口](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/477bcb28c9812b385cb51a4605ddf30d7b2266e2/src/ui-ux-pro-max/scripts/search.py)

这些链接支撑静态实现解释；实际分支覆盖、用例数与观察结果以本轮实验日志为准。固定版本的历史笔记只用来关联概念，不替本轮上游或实验背书。


## 11. 交付证据定位

首轮执行：2026-10-05 08:54:41.416153 至 08:54:47.438604 UTC，Python 3.12.14。完整命令与实测输出见实验日志和练习包 results。主要源代码、选定测试与数据共49文件，逐字节对应固定上游提交，保留MIT原文。

主例来源逻辑数据行（不含CSV表头）：products 1、ui-reasoning 1、styles 1、colors 1、typography 13、landing 1；实际物理行、原值和文件/行哈希见 design.json。不是所有组合或派生文本字段都逐个断言相等；本轮明确断言来源身份可唯一解析，以及每个样例20个颜色输出字段对应原值。
