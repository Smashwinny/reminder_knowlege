// Original source: https://github.com/f-e-n-g-0531/dsh-code-review/blob/0d3f6b03f9080153cc01fb8b75a79ddcbcae86d4/src/model-approval.mjs
// Source: f-e-n-g-0531/dsh-code-review 0d3f6b03f9080153cc01fb8b75a79ddcbcae86d4 src/model-approval.mjs
// Personal non-commercial learning only. Full custom license bundled. Fake host authority; no model call.
import assert from 'node:assert/strict';const {requestModelApproval}=await import('./upstream/review-feng/src/model-approval.mjs');
assert.equal(await requestModelApproval({request:async()=> 'allowed-once'},{}),true);console.log('allowed-once -> accepted');
for(const result of ['rejected','cancelled','unavailable',true,undefined]){await assert.rejects(()=>requestModelApproval({request:async()=>result},{}));console.log(JSON.stringify({result:result??'<undefined>',accepted:false}));}
await assert.rejects(()=>requestModelApproval(undefined,{}),/missing/);console.log('missing approval service -> rejected');
assert.equal(globalThis.__networkAttempts.length,0);console.log('PASS: 7 mock-host approval outcomes; network attempts=0; not real host authorization or code review');
