from pathlib import Path
import sys,json,hashlib,platform
P=Path(__file__).parent
step=int(sys.argv[1])
def emit(**v):
 print(json.dumps(v,ensure_ascii=False,sort_keys=True))
 (P/f"result-{step}.json").write_text(json.dumps(v,ensure_ascii=False,indent=2))

# 自写数值教学模型，不是原网页/AVR CPU模拟器。
def colour(cm):return 'RED' if cm<20 else 'AMBER' if cm<50 else 'GREEN'
if step==1:emit(python=platform.python_version(),scope='HC-SR04往返时间算术与迟滞交通灯状态机')
if step==2:
 values=[(us,round(us*0.0343/2,3)) for us in [580,1160,2915]]
 assert values[0][1]==9.947
 emit(temperature_assumption='声速343 m/s；没有温度/硬件校准',echo_us_distance_cm=values)
if step==3:
 samples=[10,19.9,20,49.9,50,100];out=[colour(x) for x in samples]
 assert out==['RED','RED','AMBER','AMBER','GREEN','GREEN']
 (P/'trace.csv').write_text('cm,colour\n'+'\n'.join(f'{x},{colour(x)}' for x in samples))
 emit(samples=samples,colours=out,mutual_exclusion=True)
if step==4:
 samples=[19,21,19,21,19,21];raw=[colour(x) for x in samples];state='RED';stable=[]
 for x in samples:
  if state=='RED' and x>=23:state='AMBER'
  elif state=='AMBER' and x<17:state='RED'
  stable.append(state)
 changes=lambda a:sum(x!=y for x,y in zip(a,a[1:]))
 assert changes(raw)==5 and changes(stable)==0
 emit(noisy_cm=samples,raw_transitions=changes(raw),hysteresis_transitions=changes(stable),warning='迟滞仅演示17/23cm边界，不是安全刹车系统')
