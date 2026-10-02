/**
 * 验证 Deadrun 手搓 Web Mercator 投影算出的瓦片坐标，指向的确实是真实城市街道。
 * 对照组：同一 z/x/y 从 OpenStreetMap 官方瓦片服务器下载，市中心瓦片应远大于太平洋瓦片。
 * 用法：node --experimental-transform-types osm-crosscheck.ts
 */
import { project, TILE_SIZE, TILE_ZOOM } from './node-src/tiles.ts';

async function sizeOf(url: string): Promise<number> {
  const res = await fetch(url, {
    headers: { 'User-Agent': 'deadrun-exercise-crosscheck/1.0' },
  });
  if (!res.ok) throw new Error(url + ' -> ' + res.status);
  return (await res.arrayBuffer()).byteLength;
}

const places = [
  { name: 'Galata Tower (Istanbul 市中心)', at: { latitude: 41.0256, longitude: 28.9744 } },
  { name: 'Open Pacific (太平洋公海)', at: { latitude: -30, longitude: -140 } },
];

const rows: Array<{ name: string; x: number; y: number; bytes: number }> = [];
for (const p of places) {
  const q = project(p.at);
  const x = Math.floor(q.x / TILE_SIZE);
  const y = Math.floor(q.y / TILE_SIZE);
  const url = `https://tile.openstreetmap.org/${TILE_ZOOM}/${x}/${y}.png`;
  const bytes = await sizeOf(url);
  rows.push({ name: p.name, x, y, bytes });
  console.log(`z${TILE_ZOOM}/${x}/${y}  ${p.name}  ${bytes} B  (${url})`);
}

const [city, ocean] = rows;
const ratio = city.bytes / ocean.bytes;
console.log(`\n市中心/太平洋 字节比 = ${ratio.toFixed(1)}x`);
if (ratio > 2) {
  console.log('CROSS-CHECK PASS：手搓投影算出的坐标指向真实街道，不是空白海面。');
} else {
  console.log('CROSS-CHECK FAIL：坐标可能有错。');
  process.exit(1);
}
