// All upstream source mapped at the pinned SHA; no upstream source edits.
import {defineConfig} from 'vitest/config';
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {resolve} from 'node:path';
const root=fileURLToPath(new URL('../',import.meta.url));
const alias=[];
for(const name of ['durable','chord','ai','codemode','schema','telemetry']){
 const dir=resolve(root,'repo/packages',name); const p=JSON.parse(readFileSync(resolve(dir,'package.json'),'utf8'));
 for(const [key,t] of Object.entries(p.exports)){
  if(typeof t!=='object'||!t)continue;
  let s=(t as any).source??(t as any).import; if(typeof s!=='string'||s.endsWith('.json'))continue;
  s=s.replace('./dist/','./src/').replace('.js','.ts');
  const imp=p.name+(key==='.'?'':key.slice(1));
  alias.push({find:new RegExp('^'+imp.replace('*','(.+)')+'$'),replacement:resolve(dir,s).replace('*','$1')});
 }
}
export default defineConfig({resolve:{conditions:['source'],alias},ssr:{resolve:{conditions:['source']}},test:{root,include:['exercise/ma-laoshi-20261111-lab.test.ts','repo/packages/durable/test/{sqlite-storage,harness-compaction,harness-context,harness-deferred-progress,harness-sleep}.test.ts'],setupFiles:['repo/packages/durable/test/setup-document-retention.ts'],maxWorkers:1,fileParallelism:false}});
