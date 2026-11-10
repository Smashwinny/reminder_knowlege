"""作者/README历史报价算术复核，不是当前官方报价或实付账单。"""
import json
from decimal import Decimal as D
from pathlib import Path
rate=D('1.5');price=D('0.03125');seconds=D(67)*60
base=seconds*rate*price;claimed=D('191.47');over=claimed-base
r={'basis':'作者文章: 1.5积分/秒、约169元/小时、67分钟账单191.47元；README:0.03125元/积分','yuan_per_second':str(rate*price),'yuan_per_hour':str(D(3600)*rate*price),'base_67min_yuan':str(base),'author_claimed_bill_yuan':str(claimed),'difference_yuan':str(over),'equivalent_extra_seconds_not_measured':str(over/(rate*price)),'budget_100yuan_minutes':str(D(100)/(rate*price)/60),'24h_yuan_without_overhead':str(D(86400)*rate*price),'limits':'差额不能归因到某一次换装；预热、重启、舍入等占比未获原始账单，作者声称不作独立核验。'}
assert base==D('188.43750') and over==D('3.03250')
Path(__file__).with_name('cost-results.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps(r,ensure_ascii=False,indent=2))
