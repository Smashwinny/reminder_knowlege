from decimal import Decimal as D
import json,sys,math,csv
from pathlib import Path
P=Path(__file__).parent
s=sys.argv[1]
# 教学假设：所有订单均消耗进货、出库、获客；退款单全额退货款，退回货物保守计不回收。
def margin(ret,ad):return (D('29.9')*(1-ret))-(D('9.9')+D('4')+D('1')+ad+D('29.9')*D('.05')*(1-ret)+ret*D('5'))
if s=='prepare':
 a={'price':'29.9','purchase':'9.9','shipping':'4','packaging':'1','fee_rate':'.05','return_cost':'5','fixed':'900','note':'hypothetical; not a real merchant ledger'};(P/'assumptions.json').write_text(json.dumps(a));print(a)
elif s=='base':
 m=margin(D('.1'),D('5'));q=math.ceil(D('900')/m);assert m>0;print('unit_contribution=',m,'break_even_orders=',q,'100_orders_net=',100*m-900)
elif s=='sensitivity':
 rows=[]
 for ret in ['0','.1','.2','.3']:
  for ad in ['0','5','10','15']:rows.append([ret,ad,str(margin(D(ret),D(ad)))])
 with (P/'sensitivity.csv').open('w') as f:csv.writer(f).writerows([['return_rate','ad_per_order','contribution']]+rows)
 print('scenarios=',len(rows),'negative=',sum(D(x[2])<0 for x in rows),'worst=',min(D(x[2]) for x in rows))
elif s=='million':
 m=margin(D('.1'),D('5'));rev_orders=math.ceil(D('1000000')/D('29.9'));profit_orders=math.ceil((D('1000000')+D('900'))/m)
 print('1M gross revenue needs orders=',rev_orders,'1M hypothetical contribution-minus-fixed needs=',profit_orders);assert profit_orders>rev_orders
