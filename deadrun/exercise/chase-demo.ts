/**
 * 用 Deadrun 纯函数引擎 headless 模拟一整局逃跑，把玩家与丧尸的轨迹画成 SVG。
 * 证明：整个游戏循环（GPS 注入 → tick → 波次 → 追逐 → 被抓）无需手机和 GPS 芯片即可复现。
 * 用法：node --experimental-transform-types chase-demo.ts [seconds] [seed]
 */
import { TICK_MS, WAVE_MS } from './node-src/config.ts';
import { beginRun, createGame, tick } from './node-src/engine.ts';
import { bearingDeg, destination, distanceM, type LatLng } from './node-src/geo.ts';
import type { GameState, PlayerFix } from './node-src/types.ts';

const MAX_SECONDS = Number(process.argv[2] ?? 240);
const SEED = Number(process.argv[3] ?? 42);
const SPEED_MS = 3.3; // 一个普通跑者的速度

/* ---- 与 scripts/simulate.ts 相同的"斥力逃跑"策略 ---------------------- */
function chooseHeading(state: GameState, pos: LatLng): number {
  let x = 0;
  let y = 0;
  for (const z of state.zombies) {
    const d = distanceM(z.pos, pos);
    if (d > 160) continue;
    const away = (bearingDeg(z.pos, pos) * Math.PI) / 180;
    const w = 1 / Math.max(64, d * d);
    x += Math.sin(away) * w;
    y += Math.cos(away) * w;
  }
  if (x === 0 && y === 0) return 0;
  return ((Math.atan2(x, y) * 180) / Math.PI + 360) % 360;
}

const START: LatLng = { latitude: 41.0082, longitude: 28.9784 };
let state = createGame('runner', SEED);
let now = 1_700_000_000_000;
let pos = START;
let heading = 0;
let fix: PlayerFix = { pos, accuracy: 5, speed: 0, heading: -1, at: now };
state = beginRun(state, fix, now);
let lastFixAt = now;

const playerPath: LatLng[] = [pos];
const zombieTrails = new Map<string, LatLng[]>();
const waveMarks: Array<{ wave: number; at: LatLng }> = [];

while (state.status === 'running' && state.elapsedMs < MAX_SECONDS * 1000) {
  now += TICK_MS;
  if (now - lastFixAt >= 1000) {
    const dtSec = (now - lastFixAt) / 1000;
    heading = chooseHeading(state, pos);
    pos = destination(pos, heading, SPEED_MS * dtSec);
    lastFixAt = now;
    fix = { pos, accuracy: 5, speed: SPEED_MS, heading, at: now };
    playerPath.push(pos);
  }
  const before = state.wave;
  state = tick(state, { now, dtMs: TICK_MS, fix }).state;
  if (state.wave > before) waveMarks.push({ wave: state.wave, at: { ...pos } });
  for (const z of state.zombies) {
    const t = zombieTrails.get(z.id) ?? [];
    t.push({ ...z.pos });
    zombieTrails.set(z.id, t);
  }
}

/* ---- 投影成平面米坐标画 SVG ------------------------------------------- */
const EARTH_R = 6371008.8;
function toM(p: LatLng): [number, number] {
  const lat0 = (START.latitude * Math.PI) / 180;
  const x = ((p.longitude - START.longitude) * Math.PI / 180) * EARTH_R * Math.cos(lat0);
  const y = -((p.latitude - START.latitude) * Math.PI / 180) * EARTH_R; // SVG y 向下 = 南
  return [x, y];
}
const allPts = [...playerPath, ...waveMarks.map((w) => w.at)];
for (const t of zombieTrails.values()) allPts.push(...t);
const xs = allPts.map((p) => toM(p)[0]);
const ys = allPts.map((p) => toM(p)[1]);
const minX = Math.min(...xs) - 40, maxX = Math.max(...xs) + 40;
const minY = Math.min(...ys) - 40, maxY = Math.max(...ys) + 40;
const W = 900;
const H = Math.max(300, Math.round((W * (maxY - minY)) / Math.max(1, maxX - minX)));
const sx = (p: LatLng) => {
  const [x, y] = toM(p);
  return `${(((x - minX) / (maxX - minX)) * W).toFixed(1)},${(((y - minY) / (maxY - minY)) * H).toFixed(1)}`;
};

const colors = ['#e5484d', '#f76b15', '#8e4ec6', '#0090ff', '#30a46c', '#d6409f'];
let i = 0;
const zombieLines = [...zombieTrails.entries()]
  .map(([id, trail]) => {
    const c = colors[i++ % colors.length];
    return `<polyline points="${trail.map(sx).join(' ')}" fill="none" stroke="${c}" stroke-width="1.2" opacity="0.55"/>`;
  })
  .join('\n  ');

const waveDots = waveMarks
  .map((w) => {
    const [x, y] = sx(w.at).split(',');
    return `<circle cx="${x}" cy="${y}" r="4" fill="#f5a524"/><text x="${Number(x) + 7}" y="${Number(y) - 5}" font-size="12" fill="#f5a524" font-weight="bold">W${w.wave}</text>`;
  })
  .join('\n  ');

const startPt = sx(START).split(',');
const endPt = sx(playerPath[playerPath.length - 1]).split(',');

const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" font-family="sans-serif">
  <rect width="${W}" height="${H}" fill="#101418"/>
  <text x="12" y="22" font-size="14" fill="#fff" font-weight="bold">DEADRUN headless chase replay · seed ${SEED} · runner ${SPEED_MS} m/s · difficulty=runner</text>
  ${zombieLines}
  <polyline points="${playerPath.map(sx).join(' ')}" fill="none" stroke="#12a594" stroke-width="2.5"/>
  <circle cx="${startPt[0]}" cy="${startPt[1]}" r="5" fill="#12a594"/>
  <text x="${Number(startPt[0]) + 8}" y="${Number(startPt[1]) + 4}" font-size="12" fill="#12a594" font-weight="bold">start</text>
  <circle cx="${endPt[0]}" cy="${endPt[1]}" r="6" fill="#e5484d"/>
  <text x="${Number(endPt[0]) + 9}" y="${Number(endPt[1]) + 4}" font-size="12" fill="#e5484d" font-weight="bold">end (${state.endReason ?? 'survived'})</text>
  ${waveDots}
  <text x="12" y="${H - 12}" font-size="12" fill="#9aa4b2">绿=玩家轨迹 彩线=各丧尸轨迹 黄点=波次刷新 帧间隔=${TICK_MS}ms 波次间隔=${WAVE_MS / 1000}s</text>
</svg>`;

const fs = await import('node:fs');
fs.writeFileSync(new URL('./chase-replay.svg', import.meta.url), svg);

const mins = Math.floor(state.elapsedMs / 60000);
const secs = Math.round((state.elapsedMs % 60000) / 1000);
console.log(`模拟结束: ${state.endReason ?? 'survived'} · ${mins}m${String(secs).padStart(2, '0')}s · ${state.wave} 波 · 跑出 ${Math.round(state.distanceM)} m · 击杀 ${state.kills} · 得分 ${state.score}`);
console.log(`轨迹点: 玩家 ${playerPath.length} 个 · 丧尸 ${zombieTrails.size} 条 · 已写出 chase-replay.svg (${W}x${H})`);
