// Original experiment, using official source at b30d54b8aebe6408e02d1473446d25f8083da68f.
// https://github.com/earendil-works/pi/tree/b30d54b8aebe6408e02d1473446d25f8083da68f/packages/durable/test
import { it, expect } from 'vitest';
import { DatabaseSync } from 'node:sqlite';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { openNodeSqliteStorage } from '../repo/packages/durable/src/storage/sqlite/node.ts';
import { commitWrites } from '../repo/packages/durable/src/testing/commit-writes.ts';
import { ROOT_CONVERSATION_ID } from '../repo/packages/durable/src/types.ts';
import { context, ControlledStorage } from '../repo/packages/durable/test/session-support.ts';
import { chatSetup, openChat } from '../repo/packages/durable/test/chat-support.ts';
import { fauxAssistantMessage } from '@earendil-works/pi-ai';
it('two prefixes share one real SQLite file; same IDs cannot leak across prefixes', async () => {
 const dir=await mkdtemp(join(tmpdir(),'ma-durable-')); const path=join(dir,'shared.sqlite');
 const a=await openNodeSqliteStorage(path,{prefix:'alpha_'});
 const b=await openNodeSqliteStorage(path,{prefix:'beta_'});
 for(const s of [a,b]) await commitWrites(s,[{type:'conversation',value:{id:ROOT_CONVERSATION_ID}}],context);
 const id=await a.mintId();
 await commitWrites(a,[{type:'entry',value:{id,conversationId:ROOT_CONVERSATION_ID,kind:'message',data:'ALPHA ONLY'}}],context);
 expect((await a.entry(id,context))?.entry.data).toBe('ALPHA ONLY'); expect(await b.entry(id,context)).toBeUndefined();
 const bid=await b.mintId();
 await commitWrites(b,[{type:'entry',value:{id:bid,conversationId:ROOT_CONVERSATION_ID,kind:'message',data:'BETA ONLY'}}],context);
 expect((await a.entry(id,context))?.entry.data).toBe('ALPHA ONLY');
 await a.close(context); await b.close(context);
 const db=new DatabaseSync(path); const names=db.prepare("SELECT name FROM sqlite_master WHERE type='table'").all().map(x=>x.name); db.close();
 const again=await openNodeSqliteStorage(path,{prefix:'beta_'}); expect((await again.entry(bid,context))?.entry.data).toBe('BETA ONLY'); await again.close(context);
 console.log(JSON.stringify({experiment:'sqlite-isolation',sameFile:true,aId:id,bId:bid,tableCount:names.length,names,reopen:'BETA ONLY',pass:true})); await rm(dir,{recursive:true});
});
it('measure committed document batches with the same faux stream at two persistence intervals', async () => {
 const rows=[];
 for(const persistWithinMs of [0,400]){
  const storage=new ControlledStorage(); const setup=chatSetup({tokensPerSecond:80,tokenSize:{min:4,max:4}});
  setup.settings.progress={partialIntervalMs:100,persistWithinMs}; setup.faux.setResponses([fauxAssistantMessage('streamed '.repeat(80))]);
  const {harness,root}=await openChat(storage,setup); harness.resume(); const start=storage.commits.length;
  const settled=await (await root.submit({type:'input',content:'offline only'},context)).wait(context);
  const batches=storage.commits.slice(start); rows.push({persistWithinMs,totalBatches:batches.length,documentBatches:batches.filter(b=>b.some(w=>w.type==='document.change')).length,status:settled.status}); await harness.close(context);
 }
 console.log(JSON.stringify({experiment:'faux-write-count',rows,unit:'ControlledStorage batch, NOT remote I/O or disk write'}));
 expect(rows[1].documentBatches).toBeLessThan(rows[0].documentBatches); expect(rows.every(x=>x.status==='done')).toBe(true);
},15000);
