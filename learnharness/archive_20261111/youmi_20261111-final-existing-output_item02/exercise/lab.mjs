// Self-authored runner; upstream TS modules are imported byte-for-byte.
import {createTree,emptyTree,PlanTreeError} from '../upstream/src/core/plan-tree.ts';
import {parseMermaidPlan} from '../upstream/src/agent/tools/mermaid-plan.ts';
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import assert from 'node:assert/strict';
const root=path.resolve(import.meta.dirname,'..');
const save=(name,data)=>{fs.mkdirSync(path.join(root,'results'),{recursive:true});fs.writeFileSync(path.join(root,'results',name),JSON.stringify(data,null,2)+'\n');console.log(JSON.stringify(data,null,2));};
const source=fs.readFileSync(path.join(root,'upstream/tests/plan-tree.test.ts'),'utf8');
const extract=()=>{
 const helper=source.slice(source.indexOf('const N ='),source.indexOf('// ─── 1. pure ops'));
 const pure=source.slice(source.indexOf('describe("plan-tree pure ops"'),source.indexOf('// ─── 2. tool execute'));
 const imports=`import assert from 'node:assert/strict';\nimport {describe,it} from 'node:test';\nimport {createTree,emptyTree,PlanTreeError} from '../upstream/src/core/plan-tree.ts';\nimport type {PlanTree} from '../upstream/src/core/contracts.ts';\n`;
 fs.writeFileSync(path.join(root,'exercise/upstream-pure.test.ts'),imports+helper+pure);
 console.log('Extracted upstream pure group: 5 it() tests; no tool/store tests selected.');
};
const manifest=()=>{const list=['README.md','LICENSE','package.json','docs/architecture.md','docs/development.md','docs/teaching-methodology.md','src/core/plan-tree.ts','src/agent/tools/mermaid-plan.ts','tests/plan-tree.test.ts'];save('manifest.json',list.map(f=>{const b=fs.readFileSync(path.join(root,'upstream',f));return {path:f,bytes:b.length,sha256:crypto.createHash('sha256').update(b).digest('hex')};}));};
const positive=()=>{const parsed=parseMermaidPlan('graph LR\n fractions[分数] --> ratio[比例] --> probability[概率]\n fractions --> ratio\n');assert.equal(parsed.ok,true);const tree=createTree(parsed.plan.nodes,parsed.plan.edges);assert.equal(tree.nodes.length,3);assert.equal(tree.edges.length,2);save('positive.json',{input:'合成的分数→比例→概率，不是模型或学习者数据',tree,edgeMeaning:'from 必须先于 to 理解；仅结构，不证明知识已掌握'});};
const negative=()=>{const r=[];for(const [id,input] of [['cycle','graph TD\n a --> b\n b --> a'],['invalid-slug','graph TD\n Bad.id[Bad] --> valid'],['missing-header','a --> b']]){try{const p=parseMermaidPlan(input);if(!p.ok)r.push({id,stage:'parse',problems:p.problems});else {createTree(p.plan.nodes,p.plan.edges);r.push({id,unexpected:'accepted'});}}catch(e){r.push({id,stage:'DAG',error:e.message});}}assert.ok(r.every(x=>!x.unexpected));save('negative.json',r);};
const selftest=()=>{let n=0;const test=(name,fn)=>{fn();n++;console.log('PASS',name);};
 test('empty version zero',()=>assert.equal(emptyTree().version,0));
 test('parser deduplicates edges',()=>assert.equal(parseMermaidPlan('graph TD\n a --> b\n a --> b').plan.edges.length,1));
 test('core rejects duplicate edges',()=>assert.throws(()=>createTree([{id:'a',title:'A'},{id:'b',title:'B'}],[{from:'a',to:'b'},{from:'a',to:'b'}]),PlanTreeError));
 test('parser first label wins',()=>assert.equal(parseMermaidPlan('graph TD\n a[First]\n a[Second]').plan.nodes[0].title,'First'));
 test('parser accepts underscore',()=>assert.equal(parseMermaidPlan('graph TD\n a_b --> c').ok,true));
 test('core alone accepts uppercase ids',()=>assert.equal(createTree([{id:'A',title:'A'}],[]).nodes[0].id,'A'));
 test('parser rejects uppercase ids',()=>assert.equal(parseMermaidPlan('graph TD\n A[Alpha]').ok,false));
 test('output not linked to caller arrays',()=>{const nodes=[{id:'a',title:'Before'}];const out=createTree(nodes,[]);nodes[0].title='After';assert.equal(out.nodes[0].title,'Before');});
 save('selftest.json',{self_authored_checks:n,passed:n,scope:'原始纯模块；非UI、推理、教学效果或完整上游套件'});};
({extract,manifest,positive,negative,selftest})[process.argv[2]]();
