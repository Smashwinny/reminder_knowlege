# 第4项来源与可读性

访问统一2026-11-11 Asia/Shanghai。非Git帖子/网页SHA不适用，本地文件字节由批次SHA256SUMS留证。

## 原帖
- https://x.com/i/status/2112838884510048647 — 通过x只读工具note_tweet全文可读，作者数字生命卡兹克；规范URL https://x.com/Khazix0918/status/2112838884510048647 。创建2026-10-21 17:30:19 Asia/Shanghai；未返回引用关系；原文转录见sources/post-reading.md。
- https://pbs.twimg.com/media/HVJO02_awAA24Yt.jpg — 下载成功并Read，白天微缩厂区图。
- https://pbs.twimg.com/media/HVJO3LJbwAAeAxH.jpg — 下载成功并Read，夜间雪景图。两图均为作者展示，非本轮结果。
原帖只附配图，无仓库链接。

## 作者后来公开的相关中台（不是已确认的微缩前端）
固定main SHA `e8748fd0c2aad4013e5996c3188535567070f24a`。提交2026-11-11 01:17:23 Asia/Shanghai。README明确没有后台界面，协议也明确中台没有界面；未取得可核实的原帖微缩前端开源仓库，不断言其他地方绝不存在。
- https://github.com/KKKKhazix/agent-autoloop/blob/e8748fd0c2aad4013e5996c3188535567070f24a/README.md — 实读1–180；无后台界面声明与职责。
- https://github.com/KKKKhazix/agent-autoloop/blob/e8748fd0c2aad4013e5996c3188535567070f24a/LICENSE — 全文实读；MIT不自动覆盖未公开的3D美术资源。
- https://github.com/KKKKhazix/agent-autoloop/blob/e8748fd0c2aad4013e5996c3188535567070f24a/docs/protocol.md — 实读1–150、297–319及定向检索；事件身份与快照seq，不运行请求。
- https://github.com/KKKKhazix/agent-autoloop/blob/e8748fd0c2aad4013e5996c3188535567070f24a/package.json — 全文实读；Node24+。
- https://github.com/KKKKhazix/agent-autoloop/blob/e8748fd0c2aad4013e5996c3188535567070f24a/cli/status.ts — 全文实读；纯状态渲染，未运行。
- https://github.com/KKKKhazix/agent-autoloop/blob/e8748fd0c2aad4013e5996c3188535567070f24a/cli/spend.ts — 全文实读；纯展示函数，未运行。
- https://github.com/KKKKhazix/agent-autoloop/blob/e8748fd0c2aad4013e5996c3188535567070f24a/tests/status-view.test.ts — 全文实读；3项纯测试未执行，不写通过。

## 知识库
main已首先ls-remote确认未变：`a8674777e18302b8804b137212b1396cbfe5a747`。旧克隆仅只读，未改共享_common。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/00-总览.md — 前项已读同SHA，本项全文关键词查重。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/JSONL事件日志与折叠模型.md — 全文实读，不借用原项目乱序/幂等保证。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/多窗口额度的展示选择规则.md — 全文实读，展示规则/新鲜度与业务动作分开。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/agent_desktop/agent_desktop-小白指南.html — 沿用前项已研究旧成果风格；本项复用自有模板。

## 官方文档与真实公开数据
- https://open-meteo.com/en/docs — WebFetch全文可读；current为15分钟天气模型数据，is_day、WMO天气码、单位与时区。
- https://open-meteo.com/en/licence — 全文可读；数据署名要求与开源代码AGPLv3是不同层。
- https://open-meteo.com/en/terms — 全文可读；免费API仅非商业，调用限额与CC-BY4.0。本轮教育取数一次，无购买/订阅。
- https://api.open-meteo.com/v1/forecast?latitude=31.23&longitude=121.47&current=temperature_2m,is_day,precipitation,weather_code&timezone=Asia%2FShanghai — 实际curl成功；响应见sources/weather-response.json。请求点是公开固定演示点，不是用户位置。
- https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html — 全文可读；暂停/停止/隐藏与自动更新边界；未做完整WCAG验收。
- https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html — 全文可读；颜色不能是唯一信息通道，未实测无障碍行为。

## 仅作发现，不当一手执行证据
定向搜索“Khazix0918 流水线 github 2026”“数字生命卡兹克 微缩 Agent 开源2026”。结果包括 https://aibrev.com/sdlc-playbook/articles/agent-autoloop/ 、https://www.jxxy.net/ai/articles/Khazix0918-2117776745688646139/ 、https://teapaw.org/Khazix0918/media 、https://www.shippingskool.com/use-cases/khazix-routes-events-claude-codex-agents-mac-minis 、https://www.30aitool.com/daily/read/9735/10/ 、https://aihot.news/story/bb685c8f-8176-4496-8733-0a85a9a01513 、https://weibo.com/5700099573/Rolnrhdo1 及nitter镜像。只读搜索摘要后定位官方仓库，不把后续天数、性能/费用或作者宣传当本轮实测；其中安装/发布/自动化建议均未执行。

## 用户叫停
停止继续实验，不把源码/测试阅读说成实际执行。候选网页与headless场景截图未完成；PDF仅是学习笔记的打印。
