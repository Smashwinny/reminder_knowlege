---
tags: [概念]
领域: AI 工程 / 数据输出契约
别名: [meta wrapper, freshness声明, possibly_stale]
首次来源: "[[项目笔记/wx_cli_again]]"
---

# meta新鲜度声明

**一句话定义**：给 AI Agent 消费的查询输出不返回裸数组，而是 `{data, meta}` 包装——meta 里显式声明数据新鲜度（status/unknown_shards/双源时间对账），让 agent 自己判断"这份结果能不能信、缺了哪块"，而不是输出残缺的假完整。

**属于领域**：AI 友好的数据输出契约。

**通俗理解**：像超市货架上的标签不只有价格，还有生产日期和"缺货中"告示。`meta.status` 是保质期（ok / possibly_stale / windowed），`unknown_shards` 是缺货清单（磁盘上存在但没密钥的分片），`chat_latest_timestamp` vs `session_last_timestamp` 是双账本对账——微信自己记的账比查到的多，就是漏了。讲完比喻落回术语：分片库（message_N.db）各持独立密钥，冷分片可能永远没密钥，查询结果必须如实标注覆盖面；人类看 stderr 警告，agent 直接读 stdout 的 meta 字段。

**与已有概念的关联**：
- 与 [[证据优先质检ProofOverClaims]] 同向：不让下游把"残缺输出"当完整证据用，但它是声明式（在输出里写清）而非质检式（事后验）
- [[证据状态机]] 给证据分级，meta.status 给查询结果分级，都是"先把成色亮出来"
- 缺密钥分片问题源于微信分片结构（见 [[项目笔记/wx_cli_again]]）

**首次接触于**：[[项目笔记/wx_cli_again]]
