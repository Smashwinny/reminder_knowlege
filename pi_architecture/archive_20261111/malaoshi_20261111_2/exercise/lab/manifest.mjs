// Source: https://github.com/earendil-works/pi/blob/914cf1472e715297caa30db4b9535d534a9eb718/packages/coding-agent/ ; npm @earendil-works/pi-coding-agent@0.84.2
// Harness reused from prior audit; run status is recorded separately. No main CLI/model invocation.
import fs from 'node:fs';
import assert from 'node:assert/strict';
const p = JSON.parse(fs.readFileSync('package/package.json','utf8'));
assert.equal(p.name, '@earendil-works/pi-coding-agent');
assert.equal(p.version, '0.84.2');
const names = Object.keys(p.dependencies);
assert(!names.includes('@earendil-works/pi-mcp'));
assert(!names.includes('@earendil-works/pi-codemode'));
assert(names.includes('@earendil-works/pi-client'));
assert(names.includes('@earendil-works/pi-protocol'));
assert.equal(p.bin.pi, 'dist/cli.js');
assert(p.exports['./client']);
assert(fs.readFileSync('package/README.md','utf8').includes('**No MCP.**'));
console.log(p.name+'@'+p.version);
console.log('own deps:', names.filter(n=>n.startsWith('@earendil-works/')).join(','));
console.log('PASS: version/dependencies/exports; not a runtime MCP conformance test');
