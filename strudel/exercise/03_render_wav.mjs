// 实验4（主实验高潮）：把 Strudel pattern 渲染成真正可听的 .wav 文件
// 思路：pattern.queryArc() 拿到事件（何时、什么音）→ 用 Node 纯手写合成器填样本 → 写 WAV
import { mini } from '@strudel/mini';
import { stack } from '@strudel/core';
import { WriteStream } from 'node:fs';
import { Buffer } from 'node:buffer';

const SR = 44100;              // 采样率
const CYCLE = 1.5;             // 每循环秒数（Strudel 网页版默认约 2s，这里取 1.5 更带感）
const CYCLES = 4;              // 渲染 4 个循环
const DUR = SR * CYCLE * CYCLES;

// ---------- 1. 用 Strudel 写"谱子" ----------
const song = stack(
  mini('bd ~ bd ~ bd ~ bd bd'),                  // 底鼓
  mini('~ sd ~ sd ~ sd ~ sd'),                   // 军鼓（2、4拍）
  mini('hh*8'),                                  // 踩镲八连
  mini('<c3 e3 g3> <a2 c3 e3> <f2 a2 c3> <g2 b2 d3>'), // 和弦琶音
  mini('<c2 g1>*2 <a1 f1>*2'),                   // 贝斯（每半循环一个音）
);

// ---------- 2. 拿事件 ----------
const haps = song.queryArc(0, CYCLES);
console.log(`pattern 共 ${haps.length} 个事件，开始渲染 ${CYCLES} 循环 × ${CYCLE}s = ${CYCLE * CYCLES}s ...`);

// ---------- 3. 简易合成器 ----------
const buf = new Float32Array(DUR);

function addKick(t) {           // 底鼓：正弦从 130Hz 滑到 45Hz + 指数衰减
  const len = 0.28 * SR;
  for (let i = 0; i < len; i++) {
    const idx = (t * SR + i) | 0;
    if (idx >= DUR) break;
    const p = i / len;
    const f = 45 + 85 * Math.exp(-p * 9);
    buf[idx] += 0.9 * Math.sin((2 * Math.PI * f * i) / SR) * Math.exp(-p * 6);
  }
}
function addHat(t, open = false) { // 踩镲：白噪声短爆发
  const len = (open ? 0.18 : 0.05) * SR;
  for (let i = 0; i < len; i++) {
    const idx = (t * SR + i) | 0;
    if (idx >= DUR) break;
    buf[idx] += 0.25 * (Math.random() * 2 - 1) * Math.exp((-4 * i) / len);
  }
}
function addSnare(t) {          // 军鼓：噪声 + 180Hz 主体
  const len = 0.18 * SR;
  for (let i = 0; i < len; i++) {
    const idx = (t * SR + i) | 0;
    if (idx >= DUR) break;
    const env = Math.exp((-5 * i) / len);
    buf[idx] += (0.35 * (Math.random() * 2 - 1) + 0.3 * Math.sin((2 * Math.PI * 180 * i) / SR)) * env;
  }
}
const NOTE_RE = /^([a-g])([#b]?)(\d)?$/;
const SEMI = { c: 0, d: 2, e: 4, f: 5, g: 7, a: 9, b: 11 };
function noteFreq(v) {          // 'c3' / 'f#2' → Hz（A4=440）
  const name = typeof v === 'object' && v !== null ? (v.note ?? v.n ?? '') : v;
  const m = NOTE_RE.exec(String(name).trim().toLowerCase());
  if (!m) return null;
  let midi = (m[3] ? +m[3] + 1 : 5) * 12 + SEMI[m[1]] + (m[2] === '#' ? 1 : m[2] === 'b' ? -1 : 0);
  return 440 * Math.pow(2, (midi - 69) / 12);
}
function addTone(t, freq, dur, vol, kind) { // 琶音/贝斯：谐波+包络
  const len = dur * SR;
  for (let i = 0; i < len; i++) {
    const idx = (t * SR + i) | 0;
    if (idx >= DUR) break;
    const env = Math.min(1, i / (0.01 * SR)) * Math.exp((-3 * i) / len);
    const ph = (2 * Math.PI * freq * i) / SR;
    const s = Math.sin(ph) + (kind === 'bass' ? 0.5 * Math.sin(2 * ph) : 0.3 * Math.sin(2 * ph) + 0.15 * Math.sin(3 * ph));
    buf[idx] += vol * s * env;
  }
}

// ---------- 4. 逐事件填样本 ----------
let counts = { bd: 0, sd: 0, hh: 0, chord: 0, bass: 0 };
for (const h of haps) {
  const t = Number(h.whole.begin) * CYCLE;
  const v = h.value;
  const name = typeof v === 'object' && v !== null ? String(v.note ?? '') : String(v);
  if (name === 'bd') { addKick(t); counts.bd++; }
  else if (name === 'sd') { addSnare(t); counts.sd++; }
  else if (name === 'hh') { addHat(t, Number(h.whole.begin) % 1 > 0.875); counts.hh++; }
  else {
    const f = noteFreq(v);
    if (f == null) continue;
    const d = Math.max(0.12, (Number(h.whole.end) - Number(h.whole.begin)) * CYCLE);
    if (f < 120) { addTone(t, f, d, 0.5, 'bass'); counts.bass++; }
    else { addTone(t, f, d, 0.3, 'chord'); counts.chord++; }
  }
}

// ---------- 5. 削波保护 + 写 WAV（16bit PCM mono）----------
let peak = 0;
for (let i = 0; i < DUR; i++) peak = Math.max(peak, Math.abs(buf[i]));
const gain = peak > 0 ? Math.min(1, 0.89 / peak) : 1;
const data = Buffer.alloc(DUR * 2);
for (let i = 0; i < DUR; i++) data.writeInt16LE(Math.round(buf[i] * gain * 32767), i * 2);
const header = Buffer.alloc(44);
header.write('RIFF', 0); header.writeUInt32LE(36 + data.length, 4); header.write('WAVE', 8);
header.write('fmt ', 12); header.writeUInt32LE(16, 16); header.writeUInt16LE(1, 20);
header.writeUInt16LE(1, 22); header.writeUInt32LE(SR, 24); header.writeUInt32LE(SR * 2, 28);
header.writeUInt16LE(2, 32); header.writeUInt16LE(16, 34);
header.write('data', 36); header.writeUInt32LE(data.length, 40);
const { writeFileSync, statSync } = await import('node:fs');
writeFileSync('strudel_jam.wav', Buffer.concat([header, data]));
const kb = (statSync('strudel_jam.wav').size / 1024).toFixed(1);
console.log(`✅ strudel_jam.wav 生成：${kb} KB，${(DUR / SR).toFixed(1)} 秒，峰值 ${peak.toFixed(2)}（归一化增益 ${gain.toFixed(2)}）`);
console.log(`   渲染统计：底鼓×${counts.bd} 军鼓×${counts.sd} 踩镲×${counts.hh} 和弦音×${counts.chord} 贝斯音×${counts.bass}`);
