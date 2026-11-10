// Original source: https://github.com/SiriLee/dsh-rewind/blob/f5668ded87eb5c230916e288f26a887c633b4154/src/snapshot-format.ts
// Source: SiriLee/dsh-rewind f5668ded87eb5c230916e288f26a887c633b4154 src/snapshot-format.ts
// Tests real codecs/validators, NOT actual session rewind or file restoration.
import assert from 'node:assert/strict';import fs from 'node:fs/promises';
const {safeSessionId,isSafeLinkRef,isSafeBackupRef,textSourceOf,readEntry,UnknownStoreVersionError}=await import('./upstream/dsh-rewind/src/snapshot-format.ts');
const checks=[['session-dot',safeSessionId('..'),'session'],['session-slashes',safeSessionId('../x'),'.._x'],['link-valid',isSafeLinkRef('12/call_1.json'),true],['link-traversal',isSafeLinkRef('../a.json'),false],['link-absolute',isSafeLinkRef('/12/a.json'),false],['backup-valid',isSafeBackupRef('12/a.before'),true],['rescue-valid',isSafeBackupRef('rescue/op/1.before'),true],['backup-traversal',isSafeBackupRef('12/../a.before'),false],['backup-backslash',isSafeBackupRef('12\\a.before'),false],['plain-utf8',textSourceOf('你好').kind,'text'],['lossy-utf8',textSourceOf('\uFFFD').kind,'lossyText']];
for(const[label,got,want]of checks){assert.equal(got,want);console.log(JSON.stringify({label,got,want}));}
const dir=new URL('./fixtures/rewind/',import.meta.url);await fs.mkdir(dir,{recursive:true});const f=new URL('entry.json',dir);
await fs.writeFile(f,JSON.stringify({store:99}));await assert.rejects(()=>readEntry(f.pathname,1),UnknownStoreVersionError);console.log('future store=99: UnknownStoreVersionError (fail closed)');
await fs.writeFile(f,'{broken');assert.equal(await readEntry(f.pathname,1),undefined);console.log('corrupt JSON: undefined (not guessed into a delete)');
await fs.writeFile(f,JSON.stringify({store:2,file:'fixture.txt',blob:null,size:2}));assert.equal(await readEntry(f.pathname,1),undefined);console.log('inconsistent absent-file marker with size=2: rejected');
assert.equal(globalThis.__networkAttempts.length,0);console.log('PASS: 11 validators/byte classifications + 3 codec cases; network attempts=0; no real restore');
