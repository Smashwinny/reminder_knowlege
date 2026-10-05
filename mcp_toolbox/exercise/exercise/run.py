#!/usr/bin/env python3
"""Synthetic SQLite-only MCP Toolbox experiment. Python standard library only.
No SQL keyword security filter, credentials, HTTP listener or client registration.
"""
import argparse, datetime, hashlib, json, os, pathlib, queue, sqlite3, subprocess, sys, threading, time
BASE = pathlib.Path(__file__).resolve().parent
EXPECTED_SHA = 'd8e0df24b5ce9934c8f7ae8466f64ff5512857c5a7e47640301750ee82f92db3'
VERSION = '1.13.1+binary.linux.amd64.e14cda6'
URL = 'https://storage.googleapis.com/mcp-toolbox-for-databases/v1.13.1/linux/amd64/toolbox'
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
p=argparse.ArgumentParser(); p.add_argument('--binary',default=str(BASE/'vendor/toolbox')); p.add_argument('--output',default=str(BASE/'evidence/run'))
a=p.parse_args(); binary=pathlib.Path(a.binary).resolve(); out=pathlib.Path(a.output).resolve()
if out.exists(): raise SystemExit('Use a fresh --output directory; no existing files are overwritten')
out.mkdir(parents=True); (out/'home').mkdir()
checks=[]; transcript=[]; commands=[]; start=now()
def check(name,condition,detail=None):
    checks.append({'name':name,'passed':bool(condition),'detail':detail})
    print(('PASS ' if condition else 'FAIL ')+name,flush=True)
    if not condition: raise AssertionError(name+': '+str(detail))
env={'PATH':os.environ.get('PATH','/usr/bin:/bin'),'HOME':str(out/'home'),'LANG':'C.UTF-8','TMPDIR':str(out)}
class MCP:
    def __init__(self,label,args,extra=None):
        self.label=label; self.i=0; self.q=queue.Queue(); self.log=open(out/(label+'.stderr.log'),'w')
        cmd=[str(binary),*args,'--stdio','--disable-version-check','--disable-reload','--log-level','ERROR']
        commands.append({'label':label,'argv':cmd,'environment':{**env,**(extra or {})}})
        self.proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.log,text=True,bufsize=1,cwd=out,env={**env,**(extra or {})})
        def reader():
            for line in self.proc.stdout: self.q.put(line)
            self.q.put(None)
        threading.Thread(target=reader,daemon=True).start()
    def send(self,method,params=None,notify=False):
        self.i+=1; msg={'jsonrpc':'2.0','method':method}
        if not notify: msg['id']=self.i
        if params is not None: msg['params']=params
        transcript.append({'at':now(),'server':self.label,'direction':'request','message':msg})
        self.proc.stdin.write(json.dumps(msg)+'\n'); self.proc.stdin.flush()
        if notify: return None
        deadline=time.monotonic()+20
        while True:
            line=self.q.get(timeout=max(.01,deadline-time.monotonic()))
            if line is None: raise RuntimeError(self.label+' exited; read stderr log')
            res=json.loads(line); transcript.append({'at':now(),'server':self.label,'direction':'response','message':res})
            if res.get('id')==self.i: return res
    def init(self):
        r=self.send('initialize',{'protocolVersion':'2025-06-18','capabilities':{},'clientInfo':{'name':'synthetic-sqlite-lesson','version':'1.0'}})
        check(self.label+' MCP initialize',r.get('result',{}).get('protocolVersion')=='2025-06-18',r)
        self.send('notifications/initialized',notify=True)
    def call(self,name,args): return self.send('tools/call',{'name':name,'arguments':args})
    def close(self):
        self.proc.stdin.close()
        try:self.proc.wait(timeout=8)
        except subprocess.TimeoutExpired:self.proc.terminate();self.proc.wait(timeout=8)
        self.log.close(); commands.append({'label':self.label,'exit_code':self.proc.returncode})
def iserror(r): return 'error' in r or r.get('result',{}).get('isError') is True
def texts(r): return '\n'.join(c.get('text','') for c in r.get('result',{}).get('content',[]) if c.get('type')=='text')
def rows(r):
    result=[]
    for c in r.get('result',{}).get('content',[]):
        if c.get('type')=='text':
            v=json.loads(c['text']); result.extend(v if isinstance(v,list) else [v])
    return result
servers=[]
try:
    print('STEP 1: verify official binary and seed disposable synthetic databases',flush=True)
    check('official downloaded binary SHA-256 matches recorded bytes',digest(binary)==EXPECTED_SHA)
    ver=subprocess.check_output([str(binary),'--version'],text=True,env=env).strip(); check('binary version matches release',VERSION in ver,ver)
    for name in ['readonly.db','writable.db']:
        with sqlite3.connect(out/name) as db:
            db.execute('CREATE TABLE inventory(id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, qty INTEGER NOT NULL)')
            db.executemany('INSERT INTO inventory(name,qty) VALUES (?,?)',[('apples',4),('pears',7)])
    before=digest(out/'readonly.db'); ro_uri=(out/'readonly.db').as_uri()+'?mode=ro'
    print('STEP 2: official prebuilt SQLite discovery and successful read',flush=True)
    s=MCP('prebuilt-readonly',['--prebuilt','sqlite/sqlite_database_tools'],{'SQLITE_DATABASE':ro_uri});servers.append(s);s.init()
    manifest=s.send('tools/list',{}); ts=manifest.get('result',{}).get('tools',[]); names={t['name'] for t in ts}
    check('prebuilt toolset exposes execute_sql and list_tables',names=={'execute_sql','list_tables'},sorted(names))
    hint=next(t for t in ts if t['name']=='execute_sql').get('annotations',{}).get('readOnlyHint')
    check('SQLite native URI does not automatically advertise readOnlyHint=true',hint is False,hint)
    r=s.call('list_tables',{'output_format':'simple','table_names':''});check('prebuilt table discovery succeeds',not iserror(r) and 'inventory' in texts(r),r)
    r=s.call('execute_sql',{'sql':'SELECT id,name,qty FROM inventory ORDER BY id'}); check('prebuilt SELECT returns two synthetic rows',not iserror(r) and len(rows(r))==2,r)
    print('STEP 3: native mode=ro rejects write statements without keyword filtering',flush=True)
    writes=[('insert',"INSERT INTO inventory(name,qty) VALUES ('blocked',1)"),('update','UPDATE inventory SET qty=99 WHERE id=1'),('delete','DELETE FROM inventory WHERE id=1'),('ddl','CREATE TABLE forbidden(id INTEGER)'),('query_only reset chain',"PRAGMA query_only=OFF; INSERT INTO inventory(name,qty) VALUES ('still_blocked',1)")]
    for label,sql in writes:
        r=s.call('execute_sql',{'sql':sql});check('native read-only rejects '+label,iserror(r) and ('readonly' in texts(r).lower() or 'read-only' in texts(r).lower()),r)
    r=s.call('execute_sql',{'sql':'SELECT count(*) AS n, sum(qty) AS total FROM inventory'});check('read still works after denied writes',rows(r)==[{'n':2,'total':11}],r)
    s.close();servers.remove(s);check('readonly main database byte hash unchanged',digest(out/'readonly.db')==before)
    print('STEP 4: custom parameter binding, input errors and tool discovery',flush=True)
    custom='''kind: source\nname: local\ntype: sqlite\ndatabase: %s\n---\nkind: tool\nname: lookup_item\ntype: sqlite-sql\nsource: local\ndescription: Exact name lookup of synthetic inventory\nstatement: SELECT id,name,qty FROM inventory WHERE name = ? ORDER BY id\nparameters:\n  - name: name\n    type: string\n    description: Exact item name\nannotations:\n  readOnlyHint: true\n---\nkind: toolset\nname: lookup_only\ntools:\n  - lookup_item\n''' % json.dumps(ro_uri)
    cfg=out/'custom.yaml';cfg.write_text(custom);s=MCP('custom-readonly',['--config',str(cfg)]);servers.append(s);s.init()
    r=s.send('tools/list',{});check('custom manifest exposes only configured lookup', [t['name'] for t in r.get('result',{}).get('tools',[])]==['lookup_item'],r)
    r=s.call('lookup_item',{'name':'apples'});check('parameterized lookup returns expected row',rows(r)==[{'id':1,'name':'apples','qty':4}],r)
    r=s.call('lookup_item',{'name':"apples' OR 1=1 --"});check('SQL-looking parameter stays a value',not iserror(r) and rows(r)==[],r)
    r=s.call('lookup_item',{'name':123});check('wrong parameter type produces MCP error',iserror(r),r)
    r=s.call('execute_sql',{'sql':'SELECT 1'});check('unconfigured tool call rejected as unknown tool',iserror(r),r)
    s.close();servers.remove(s)
    print('STEP 5: deliberately false annotation does not stop a writable control',flush=True)
    false_hint='''kind: source\nname: local\ntype: sqlite\ndatabase: %s\n---\nkind: tool\nname: misleading_hint\ntype: sqlite-execute-sql\nsource: local\ndescription: Deliberately incorrect hint for isolated safety experiment\nannotations:\n  readOnlyHint: true\n'''
    cfg=out/'hint-control.yaml';cfg.write_text(false_hint%json.dumps((out/'writable.db').as_uri()+'?mode=rw'))
    s=MCP('writable-hint-control',['--config',str(cfg)]);servers.append(s);s.init()
    r=s.send('tools/list',{});check('negative control advertises deliberately false read-only hint',r['result']['tools'][0]['annotations']['readOnlyHint'] is True,r)
    r=s.call('misleading_hint',{'sql':"INSERT INTO inventory(name,qty) VALUES ('control_write',1)"});check('hint alone does not block writes',not iserror(r),r)
    s.close();servers.remove(s)
    with sqlite3.connect(out/'writable.db') as db:n=db.execute('SELECT count(*) FROM inventory').fetchone()[0]
    check('negative control write really persisted',n==3,n)
    print('STEP 6: unsupported source field fails and final evidence persists',flush=True)
    invalid=out/'unsupported-readonly.yaml';invalid.write_text('kind: source\nname: invalid\ntype: sqlite\ndatabase: '+json.dumps(ro_uri)+'\nreadOnly: true\n')
    cmd=[str(binary),'--config',str(invalid),'--stdio','--disable-version-check','--disable-reload'];bad=subprocess.run(cmd,input='',capture_output=True,text=True,timeout=20,cwd=out,env=env)
    commands.append({'label':'unsupported-readonly-field','argv':cmd,'exit_code':bad.returncode});(out/'unsupported-readonly.stderr.log').write_text(bad.stderr)
    check('SQLite readOnly field rejected at startup',bad.returncode!=0 and 'unknown field "readOnly"' in bad.stderr,bad.stderr)
    check('final readonly database byte hash unchanged',digest(out/'readonly.db')==before)
    status='passed'
except Exception as exc:
    status='failed';checks.append({'name':'unhandled experiment error','passed':False,'detail':repr(exc)})
    print('ERROR '+repr(exc),flush=True)
finally:
    for s in servers:
        try:s.close()
        except Exception:pass
    result={'status':status,'started_at_utc':start,'finished_at_utc':now(),'python_version':sys.version,'python_sqlite_version':sqlite3.sqlite_version,'binary':{'url':URL,'version':VERSION,'sha256':EXPECTED_SHA,'release_commit':'e14cda6b4f483e6b5e5ec23e342f9f232a6ce60f','checksum_scope':'SHA-256 measured from official download; not a separately published signature'},'checks':checks,'passed_checks':sum(c['passed'] for c in checks),'total_checks':len(checks),'limitations':['SQLite native mode=ro protects this main DB connection; not Toolbox readOnly support or whole-process sandbox','No credentials, OAuth, identity permissions, production DB, cloud managed DB readOnly, HTTP exposure, named endpoint authorization or exhaustive SQL adversarial testing','Default stdio manifest contains all configured tools. Toolset filtering in prebuilt config is exercised; named HTTP endpoint scoping is not','Deliberately false readOnlyHint in synthetic writable control is a test fixture, not recommended configuration','No telemetry exporter configured; startup version check disabled; no OS network sandbox claimed']}
    (out/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');(out/'commands.json').write_text(json.dumps(commands,indent=2)+'\n');(out/'mcp-transcript.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in transcript))
    print(json.dumps({'status':status,'passed':result['passed_checks'],'total':result['total_checks'],'output':str(out)}),flush=True)
if status!='passed':raise SystemExit(1)
