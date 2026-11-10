import sys,sqlite3,hashlib,json
from pathlib import Path
mode=sys.argv[1];db=Path('exercise/ledger.sqlite')
if mode=='prepare':
 db.unlink(missing_ok=True);c=sqlite3.connect(db);c.execute('create table jobs(hash text primary key,state text,attempts int)');c.commit();print('SQLite ledger created; synthetic jobs only')
elif mode=='unknown':
 c=sqlite3.connect(db);h=hashlib.sha256(b'synthetic-media').hexdigest();c.execute('insert into jobs values(?,?,?)',(h,'UNKNOWN',1));c.commit();print('simulated create timeout: UNKNOWN; resubmit disabled')
elif mode=='verify':
 c=sqlite3.connect(db);h=hashlib.sha256(b'synthetic-media').hexdigest();fake_list=[h];assert h in fake_list;c.execute('update jobs set state=? where hash=?',('LIST_VERIFIED',h));c.commit()
 try:c.execute('insert into jobs values(?,?,?)',(h,'NEW',0));c.commit();raise AssertionError('duplicate accepted')
 except sqlite3.IntegrityError:pass
 row=c.execute('select state,attempts from jobs').fetchone();assert row==('LIST_VERIFIED',1);print('fake list readback + unique hash:',row,'duplicate rejected; no external publish')
elif mode=='media':
 import subprocess
 out=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json','exercise/subtitled.mp4']))
 v=out['streams'][0];assert (v['width'],v['height'])==(360,640);assert 1.9<float(out['format']['duration'])<2.2;print('ffprobe actual:',v['width'],v['height'],v['codec_name'],out['format']['duration'],'seconds')
