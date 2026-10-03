// logic_test.mjs — 四个 Gameplay 逻辑件的 Node 侧真实测试（不需要浏览器/显卡）
import { makeGrid, hitsWall, moveWithCollision, DialogueFSM, SceneManager, NetSync } from './js/logic.js';

let pass = 0, fail = 0;
function check(name, cond, extra = '') {
  if (cond) { pass++; console.log(`PASS  ${name}${extra ? '  (' + extra + ')' : ''}`); }
  else { fail++; console.log(`FAIL  ${name}${extra ? '  (' + extra + ')' : ''}`); }
}

// ===== 1. 网格碰撞：撞墙停 + 贴墙滑 =====
const g = makeGrid([
  '#######',
  '#     #',
  '# ### #',
  '#     #',
  '#######',
]);
const TS = 1, R = 0.3;
check('空地中心不撞墙', !hitsWall(g, TS, 1.5, 1.5, R));
check('贴墙位置撞墙', hitsWall(g, TS, 1.2, 1.5, R));          // 离左墙 0.2 < 半径 0.3
check('越界算墙', hitsWall(g, TS, -0.5, 1.5, R));

// 在中央墙块所在行（y=2.5，块占 y∈[2,3) x∈[2,5)）向右走：x 方向被拦，y 方向仍可滑
const pos = { x: 1.5, y: 2.5 };
moveWithCollision(g, TS, pos, 3, 0, 1.0, R);   // 尝试右移 3 格
check('撞中央墙块 x 被拦', Math.abs(pos.x - 1.7) < 1e-9, `x=${pos.x.toFixed(3)}`);
moveWithCollision(g, TS, pos, 0, -3, 1.0, R);  // 向下滑，应能滑过墙块侧面
check('贴墙滑行 y 可动', pos.y < 2.5, `y=${pos.y.toFixed(3)}`);

// ===== 2. 对话状态机：打字机 → 等待 → 翻页 → 关闭 =====
const dlg = new DialogueFSM(['你好，旅行者。', '北边的门后面是屋子。'], 20);
check('初始关闭', dlg.state === 'closed');
check('advance 在关闭时无效', dlg.advance() === false);
dlg.open();
check('open 后进入打字', dlg.state === 'typing');
dlg.update(0.1); check('打字 0.1s@20字/s = 2 字', dlg.text === '你好', `text="${dlg.text}"`);
dlg.advance(); check('advance 跳过打字', dlg.state === 'waiting' && dlg.text === '你好，旅行者。');
dlg.advance(); check('翻到第二句', dlg.state === 'typing' && dlg.text === '');
dlg.advance(); check('第二句秒读完', dlg.state === 'waiting' && dlg.text === '北边的门后面是屋子。');
dlg.advance(); check('最后一句后关闭', dlg.state === 'closed');

// ===== 3. 场景切换：踩门格 → fade 过场 → 半程换场景 =====
const scenes = {
  village: { name: 'village', grid: g, spawn: { x: 1.5, y: 1.5 }, exits: { D: 'house' } },
  house:   { name: 'house', grid: makeGrid(['###', '#D#', '###']), spawn: { x: 1.5, y: 1.5 }, exits: { D: 'village' } },
};
const sm = new SceneManager(scenes, 'village');
check('初始场景 village', sm.current === 'village');
const idle = sm.update(0.1, { char: ' ' });
check('非门格不触发', idle === false && sm.current === 'village');
let switching = false;
switching = sm.update(0.1, { char: 'D' });
check('踩门格发起过场 fade=0.6（发起帧不扣时）', switching && Math.abs(sm.fade - 0.6) < 1e-9, `fade=${sm.fade.toFixed(2)}`);
sm.update(0.2); sm.update(0.35);              // 共 0.55s：已过半程(0.6-0.15=0.45)
check('半程已换到 house', sm.current === 'house', `current=${sm.current}`);
check('过场结束 fade 归零', (sm.update(0.3), sm.fade <= 0));

// ===== 4. 位置同步：100ms 延迟下渲染的是"过去"的位置，两包之间线性插值 =====
const net = new NetSync(0.1);
check('没包时返回 null', net.sample(1.0) === null);
net.push(1.0, 0, 0);
net.push(1.2, 2, 0);
const s1 = net.sample(1.2);                    // 想看 1.1 时刻 → 在两包之间 k=(1.1-1.0)/0.2=0.5
check('延迟后取的是过去时刻', Math.abs(s1.x - 1.0) < 1e-9, `x=${s1.x}`);
check('y 不漂移', s1.y === 0);
const s2 = net.sample(2.0);                    // 想看 1.9，但最新包只有 1.2 → 停在最新位置
check('断流时停在最新包', s2.x === 2 && s2.y === 0, `x=${s2.x}`);
const s3 = net.sample(1.05);                   // 早于首包 → 夹到首包
check('早于首包夹住', s3.x === 0);

console.log(`\nTOTAL: ${pass} pass, ${fail} fail`);
process.exit(fail ? 1 : 0);
