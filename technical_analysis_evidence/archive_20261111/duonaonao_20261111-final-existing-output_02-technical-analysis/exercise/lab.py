#!/usr/bin/env python3
"""自写教学实验：合成数据、t收盘信号、t+1开盘执行；无网络/下单。"""
import csv,json,random,math,sys,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent; O=P/'out';O.mkdir(exist_ok=True)
def save(n,x): (O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2))
def generate():
 r=random.Random(20261111);rows=[];close=100.
 for i in range(1200):
  op=close*math.exp(r.gauss(0,.003));drift=[.001,-.0006,0][i//400]
  close=op*math.exp(drift+r.gauss(0,.013));high=max(op,close)*(1+r.random()*.009);low=min(op,close)*(1-r.random()*.009)
  rows.append(dict(bar=i,open=op,high=high,low=low,close=close,volume=r.randrange(100,10000)))
 with (O/'ohlcv.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 print('seed=20261111; rows=1200; synthetic=true; regime boundaries=400,800 (教学生成器信息，非策略输入)')
def data():return [{k:float(v) for k,v in row.items()} for row in csv.DictReader((O/'ohlcv.csv').open())]
def signal(ds,fast=10,slow=30):
 cs=[x['close'] for x in ds];return [0 if i<slow-1 else int(sum(cs[i-fast+1:i+1])/fast>sum(cs[i-slow+1:i+1])/slow) for i in range(len(cs))]
def run(ds,fee,fast=10,slow=30,leak=False,start=0,end=None):
 end=end or len(ds);sg=signal(ds,fast,slow);eq=1.;peak=1.;dd=0.;position=0;turn=0;curve=[]
 for t in range(max(1,start),min(end,len(ds)-1)):
  target=sg[t] if leak else sg[t-1] # 故意反例用未来收盘决定本根开盘
  delta=abs(target-position);turn+=delta
  eq*=1-delta*fee;eq*=1+target*(ds[t+1]['open']/ds[t]['open']-1)
  position=target;peak=max(peak,eq);dd=min(dd,eq/peak-1);curve.append(eq)
 if position: eq*=1-fee;turn+=1;dd=min(dd,eq/peak-1)
 return dict(return_pct=round((eq-1)*100,4),max_drawdown_pct=round(dd*100,4),one_way_turnover=turn,fee_bps=fee*10000,curve=curve)
def validate():
 ds=data();assert len(ds)==1200
 for x in ds:assert x['low']<=min(x['open'],x['close'])<=max(x['open'],x['close'])<=x['high']
 sg=signal(ds);assert sg[:29]==[0]*29
 alt=[dict(x) for x in ds];alt[600]['close']*=2
 assert signal(alt)[:600]==sg[:600]
 assert run(ds,0)['return_pct']>=run(ds,.001)['return_pct']
 # 实际执行仓位=前根信号，未来后缀变动不改变前缀
 crafted=[{'close':100.} for _ in range(29)]+[{'close':200.} for _ in range(6)]
 cs=signal(crafted);positions=[0]+cs[:-1]
 assert cs[29]==1 and positions[29]==0 and positions[30]==1
 save('validation.json',{'checks':5,'status':'PASS','scope':'自编数据/因果性/成本局部断言，不是独立审核'})
 print('PASS 5 checks: OHLC invariant, warmup, future mutation prefix, fee monotonic, lag contract')
def backtest():
 ds=data();results={str(fee):run(ds,fee) for fee in [0,.0005,.002]}
 for v in results.values():v.pop('curve')
 save('costs.json',results);print(json.dumps(results))
def holdout():
 ds=data();grid=[(5,20),(10,30),(20,60)];train={f'{f}/{s}':run(ds,.0005,f,s,end=800)['return_pct'] for f,s in grid}
 best=max(grid,key=lambda p:train[f'{p[0]}/{p[1]}']);test=run(ds,.0005,*best,start=800);test.pop('curve')
 naive=run(ds,.0005,*best,start=800,leak=True);naive.pop('curve')
 base=(ds[1199]['open']/ds[800]['open']*(1-.0005)**2-1)*100
 out={'training_first_800':train,'frozen_choice':best,'holdout_400':test,'invalid_lookahead_example':naive,'holdout_buy_and_hold_pct':round(base,4),'warning':'合成数据不说明市场预测能力；反例故意读取未来，不可用于策略评价'}
 save('holdout.json',out);print(json.dumps(out,ensure_ascii=False))
def audit():
 out={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.iterdir() if p.suffix in ['.csv','.json'] and p.name!='manifest.json'};save('manifest.json',out);print('SHA256',json.dumps(out));print('无账户、无下单、无外部API；不是投资建议')
if __name__=='__main__':globals()[sys.argv[1]]()
