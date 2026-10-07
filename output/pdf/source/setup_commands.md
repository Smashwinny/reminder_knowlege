# 逐终端补充命令

这些是供新手执行的手册，**本次没有运行其中的真实登录、生产部署或 Git 推送**。Bash 在 Ubuntu / 阿里云执行；PowerShell 在 Windows 执行。将 `YOUR_DOMAIN`、`ADMIN`、`ECS_HOST`、`TASK`、`PROJECT`、`ORIGINAL_OWNER` 和审核者替换为自己的真实值。尖括号占位值不是合法回执。先看每步结果，再进入下一步。

## 1 · 手机 / 网页：先验证同账号同步

从 X 或抖音的分享菜单复制链接，粘贴到拾遗记录框保存。Android 在“账号与同步”检查同步服务地址和本人账户；自建实例用自己的 HTTPS 域名。网页在同一服务、同一账号登录后，应看到同一条任务。源码当前是粘贴识别，不声称 Android 系统分享已直接调用 ACTION_SEND。

X 登录墙、抖音视频壳和短链接必须记录实际可读程度。正文或字幕不可访问时保存“证据不足”及候选来源；仅有搜索命中不能把不同项目强行绑定。先用一个公开仓库链接联调，再扩展视频材料。

## 2 · Ubuntu 本地：取得代码与运维连接

PDF 第 19 页给出 clone、测试和 SSH 命令。网站仓库是私有仓库，需要拥有者授权。首次测试至少运行：

```bash
cd reminder
node --version
node --test sync-server/server.test.js
node --test sync-server/dot-integration.test.js
git status --short
ssh -i /PRIVATE/PATH/key ADMIN@ECS_HOST
```

Node 版本与当前 Dockerfile 的 Node 22 核对。SSH 成功后的命令运行于阿里云，不能再按 Ubuntu 本地路径理解。已有源码改动先保留并核对，不 reset；部署版本由唯一运维者确定。

全新 Ubuntu 缺少基础工具时，先安装：

```bash
sudo apt update
sudo apt install -y git openssh-client python3
```

没有 Node 的 Ubuntu 可按 PDF 第 20 页官方步骤在这台机器安装 Docker，然后用与项目一致的 Node 22 容器运行离线测试：

```bash
cd reminder
sudo docker run --rm --network none --read-only --tmpfs /tmp -v "$PWD:/app:ro" -w /app node:22-alpine node --test sync-server/server.test.js
sudo docker run --rm --network none --read-only --tmpfs /tmp -v "$PWD:/app:ro" -w /app node:22-alpine node --test sync-server/dot-integration.test.js
```

只挂载源码只读，测试临时文件放容器 /tmp。首次镜像拉取需要联网；容器测试阶段不连接生产服务。

## 3 · 阿里云：普通站点、密钥与入口

先按 PDF 第 20–21 页准备 Docker 和新站点。`.env` 中邀请码、Dot 的四项配置由本人私密填写；Kimi 摘要可选。容器以独立用户运行，宿主机 Key 文件仅 chmod 600 可能导致它无权读取。如启用 Kimi，先构建镜像，再按真实容器 UID / GID 赋予 **这一份 Key 文件**读取权限：

```bash
cd /opt/reminder
sudo docker compose -f deploy/docker-compose.yml build app
reminder_uid=$(sudo docker run --rm --entrypoint id reminder-sync:local -u)
reminder_gid=$(sudo docker run --rm --entrypoint id reminder-sync:local -g)
sudo nano deploy/kimi.key
sudo chown "$reminder_uid:$reminder_gid" deploy/kimi.key
sudo chmod 600 deploy/kimi.key
sudo docker compose -f deploy/docker-compose.yml up -d
sudo docker compose -f deploy/docker-compose.yml ps
curl -fsS http://127.0.0.1:8787/api/healthz
```

不要 chmod 644 把 Key 变成所有本机用户可读。已有服务的 .env 或 token 不复制给朋友。摘要 Key 不提供 Dot 本人 OAuth 权限。

### Cloudflare 入口示例：全新 Linux amd64 机器

参考 [官方下载](https://developers.cloudflare.com/tunnel/downloads/) 和 [运行参数](https://developers.cloudflare.com/tunnel/reference/run-parameters/)。先在本人 Cloudflare 控制台创建命名隧道和公开主机名，服务 URL 指向 `http://127.0.0.1:8787`。私密保存该隧道 token，不把包含 token 的安装命令发到聊天或 Issue。

以下采用官方二进制加本项目 service，使用专用系统用户及 `/etc` 的私密 token；这样无需向 nobody 开放整个项目目录。已有入口无需重复配置。

```bash
uname -m
# 仅 x86_64 使用下面的 amd64 下载；其他架构先按官方下载表替换
curl -fL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /tmp/reminder-cloudflared
sudo install -m 0755 /tmp/reminder-cloudflared /usr/local/bin/cloudflared
/usr/local/bin/cloudflared --version
sudo adduser --system --group --no-create-home reminder-tunnel
sudo install -d -m 0750 -o root -g reminder-tunnel /etc/reminder-tunnel
sudo install -m 0600 -o root -g root /dev/null /etc/reminder-tunnel/token
sudo nano /etc/reminder-tunnel/token
sudo chown root:reminder-tunnel /etc/reminder-tunnel/token
sudo chmod 0640 /etc/reminder-tunnel/token
cd /opt/reminder
sudo cp deploy/reminder-tunnel.service /etc/systemd/system/
sudo install -d /etc/systemd/system/reminder-tunnel.service.d
sudo tee /etc/systemd/system/reminder-tunnel.service.d/override.conf <<'EOF'
[Service]
User=reminder-tunnel
Group=reminder-tunnel
ExecStart=
ExecStart=/usr/local/bin/cloudflared tunnel --no-autoupdate run --token-file /etc/reminder-tunnel/token
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now reminder-tunnel.service
sudo systemctl status reminder-tunnel.service
curl -fsS https://YOUR_DOMAIN/api/healthz
```

预期：隧道健康，真实 HTTPS 域名返回健康结果。公网不开放 8787。Cloudflare 服务连接异常由运维者检查网络和控制台；不要把临时公开隧道当正式数据入口。若采用 Nginx 路线，参考仓库 `deploy/nginx-reminder.conf.example`，按自己已取得证书配置，先 `sudo nginx -t` 再由唯一运维者加载。

## 4 · 浏览器 + 阿里云：本人 Dot 私有连接

在创建 MCP 应用界面填本人的 `https://YOUR_DOMAIN/mcp`，选择预定义自定义 OAuth 公共客户端，复制精确 client ID 和 callback URL。网站真实主账户 UUID 可通过正式登录响应确认，不能按账号名推测；允许的列表由本人在 `/dot` 界面选择。

阿里云 `.env` 的四项变量需全部齐备：

```text
DOT_ALLOWED_USER_ID=本人真实主账户UUID
DOT_PUBLIC_ORIGIN=https://YOUR_DOMAIN
DOT_OAUTH_CLIENT_ID=本人私有应用的精确客户端ID
DOT_OAUTH_REDIRECT_URI=该应用显示的精确callbackURL
```

不将真实配置填进公开仓库。唯一运维者变更后使配置生效：

```bash
cd /opt/reminder
nano deploy/.env
sudo docker compose -f deploy/docker-compose.yml up -d --force-recreate app
sudo docker compose -f deploy/docker-compose.yml ps
curl -fsS https://YOUR_DOMAIN/api/healthz
curl -fsS https://YOUR_DOMAIN/.well-known/oauth-protected-resource
curl -fsS https://YOUR_DOMAIN/.well-known/oauth-authorization-server
```

若当前部署使用带路径的 discovery 地址，以该服务实际 MCP 元数据为准。404 / 503 先核当前源码路由和四项门控，不更改用户数据。本人在 OAuth 同意页核对一个账户、一个允许列表和 `records.read` / `analysis.write` / `learning.write`，确认后实际调用 `reminder_identity`。成功标准是身份、允许列表、scope、分析权限真实回读一致，受控范围外测试被拒绝；连接成功不能替代首条完整学习验收。

## 5 · Dot 云端：读取方法、固定知识，再验收首条

提供 `本机工具补齐/.claude/skills/learn-project/SKILL.md`、`云端方法/RUNNING_IN_DOT.md` 和 `云端方法/knowledge-index.md`。原方法的本机 Git 步骤由最新 AGENTS 和云端说明限定为本机协调者执行。Dot 需要实际读取方法；把参考原件附到私密对话不会把 Windows 目录挂载给 Dot。

公开 raw 地址打不开时，可以在允许网络与工具范围内获取固定版本 Git 对象读取同一文件。记录来源 commit、文件路径、Blob / SHA256 和实际内容；不能更换安全策略或把私有文件公开来绕开限制。

实际阶段：identity → preliminary 领取 → 来源核实 → 分类理由与报告 → 保存和回读 → 释放；获准 learning 再 full 领取 → 实验、六原件、PDF 逐页检查与独立审核 → 保存完整标签和原件 → 回读 → 释放。任务勾选始终由本人执行。

采用 PDF 第 24 页 / 讲解 Markdown 的启动指令。首条成功后，明确批次 ID 范围、时区、15 分钟周期、异常记录和通知方式，再在 Dot 中实际保存日程并 list 回读。新记录加入允许列表与派入日程是两个检查点。不要声称本手册已经新增或修改日程。

## 6 · Windows：安装本机工具、登录、一次备份

先按 `本机工具补齐/README.md` 在 **新干净 clone** 补齐明确文件。既有目录交由唯一协调者逐文件合并。自建域名时，现有工具还有两个固定服务 origin，先在本机副本中修改：`tools/shiyi_sync.py` 的 `BASE` 和 `tools/reminder_dot_http.py` 的 `SITE`。二者必须等于本人 HTTPS 服务；Android 同步地址、MCP URL、服务器 public origin 也必须一致。只修改 `.env` 不能改变本机 Python 目标。

以下登录示例只接收交互输入，不打印 token，不带密码命令参数；`--save` 明确创建会话文件，不覆盖旧凭据。该会话属于本人网站账户，只用于本机备份，不传给 Dot。

```powershell
Set-Location F:\reminder
python tools/private_login_example.py --help
python tools/private_login_example.py --root F:\reminder --site https://YOUR_DOMAIN --save
$reminderUser = [Security.Principal.WindowsIdentity]::GetCurrent().Name
icacls tools/.shiyi_token /inheritance:r /grant:r "${reminderUser}:(R,W)"
New-Item -ItemType Directory -Force 完成/.pipeline
Copy-Item reminder-dot/dot-backup-config.example.json 完成/.pipeline/dot-backup-config.json
notepad 完成/.pipeline/dot-backup-config.json
& ./tools/reminder_dot_on_login.ps1
& ./tools/install_reminder_dot_backup_trigger.ps1 -WhatIf
& ./tools/install_reminder_dot_backup_trigger.ps1
Get-ScheduledTask -TaskName Reminder-Dot-Backup-OnLogon
Get-ScheduledTaskInfo -TaskName Reminder-Dot-Backup-OnLogon
```

先检查 ACL 显示的真实权限；没有成功限制读取则先停止注册自动任务并由本人处理私密权限。配置填本人 accountId / listId。已存在 token 时示例拒绝覆盖，使用既有会话更新流程，不为登录删旧凭据。账户 UUID 从私密登录结果或 identity 核对，不能放到本包或公开 Issue。

预期：真实下载、报告和六原件全部通过 SHA256，重复运行新增 0；云端原件保留。登录触发只自动备份。学习审核、知识入库与 Git 仍由本机模型协调者执行。

## 7 · Windows 唯一协调者：本地队列与真实验收

首次本机入库前先取得协调者租约；已有协调者只允许本人原名续约，不创建新名字绕过。队列为本目录 SQLite，只读 sync 正式源。网站 full 票据与本机 owner 是不同层级的租约，云端未释放时本机不得抢占。

```powershell
Set-Location F:\reminder
python tools/reminder_coordinator.py status
python tools/reminder_coordinator.py acquire --owner coordinator_example
python tools/reminder_pipeline.py sync
python tools/reminder_pipeline.py status --task TASK
```

新任务未认领、未受保护、来源可核实才做下面的分类与 start；**不得给旧进行中记录强行 claim**。已有 start 票据跳过这组命令，仅原 owner 续约：

```powershell
python tools/reminder_pipeline.py claim --task TASK --owner ORIGINAL_OWNER
python tools/reminder_pipeline.py classify --task TASK --owner ORIGINAL_OWNER `
  --kind learning --reason "真实来源、具体判断、已有知识关联和下一步" `
  --evidence https://AUTHOR_OR_OFFICIAL_SOURCE
python tools/reminder_pipeline.py start --task TASK --owner ORIGINAL_OWNER --project PROJECT
```

这不是请读者用占位理由分类。实际证据必须已经读取、具体理由写全。不仅依赖旧 CLI help 中的“手动 start”文本；当前用户已明确授权获准列表中的核实学习自动完整执行，最终用户勾选仍独立。不同新用户需本人先确认这一执行范围。

长审核或网络等待时，在租约结束前由原名续约：

```powershell
python tools/reminder_pipeline.py renew --task TASK --owner ORIGINAL_OWNER --lease-seconds 3600
python tools/reminder_coordinator.py renew --owner coordinator_example --ttl 7200
```

用 `模板/manifest.example.json` 整理实际指南、HTML、解包后的练习和日志，合并知识提案进 vault 后由另一位实际审核者检查。PDF 和网站原件应完全相同；知识提案合并后的变化需要在私有 handoff 对应 report 的 `knowledge` 中记录 `status: merged` 和真实 `note` 相对路径。

```powershell
python tools/reminder_pipeline.py ready --task TASK --owner ORIGINAL_OWNER --manifest PROJECT/manifest.json
python tools/reminder_pipeline.py review --task TASK --owner ORIGINAL_OWNER `
  --reviewer REVIEWER --notes "真实逐页、实验和知识复核结论"
python tools/reminder_pipeline.py confirm-analysis --task TASK --owner ORIGINAL_OWNER `
  --coordinator coordinator_example --receipt 完成/.pipeline/confirmation-receipt.json
python tools/reminder_pipeline.py render
```

receipt 是路径与校验信息，不能替代真实数据。`backupSha256` 来自此次已有 export 原件 SHA256，`backupBundle` 必须匹配该 hash 命名的 .json，`handoff` 指向同账户和列表，reportId / taskId / sourceHash 与 full 当前来源一致。confirm-analysis 再只读核网站，成功后释放任务资源，**不勾选任务**。六原件缺失、来源变更或独立审核不通过保留待处理，不强填回执。

## 8 · Windows 唯一协调者：独立公开发布副本

PDF 第 29 页展示提交前后命令。第一次初始化发布副本：

```powershell
git clone https://github.com/Smashwinny/reminder_knowlege.git 完成/.pipeline/knowledge-publication
git -C 完成/.pipeline/knowledge-publication config user.name 'YOUR_NAME'
git -C 完成/.pipeline/knowledge-publication config user.email 'YOUR_EMAIL'
git -C 完成/.pipeline/knowledge-publication remote -v
git -C 完成/.pipeline/knowledge-publication diff --cached --name-only
```

朋友用自己的 fork 改远端；两项署名仅配置这一发布副本。凭据由正式 Git 登录管理，不写进 URL。非空且归属不明的暂存区先停止。逐份复制已审核成果，不复制私密报告、原记录、backup 或 token：

```powershell
$publication = 'F:\reminder\完成\.pipeline\knowledge-publication'
New-Item -ItemType Directory -Force "$publication/PROJECT/exercise"
Copy-Item PROJECT/guide.pdf "$publication/PROJECT/guide.pdf"
Copy-Item PROJECT/guide.html "$publication/PROJECT/guide.html"
Copy-Item PROJECT/exercise/main.py "$publication/PROJECT/exercise/main.py"
Copy-Item PROJECT/experiment_log.txt "$publication/PROJECT/experiment_log.txt"
# 以下笔记目录首次不存在时，先创建对应目录
Copy-Item vault/项目笔记/PROJECT.md "$publication/vault/项目笔记/PROJECT.md"
Copy-Item vault/概念/CONCEPT.md "$publication/vault/概念/CONCEPT.md"
Copy-Item vault/00-总览.md "$publication/vault/00-总览.md"
```

例子只展示一份实验和一个概念；实际多份交付逐个增加明确文件名。保持协调者租约，依 PDF 第 29 页显式 add、diff、commit、push、远端 SHA 回读。每一步是真实执行后才在私有 handoff 中记状态。远端 main 与实际提交 SHA 一致后记 pushed；失败保留 pending。完成本次收尾或明确保留待同步后，原协调者 release；不得声称失败时也已推送。

更新云端查重参考必须来自已发布版本：

```powershell
git -C 完成/.pipeline/knowledge-publication fetch origin main
$published = git -C 完成/.pipeline/knowledge-publication rev-parse origin/main
python tools/reminder_dot_reference.py --root 完成/.pipeline/knowledge-publication `
  --source-commit $published --output 完成/.pipeline/public-reference
```

该工具当前显式允许 Smashwinny/reminder_knowlege；朋友 fork 必须先评审调整工具中的 `REPOSITORY`，不能随意扩大读取范围。把新固定索引通过私密对话交给 Dot 并实际读取，不只生成本地文件就宣布云端已更新。

## 9 · Obsidian：本人建立知识网络与复习

用 Obsidian 打开 `F:\reminder\vault`。`模板/概念笔记.md` 放入 `vault/概念/`，项目笔记放入 `vault/项目笔记/`，复习样例放入 `vault/复习/`。填写自己的定义、已读来源、实验证据和边界，先查重再命名；`[[概念名]]` 对应真实笔记，不留假链接。项目指南位于 vault 外时，可用相对 Markdown 链接供阅读，但 Obsidian 外部根路径打开可能依平台而异；需要跨设备稳定点击时使用已发布 Git 文件链接或把允许的附件放在 vault 内。

打开 `00-总览.md` 和局部图谱验证双链。每日先回答 3–5 个概念问题，主动回忆定义、机制、反例与迁移小实验，然后对照 PDF / 日志。Dot 根据本人回答给评分建议，本人确认，保存日期、错因和下次时间。PDF 第 31 页给出建议日程；本次未修改已有复习日程，评分写回与间隔算法需另行验收。

## 10 · 联调通过后才开始批量

按 PDF 第 32 页逐项实际检查。每个“已完成”必须说明是云端报告保存、本机备份、知识合并、内容验收、Git commit 还是远端 push；本机离线允许云端继续，只保留待回迁状态。用户名、token、列表 UUID、原私密记录、私密任务链接不放入公开协作 Issue。
