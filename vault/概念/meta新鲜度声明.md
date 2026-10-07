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

## Metrik：未知、陈旧与旧周期失效分开（2026-10-05）

[[项目笔记/metrik]] 把“数值连同成色传递”的方法用于额度展示，但它的窗口 view 字段不是本文原项目的 meta 协议。读数至少需要分清：

- available=false：没有可用读数；不能把占位 0 当成零余量
- available=true 且数值为 0：有效的零余量，应与未知区分
- stale=true、resetExpired=false：读数陈旧但仍属于未结束的周期；真实 JS 选择器保留它，调用方仍须带陈旧提示
- resetExpired=true：记录的重置点已经过去；选择器排除旧周期读数，但不能据此宣称已查询到新周期的 100%

托盘决策函数对 null 显示 `--`，对有效 0 显示 `0`；tooltip 与状态指纹保留 stale 位。另一个 `compactTokens(null)` 格式化器会返回字符串 `0`，所以不能拿格式化文本替代可用性证据；本轮未测试完整 UI，不能据此断言产品误报。字段契约关联 [[单一馈送与schema冻结]]，选择流程见 [[多窗口额度的展示选择规则]]。

已有实验只执行“给定状态位进入 JavaScript 后”的逻辑；后端如何计算 age/stale/resetExpired、缓存 TTL、鉴权与刷新均只作源码审阅。[[缓存]] 与 [[缓存有效期与发布边界]] 提供相关时效思路，但旧项目 TTL 不迁移成 Metrik 刷新周期；[[双时钟模型]] 讨论回放内容与呈现时钟，也不与这里的采样时间、当前时间和重置点做同义合并。

来源：[quotaWindows.js](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src/quotaWindows.js)、[trayBadge.js](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src/trayBadge.js)、[tokenFormat.js](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src/tokenFormat.js)、[后端时效派生](https://github.com/keros68/metrik/blob/637444bdc8d91475f66f5319a15dda0e4be1c652/src-tauri/src/engine.rs#L1343-L1372)。实测范围见 [实验日志](../../metrik/delivery/04-experiment-log.md)。
