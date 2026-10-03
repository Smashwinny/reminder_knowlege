// exp1 — 亲手验证 fitState 的 8 档阶梯降级：预算逐步收紧，看每一档何时触发，
// 以及最后一档仍塞不下时的"保险丝"（throw）。运行：node exp1_fit_state_ladder.mjs
import { collectToolCalls, fitState } from './replica.mjs';

// 合成一份 40 条消息的编码会话：开头用户约束、中段大量旧读写、结尾几条新消息。
const filler = (n) => 'x'.repeat(n);
const messages = [
  {
    role: 'user',
    text: 'Fix the failing test in src/auth. Never edit src/generated. Run npm test before you finish.',
    toolUses: [],
  },
];
for (let i = 0; i < 16; i++) {
  messages.push({
    role: 'assistant',
    text: `Step ${i}: reading the module and running checks. ${filler(900)}`,
    toolUses: [{ tool_use_id: `u${i}`, tool: 'Read', input: { file_path: `src/mod_${i}.ts` } }],
  });
  messages.push({
    role: 'user',
    text: '',
    toolUses: [],
    toolResults: [{ tool_use_id: `u${i}`, text: `export function mod${i}() { ${filler(1500)} }` }],
  });
}
for (let i = 0; i < 3; i++) {
  messages.push({ role: 'assistant', text: `Recent step ${i}.`, toolUses: [] });
}
messages.push({
  role: 'assistant',
  text: 'Now editing the auth module.',
  toolUses: [{ tool_use_id: 'uLast', tool: 'Edit', input: { file_path: 'src/auth.ts' } }],
});
messages.push({
  role: 'user',
  text: '',
  toolUses: [],
  toolResults: [{ tool_use_id: 'uLast', text: 'The file has been updated. Tests pass.' }],
});

const calls = collectToolCalls(messages, 6);
const candidates = calls.filter((c) => !c.pinned);
console.log(
  `transcript: ${messages.length} messages, ${calls.length} tool calls, ${candidates.length} candidates (pinned ${calls.length - candidates.length})`,
);
console.log('budget(tok) | stage reached              | state tok');
for (const budget of [1e9, 8_000, 4_000, 2_500, 1_500, 1_100, 900, 700, 500, 300]) {
  try {
    const f = fitState(messages, calls, { maxStateTokens: budget, preserveRecentMessages: 6 });
    console.log(
      `${String(Math.round(budget)).padStart(10)} | ${f.stage.padEnd(26)} | ${f.tokens}`,
    );
  } catch (e) {
    console.log(`${String(Math.round(budget)).padStart(10)} | THREW (保险丝)            | ${e.message}`);
  }
}

// 场景 B：全 call-only 消息（text 全空）→ 触发最后两档 left out / merged
console.log('\n场景 B（call-only 消息串）:');
const msgsB = [{ role: 'user', text: 'grep the repo for TODOs', toolUses: [] }];
for (let i = 0; i < 30; i++) {
  msgsB.push({
    role: 'assistant',
    text: '',
    toolUses: [{ tool_use_id: `b${i}`, tool: 'Grep', input: { pattern: 'TODO', path: `src/pkg${i}` } }],
  });
  msgsB.push({
    role: 'user',
    text: '',
    toolUses: [],
    toolResults: [{ tool_use_id: `b${i}`, text: 'src/pkg' + i + '/a.ts: TODO fix me' + 'q'.repeat(120) }],
  });
}
const callsB = collectToolCalls(msgsB, 2);
for (const budget of [6000, 4500, 3000, 2000, 1200]) {
  try {
    const f = fitState(msgsB, callsB, { maxStateTokens: budget, preserveRecentMessages: 2 });
    console.log(`${String(budget).padStart(6)} | ${f.stage.padEnd(26)} | ${f.tokens}`);
  } catch (e) {
    console.log(`${String(budget).padStart(6)} | THREW (保险丝)            | ${e.message}`);
  }
}
