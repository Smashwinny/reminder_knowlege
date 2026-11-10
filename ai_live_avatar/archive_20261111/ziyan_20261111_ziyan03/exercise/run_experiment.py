"""离线运行固定 SHA 的纯逻辑；绝不实例化 Vidu/网络客户端。"""
import ast, hashlib, json, random, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'vendor'))
from live.moderation import Moderator
from live.router import classify
from live.queue import CommandQueue
m=Moderator.from_file(ROOT/'vendor/moderation.json')
q=CommandQueue('fifo',max_age_seconds=60,max_size=3)
rows=[]
inputs=[('A','你好'),('A','你好！'),('B','加我微信'),('C','今天又摸鱼了'),('D','比个心'),('E','背景换成海边'),('F','换衣服要等多久'),('G','穿泳装'),('H','😂😂'),('I','长'*41)]
for i,(u,t) in enumerate(inputs):
 v=m.check(u,t,now=1000+i)
 r={'user':u,'text':t,'accepted':v.ok,'reason':v.reason,'category':v.category}
 if v.ok:
  c=classify(u,t);c.created_at=1000+i;r['raw_intent']=c.kind
  # 教学适配层：只展示聊天和小动作；背景/道具/无衣柜换装不执行。
  if c.kind in {'background','object','garment'}:c.kind='chat';r['offline_gate']='visual -> chat'
  q.push(c);r['queue_ids']=[x.user for x in q.waiting()]
 rows.append(r)
picks=[]
while (c:=q.pick(now=1010)) is not None:picks.append({'user':c.user,'kind':c.kind})
assert sum(r['accepted'] for r in rows)==5
assert [x['user'] for x in picks]==['D','E','F']
# 明确时钟：61秒触发过期；preparing 不抢占 ready。
old=classify('old','你好');old.created_at=100
prep=classify('prep','你好');prep.created_at=160;prep.status='preparing'
ready=classify('ready','挥手');ready.created_at=160
q2=CommandQueue('fifo',max_age_seconds=60)
for c in [old,prep,ready]:q2.push(c)
assert q2.pick(now=161) is ready
assert old.status=='expired' and q2.pick(now=161) is None
prep.status='ready';assert q2.pick(now=161) is prep
# 仅 AST 编译上游真实函数，隔离 session 的 aiohttp/网络依赖；未重写逻辑。
src=(ROOT/'vendor/live/session.py').read_text();tree=ast.parse(src)
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='pick_idle_topic')
ns={'random':random};exec(compile(ast.Module(body=[node],type_ignores=[]),'<upstream-pick_idle_topic>','exec'),ns)
random.seed(20261111);topics=[f'原创人设话题{i:03d}' for i in range(100)];used=set();out=[];last=''
for _ in range(201):
 last=ns['pick_idle_topic'](topics,used,last);out.append(last)
assert len(set(out[:100]))==100 and len(set(out[100:200]))==100
assert out[99]!=out[100] and out[199]!=out[200]
try: ns['pick_idle_topic']([],set())
except IndexError: empty='IndexError: 空话题列表需要调用端兜底'
else: raise AssertionError('unexpected empty pool result')
# 边界证据：max_size 不是所有输入下的硬上限；不启用真实礼物逻辑。
q3=CommandQueue('fifo',max_size=2)
for i in range(3):q3.push(classify(str(i),'你好',gift=1))
assert len(q3.items)==3
result={'upstream_sha':'dc87db8ad53fb81cfe07dcac08215497dfa1a50d','mode':'stdlib-only offline pieces; no API, no streaming','inputs':rows,'accepted':5,'blocked':5,'fifo_max3_picks':picks,'expiry_and_preparing':'PASS','idle':{'draws':201,'unique_round1':100,'unique_round2':100,'boundary_no_repeat':True,'first10':out[:10],'empty_pool':empty},'queue_all_gift_counterexample':{'max_size':2,'actual_size':len(q3.items)},'source_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'vendor/live').glob('*.py')}}
(ROOT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
