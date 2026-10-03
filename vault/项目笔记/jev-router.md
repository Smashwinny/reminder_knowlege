---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/gargpratyush/jev-router (MIT, 525★)
完成日期: 2026-10-03
---

# jev-router

**这是什么**（一句话）：给 Claude Code / OpenAI Codex 加"AI 裁判"的开源路由框架——本机回环代理 + 哨兵模型 `jev-router` + Jev 决策模型逐轮选档（Haiku 琐事 / Sonnet 普通 / Opus 硬活），fail-open 设计。

**它给我什么能力**：npm 一行装上省钱外挂；看懂"决策模型"新物种；可平移的"回环代理+哨兵+本地策略"CLI 改造范式；无 key 用 mock Jev 全流程演练的教具。

**引入的概念**：
- [[SystemOne决策模型Jev]]（Choice/Score/Noul 类型化决策，闭源托管，$0.042/M 输入输出免费）
- [[逐轮模型路由与哨兵代理]]（回环代理 + 哨兵模型 + policy 兜底）

**实验记录**（2026-10-03，全部真实运行）：
1. `npm install` + `npm test`：65 用例 64 过 1 跳过（live-routing 需真 key）0 失败
2. 自建 `exercise/mock-jev-server.mjs`（100 行实现 POST /v1/systemone 假裁判，利用 SDK 的 TYPESAFE_BASE_URL 接缝）+ `exercise/demo-routing.mjs` 驱动 repo 真实 askJev/decide：五场景（琐碎→haiku/普通→sonnet/困难→opus/低置信0.10→封顶sonnet/"use opus"→override）全部符合策略设计，回环延迟 3~61ms
3. 端到端 `node bin/jev-claude.mjs -p`：真实拉起回环代理 + claude CLI；默认模型非哨兵 → 日志 `[jev] passthrough, user selected kimi-for-coding`（哨兵直通机制实证）；本机 claude 配的是第三方 kimi-for-coding 供应商，授权头转发 api.anthropic.com 必然 401（本机配置限制，非 jev-router 缺陷）
4. `--model jev-router` 强制哨兵 + mock 服务器已退出（模拟 Jev 宕机）：日志 `[jev] rewrite jev-router -> claude-opus-5`——fail-open 退最安全默认档，会话不阻塞
- 坑：Jev 不在 OpenRouter /models 列表（工具枚举看不到它）；路由要把用户 prompt 发 TypeSafe 云端（隐私掂量）；官方"快193倍/便宜444倍"为厂商自宣未独立验证
- 判例注：拾遗主池 604727ff 已判 Jev 闭源本体非学习类（白名单+无开源载体不能动手）；本条因推文对应的 jev-router 开源路由框架可 clone 可跑测试可实测 fail-open 而判学习类，两条判例互补不冲突

**后续可深入的方向**：OpenRouter 充 $1 换真裁判实测真实延迟/省钱比；jev-mcp/jev-review 给 Agent 加裁判工具；把哨兵代理范式移植到其他 CLI；TypeSafe 官方 composite-scoring 机筛简历案例。

源头：https://x.com/GeekCatX/status/2100956459580395585（知识猫AI实验室，28 玩法聚合帖）
产出：`jev-router/jev-router-小白指南.pdf`（12 问 6 步实验，Edge 无头打印 1.14MB）
