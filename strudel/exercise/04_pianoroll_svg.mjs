// 辅助脚本：把歌曲 pattern 的真实事件渲染成钢琴roll SVG（嵌入 PDF 用）
import { mini } from '@strudel/mini';
import { stack } from '@strudel/core';
import { writeFileSync } from 'node:fs';

const song = stack(
  mini('bd ~ bd ~ bd ~ bd bd'),
  mini('~ sd ~ sd ~ sd ~ sd'),
  mini('hh*8'),
  mini('<c3 e3 g3> <a2 c3 e3> <f2 a2 c3> <g2 b2 d3>'),
  mini('<c2 g1>*2 <a1 f1>*2'),
);
const haps = song.queryArc(0, 4);
const NOTE_RE = /^([a-g])([#b]?)(\d)$/;
const SEMI = { c: 0, d: 2, e: 4, f: 5, g: 7, a: 9, b: 11 };
const W = 760, LANE_H = 46, TOP = 30, LEFT = 60;
const lanes = { bd: 0, sd: 1, hh: 2, chord: 3, bass: 4 };
const colors = { bd: '#e91e63', sd: '#ff9800', hh: '#ffd600', chord: '#00bcd4', bass: '#7c4dff' };
let out = [];
for (const h of haps) {
  const v = typeof h.value === 'object' ? String(h.value.note ?? '') : String(h.value);
  const b = Number(h.whole.begin), e = Number(h.whole.end);
  let lane, label, y, hh;
  if (lanes[v] !== undefined) { lane = lanes[v]; label = v; }
  else {
    const m = NOTE_RE.exec(v);
    const midi = (Number(m[3]) + 1) * 12 + SEMI[m[1]];
    lane = midi < 48 ? 4 : 3;
    label = v;
  }
  y = TOP + lane * LANE_H;
  const x = LEFT + (b / 4) * (W - LEFT - 10);
  const w = Math.max(6, ((e - b) / 4) * (W - LEFT - 10) - 2);
  hh = LANE_H - 14;
  out.push(`<rect x="${x.toFixed(1)}" y="${y}" width="${w.toFixed(1)}" height="${hh}" rx="5" fill="${colors[lane === 3 ? 'chord' : lane === 4 ? 'bass' : v]}" opacity="0.92"/><text x="${(x + 3).toFixed(1)}" y="${y + hh - 6}" font-size="11" fill="#1a1a2e" font-weight="bold" font-family="Segoe UI">${label}</text>`);
}
const gridX = [0, 1, 2, 3].map((c) => `<line x1="${LEFT + (c / 4) * (W - LEFT - 10)}" y1="${TOP - 8}" x2="${LEFT + (c / 4) * (W - LEFT - 10)}" y2="${TOP + 5 * LANE_H}" stroke="#bbb" stroke-dasharray="4 4"/>`).join('');
const laneLabels = ['底鼓 bd', '军鼓 sd', '踩镲 hh', '琶音', '贝斯'].map((t, i) => `<text x="8" y="${TOP + i * LANE_H + 28}" font-size="13" fill="#333" font-family="Segoe UI">${t}</text>`).join('');
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${TOP + 5 * LANE_H + 10}" viewBox="0 0 ${W} ${TOP + 5 * LANE_H + 10}"><rect width="${W}" height="100%" fill="#fafaff"/>${gridX}${laneLabels}${out.join('')}</svg>`;
writeFileSync('pianoroll.svg', svg);
console.log(`pianoroll.svg 写出，共 ${haps.length} 个事件块`);
