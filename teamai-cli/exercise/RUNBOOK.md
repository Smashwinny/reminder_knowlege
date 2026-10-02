# teamai-cli 轻量实验 RUNBOOK（全命令实测，2026-10-03）

环境：Windows 11 / Node v24.21.0 / Git 2.55 / teamai-cli v0.26.0（npm 全局）

## 实验设计

无真实 GitHub 托管端时，用"本地 bare 仓 + 自签证书 HTTPS 静态服务"模拟 Git 托管端
（git dumb HTTP 协议只需静态文件 + `git update-server-info`），验证完整分发链路：

```
管理员(seed/) --git push--> team-repo.git --update-server-info+HTTPS--> 成员端 init/pull
```

## 步骤与真实输出

### 1. 管理员端准备资产
```bash
git init --bare team-repo.git && git clone team-repo.git seed
# seed/ 中写入 skills/hello-team/SKILL.md、skills/deploy-check/SKILL.md、rules/*.md
git add -A && git commit -m "feat: 首批团队资产" && git push origin main
```
材料见 `materials/`。

### 2. 起本地 HTTPS 服务（dumb HTTP）
```bash
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 2 -nodes -subj "//CN=127.0.0.1"
cd team-repo.git && git update-server-info   # 生成 info/refs
python https_server.py                        # 见本目录，端口 8667
```
坑①：URL 必须是 `https://host/group/repo.git` 形态 → 服务根目录要取上一层，
让 `/team/repo.git` 恰好映射到 `team-repo.git`（映射错一位 → git 404，看服务访问日志定位）。
坑②：plain HTTP 被拒（teamai 明确报 "plain HTTP is not supported"）。
坑③：本地裸路径（`F:/.../team-repo.git`）也被拒，同样报 URL 格式错。

### 3. 成员端初始化（真输出）
```bash
GIT_SSL_NO_VERIFY=1 TEAMAI_NONINTERACTIVE=1 \
  teamai init https://127.0.0.1:8667/team/repo.git --provider git --agent claude --force
```
```
✔ Using Git identity Smashwinny
ℹ Clone path: C:\Users\Windows\.teamai\projects\F-reminder-5680e43d1265317e\team-repo
✔ Team repo cloned
⚠ Push failed ... Author identity unknown        # 团队仓 teamai.yaml 直推 main 需配置身份
✔ Updated teamai hooks in C:\Users\Windows\.claude\settings.json
✔ teamai initialized successfully!
```
init 做了三件事：克隆团队仓到 `~/.teamai/projects/<项目hash>/`、注入 hook、部署内置 teamai skill。
注入的 hook（真实 settings.json 节选，注意 `|| true` fail-open）：
```
SessionStart: "C:/Program Files/Git/bin/bash.exe" -lc "teamai hook-dispatch session-start --tool claude 2>/dev/null" || true
Stop / PostToolUse / UserPromptSubmit 同理，各带 matcher
```

### 4. 分发验证（真输出）
```bash
teamai pull
```
```
✔ [project] Synced 2 skills (2 new, 0 updated)
    new: deploy-check, hello-team
✔ [project] Synced 2 rule(s)
```
落点：`F:\reminder\.claude\skills\{hello-team,deploy-check,teamai}` + `.claude\rules\*.md`
坑④：成员目录不是 git 仓时，teamai **向上锚定最近 git 仓根**做 project scope——
member2 建在总仓库内，资产直接装进了总仓库 `.claude/`，当前 Claude Code 会话即时热加载出
deploy-check / hello-team / teamai 三个 skill（活的证据）。

### 5. 增量同步验证（真输出）
管理员改 hello-team → v2，push 后刷新 served 副本（dumb HTTP 无钩子，需再跑
update-server-info；真实托管端由平台 webhook 兜住，无此手工步），成员端：
```
✔ [project] Team repo: 1 file(s) changed
✔ [project] Synced 2 skills (all updated)
✔ [project] Synced 2 rule(s)
```
本地 `SKILL.md` 变 v2，会话内 Skill 清单同步刷新。

### 6. 其他命令级验证
- `teamai list skills` → REPO SKILLS: deploy-check, hello-team；LOCAL AGENTS: [claude] F:\reminder\.claude\skills 4 skills
- `teamai status` → last pull 时间 + Team resources: skills 2 / rules 2
- `teamai roles/tags --help` → 子命令 init/list/set/add 确认分发策略入口

### 7. 清理（真实环境还原）
```bash
TEAMAI_NONINTERACTIVE=1 teamai uninstall --force
```
```
✔ Removed teamai hooks in C:\Users\Windows\.claude\settings.json
✔ Removed 3 skill directories
✔ Removed 2 rule files
✔ Removed C:\Users\Windows\.teamai\projects\.../
✔ teamai uninstalled
```
再手工删 `~/.teamai` 残余（dashboard/debug.log/locks/state.json）并杀掉 8667 服务进程。

## 实验未覆盖（诚实记录）
- MR 评审流：dumb HTTP 只读，`teamai push`（建分支+MR）需要真实 GitHub/GitLab 端，未实测
- Roles/Tags/Sources 实际分发差异：只验证了命令面与文档行为，未做多角色对比
- Team Context / Improvement 层（recall、代码知识图谱、dashboard）：beta 功能未实测
