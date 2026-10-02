---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/Rion-Wu-tech/wechat-intelligence-hub
完成日期: 2026-10-03
---

# wechat-intelligence-hub

**这是什么**（一句话）：跑在本机的"微信个人情报库"——只读读取本地微信聊天记录，用确定性规则引擎产出待回复/承诺/商单/复联线索日报（Markdown + 净化 HTML），数据不出电脑、不 Hook 不代发。来源：X 拾遗链接（gkxspace 推荐"先 fork"帖）。AGPL-3.0，v0.9.2-preview.2，2.6k★。

**它给我什么能力**：
- 聊天导出文件 → 商单日报（类别×阶段×优先级信号 + 证据原句）
- 承诺/待回复跟踪、商机雷达（金额抽取）、复联线索识别
- 本地情报库按人/关键词/日期检索；Markdown→净化 HTML 报告
- 两个 Codex Skill 目录可作"给 Agent 的操作规程"模板

**引入的概念**：
- [[CleanRoom只读读取器]] —— 不 Hook/不重签名/不注入的只读边界（SQLCipher+WCDB+zstd 三道门）
- [[确定性信号引擎]] —— 规则打标"类别×阶段×优先级"，附证据原句，筛子非裁判
- [[文档渲染与XSS净化]] —— pandoc 转换 + nh3 白名单消毒，缺件明确报错不降级

**实验记录**（Windows 11 + Python 3.14，全实测）：
- 官方虚构 demo 跑通：8 消息→21 信号→5 对象；fake-vault 3 消息→9 信号
- 自建 13 条"考题"（exercise/my_chat.txt）：7 信号。"尾款/首款"精准命中结算（优先级5）、老同学合作命中复联新线索；误报：买票/读书会报名被判"待确认排期"；漏报："改好了晚上发你"类承诺句；猎聘 JD/快递正确忽略 → 印证"宁可多报"的筛子定位
- 环境坑：Git Bash 下需 `PYTHON_BIN=python`；pandoc 用 `pypandoc-binary` 自带 3.9 免安装；nh3/zstandard 直接 pip
- 边界验证：无授权库时 `home`/`db-status` 明确报"找不到数据库"，不降级
- 产物：`wechat-intelligence-hub-小白指南.pdf`（10 页彩色）、`exercise/`（my_chat.txt + out-my-scan/ 含 signals.csv、daily_digest.md/html）

**后续可深入的方向**：读 `wechat_intelligence_hub.py` 的规则表改出中文语境更准的承诺识别；研究 skills/ 目录的规程写法迁移到自己的 Agent 项目；关注 Windows 首次取钥合入进展（未真机验收前勿用于真库）。
