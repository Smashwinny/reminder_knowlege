#!/usr/bin/env python3
import datetime,json,platform,subprocess,sys
from pathlib import Path
p=Path(__file__).resolve().parent
runs=[]
for action in ['init','validate','shortlist','costs','test','audit']:
 command=[sys.executable,str(p/'lab.py'),action]
 r=subprocess.run(command,capture_output=True,text=True,check=False)
 runs.append(dict(command='python3 exercise/lab.py '+action,at=datetime.datetime.now().astimezone().isoformat(),exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr))
 if r.returncode:break
report=dict(environment=platform.platform(),python=platform.python_version(),runs=runs)
(p/'run-log.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
for r in runs:print('$ '+r['command']+'\n'+r['stdout']+'exit='+str(r['exit_code']))
assert all(r['exit_code']==0 for r in runs)
