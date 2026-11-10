// Source: https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/ ; npm @earendil-works/pi-coding-agent@0.84.2
// Harness reused from prior audit; run status is recorded separately. No main CLI/model invocation.
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import { isInstallTelemetryEnabled } from './package/dist/core/telemetry.js';
import { getPiUserAgent } from './package/dist/utils/pi-user-agent.js';
const source = fs.readFileSync('package/dist/modes/interactive/interactive-mode.js','utf8');
const start = source.indexOf('    reportInstallTelemetry(version) {');
assert(start >= 0, 'method marker missing: stop rather than guessing');
const end = source.indexOf('    getMarkdownThemeWithSettings()', start);
assert(end > start, 'end marker missing');
const method = source.slice(start,end).trim();
assert(method.endsWith('}'));
for (const c of [
 {flag:undefined, offline:undefined, setting:true, count:1},
 {flag:'0', offline:undefined, setting:true, count:0},
 {flag:undefined, offline:'1', setting:true, count:0},
 {flag:undefined, offline:'0', setting:true, count:0},
 {flag:undefined, offline:undefined, setting:false, count:0},
]) {
 const calls=[];
 const context={
  process:{env:{PI_OFFLINE:c.offline}},
  isInstallTelemetryEnabled:()=>isInstallTelemetryEnabled(
   {getEnableInstallTelemetry:()=>c.setting}, c.flag??''
  ),
  getPiUserAgent,
  AbortSignal:{timeout:ms=>({mockTimeoutMs:ms})},
  fetch:(url,opts)=>{calls.push({url,opts}); return Promise.resolve({});},
 };
 // For an unset flag, select the setting directly without reading host env.
 if (c.flag===undefined) context.isInstallTelemetryEnabled=()=>c.setting;
 vm.runInNewContext('(function '+method+').call({settingsManager:{}}, "0.84.2")',
                    context, {timeout:1000});
 assert.equal(calls.length,c.count);
 if(c.count) {
  assert.equal(calls[0].url,'https://pi.dev/api/report-install?version=0.84.2');
  assert.equal(calls[0].opts.body,undefined);
  assert.equal(calls[0].opts.signal.mockTimeoutMs,5000);
  assert.match(calls[0].opts.headers['User-Agent'], /^pi\/0\.84\.2 /);
  console.log(JSON.stringify(calls[0]));
 }
 console.log('branch',JSON.stringify(c),'mock requests',calls.length);
}
console.log('PASS: 5 mocked branches; no real fetch or model invocation');
