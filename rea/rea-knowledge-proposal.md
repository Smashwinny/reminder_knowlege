# REA 知识入库提案（vault-note-proposal）

> 提案性质：供协调者查重合并用，worker 不直写 vault。
> 关联任务：84e16939-fb85-42df-a274-f2627a983a2b ｜ 项目目录：F:\reminder\rea ｜ 实测版本 v6.8.0

## 一、新概念笔记（建议新建，vault 查重未见同名）

### 1. 三态证据框架（SEEN/INFERRED/UNKNOWN）
- 一句话定义：每条分析结论强制打三态之一——SEEN=工件里直接读到（附源码行列号+SHA-256）、INFERRED=从证据推导（血缘可追溯）、UNKNOWN=无法确定（如实记账不猜）。
- 领域：AI 工具生态 / 可信 AI
- 已有概念关联：[[证据优先质检ProofOverClaims]]（同一哲学的结构化强制执行版）；[[事实与判断分离]]（SEEN=事实、INFERRED=判断的机器可检版）
- 来源项目：rea（v6.8.0 实测：162 节点/105 关系伴 63 条 unknowns，limitations 明示"runtime registration unproven"）
- 可复用性：任何"AI 分析不可信输入"的管道都应套用此三态记账法

### 2. 逆向工程工具路由层
- 一句话定义：不重复造逆向引擎，只做"目标类型→有序引擎列表→第一个可用者当选"的路由 + 统一证据格式，让 M 个 Agent 经 MCP 用 N 个引擎只需 M+N 对接。
- 领域：AI 工具生态 / MCP
- 已有概念关联：[[能力层与后端路由]]（同构满配版）；[[M×N集成问题]]/[[MCP协议]]（收敛机制）；[[健康探测三态]]（doctor 命令的 17 项检查即其落地）
- 来源项目：rea

## 二、项目笔记（建议新建 vault\项目笔记\rea.md）
- 项目是什么：morluto/rea，395K★，MIT，"Reverse Engineer Anything"——逆向工程的 MCP 总调度台（v6.8.0，TypeScript，Node 22.23.4+/24.22.1+）
- 带来的概念：[[三态证据框架（SEEN/INFERRED/UNKNOWN）]]、[[逆向工程工具路由层]]
- 实验做了什么：自建带 3 谜题的 Electron 样本（隐藏快捷键/假验证后门/IPC 通道），REA 免引擎静态分析全部命中（带行列号），63 unknowns 如实记账；踩 2 坑（Node 补丁版本需 --force；git 源码不带 Windows 原生控件需从 npm tarball 恢复）
- 坑与结论：build:cached 不编译 TS 需 compile；JS/Electron 分析是零外部依赖入门路径

## 三、合并建议（不新建，增补已有笔记）
- [[能力层与后端路由]]：增补 REA 作为"路由层+证据层"组合的战例
- [[证据优先质检ProofOverClaims]]：增补 REA 三态框架作为"证据带状态标签"的范式引用
- agent-reach / artemis 项目笔记：与 REA 在安卓分析域互链（同域项目关联）

## 四、MOC 更新建议
在"领域：AI 工具生态"区增补：[[逆向工程工具路由层]]、[[三态证据框架（SEEN/INFERRED/UNKNOWN）]] 两条；项目索引加 rea。
