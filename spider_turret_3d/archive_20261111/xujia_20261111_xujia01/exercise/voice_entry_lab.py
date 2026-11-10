"""自写、零依赖、离线的证据/状态矩阵练习；不是 iOS 或 Grok Bot 实现。"""
import argparse, hashlib, json, pathlib, itertools, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'results'
def dump(name,data):
 OUT.mkdir(exist_ok=True);(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');print(json.dumps(data,ensure_ascii=False,indent=2))
def manifest():
 rows=[]
 for name in ['source-post-raw.txt','apple-vocal.html','apple-shortcuts.html']:
  p=ROOT/name;b=p.read_bytes();rows.append({'file':name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
 dump('manifest.json',rows)
def matrix():
 rows=[]
 for lock,noise,net in itertools.product(['unlocked','locked'],['quiet','noisy'],['online','offline']):
  rows.append({'case':len(rows)+1,'lock':lock,'noise':noise,'network':net,'trigger_observed':None,'app_open_observed':None,'reply_observed':None,'latency_ms':None,'status':'待真机验证'})
 dump('device-matrix.json',rows)
def audit(r):
 errs=[]
 for row in r:
  if row.get('status')=='真实完成' and not (row.get('trigger_observed') is True and row.get('app_open_observed') is True and row.get('reply_observed') is True):errs.append(row['case'])
 return errs
def negative():
 r=[{'case':1,'status':'真实完成','trigger_observed':True,'app_open_observed':True,'reply_observed':None}]
 dump('negative.json',{'synthetic_input':r,'rejected_cases':audit(r),'meaning':'检测到缺少语音回复证据；不是设备故障实测'})
class Tests(unittest.TestCase):
 def test_pending(self): self.assertEqual(audit([{'case':1,'status':'待真机验证'}]),[])
 def test_false_success(self): self.assertEqual(audit([{'case':2,'status':'真实完成'}]),[2])
 def test_partial(self): self.assertEqual(audit([{'case':3,'status':'真实完成','trigger_observed':True,'app_open_observed':True,'reply_observed':False}]),[3])
 def test_complete(self): self.assertEqual(audit([{'case':4,'status':'真实完成','trigger_observed':True,'app_open_observed':True,'reply_observed':True}]),[])
 def test_zero_not_missing(self): self.assertEqual(audit([{'case':5,'status':'真实完成','trigger_observed':1,'app_open_observed':True,'reply_observed':True}]),[5])
def report():
 r=json.loads((OUT/'device-matrix.json').read_text());dump('summary.json',{'matrix_cases':len(r),'measured_device_cases':sum(x['reply_observed'] is not None for x in r),'pending_device_cases':sum(x['status']=='待真机验证' for x in r),'false_success_in_matrix':audit(r),'cloud_scope':'来源指纹、试验设计、证据护栏；未操作iPhone'})
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('step',choices=['manifest','matrix','negative','test','report']);args=p.parse_args()
 if args.step=='test':unittest.main(argv=['voice_entry_lab'],verbosity=2)
 else:globals()[args.step]()
