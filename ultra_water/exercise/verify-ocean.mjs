#!/usr/bin/env node
/**
 * Ultra-Water CPU verification at upstream 30ea65e.
 *
 * Evidence tiers:
 *  A. Directly import and execute upstream JS exports.
 *  B. Execute the private upstream jonswapParams function in a VM after only
 *     removing imports/ESM export keywords (no algorithm copied for this test).
 *  C. CPU-interpret the exact GLSL arithmetic and compare Stockham FFT against
 *     an independent naive DFT. This is NOT a GPU compile/render/fp16 test.
 */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';
import {
  N,
  CASCADE_LENGTHS,
  defaultOceanParams,
} from '../repo/src/water/OceanSim.js';

const sourcePath = fileURLToPath(new URL('../repo/src/water/OceanSim.js', import.meta.url));
const source = readFileSync(sourcePath, 'utf8');
let checks = 0;
const started = new Date().toISOString();
const metrics = {};

function check(name, fn) {
  fn();
  checks++;
  console.log(`PASS ${String(checks).padStart(2, '0')} ${name}`);
}
function near(actual, expected, tolerance = 1e-12, label = 'value') {
  assert.ok(Number.isFinite(actual), `${label}: non-finite ${actual}`);
  assert.ok(Math.abs(actual - expected) <= tolerance,
    `${label}: ${actual} != ${expected} (tol ${tolerance})`);
}
function maxAbs(values) { return Math.max(...values.map(Math.abs)); }
function fract(x) { return x - Math.floor(x); }

// Only expose the actual private upstream JS function; do not reimplement it here.
const instrumented = source
  .replace(/^import .*;\s*$/gm, '')
  .replace(/\bexport const /g, 'const ')
  .replace(/\bexport class /g, 'class ')
  + '\nglobalThis.__upstreamPure = { jonswapParams, COMMON, EVOLVE_FRAG, FFT_FRAG, ASSEMBLE_FRAG, G, SIGMA_RHO, LOOP };\n';
const sandbox = {};
vm.runInNewContext(instrumented, sandbox, { filename: 'OceanSim.js.instrumented-for-pure-test' });
const {
  jonswapParams, COMMON, EVOLVE_FRAG, FFT_FRAG, ASSEMBLE_FRAG,
  G, SIGMA_RHO: ST, LOOP,
} = sandbox.__upstreamPure;
assert.equal(typeof jonswapParams, 'function');

console.log('Ultra-Water ocean numerical verification');
console.log(`started=${started}`);
console.log(`source=${sourcePath}`);
console.log('scope=upstream JS execution + CPU GLSL arithmetic; no GPU claim');

check('direct upstream exports: fixed 256^2 radix-2 grid and four atlas cascades', () => {
  assert.equal(N, 256);
  assert.deepEqual([...CASCADE_LENGTHS], [600, 85, 12, 2.1]);
  assert.equal(Math.log2(N), 8);
  assert.equal(N * CASCADE_LENGTHS.length, 1024);
  metrics.atlas = [N, N * CASCADE_LENGTHS.length];
  metrics.cascadeTexelMetres = CASCADE_LENGTHS.map((L) => L / N);
});

check('cascade cuts are ordered and equal six fundamentals of the next cascade', () => {
  const cuts = CASCADE_LENGTHS.slice(1).map((L) => (2 * Math.PI / L) * 6);
  for (let i = 0; i < cuts.length; i++) {
    near(cuts[i], 12 * Math.PI / CASCADE_LENGTHS[i + 1], 1e-14, `cut${i}`);
    assert.ok(cuts[i] > 2 * Math.PI / CASCADE_LENGTHS[i]);
    if (i) assert.ok(cuts[i] > cuts[i - 1]);
  }
  assert.ok(source.includes('CASCADE_LENGTHS.slice(1).map((L) => (2 * Math.PI / L) * 6)'));
  metrics.cascadeCuts = cuts;
});

check('upstream update really runs horizontal + vertical, eight stages each', () => {
  assert.ok(source.includes('for (let dir = 0; dir < 2; dir++)'));
  assert.ok(source.includes('for (let s = 1; s <= LOG_N; s++)'));
  assert.ok(source.includes('fu.uSub.value = 1 << s'));
  assert.ok(source.includes('count: 2'));
  assert.ok(source.includes('q.render(r, dst)'));
  metrics.fftStagesPerFrame = 16;
});

check('defaultOceanParams returns independent, finite defaults', () => {
  const a = defaultOceanParams();
  const b = defaultOceanParams();
  assert.notEqual(a, b);
  assert.equal(a.windSpeed, 9);
  assert.equal(a.fetchKm, 120);
  assert.equal(a.capillaryFade, 0.08);
  a.windSpeed = 123;
  assert.equal(b.windSpeed, 9);
  for (const [key, value] of Object.entries(b)) {
    assert.ok(Number.isFinite(value), `${key} is not finite`);
  }
});

check('private upstream jonswapParams executes at normal UI-domain values', () => {
  const p = jonswapParams(9, 120);
  assert.ok(Number.isFinite(p.alpha) && p.alpha > 0);
  assert.ok(Number.isFinite(p.peakOmega) && p.peakOmega > 0);
  const expectedAlpha = 0.076 * Math.pow((9.81 * 120000) / 81, -0.22);
  const expectedPeak = 22 * Math.pow((9 * 120000) / (9.81 * 9.81), -0.33);
  near(p.alpha, expectedAlpha, 1e-15, 'alpha');
  near(p.peakOmega, expectedPeak, 1e-14, 'peakOmega');
  metrics.jonswapDefault = p;
});

check('upstream JONSWAP trends: stronger wind raises alpha and lowers peak omega', () => {
  const weak = jonswapParams(5, 120);
  const strong = jonswapParams(15, 120);
  assert.ok(strong.alpha > weak.alpha);
  assert.ok(strong.peakOmega < weak.peakOmega);
  const nearFetch = jonswapParams(9, 10);
  const farFetch = jonswapParams(9, 500);
  assert.ok(farFetch.alpha < nearFetch.alpha);
  assert.ok(farFetch.peakOmega < nearFetch.peakOmega);
});

check('boundary probe documents absent pure-function validation (zero/negative inputs)', () => {
  const cases = {
    zeroWind: jonswapParams(0, 120),
    zeroFetch: jonswapParams(9, 0),
    negativeWind: jonswapParams(-9, 120),
    negativeFetch: jonswapParams(9, -120),
  };
  for (const [name, p] of Object.entries(cases)) {
    assert.ok(!Number.isFinite(p.alpha) || !Number.isFinite(p.peakOmega),
      `${name} unexpectedly produced two finite values`);
  }
  metrics.jonswapInvalid = cases;
});

// --- CPU interpretation of upstream GLSL ---------------------------------------
const W0 = 2 * Math.PI / LOOP;
function omega(k) { return Math.sqrt(G * k + ST * k * k * k); }
function quantizedPhase(k, time) {
  return 2 * Math.PI * fract(Math.floor(omega(k) / W0) * (time / LOOP));
}
function jacobian(dxx, dzz, dxz) { return (1 + dxx) * (1 + dzz) - dxz * dxz; }
function foamStep(previous, jac, dt, recovery) {
  return Math.min(jac, previous + dt * recovery / Math.max(jac, 0.5));
}

check('CPU GLSL ports remain bound to evaluated upstream shader strings', () => {
  for (const [shader, snippet] of [
    [COMMON, 'float omega(float k) { return sqrt(G * k + ST * k * k * k); }'],
    [EVOLVE_FRAG, 'float ph = 2.0 * PI * fract(floor(omega(kl) / W0) * (uTime / 300.0));'],
    [ASSEMBLE_FRAG, 'float jac = (1.0 + dxx) * (1.0 + dzz) - dxz * dxz;'],
    [ASSEMBLE_FRAG, 'float turb = min(jac, prev + uDt * uFoamRecovery / max(jac, 0.5));'],
    [FFT_FRAG, 'out0 = vec4(e0.xy + cmul(tw, o0.xy), e0.zw + cmul(tw, o0.zw));'],
  ]) assert.ok(shader.includes(snippet), `missing upstream snippet: ${snippet}`);
});

check('capillary-gravity dispersion is monotone with correct limiting terms', () => {
  const ks = [0.001, 0.01, 0.1, 1, 10, 100, 1000];
  const values = ks.map((k) => ({ k, omega: omega(k), gravity: G * k, capillary: ST * k ** 3 }));
  for (let i = 0; i < values.length; i++) {
    const v = values[i];
    near(v.omega ** 2, v.gravity + v.capillary, Math.max(1e-9, v.omega ** 2 * 1e-14));
    if (i) assert.ok(v.omega > values[i - 1].omega);
  }
  assert.ok(values[1].capillary / values[1].gravity < 1e-8);
  assert.ok(values.at(-1).capillary / values.at(-1).gravity > 7);
  metrics.dispersion = values;
});

check('300 s quantized phase loops and half-period reverses odd modes', () => {
  const samples = [0.01, 0.1, 1, 10, 100, 1000];
  let oddChecked = false;
  for (const k of samples) {
    const n = Math.floor(omega(k) / W0);
    assert.ok(omega(k) - n * W0 >= 0 && omega(k) - n * W0 < W0);
    near(quantizedPhase(k, 0), 0, 0);
    near(quantizedPhase(k, LOOP), 0, 1e-12);
    near(quantizedPhase(k, 2 * LOOP), 0, 1e-12);
    near(quantizedPhase(k, 37.5), quantizedPhase(k, 337.5), 1e-12);
    if (n % 2 === 1) {
      const a = quantizedPhase(k, 0);
      const b = quantizedPhase(k, LOOP / 2);
      near(Math.cos(b), -Math.cos(a), 1e-12);
      near(Math.sin(b), -Math.sin(a), 1e-12);
      oddChecked = true;
    }
  }
  assert.ok(oddChecked);
  metrics.loopSeconds = LOOP;
});

check('Jacobian detects compression/expansion and foam recovery is dt-partition invariant', () => {
  near(jacobian(0, 0, 0), 1, 0);
  near(jacobian(-0.6, -0.6, 0), 0.16, 1e-15);
  near(jacobian(1, 1, 0), 4, 1e-15);
  near(jacobian(0, 0, 0.5), 0.75, 1e-15);
  assert.ok(foamStep(1, 0.16, 1 / 60, 0.7) === 0.16);
  function recover(steps) {
    let value = 0.16;
    for (let i = 0; i < steps; i++) value = foamStep(value, 0.8, 1 / steps, 0.7);
    return value;
  }
  near(recover(60), recover(6), 1e-15, 'dt partition');
  near(recover(60), 0.8, 1e-15, 'one second recovery clamps to jac');
  near(foamStep(0.16, 0.8, 0, 0.7), 0.16, 0, 'zero dt');
});

// Complex values are [real, imaginary]. This follows the upstream stage indexing;
// the oracle below is the independently evaluated O(N^4) 2D DFT definition.
function cmul(a, b) { return [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]]; }
function stockham1D(input) {
  const n = input.length;
  assert.ok(Number.isInteger(Math.log2(n)));
  let src = input.map((z) => [...z]);
  for (let sub = 2; sub <= n; sub *= 2) {
    const dst = Array.from({ length: n }, () => [0, 0]);
    const hs = sub >> 1;
    for (let i = 0; i < n; i++) {
      const e = Math.floor(i / sub) * hs + (i & (hs - 1));
      const angle = 2 * Math.PI * (i & (sub - 1)) / sub;
      const product = cmul([Math.cos(angle), Math.sin(angle)], src[e + n / 2]);
      dst[i] = [src[e][0] + product[0], src[e][1] + product[1]];
    }
    src = dst;
  }
  return src;
}
function stockham2D(input, n) {
  let data = input.map((z) => [...z]);
  for (let y = 0; y < n; y++) {
    const row = stockham1D(data.slice(y * n, (y + 1) * n));
    for (let x = 0; x < n; x++) data[y * n + x] = row[x];
  }
  const columns = [];
  for (let x = 0; x < n; x++) {
    const column = stockham1D(Array.from({ length: n }, (_, y) => data[y * n + x]));
    columns.push(column);
  }
  return data.map((_, i) => {
    const x = i % n, y = Math.floor(i / n), sign = ((x + y) & 1) ? -1 : 1;
    return [sign * columns[x][y][0], sign * columns[x][y][1]];
  });
}
function naiveDft2D(input, n) {
  const output = Array.from({ length: n * n }, () => [0, 0]);
  for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) {
    for (let ky = 0; ky < n; ky++) for (let kx = 0; kx < n; kx++) {
      const angle = 2 * Math.PI * (kx * x + ky * y) / n;
      const term = cmul(input[ky * n + kx], [Math.cos(angle), Math.sin(angle)]);
      output[y * n + x][0] += term[0];
      output[y * n + x][1] += term[1];
    }
  }
  // Match ASSEMBLE_FRAG's undo of the centred-k frequency shift.
  return output.map((z, i) => {
    const sign = ((i % n + Math.floor(i / n)) & 1) ? -1 : 1;
    return [sign * z[0], sign * z[1]];
  });
}
let randomState = 0x1337;
function random() {
  randomState = (Math.imul(randomState, 1664525) + 1013904223) >>> 0;
  return randomState / 4294967296;
}
function randomSpectrum(n) { return Array.from({ length: n * n }, () => [random() * 2 - 1, random() * 2 - 1]); }
function maxComplexError(a, b) {
  return Math.max(...a.map((z, i) => Math.hypot(z[0] - b[i][0], z[1] - b[i][1])));
}

check('upstream Stockham indexing matches independent naive 2D inverse DFT at N=4,8', () => {
  metrics.dftErrors = {};
  for (const n of [4, 8]) {
    const input = randomSpectrum(n);
    const actual = stockham2D(input, n);
    const expected = naiveDft2D(input, n);
    const error = maxComplexError(actual, expected);
    if (error >= 2e-11) console.log('DFT_DEBUG ' + JSON.stringify({ n, input, actual, expected }));
    assert.ok(error < 2e-11, `N=${n} error=${error}`);
    metrics.dftErrors[n] = error;
  }
});

check('centred sign undo is necessary; omission has a large DFT mismatch', () => {
  const n = 4, input = randomSpectrum(n);
  const transformed = stockham2D(input, n);
  const withoutSign = transformed.map((z, i) => ((i % n + Math.floor(i / n)) & 1) ? [-z[0], -z[1]] : z);
  assert.ok(maxComplexError(withoutSign, naiveDft2D(input, n)) > 0.1);
});

check('Hermitian spectrum gives real IFFT; pack2 recovers two real fields', () => {
  const n = 8;
  function hermitian() {
    const h = randomSpectrum(n);
    for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) {
      const nx = (n - x) % n, ny = (n - y) % n;
      const i = y * n + x, j = ny * n + nx;
      if (j < i) h[i] = [h[j][0], -h[j][1]];
    }
    for (const [x, y] of [[0, 0], [n / 2, 0], [0, n / 2], [n / 2, n / 2]]) h[y * n + x][1] = 0;
    return h;
  }
  const a = hermitian(), b = hermitian();
  const packed = a.map((z, i) => [z[0] - b[i][1], z[1] + b[i][0]]);
  const fieldA = stockham2D(a, n), fieldB = stockham2D(b, n), fieldPacked = stockham2D(packed, n);
  assert.ok(maxAbs(fieldA.map((z) => z[1])) < 2e-11);
  assert.ok(maxAbs(fieldB.map((z) => z[1])) < 2e-11);
  const reconstructionError = Math.max(...fieldPacked.map((z, i) => Math.max(
    Math.abs(z[0] - fieldA[i][0]), Math.abs(z[1] - fieldB[i][0]),
  )));
  assert.ok(reconstructionError < 2e-11);
  metrics.pack2ReconstructionError = reconstructionError;
  metrics.hermitianImaginaryMax = maxAbs(fieldA.map((z) => z[1]));
});

console.log(`SUMMARY checks=${checks} status=PASS gpu=NOT_TESTED`);
console.log('METRICS ' + JSON.stringify(metrics));
