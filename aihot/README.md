# AIHOT 学习成果 / GeniusQI 应用

日期：2026-10-03。按用户指定 `learn-project` skill 执行；研究与离线验证，不是线上发布。

## 成果

- `AIHOT-小白指南与网站应用.pdf`：13 页彩色图文，12 个新问题、能力清单、6 步主实验、项目分轨和 Three.js 建议。
- `aihot_guide.html`：指南 HTML 源；不联网也可读。
- `learning_lab.html`：互动学习材料，过滤公开项目轨道与观察真实缓存用例输出；不是正式站点。
- `exercise/`：自建实验。`output/` 保存结果和资产审计。无真实私有源、凭据、API Key。
- `build_guide.py` / `render_pdf.py`：可重复生成 HTML 与 PDF。

## 固定输入

上游源码：`KKKKhazix/AIHOT`，commit `3343fe2b20db4be7269113752d82d3992fc52b6b`。

网站本地版本：`Smashwinny/my_website`，HEAD `4ce04f8d47dc810c51aac8175b8133dab85e9826`，2026-10-03 检查时工作区干净。未推断其他设备的状态。

## 验证记录

1. Node v24.19.0 已可用；实验零外部依赖，不安装完整 AIHOT 依赖。生成文档的 Python 使用进程级 PYTHONUTF8=1。
2. 原版架构测试 3/5，通过路径兼容实验夹具后 5/5。两项误报来自 Windows `\\` 与 POSIX `/` 比较；未修改上游文件。
3. `lab.mjs`：6 个真实上游缓存函数用例 + 5 个自建公开快照断言，共 11 个通过。纯函数通过 Node stripTypeScriptTypes + vm 隔离运行，源函数 SHA-256 固定在输出中。
4. 快照候选 7 个：6 个 Fork 学习/改造，1 个非 Fork 个人实现候选（街区猫王）。非 Fork 不等于所有玩法/素材原创，Demo 均未验证。
5. 当前 4 个 web/lite VRM 的 gzip 解压后与原文件逐字节一致；统计了文件字节、图片数量与假设 4Mbps 的理想传输时间。理想传输不是浏览器速度，不用它宣称提速。
6. 由于 Edge 无头打印在当前环境没有生成 PDF，按本机 PDF 工具退路使用 ReportLab + 微软雅黑生成；保留 HTML，Poppler 渲染 13 页并检查。没有用一个空 PDF 交付。
7. 互动 HTML 在 VM 的最小 DOM 单元夹具中检查全部/个人实现/改造数量、选中状态与 no-cache 输出，5/5 通过。这不是浏览器验证：应用内浏览器连接本机预览超时，未声称完成实机点击和手机视觉验收。

未运行：完整数据库/采集/付费模型/新闻后台；街区猫王实机；新性能 A/B；生产构建与部署。本次不能说“全站已跑通”或“网站又提速了”。

## 最小复跑（PowerShell）

```powershell
$node = 'C:\Users\Windows\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe'
Set-Location -LiteralPath 'F:\reminder\aihot'
& $node .\exercise\architecture-windows.mjs
& $node .\exercise\lab.mjs
Get-Content -LiteralPath .\exercise\output\public-projects.json
& $node .\exercise\audit-website.mjs
```

上游 `repo/` 放在 F 盘且不提交。其他设备可用 Node>=24.11 并给脚本传入本机仓库路径。脚本只读上游与网站源码，生成自己的实验输出。

## 对网站的明确建议

内容：统一公开项目契约，区分个人实现 / 上游学习 / 有证据的二次改造；先接可试玩的街区猫王与学习指南。摘要、日志在后台或构建期生成并审核，公开访客不临时请求 GitHub 或付费模型。

性能：已有 Three.js、按世界 lazy import、gzip 与字节缓存。下一轮先拆 click-to-controllable：JS、下载、解压、VRM 解析、地形碰撞、贴图上传、编译、首帧与输入。KTX2、Meshopt 与 compileAsync 只是候选；每项保持材质/骨骼/玩法回归，同期交替 A/B 各至少 10 次，再决定是否保留和上线。

F:\reminder 的其他任务未提交文件不在本次同步范围；不得因调用学习 skill 就打包提交它们。正式站点、DNS/CDN 与私有仓库权限都未改。
