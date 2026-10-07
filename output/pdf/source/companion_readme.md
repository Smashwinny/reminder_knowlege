# 拾遗到知识网络：可编辑讲解与命令包

本包与 36 页 PDF 配套。状态核验基线为 **2026-10-05 14:07，Asia/Shanghai**。架构、完成记录与待打通事项均是当时快照。以下新手安装、部署及登录命令没有替读者在真实环境运行；每步都需要看实际结果再继续。

## 阅读与演示

1. 打开 `workflow_guide.html`，浏览器可阅读 36 页彩色矢量讲解；打印选择 A4、横向、100% 比例。
2. 打开同名 `.md` 获取讲解、Dot 启动和复习指令以及可复制终端命令。
3. `diagrams/page_04.svg` 是总架构图；其他 SVG 对应逐页内容，可导入演示软件编辑。
4. `逐终端补充命令.md` 补全首次配置、入口、权限、回执和 Git 的具体步骤。
5. `模板/` 给出概念、项目和每日复习的 Obsidian 样例，以及 manifest / receipt 结构；样例不是合格证据。
6. `本机工具补齐/README.md` 说明本机工具如何安装、哪些文件允许复制。

## 快速向伙伴讲清楚

- 手机负责“收集与本人选择”；阿里云保存正式数据并限制权限。
- Dot 在自己的云端电脑读取核实过的链接，按 learn-project 做疑问、讲解、实验、彩色指南与独立审核。Skill 是作业方法，需要实际工具执行。
- 网站保存私有报告和六类原件；“分析完成”标签和用户任务勾选独立。
- Windows 开机后只自动拉取并校验私有副本；唯一协调者合并 Obsidian 知识网、内容审核并推送学习成果到公开 Git。
- 每日复习应先让本人闭卷回答，再反馈与确认评分；完整的复习写回模板仍需实施验收。

## 当前边界

15 分钟日程已派发固定旧批次，不等于今后全部新记录已经自动派发；本机登录触发不等于模型自动审核和 Git；原生 Dot 唤醒本机既有聊天的路由未验收。链接保存不等于已读取 X 原帖或抖音视频。本机文件与 Dot 云端文件系统相互独立。用户账号、列表与 OAuth 必须由本人配置，不随本包复用。

## 本包版本与隐私

公开知识索引固定于 `109ffa9763c24f6ff05d2b7f1b1d9ed14e7d79e0`。本机集成工具依据当前工作区白名单快照，基准提交 `8536dae002ebf87c6864dfeeae3b2ee6df41e0b6` 当时尚未推送。每份分发文件的 SHA256 列在 `package_manifest.json`。

本包不包含私有网站源码、原任务正文、分类报告、队列数据库、token、.env、服务器 SSH 信息、浏览器状态或 Git 历史。网页公开域名和已发布知识链接保留。配套 `.claude/skills/learn-project/SKILL.md` 是原方法；发生冲突时以当前 `AGENTS.md` 为准：worker 不操作 Git，唯一协调者使用明确文件清单，禁止全仓 add 和共享工作区自动 rebase。

复制方法文件到 Dot 不是安装本机 skills，也不授予电脑权限。Dot 应实际读取方法与固定版本知识，取得限定 MCP 权限后按方法执行；不能只输出“已读 skill”。

## 重建讲解

`讲解源码/` 保存 ReportLab 构建器和渲染检查器。需要 Python、reportlab、pypdf、Pillow、pdftoppm，以及构建器指定的中文字体；新环境先改路径和字体。当前 PDF 用 ReportLab 矢量生成，HTML 是同步可编辑版，没有将受阻的云端 HTML→PDF 计为成功。

## 官方依据

- [Dot 的电脑和应用](https://learn.chatgpt.com/docs/dots/computers-and-apps)
- [Dot 的任务和日程](https://learn.chatgpt.com/docs/dots/tasks-and-memory)
- [MCP / OAuth](https://developers.openai.com/plugins/build/auth)
- [Obsidian 内部链接](https://help.obsidian.md/links)、[图谱](https://help.obsidian.md/plugins/graph)
- [Docker Ubuntu 安装](https://docs.docker.com/engine/install/ubuntu/)
- [WinGet 安装](https://learn.microsoft.com/en-us/windows/package-manager/winget/install)
- [Cloudflare Tunnel 下载](https://developers.cloudflare.com/tunnel/downloads/)、[运行参数](https://developers.cloudflare.com/tunnel/reference/run-parameters/)
- [主动回忆原研究](https://pubmed.ncbi.nlm.nih.gov/16507066/)
