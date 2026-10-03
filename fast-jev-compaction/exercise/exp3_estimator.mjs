// exp3 — 亲手验证无分词器 token 估算器的校准逻辑：
// 为什么不用 chars/4？README：JSON 重度状态按比例估会少算最多 40%。
// 运行：node exp3_estimator.mjs
import { estimateTokens } from './replica.mjs';

const samples = [
  ['英文散文', 'The assistant read the test file and ran the full test suite before editing the module.'],
  ['中文文本', '修复失败的测试用例，先读源码再跑完整测试套件，最后才动手改模块。'],
  ['JSON 工具输入', JSON.stringify({ file_path: 'src/auth.test.ts', limit: 200, offset: 1, command: 'npm test --filter auth' })],
  ['混合行（代码）', 'const result = await compact(messages, asker, { maxStateTokens: 25_000 }); // t12 Read → ok 480ch'],
  ['纯数字串', '20260918 3600 42'],
  ['重复符号', 'x'.repeat(60)],
];

console.log('sample            | chars | estimateTokens | chars/4 | 差距');
for (const [name, text] of samples) {
  const est = estimateTokens(text);
  const byRatio = Math.ceil(text.length / 4);
  console.log(
    `${name.padEnd(16)} | ${String(text.length).padStart(5)} | ${String(est).padStart(14)} | ${String(byRatio).padStart(7)} | ${(((est - byRatio) / byRatio) * 100).toFixed(0)}%`,
  );
}

// JSON 重度状态：大量标点/引号/花括号，每个符号 0.9 token，比 chars/4 贵一倍多
const stateLike = JSON.stringify({
  context: 'A coding assistant conversation is being compacted '.repeat(8),
  goal: 'fix tests',
  history: Array.from({ length: 20 }, (_, i) => ({
    i,
    role: 'assistant',
    text: 'step',
    tool_calls: [{ id: `t${i}`, tool: 'Read', input: '{"file_path":"src/a.ts"}', result: 'ok, 4213 chars (omitted)' }],
  })),
});
const est = estimateTokens(stateLike);
const byRatio = Math.ceil(stateLike.length / 4);
console.log('\nJSON 重度 state 样本:');
console.log(`chars=${stateLike.length} estimateTokens=${est} chars/4=${byRatio} → chars/4 少算 ${(((est - byRatio) / est) * 100).toFixed(0)}%（README 声称最多 40%）`);
// 估算器校准方向：声称比 Jev 真实计数高 2-18%（宁高勿低，防止请求超限）
console.log('估算器设计取向：宁高勿低（高估 → 提前分批/降级，不会撞 32k 请求上限）');
