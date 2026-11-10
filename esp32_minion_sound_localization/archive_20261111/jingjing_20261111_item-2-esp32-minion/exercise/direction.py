"""自写双麦理想远场数值实验，不是小黄人硬件或固件。"""
import numpy as np,json,sys,pathlib,math
P=pathlib.Path(__file__).parent
fs=48000;d=.08;c=343
mode=sys.argv[1]
if mode=='fixture':
 rng=np.random.default_rng(20261111);x=rng.normal(size=4096);signals={}
 for angle in [-60,-30,0,30,60]:
  lag=int(round(fs*d*math.sin(math.radians(angle))/c));y=np.zeros_like(x)
  if lag>=0:y[lag:]=x[:len(x)-lag] if lag else x
  else:y[:lag]=x[-lag:]
  signals[str(angle)+'_x']=x;signals[str(angle)+'_y']=y
 np.savez(P/'signals.npz',**signals);print('5 ideal broadband pairs; fs=48000 Hz, spacing=0.08 m; synthetic only')
elif mode=='run':
 a=np.load(P/'signals.npz');rows=[]
 for angle in [-60,-30,0,30,60]:
  x=a[str(angle)+'_x'];y=a[str(angle)+'_y'];lag=int(np.argmax(np.correlate(y,x,mode='full'))-len(x)+1);theta=math.degrees(math.asin(np.clip(lag*c/(fs*d),-1,1)))
  target=float(np.clip(90+theta,30,150));prev=90.;command=prev+float(np.clip(target-prev,-10,10));rows.append(dict(truth=angle,lag_samples=lag,estimate_deg=round(theta,3),error_deg=round(abs(theta-angle),3),target_deg=round(target,3),first_command_deg=round(command,3)))
 (P/'results.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
elif mode=='verify':
 rows=json.loads((P/'results.json').read_text());assert len(rows)==5
 assert max(r['error_deg'] for r in rows)<5
 assert all(30<=r['target_deg']<=150 for r in rows)
 assert all(abs(r['first_command_deg']-90)<=10 for r in rows)
 assert rows[0]['lag_samples']<0<rows[-1]['lag_samples']
 print('PASS 5 assertions; max error',max(r['error_deg'] for r in rows),'deg; no noise, reverberation, servo, board or API tested')
