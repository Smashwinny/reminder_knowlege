// main.js — 复刻推文五点思路的浏览器 demo：像素风 3D 迷你 JRPG 世界
// 对应推文：1 引擎=Three.js  2 Gameplay=行走/对话/场景切换(logic.js)  3 资产=全程序化生成(零美术)
//          4 画面=cel shading + 描边 + 像素化后处理  5 多人=脚本假远端玩家 + NetSync 插值
import * as THREE from 'three';
import { makeGrid, moveWithCollision, DialogueFSM, SceneManager, NetSync } from './logic.js';

// ---------- URL 参数（确定性验证用） ----------
const q = new URLSearchParams(location.search);
const DEMO = q.get('demo') === '1';          // 跑脚本化演示（验证 harness 用）
const FREEZE_T = q.get('t') !== null ? parseFloat(q.get('t')) : null; // 快进到 t 秒
const FREEZE = FREEZE_T !== null;            // 快进后停表，方便截图取证
const PIXEL = q.get('pixel') !== '0';        // 像素化后处理开关（A/B 实验）

// ---------- 固定时间步模拟（确定性：同 t 永远同状态） ----------
const DT = 1 / 60;
let simTime = 0;

// ---------- 确定性 RNG（程序化资产生成必须可复现） ----------
let seed = 1337;
function rnd() { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; }

// ---------- 推文第 3 点：程序化像素资产（零外部文件） ----------
function pixelCanvas(w, h, draw) {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  draw(c.getContext('2d'));
  const tex = new THREE.CanvasTexture(c);
  tex.magFilter = THREE.NearestFilter; tex.minFilter = THREE.NearestFilter;
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}
// 12x12 像素小人：palette 索引画法（'.'透明），四方向靠翻转/换色，走路两帧靠腿错位
const PAL = { H: '#3a2a18', S: '#f0c8a0', T: '#2e86de', L: '#2c3e50' };
const HERO_ROWS = [
  '....HHHH....',
  '...HHHHHH...',
  '..HHHHHHHH..',
  '..HSSHHSSH..',
  '..SSSSSSSS..',
  '...SSTTSS...',
  '..TTTTTTTT..',
  '.TTTTTTTTTT.',
  '.STTTTTTTTS.',
  '..TTTTTTTT..',
  '..LL.LL.LL..',
  '..LL..L..LL.',
];
function drawHero(g, dir, step) {
  const flip = (dir === 'left');
  for (let y = 0; y < HERO_ROWS.length; y++) {
    const row = HERO_ROWS[y];
    for (let x = 0; x < row.length; x++) {
      const ch = row[flip ? row.length - 1 - x : x];
      if (ch === '.') continue;
      let color = PAL[ch];
      if (y >= 10) {                              // 腿：两帧交替"抬起"
        const lifted = (step === 1) ? (x % 3 === 0) : (x % 3 === 2);
        if (lifted) continue;
      }
      if (dir === 'up' && y >= 3 && y <= 4) color = PAL.H; // 背面：后脑勺盖脸
      if (dir === 'left' || dir === 'right') { if (y >= 3 && y <= 4) color = (x >= 5 && x <= 8) ? PAL.H : color; }
      g.fillStyle = color; g.fillRect(x, y, 1, 1);
    }
  }
}
const HERO_TEX = {};
for (const dir of ['down', 'up', 'left', 'right'])
  for (const step of [0, 1])
    HERO_TEX[dir + step] = pixelCanvas(12, 12, (g) => drawHero(g, dir, step));
function groundTexture(base, speck, speck2) {
  return pixelCanvas(16, 16, (g) => {
    g.fillStyle = base; g.fillRect(0, 0, 16, 16);
    for (let i = 0; i < 26; i++) { g.fillStyle = rnd() < 0.6 ? speck : speck2; g.fillRect((rnd() * 16) | 0, (rnd() * 16) | 0, 1, 1); }
  });
}

// ---------- 推文第 4 点：日式 RPG 风 shader = cel 量化 + 描边(反转法线外壳) ----------
const gradTex = (() => {
  const colors = new Uint8Array([90, 170, 255]);
  const t = new THREE.DataTexture(colors, 3, 1, THREE.RedFormat);
  t.needsUpdate = true; t.minFilter = THREE.NearestFilter; t.magFilter = THREE.NearestFilter;
  return t;
})();
function celMaterial(color) {
  return new THREE.MeshToonMaterial({ color, gradientMap: gradTex });
}
function addOutline(mesh, thickness = 0.05) {
  const out = new THREE.Mesh(mesh.geometry, new THREE.MeshBasicMaterial({ color: 0x101018, side: THREE.BackSide }));
  out.scale.multiplyScalar(1 + thickness);
  mesh.add(out);
}

// ---------- 地图 ----------
const villageRows = [
  '############',
  '#N.........#',
  '#..........#',
  '#..HH..HH..#',
  '#..HH..HH..#',
  '#.....D....#',
  '#....o.....#',
  '#.T........#',
  '#........T.#',
  '############',
];
const houseRows = [
  '######',
  '#....#',
  '#..C.#',
  '#....#',
  '##D###',
];
function findTile(rows, ch) {
  for (let y = 0; y < rows.length; y++) for (let x = 0; x < rows[y].length; x++) if (rows[y][x] === ch) return { x, y };
  return null;
}
const scenes = {
  village: { name: 'village', rows: villageRows, exits: { D: 'house' } },
  house: { name: 'house', rows: houseRows, exits: { D: 'village' } },
};

// ---------- 渲染器 + 像素化后处理 ----------
const OUT_W = 480, OUT_H = 270;               // 内部低分辨率渲染目标（像素感的来源）
const canvas = document.getElementById('game');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false });
renderer.setSize(960, 540, false);            // 画布固定 960x540，CSS 再放大交给 image-rendering
renderer.setPixelRatio(1);
renderer.info.autoReset = false;              // 手动 reset，让 HUD 能看到整帧 drawCalls
const scene = new THREE.Scene();
scene.add(new THREE.AmbientLight(0xffffff, 1.6));
const sun = new THREE.DirectionalLight(0xffffff, 2.2); sun.position.set(6, 12, 4); scene.add(sun);
scene.background = new THREE.Color(0xff0000);
const camera = new THREE.OrthographicCamera(-7.6, 7.6, 4.28, -4.28, 0.1, 100);
// JRPG 斜俯视：正交相机从斜上方 45° 看下去——"假 3D 俯视"的经典摆法
const CAM_DIR = new THREE.Vector3(1, 1.35, 1).normalize();   // 相机在斜上方 3/4 俯视
function placeCamera(target) {
  camera.position.copy(target).addScaledVector(CAM_DIR, 30);
  camera.lookAt(target);
}
const camTarget = new THREE.Vector3();

// 低分辨率 RT + 最近邻放大全屏 quad（最近邻 = 放大不插值 = 大像素块）
const rt = new THREE.WebGLRenderTarget(OUT_W, OUT_H, { minFilter: THREE.NearestFilter, magFilter: THREE.NearestFilter });
const postScene = new THREE.Scene();
const postCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
const postMat = new THREE.ShaderMaterial({
  uniforms: { tex: { value: rt.texture } },
  vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }',
  fragmentShader: 'uniform sampler2D tex; varying vec2 vUv; void main(){ gl_FragColor = texture2D(tex, vUv); }',
});
postScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), postMat));

// ---------- 构建两个场景子树 ----------
function buildScene(def) {
  const grid = makeGrid(def.rows);
  const group = new THREE.Group();
  const floorMat = new THREE.MeshBasicMaterial({
    map: def.name === 'village' ? groundTexture('#59b94c', '#4aa63f', '#6fce5f')
                                : groundTexture('#b98b4e', '#a87a40', '#c99a5e'),
  });
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(grid.w, grid.h), floorMat);
  floor.rotation.x = -Math.PI / 2;
  floor.position.set(grid.w / 2 - 0.5, 0, grid.h / 2 - 0.5);
  group.add(floor);
  const wallMat = celMaterial(def.name === 'village' ? 0x8d6e63 : 0x795548);
  for (let y = 0; y < grid.h; y++) for (let x = 0; x < grid.w; x++) {
    const ch = grid.tiles[y][x];
    if (ch === '#') {
      const h = def.name === 'village' ? 1.2 : 1.0;
      const m = new THREE.Mesh(new THREE.BoxGeometry(1, h, 1), wallMat);
      m.position.set(x, h / 2, y);
      addOutline(m);
      group.add(m);
    } else if (ch === 'T') {
      const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.16, 0.6, 6), celMaterial(0x6d4c41));
      trunk.position.set(x, 0.3, y);
      const crown = new THREE.Mesh(new THREE.IcosahedronGeometry(0.55, 0), celMaterial(0x2e7d32));
      crown.position.set(x, 0.95, y);
      addOutline(crown);
      group.add(trunk, crown);
    } else if (ch === 'H') {
      const m = new THREE.Mesh(new THREE.BoxGeometry(1, 1.6, 1), celMaterial(0xd35400));
      m.position.set(x, 0.8, y);
      addOutline(m);
      group.add(m);
    } else if (ch === 'C') {
      const m = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.5, 0.5), celMaterial(0xf39c12));
      m.position.set(x, 0.25, y);
      addOutline(m);
      group.add(m);
    } else if (ch === 'o') {
      const m = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 0.5, 8), celMaterial(0x7f8c8d));
      m.position.set(x, 0.25, y);
      addOutline(m);
      group.add(m);
    } else if (ch === 'D') {
      const m = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.9, 0.12), celMaterial(0xf1c40f));
      m.position.set(x, 0.45, y);
      group.add(m);
    }
  }
  return { grid, group, ...def };
}
const builtScenes = {};
for (const k in scenes) builtScenes[k] = buildScene(scenes[k]);
scene.add(builtScenes.village.group);
const sm = new SceneManager(builtScenes, 'village');

// ---------- 玩家（像素精灵 + 影子） ----------
const player = { x: 2.5, y: 1.5, r: 0.3, facing: 'down', moving: false };
const SPEED = 2.6; // 格/秒
const heroMat = new THREE.SpriteMaterial({ map: HERO_TEX.down0 });
const hero = new THREE.Sprite(heroMat);
hero.scale.set(1.2, 1.2, 1); hero.center.set(0.5, 0.1);
scene.add(hero);
const shadow = new THREE.Mesh(new THREE.CircleGeometry(0.3, 12), new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.3 }));
shadow.rotation.x = -Math.PI / 2; shadow.position.y = 0.02;
scene.add(shadow);

// ---------- NPC（放 village 子树里：进屋自动看不见） ----------
const npcTile = findTile(villageRows, 'N');
const npcMat = new THREE.SpriteMaterial({ map: HERO_TEX.down0 });
npcMat.color = new THREE.Color(0xff8ff0);
const npc = new THREE.Sprite(npcMat);
npc.scale.set(1.1, 1.1, 1); npc.center.set(0.5, 0.1);
npc.position.set(npcTile.x + 0.5, 0, npcTile.y + 0.5);
builtScenes.village.group.add(npc);
const dlg = new DialogueFSM([
  '欢迎来到像素村！我们整个世界只有 480x270 个像素。',
  '去下面的黄门，能走进屋里——就是"场景切换"。',
]);
function nearNPC() {
  if (sm.current !== 'village') return false;
  return Math.hypot(player.x - npc.position.x, player.y - npc.position.z) < 1.3;
}

// ---------- 推文第 5 点：假"远端玩家"（脚本路径 + 100ms 延迟 + 插值） ----------
const ghostMat = new THREE.SpriteMaterial({ map: HERO_TEX.up0 });
ghostMat.color = new THREE.Color(0x9b59b6);
const ghost = new THREE.Sprite(ghostMat);
ghost.scale.set(1.1, 1.1, 1); ghost.center.set(0.5, 0.1);
builtScenes.village.group.add(ghost);
const net = new NetSync(0.1);
const WAYPOINTS = [[2, 8], [10, 8], [10, 2], [2, 2]];
function ghostTruePos(t) { // 远端"真相"：沿路点循环匀速走
  const speed = 1.6; const total = 34; let dist = (t * speed) % total; let acc = 0;
  for (let i = 0; i < WAYPOINTS.length; i++) {
    const a = WAYPOINTS[i], b = WAYPOINTS[(i + 1) % WAYPOINTS.length];
    const len = Math.hypot(b[0] - a[0], b[1] - a[1]);
    if (dist <= acc + len) { const k = (dist - acc) / len; return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k]; }
    acc += len;
  }
  return WAYPOINTS[0];
}

// ---------- 输入 ----------
const keys = {};
addEventListener('keydown', (e) => {
  const k = e.key.toLowerCase();
  keys[k] = true;
  if (k === 'e' && nearNPC()) { if (!dlg.open()) dlg.advance(); }
});
addEventListener('keyup', (e) => { keys[e.key.toLowerCase()] = false; });
function readManual() {
  return { x: (keys['d'] || keys['arrowright'] ? 1 : 0) - (keys['a'] || keys['arrowleft'] ? 1 : 0),
           y: (keys['s'] || keys['arrowdown'] ? 1 : 0) - (keys['w'] || keys['arrowup'] ? 1 : 0), e: false };
}

// ---------- 脚本化演示（验证 harness 用；以"帧号"为时间轴，完全确定） ----------
// 时间轴：0-59 站立 | 60-119 向右走 | 120-203 向左走回 NPC 旁 | 204 按 E 开对话(打字机)
//         300 按 E 跳完第一句 | 330 按 E 翻到第二句(继续打字) | 480 按 E 关闭
//         490-586 向下走进第五行 | 587-719 向右走到黄门 | ~700 踩门 → 切换到屋内
function demoInput(frame) {
  const v = { x: 0, y: 0, e: false };
  if (frame >= 60 && frame < 120) v.x = 1;
  if (frame >= 120 && frame < 204) v.x = -1;
  if (frame === 204 || frame === 300 || frame === 330 || frame === 480) v.e = true;
  if (frame >= 490 && frame < 587) v.y = 1;
  if (frame >= 587 && frame < 720) v.x = 1;
  return v;
}

// ---------- SceneManager 半程换子树 + 传送（logic.js 只管状态，子树交换在这） ----------
const _smUpdate = sm.update.bind(sm);
sm.update = (dt, tile) => {
  const before = sm.current;
  const r = _smUpdate(dt, tile);
  if (sm.current !== before) {
    const target = builtScenes[sm.current];
    scene.remove(builtScenes[before].group);
    scene.add(target.group);
    const door = findTile(target.rows, 'D');
    const away = sm.current === 'house' ? -1.6 : 1.6;   // 出门后站到离门 1.6 格，防止原地再触发
    player.x = door.x + 0.5; player.y = door.y + away;
  }
  return r;
};

// ---------- HUD ----------
const hud = document.getElementById('hud');
let drawCalls = 0; let ghostPos = '';

// ---------- 模拟一步 ----------
function step(dt, input) {
  simTime += dt;
  player.moving = input.x !== 0 || input.y !== 0;
  const cur = builtScenes[sm.current];
  const len = Math.hypot(input.x, input.y) || 1;
  moveWithCollision(cur.grid, 1, player, (input.x / len) * SPEED, (input.y / len) * SPEED, dt, player.r);
  if (input.x < 0) player.facing = 'left'; else if (input.x > 0) player.facing = 'right';
  else if (input.y > 0) player.facing = 'down'; else if (input.y < 0) player.facing = 'up';
  if (input.e) { if (nearNPC()) { if (!dlg.open()) dlg.advance(); } }
  dlg.update(dt);
  const tx = Math.floor(player.x), ty = Math.floor(player.y);
  const tileChar = (tx >= 0 && ty >= 0 && tx < cur.grid.w && ty < cur.grid.h) ? cur.grid.tiles[ty][tx] : '#';
  sm.update(dt, { char: tileChar });
  const tp = ghostTruePos(simTime);
  net.push(simTime, tp[0], tp[1]);
}

// ---------- 渲染一帧 ----------
function render() {
  renderer.info.reset();
  hero.position.set(player.x, 0, player.y);
  shadow.position.set(player.x, 0.02, player.y);
  const step = player.moving ? (Math.floor(simTime * 6) % 2) : 0;
  heroMat.map = HERO_TEX[player.facing + step];
  const gp = net.sample(simTime);
  if (gp) { ghost.position.set(gp.x, 0, gp.y); ghostPos = gp.x.toFixed(2) + ',' + gp.y.toFixed(2); }
  camTarget.set(player.x, 0, player.y);
  placeCamera(camTarget);
  if (sm.fade > 0) {  // 切换过场：背景压黑再弹回（fade 0.6→0，半程最黑）
    const dark = 1 - Math.abs(sm.fade - 0.3) / 0.3;
    scene.background.setScalar(0.53 * (1 - dark) + 0.05 * dark);
  } else scene.background.set(0x87ceeb);
  if (PIXEL) {        // 像素化：低分辨率 RT → 最近邻放大
    renderer.setRenderTarget(rt);
    renderer.render(scene, camera);
    renderer.setRenderTarget(null);
    renderer.render(postScene, postCam);
  } else {
    renderer.setRenderTarget(null);
    renderer.render(scene, camera);
  }
  drawCalls = renderer.info.render.calls;
}

// ---------- 主循环 ----------
function hudUpdate() {
  const dstate = dlg.state === 'closed' ? 'closed' : dlg.state + ':' + dlg.text;
  hud.textContent = `${bootErr ? bootErr + ' | ' : ''}scene=${sm.current} | pos=${player.x.toFixed(2)},${player.y.toFixed(2)} | dlg=${dstate} | pixel=${PIXEL ? 'on' : 'off'} | ghost=${ghostPos} | t=${simTime.toFixed(2)} | drawCalls=${drawCalls}`;
}
let booted = false;
let bootErr = '';
function boot() {
  booted = true;
  if (FREEZE) {       // 确定性快进：从 0 一帧不跳跑到 t
    const frames = Math.round(FREEZE_T / DT);
    try {
      for (let i = 0; i < frames; i++) step(DT, DEMO ? demoInput(i) : readManual());
    } catch (e) { bootErr = 'BOOT_ERR@' + simTime.toFixed(3) + ': ' + e.message + ' || ' + (e.stack || '').split('\n').slice(0, 3).join(' ~ ').replace(/https?:\/\/[^ ]+/g, ''); }
  }
}
let last = performance.now() / 1000;
function tick() {
  requestAnimationFrame(tick);
  if (!booted) boot();
  const now = performance.now() / 1000;
  let dt = Math.min(now - last, 0.1); last = now;
  if (!FREEZE) {
    while (dt > 0) { const h = Math.min(dt, DT); step(h, DEMO ? demoInput(Math.round(simTime / DT)) : readManual()); dt -= h; }
  }
  render();
  hudUpdate();
}
tick();
