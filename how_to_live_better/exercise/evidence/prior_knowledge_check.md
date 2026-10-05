# HowToLiveBetter：已发布知识关联核对

核对日期：2026-10-05 UTC。本文是本次学习的证据记录和入库提案，不是用户掌握程度测试，也不是最新本机知识库快照。

## 1. 实际范围

- 索引仓库：Smashwinny/reminder_knowlege
- 索引提交：`1f61909da967cea8bc68dbfaffc642a4331b3352`
- 索引文件：`reminder-dot/cloud-reference/knowledge-index.json`
- 笔记源提交：`1043e9d6080bff7af9724162e2c44559fab63e40`
- 索引共 394 条。对全部标题/路径元数据检索了“事实、判断、证据、拒答、置信、不确定、审计、因果”；再对“风险、决策、收益、成本、相关、统计、贝叶斯、抽样、选择性、校准”作标题级补充检索
- 精读正文限下列 5 篇，逐篇读完。每篇 SHA-256 与字节数均匹配固定索引；原文副本、URL、Git blob SHA、实际校验值见 `read_manifest.json` 与 `originals/`
- 未做全库正文扫描，没有读取 Windows 当前工作树、未提交 vault、私密记录或本机 Obsidian 配置。索引自身明确 `publishedSnapshotOnly=true`、`workingTreeIncluded=false`、`privateRecordsIncluded=false`
- 根据协调者 2026-10-05 03:31Z 实际 Reminder 回读：`totalNotes=0`、`totalChunks=0`、`items=[]`、`nextCursor=null`，snapshot `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`。本核对者没有重复该调用；这仅表示当时获准网站列表下完整分页的 knowledge_notes 为空，不表示本机知识库为空
- 本报告只对五篇实际精读笔记作“已有依据”判断。“公开笔记中已有记录”不等于“用户已经掌握”

[固定索引](https://github.com/Smashwinny/reminder_knowlege/blob/1f61909da967cea8bc68dbfaffc642a4331b3352/reminder-dot/cloud-reference/knowledge-index.json)

## 2. 实际读到的旧概念与本次迁移

### 2.1 事实与判断分离

原笔记核心：数字事实由确定性代码计算，LLM 负责事实之上的综合解释；不能把原始数字扔给模型后让它凭空“心算”。

本次可迁移：原文条目、成本标签、研究类型和提取到的数字是输入；计算规则可复现；“哪件事更值得”仍是作者或使用者的价值判断。自动算出了某档，并不会让该档变成科学事实。

[原笔记](https://github.com/Smashwinny/reminder_knowlege/blob/1043e9d6080bff7af9724162e2c44559fab63e40/vault/概念/事实与判断分离.md)

SHA-256：`53f5643580c0ab2e2860c6d2b25e3ea7eeb80cf806c1fdf4d989cab59319427b`

### 2.2 证据状态机

原笔记核心：把事件类型 kind 与说法状态 state 分开，区分 announced / reported / unconfirmed / information，只有规定的状态允许驱动下游动作；不能把预告显示成已经发生，也不能把“查不了”显示成“查无”。

本次可迁移：必须分开“仓库原文如此记载”“本次已核验原始来源”“适用条件尚未确认”。这只是状态分离原则的迁移，不应照搬原来的公告枚举为医学证据等级，也不能把 A/B/C 当作采集是否成功的状态。

原笔记的一处精确性提醒：它先列四种 state，后文又使用 confirmed 作为动作准入词，未在该笔记完整定义这项枚举；本次不据此实现或声称已验证其原项目状态机。

[原笔记](https://github.com/Smashwinny/reminder_knowlege/blob/1043e9d6080bff7af9724162e2c44559fab63e40/vault/概念/证据状态机.md)

SHA-256：`4ac12b197891357591ebd092a9120bd67fa6fa1a09a407ed9c0fea3bc9b97328`

### 2.3 置信度门控与弃权

原笔记核心：低于阈值时停止自动作答并升级给人；代价是降低覆盖率。原笔记特别警告，门控只有在置信度校准可靠时才可能提高准确率，它记录的一次本机小测试里筛选后准确率反而更低。

本次可迁移：适用人群、禁忌、政策有效日期或来源未确认时，应保留待核验，不硬下个人结论。“A 级证据”不是经过校准的个人获益概率，“性价比高”也不是适用性保证。本次建议的是检查条件的准入规则，并未训练概率模型、拟合阈值或验证置信度校准。

[原笔记](https://github.com/Smashwinny/reminder_knowlege/blob/1043e9d6080bff7af9724162e2c44559fab63e40/vault/概念/置信度门控与弃权.md)

SHA-256：`33584b31890cf4ba595adf9715548089b637eb19cc02ba31af5b59f1acd05e03`

### 2.4 证据优先质检 ProofOverClaims

原笔记核心：编译成功不能替代运行结果；需要实际截图、录像或日志，并给证据加可定位的帧、版本、SHA-256 与口径。它还强调自己的文档也要核验，缺数据不凑数。

本次可迁移：指南是否可读要看实际 PDF 渲染；实验是否执行要看命令日志与断言；引用是否来自同一版本要看提交和哈希。它们验证的是交付与可追溯性，并不能替代对所有原始医学/法律文献的独立验证。

[原笔记](https://github.com/Smashwinny/reminder_knowlege/blob/1043e9d6080bff7af9724162e2c44559fab63e40/vault/概念/证据优先质检ProofOverClaims.md)

SHA-256：`c54ea2f3bcfe830556942d04c502ba84472a7382c45b76dd07401861e44c2fac`

### 2.5 AI 味模式库与信号非证据

原笔记核心：文本模式只是线索，受语境和误报影响，不足以单独作为高后果判断的依据。

本次可迁移：项目热度、排版、引用数量或一个看似精确的评分，都只能引导进一步检查；不能替代原始来源、研究设计、适用人群及边界。此处是跨场景类比，不宣称该笔记已经验证 HowToLiveBetter。

[原笔记](https://github.com/Smashwinny/reminder_knowlege/blob/1043e9d6080bff7af9724162e2c44559fab63e40/vault/概念/AI味模式库与信号非证据.md)

SHA-256：`294ec3ddd248e8db25c76f17c8747993b98a9a324f4a3b0502eb67c72bc352ef`

## 3. HowToLiveBetter 在该范围内增加什么

依据本次实际读取的 HowToLiveBetter `README.md` 第 1–90、168–236 行，以及完整 `skills/life-decision-guide/SKILL.md`；上游提交固定为 `bc149af3a02e721f0e3d03a673a0ec64fca765c4`。这里只复述项目方法论，不给个人医疗、法律或投资结论。

1. **证据等级与性价比双轴**：README 明确把 A/B/C 与极高/高/一般分开，后者是作者自己的判断、按本书口径只算 C 级。可计算的排序不是客观的价值排序
2. **A 级不等于因果已证实**：项目 A 级既可包含随机试验，也可包含只观察不分组的研究；政策法律类 A 级则指向原文。必须读研究类型和条目备注，不能只看字母
3. **相对风险与绝对风险**：同一个相对降幅在不同基线风险下有不同绝对差值。只知道“降低百分之几”不足以推出某个人能获益多少
4. **收益口径不可直接通约**：寿命、金钱、时间精力、人身自由分别看，不把所有收益强塞进一个排行榜
5. **把适用条件留在条目里**：仓库 skill 要求读完整条目和备注，保留人群、年份、争议及待核验项；政策金额与时限要带日期。阅读入口很有用，但不保证对个体处境适用

[README 证据分级与性价比](https://github.com/eternity4719/HowToLiveBetter/blob/bc149af3a02e721f0e3d03a673a0ec64fca765c4/README.md#L172-L200)

[README 风险数字说明](https://github.com/eternity4719/HowToLiveBetter/blob/bc149af3a02e721f0e3d03a673a0ec64fca765c4/README.md#L184-L186)

[仓库使用方法](https://github.com/eternity4719/HowToLiveBetter/blob/bc149af3a02e721f0e3d03a673a0ec64fca765c4/skills/life-decision-guide/SKILL.md)

## 4. 入库处理提案（待本机查重）

- 事实与判断分离、证据状态机、置信度门控与弃权：已有公开同名笔记，不新建同义副本；建议追加本项目关联段和反向链接，保留其原领域与含义
- 证据优先质检、信号非证据：引用旧条目即可，本项目只增加应用案例
- “证据等级与性价比双轴”“相对风险与绝对风险”“收益口径不可直接通约”：可作为新概念候选，分别关联上述旧概念。本次仅在选定的五篇正文中未见相同完整论述；不能据此声称全库没有。先在 Windows 当前 vault 按别名、全文和相关项目笔记查重，再决定新建、合并或双向关联
- 项目笔记应记录此次实际实验能证明什么、不能证明什么，并区分数据提取正确、算法复现正确、原始研究真实可靠、对个人适用这四个不同问题
- 这里没有执行本机回迁、vault 合并、任务完成、Git 提交或推送；这些状态不能由本报告代替

## 5. 可重复核查

`read_manifest.json` 保存索引哈希、每篇固定路径/URL、预期与实际 SHA-256、字节数、Git blob SHA 和精读范围。可用以下命令验证本地五份副本仍与清单一致：

```bash
python knowledge_reference/verify_reference.py
```

同一输入、同一 SHA-256 只确认本文使用了同一份字节；不代表其中每项历史实验或外部文献已经重新验证。旧笔记中的项目测试数字在本次未重跑，也未当作本次实验结果使用。
