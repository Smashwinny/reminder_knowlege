import json,sys
from pathlib import Path
P=Path(__file__).parent;S=P.parent/'sources';s=sys.argv[1]
if s=='inventory':
 for p in sorted(S.glob('*.json')):
  x=json.loads(p.read_text())
  if x.get('version'):print(p.stem,x['version'],x.get('gitHead','unknown'))
elif s=='catalog':
 tools=[{'name':f'tool_{i}','description':'synthetic description '*20,'parameters':{'type':'object','properties':{'query':{'type':'string'}}}} for i in range(100)]
 full=len(json.dumps(tools).encode());proxy=len(json.dumps({'name':'mcp','search':'string','tool':'string','args':'object'}).encode());print('synthetic catalog bytes=',full,'proxy bytes=',proxy,'ratio=',round(full/proxy,2));assert full>proxy;print('bytes NOT model tokens; lookup and result costs excluded')
elif s=='compression':
 old={'goal':'read only','forbidden':['send','delete'],'open':['verify original'],'history':'x'*10000};bad={'goal':old['goal']};good={k:v for k,v in old.items() if k!='history'}
 check=lambda x:all(k in x for k in ['goal','forbidden','open'])
 assert not check(bad) and check(good);print('bad_summary=rejected good_summary=accepted; deterministic field retention, NOT plugin quality')
elif s=='question':
 q={'question':'缺哪个输入？','options':['来源URL','离线文件'],'other':True};assert len(q['options'])>=2;print(json.dumps(q,ensure_ascii=False));print('no UI invoked; plugins NOT installed; no real credentials read')
