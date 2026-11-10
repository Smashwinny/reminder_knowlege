// 自写离线夹具；真实被测代码来自 ZiChuanLan/pi-purge。
// current SHA efb87cc06b0882ba90bd90e21413d1f7e1a65cbb
// pinned SHA ffafeb940339d59fc6af4a05dc754019cef3a1ac (only persona redacted)
// https://github.com/ZiChuanLan/pi-purge/blob/<SHA>/extensions/pi-purge.ts
// Pi sources: 0.84.2=914cf1472e715297caa30db4b9535d534a9eb718;
// latest=b30d54b8aebe6408e02d1473446d25f8083da68f. No model client imported.
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {stripTypeScriptTypes} from 'node:module';
import vm from 'node:vm';
import {pathToFileURL} from 'node:url';
import {resolve,dirname} from 'node:path';
const root=resolve(import.meta.dirname,'..');
const stage=process.argv[2]??'all';
const want=(n)=>stage==='all'||stage===n;
let checks=0;
function check(name,condition){assert.ok(condition,name);checks++;console.log('PASS '+name)}
// Guard is a precaution for audited code path, not an OS sandbox/network audit.
globalThis.fetch=()=>{throw Error('Network forbidden in offline lab')};
delete process.env.PI_PURGE_SOURCE;
const get=(p)=>readFileSync(resolve(root,'evidence',p),'utf8');
function hostPrompt(label){
 const source=get(label+'/packages/coding-agent/src/core/system-prompt.ts');
 const noImports=source.replace(/^import .*;\n/gm,'');
 const js=stripTypeScriptTypes(noImports,{mode:'strip'}).replace(/export /g,'');
 const ctx={getReadmePath:()=>'/LAB/README.md',getDocsPath:()=>'/LAB/docs',getExamplesPath:()=>'/LAB/examples',formatSkillsForPrompt:()=>'<skills>LAB_SKILL</skills>'};
 const fn=label==='pi-0842'?'buildSystemPrompt':'buildSystemPromptSections';
 // Original builder code; only config-path and skills-renderer seams are stubs.
 return vm.runInNewContext(js+`; ${fn}`,ctx,{timeout:1000});
}
const opts={cwd:'C:\\LAB',selectedTools:['read','bash'],toolSnippets:{read:'Read',bash:'Shell'},contextFiles:[{path:'/LAB/AGENTS.md',content:'LAB_PROJECT_RULE'}],skills:[{name:'lab'}]};
const old=hostPrompt('pi-0842')(opts);
// Current builder returns structured sections: join here is a fixture renderer,
// not pi-ai serializer integration. Marker presence is independent of separators.
const cur=Object.values(hostPrompt('pi-latest')(opts)).join('\n\n');
async function load(label){
 const events=new Map(),commands=new Map(),notes=[];
 const mod=await import(pathToFileURL(resolve(root,'evidence',label,'extensions/pi-purge.ts')).href+'?isolated='+Math.random());
 mod.default({on:(k,v)=>events.set(k,v),registerCommand:(k,v)=>commands.set(k,v)});
 const ctx={ui:{setStatus:()=>{},notify:(text,level)=>notes.push({text,level})}};
 return {notes,start:()=>events.get('session_start')({},ctx),cmd:(s)=>commands.get('purge').handler(s,ctx),inject:(systemPrompt=old,options={cwd:'C:\\LAB'})=>events.get('before_agent_start')({systemPrompt,systemPromptOptions:options},ctx)};
}
if(want('modes')){
 for(const label of ['purge-current','purge-post']){
  const a=await load(label);await a.start();
  check(label+' default disabled',(await a.inject())===undefined);
  await a.cmd('on');
  const strict=(await a.inject()).systemPrompt;
  check(label+' strict retains cwd',strict.endsWith('Current working directory: C:/LAB'));
  check(label+' strict drops project/tools',!strict.includes('LAB_PROJECT_RULE')&&!strict.includes('Available tools:'));
  await a.cmd('mode replace');const replaced=(await a.inject()).systemPrompt;
  check(label+' replace removes old identity',!replaced.includes('You are an expert coding assistant'));
  check(label+' replace removes old docs',!replaced.includes('Pi documentation'));
  check(label+' replace retains project',replaced.includes('LAB_PROJECT_RULE'));
  await a.cmd('mode append');const appended=(await a.inject()).systemPrompt;
  check(label+' append is actually prepend',appended.endsWith(old)&&appended.length>old.length);
  console.log(JSON.stringify({label,hostChars:old.length,strictChars:strict.length,replaceChars:replaced.length,appendChars:appended.length}));
 }
}
if(want('lifecycle')){
 const a=await load('purge-current');await a.start();await a.cmd('mode append');await a.cmd('on');
 await a.inject();await a.start();check('session_start disables',(await a.inject())===undefined);
 await a.cmd('status');check('mode does NOT reset on session_start',a.notes.at(-1).text.includes('append'));
 await a.cmd('on');await a.cmd('mode replace');await a.inject();await a.cmd('status');const statusBefore=a.notes.at(-1).text;
 await a.cmd('mode append');await a.inject();await a.cmd('status');
 check('append status retains stale cut',statusBefore.includes('已切除')&&a.notes.at(-1).text.includes('已切除'));
 await a.cmd('reload');check('README reload command not implemented',a.notes.at(-1).text.includes('未知子命令'));
 await a.cmd('source /LAB/MISSING_FILE');check('bad source reports error',a.notes.at(-1).level==='error');
 check('bad source rollback keeps persona',(await a.inject()).systemPrompt.includes('helpful assistant'));
 // Two extension registrations from one module share its top-level state.
 const mod=await import(pathToFileURL(resolve(root,'evidence/purge-current/extensions/pi-purge.ts')).href+'?shared=one');
 const maps=[new Map(),new Map()],cmds=[new Map(),new Map()];
 const ctx={ui:{setStatus:()=>{},notify:()=>{}}};
 maps.forEach((m,i)=>mod.default({on:(k,v)=>m.set(k,v),registerCommand:(k,v)=>cmds[i].set(k,v)}));
 await maps[0].get('session_start')({},ctx);await cmds[0].get('purge').handler('on',ctx);
 check('same-module multiple registrations share state',(await maps[1].get('before_agent_start')({systemPrompt:old,systemPromptOptions:{cwd:'/LAB'}},ctx))!==undefined);
}
if(want('compat')){
 const a=await load('purge-current');await a.start();await a.cmd('mode replace');await a.cmd('on');
 const r=(await a.inject(cur)).systemPrompt;
 check('latest identity anchor no match',r.includes('You are a coding assistant running inside pi'));
 check('latest docs anchor no match',r.includes('Pi documentation (read only when the user asks about the harness itself'));
 check('replace latest behaves like prepend',r.endsWith(cur));
 await a.cmd('mode strict');check('strict latest drops all host sections',!(await a.inject(cur)).systemPrompt.includes('LAB_PROJECT_RULE'));
 const partial='You are an expert coding assistant operating inside pi, a coding agent harness.\nPi documentation NEW UNMATCHED';
 await a.cmd('mode replace');const part=(await a.inject(partial)).systemPrompt;
 check('partial match removes identity independently',!part.includes('You are an expert coding assistant')&&part.includes('Pi documentation NEW UNMATCHED'));
 console.log('Compatibility: 0.84.2 markers match; 1.5.2 current markers changed. CLI/E2E not executed.');
}
console.log(`RESULT stage=${stage} checks=${checks}; zero model client; fixture-level only`);
