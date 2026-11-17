const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
require('esbuild').buildSync({
  entryPoints: [path.join(root, 'src/workbench.ts')],
  outfile: path.join(root, 'out/workbench-manifest.cjs'),
  bundle: true,
  platform: 'node',
  format: 'cjs',
  packages: 'external',
  logLevel: 'warning',
});
const { WORKBENCH } = require(path.join(root, 'out/workbench-manifest.cjs'));
assert.equal(WORKBENCH.total, 180);
assert.equal(WORKBENCH.fps, 30);
assert.equal(WORKBENCH.shots.length, 2);
assert.equal(WORKBENCH.transitions.length, 1);
assert.equal(WORKBENCH.captions.length, 1);
assert.equal(WORKBENCH.sfx.length, 3);
assert.deepEqual(WORKBENCH.shots.map((s) => [s.from, s.duration]), [[0, 90], [90, 90]]);
assert.deepEqual(WORKBENCH.sfx.map((s) => s.from), [14, 53, 100]);
for (const unit of [...WORKBENCH.shots, ...WORKBENCH.transitions, ...WORKBENCH.captions]) {
  assert.equal(typeof unit.component, 'function', `${unit.id}: component missing`);
  assert.ok(Number.isFinite(unit.from) && Number.isFinite(unit.duration), `${unit.id}: timing missing`);
}
for (const shot of WORKBENCH.shots) {
  assert.ok(shot.schema.length >= 4, `${shot.id}: editable schema missing`);
  for (const field of shot.schema) assert.ok(field.key in shot.props, `${shot.id}: ${field.key} default missing`);
}
const serializable = {
  name: WORKBENCH.name,
  fps: WORKBENCH.fps,
  width: WORKBENCH.width,
  height: WORKBENCH.height,
  total: WORKBENCH.total,
  shots: WORKBENCH.shots.map(({ component, ...s }) => ({ ...s, component: component.name })),
  transitions: WORKBENCH.transitions.map(({ component, ...s }) => ({ ...s, component: component.name })),
  captions: WORKBENCH.captions.map(({ component, ...s }) => ({ ...s, component: component.name })),
  sfx: WORKBENCH.sfx,
  note: 'The real TS manifest was bundled and evaluated. This is not a browser-UI or pixel-parity test.',
};
fs.writeFileSync(path.join(root, 'out/workbench-manifest.json'), JSON.stringify(serializable, null, 2));
console.log(JSON.stringify({ status: 'passed', tracks: { shots: 2, transitions: 1, captions: 1, sfx: 3 }, sfxFrom: [14, 53, 100], note: serializable.note }, null, 2));
