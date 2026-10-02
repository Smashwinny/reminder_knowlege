// 实验2：mini-notation 节奏语言 —— 一行字符串描述一段鼓点
import { mini } from '@strudel/mini';

function show(name, code, cycles = 2) {
  const p = mini(code);
  console.log(`\n【${name}】 mini("${code}")`);
  for (let c = 0; c < cycles; c++) {
    const haps = p.queryArc(c, c + 1);
    const line = haps
      .map((h) => {
        const begin = +h.whole.begin.toFraction ? +h.whole.begin - c : +h.whole.begin - c;
        const b = Number(h.whole.begin) - c;
        const e = Number(h.whole.end) - c;
        const v = typeof h.value === 'object' ? JSON.stringify(h.value) : h.value;
        return `${v}@${b.toFixed(2)}~${e.toFixed(2)}`;
      })
      .join('  ');
    console.log(`  cycle ${c}: ${line}`);
  }
  console.log(`  → 第1循环共 ${p.queryArc(0, 1).length} 个事件`);
}

show('基础序列', 'bd sd bd sd');
show('休止符 ~', 'bd ~ sd ~');
show('重复 *', 'bd*2 sd hh*4', 1);
show('分组 []', '[bd sd] hh*2', 1);
show('交替 <>', '<bd sd> hh', 2);
show(' alt(3,8) 欧几里得节奏', 'bd(3,8)', 1);
show('音符旋律', 'c a f e', 1);
show('带八度与和弦进行', '<c3 e3 g3> <a2 c3 e3>', 2);
