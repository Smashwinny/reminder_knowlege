---
tags: [项目]
类别: 开源项目类（Cloudflare Serverless 全栈最小件）
上游仓库: https://github.com/replicate/hype
完成日期: 2026-10-03
---

# replicate-hype（hype.replicate.dev）

**这是什么**（一句话）：Replicate 官方开源的 HN 风格 AI 趋势聚合站（Apache-2.0，254★）——每小时抓 GitHub 新 Python 仓库 / Replicate 模型调用 / HuggingFace 新模型 / Reddit 三大 AI 版周榜，用跨平台评分公式统一排名，仅 9 个源码文件共 593 行。

**它给我什么能力**：
- 每天看一张榜追踪全球 AI 热点（行为数据信号，不是推特口头安利）
- 自部署模板：fork 后 wrangler 五步上线自己的趋势雷达（Cloudflare 免费额度即可）
- 开放 JSON API（/api/posts 支持 filter 时间窗 + sources 源过滤），可接日报机器人
- Serverless 全栈入门最佳教材体量：Hono 路由 + D1 SQL + Mustache 渲染 + Actions 定时

**引入的概念**：
- [[Serverless边缘函数]]（Cloudflare Workers + D1 + wrangler --local 本地模拟）
- [[跨源评分归一化]]（scorePost：×0.3 / ^0.6 幂函数压大数；先截断后归一的误杀教训）

**实验记录**（`F:\reminder\replicate_hype\exercise\seed.sql` + dev.log，全部真实运行，6/6 PASS）：
- 本地 D1 建表 → seed.sql 造 9 条混合源数据（5 评分组 + 2 黑名单组 + 2 时间窗组）→ wrangler dev 起站 127.0.0.1:8787
- 排序实测与 scorePost 预测逐位一致：gh-a(2000) > gh-b(1000) > Reddit(原始3000→900) > HF(800) > day-old(600) > Replicate(原始32000→504)
- 黑名单（99999★ crypto / 88888★ nft）0 泄漏；past_day 正确剔除 2 天前条目；sources=GitHub 只留 3 条
- 改参数看变化：reddit 权重 0.3→1.0 热重载后 Reddit 条目从第 3 跳第 1（权重即编辑立场），git checkout 恢复
- 坑：npm 11 拦 postinstall，需 `npm install-scripts approve workerd esbuild`；.dev.vars token 留空不影响本地实验（不走 /api/update 即可）

**后续可深入的方向**：
- 自部署一份改黑名单词与权重，做垂直领域雷达（量化/安全圈）
- 把归一化下推进 SQL，修复"先截断后归一"误杀，给上游提 PR
- /api/posts 接飞书/TG 做每日 AI 情报推送
