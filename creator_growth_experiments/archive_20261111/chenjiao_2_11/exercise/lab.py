import math,sys,json
from pathlib import Path
P=Path(__file__).parent;s=sys.argv[1]
def wilson(k,n):
 z=1.96;p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d;h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;return (c-h,c+h)
if s=='prepare':
 rows=[['A','warm',80,100],['A','cold',10,100],['B','warm',9,10],['B','cold',120,1000]];(P/'synthetic.json').write_text(json.dumps(rows));print('synthetic cohorts=',rows,'NOT author analytics')
elif s=='interval':
 a=wilson(8,100);b=wilson(12,100);print('8/100 CI95=',a,'12/100 CI95=',b);assert a[1]>b[0]
elif s=='confounding':
 rows=json.loads((P/'synthetic.json').read_text());a=90/200;b=129/1010;print('aggregate A=',a,'B=',b,'within warm B .90 > A .80; cold B .12 > A .10');assert a>b and .90>.80 and .12>.10
elif s=='cost':
 for hours,followers in [(2,8),(4,12)]:print('hours=',hours,'follows=',followers,'labor_cost_per_follow=',hours*50/followers)
 print('pre-register: same audience, fixed 14 posts, no optional stopping, no automatic publishing')
