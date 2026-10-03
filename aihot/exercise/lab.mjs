import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {stripTypeScriptTypes} from 'node:module';
import {Script,createContext} from 'node:vm';
import assert from 'node:assert/strict';

const root=path.resolve(process.argv[2] || 'F:/reminder/aihot/repo');
const source=readFileSync(path.join(root,'apps/web/app/lib/api.server.ts'),'utf8');
// Run the exact upstream pure function, without importing React Router or starting any service.
const pure=source.slice(source.indexOf('export function releaseBoundCache('));
assert(pure.startsWith('export function releaseBoundCache('));
const js=stripTypeScriptTypes(pure,{mode:'strip'}).replace('export function','function');
const context=createContext({Date,Math,Number});
new Script(js).runInContext(context,{timeout:1000});
const now=Date.parse('2026-10-03T00:00:00Z');
const upstream=values=>({get:name=>values[name]??null});
const cases=[
  ['normal',null,undefined,'public, max-age=0, s-maxage=60'],
  ['release in 5s',new Date(now+5000).toISOString(),undefined,'public, max-age=0, s-maxage=5'],
  ['upstream in 2s',null,upstream({'X-Accel-Expires':'@'+(now/1000+2)}),'public, max-age=0, s-maxage=2'],
  ['upstream no-store',null,upstream({'Cache-Control':'no-store'}),'no-cache'],
  ['already released',new Date(now-1000).toISOString(),undefined,'no-cache'],
  ['upstream zero',null,upstream({'X-Accel-Expires':'0'}),'no-cache'],
];
const cacheResults=cases.map(([label,refreshAt,headers,expected])=>{
  const result=context.releaseBoundCache(refreshAt,60,now,headers);
  assert.equal(result['Cache-Control'],expected,label);
  return {label,actual:result['Cache-Control'],pass:true};
});

const fixture=JSON.parse(readFileSync(new URL('./repository-evidence.json',import.meta.url),'utf8'));
// Negative cases are synthetic. Never include real private-repository metadata in public artifacts.
const candidates=[...fixture.repositories,{name:'synthetic-private',visibility:'private',fork:false},
  {name:'synthetic-draft',visibility:'public',approved:false,fork:false}];
const publicProjects=candidates.filter(r=>r.visibility==='public'&&r.approved!==false).map(r=>({
  name:r.name,url:r.url,description:r.description,upstream:r.upstream,
  track:r.fork?'study-and-adaptation':'self-maintained-implementation',
  evidence:r.fork?'Public fork; personal contribution not yet verified':'Public non-fork + README; not a running-demo verification',
  demoStatus:'not-verified',license:r.license,
}));
assert.equal(publicProjects.length,7);
assert(!publicProjects.some(p=>p.name.startsWith('synthetic-')));
assert.equal(publicProjects.filter(p=>p.track==='study-and-adaptation').length,6);
assert.equal(publicProjects.find(p=>p.name==='street-cat-king').track,'self-maintained-implementation');
assert(!JSON.stringify(publicProjects).includes('synthetic-private'));
const out=new URL('./output/',import.meta.url);mkdirSync(out,{recursive:true});
writeFileSync(new URL('public-projects.json',out),JSON.stringify(publicProjects,null,2)+'\n');
const result={upstreamCommit:'3343fe2b20db4be7269113752d82d3992fc52b6b',
  sourceSha256:createHash('sha256').update(pure).digest('hex'),
  testsPassed:11,cacheResults,publicCount:7,adaptationCount:6,
  scope:'Isolated upstream cache-function tests + self-authored public-snapshot experiment. No DB, LLM, paid API, collection, or website deployment.'};
writeFileSync(new URL('lab-results.json',out),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
