# HowToLiveBetter 知识笔记与入库提案

日期：2026-10-05 UTC。项目固定版本：bc149af3a02e721f0e3d03a673a0ec64fca765c4

学习范围：证据组织、引用追踪、作者判断隔离；只读检索第4节3/6/7条。不是健康、法律、金融的个人建议，也没有对用户进行行为干预。

## 已读依据与查重边界

已检索公开知识索引394条元数据，全文读取并核对以下5篇已发布笔记的SHA-256。索引版本为 1f61909da967cea8bc68dbfaffc642a4331b3352，正文固定在 1043e9d6080bff7af9724162e2c44559fab63e40。获准列表的既有 knowledge_notes 在本轮完整分页快照中为空。没有读取本机最新 vault 或私密未提交笔记；笔记存在不等于用户已掌握。

## 五篇旧笔记如何关联

### 事实与判断分离

已有概念强调确定性代码计算、模型解释。本次沿用事实与判断分开存储的纪律，补充“来源存在”与“断言已验证”也必须分开；不是重复建立同名概念。

来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E4%BA%8B%E5%AE%9E%E4%B8%8E%E5%88%A4%E6%96%AD%E5%88%86%E7%A6%BB.md

SHA-256：53f5643580c0ab2e2860c6d2b25e3ea7eeb80cf806c1fdf4d989cab59319427b

### 证据状态机

已有概念区分公告/自称完成/未确认/资讯。本次借用状态分离思想，记录仓库转述、摘要可见、全文未读、适用性未知；这是类比，不能把这些状态与A/B/C等同。

来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%AF%81%E6%8D%AE%E7%8A%B6%E6%80%81%E6%9C%BA.md

SHA-256：4ac12b197891357591ebd092a9120bd67fa6fa1a09a407ed9c0fea3bc9b97328

### 置信度门控与弃权

已有概念还警告置信度需校准。本次用非数值门控：没读到比例就不输出比例。不可把A等级或任何作者评分解释为个人成功概率。

来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E7%BD%AE%E4%BF%A1%E5%BA%A6%E9%97%A8%E6%8E%A7%E4%B8%8E%E5%BC%83%E6%9D%83.md

SHA-256：33584b31890cf4ba595adf9715548089b637eb19cc02ba31af5b59f1acd05e03

### 证据优先质检ProofOverClaims

已有概念重视实际运行和视觉证据。本次补充实验真实日志、固定输入指纹、逐页PDF渲染及不同执行者审核；不把生成成功当作质量通过。

来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%AF%81%E6%8D%AE%E4%BC%98%E5%85%88%E8%B4%A8%E6%A3%80ProofOverClaims.md

SHA-256：c54ea2f3bcfe830556942d04c502ba84472a7382c45b76dd07401861e44c2fac

### AI味模式库与信号非证据

已有概念强调信号不是证据。本次把漂亮界面、星标数、来源数量视为继续检查的线索，不作为研究正确的证明。

来源：https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/AI%E5%91%B3%E6%A8%A1%E5%BC%8F%E5%BA%93%E4%B8%8E%E4%BF%A1%E5%8F%B7%E9%9D%9E%E8%AF%81%E6%8D%AE.md

SHA-256：294ec3ddd248e8db25c76f17c8747993b98a9a324f4a3b0502eb67c72bc352ef

## 建议新增或补充的概念

### 证据等级与性价比双轴

定义：研究来源的证据标签和基于成本收益的取舍排序是独立信息。领域：证据阅读与知识管理。关联：[[事实与判断分离]]、[[证据状态机]]。仓库明确性价比档是作者判断；本提案只在5篇已读笔记范围内判断新增价值，待本机全面查重。

### 可读层级与来源追踪

定义：把引用定位、元数据、摘要、全文、适用性分别记录，不用“有链接”覆盖后续层级。领域：信息检索与证据管理。关联：[[证据状态机]]、[[置信度门控与弃权]]。这是本次方法综合，不冒充仓库自带术语。

### 固定版本中的跨文件时间漂移

定义：即使整个仓库固定在同一提交，正文与核实记录也可能各自保留不同更新时间的判断。领域：数据溯源。关联：[[证据优先质检ProofOverClaims]]。真实例子：§4.3当前备注包含4.11，旧核实记录仍说未确认。结论只能是更新依据未调和，不是数值已被证伪。

## 项目实验结论

主实验实际读取3个真实源文件，解析第4节18个条目，深查3个条目及6个DOI。11类校验通过；未知百分比输出null；缺条目/缺来源弃权；内存损坏对照被拒绝；输入前后字节哈希一致。实验完整命令和输出见04-experiment-log.txt，代码与快照见03-exercises.zip。

初次运行发现收益栏混有作者算账表述，修订后拆成独立author_accounting_assumption；日志保留这次修正，不能只看首次输出。

本脚本不联网验证论文。外源补充只读到搜索可见的出版方/官方索引摘要和元数据；直接开页受限，全文未读。仓库作者核实记录的既往访问不能算作本次访问。

## 回迁提案与尚未完成

将上述三项先与现有概念查重，同义内容合并，相关内容互链；再加入项目索引。本次不修改本机vault，不执行提交或推送，不代用户点击任务完成。Windows回迁、入库合并及最终同步仍待协调者核对。

## 版本与归属

项目：https://github.com/eternity4719/HowToLiveBetter/tree/bc149af3a02e721f0e3d03a673a0ec64fca765c4

原学习方法：Smashwinny/reminder_knowlege@1043e9d6080bff7af9724162e2c44559fab63e40 的 .claude/skills/learn-project/SKILL.md 已实际读取。云端规则：同库@1f61909da967cea8bc68dbfaffc642a4331b3352 的 reminder-dot/cloud-reference/RUNNING_IN_DOT.md 已实际读取。本次按明确授权以ReportLab直接出PDF，未执行其中本机Git操作。

正文摘录/改编来自《高性价比人生指南》，作者 albert4719 / eternity4719：https://github.com/eternity4719/HowToLiveBetter。许可 CC BY 4.0：https://creativecommons.org/licenses/by/4.0/ 。本学习材料重新组织、解释并加入自建实验，已作改编。
