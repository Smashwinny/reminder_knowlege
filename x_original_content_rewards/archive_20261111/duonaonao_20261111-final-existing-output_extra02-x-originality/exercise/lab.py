"""Offline preflight: warnings only, no network, never posts."""
from pathlib import Path
import json,sys,re,unicodedata,hashlib
from difflib import SequenceMatcher
P=Path(__file__).parent;O=P/'out';O.mkdir(exist_ok=True)
def save(n,v): (O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
def norm(t):return ''.join(c for c in unicodedata.normalize('NFKC',t).lower() if c.isalnum())
def check(d,corpus):
 reasons=[];text=norm(d['text']);similar=max([SequenceMatcher(None,text,norm(x)).ratio() for x in corpus] or [0])
 if d['mode']=='reupload':reasons.append('REUPLOAD_NOT_QUOTE')
 if d['third_party']:
  if d.get('rights') not in ['permission','licensed']:reasons.append('RIGHTS_UNVERIFIED')
  if not d.get('attribution'):reasons.append('MISSING_ATTRIBUTION')
  if not re.match(r'^https://x[.]com/[^/]+/status/[0-9]+$',d.get('source_url','')):reasons.append('MISSING_CANONICAL_SOURCE')
 if d['mode']=='quote' and not d.get('source_url'):reasons.append('QUOTE_WITHOUT_LINK')
 if d.get('automated'):reasons.append('AUTOMATION_REVIEW')
 if similar>=0.85:reasons.append('HIGH_TEXT_SIMILARITY')
 return dict(id=d['id'],result='review' if reasons else 'no_rule_hit',reasons=reasons,similarity=round(similar,4),legal_clearance=False,platform_approval=False)
def load():return json.loads((O/'fixtures.json').read_text())
cmd=sys.argv[1]
if cmd=='init':
 base=dict(text='我用自绘几何素材测试两种遮挡顺序，黑边占画布高度的18%。',mode='original',third_party=False,automated=False)
 cases=[]
 def add(i,expect,**kw):cases.append(dict(base,id=i,expected=expect,**kw))
 add('self_written','no_rule_hit')
 add('unlicensed_reupload','review',third_party=True,mode='reupload',text='下载别人作品后重新上传。')
 add('credited_but_no_permission','review',third_party=True,attribution='示例作者',source_url='https://x.com/example/status/1',text='署名不等于拥有商用许可。')
 add('quote_with_ledger','no_rule_hit',third_party=True,rights='permission',mode='quote',attribution='示例作者',source_url='https://x.com/example/status/1',text='这里补充我自己的实验，不重传第三方媒体。')
 add('quote_missing_link','review',mode='quote',third_party=True,rights='permission',attribution='示例作者',text='我想引用一篇没有记录链接的帖子。')
 add('automated_copy','review',automated=True,text='自动批量发布也必须停下来人工审查。')
 add('exact_copy','review',text='这是一条用于离线测试的合成来源文本，不属于真实作者。')
 add('unicode_copy','review',text='ＡＢＣ１２３ test!')
 add('semantic_paraphrase_known_miss','no_rule_hit',text='太阳一落山，这里就凉快了。')
 add('short_common_phrase_known_false_alarm','review',text='Hello world')
 save('fixtures.json',dict(corpus=['这是一条用于离线测试的合成来源文本，不属于真实作者。','ABC123 TEST','日落之后温度降低','Hello world'],drafts=cases))
 print('created 10 synthetic drafts + 4 synthetic sources; no real account data')
elif cmd=='scan':
 d=load();r=[check(x,d['corpus']) for x in d['drafts']];save('results.json',r)
 print('drafts=',len(r),'review=',sum(x['result']=='review' for x in r),'no_rule_hit=',sum(x['result']=='no_rule_hit' for x in r));print('No-rule-hit != original / legal / approved; nothing published')
elif cmd=='test':
 d=load();r={x['id']:x for x in json.loads((O/'results.json').read_text())}
 for x in d['drafts']: assert r[x['id']]['result']==x['expected'],x['id']
 assert 'HIGH_TEXT_SIMILARITY' in r['unicode_copy']['reasons']
 assert r['semantic_paraphrase_known_miss']['result']=='no_rule_hit'
 print('10/10 fixture assertions passed; explicitly reproduced 1 semantic miss + 1 common-phrase false alarm')
 print('Rules catch ledger gaps, not plagiarism in general; no external search coverage')
elif cmd=='report':
 r=json.loads((O/'results.json').read_text());rows=['# Offline preflight review queue','No automatic publishing. Human review required for every draft.']
 rows += [x['id']+' | '+x['result']+' | '+(', '.join(x['reasons']) or 'no hit; manually check originality and rights') for x in r]
 (O/'review-queue.md').write_text('\n'.join(rows));print('wrote out/review-queue.md; 10 drafts queued for human review; posting calls=0')
elif cmd=='audit':
 manifest={str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(O.iterdir()) if f.is_file() and f.name!='manifest.json'};save('manifest.json',manifest)
 assert all(not x['legal_clearance'] and not x['platform_approval'] for x in json.loads((O/'results.json').read_text()))
 print('sha256 manifest entries=',len(manifest));print('legal_clearance=false and platform_approval=false for all 10 drafts; network calls=0')
else:raise SystemExit('init|scan|test|report|audit')
