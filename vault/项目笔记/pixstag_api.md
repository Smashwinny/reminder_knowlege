---
tags: [项目笔记, 视频生成 API, 异步任务, 用量对账]
created: 2026-10-27
---
# PixStag 视频生成 API

PixStag 是多模型视频生成聚合接口（MiniMax-H3 / Seedance 2 / 2.5）：创建任务返回 task_id，用轮询或 webhook 追踪，usage 按秒计量。

## 核心概念
- [[异步任务五态契约]]：queued/running/succeeded/failed/cancelled，受理与完成必须分开。
- [[按秒用量对账]]：请求时长与 usage.total_seconds 必须一致，另核对积分有效期与失败重试成本。

## 实测
真实无 token `GET /user/me` 返回 HTTP 401 + code 1004，与官方错误契约一致。本地状态机三轮到达 succeeded；用量一致放行、篡改拒付复核通过。content.text 必填非空≤5000 字，role 包含 first_frame/last_frame/reference 三类。

未执行付费创建任务，真实生成质量、速度和账单未验证。
