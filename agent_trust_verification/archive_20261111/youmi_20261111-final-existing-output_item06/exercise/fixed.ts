export type Draft={kind:'draft';text:string};
export type Approved={kind:'approved';text:string;approvalId:string};
export function parseDraft(input:unknown):Draft {
 if(typeof input!=='object'||input===null||!('kind'in input)||input.kind!=='draft'||!('text'in input)||typeof input.text!=='string'||input.text.trim().length===0)throw Error('invalid draft');
 return {kind:'draft',text:input.text};
}
export function approve(d:Draft, syntheticConsentId:string):Approved {
 if(!syntheticConsentId.trim())throw Error('missing synthetic consent');
 return {kind:'approved',text:d.text,approvalId:syntheticConsentId};
}
// Only a pure simulated receipt. No transport, filesystem or message sender.
export function simulateDeliver(a:Approved){return {kind:'sent',text:a.text,approvalId:a.approvalId};}
const inputs:unknown[]=[{kind:'draft',text:'hello'},{kind:'approved',text:'injected'},{kind:'draft',text:1},{kind:'draft',text:''}];
let accepted=0,rejected=0;
for(const input of inputs){try{parseDraft(input);accepted++;}catch{rejected++;}}
console.log(JSON.stringify({synthetic_only:true,accepted,rejected,receipt:simulateDeliver(approve(parseDraft(inputs[0]),'fixture-consent'))}));
