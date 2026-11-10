#!/usr/bin/env python3
"""自编零依赖发行初筛实验；不是平台 SDK、法律引擎或发行审批。"""
import argparse,csv,hashlib,json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
DATA=ROOT/'data'; OUT=ROOT/'results'
def save(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def load(p):return json.loads(p.read_text())
# 文档事实由人工实读；费用不是SDK/制作/税务总成本。None表示未知，不是0。
CHANNELS=[
 dict(id='apple',name='App Store',builds=['ios'],modes=['paid','iap','ads'],once_usd=0,annual_usd=99,per_app_usd=0,sources=['S01','S13'],web_exclusive=False,curated=True),
 dict(id='play',name='Google Play',builds=['android'],modes=['paid','iap','ads'],once_usd=25,annual_usd=0,per_app_usd=0,sources=['S02','S12'],web_exclusive=False,curated=True),
 dict(id='steam',name='Steam',builds=['desktop'],modes=['paid','iap'],once_usd=0,annual_usd=0,per_app_usd=100,sources=['S03'],web_exclusive=False,curated=True),
 dict(id='itch-download',name='itch 下载',builds=['desktop','android','html5'],modes=['paid','donation'],once_usd=0,annual_usd=0,per_app_usd=0,sources=['S04','S06'],web_exclusive=False,curated=False),
 dict(id='itch-html5',name='itch 浏览器',builds=['html5'],modes=['donation'],once_usd=0,annual_usd=0,per_app_usd=0,sources=['S04','S05','S06'],web_exclusive=False,curated=False),
 dict(id='poki',name='Poki',builds=['html5'],modes=['ads'],once_usd=None,annual_usd=None,per_app_usd=None,sources=['S07'],web_exclusive=True,curated=True),
 dict(id='wechat',name='微信小游戏',builds=['wechat'],modes=['ads'],once_usd=None,annual_usd=None,per_app_usd=None,sources=['S08','S09','S10','S11'],web_exclusive=False,curated=True)
]
PROFILES=[
 dict(id='A',description='合成：HTML5原型，仅浏览器试玩/捐赠，不接受网页独占',build='html5',mode='donation',browser_only=True,budget_usd=0,accept_exclusive=False,domestic=False),
 dict(id='B',description='合成：PC买断，1款作品，准入费上限100美元',build='desktop',mode='paid',browser_only=False,budget_usd=100,accept_exclusive=False,domestic=False),
 dict(id='C',description='合成：国内微信广告小游戏，资质尚未核实',build='wechat',mode='ads',browser_only=False,budget_usd=100,accept_exclusive=False,domestic=True)
]
def cost(c,years=1,apps=1):
 if any(c[k] is None for k in ['once_usd','annual_usd','per_app_usd']):return None
 return c['once_usd']+math.ceil(years)*c['annual_usd']+apps*c['per_app_usd']
def assess(c,p):
 reasons=[]
 if p['build'] not in c['builds']:reasons.append('构建目标不匹配')
 if p['mode'] not in c['modes']:reasons.append('本实验核实的变现模式不匹配')
 if p['browser_only'] and c['id']=='itch-download':reasons.append('下载模式不满足浏览器内试玩目标')
 if c['web_exclusive'] and not p['accept_exclusive']:reasons.append('不接受网页独占')
 fee=cost(c)
 if fee is not None and fee>p['budget_usd']:reasons.append('已知准入费超预算')
 pending=['主体/地区/收款税务/内容/隐私与实际平台审核均未验证']
 if c['curated']:pending.append('平台审查或合作接纳待验证')
 if fee is None:pending.append('费用未知，不能按0计入预算')
 if p['domestic']:pending.append('国内出版/备案/广告资格必须分别核实')
 return dict(profile=p['id'],channel=c['id'],name=c['name'],status='排除' if reasons else ('待核' if fee is None or p['domestic'] else '候选'),fee_usd=fee,reasons=reasons,pending=pending,sources=c['sources'])
def validate(channels,sources):
 ids={s['id'] for s in sources}
 assert len(channels)==len({c['id'] for c in channels})
 for c in channels:
  assert c['sources'] and set(c['sources'])<=ids
  assert all(c[k] is None or c[k]>=0 for k in ['once_usd','annual_usd','per_app_usd'])
 return {'channels':len(channels),'source_ids_used':len(set(s for c in channels for s in c['sources'])),'unknown_fee_channels':[c['id'] for c in channels if cost(c) is None]}
def main(action):
 OUT.mkdir(exist_ok=True)
 if action=='init':
  save(DATA/'channels.json',CHANNELS);save(DATA/'profiles.json',PROFILES)
  print('init: 7渠道记录，3个合成画像；官方费用+人工结构化，画像不是用户数据')
 elif action=='validate':
  r=validate(load(DATA/'channels.json'),load(ROOT.parent/'sources.json'));save(OUT/'validation.json',r);print(json.dumps(r,ensure_ascii=False))
 elif action=='shortlist':
  cs=load(DATA/'channels.json');ps=load(DATA/'profiles.json');rs=[assess(c,p) for p in ps for c in cs];save(OUT/'shortlist.json',rs)
  with (OUT/'shortlist.csv').open('w',newline='') as f:
   w=csv.writer(f);w.writerow(['画像','渠道','状态','准入费USD','排除原因','未验证']);w.writerows((r['profile'],r['name'],r['status'],r['fee_usd'] if r['fee_usd'] is not None else '未知','；'.join(r['reasons']),'；'.join(r['pending'])) for r in rs)
  for p in ps:
   print(p['id']+': '+json.dumps({s:[r['channel'] for r in rs if r['profile']==p['id'] and r['status']==s] for s in ['候选','待核','排除']},ensure_ascii=False))
 elif action=='costs':
  cs=load(DATA/'channels.json');r={c['id']:{'1年1款':cost(c,1,1),'3年2款':cost(c,3,2)} for c in cs};save(OUT/'costs.json',r)
  print(json.dumps(r,ensure_ascii=False));print('仅准入费；Steam回收未抵扣；税费/制作/抽成/退款/支付费未计入')
 elif action=='test':
  cs=load(DATA/'channels.json');by={c['id']:c for c in cs};a,b,c=PROFILES;tests=[]
  def check(n,x):assert x,n;tests.append(n)
  check('A浏览器候选itch',assess(by['itch-html5'],a)['status']=='候选')
  check('A不误荐付费下载',assess(by['itch-download'],a)['status']=='排除')
  check('B Steam准入100',assess(by['steam'],b)['fee_usd']==100)
  check('B Steam候选非审批',assess(by['steam'],b)['status']=='候选')
  check('C合规未知不放行',assess(by['wechat'],c)['status']=='待核')
  check('Poki费用未知不是零',cost(by['poki']) is None)
  check('Poki网页独占冲突', '不接受网页独占' in assess(by['poki'],dict(a,mode='ads'))['reasons'])
  check('Apple三年两款297',cost(by['apple'],3,2)==297)
  check('Play三年两款25',cost(by['play'],3,2)==25)
  check('Steam三年两款200',cost(by['steam'],3,2)==200)
  check('未承诺永久',assess(by['play'],dict(b,build='android'))['pending']!=[])
  check('超预算被拒',assess(by['steam'],dict(b,budget_usd=99))['status']=='排除')
  check('itch HTML5不误支持买断',assess(by['itch-html5'],dict(a,mode='paid'))['status']=='排除')
  bad=[dict(cs[0],sources=['FAKE'])]
  try:validate(bad,load(ROOT.parent/'sources.json')); rejected=False
  except AssertionError:rejected=True
  check('伪造来源ID拒收',rejected)
  save(OUT/'tests.json',{'passed':len(tests),'tests':tests,'scope':'自编模型局部断言，非独立审核/平台SDK测试'});print(f'PASS {len(tests)}/{len(tests)} 自编模型断言；非平台接入验收')
 elif action=='audit':
  paths=sorted([*DATA.glob('*.json'),*(p for p in OUT.glob('*.json') if p.name!='manifest.json'),OUT/'shortlist.csv',ROOT/'lab.py'])
  hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths};save(OUT/'manifest.json',{'sha256':hashes,'network_during_lab':False,'publishing':False});print(f'audit: {len(hashes)}个文件指纹；无网络调用，无发布，无账号操作')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=['init','validate','shortlist','costs','test','audit']);main(p.parse_args().action)
