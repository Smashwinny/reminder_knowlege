from pathlib import Path
import sys,json,hashlib,platform
P=Path(__file__).parent
step=int(sys.argv[1])
def emit(**v):
 print(json.dumps(v,ensure_ascii=False,sort_keys=True))
 (P/f"result-{step}.json").write_text(json.dumps(v,ensure_ascii=False,indent=2))

# 自写教学夹具：ADB host smart socket，不连接任何设备。
def frame(s):
 b=s.encode();return f'{len(b):04x}'.encode()+b
def parse(b):
 n=int(b[:4],16)
 if len(b)!=n+4:raise ValueError('length mismatch')
 return b[4:].decode()
if step==1:emit(python=platform.python_version(),scope='离线ADB帧与可逆状态夹具；无设备连接')
if step==2:
 a=frame('host:devices-l');assert parse(a)=='host:devices-l'
 try:parse(a[:-1]);raise AssertionError()
 except ValueError:pass
 emit(frame_hex=a.hex(),prefix=a[:4].decode(),payload=parse(a),truncated='rejected')
if step==3:
 old={'launcher':'vendor.home','ad.demo':True,'input':True};state=old.copy();state['launcher']='demo.home';state['ad.demo']=False
 journal=[{'key':k,'old':old[k],'new':state[k]} for k in state if state[k]!=old[k]]
 for j in reversed(journal):state[j['key']]=j['old']
 assert state==old
 emit(changes=journal,restored=state==old,hardware='待验证')
if step==4:
 def light(v):
  if not 0<=v<=100:raise ValueError('brightness')
  return {'brightness':v}
 results=[light(v) for v in [0,25,50,100]]
 try:light(101);raise AssertionError()
 except ValueError:pass
 emit(scene=results,invalid='rejected',claims='只验证模拟控制值，不证明灯具/相机兼容')
