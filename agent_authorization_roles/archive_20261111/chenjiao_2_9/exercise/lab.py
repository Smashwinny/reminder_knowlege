import json,hashlib,sys
from pathlib import Path
P=Path(__file__).parent
stage=sys.argv[1]
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()
if stage=='prepare':
 x={'owns':'公开资料对比报告','inputs':['三条公开资料'],'may':['read','draft'],'must_ask':['send','delete'],'done':['来源齐全','缺口明确']};(P/'role.json').write_text(json.dumps(x,ensure_ascii=False));print(json.dumps(x,ensure_ascii=False))
elif stage=='gate':
 def gate(action,approval=False):return 'allow' if action in ['read','draft'] else 'park'
 rows={x:gate(x) for x in ['read','draft','send','delete','unknown']};assert list(rows.values())==['allow','allow','park','park','park'];print(rows)
elif stage=='binding':
 proposal={'tool':'send','target':'demo.invalid','body':'draft only'};approval=digest(proposal);changed={**proposal,'body':'changed'};assert digest(changed)!=approval
 used=set();consume=lambda k:False if k in used else (used.add(k) or True)
 assert consume(approval) and not consume(approval);print('changed_parameters=rejected replay=rejected; external_sent=0 (local token simulation only)')
elif stage=='probation':
 clean=[True,True,True,True,True];bad=[True,True,False,True,True];eligible=lambda xs,rollback:len(xs)>=5 and all(xs[-5:]) and rollback
 assert eligible(clean,True) and not eligible(bad,True) and not eligible(clean,False)
 print('5 clean + rollback => eligible; failure/no rollback => denied; 0.8^5=',0.8**5)
