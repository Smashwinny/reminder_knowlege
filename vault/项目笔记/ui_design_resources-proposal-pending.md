# UI 设计四资源 知识入库提案（vault-note-proposal）

> 提案性质：供协调者查重合并用，worker 不直写 vault。
> 关联任务：b7a65371-8ba1-44a0-9f05-d0c1a728061f ｜ 项目目录：F:\reminder\ui_design_resources

## 一、新概念笔记（建议新建，vault 查重未见同名）

### 1. AI 味确定性规则检测
- 一句话定义：把"AI 生成 UI 的套路"编译成免 LLM 的确定性规则（字体/色相范围/对比度公式/结构模式），输出命中清单+修复指令，exit 非零即 fail-closed——审美问题机检化。
- 领域：AI 原生开发 / 设计系统
- 已有概念关联：[[AI味模式库与信号非证据]] 的 UI 孪生；[[设计令牌DesignToken]]（审美变数字）；[[证据优先质检ProofOverClaims]]
- 来源项目：ui_design_resources（impeccable 62 规则源码核实 + 自写迷你检测器 6/6 命中）

### 2. 产品事实与视觉方向分离
- 一句话定义：PRODUCT.md 存稳定层（受众/目的/红线，带 schema 版本注释），DESIGN.md 存易变层（本轮视觉方向），分文件防"改配色污染定位"。
- 领域：AI 原生开发 / 设计系统
- 已有概念关联：[[DESIGN.md规范文档]]（其纪律层）；[[事实与判断分离]]；[[快照契约与不可变只读]] 的版本注释同族
- 来源项目：ui_design_resources（impeccable 自家 PRODUCT.md 实测带 product-schema 1 注释）

## 二、项目笔记（建议新建 vault\项目笔记\ui_design_resources.md）
- 项目是什么：X 文推荐的四资源组合——getdesign.md（规范）/ libraries.dev（组件）/ pbakaus/impeccable（审查，1 skill 24 命令 62 规则）/ nexu-io/open-design（工作流）
- 带来的概念：[[AI味确定性规则检测]]、[[产品事实与视觉方向分离]]
- 实验做了什么：impeccable 源码静态核实（规则 ID 真实、PRODUCT.md schema 注释）、自写迷你检测器对示例页 6/6 命中（含 WCAG 2.85:1 实算）
- 坑与结论：引擎需构建/下载（本班构建被拒）；四资源应逐个引入做对照而非同时装

## 三、合并建议（不新建，增补已有笔记）
- [[DESIGN.md规范文档]]：增补 PRODUCT.md/DESIGN.md 分离与 schema 版本机制
- [[AI味模式库与信号非证据]]：增补 UI 域孪生概念
- [[质检Gate与自我纠错循环]]：增补 detect→命中清单→修复指令闭环

## 四、MOC 更新建议
"AI 原生 UI / 设计系统"分区增补两条新概念；项目索引加 ui_design_resources。
