# capcut-cli 知识入库提案（vault-note-proposal）

> 提案性质：供协调者查重合并用，worker 不直写 vault。
> 关联任务：fc6b3e7b-4b5c-44d1-b3f6-ea15458366ba ｜ 项目目录：F:\reminder\capcut_cli ｜ 实测 v0.31.1 (master@f3d6c75)

## 一、新概念笔记（建议新建，vault 查重未见同名）

### 1. 工程文件自动化（File-format Automation）
- 一句话定义：对没有 API 的 GUI 专业软件，直接逆向其工程文件格式 + 版本感知 schema + 原子写备份，把"只能人操作的软件"变成"可编程资源"——Agent 时代的通用集成路线。
- 领域：AI 工具生态 / Agent 集成
- 已有概念关联：[[JSON-IR类型化中间表示]]（工程文件即 IR）；[[Checkpoint存档与持久执行]]（.bak+restore 是其文件级实现）；[[能力地板选型]] 无关
- 来源项目：capcut-cli（剪映草稿 JSON 直接读写，实测建草稿/编辑/lint 全通）

### 2. 版本感知 schema 读写
- 一句话定义：读写第三方格式时先探测版本标记、按版本选 schema 规则、多时间线目标全部对齐——不承认单一文件是唯一真值（CapCut 8.7 mirror 修复）。
- 领域：软件工程 / 数据格式
- 已有概念关联：[[证据优先质检ProofOverClaims]]（读前先验契约）；[[快照契约与不可变只读]] 的写入侧镜像
- 来源项目：capcut-cli（version 命令实测：6.5.0 模板，schema 特性检测，支持 6.x–9.x）

## 二、项目笔记（建议新建 vault\项目笔记\capcut_cli.md）
- 项目是什么：renezander030/capcut-cli，966★，MIT，v0.31.1——非官方剪映草稿 CLI（Node≥18 零运行时依赖），"JSON in, JSON out"
- 带来的概念：[[工程文件自动化（File-format Automation）]]、[[版本感知 schema 读写]]
- 实验做了什么：无 CapCut/无 ffmpeg 环境，Python 自造 PNG+WAV → quickstart 建草稿（lint 0 警告）→ add-text 加文字轨道 → dry-run 预览 → .bak 机制验证
- 坑与结论：bin 入口是 dist/index.js；无 ffprobe 时图片用 5s 占位并明示；0.18.0 前有命令注入污点务必用新版；云字幕上传字节服务器须谨慎

## 三、合并建议（不新建，增补已有笔记）
- [[声明式视频源语言]] / [[分镜表驱动生成]]：增补"寄生在现有工业软件上的自动化层"对照路线
- [[质检Gate与自我纠错循环]]：增补 lint+doctor+dry-run 写盘前三重 Gate 实例
- [[Checkpoint存档与持久执行]]：增补 .bak+restore 文件级 checkpoint 实例

## 四、MOC 更新建议
"AI / 视频"分区增补两条新概念；项目索引加 capcut_cli。
