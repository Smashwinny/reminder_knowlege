---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/Tencent/teamai-cli
完成日期: 2026-10-03
---

# teamai-cli

**这是什么**（一句话）：腾讯开源的团队 AI 资产同步 CLI——把一个人的调教经验（skills/rules/hooks/MCP 等）放进共享 Git 仓库，经 PR 审核后自动分发到 16 种 AI 编码工具的本地原生目录（"Make Every Team AI Native"，One Team. One Harness. Every Agent.）。

**它给我什么能力**：
1. 一条命令把普通 Git 仓库变成团队 AI 资源库（`teamai init <仓库URL>`）
2. push 自动走"建分支+MR"评审流，代码 review 纪律搬到 AI 资产上
3. 成员开会话即自动 pull（SessionStart hook），无感拿到团队最新 harness
4. Roles/Tags/Sources/Projects 四维分发策略，不同角色领不同资产
5. 摩擦信号驱动经验沉淀：被打断/纠正/重试失败的会话才提示 `/teamai share`
6. dashboard/digest 看板：成员干预次数、token 用量、知识库健康

**引入的概念**：
- [[团队Harness的Git原生分发]]
- [[摩擦信号经验沉淀]]
- [[资源命名空间分发]]

**实验记录**（做了什么、结果、坑）：
- 全本地闭环真跑通（npm v0.26.0）：管理员 seed 仓写 2 skills + 2 rules → push 到本地 bare 仓 → 自签证书 HTTPS 静态服务（dumb HTTP：`git update-server-info`）模拟 Git 托管端 → 成员端 `teamai init https://127.0.0.1:8667/team/repo.git --provider git --agent claude`：克隆团队仓 + 向真实 `~/.claude/settings.json` 注入四类 hook + 部署内置 teamai skill → `teamai pull` 把 skills/rules 同步进项目 `.claude/` 目录，当前 Claude Code 会话**实时热加载**出新 skill
- 增量验证：管理员改 hello-team 到 v2 → push → 刷新 served 副本 → pull 输出 "1 file(s) changed / Synced 2 skills (all updated)"，本地文件与 Skill 清单同时变 v2
- 坑：①URL 强制 https://host/group/repo.git 或 ssh 格式，本地路径/plain HTTP 一律拒绝；②dumb HTTP 只读，push（MR 流）必须真实 Git 托管端；③项目 scope 向上锚定最近 git 仓根——member2 不是 git 仓，资产直接装进了外层总仓库 `.claude/`（当前会话热看到的原因）；④HTTP 服务根目录映射错一位 → git 404，看服务访问日志定位
- 清理：`teamai uninstall --force` 还原 settings.json hooks、删 3 skill 目录 + 2 rules + ~/.teamai，杀掉服务进程

**后续可深入的方向**：
- 单仓模式（`teamai init .`，业务仓即团队仓）与 learnings/reports 孤儿分支
- Team Context 层：`teamai import` 代码知识图谱（tree-sitter AST 轨 + 启发式轨双轨提取）
- 在真实 GitHub 上跑一次完整 MR 评审流（本实验因 dumb HTTP 只读未覆盖）
