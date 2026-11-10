from pathlib import Path
import subprocess,sys,datetime
r=Path(__file__).resolve().parent.parent;stage=sys.argv[1]
cmd=['node','exercise/lab.mjs',stage];p=subprocess.run(cmd,cwd=r,text=True,capture_output=True)
s='Asia/Shanghai '+datetime.datetime.now().isoformat()+'\nCWD '+str(r)+'\n$ '+' '.join(cmd)+'\nEXIT '+str(p.returncode)+'\n'+p.stdout+'\nSTDERR\n'+p.stderr
(r/'evidence'/('run-'+stage+'.txt')).write_text(s);print(s);sys.exit(p.returncode)
