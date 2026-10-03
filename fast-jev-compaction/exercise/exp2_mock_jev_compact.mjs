// exp2 — 用 mock Jev（程序化打分，零 API）驱动完整 compact 主流程，
// 验证三分支决策矩阵、钉扎保护、孤儿结果禁令、逐字保留 vs 有损摘要。
// 运行：node exp2_mock_jev_compact.mjs
import { compact, reductionRatio, resolveOptions, batchCalls, questionsFor } from './replica.mjs';
import { estimateTokens } from './replica.mjs';

// ---- 会话：一条含关键约束的用户指令 + 4 次工具调用（新旧、重要/过时混合）----
const FILE = 'src/generated/tables.ts'; // 生成的代码：内容没用，但"改过它"这件事重要
const messages = [
  {
    role: 'user',
    text: 'Fix the failing test. Never edit src/generated. The CI token lives in .env.ci, do not print it.',
    toolUses: [],
  },
  {
    role: 'assistant',
    text: '',
    toolUses: [{ tool_use_id: 't1', tool: 'Read', input: { file_path: 'src/auth.test.ts' } }],
  },
  {
    role: 'user',
    text: '',
    toolUses: [],
    toolResults: [
      {
        tool_use_id: 't1',
        text: 'assertEqual(session.ttl, 3600)\n> expected 3600 got 60\n  at auth.test.ts:42',
      },
    ],
  },
  {
    role: 'assistant',
    text: '',
    toolUses: [{ tool_use_id: 't2', tool: 'Bash', input: { command: 'npm test 2>&1 | tail -20' } }],
  },
  {
    role: 'user',
    text: '',
    toolUses: [],
    toolResults: [
      { tool_use_id: 't2', text: 'FAIL src/auth.test.ts\n1 failed, 18 passed\nTTL mismatch: 60 != 3600' },
    ],
  },
  {
    role: 'assistant',
    text: '',
    toolUses: [
      { tool_use_id: 't3', tool: 'WebSearch', input: { query: 'claude code session ttl default' } },
    ],
  },
  {
    role: 'user',
    text: '',
    toolUses: [],
    toolResults: [
      { tool_use_id: 't3', text: 'Search results: (10 links about unrelated defaults) ' + 'y'.repeat(2400) },
    ],
  },
  {
    role: 'assistant',
    text: '',
    toolUses: [{ tool_use_id: 't4', tool: 'Edit', input: { file_path: FILE, old: 'ttl: 60', new: 'ttl: 3600' } }],
  },
  {
    role: 'user',
    text: '',
    toolUses: [],
    toolResults: [{ tool_use_id: 't4', text: 'The file ' + FILE + ' has been updated. ' + 'z'.repeat(1800) }],
  },
  { role: 'assistant', text: 'Fixed the TTL. Running the full suite now.', toolUses: [] },
  { role: 'user', text: 'Good. Now also check the refresh-token path.', toolUses: [] },
];

// ---- mock Jev：按"语义剧本"打分（真实服务会给出类似形状的概率）----
// t1 Read 测试文件：结果仍有用（失败栈要看原文）→ keep
// t2 npm test：结论已进对话文本，原始输出不必逐字留 → 截留头部
// t3 WebSearch：查的东西没派上用场，连"查过"都不重要 → 整删
// t4 Edit 生成文件：内容无所谓（重跑/重读都行）但"动过 src/generated"重要 → 截留头部
const script = {
  t1: { keepCall: 0.9, keepResult: 0.95 },
  t2: { keepCall: 0.8, keepResult: 0.2 },
  t3: { keepCall: 0.1, keepResult: 0.05 },
  t4: { keepCall: 0.85, keepResult: 0.15 },
};
const asker = {
  async ask(state, questions) {
    const names = Object.keys(questions);
    const answers = {};
    for (const name of names) {
      const callId = name.replace(/^(call|result)_/, '');
      answers[name] = { noul: name.startsWith('call_') ? script[callId].keepCall : script[callId].keepResult };
    }
    // 观察：每个请求都带完整 state；state 里旧结果已被换成 note
    console.log(
      `[mock Jev] request: ${names.length} questions, state ~${estimateTokens(JSON.stringify(state))} tok, goal="${state.goal.slice(0, 40)}..."`,
    );
    return { answers };
  },
};

const result = await compact(messages, asker, { preserveRecentMessages: 4 });
const opts = resolveOptions({ preserveRecentMessages: 4 });

console.log('\n=== 决策 ===');
for (const d of result.decisions) {
  console.log(
    `${d.id} ${d.tool.padEnd(10)} action=${d.action.padEnd(12)} keepCall=${d.keepCall} keepResult=${d.keepResult} reason=${d.reason}`,
  );
}
console.log('\n=== stats ===');
const s = result.stats;
console.log(
  `messages ${s.messagesBefore}->${s.messagesAfter} | chars ${s.charsBefore}->${s.charsAfter} (reduction ${(reductionRatio(result) * 100).toFixed(1)}%)`,
);
console.log(`kept=${s.kept} resultsDropped=${s.resultsDropped} callsDropped=${s.callsDropped} pinned=${s.pinned} | state=${s.stateTokens}tok stage=${s.stateStage} | ${s.requests} request(s) ${s.ms}ms`);

console.log('\n=== 断言（不变量） ===');
const flat = (ms) => ms.flatMap((m) => [...m.toolUses, ...(m.toolResults ?? [])].map((t) => t.tool_use_id));
const after = new Set(flat(result.messages));
const orphans = [...after].filter(
  (id) => after.has(id) && !result.messages.some((m) => m.toolUses.some((t) => t.tool_use_id === id)),
);
console.log(`orphan results (result without call): ${orphans.length === 0 ? '0 ✅' : orphans.join(',') + ' ❌'}`);
const searchGone = !flat(result.messages).includes('t3');
console.log(`t3 (WebSearch) 连调用带结果整体消失: ${searchGone ? '✅' : '❌'}`);
const t1msg = result.messages.find((m) => m.toolResults?.some((r) => r.tool_use_id === 't1'));
const t1verbatim = t1msg.toolResults.find((r) => r.tool_use_id === 't1').text.includes('at auth.test.ts:42');
console.log(`t1 结果逐字保留（含行号细节）: ${t1verbatim ? '✅' : '❌'}`);
const firstUserIntact = result.messages[0].text === messages[0].text;
console.log(`用户文本永不改写（约束原文一字不动）: ${firstUserIntact ? '✅' : '❌'}`);
const pinnedT4 = result.messages.some((m) => flat([m]).includes('t4'));
console.log(`t4 处于钉扎区（最后 4 条）→ action=keep/pinned: ${result.decisions.find((d) => d.id === 't4').reason === 'pinned' ? '✅' : '❌'}`);

console.log('\n=== 对照：有损摘要把关键约束弄丢 ===');
const naiveSummary =
  'User asked to fix a failing test. The assistant read the test file, ran the test suite, searched the web, edited a file, and fixed the TTL issue.';
console.log(`约束"Never edit src/generated"在逐字压缩后仍在: ${result.messages[0].text.includes('Never edit src/generated') ? '✅' : '❌'}`);
console.log(`同一约束在传统摘要里: ${naiveSummary.includes('Never edit src/generated') ? '在' : '丢了 ❌（下轮就可能再犯）'}`);
console.log(`CI token 约束在摘要里: ${naiveSummary.includes('.env.ci') ? '在' : '丢了 ❌'}`);
