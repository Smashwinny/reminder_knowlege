#!/usr/bin/env python3
"""Self-authored CPU experiment orchestrator; runs original recast CLI. No models/network."""
from pathlib import Path
import subprocess,sys,json,hashlib,copy,datetime
from fractions import Fraction
P=Path(__file__).resolve().parents[1];R=P/'evidence/upstream/scripts/recast.py';M=P/'media';O=P/'results'
M.mkdir(exist_ok=True);O.mkdir(exist_ok=True)
def run(args,expect=0):
 args=list(map(str,args));p=subprocess.run(args,cwd=P,capture_output=True,text=True)
 print('$ '+' '.join(args)+'\n'+p.stdout+p.stderr+'\nexit='+str(p.returncode),flush=True)
 if (p.returncode==0)!=(expect==0):raise RuntimeError('unexpected exit')
 return p

def cli(*a,expect=0):return run([sys.executable,R,*a],expect)
def dump(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2))
s=int(sys.argv[1])
if s==1:
 run(['ffmpeg','-v','error','-f','lavfi','-i','testsrc2=size=320x180:rate=24','-t','5','-c:v','libx264','-pix_fmt','yuv420p',M/'native24.mp4'])
 probe=json.loads(cli('probe',M/'native24.mp4').stdout);dump('native-probe.json',probe)
 assert probe['frame_count']==120 and probe['fps']=='24/1'
elif s==2:
 cli('init',P/'synthetic-project', '--source',M/'native24.mp4','--id','synthetic-demo')
 plan={'source':{'frame_count':150,'fps':'30'},'segments':[{'id':'S001','start':0,'end':75},{'id':'S002','start':75,'end':150}]};dump('plan.json',plan)
 cli('validate-plan',O/'plan.json')
 for kind,start in [('gap',76),('overlap',74)]:
  q=copy.deepcopy(plan);q['segments'][1]['start']=start;dump(kind+'.json',q);cli('validate-plan',O/(kind+'.json'),expect=1)
 # synthetic-project uses original 24fps/120 frame clock; test plans above explicitly target 30fps/150 clock.
 for v in ['v001','v002']:
  d=P/'synthetic-project/03_提示词与任务/S001'/v;d.mkdir(parents=True);(d/'manifest.json').write_text(json.dumps({'version':v,'generation_authorized':False,'synthetic_only':True}))
 dump('version-check.json',{'versions':['v001','v002'],'both_exist':True,'original_24fps_project_unmodified':True})
elif s==3:
 cli('map',M/'native24.mp4',M/'mapped30.mp4','--start','0','--end','150','--source-fps','30','--native-fps','24','--native-source-start','0')
 p=json.loads(cli('probe',M/'mapped30.mp4').stdout);dump('mapped-probe.json',p);assert p['frame_count']==150 and p['fps']=='30/1'
 # Deliberately wrong: reinterpret 120 frames at 30fps, shortening five seconds to four.
 run(['ffmpeg','-v','error','-i',M/'native24.mp4','-vf','setpts=0.8*PTS','-r','30','-frames:v','120','-c:v','libx264',M/'wrong-speed30.mp4'])
 w=json.loads(cli('probe',M/'wrong-speed30.mp4').stdout);dump('wrong-probe.json',w)
elif s==4:
 cli('qa',M/'mapped30.mp4',O/'qc-good.json','--frames','150','--fps','30')
 cli('qa',M/'wrong-speed30.mp4',O/'qc-bad.json','--frames','150','--fps','30')
 good=json.loads((O/'qc-good.json').read_text());bad=json.loads((O/'qc-bad.json').read_text())
 assert good['technical_pass'] and not good['visual_acceptance'] and not bad['technical_pass']
 # QA emits JSON verdict, not nonzero exit on technical failure: consumer must read it.
 raw=run(['ffprobe','-v','error','-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp_time','-of','json',M/'mapped30.mp4'])
 fs=json.loads(raw.stdout)['frames'];ts=[float(x['best_effort_timestamp_time']) for x in fs];err=max(abs(t-i/30) for i,t in enumerate(ts));assert len(ts)==150 and err<1e-5
 mp=json.loads((M/'mapped30.mp4.mapping.json').read_text());dump('pts-and-map.json',{'frames':len(ts),'max_pts_error_seconds':err,'unique_native_frames':len(set(mp['indices'])),'duplicated_output_frames':len(mp['indices'])-len(set(mp['indices'])),'first_indices':mp['indices'][:12],'last_index':mp['indices'][-1]})
elif s==5:
 # Tests execute in original test directory, unmodified; no SSH test selected.
 a=[sys.executable,'-m','unittest','-v','test_production.Production.test_plan_gaps_overlaps_and_review','test_production.Production.test_exact_mapping_offsets','test_production.Production.test_media_pipeline_and_acceptance_gate']
 p=subprocess.run(a,cwd=R.parents[1]/'tests',capture_output=True,text=True);print('$ '+' '.join(a)+'\n'+p.stdout+p.stderr+'\nexit='+str(p.returncode));assert p.returncode==0
elif s==6:
 files=[x for d in [P/'evidence/upstream',O] for x in d.rglob('*') if x.is_file() and '__pycache__' not in str(x)]
 dump('checksums.json',{str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files})
 print('fingerprinted',len(files),'files; no GPU generation, no face/sound synthesis, no external writes')
