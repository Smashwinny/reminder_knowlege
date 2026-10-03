---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/gotempsh/temps
完成日期: 2026-10-03
---

# temps（Temps）

**这是什么**（一句话）：Rust 写的自托管 PaaS——"一个 Rust 二进制 + 一个 Postgres"吃下 Vercel+Sentry+PostHog+Pingdom+Resend+E2B 六个 SaaS 的活，AI 原生（440+ CLI 命令 + 13 个官方 Claude 技能包）。MIT OR Apache-2.0 双许可。

**它给我什么能力**：
- 一台 VPS 拥有 Git push 部署、预览 URL、自动 TLS、托管 PG/Redis/S3/Mongo
- 零成本可观测栈：分析/会话回放/错误追踪/OTel/可用性监控内置
- AI 运维：skills/ 目录 13 个 drop-in 技能包直接进 .claude/skills/，agent 可驱动全部平台操作
- Pingora 进程内代理：域名路由表实时查库，edge 子命令还能当 CDN 节点

**引入的概念**：
- [[单二进制自托管架构]]
- [[Postgres即平台]]
- [[BYOK模型网关与用量归因]]

关联已有：[[AgentSkills技能包]]（13 个 drop-in skills 同构）、[[负载均衡与反向代理]]（Pingora vs Nginx）、[[控制面与数据面]]（server/worker/edge）、[[提交即部署]]、[[内容型开源与双许可]]、[[Realtime协议兼容层]]（Sentry/Vercel-SDK/OpenAI 兼容=同一"协议面标准化吃生态"思想）。

**实验记录**（3 个零依赖实验真跑，材料在 F:\reminder\temps\exercise\）：
1. exp1_arch_anatomy.py——workspace 94 crates 分 9 大领域；4 个 main.rs 但发布单一 temps 二进制，18 子命令枚举与源码一致；
2. exp2_cli_skills_count.py——npm CLI 77 命令组/143 命令文件（README 口径 69 组/440+ 条为子命令展开数，已标注差异）；OpenAPI 853 路径含 Sentry 兼容 /0/ 风格；13 个官方 skills；
3. exp3_deploy_anatomy.py——deploy.sh 4418 行 TUI，9 步向导只装 temps 二进制（systemd）+ timescale/timescaledb-ha:pg18 容器，"一个二进制+一个 Postgres"实锤。

**坑与结论**：
- Windows 未跑 temps serve 全功能（需 Docker+systemd），判学习类靠源码与安装器解剖，不靠起服务；
- CLI "440+ 命令"是营销口径，源码文件数 143，两种统计都记入 PDF；
- 抖音视频本体抓不到（douyin JS 渲染+风控），靠 WebSearch 交叉验证锁定主体为 Temps（与分享文本"一个 Rust 二进制 + 一个 Postgres"逐字吻合）。

**后续可深入的方向**：
- Linux 机器真跑 deploy.sh 全流程，体验 push-to-deploy + 预览 URL
- 读 ADR 目录（48 个 ADR）学"架构决策记录"写作
- 把 13 个官方技能包与本仓库 learn-project skill 对比，吸收 AI 运维设计
