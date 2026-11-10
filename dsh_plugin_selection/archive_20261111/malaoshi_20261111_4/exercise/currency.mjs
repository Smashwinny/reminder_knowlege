// Original source: https://github.com/Han-1413141/dsh-cost-meter/blob/c876735d80760fc89d88fa99c19c90c56e984c23/lib/pricing.js
// Real pinned pricing.js:770-825,1398-1418. Synthetic prices/exchange rate only.
import assert from 'node:assert/strict';const {normalizePrice,costOf,usdFromCost,formatMoney}=await import('./upstream/dsh-cost-meter/lib/pricing.js');
const p=normalizePrice({input:2,output:8,multiplier:.8});assert.deepEqual(normalizePrice(p),p);
assert.equal(costOf({input:1e6},p),1.6);console.log('multiplier: raw input=2; factor=.8; effective cost=1.6; renormalize unchanged');
assert.equal(usdFromCost(7.2,'CNY',7.2),1);assert.equal(formatMoney(1,{symbol:'¥',exchangeRate:7.2,decimals:2}),'¥7.2');console.log('currency: synthetic CNY 7.2 -> USD 1 -> display ¥7.2');
assert.equal(normalizePrice({}),null);assert.deepEqual(normalizePrice({unpriced:true}),{unpriced:true});console.log('unknown price: {} -> null; explicit unpriced retained (not evidence of free use)');
for(const multiplier of [-1,Infinity,'0.5'])assert.equal(normalizePrice({input:2,output:8,multiplier}),null);
assert.equal(costOf({input:1e6},normalizePrice({input:2,output:8,multiplier:0})),0);console.log('negative/infinite/string multipliers rejected; explicit factor=0 computes 0');
assert.equal(globalThis.__networkAttempts.length,0);console.log('PASS: multiplier/currency/unknown validation; network attempts=0; not a bill or quota test');
