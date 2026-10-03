import {readFileSync} from 'node:fs';
import {Script,createContext} from 'node:vm';
import assert from 'node:assert/strict';
// Unit fixture only, not a real browser or visual QA. The local browser connection timed out.
class Element {
 constructor(tag='div'){this.tag=tag;this.children=[];this.textContent='';this.value='0';this.dataset={};this.attrs={};}
 append(...xs){this.children.push(...xs)}
 replaceChildren(...xs){this.children=xs}
 setAttribute(n,v){this.attrs[n]=v}
}
const fields=Object.fromEntries(['cards','count','case','cache'].map(id=>['#'+id,new Element()]));
const buttons=['all','self-maintained-implementation','study-and-adaptation'].map(filter=>{
 const e=new Element('button');e.dataset.filter=filter;return e;
});
const document={querySelector:s=>fields[s],querySelectorAll:s=>buttons,createElement:tag=>new Element(tag)};
const html=readFileSync(new URL('../learning_lab.html',import.meta.url),'utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)?.[1];assert(script,'embedded script exists');
new Script(script).runInContext(createContext({document}),{timeout:1000});
assert.equal(fields['#cards'].children.length,7);
buttons[1].onclick();assert.equal(fields['#cards'].children.length,1);
buttons[2].onclick();assert.equal(fields['#cards'].children.length,6);
assert.equal(buttons[2].attrs['aria-pressed'],'true');
fields['#case'].value='3';fields['#case'].onchange();assert.equal(fields['#cache'].textContent,'no-cache');
console.log('5/5 UI unit-fixture assertions pass; NOT browser interaction or visual verification.');
