from pathlib import Path
import sys,json,hashlib,platform
P=Path(__file__).parent
step=int(sys.argv[1])
def emit(**v):
 print(json.dumps(v,ensure_ascii=False,sort_keys=True))
 (P/f"result-{step}.json").write_text(json.dumps(v,ensure_ascii=False,indent=2))

# 自写按称呼路由器，仅字符串/设备状态，无模型或CLI调用。
if step==1:emit(python=platform.python_version(),layers=['设备固件','ASR/TTS网关','Agent或模型'],scope='合成输入路由，不是上游网关集成')
if step==2:
 aliases={'Claude':'claude','DeepSeek':'deepseek'};current={};out=[]
 for dev,text in [('A','嗨 Claude，整理笔记'),('B','嗨 DeepSeek，解释PWM'),('A','继续'),('B','继续')]:
  for alias,agent in aliases.items():
   if text.startswith('嗨 '+alias):current[dev]=agent
  out.append([dev,current.get(dev,'default')])
 assert out==[['A','claude'],['B','deepseek'],['A','claude'],['B','deepseek']]
 (P/'routes.json').write_text(json.dumps(current));emit(routes=out,device_isolation=True)
if step==3:
 state=json.loads((P/'routes.json').read_text());assert state=={'A':'claude','B':'deepseek'}
 emit(reloaded=state,unknown_alias_policy='保留既有路由或默认，不执行未知命令',persistence='仅本地JSON正常写读；非崩溃一致性证明')
if step==4:
 states=['accepted','waiting','timed_out','reply_ready'];assert states[-1]!='played'
 emit(states=states,retry_submissions=0,played=False,warning='超时不是取消，也不是可以重新派单的证据')
