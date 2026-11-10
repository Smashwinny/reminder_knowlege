"""mjfit真实几何/接触实验；无机器人策略训练，不复现论文73%成功率。"""
from pathlib import Path
import sys,json,platform,argparse,time,importlib.metadata as md
import numpy as np
import mujoco,mjfit
from mjfit import shapes
P=Path(__file__).resolve().parent

def env():
 return {'python':sys.version.split()[0],'platform':platform.platform(),'mujoco':mujoco.__version__,'mjfit':mjfit.__version__,'numpy':np.__version__,'mjfit_sha':'5833f465896e1e06bc4be4f003be847f5183a4db','scope':'CPU MuJoCo passive geometry/contact; no RL actor'}

def trial(clearance=1e-4,offset=(0,0),width=.016,height=.016,mu=1.,tau=.002,tag=None,dt=.001):
 xml=mjfit.peg(hole=shapes.rect(width,height),clearance=clearance,peg_length=.02,plate_thickness=.01,plate_size=.06,spawn_height=.001,friction=mu,timestep=dt)
 import xml.etree.ElementTree as ET
 root=ET.fromstring(xml)
 for x in root.iter('geom'):
  if 'solref' in x.attrib:x.set('solref',f'{tau} 1')
 xml=ET.tostring(root,encoding='unicode');m=mujoco.MjModel.from_xml_string(xml);d=mujoco.MjData(m)
 j=m.joint('peg_joint').qposadr[0];d.qpos[j:j+2]+=offset;mujoco.mj_forward(m,d)
 b=m.body('peg').id;pb=m.body('plate').id;z0=float(d.xpos[b,2]);trace=[];contacts=0;maxc=0;mind=0.;start=time.perf_counter()
 for n in range(round(.25/dt)):
  mujoco.mj_step(m,d)
  pc=[c for c in d.contact[:d.ncon] if {int(m.geom_bodyid[g]) for g in c.geom}=={b,pb}]
  contacts+=len(pc);maxc=max(maxc,len(pc))
  if pc:mind=min(mind,min(float(c.dist) for c in pc))
  if n%10==0:trace.append([float(d.time),*map(float,d.xpos[b])])
 elapsed=time.perf_counter()-start;drop=z0-float(d.xpos[b,2]);passed=drop>.009
 if tag:
  (P/(tag+'.xml')).write_text(xml);(P/(tag+'-trace.json')).write_text(json.dumps(trace))
 return {'clearance_mm':clearance*1000,'offset_mm':[float(x*1000) for x in offset],'width_mm':width*1000,'height_mm':height*1000,'friction':mu,'tau_ms':tau*1000,'dt_ms':dt*1000,'drop_mm':drop*1000,'peg_plate_contact_count':contacts,'max_simultaneous_contacts':maxc,'minimum_contact_distance_um':mind*1e6,'passed_depth_threshold':passed,'simulation_s':float(d.time),'cpu_wall_s':elapsed}

def clearance():
 rows=[]
 for c in [2e-5,1e-4,5e-4]:
  for off in [(0,0),(.002,0)]:rows.append(trial(c,off,tag='aligned' if c==1e-4 and off==(0,0) else 'blocked' if c==1e-4 else None))
 # Analytic polygon dimension: rect offset reduces both dimensions by 2c.
 assert all(x['passed_depth_threshold'] for x in rows if x['offset_mm']==[0.,0.])
 assert all(not x['passed_depth_threshold'] for x in rows if x['offset_mm']==[2.,0.])
 (P/'clearance-results.json').write_text(json.dumps(rows,indent=2))
 return rows

def randomize():
 rng=np.random.default_rng(2026);rows=[]
 for i in range(32):
  w,h=rng.uniform(.014,.024,2);c=float(rng.uniform(.0001,.0005));mu=float(np.exp(rng.uniform(np.log(.25),np.log(2))));tau=float(rng.uniform(.0025,.006));off=rng.uniform(-.0015,.0015,2)
  args=dict(clearance=c,width=w,height=h,mu=mu,tau=tau)
  a=trial(offset=tuple(off),**args);b=trial(offset=(0,0),**args)
  rows.append({'id':i,'randomized_offset':a,'oracle_centered':b})
 (P/'randomized-results.json').write_text(json.dumps(rows,indent=2))
 nominal=trial();a=sum(x['randomized_offset']['passed_depth_threshold'] for x in rows);b=sum(x['oracle_centered']['passed_depth_threshold'] for x in rows)
 return {'seed':2026,'pairs':32,'nominal_centered_pass':nominal['passed_depth_threshold'],'randomized_passes':a,'oracle_centered_passes':b,'scope':'paired passive drop distribution test; oracle uses exact hole center, NOT blind policy or randomized training'}

def sampling():
 a=mjfit.sample_pegs(8,seed=17,family='primitive');b=mjfit.sample_pegs(3,seed=17,family='primitive')
 assert json.dumps(a[:3],sort_keys=True)==json.dumps(b,sort_keys=True)
 rows=[]
 for i,c in enumerate(a):
  xml=mjfit.build(c);m=mujoco.MjModel.from_xml_string(xml);d=mujoco.MjData(m)
  for _ in range(20):mujoco.mj_step(m,d)
  assert np.isfinite(d.qpos).all()
  rows.append({'id':i,'ngeom':m.ngeom,'nmesh':m.nmesh,'time_s':d.time})
 (P/'sampled-configs.json').write_text(json.dumps(a,indent=2));(P/'sampled-results.json').write_text(json.dumps(rows,indent=2))
 return {'generated_compiled_stepped':8,'steps_each':20,'seed_prefix_reproducible':True,'geom_counts':[x['ngeom'] for x in rows],'scope':'real mjfit.sample_pegs/build/compile/step, not learned insertion'}

def evidence():
 k,n=173,237;z=1.95996398454;p=k/n;den=1+z*z/n;mid=(p+z*z/(2*n))/den;half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
 # Contact time-constant settings and timestep sensitivity for this single blocked case.
 fine=trial(offset=(.002,0),dt=.0005);base=trial(offset=(.002,0),dt=.001)
 return {'paper_success_count':k,'paper_trial_count':n,'paper_fraction_recomputed':p,'wilson95':[mid-half,mid+half],'scope':'counts are authors reported; only interval calculation ours','blocked_drop_dt05ms':fine['drop_mm'],'blocked_drop_dt1ms':base['drop_mm'],'dt_sensitivity_scope':'one passive scene, not convergence proof'}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('step',choices=['env','clearance','randomize','sampling','evidence']);a=ap.parse_args();out=globals()[a.step]();(P/(a.step+'-summary.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False,indent=2))
