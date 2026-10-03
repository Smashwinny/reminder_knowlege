// logic.js — 复刻像素风 3D 网站的四个核心逻辑件（纯函数/类，浏览器与 Node 共用）
// 1) 网格碰撞  2) 对话状态机  3) 场景切换器  4) 多人位置同步（延迟+插值）
// 不依赖 three.js：玩法逻辑和渲染引擎分离，正是推文第 2 点"核心逻辑=Gameplay"的工程体现。

// ---------- 1. 网格地图与碰撞 ----------
// 地图 = 字符串数组。'#'=墙 ' '=空地 'D'=门(切换场景) 'N'=NPC。小人用圆形碰撞体。
function makeGrid(rows) {
  const h = rows.length, w = rows[0].length;
  const tiles = [];
  for (let y = 0; y < h; y++) {
    tiles.push([]);
    for (let x = 0; x < w; x++) tiles[y].push(rows[y][x]);
  }
  return { w, h, tiles };
}
function tileAt(grid, tx, ty) {
  if (tx < 0 || ty < 0 || tx >= grid.w || ty >= grid.h) return '#';
  return grid.tiles[ty][tx];
}
// 圆形碰撞体 vs 墙块（AABB）：把小人周围 3x3 格里的墙都当成方块，做圆-方相交测试
function hitsWall(grid, ts, x, y, r) {
  const tx0 = Math.floor((x - r) / ts), tx1 = Math.floor((x + r) / ts);
  const ty0 = Math.floor((y - r) / ts), ty1 = Math.floor((y + r) / ts);
  for (let ty = ty0; ty <= ty1; ty++) {
    for (let tx = tx0; tx <= tx1; tx++) {
      if (tileAt(grid, tx, ty) !== '#') continue;
      const cx = Math.max(tx * ts, Math.min(x, (tx + 1) * ts));
      const cy = Math.max(ty * ts, Math.min(y, (ty + 1) * ts));
      const dx = x - cx, dy = y - cy;
      if (dx * dx + dy * dy < r * r) return true;
    }
  }
  return false;
}
// 轴分离移动：先动 X 再动 Z；撞墙的轴精确钳到"贴墙"位置——"贴墙滑行"手感的关键。
// 做法：把扫过的格子都看一遍，路径上遇到墙就算出"贴墙"的极限坐标，取最紧的一个钳住。
function moveWithCollision(grid, ts, pos, vx, vz, dt, r) {
  const clampAxis = (isX, d) => {
    if (d === 0) return;
    const dir = Math.sign(d);
    const lead = isX ? pos.x : pos.y;                     // 移动轴当前坐标
    const target = lead + d;
    const perp = isX ? pos.y : pos.x;                     // 垂直轴坐标
    const EPS = 1e-9;                                     // 相切(距离恰=r)不算撞
    const perp0 = Math.floor((perp - r + EPS) / ts), perp1 = Math.floor((perp + r - EPS) / ts);
    const a0 = dir > 0 ? Math.floor((lead - EPS) / ts) : Math.floor((target - r + EPS) / ts);
    const a1 = dir > 0 ? Math.floor((target + r - EPS) / ts) : Math.floor((lead + EPS) / ts);
    let lim = target;
    for (let p = perp0; p <= perp1; p++) {
      for (let a = a0; a <= a1; a++) {
        const ch = isX ? tileAt(grid, a, p) : tileAt(grid, p, a);
        if (ch !== '#') continue;
        const wall = dir > 0 ? a * ts : (a + 1) * ts;     // 挡在前面的那一面
        const allowed = dir > 0 ? wall - r : wall + r;
        lim = dir > 0 ? Math.min(lim, allowed) : Math.max(lim, allowed);
      }
    }
    if (isX) pos.x = lim; else pos.y = lim;
  };
  clampAxis(true, vx * dt);
  clampAxis(false, vz * dt);
  return pos;
}

// ---------- 2. 对话状态机 ----------
// closed --open--> typing --打完字--> waiting --advance--> 下一条 typing ... 最后一条后 --> closed
class DialogueFSM {
  constructor(lines, charsPerSec = 20) {
    this.lines = lines; this.cps = charsPerSec;
    this.state = 'closed'; this.idx = 0; this.shown = 0; this._t = 0;
  }
  open() { if (this.state !== 'closed') return false;
    this.state = 'typing'; this.idx = 0; this.shown = 0; this._t = 0; return true; }
  // 返回 true 表示这一下"推进"被消化了（跳过打字或翻页），false 表示本来就关着
  advance() {
    const line = this.lines[this.idx] || '';
    if (this.state === 'typing' && this.shown < line.length) {
      this.shown = line.length; this.state = 'waiting'; return true;
    }
    if (this.state === 'waiting') {
      this.idx++; this.shown = 0; this._t = 0;
      if (this.idx >= this.lines.length) { this.state = 'closed'; } else { this.state = 'typing'; }
      return true;
    }
    return false;
  }
  update(dt) {
    if (this.state !== 'typing') return;
    this._t += dt * this.cps;
    const line = this.lines[this.idx] || '';
    while (this.shown < line.length && this._t >= 1) { this.shown++; this._t -= 1; }
    if (this.shown >= line.length) this.state = 'waiting';
  }
  get text() { return (this.lines[this.idx] || '').slice(0, this.shown); }
}

// ---------- 3. 场景切换器 ----------
// 每个"场景"= { name, grid, spawn(入口点), exits: {'D': targetSceneName} }
// 站上门格 D 时按 exits 跳转并把玩家放到目标场景的 spawn。
class SceneManager {
  constructor(scenes, startName) {
    this.scenes = scenes; this.current = startName;
    this.fade = 0;            // >0 表示切换过场中，画面压黑
    this.pending = null;      // {scene, spawn}
  }
  // 每帧检查：脚下格子是 D 就发起切换（fade 半程真正换场景）
  update(dt, playerTile) {
    if (this.fade > 0) {
      this.fade -= dt;
      if (this.fade <= 0.15 && this.pending) {   // 半程：真的换
        this.current = this.pending.scene;
        this.pending = null;
      }
      return true;
    }
    const t = playerTile;
    const sc = this.scenes[this.current];
    if (t && t.char === 'D' && sc.exits[t.char]) {
      this.pending = { scene: sc.exits[t.char] };
      this.fade = 0.6;
      return true;
    }
    return false;
  }
}

// ---------- 4. 多人位置同步（收包延迟 + 渲染插值） ----------
// 远端玩家每 tick 上报位置；因为网络延迟 T_delay，本地在"过去"的时间轴上渲染，
// 收到两个样本后对 renderTime = now - delay 做线性插值——这就是"简单位置同步"的最小可用版。
class NetSync {
  constructor(delay = 0.1) {
    this.delay = delay; this.samples = []; // [{t, x, y}]
  }
  push(t, x, y) { this.samples.push({ t, x, y }); if (this.samples.length > 60) this.samples.shift(); }
  // 渲染时刻 now，其实想看的是 now-delay 那一刻远端在哪
  sample(now) {
    const rt = now - this.delay;
    const s = this.samples;
    if (s.length === 0) return null;
    if (rt <= s[0].t) return { x: s[0].x, y: s[0].y };
    for (let i = 1; i < s.length; i++) {
      if (rt <= s[i].t) {
        const a = s[i - 1], b = s[i];
        const k = (rt - a.t) / (b.t - a.t);
        return { x: a.x + (b.x - a.x) * k, y: a.y + (b.y - a.y) * k };
      }
    }
    return { x: s[s.length - 1].x, y: s[s.length - 1].y }; // 还没收到更新的包：停在最新位置
  }
}

export { makeGrid, tileAt, hitsWall, moveWithCollision, DialogueFSM, SceneManager, NetSync };
