"""自写、零API：真实文章结构审计 + 明确合成的筛选/敏感性实验。不评价真人账号。"""
from pathlib import Path
import json,re,hashlib,statistics,math,unittest,argparse
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results'
def save(n,d):
 OUT.mkdir(exist_ok=True);(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(json.dumps(d,ensure_ascii=False,indent=2))
def manifest():
 save('manifest.json',[{'file':n,'bytes':len((b:=(ROOT/n).read_bytes())),'sha256':hashlib.sha256(b).hexdigest()}for n in ['source-post.json','article.txt','x-data-dictionary.html','python-statistics.html']])
def audit():
 s=(ROOT/'article.txt').read_text();a=s.index('二、Top 30');b=s.index('二、完整名单',a);c=s.index('✅ 以上',b);top=re.findall(r'@([A-Za-z0-9_]{1,15})',s[a:b]);full=re.findall(r'@([A-Za-z0-9_]{1,15})',s[b:c]);allnames=top+full;fold=[x.lower()for x in allnames]
 result={'top_count':len(top),'full_count':len(full),'total':len(allnames),'unique_casefold':len(set(fold)),'cross_duplicates':sorted(set(x.lower()for x in top)&set(x.lower()for x in full)),'new_markers_literal':s[a:c].count('🆕'),'marked_account_rows':sum('🆕'in line and bool(re.search(r'@[A-Za-z0-9_]{1,15}',line))for line in s[a:c].splitlines()),'arithmetic_old':94+7+45,'arithmetic_drop_reasons':14+11+8+3+3+3+3,'arithmetic_final':180+42-4-20,'category_sum':30+94+28+20+20+6,'real_metric_rows_available':0}
 assert result['total']==result['unique_casefold']==198
 save('article-audit.json',result);save('extracted-handles.json',{'top30':top,'full168':full,'note':'原文结构核验，不是当前账号有效性/入选标准复核'})
def num(v):return isinstance(v,(int,float))and not isinstance(v,bool)and math.isfinite(v)
def metric(v,t):return None if not num(v)else v>=t
def evaluate(x,view_floor=300,day_limit=14):
 reasons=[];unknown=[]
 for name,pred in [('followers',lambda v:v>=5000),('days',lambda v:0<=v<=day_limit),('originals',lambda v:8<=v<=450),('zh_share',lambda v:0.5<v<=1)]:
  v=x.get(name)
  if not num(v):unknown.append(name)
  elif not pred(v):reasons.append(name)
 for flag in ['promotion','excluded_topic']:
  if x.get(flag) is True:reasons.append(flag)
  elif x.get(flag) is not False:unknown.append(flag)
 f=x.get('followers')
 if num(f):
  a=metric(x.get('median_views'),max(view_floor,0.01*f));b=metric(x.get('median_likes'),max(5,0.0002*f))
  if a is not True and b is not True:
   if a is False and b is False:reasons.append('interaction')
   else:unknown.append('interaction')
 else:unknown.append('interaction')
 return {'status':'reject'if reasons else('unknown'if unknown else'pass'),'reasons':reasons,'unknown':unknown}
def base(**kw):return {'followers':5000,'days':14,'originals':8,'zh_share':5/8,'median_views':300,'median_likes':0,'promotion':False,'excluded_topic':False}|kw
CASES={'boundary':base(),'likes_only':base(followers=100000,median_views=999,median_likes=20),'too_small':base(followers=4999),'exact_half_zh':base(zh_share=.5),'missing_metrics':base(median_views=None,median_likes=None),'manual_promotion':base(promotion=True),'high_frequency':base(originals=451),'relative_floor_fail':base(followers=100000,median_views=900,median_likes=4)}
def filtering():
 r={name:evaluate(x)for name,x in CASES.items()};save('filtering.json',{'synthetic_only':True,'fixtures':CASES,'results':r,'counts':{s:sum(y['status']==s for y in r.values())for s in ['pass','reject','unknown']},'policy_note':'450为练习离散化上限，原文约450需人工裁量；中文用严格大于一半'})
def sensitivity():
 v=[100]*7+[10000];save('sensitivity.json',{'synthetic_views':v,'mean':statistics.mean(v),'median':statistics.median(v),'mean_threshold_pass':statistics.mean(v)>=300,'median_threshold_pass':statistics.median(v)>=300,'floor_sweep':{str(t):evaluate(base(),view_floor=t)['status']for t in [299,300,301]},'meaning':'只说明本合成样本及规则敏感性，不推断真人质量'})
def aging():
 rows=[{'days_since_snapshot':shift,'last_post_age':7+shift,'decision':evaluate(base(days=7+shift))['status']}for shift in [0,7,8,180]];save('aging.json',{'synthetic_only':True,'rows':rows,'original_claim':'半年约为作者复盘经验，不是经过生存分析证明的通用寿命','scheduled_tasks_created':0})
class Tests(unittest.TestCase):
 def test_boundary(self):self.assertEqual(evaluate(base())['status'],'pass')
 def test_like_or(self):self.assertEqual(evaluate(CASES['likes_only'])['status'],'pass')
 def test_both_fail(self):self.assertEqual(evaluate(CASES['relative_floor_fail'])['status'],'reject')
 def test_missing(self):self.assertEqual(evaluate(CASES['missing_metrics'])['status'],'unknown')
 def test_missing_one_other_pass(self):self.assertEqual(evaluate(base(median_likes=None))['status'],'pass')
 def test_half(self):self.assertEqual(evaluate(base(zh_share=.5))['status'],'reject')
 def test_older(self):self.assertEqual(evaluate(base(days=15))['status'],'reject')
 def test_high(self):self.assertEqual(evaluate(base(originals=451))['status'],'reject')
 def test_promotion(self):self.assertEqual(evaluate(base(promotion=True))['status'],'reject')
 def test_nan_not_zero(self):self.assertEqual(evaluate(base(median_views=float('nan'),median_likes=None))['status'],'unknown')
 def test_booleans_not_numbers(self):self.assertEqual(evaluate(base(followers=True))['status'],'unknown')
 def test_median_even(self):self.assertEqual(statistics.median([1,3,5,7]),4)
def test():unittest.main(argv=['filter_lab'],verbosity=2)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('step',choices=['manifest','audit','filtering','sensitivity','aging','test']);a=p.parse_args();globals()[a.step]()
