// Original source: https://github.com/Han-1413141/dsh-cost-meter/blob/c876735d80760fc89d88fa99c19c90c56e984c23/lib/pricing.js
// Real upstream implementation: Han-1413141/dsh-cost-meter c876735d80760fc89d88fa99c19c90c56e984c23 lib/pricing.js:1366-1384
import assert from 'node:assert/strict';
const {normalizePrice,costOf}=await import('./upstream/dsh-cost-meter/lib/pricing.js');
const at=Date.parse('2026-11-10T10:00:00+08:00');
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-10,`${a} != ${b}`);
const p=normalizePrice({cacheMiss:2,cacheHit:.5,cacheWrite:3,output:8});
const cases=[['four buckets',{input:100000,cacheRead:50000,cacheWrite:10000,output:20000},p,.415],['one million input',{input:1e6},p,2],['fallback write rate',{cacheWrite:1e6},normalizePrice({cacheMiss:2,cacheHit:.5,output:8}),.5],['invalid token amounts',{input:-2,output:Infinity,cacheRead:NaN},p,0]];
for(const [label,tokens,price,want] of cases){const got=costOf(tokens,price,at);near(got,want);console.log(JSON.stringify({label,tokens,got,want}));}
assert.equal(globalThis.__networkAttempts.length,0);console.log('PASS: 4 synthetic cost scenarios; network attempts=0; rates are fixtures, not market prices');
