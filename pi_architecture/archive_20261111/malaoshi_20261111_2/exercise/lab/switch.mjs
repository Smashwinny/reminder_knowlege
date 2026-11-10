// Source: https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/ ; npm @earendil-works/pi-coding-agent@0.84.2
// Harness reused from prior audit; run status is recorded separately. No main CLI/model invocation.
import assert from 'node:assert/strict';
import { isInstallTelemetryEnabled } from './package/dist/core/telemetry.js';
const settingOn = { getEnableInstallTelemetry:()=>true };
const settingOff = { getEnableInstallTelemetry:()=>false };
// 清除默认参数可能读取的进程变量，仅影响本实验进程。
delete process.env.PI_TELEMETRY;
const cases = [
 [settingOn, undefined, true], [settingOff, undefined, false],
 [settingOn, '0', false], [settingOn, 'false', false],
 [settingOn, 'no', false], [settingOn, '', false],
 [settingOn, 'garbage', false], [settingOff, '1', true],
 [settingOff, 'TRUE', true], [settingOff, 'yes', true],
];
for (const [s,e,want] of cases) {
 const got = isInstallTelemetryEnabled(s,e);
 assert.equal(got,want);
 console.log(JSON.stringify({env:e??'<unset>',setting:s.getEnableInstallTelemetry(),got}));
}
console.log('PASS: 10 telemetry-switch cases; no fetch or model invocation');
