// Original teaching harness, inspired by pinned skill guidance; no model/engine SDK.
export const CONFIG=Object.freeze({version:1,maxHp:3,target:3,width:640,seed:42});
export function setup(){return {version:1,hp:3,score:0,phase:'PLAY',x:20,seen:[]};}
export function validate(s){if(s.version!==1||!Number.isInteger(s.hp)||s.hp<0||s.hp>3||!Number.isInteger(s.score)||s.score<0||!['PLAY','WIN','LOSE'].includes(s.phase))throw Error('contract');return true;}
export function apply(s,a){validate(s);const n=structuredClone(s),events=[];if(s.phase!=='PLAY'||s.seen.includes(a.id))return {state:n,events};n.seen.push(a.id);if(a.type==='collect'){n.score++;events.push({type:'score_changed',value:n.score});if(n.score>=CONFIG.target)n.phase='WIN';}else if(a.type==='damage'){n.hp=Math.max(0,n.hp-1);events.push({type:'health_changed',value:n.hp});if(n.hp===0)n.phase='LOSE';}else if(a.type==='move'){n.x=Math.max(0,Math.min(CONFIG.width,n.x+a.dx));}else throw Error('intent');validate(n);return {state:n,events};}
export function hud(s){return {hp:s.hp,score:s.score,phase:s.phase};}
export class Screens{constructor(){this.stack=[{name:'game',focus:'pause'}];}push(name,focus){this.stack.push({name,focus});}pop(){if(this.stack.length>1)this.stack.pop();return this.top();}top(){return this.stack.at(-1);}}
export function layout(w,h,inset=16){return {hp:{x:inset,y:inset,w:Math.min(200,w/2-inset*2),h:44},pause:{x:w-inset-44,y:inset,w:44,h:44},bounds:{w,h}};}
export class Feedback{constructor(){this.trauma=0;this.until=0;}hit(now,duration=.08){this.trauma=Math.min(1,this.trauma+.4);this.until=Math.max(this.until,now+duration);}advance(now,dt,reduced=false){this.trauma=Math.max(0,this.trauma-1.2*dt);return {frozen:now<this.until,offset:reduced?0:12*this.trauma**2*Math.sin(now*23)};}}
