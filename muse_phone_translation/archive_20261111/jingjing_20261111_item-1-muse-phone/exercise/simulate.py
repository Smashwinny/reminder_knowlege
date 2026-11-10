"""自写离线角色/验证状态机；不是Muse实现，无电话或网络。"""
import json,sys,pathlib
ROOT=pathlib.Path(__file__).parent

def transition(state,event):
    rules={('draft','consent'):'approved',('approved','business_connected'):'interpreting',('interpreting','verify'):'awaiting_user',('awaiting_user','user_verifies'):'interpreting',('interpreting','done'):'finished'}
    if event in ('share_otp','impersonate_user','unapproved_purchase'): return 'rejected'
    if event=='disconnect': return 'outcome_unknown'
    return rules.get((state,event),'rejected')

def run(events):
    s='draft'; trace=[s]
    for e in events:s=transition(s,e);trace.append(s)
    return trace
mode=sys.argv[1]
if mode=='fixture':
    cases={'normal':['consent','business_connected','verify','user_verifies','done'],'no_consent':['business_connected'],'otp':['consent','business_connected','share_otp'],'disconnect':['consent','business_connected','disconnect','done']}
    ROOT.joinpath('cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2));print('4 synthetic scenarios written; real calls=0')
elif mode=='run':
    cases=json.loads(ROOT.joinpath('cases.json').read_text());out={k:run(v) for k,v in cases.items()};ROOT.joinpath('results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False,indent=2))
elif mode=='verify':
    r=json.loads(ROOT.joinpath('results.json').read_text());assert r['normal'][-1]=='finished';assert r['no_consent'][-1]=='rejected';assert r['otp'][-1]=='rejected';assert 'outcome_unknown' in r['disconnect'];assert r['disconnect'][-1]=='rejected';print('PASS 5 assertions; no real Muse, translation, PSTN, identity or service resolution tested')
