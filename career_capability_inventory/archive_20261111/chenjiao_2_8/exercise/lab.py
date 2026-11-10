import sys,json
from pathlib import Path
mode=sys.argv[1]
if mode=='baseline':
 d={'monthly_income':10000,'essential':6000,'optional':1000,'liquid_savings':30000};Path('exercise/scenario.json').write_text(json.dumps(d));surplus=d['monthly_income']-d['essential']-d['optional'];assert surplus==3000;print('synthetic baseline surplus=',surplus,'CNY/month; NOT user financial data')
elif mode=='runway':
 d=json.load(open('exercise/scenario.json'));r=d['liquid_savings']/d['essential'];stress=d['liquid_savings']/(d['essential']*1.2);assert r==5;print('zero income, essentials only: runway=',r,'months; expenses +20% ->',round(stress,3),'months; simplified')
elif mode=='cost':
 d=json.load(open('exercise/scenario.json'));tool=300;surplus=d['monthly_income']-d['essential']-d['optional']-tool;assert surplus==2700;print('hypothetical tools 300/month -> surplus=',surplus,'annual tool cost=',tool*12,'; no subscriptions purchased')
elif mode=='priority':
 actions=[('整理现有笔记',0,2,True),('用现有电脑做CSV工具',0,3,True),('先购买新设备',8000,1,False)]
 safe=[x[0] for x in actions if x[1]==0 and x[3]];assert len(safe)==2;print('reversible zero-purchase learning actions=',safe,'; arbitrary ranking is not earnings forecast')
