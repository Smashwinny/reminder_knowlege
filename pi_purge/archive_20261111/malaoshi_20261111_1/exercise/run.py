import subprocess,pathlib,datetime,sys
root=pathlib.Path(__file__).resolve().parent.parent
stage=sys.argv[1]
cmd= {'upstream':['node','test/pi-purge.test.mjs'],'env':['node','test/pi-purge-env-source.test.mjs']}.get(stage,['node','exercise/lab.mjs',stage])
cwd=root/'evidence/purge-current' if stage in ('upstream','env') else root
r=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True)
log=root/'evidence'/('run-'+stage+'.txt')
log.write_text('Time Asia/Shanghai: '+datetime.datetime.now().isoformat()+'\nCWD: '+str(cwd)+'\nCOMMAND: '+' '.join(cmd)+'\nEXIT: '+str(r.returncode)+'\nSTDOUT:\n'+r.stdout+'\nSTDERR:\n'+r.stderr)
print(log.read_text());sys.exit(r.returncode)
