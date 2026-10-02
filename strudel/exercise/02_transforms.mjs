// 实验3：pattern 变换 —— 函数式音乐：同一个 pattern 经变换产生新 pattern
import { mini } from '@strudel/mini';
import { stack } from '@strudel/core';

const base = mini('bd sd hh cp');

function dump(name, p, cycles = 2) {
  let total = 0;
  const lines = [];
  for (let c = 0; c < cycles; c++) {
    const haps = p.queryArc(c, c + 1);
    total += haps.length;
    lines.push(
      `  cycle ${c}: ` +
        haps.map((h) => `${h.value}@${(Number(h.whole.begin) - c).toFixed(2)}`).join(' '),
    );
  }
  console.log(`【${name}】 ${cycles} 循环共 ${total} 个事件`);
  lines.forEach((l) => console.log(l));
}

dump('原样 base', base);
dump('.fast(2) 加倍速', base.fast(2));
dump('.slow(2) 减半速', base.slow(2));
dump('.rev() 倒放', base.rev());
dump('.add(3) 整体移调', mini('c a f e').add(3));

// stack 叠层：鼓 + 贝斯 + 旋律 = 一首歌的骨架
const song = stack(
  mini('bd ~ sd ~ bd ~ sd ~'),        // 鼓
  mini('hh*8'),                        // 踩镲
  mini('<c2 c2 g1 g1 a1 a1 f1 f1>').add(0), // 贝斯音
);
dump('stack(鼓,镲,贝斯)', song, 2);
