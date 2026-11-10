// 自写离线学习实验；只执行真实的纯 mountOnce 模块，其余源仅作为数据。
// Source: https://github.com/zhu1090093659/dsh-web/blob/29e4dc579d6cd691f0987925ff3fdd769bb77823/shared/host/mount-once.ts
// No host initialization, timers/schedules, SSH engine, model client, install scripts or credentials.
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import {performance} from 'node:perf_hooks';
const root=resolve(import.meta.dirname,'..'),stage=process.argv[2]??'all';
const read=(p)=>readFileSync(resolve(root,p),'utf8');
const data=(p)=>JSON.parse(read(p));
const want=(s)=>stage==='all'||stage===s;
let checks=0;const check=(s,v)=>{assert.ok(v,s);checks++;console.log('PASS '+s)};
const prefix='evidence/zhu1090093659/dsh-web/';
globalThis.fetch=()=>{throw Error('network not allowed in this audited lab path')};
if(want('catalog')){
 const rows=data('evidence/catalog-leads.json'),probes=data('evidence/repo-probes.json');
 check('57 article entries',rows.length===57);
 check('52 distinct repository roots',new Set(rows.map(x=>x.repo)).size===52);
 check('51 public metadata successes',Object.values(probes).filter(x=>x.http===200).length===51);
 check('one HTTP404 observation',Object.values(probes).filter(x=>x.http===404).length===1);
 const groups={};for(const x of rows)(groups[x.name.replace(/（.*?）/g,'').toLowerCase()]??=[]).push(x.repo);
 const same=Object.entries(groups).filter(([,v])=>v.length>1);console.log('same display-name groups',JSON.stringify(same));
 check('2 same-display-name groups',same.length===2);
 check('same display name does not mean same repository',same.every(([,v])=>new Set(v).size===2));
 console.log('HTTP404 is a point-in-time response, not proof of permanent nonexistence.');
}
if(want('overlap')){
 const all=data(prefix+'packages/dsh-web-all/package.json'),task=data(prefix+'packages/dsh-task-board/package.json'),ssh=data(prefix+'packages/dsh-ssh/package.json');
 const duplicates=[task.name,ssh.name].filter(n=>n in all.dependencies);
 console.log('aggregate dependencies',Object.keys(all.dependencies).length,'redundant selections',JSON.stringify(duplicates));
 check('aggregate contains task-board and SSH dependencies',duplicates.length===2);
 const patch=read(prefix+'packages/dsh-web-all/cordis.patch.yml');
 // Static name extraction ONLY. Never evaluate YAML !!js tags, parse no functions.
 const names=[...patch.matchAll(/^\s+name: ['"]?([^'"\n]+)['"]?$/gm)].map(x=>x[1].trim());
 check('aggregate patch really mounts both package names',duplicates.every(n=>names.includes(n)));
 const taskPatch=read(prefix+'packages/dsh-task-board/cordis.patch.yml');
 check('standalone and aggregate have different row IDs',taskPatch.includes('id: ui-task-board')&&patch.includes('id: web-ui-task-board'));
 check('both task/SSH use package-name mountOnce',read(prefix+'packages/dsh-task-board/src/index.ts').includes(`mountOnce('${task.name}'`)&&read(prefix+'packages/dsh-ssh/src/index.ts').includes(`mountOnce('${ssh.name}'`));
 console.log('Static overlap != actual startup failure: current code has a guard.');
}
if(want('guard')){
 const path=pathToFileURL(resolve(root,prefix+'shared/host/mount-once.ts')).href;
 const {mountOnce}=await import(path+'?copy=A');const copy=await import(path+'?copy=B');
 function ctx(){const ds=[];return {effect:fn=>{const d=fn();if(typeof d==='function')ds.push(d)},dispose:()=>{for(const d of ds.splice(0).reverse())d()}}}
 const settle=async()=>{await Promise.resolve();await Promise.resolve()};
 let calls=[];const apply=mountOnce('LAB/ssh',(c,x)=>calls.push(x));
 let a=ctx(),b=ctx();apply(a,'A');apply(b,'B');check('only holder mounts',calls.join()==='A');a.dispose();await settle();check('waiter takes over after dispose',calls.join()==='A,B');b.dispose();
 calls=[];a=ctx();b=ctx();apply(a,'A');apply(b,'B');b.dispose();a.dispose();await settle();check('disposed waiter is not resurrected',calls.join()==='A');
 calls=[];a=ctx();b=ctx();const c=ctx();apply(a,'A');apply(b,'B');apply(c,'C');a.dispose();await settle();check('several waiters keep one next owner',calls.join()==='A,B');b.dispose();await settle();check('second waiter handover',calls.join()==='A,B,C');c.dispose();
 calls=[];a=ctx();b=ctx();mountOnce('LAB/shared',()=>calls.push('first'))(a);copy.mountOnce('LAB/shared',()=>calls.push('second'))(b);check('separate module copies share global registry',calls.join()==='first');b.dispose();a.dispose();
 calls=[];a=ctx();b=ctx();mountOnce('LAB/pkgA',()=>calls.push('A'))(a);mountOnce('LAB/pkgB',()=>calls.push('B'))(b);check('different package names mount independently',calls.join()==='A,B');a.dispose();b.dispose();
 const key=Symbol.for('dsh-web.mounted-plugins');globalThis[key]=new Map();a=ctx();mountOnce('LAB/foreign',()=>{})(a);check('foreign registry shape repaired to Set',globalThis[key] instanceof Set);a.dispose();
 check('all synthetic package names released',globalThis[key].size===0);
 console.log('Real mountOnce; fake ctx.effect/dispose; no DSH loader, browser or SSH connection.');
}
if(want('cost')){
 const files=[
 ['context','evidence/ranxianglei/billion-context/package.json'],['sidebar','evidence/omdsh-dev/DSH-better-sidebar/package.json'],['task',prefix+'packages/dsh-task-board/package.json'],['ssh',prefix+'packages/dsh-ssh/package.json'],['all',prefix+'packages/dsh-web-all/package.json']];
 const result=[];
 for(const [label,p]of files){const text=read(p),j=JSON.parse(text);let checksum=0;const samples=[];for(let k=0;k<7;k++){const t=performance.now();for(let i=0;i<2000;i++)checksum+=Object.keys(JSON.parse(text)).length;samples.push((performance.now()-t)/2000)}samples.sort((a,b)=>a-b);const row={label,name:j.name,manifestBytes:Buffer.byteLength(text),prodDeps:Object.keys(j.dependencies??{}).length,peerDeps:Object.keys(j.peerDependencies??{}).length,parseMedianMs:samples[3],iterations:14000,checksum};result.push(row);console.log(JSON.stringify(row));check(label+' parse workload actually ran',checksum>0)}
 check('all manifest fan-out is greater than 2 selections',result.find(x=>x.label==='all').prodDeps>2);
 writeFileSync(resolve(root,'evidence/static-cost.json'),JSON.stringify(result,null,2));
 console.log('Timing measures warm JSON.parse + Object.keys ONLY; not plugin startup/import/render/network latency.');
}
console.log(`RESULT stage=${stage}; checks=${checks}; model/SSH/host not invoked`);
