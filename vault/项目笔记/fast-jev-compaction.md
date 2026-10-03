---
tags: [项目]
类别: 开源项目类
上游仓库: https://github.com/tamaratran/fast-jev-compaction (MIT, 7339★)
完成日期: 2026-10-03
---

# fast-jev-compaction

**这是什么**（一句话）：Claude Code 的"记忆手术刀"插件 + npm 库——用 Jev 决策替代内置 compaction 摘要：每次工具调用/结果被打两个置信分（keepCall/keepResult），有用的逐字留、没用的整条删、中间态截 300 字符加 `re-run` 注记；用户/助手文本永不改写。

**它给我什么能力**：长任务不再越跑越失忆（约束/报错/路径不蒸发）；可移植的"决策式压缩"范式（`compactMessages` 库任何 Agent 都能用）；"JevAsker 接缝 + mock"零 API 教具路线；function hooks（2.1.274+ 早期特性）双挂点实战样例。

**引入的概念**：
- [[决策式无损压缩]]（第三流派：只做减法不做改写；双问题置信评估）
- [[阶梯降级与保险丝]]（fitState 8 档能塞就停 + 塞不下 throw 回退；宁高勿低 token 估算）

**实验记录**（2026-10-03，全部真实运行，Node v24.21.0 纯零依赖复刻）：
1. **坑**：上游 `npm install`/`npm test` 被本机安全策略拦（Code from External），按先例如实记录，改 `exercise/replica.mjs` 忠实复刻上游 MIT 算法（estimateTokens/fitState/compact 全函数转写）+ 3 驱动脚本。
2. exp1 阶梯降级：38 消息/17 调用合成会话，预算 8000→full(4367tok)、4000→texts abridged、2500→old messages collapsed、1500→old calls compacted、≤1100→保险丝 throw；场景 B（call-only 串）1200→old calls merged。8 档实证 7 档+保险丝（唯 left out 档未触发，如实标注）。
3. exp2 mock Jev 全流程：t1 Read 测试文件 .9/.95→kept 逐字保留（含 `at auth.test.ts:42`）；t2 npm test .8/.2→drop_result 截留；t3 空手 WebSearch .1/.05→drop_call 整删；t4 钉扎区→pinned。不变量 5/5 ✅（无孤儿结果/用户文本一字不动/压缩率 51.9%）。对照传统摘要："Never edit src/generated"与".env.ci token"两条约束全丢。
4. exp3 估算器：中文 chars/4 少算 263%、JSON 重度 state 少算 51%（README 称最多 40%，方向一致）、英文散文估高 14%→宁高勿低。
- 复刻首跑坑：askBatch 忘取 `.noul` 数值致 t1 误判整删——恰证明上游 noulAnswer 严格校验 + throw 的价值（畸形答案比压缩失败更危险）。
- 判例注：源头推文（KK.aWSB Jev 推荐帖）本体指向 TypeSafe 闭源 Jev（主池 604727ff 已判非学习类），但其"开源插件压缩上下文"指向本仓库（独立于已学 jev-router），故判学习类深挖。

**后续可深入的方向**：充 key 实测真实 Jev 打分 vs 我 mock 剧本的差距；把双问题模式移植到聊天记录归档/日志治理；`demo/JevDemo`（SwiftUI 演示 app，仅 macOS）。

源头：https://x.com/KKaWSB/status/2101043826714661033
产出：`fast-jev-compaction/fast-jev-compaction-小白指南.pdf`（12 问 3 实验，Edge 无头打印 1.72MB）
