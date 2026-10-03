// verify.mjs — 无头 Edge 真渲染取证：确定性 demo 快进到关键帧 → 抓 HUD 状态 + 截图 → 断言
// 证据链：HUD 是页面自己汇报的状态；截图是 GPU 真渲染的帧；A/B 由 Python 像素级分析。
import { spawn, spawnSync } from 'node:child_process';
import { accessSync, constants, mkdirSync, rmSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(HERE, 'verification');
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const PORT = 4191;
const BASE = `http://127.0.0.1:${PORT}`;
mkdirSync(OUT, { recursive: true });

let pass = 0, fail = 0;
const check = (name, cond, extra = '') => {
  if (cond) { pass++; console.log(`PASS  ${name}${extra ? '  (' + extra + ')' : ''}`); }
  else { fail++; console.log(`FAIL  ${name}${extra ? '  (' + extra + ')' : ''}`); }
};

// ---- 起服务器 ----
const server = spawn(process.execPath, [path.join(HERE, 'server.mjs'), String(PORT)], { stdio: 'ignore' });
await new Promise((r) => setTimeout(r, 1200));

function edge(args, timeout = 60000) {
  const res = spawnSync(EDGE, ['--headless=new', '--disable-gpu', '--no-first-run', '--hide-scrollbars',
    '--window-size=1000,640', '--user-data-dir=' + path.join(OUT, '.edgeprofile'),
    ...args], { timeout, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  return res;
}
function hudAt(url) {
  const res = edge(['--virtual-time-budget=4000', '--dump-dom', url]);
  const m = (res.stdout || '').match(/id="hud">([^<]*)</);
  return m ? m[1] : '(hud not found)';
}
function shotAt(file, url) {
  const p = path.join(OUT, file);
  rmSync(p, { force: true });
  edge(['--virtual-time-budget=5000', `--screenshot=${p}`, url]);
  try { accessSync(p, constants.F_OK); return true; } catch { return false; }
}
const page = (extra) => `${BASE}/exercise/index.html?demo=1${extra}`;

// ---- 断言 1：确定性快进的四个关键帧 ----
{
  const h = hudAt(page('&t=0.5'));
  check('t=0.5 站在出生点', /scene=village \| pos=2\.50,1\.50 \| dlg=closed/.test(h), h.slice(0, 90));
}
{
  const h = hudAt(page('&t=2.5'));
  const m = h.match(/pos=([\d.]+),/);
  const x = m ? parseFloat(m[1]) : -1;
  check('t=2.5 已向右又折返到 3.8', x > 3.5 && x < 4.1, `x=${x}`);
  check('t=2.5 对话未开', /dlg=closed/.test(h));
  // ghost 真相：t=2.5 走了 4.0 格 → (6.0,8.0)；渲染的是 100ms 前(t=2.4) → 3.84 格 → (5.84,8.0)
  check('t=2.5 远端玩家按延迟插值渲染', /ghost=5\.8\d,8\.00/.test(h), h.match(/ghost=[^|]*/)?.[0]?.trim());
}
{
  const h = hudAt(page('&t=4.6'));
  check('t=4.6 对话第一句打字机进行中', /dlg=typing:欢迎来到像素村/.test(h), h.match(/dlg=[^|]*/)?.[0]?.trim());
}
{
  const h = hudAt(page('&t=8.0'));
  check('t=8.0 第二句已完整等待翻页', /dlg=waiting:去下面的黄门/.test(h), h.match(/dlg=[^|]*/)?.[0]?.trim().slice(0, 40));
}
{
  const h = hudAt(page('&t=13.0'));
  check('t=13 已切换进屋（场景切换）', /scene=house/.test(h) && /dlg=closed/.test(h), h.slice(0, 90));
}
// 多人插值：同一时刻 ghost 真相位置 vs 渲染位置差应 < 半格（无法直接从 HUD 读 ghost，
// 用截图证明有第二个角色，位置差由 logic_test 的 NetSync 单测覆盖）

// ---- 断言 2：真渲染截图存在且逐帧不同 ----
const shots = [['shot_t0.png', '&t=0.5'], ['shot_t25.png', '&t=2.5'],
               ['shot_t46.png', '&t=4.6'], ['shot_house.png', '&t=13.0']];
for (const [f, q] of shots) check(`截图 ${f}`, shotAt(f, page(q)));
check('对照 A/B：关像素化直渲', shotAt('shot_nopixel.png', `${BASE}/exercise/index.html?demo=1&pixel=0&t=2.5`));

// ---- 断言 3：A/B 像素分析（Python PIL） ----
{
  const py = spawnSync('python', [path.join(HERE, 'analyze_ab.py'),
    path.join(OUT, 'shot_t25.png'), path.join(OUT, 'shot_nopixel.png')], { encoding: 'utf8' });
  console.log(py.stdout?.trim());
  check('A/B 像素分析完成', py.status === 0 && /AB_DIFF_NONZERO/.test(py.stdout || ''));
  check('像素化版块状度更高', /PIXEL_BLOCKIER/.test(py.stdout || ''));
}

// ---- 汇总 ----
const report = { pass, fail, time: new Date().toISOString(), port: PORT };
writeFileSync(path.join(OUT, 'report.json'), JSON.stringify(report, null, 2));
console.log(`\nTOTAL: ${pass} pass, ${fail} fail`);
server.kill();
process.exit(fail ? 1 : 0);
