// Original source: https://github.com/Han-1413141/dsh-cost-meter/blob/c876735d80760fc89d88fa99c19c90c56e984c23/lib/pricing.js
// Same pinned pricing.js:1324-1384; self-written boundary scenarios, NOT upstream test suite.
import assert from 'node:assert/strict';const {normalizePrice,costOf}=await import('./upstream/dsh-cost-meter/lib/pricing.js');
const p=normalizePrice({cacheMiss:2,cacheHit:1,output:8,longContext:{aboveInputTokens:200000,cacheMiss:4,cacheHit:2,output:16}});
const at=Date.parse('2026-11-10T10:00:00+08:00');const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-10);
const cases=[['exactly threshold',{input:200000},.4],['one above',{input:200001},.800004],['cache participates',{input:100000,cacheRead:100001},.600002],['output excluded from threshold',{input:1,output:300000},2.400002]];
for(const[label,t,want]of cases){const got=costOf(t,p,at);near(got,want);console.log(JSON.stringify({label,got,want}));}
const separate=2*costOf({input:125000},p,at),aggregated=costOf({input:250000},p,at);near(separate,.5);near(aggregated,1);assert.notEqual(separate,aggregated);
console.log(JSON.stringify({counterexample:'sum two per-call charges, not aggregate tokens then charge',separate,aggregated}));
assert.equal(globalThis.__networkAttempts.length,0);console.log('PASS: 4 boundaries + aggregation counterexample; network attempts=0');
