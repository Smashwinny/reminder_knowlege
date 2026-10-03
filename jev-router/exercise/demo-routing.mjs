// demo-routing.mjs — 用"本地假 Jev"驱动 jev-router 的真实决策代码
// 调用 repo 里真实的 askJev()（router.mjs，走 @typesafe-ai/sdk 真实 HTTP 请求）
// 和真实的 decide()（policy.mjs），观察四种场景下路由器怎么选模型。
//
// 前置: node mock-jev-server.mjs 8377   （另开一个终端）
// 运行: node demo-routing.mjs
import { askJev } from "../repo/src/router.mjs";
import { decide, detectOverride } from "../repo/src/policy.mjs";

const MODELS = [
  { id: "claude-haiku-4-5-20251001", tier: "haiku" },
  { id: "claude-sonnet-5", tier: "sonnet" },
  { id: "claude-opus-5", tier: "opus" },
];
const AVAILABLE = ["haiku", "sonnet", "opus"];

const scenarios = [
  { prompt: "what is 2+2?", note: "琐碎问答，期望路由到 haiku" },
  { prompt: "write a unit test for the parse function", note: "普通工程任务，期望 sonnet" },
  { prompt: "refactor everything: redesign the architecture for concurrency", note: "高难度任务，期望 opus" },
  { prompt: "uncertain legacy bug, maybe fix it", note: "Jev 置信度仅 0.10，期望被策略钳制（不许降级、升级封顶 sonnet）" },
  { prompt: "use opus to audit the auth module", note: "人类点名 opus，期望 override 生效" },
];

console.log("场景 | Jev 原始选择(置信度) | 策略最终决定 | 理由 | 耗时");
console.log("---|---|---|---|---");
for (const s of scenarios) {
  const jev = await askJev({ prompt: s.prompt, current: "sonnet", contextTokens: 3000, models: MODELS });
  const chosen = MODELS.find((m) => m.id === jev?.choice);
  const tierAnswer = jev && { ...jev, choice: chosen?.tier };
  const override = detectOverride(s.prompt);
  const { tier, reason } = decide({
    prompt: s.prompt,
    jev: override ? null : tierAnswer,
    current: "sonnet",
    available: AVAILABLE,
    contextTokens: 3000,
  });
  if (override) {
    console.log(`${JSON.stringify(s.prompt)} | (人类点名 ${override}) | ** ${override} ** | explicit-override | -`);
  } else {
    console.log(`${JSON.stringify(s.prompt)} | ${jev ? `${chosen?.tier ?? jev.choice} (${jev.confidence})` : "Jev 不可用"} | ** ${tier} ** | ${reason} | ${jev?.ms}ms`);
  }
}
