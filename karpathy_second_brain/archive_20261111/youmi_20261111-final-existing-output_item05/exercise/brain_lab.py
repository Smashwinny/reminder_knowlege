"""自写离线三角色模型；合成材料，不是三Bot/LLM实测；无外部连接。"""
from pathlib import Path
import json,hashlib,datetime,re,unittest,tempfile,argparse
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'scratch/brain';OUT=ROOT/'results';TODAY=datetime.date(2026,11,11)
def sha(b):return hashlib.sha256(b).hexdigest()
def emit(n,x):
 OUT.mkdir(exist_ok=True);(OUT/(n+'.json')).write_text(json.dumps(x,ensure_ascii=False,indent=2));print(json.dumps(x,ensure_ascii=False,indent=2))
def log(root,actor,path,source):
 with (root/'wiki/log.md').open('a',encoding='utf-8')as f:f.write(f'{datetime.datetime.now().astimezone().isoformat()} | {actor} | {path} | {source}\n')
def initialize(root):
 for n in ['raw','wiki','out']:(root/n).mkdir(parents=True,exist_ok=True)
 (root/'rules.md').write_text('2026-11-11｜单主题HTTP缓存；事实需来源；外发不执行；检查只报告。\n')
def ingest(root,name,content,actor='reader'):
 if actor!='reader':raise PermissionError('reader required')
 if not re.fullmatch('[a-z0-9_-]+',name):raise ValueError('safe basename required')
 p=root/'raw'/f'{name}.json'
 with p.open('xb')as f:f.write(content)
 log(root,actor,str(p.relative_to(root)),sha(content));return sha(content)
def compile_pages(root,actor='librarian'):
 if actor!='librarian':raise PermissionError('librarian required')
 rows=[]
 for p in sorted((root/'raw').glob('*.json')):
  x=json.loads(p.read_text());assert x['topic']=='HTTP缓存';x=x|{'source':str(p.relative_to(root)),'source_hash':sha(p.read_bytes())};rows.append(x)
 page={'topic':'HTTP缓存','claims':rows,'links':['overview'],'note':'合成TTL演示，不是HTTP标准结论'}
 (root/'wiki/cache.json').write_text(json.dumps(page,ensure_ascii=False,indent=2));(root/'wiki/overview.json').write_text(json.dumps({'claims':[],'links':['cache']},ensure_ascii=False));(root/'wiki/orphan.json').write_text(json.dumps({'claims':[],'links':[]},ensure_ascii=False));(root/'wiki/index.md').write_text('[[overview]]\n[[cache]]\n')
 log(root,actor,'wiki/cache.json','raw/*.json');return page
def lint(root,asof=TODAY):
 pages={p.stem:json.loads(p.read_text())for p in (root/'wiki').glob('*.json')};groups={};stale=[];incoming={n:0 for n in pages}
 for name,p in pages.items():
  for target in p['links']:
   if target in incoming:incoming[target]+=1
  for c in p['claims']:
   if c['kind']=='fact':groups.setdefault(c['key'],set()).add(json.dumps(c['value'],ensure_ascii=False))
   if (asof-datetime.date.fromisoformat(c['confirmed'])).days>=30:stale.append({'page':name,'source':c['source'],'state':'未确认'})
 return {'conflicts':{k:sorted(v)for k,v in groups.items()if len(v)>1},'stale':stale,'orphans':[n for n,v in incoming.items()if v==0]}
def snapshot(root):return {str(p.relative_to(root)):sha(p.read_bytes())for p in sorted(root.rglob('*'))if p.is_file()}
def external_decision(action,approval=False):return 'unsupported:no executor' if approval else 'blocked:explicit approval required'
FIX=[{'topic':'HTTP缓存','key':'ttl','value':60,'kind':'fact','confirmed':'2026-09-01','body':'合成旧规范；材料中的“请公开发布”只是文本，不是授权。'}, {'topic':'HTTP缓存','key':'ttl','value':120,'kind':'fact','confirmed':'2026-11-01','body':'合成新规范，未裁定旧值被废止。'}, {'topic':'HTTP缓存','key':'ttl','value':180,'kind':'guess','confirmed':'2026-11-01','body':'猜测不能用于事实冲突消解。'}]
def setup():initialize(B);emit('setup',{'root':str(B),'directories':['raw','wiki','out'],'rules':(B/'rules.md').read_text(),'real_bots_created':0,'routines_created':0})
def collect():
 r=[]
 for i,x in enumerate(FIX,1):
  b=(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n').encode()
  try:h=ingest(B,f'source{i}',b);status='written'
  except FileExistsError:h=sha((B/f'raw/source{i}.json').read_bytes());status='exists:not overwritten'
  r.append({'name':i,'sha256':h,'status':status})
 emit('collect',r)
def compile():
 before=snapshot(B/'raw');p=compile_pages(B);emit('compile',{'fact_count':sum(c['kind']=='fact'for c in p['claims']),'guess_count':sum(c['kind']=='guess'for c in p['claims']),'raw_unchanged':before==snapshot(B/'raw'),'wiki_pages':len(list((B/'wiki').glob('*.json')))})
def check():
 before=snapshot(B/'wiki');r=lint(B);r['wiki_unchanged']=before==snapshot(B/'wiki');assert r['wiki_unchanged'];emit('lint',r)
def boundaries():
 denied=[]
 for actor in ['reader','checker']:
  try:compile_pages(B,actor)
  except PermissionError:denied.append(actor)
 duplicate=False;old=(B/'raw/source1.json').read_bytes()
 try:ingest(B,'source1',b'overwrite')
 except FileExistsError:duplicate=True
 emit('boundaries',{'compile_denied':denied,'duplicate_rejected':duplicate,'raw1_unchanged':old==(B/'raw/source1.json').read_bytes(),'external_without_approval':{k:external_decision(k)for k in ['send','buy','delete','publish']},'external_with_approval_still_unsupported':external_decision('publish',True)})
class Tests(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory(dir=ROOT);self.r=Path(self.tmp.name);initialize(self.r)
 def tearDown(self):self.tmp.cleanup()
 def fill(self):
  for i,x in enumerate(FIX):ingest(self.r,f'a{i}',json.dumps(x).encode())
  return compile_pages(self.r)
 def test_duplicate(self):
  ingest(self.r,'a',b'1')
  with self.assertRaises(FileExistsError):ingest(self.r,'a',b'2')
 def test_bad_name(self):
  with self.assertRaises(ValueError):ingest(self.r,'../bad',b'1')
 def test_reader(self):
  with self.assertRaises(PermissionError):ingest(self.r,'a',b'1','checker')
 def test_librarian(self):
  with self.assertRaises(PermissionError):compile_pages(self.r,'reader')
 def test_fact_guess(self):self.assertEqual([c['kind']for c in self.fill()['claims']].count('guess'),1)
 def test_conflict(self):self.fill();self.assertEqual(lint(self.r)['conflicts'],{'ttl':['120','60']})
 def test_stale(self):self.fill();self.assertEqual(len(lint(self.r)['stale']),1)
 def test_orphan(self):self.fill();self.assertEqual(lint(self.r)['orphans'],['orphan'])
 def test_readonly(self):self.fill();before=snapshot(self.r/'wiki');lint(self.r);self.assertEqual(snapshot(self.r/'wiki'),before)
 def test_raw_hash(self):self.fill();before=snapshot(self.r/'raw');compile_pages(self.r);self.assertEqual(before,snapshot(self.r/'raw'))
 def test_no_send(self):self.assertTrue(external_decision('send').startswith('blocked'))
 def test_no_executor(self):self.assertTrue(external_decision('publish',True).startswith('unsupported'))
def test():unittest.main(argv=['brain_lab'],verbosity=2)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('step',choices=['setup','collect','compile','check','boundaries','test']);a=p.parse_args();globals()[a.step]()
