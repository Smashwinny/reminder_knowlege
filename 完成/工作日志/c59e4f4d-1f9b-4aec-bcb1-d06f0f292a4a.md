# 工作日志 c59e4f4d-1f9b-4aec-bcb1-d06f0f292a4a

05:08 [分析] fxtwitter 拿到推文全文：Shixi Lin（@11Shixi）自研网站，把 Codex 和 Claude 的公开重置消息放一页，每 30 分钟检查一次，支持九种语言，下次重置时间按本地时间显示。链接 https://shixilin.com/ai/codex-claude-resets/ ，推文附 22 秒演示视频。推文未提 GitHub 仓库。下一步：查工具有无开源仓库 + 抓取该网站本体看技术实现。
05:12 [分析] 网站本体抓取成功：聚合 @thsottiaux/@ClaudeDevs/@OpenAI 的重置公告，倒计时+过去7天feed+分类标签（Quota reset/Reset credit/Reset signal/Usage update）+浏览量统计，9语言（英/简中/繁中/日/韩/西/法/德/阿）。页面无源码链接，但作者 GitHub 主页 github.com/shixi-11 有同名仓库 codex-claude-resets（JavaScript，topics 含 github-actions）→ 开源确认。判定：学习类（开源轻量 web 工具，可动手实验）。
05:25 [克隆] repo 克隆成功 @ c2a9a70，Node v24.21.0 满足要求，零依赖项目无需 pnpm install
05:30 [实验1] node --test：60/60 全过（823ms），覆盖分类回归/中继证据匹配/locale 一致性
05:32 [实验2] node scripts/build.mjs：Built 9 locales, 78 events and 711 pages → dist/ 静态站
05:33 [实验3] serve.mjs 本地 4187 端口：/ 313B meta-refresh 跳板，/en/ 465KB 完整页，/zh/ 中文标题正常，events.json 78 条
05:36 [实验4] collect.mjs 真实采集：6 个 FxEmbed 时间线全 ok（候选 19/11/16/14/21/18=99），X official embed ok，mode=profile-relay，78 记录保留
05:40 [实验5] 直调 evidence.mjs classify()：6 组用例验证证据状态机（announced/reported/unconfirmed/information），截断一律 unconfirmed，RULES_VERSION 1.4.2
05:41 [实验] 实验记录已写入 codex-claude-resets/exercise/实验记录.md。下一步：疑问清单+PDF
05:45 [疑问清单] 12 问定稿（已用 vault 过滤：事实与判断分离/健康探测三态/信号非证据等已掌握概念不重复展开）：1一句话是什么 2为什么需要 3没X API怎么采集(信任链) 4证据状态机四态 5为何截断必不确认 6数据存哪(git即数据库) 7定时调度怎么设计 8健康怎么算 9九语言实现 10时区处理 11为何非MIT 12可搬走的模式
05:46 [查重] vault 概念 grep：无"证据状态/中继印证/提交即部署"现成条目；相关已有=事实与判断分离/健康探测三态/AI味模式库与信号非证据/快照契约与不可变只读/发布交换与健康门回滚/数据源降级链 → 计划新建3概念并互链
05:52 [PDF] guide.html 写完（12问卡片+10张SVG+5步实验），Edge 无头打印成功 812KB，改名 CodexClaude重置追踪器-小白指南.pdf，直接落在 F:\reminder\codex-claude-resets\ 内（未落根目录）。坑：msedge 不在 PATH，用完整路径 "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
06:00 [入库] vault 3 概念（证据状态机/中继交叉印证/提交即部署）+ 项目笔记 codex-claude-resets.md + MOC 新分区"数据采集/可信追踪与零运维部署"+项目索引行，概念计数 154→157
06:05 [站点] shiyi_sync.py done 标完成成功；纲要追加时发现并行 worker 已占序号 47/48，改用 49
