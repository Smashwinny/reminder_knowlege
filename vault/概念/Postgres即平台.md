---
tags: [概念]
领域: 软件架构 / 数据库
别名: [Postgres as the Platform, Postgres as a backend, 万物皆 Postgres]
首次来源: "[[项目笔记/temps]]"
---

# Postgres即平台

**一句话定义**：把队列、缓存、定时任务、发布订阅、全文检索全部交给一个 Postgres 承担，让"数据库"升级为"平台的唯一状态真相"。

**属于领域**：软件架构 / 数据库设计（pgmq 队列、LISTEN/NOTIFY、SKIP LOCKED 抢占、TimescaleDB 时序扩展）

**通俗理解**（比喻/例子，讲完落回术语）：别人给你寄快递要经过分拣中心（Redis/RabbitMQ 各一道），Postgres 即平台是"所有包裹都存进同一个仓库，取件人对着账本自取"——账本本身就是分拣系统。落回术语：部署任务=数据库的一行，worker 用 `SELECT ... FOR UPDATE SKIP LOCKED` 轮询认领，排队/重试/审计天然免费，因为它们都是普通 SQL。

**实测证据**（Temps，2026-10-03）：官方安装器不装任何消息中间件/Redis，全程 Postgres（+TimescaleDB）单一依赖；网站分析事件走时序表+连续聚合；代理路由表也在库里，Pingora 进程内实时查询。

**代价与收益**：收益=备份/迁移/安全边界只剩一条（备一个库=备整个平台）；代价=Postgres 成为单点命门，规模上来后必须走向 [[控制面与数据面]] 分离或多节点（Temps 用 temps join/agent/node + ClickHouse 可选承接日志热点）。

**与已有概念的关联**：
- [[单二进制自托管架构]] — 硬币的另一面
- [[消息队列与异步削峰]] — 对照组：独立的 MQ vs PG 表当队列
- [[缓存]] — 缓存层被 PG 物化视图/表替代的取舍
- [[向量数据库]] — pgvector 是同一思想的又一战例

**首次接触于**：[[项目笔记/temps]]
