// 真实上游函数，SDK替换为无网络内存桩；仅特征化其决策，不修改云资源。
import fs from 'node:fs';import vm from 'node:vm';
const file=new URL('./',import.meta.url), read=n=>fs.readFileSync(new URL(n,file),'utf8'), write=(n,x)=>fs.writeFileSync(new URL(n,file),JSON.stringify(x,null,2));
const mode=process.argv[2];
if(mode==='fixture'){
 const base={costAmount:8,budgetAmount:10,currencyCode:'USD'};
 write('cases.json',[{name:'below',payload:base},{name:'at90',payload:{...base,costAmount:9}},{name:'threshold',payload:{...base,alertThresholdExceeded:.9}},{name:'dry',payload:{...base,dryRun:true}},{name:'bad-number',payload:{...base,costAmount:'abc'}},{name:'string-false-force',payload:{...base,forceKill:'false'}},{name:'already-off',payload:{...base,costAmount:9},enabled:false},{name:'missing-budget',payload:{}}]);
 console.log('8 synthetic payloads written; no credentials, SDK or network');
}else if(mode==='run'){
 let source=read('upstream-index.js');source=source.replace("import { CloudBillingClient } from '@google-cloud/billing';",'');source=source.replace('export const stopBilling =','globalThis.stopBilling =');const out=[];
 for(const item of JSON.parse(read('cases.json'))){
  const calls=[],logs=[];class FakeBilling{async getProjectBillingInfo(x){calls.push(['get',x]);return [{billingEnabled:item.enabled!==false,billingAccountName:'FAKE'}];}async updateProjectBillingInfo(x){calls.push(['update',x]);return [{}];}}
  const ctx={CloudBillingClient:FakeBilling,process:{env:{TARGET_PROJECT_ID:'offline-demo'}},Buffer,console:{log:(...x)=>logs.push(x.join(' ')),warn:(...x)=>logs.push(x.join(' ')),error:(...x)=>logs.push(x.join(' '))}};vm.createContext(ctx);vm.runInContext(source,ctx);await ctx.stopBilling({data:{message:{data:Buffer.from(JSON.stringify(item.payload)).toString('base64')}}});out.push({name:item.name,calls,logs});
 }write('results.json',out);console.log(JSON.stringify(out.map(x=>({name:x.name,get:x.calls.filter(x=>x[0]==='get').length,unlink_stub:x.calls.filter(x=>x[0]==='update').length})),null,2));
}else if(mode==='verify'){
 const out=JSON.parse(read('results.json'));const n=name=>out.find(x=>x.name===name).calls.filter(x=>x[0]==='update').length;
 const expectations={below:0,at90:1,threshold:1,dry:0,'bad-number':1,'string-false-force':1,'already-off':0,'missing-budget':0};for(const [k,v] of Object.entries(expectations))if(n(k)!==v)throw Error(k);
 console.log('PASS 8 upstream-characterisation checks. Two unsafe synthetic inputs trigger unlink STUB: NaN cost and string forceKill=false. This is a finding, not safety validation.');
}else if(mode==='delay'){
 const budget=10,threshold=.9,rate=2;for(const delay of [0,.5,1,24])console.log(JSON.stringify({synthetic:true,budget,delay_hours:delay,rate_per_hour:rate,cost_when_action:budget*threshold+rate*delay,overshoot:Math.max(0,budget*threshold+rate*delay-budget)}));
 console.log('real Billing/Cloud Run/PubSub/IAM calls = 0');
}
