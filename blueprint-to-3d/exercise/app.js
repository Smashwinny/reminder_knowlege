// 2D 图纸 → 3D 模型 过渡复刻
// 核心思路：
//   1. 每个模型 = 一个"零件清单"（程序化建模：代码即菜谱）
//   2. 2D 图纸不是图片，而是从零件的 2D 投影规格生成的 SVG（含尺寸标注）
//   3. 过渡 = 图纸线条 stroke-dash 重绘动画 + 3D 零件按 stagger 从"纸片"挤出成立体
import * as THREE from 'three';
import { OrbitControls } from './vendor/OrbitControls.js';

/* ================= 模型定义（3D 零件 + 2D 图纸规格） ================= */
// 单位约定：3D 用"米"，2D 图纸 1 米 = 40px，原点在图纸左下角 (ox, oy)

const MODELS = {
  tank: {
    title: 'MAIN BATTLE TANK · MK-1',
    note: 'hull / treads / turret / barrel — all procedural',
    parts3d: [
      // 履带 ×2（左右）
      { name: 'tread-L', geo: () => new THREE.BoxGeometry(4.2, 0.7, 0.55), color: 0x3a3f44, pos: [0, 0.35, 0.95] },
      { name: 'tread-R', geo: () => new THREE.BoxGeometry(4.2, 0.7, 0.55), color: 0x3a3f44, pos: [0, 0.35, -0.95] },
      // 负重轮 ×4×2
      ...[-1.5, -0.5, 0.5, 1.5].flatMap(x => ([
        { name: 'wheel', geo: () => new THREE.CylinderGeometry(0.32, 0.32, 0.62, 20), color: 0x6d747c, pos: [x, 0.35, 0.95], rot: [Math.PI / 2, 0, 0] },
        { name: 'wheel', geo: () => new THREE.CylinderGeometry(0.32, 0.32, 0.62, 20), color: 0x6d747c, pos: [x, 0.35, -0.95], rot: [Math.PI / 2, 0, 0] },
      ])),
      // 车体
      { name: 'hull', geo: () => new THREE.BoxGeometry(3.6, 0.9, 1.6), color: 0x5c7a29, pos: [0, 1.05, 0] },
      // 炮塔组（挂在 turret 节点下，展示场景图父子层级）
      { name: 'turret', geo: () => new THREE.CylinderGeometry(0.85, 1.0, 0.55, 8), color: 0x6b8e23, pos: [0, 0.68, 0], parent: 'turret' },
      { name: 'barrel', geo: () => new THREE.CylinderGeometry(0.07, 0.10, 2.2, 12), color: 0x49591b, pos: [1.55, 0.72, 0], rot: [0, 0, Math.PI / 2], parent: 'turret' },
      { name: 'antenna', geo: () => new THREE.CylinderGeometry(0.02, 0.02, 1.1, 6), color: 0x222222, pos: [-0.55, 1.5, 0.35], parent: 'turret' },
    ],
    // 2D 侧视图纸（米为单位的真实坐标）
    bp2d: [
      { t: 'rect', x: -2.1, y: 0.0, w: 4.2, h: 0.7, cls: 'bp-shape' },            // 履带外形
      ...[-1.5, -0.5, 0.5, 1.5].map(x => ({ t: 'circle', x, y: 0.35, r: 0.32, cls: 'bp-shape' })),
      { t: 'rect', x: -1.8, y: 0.7, w: 3.6, h: 0.9, cls: 'bp-shape' },             // 车体
      { t: 'rect', x: -0.85, y: 1.6, w: 1.7, h: 0.55, cls: 'bp-shape' },           // 炮塔
      { t: 'line', x1: 0.85, y1: 1.87, x2: 3.05, y2: 1.87, cls: 'bp-shape' },      // 炮管
      { t: 'line', x1: -0.55, y1: 2.15, x2: -0.55, y2: 3.25, cls: 'bp-hidden' },   // 天线
      // 尺寸标注
      { t: 'dim', x1: -2.1, y1: -0.45, x2: 2.1, y2: -0.45, label: '4200 mm' },
      { t: 'dimv', x: 3.45, y1: 0, y2: 2.15, label: '2150 mm' },
    ],
    dims: { w: 4.2, h: 2.15 },
  },

  robot: {
    title: 'SERVICE ROBOT · R-2',
    note: 'swap the builder, swap the model — 图纸同样由代码生成',
    parts3d: [
      { name: 'leg-L', geo: () => new THREE.BoxGeometry(0.35, 1.2, 0.4), color: 0x3777c8, pos: [-0.35, 0.6, 0] },
      { name: 'leg-R', geo: () => new THREE.BoxGeometry(0.35, 1.2, 0.4), color: 0x3777c8, pos: [0.35, 0.6, 0] },
      { name: 'body', geo: () => new THREE.BoxGeometry(1.2, 1.4, 0.8), color: 0xe8e8ee, pos: [0, 1.9, 0] },
      { name: 'arm-L', geo: () => new THREE.BoxGeometry(0.3, 1.1, 0.35), color: 0xd94f6b, pos: [-0.85, 1.85, 0] },
      { name: 'arm-R', geo: () => new THREE.BoxGeometry(0.3, 1.1, 0.35), color: 0xd94f6b, pos: [0.85, 1.85, 0] },
      { name: 'head', geo: () => new THREE.BoxGeometry(0.6, 0.5, 0.6), color: 0x222831, pos: [0, 2.9, 0] },
      { name: 'eye', geo: () => new THREE.BoxGeometry(0.4, 0.12, 0.05), color: 0x35e0c3, pos: [0, 2.9, 0.31] },
      { name: 'antenna', geo: () => new THREE.CylinderGeometry(0.02, 0.02, 0.6, 6), color: 0xffd166, pos: [0.2, 3.4, 0] },
    ],
    bp2d: [
      { t: 'rect', x: -0.525, y: 0, w: 0.35, h: 1.2, cls: 'bp-shape' },
      { t: 'rect', x: 0.175, y: 0, w: 0.35, h: 1.2, cls: 'bp-shape' },
      { t: 'rect', x: -0.6, y: 1.2, w: 1.2, h: 1.4, cls: 'bp-shape' },
      { t: 'rect', x: -1.0, y: 1.3, w: 0.3, h: 1.1, cls: 'bp-shape' },
      { t: 'rect', x: 0.7, y: 1.3, w: 0.3, h: 1.1, cls: 'bp-shape' },
      { t: 'rect', x: -0.3, y: 2.6, w: 0.6, h: 0.5, cls: 'bp-shape' },
      { t: 'line', x1: 0.2, y1: 3.1, x2: 0.2, y2: 3.7, cls: 'bp-hidden' },
      { t: 'dim', x1: -1.0, y1: -0.4, x2: 1.0, y2: -0.4, label: '2000 mm' },
      { t: 'dimv', x: 1.5, y1: 0, y2: 3.1, label: '3100 mm' },
    ],
    dims: { w: 2.0, h: 3.1 },
  },
};

/* ================= 2D 图纸生成（SVG，含尺寸标注） ================= */
const SCALE = 40;               // 1 米 = 40px

function buildBlueprintSVG(model) {
  const W = 430, H = 320;
  const ox = 40, oy = H - 55;   // 图纸原点（左下角，y 向上翻转）
  const X = m => ox + (m + 2.6) * SCALE;
  const Y = m => oy - m * SCALE;
  let s = '';
  for (const sh of model.bp2d) {
    if (sh.t === 'rect') {
      s += `<rect class="${sh.cls}" x="${X(sh.x)}" y="${Y(sh.y + sh.h)}" width="${sh.w * SCALE}" height="${sh.h * SCALE}"/>`;
    } else if (sh.t === 'circle') {
      s += `<circle class="${sh.cls}" cx="${X(sh.x)}" cy="${Y(sh.y)}" r="${sh.r * SCALE}"/>`;
    } else if (sh.t === 'line') {
      s += `<line class="${sh.cls}" x1="${X(sh.x1)}" y1="${Y(sh.y1)}" x2="${X(sh.x2)}" y2="${Y(sh.y2)}"/>`;
    } else if (sh.t === 'dim') {           // 水平尺寸线 + 端点 tick + 双向箭头 + 文字
      const y = Y(sh.y1), x1 = X(sh.x1), x2 = X(sh.x2);
      s += `<line class="bp-dim" x1="${x1}" y1="${y - 4}" x2="${x1}" y2="${y + 4}"/>
            <line class="bp-dim" x1="${x2}" y1="${y - 4}" x2="${x2}" y2="${y + 4}"/>
            <line class="bp-dim" x1="${x1}" y1="${y}" x2="${x2}" y2="${y}" marker-start="url(#ar)" marker-end="url(#ar)"/>
            <text class="bp-dim-text" x="${(x1 + x2) / 2}" y="${y - 6}" text-anchor="middle">${sh.label}</text>`;
    } else if (sh.t === 'dimv') {          // 垂直尺寸线
      const x = X(sh.x), y1 = Y(sh.y1), y2 = Y(sh.y2);
      s += `<line class="bp-dim" x1="${x - 4}" y1="${y1}" x2="${x + 4}" y2="${y1}"/>
            <line class="bp-dim" x1="${x - 4}" y1="${y2}" x2="${x + 4}" y2="${y2}"/>
            <line class="bp-dim" x1="${x}" y1="${y1}" x2="${x}" y2="${y2}" marker-start="url(#ar)" marker-end="url(#ar)"/>
            <text class="bp-dim-text" x="${x - 6}" y="${(y1 + y2) / 2}" text-anchor="end">${sh.label}</text>`;
    }
  }
  const el = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  el.setAttribute('viewBox', `0 0 ${W} ${H}`);
  el.style.width = '100%';
  el.style.height = '100%';
  el.innerHTML = `
    <defs>
      <marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M0,0 L10,5 L0,10 z" fill="var(--dim)"/>
      </marker>
    </defs>
    <rect x="0" y="0" width="${W}" height="${H}" fill="#0d2b4e"/>
    ${gridLines(W, H)}
    <text class="bp-title" x="16" y="26">${model.title}</text>
    <text class="bp-note" x="16" y="42">SCALE 1:${SCALE / 4} · SIDE VIEW · UNITS mm</text>
    ${s}
    <text class="bp-note" x="16" y="${H - 12}">${model.note}</text>`;
  // 给所有形状加"重绘动画"（stroke-dashoffset）
  requestAnimationFrame(() => {
    el.querySelectorAll('.bp-shape, .bp-dim, .bp-hidden').forEach((n, i) => {
      const len = 600;
      n.style.strokeDasharray = n.classList.contains('bp-hidden') ? '4 4' : len;
      if (!n.classList.contains('bp-hidden')) n.style.strokeDashoffset = len;
      n.style.transition = 'stroke-dashoffset .9s ease ' + (i * 0.05) + 's, opacity .6s ease';
    });
  });
  return el;
}
function gridLines(W, H) {
  let g = '';
  for (let x = 0; x <= W; x += 20) g += `<line x1="${x}" y1="0" x2="${x}" y2="${H}" stroke="#16406e" stroke-width="${x % 100 === 0 ? 1 : .4}"/>`;
  for (let y = 0; y <= H; y += 20) g += `<line x1="0" y1="${y}" x2="${W}" y2="${y}" stroke="#16406e" stroke-width="${y % 100 === 0 ? 1 : .4}"/>`;
  return g;
}

/* ================= Three.js 场景 ================= */
const canvas = document.getElementById('gl');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0b1d33);
scene.fog = new THREE.Fog(0x0b1d33, 18, 40);
const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
camera.position.set(6.5, 4.5, 8);
const controls = new OrbitControls(camera, canvas);
controls.target.set(0, 1.2, 0);
controls.enableDamping = true;
controls.enabled = false;   // 过渡完成后才允许交互

scene.add(new THREE.HemisphereLight(0xbfe3ff, 0x223344, 1.1));
const sun = new THREE.DirectionalLight(0xffffff, 1.6);
sun.position.set(5, 8, 4);
scene.add(sun);
const grid = new THREE.GridHelper(20, 20, 0x2b5a8c, 0x16324f);
scene.add(grid);

function resize() {
  const w = canvas.clientWidth, h = canvas.clientHeight;
  if (canvas.width !== w * renderer.getPixelRatio() || canvas.height !== h * renderer.getPixelRatio()) {
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
}
new ResizeObserver(resize).observe(canvas);

/* -------- 按零件清单程序化构建模型（场景图父子层级） -------- */
let modelGroup = null;
let turretNode = null;
const extrudeParts = [];   // 待"挤出"动画的零件

function buildModel(key) {
  if (modelGroup) scene.remove(modelGroup);
  modelGroup = new THREE.Group();
  turretNode = null;
  extrudeParts.length = 0;
  const def = MODELS[key];
  const nodes = {};
  for (const p of def.parts3d) {
    const mesh = new THREE.Mesh(p.geo(), new THREE.MeshStandardMaterial({ color: p.color, roughness: .6, metalness: .15 }));
    mesh.position.set(...p.pos);
    if (p.rot) mesh.rotation.set(...p.rot);
    mesh.name = p.name;
    nodes[p.name + '_' + Object.keys(nodes).length] = mesh;
    const parent = p.parent ? (p.parent === 'turret' ? getTurret() : modelGroup) : modelGroup;
    parent.add(mesh);
    // 初始态：压扁成"纸片"，等过渡动画挤出
    mesh.userData.finalScale = mesh.scale.clone();
    mesh.userData.finalY = mesh.position.y;
    mesh.scale.set(1, 0.02, 1);
    mesh.position.y = mesh.userData.finalY * 0.02;
    extrudeParts.push(mesh);
  }
  function getTurret() {
    if (!turretNode) {
      turretNode = new THREE.Group();
      turretNode.position.set(0, 1.1, 0);   // 炮塔基座挂点：车体顶面
      modelGroup.add(turretNode);
    }
    return turretNode;
  }
  scene.add(modelGroup);
}

/* -------- 过渡动画：纸片 → 立体（逐件 stagger） -------- */
let animStart = -1;
const STAGGER = 90, EXTRUDE_MS = 700, DRAW_MS = 900;

function startTransition() {
  // 图纸重绘
  const bp = document.getElementById('bp-svg-wrap');
  bp.querySelectorAll('.bp-shape').forEach(n => n.style.strokeDashoffset = '0');
  bp.style.transition = 'opacity 1s ease ' + (DRAW_MS + 600) + 'ms';
  bp.style.opacity = '0.25';
  animStart = performance.now();
  btnBuild.disabled = true;
}

const easeOutBack = t => { const c = 1.70158; return 1 + (c + 1) * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2); };

function tick(now) {
  requestAnimationFrame(tick);
  resize();
  if (animStart >= 0) {
    for (let i = 0; i < extrudeParts.length; i++) {
      const m = extrudeParts[i];
      const t = Math.min(Math.max((now - animStart - i * STAGGER) / EXTRUDE_MS, 0), 1);
      const e = easeOutBack(t);
      m.scale.y = 0.02 + 0.98 * e;
      m.position.y = m.userData.finalY * (0.02 + 0.98 * e);
    }
    if (now - animStart > extrudeParts.length * STAGGER + EXTRUDE_MS + 200) {
      animStart = -1;
      controls.enabled = true;   // 动画完才开放交互
    }
  }
  if (turretNode) turretNode.rotation.y += 0.003;  // 展示父子层级：转炮塔，炮管天线跟着转
  controls.update();
  renderer.render(scene, camera);
}
requestAnimationFrame(tick);

/* ================= UI 接线 ================= */
const bpWrap = document.getElementById('bp-svg-wrap');
const btnBuild = document.getElementById('btn-build');
const btnReset = document.getElementById('btn-reset');
const selModel = document.getElementById('sel-model');
const params = new URLSearchParams(location.search);

function resetAll(modelKey) {
  bpWrap.innerHTML = '';
  bpWrap.style.opacity = '1';
  bpWrap.appendChild(buildBlueprintSVG(MODELS[modelKey]));
  buildModel(modelKey);
  animStart = -1;
  controls.enabled = false;
  btnBuild.disabled = false;
}

btnBuild.addEventListener('click', startTransition);
btnReset.addEventListener('click', () => resetAll(selModel.value));
selModel.addEventListener('change', () => resetAll(selModel.value));

resetAll(params.get('model') || 'tank');
if (params.get('model')) selModel.value = params.get('model');

// 无头截图验证模式：?state=3d 直接跳到最终状态
if (params.get('state') === '3d') {
  document.getElementById('bp-svg-wrap').style.opacity = '0.25';
  for (const m of extrudeParts) {
    m.scale.y = m.userData.finalScale.y;
    m.position.y = m.userData.finalY;
  }
  controls.enabled = true;
}
// 测试钩子：渲染完成后向 DOM 报告零件数（供自动化检查）
setTimeout(() => {
  const d = document.createElement('div');
  d.id = 'stat';
  d.style.cssText = 'position:fixed;bottom:4px;right:8px;font:11px monospace;color:#35e0c3;z-index:50';
  d.textContent = `PARTS=${extrudeParts.length} DRAWCALLS=${renderer.info.render.calls} MODEL=${params.get('model') || selModel.value}`;
  document.body.appendChild(d);
}, 800);
