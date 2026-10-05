from pathlib import Path
import datetime, hashlib, json, sqlite3, subprocess
ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'qa'/'independent_runtime'
HERE.mkdir(parents=True,exist_ok=True)
BIN=ROOT/'exercise/vendor/toolbox'
DB=HERE/'reviewer_fixture.sqlite'
if DB.exists():
    raise SystemExit('Refuse to overwrite existing reviewer fixture')
con=sqlite3.connect(DB)
con.executescript("CREATE TABLE inventory(id INTEGER PRIMARY KEY, item TEXT, stock INTEGER); INSERT INTO inventory VALUES(1,'test-widget',5);")
con.commit(); con.close()
def config(name, uri, extra=''):
    p=HERE/name
    p.write_text(f'''kind: source
name: review-source
type: sqlite
database: "{uri}"
{extra}---
kind: tool
name: review-sql
type: sqlite-execute-sql
source: review-source
description: Synthetic independent reviewer fixture only.
''')
    return p
ro=config('ro.yaml',f'file:{DB}?mode=ro')
rw=config('rw.yaml',str(DB))
unsupported=config('unsupported.yaml',str(DB),'readOnly: true\n')
records=[]
def invoke(label,cfg,sql):
    cmd=[str(BIN),'invoke','review-sql',json.dumps({'sql':sql}),'--config',str(cfg),'--disable-version-check']
    p=subprocess.run(cmd,capture_output=True,text=True,timeout=20)
    records.append({'case':label,'command':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    return p
before=hashlib.sha256(DB.read_bytes()).hexdigest()
a=invoke('read_on_native_ro',ro,'SELECT item, stock FROM inventory;')
b=invoke('write_rejected_native_ro',ro,'UPDATE inventory SET stock=99 WHERE id=1;')
after_ro=hashlib.sha256(DB.read_bytes()).hexdigest()
c=invoke('unsupported_sqlite_readOnly_field',unsupported,'SELECT 1;')
d=invoke('writable_control_same_update',rw,'UPDATE inventory SET stock=99 WHERE id=1;')
e=invoke('read_confirms_writable_control',ro,'SELECT stock FROM inventory WHERE id=1;')
con=sqlite3.connect(DB); final=con.execute('SELECT stock FROM inventory WHERE id=1').fetchone()[0]; con.close()
checks={'read_ok':a.returncode==0 and 'test-widget' in a.stdout,'ro_write_error':b.returncode!=0 and 'readonly' in (b.stdout+b.stderr).lower(),'ro_hash_unchanged':before==after_ro,'unsupported_field_rejected':c.returncode!=0 and 'unknown field "readOnly"' in (c.stdout+c.stderr),'writable_control_ok':d.returncode==0 and e.returncode==0 and final==99}
result={'reviewer':'review_mcp_toolbox_delivery','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'binary_sha256':hashlib.sha256(BIN.read_bytes()).hexdigest(),'fixture_before_sha256':before,'fixture_after_ro_sha256':after_ro,'checks':checks,'records':records,'limitations':['Direct Toolbox CLI invoke; does not independently test MCP transport','Native SQLite connection mode only; not Toolbox source readOnly support','No OAuth/authentication, real database, cloud engine, browser, or security certification claim']}
(HERE/'reviewer_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(checks,indent=2))
assert all(checks.values()), 'Independent checks failed'
