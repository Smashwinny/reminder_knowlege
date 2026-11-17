# 浏览器安全工具清单 知识入库提案（vault-note-proposal）

> 提案性质：供协调者查重合并用，worker 不直写 vault。
> 关联任务：f9051c75-4321-4ba6-b914-9bac6dad9a20 ｜ 项目目录：F:\reminder\browser_security_tools
> 性质：防御性学习，不含任何攻击操作。

## 一、新概念笔记（建议新建，vault 查重未见同名）

### 1. 采集分级防御法
- 一句话定义：把"网页能拿到什么"分三级——被动指纹（无授权：UA/硬件/屏幕）、敏感权限（必授权：定位/摄像头/麦克风）、主动输入（钓鱼骗输）；三级防御策略不同，宣称拆解用"数据类别+授权路径+证据"三问。
- 领域：安全 / 浏览器隐私
- 已有概念关联：[[提示注入]]（钓鱼是对人的提示注入）；[[本地MCP端点安全四道门]]（最小授权同族）；[[证据优先质检ProofOverClaims]]（摄像头证据=硬件灯）
- 来源项目：browser_security_tools（Seeker 源码 @7bf501a 核对 + 权限页实测）

### 2. 浏览器权限状态机
- 一句话定义：每个敏感 API 走三态 prompt→granted/denied，默认 prompt；拒绝即 error 回调拿不到数据；仅安全上下文（HTTPS/localhost，Edge 的 file:// 也算）可用。
- 领域：安全 / Web 平台
- 已有概念关联：[[护栏模式Guardrails]]（平台级护栏）；[[采集分级防御法]] 的权限层
- 来源项目：browser_security_tools（实测：prompt 状态、PERMISSION_DENIED code=1）

## 二、项目笔记（建议新建 vault\项目笔记\browser_security_tools.md）
- 项目是什么：X 帖所列 5 个"开源安全工具"（Storm-Breaker/Seeker/Zphisher/HackingTool/SayCheese）的防御视角解读
- 带来的概念：[[采集分级防御法]]、[[浏览器权限状态机]]
- 实验做了什么：Seeker 源码静态核对（被动指纹 POST + geolocation 授权分支）、自建权限测试页 headless 实测（prompt→denied→code=1）
- 坑与结论：SayCheese 无仓库地址身份未核实；"点链接即定位"为夸大宣称；Edge file:// 也算安全上下文

## 三、合并建议（不新建，增补已有笔记）
- [[提示注入]]：增补"钓鱼=对人的提示注入"视角
- [[文档渲染与XSS净化]]：增补"权限请求白名单思维"
- [[证据优先质检ProofOverClaims]]：增补"硬件指示灯是可验证据"

## 四、MOC 更新建议
"数据采集 / 可信追踪"或新建"安全 / 浏览器隐私"分区增补两条概念；项目索引加 browser_security_tools。
