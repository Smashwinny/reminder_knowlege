---
tags: [概念]
领域: 云计算 / 后端架构
别名: [Cloudflare Workers, 边缘函数, Edge Function]
首次来源: "[[项目笔记/replicate-hype]]"
---

# Serverless边缘函数

**一句话定义**：把代码上传到云厂商全球节点，请求来了就近执行、没请求零计费，"无服务器要管"的部署形态——Cloudflare Workers 是其中最轻的一档（免费 10 万请求/天 + D1 SQLite + 定时触发全家桶）。

**属于领域**：云计算 / Serverless 后端架构

**通俗理解**：传统部署像开店雇全职员工（服务器 24 小时计费，没客人也发工资）；Serverless 像外卖骑手抢单——没有订单（请求）一 分钱不花，订单来了就近派最近的骑手（边缘节点）接单。hype 项目整个后端就是一个 Worker：入口导出 `fetch` 处理 HTTP + `scheduled` 处理定时，配 D1（跑在边缘的 Serverless SQLite，写的就是普通 SQL）+ Hono 路由 + Mustache 模板，593 行跑完一个完整网站。

**与已有概念的关联**：
- 本地开发用 `wrangler dev --local` 在本机模拟器跑 Worker 和 D1——不花一分钱、不申请 key 就能整站验证，同款思想见 [[本地推理引擎]]（把云上的东西搬到自家厨房先跑通）
- 定时抓取不必和 Web 服务住在一起：hype 把每小时的脏活外包给 GitHub Actions 免费算力，Worker 只负责接单——与 [[消息队列与异步削峰]] 同属"把周期性重活从常驻服务剥离"的模式
- [[个人量化工具箱范式]] 的"游击队路线"在云端的对应物：零月费跑起一个全栈网站

**实例出处**：replicate/hype（Apache-2.0），线上 hype.replicate.dev
