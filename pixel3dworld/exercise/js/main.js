// main.js — 复刻推文五点思路的浏览器 demo：像素风 3D 迷你 JRPG 世界
// 对应推文：1 引擎=Three.js  2 Gameplay=行走/对话/场景切换(logic.js)  3 资产=全程序化生成(零美术)
//          4 画面=cel shading + 描边 + 像素化后处理  5 多人=脚本假远端玩家 + NetSync 插值
import * as THREE from 'three';
import { makeGrid, moveWithCollision, DialogueFSM, SceneManager, NetSync, hitsWall } from './logic.js';

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
// 16x16 像素小人：4 方向 x 2 步帧，palette 索引画法（'.'透明）
const PAL = { H: '#3a2a18', S: '#f0c8a0', T: '#2e86de', L: '#2c3e50', O: '#1a1a1a', Y: '#f1c40f' };
const HERO_FRAMES = {
  down: ['....HHHH....', '...HHHHHH...', '..HHHHHHHH..', '..HSSHHSSH..', '..SSSSSSSS..', '...SSTTSS...',
          '..TTTTTTTT..', '.TTTTTTTTTT.', '.STTTTTTTTS.', '..TTTTTTTT..', '..LL.LL.LL..', '..LL..L..LL.'],
};
// 上面只画正面轮廓，四方向靠翻转/换发色块——demo 足够；2 步帧靠腿部错位
function heroTexture(dir, step) {
  return pixelCanvas(12, 12, (g) => {
    const rows = HERO_FRAMES.down;
    const flip = (dir === 'left');
    for (let y = 0; y < rows.length; y++) {
      const row = rows[y];
      for (let x = 0; x < row.length; x++) {
        const ch = row[flip ? row.length - 1 - x : x];
        if (ch === '.') continue;
        let color = PAL[ch];
        if (y >= 10) { // 腿：走路两帧交替抬起
          const legPhase = (step === 1) ? (x % 3 === 0) : (x % 3 === 2);
          if (legPhase) continue;
          color = PAL.L;
        }
        if (dir === 'up' && y >= 3 && y <= 4) color = PAL.H; // 背面：后脑勺盖住脸
        g.fillStyle = color; g.fillRect(x, y, 1, 1);
      }
    }
  });
}
function groundTexture(base, speck, speck2) {
  return pixelCanvas(16, 16, (g) => {
    g.fillStyle = base; g.fillRect(0, 0, 16, 16);
    for (let i = 0; i < 26; i++) { g.fillStyle = rnd() < 0.6 ? speck : speck2; g.fillRect((rnd() * 16) | 0, (rnd() * 16) | 0, 1, 1); }
  });
}

// ---------- 推文第 4 点：日式 RPG 风 shader = cel 量化 + 描边(反转法线外壳) ----------
function celMaterial(color) {
  const steps = 3;
  const colors = new Uint8Array([80, 160, 255]);
  const grad = new THREE.DataTexture(colors, 3, 1, THREE.RedFormat);
  grad.needsUpdate = true; grad.minFilter = THREE.NearestFilter; grad.magFilter = THREE.NearestFilter;
  return new THREE.MeshToonMaterial({ color, gradientMap: grad });
}
function addOutline(mesh, thickness = 0.045) {
  const out = new THREE.Mesh(mesh.geometry, new THREE.MeshBasicMaterial({ color: 0x101018, side: THREE.BackSide }));
  out.scale.multiplyScalar(1 + thickness);
  mesh.add(out);
}

// ---------- 世界构建 ----------
const TILE = 1;
function buildVillage() {
  const rows = [
    '############',
    '#N.....T...#',
    '#..........#',
    '#..HH..HH..#',
    '#..HH..HH..#',
    '#.....D....#',
    '#.T........#',
    '#....o.....#',
    '#..........#',
    '############',
  ];
  return rows;
}
const villageRows = buildVillage();
const houseRows = [
  '######',
  '#....#',
  '#.C..#',
  '#....#',
  '##D###',
];
// D 门在 village 行 5 col 6；house 门在 row4 col2
const scenes = {
  village: { name: 'village', rows: villageRows, exits: { D: 'house' } },
  house: { name: 'house', rows: houseRows, exits: { D: 'village' } },
};
// 找门/NPC 的格子
function findTile(rows, ch) {
  for (let y = 0; y < rows.length; y++) for (let x = 0; x < rows[y].length; x++) if (rows[y][x] === ch) return { x, y };
  return null;
}

// ---------- 渲染器 + 像素化后处理 ----------
const OUT_W = 480, OUT_H = 270;               // 内部低分辨率渲染目标（像素感的来源）
const canvas = document.getElementById('game');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false });
renderer.setSize(OUT_W * 2, OUT_H * 2, false); // CSS 放大交给 image-rendering: pixelated
renderer.setPixelRatio(1);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87ceeb);
const camera = new THREE.OrthographicCamera(-7.5, 7.5, 4.2, -4.2, 0.1, 100);
// JRPG 斜俯视：绕 X 轴压下去 ~55°，绕 Y 轴转 45°——正交相机斜着看世界
const CAM_DIR = new THREE.Vector3(1, -1.2, 1).normalize();
function placeCamera(target) {
  camera.position.copy(target).addScaledVector(CAM_DIR, 30);
  camera.lookAt(target);
}
const camTarget = new THREE.Vector3();

// 低分辨率 RT + 最近邻放大 quad
const rt = new THREE.WebGLRenderTarget(OUT_W, OUT_H, { minFilter: THREE.NearestFilter, magFilter: THREE.NearestFilter });
const postScene = new THREE.Scene();
const postCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
const postMat = new THREE.ShaderMaterial({
  uniforms: { tex: { value: rt.texture } },
  vertexShader: 'void main(){ gl_Position = vec4(position.xy, 0.0, 1.0); }',
  fragmentShader: `
    uniform sampler2D tex; varying vec2 vUv;
    void main(){ gl_FragColor = texture2D(tex, vUv); }`,
});
postMat.vertexShader = 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }';
const postQuad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), postMat);
postScene.add(postQuad);

// ---------- 两个场景的场景子树 ----------
function buildScene(def) {
  const grid = makeGrid(def.rows);
  const group = new THREE.Group();
  const grass = groundTexture('#59b94c', '#4aa63f', '#6fce5f');
  const floorMat = new THREE.MeshBasicMaterial({ map: def.name === 'village' ? grass : groundTexture('#b98b4e', '#a87a40', '#c99a5e') });
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(grid.w, grid.h), floorMat);
  floor.rotation.x = -Math.PI / 2;
  floor.position.set(grid.w / 2 - 0.5, 0, grid.h / 2 - 0.5);
  group.add(floor);
  const wallMat = celMaterial(0x8d6e63);
  const houseWallMat = celMaterial(0x795548);
  for (let y = 0; y < grid.h; y++) for (let x = 0; x < grid.w; x++) {
    const ch = grid.tiles[y][x];
    if (ch === '#') {
      const h = def.name === 'village' ? 1.2 : 1.0;
      const m = new THREE.Mesh(new THREE.BoxGeometry(1, h, 1), def.name === 'village' ? wallMat : houseWallMat);
      m.position.set(x, h / 2, y);
      addOutline(m);
      group.add(m);
    } else if (ch === 'T') { // 树：干 + 冠
      const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.16, 0.6, 6), celMaterial(0x6d4c41));
      trunk.position.set(x, 0.3, y);
      const crown = new THREE.Mesh(new THREE.IcosahedronGeometry(0.55, 0), celMaterial(0x2e7d32));
      crown.position.set(x, 0.95, y);
      addOutline(crown);
      group.add(trunk, crown);
    } else if (ch === 'H') { // 房子墙块
      const m = new THREE.Mesh(new THREE.BoxGeometry(1, 1.6, 1), celMaterial(0xd35400));
      m.position.set(x, 0.8, y);
      addOutline(m);
      group.add(m);
    } else if (ch === 'C') { // 宝箱
      const m = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.5, 0.5), celMaterial(0xf39c12));
      m.position.set(x, 0.25, y);
      addOutline(m);
      group.add(m);
    } else if (ch === 'o') { // 水井
      const m = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 0.5, 8), celMaterial(0x7f8c8d));
      m.position.set(x, 0.25, y);
      addOutline(m);
      group.add(m);
    } else if (ch === 'D') { // 门：醒目黄色平板
      const m = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.9, 0.1), celMaterial(0xf1c40f));
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
const heroSprites = {};
for (const dir of ['down', 'up', 'left', 'right']) heroSprites[dir] = heroTexture(dir, 0);
const heroMat = new THREE.SpriteMaterial({ map: heroSprites.down });
const hero = new THREE.Sprite(heroMat);
hero.scale.set(1.2, 1.2, 1);
hero.center.set(0.5, 0.15);
scene.add(hero);
const shadow = new THREE.Mesh(new THREE.CircleGeometry(0.3, 12), new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.3 }));
shadow.rotation.x = -Math.PI / 2; shadow.position.y = 0.02;
scene.add(shadow);
const player = { x: 1.5, y: 1.5, r: 0.3, facing: 'down', moving: false };
const SPEED = 2.6; // 格/秒

// ---------- NPC ----------
const npcTile = findTile(villageRows, 'N');
const npcMat = new THREE.SpriteMaterial({ map: heroTexture('down', 0) });
npcMat.color = new THREE.Color(0xff9ff3);
const npc = new THREE.Sprite(npcMat);
npc.scale.set(1.1, 1.1, 1); npc.center.set(0.5, 0.15);
npc.position.set(npcTile.x, 0, npcTile.y);
scene.add(npc);
const dlg = new DialogueFSM([
  '欢迎来到像素村！我们整个世界只有 480x270 个像素那么大。',
  '按 E 再说一次，按方向键去下面的黄门，能进屋。',
]);

// ---------- 推文第 5 点：假"远端玩家"（脚本路径 + 100ms 延迟 + 插值） ----------
const ghostMat = new THREE.SpriteMaterial({ map: heroTexture('up', 0) });
ghostMat.color = new THREE.Color(0x9b59b6);
const ghost = new THREE.Sprite(ghostMat);
ghost.scale.set(1.1, 1.1, 1); ghost.center.set(0.5, 0.15);
scene.add(ghost);
const net = new NetSync(0.1);
const WAYPOINTS = [[2, 8], [10, 8], [10, 1.5], [2, 1.5]];
function ghostTruePos(t) { // 远端"真相"：沿路点循环匀速走
  const speed = 1.6; let dist = (t * speed) % 34; let acc = 0;
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
addEventListener('keydown', (e) => { keys[e.key.toLowerCase()] = true; if (e.key.toLowerCase() === 'e') interact(); });
addEventListener('keyup', (e) => { keys[e.key.toLowerCase()] = false; });
function interact() { if (demoInteract !== null) return; if (nearNPC()) dlg.open() || dlg.advance(); }
function nearNPC() {
  const sc = sm.current === 'village' ? builtScenes.village : null;
  if (!sc) return false;
  return Math.hypot(player.x - (npcTile.x + 0.5), player.y - (npcTile.y + 0.5)) < 1.3;
}

// ---------- 脚本化演示（验证 harness 用，确定性） ----------
let demoInteract = null; // null=手动；demo 模式下是时间轴回调
function demoInput(t) {
  const v = { x: 0, y: 0, e: false };
  if (t >= 1.0 && t < 3.0) v.x = 1;
  if (t >= 3.4 && t < 3.5) v.e = true;
  if (t >= 4.9 && t < 5.0) v.e = true;
  if (t >= 6.3 && t < 6.4) v.e = true;
  if (t >= 7.0 && t < 8.6) v.y = 1;
  if (t >= 9.0 && t < 9.1) v.e = true;
  return v;
}

// ---------- HUD ----------
const hud = document.getElementById('hud');
let drawCalls = 0, frameMs = 0;

// ---------- 主循环 ----------
function step(dt, input) {
  simTime += dt;
  // 移动
  player.moving = input.x !== 0 || input.y !== 0;
  const len = Math.hypot(input.x, input.y) || 1;
  moveWithCollision(sm.current === 'village' ? builtScenes.village : builtScenes.house,
    TILE, player, (input.x / len) * SPEED, (input.y / len) * SPEED, dt, player.r);
  if (input.x < 0) player.facing = 'left'; else if (input.x > 0) player.facing = 'right';
  else if (input.y > 0) player.facing = 'down'; else if (input.y < 0) player.facing = 'up';
  // 对话
  if (input.e) { if (!dlg.open()) dlg.advance(); }
  dlg.update(dt);
  // 场景切换
  const g = sm.current === 'village' ? builtScenes.village : builtScenes.house;
  const tx = Math.floor(player.x), ty = Math.floor(player.y);
  const tileChar = (tx >= 0 && ty >= 0 && tx < g.grid.w && ty < g.grid.h) ? g.grid.tiles[ty][tx] : '#';
  sm.update(dt, { char: tileChar });
  // 场景切换半程：换子树 + 传送到目标场景入口
  if (sm.pendingSwitch) { /* SceneManager 内部处理 */ }
  // 假联机：远端发包 + 本地按"过去"插值渲染
  const tp = ghostTruePos(simTime);
  net.push(simTime, tp[0], tp[1]);
}

// SceneManager 半程换场景：包一层（logic.js 只管状态，子树交换在这）
const _smUpdate = sm.update.bind(sm);
sm.update = (dt, tile) => {
  const before = sm.current;
  const wasFade = sm.fade > 0;
  const r = _smUpdate(dt, tile);
  if (sm.pending && !wasFade) { /* 刚发起 */ }
  if (sm.current !== before) {
    const target = builtScenes[sm.current];
    scene.remove(sm.scenes[before] && builtScenes[before].group);
    scene.add(target.group);
    const door = findTile(target.rows, 'D');
    player.x = door.x + 0.5; player.y = door.y + (sm.current === 'house' ? -0.8 : 0.8);
  }
  return r;
};

function render() {
  const g = sm.current === 'village' ? builtScenes.village : builtScenes.house;
  // 玩家位置 → 世界坐标（tile 平面：x→x, y→z）
  hero.position.set(player.x, 0, player.y);
  shadow.position.set(player.x, 0.02, player.y);
  const step = player.moving ? (Math.floor(simTime * 6) % 2) : 0;
  heroMat.map = player.moving ? heroTexture(player.facing, step) : heroSprites[player.facing];
  npc.position.y = 0;
  npc.material.rotation = 0;
  // 幽灵玩家：插值渲染
  const gp = net.sample(simTime);
  if (gp) ghost.position.set(gp.x, 0, gp.y);
  // 相机跟随（带场景切换压黑）
  camTarget.set(player.x, 0, player.y);
  placeCamera(camTarget);
  if (sm.fade > 0) scene.background.setScalar(Math.max(0.08, 1 - Math.min(sm.fade, 0.6 - sm.fade + 0.3)));
  else scene.background.set(0x87ceeb);
  // 渲染：先低分辨率 RT，再最近邻放大（pixel=0 时直接整分辨率渲染对照）
  if (PIXEL) {
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

let last = performance.now() / 1000;
let started = false;
function boot() {
  if (FREEZE) {
    // 确定性快进：从 0 一步不跳跑到 t
    for (let i = 0; i * DT < FREEZE_T; i++) step(DT, DEMO ? demoInput(i * DT) : readManual());
    step(DT, { x: 0, y: 0, e: false }); // 收尾一步
  }
  started = true;
}
function readManual() {
  const v = { x: (keys['d'] || keys['arrowright'] ? 1 : 0) - (keys['a'] || keys['arrowleft'] ? 1 : 0),
              y: (keys['s'] || keys['arrowdown'] ? 1 : 0) - (keys['w'] || keys['arrowup'] ? 1 : 0), e: false };
  return v;
}
function tick() {
  requestAnimationFrame(tick);
  const now = performance.now() / 1000;
  let dt = Math.min(now - last, 0.1); last = now;
  if (!started) boot();
  if (!FREEZE) {
    while (dt > 0) { const h = Math.min(dt, DT); step(h, DEMO ? demoInput(simTime) : readManual()); dt -= h; }
  }
  render();
  const dstate = dlg.state === 'closed' ? 'closed' : dlg.state + ':' + dlg.text;
  hud.textContent = `scene=${sm.current} | pos=${player.x.toFixed(2)},${player.y.toFixed(2)} | dlg=${dstate} | pixel=${PIXEL ? 'on' : 'off'} | t=${simTime.toFixed(2)} | drawCalls=${drawCalls}`;
}
if (!FREEZE) tick();
else { boot(); tick(); setTimeout(() => { /* 一帧后停 */ }, 50); }
