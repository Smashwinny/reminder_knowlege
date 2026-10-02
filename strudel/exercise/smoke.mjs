import { sequence } from '@strudel/core';
import { mini } from '@strudel/mini';
const p = sequence('a', ['b', 'c']);
console.log(p.queryArc(0, 1).map(e => `${e.value}: ${e.whole.begin.toFraction()} - ${e.whole.end.toFraction()}`).join('\n'));
console.log('---');
const m = mini('c a f e');
console.log(m.queryArc(0, 1).map(e => JSON.stringify(e.value)).join('\n'));
