"""真实公开快照处理＋明确合成的排名/成本计算。不是模型测评、推荐排行或定时器。"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,urljoin
import json,re,hashlib,math,unittest,argparse
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results'
CHANNELS={'ai_news':'聚合发现','the_batch':'编辑解读','hf_papers':'社区发现','alphaxiv':'研究发现与讨论','arxiv_recent':'原始论文','arena_home':'偏好评测入口','aa_method':'性能/价格方法'}
def emit(n,x):
 OUT.mkdir(exist_ok=True);(OUT/(n+'.json')).write_text(json.dumps(x,ensure_ascii=False,indent=2));print(json.dumps(x,ensure_ascii=False,indent=2))
def canonical(url):
 p=urlparse(url)
 if p.hostname not in ['arxiv.org','www.arxiv.org','huggingface.co','alphaxiv.org','www.alphaxiv.org']:return None
 m=re.search(r'/(?:abs|pdf|html|papers)/(\d{4}\.\d{4,5})(v\d+)?(?:\.pdf)?(?:/|$)',p.path)
 return None if not m else {'family':m[1],'version':m[2]or None,'canonical':'https://arxiv.org/abs/'+m[1]+(m[2]or'')}
class Links(HTMLParser):
 def __init__(self):super().__init__();self.hrefs=[]
 def handle_starttag(self,t,a):
  if t=='a':self.hrefs +=[v for k,v in a if k=='href'and v]
def catalog():
 rows=json.loads((ROOT/'source-manifest.json').read_text());x={'channels':CHANNELS,'raw_http_success':sum(r.get('status')==200 for r in rows),'raw_http_failures':sum('error'in r for r in rows),'webfetch_read_excerpts':sum('webfetch_read'in r for r in rows),'original_post_sha256':hashlib.sha256((ROOT/'source-post.json').read_bytes()).hexdigest(),'note':'主7渠道都经WebFetch实读；原始HTTP失败保留，与成功WebFetch不能混报'};emit('catalog',x)
def dedupe():
 r={}
 for name,base in [('hf_papers','https://huggingface.co'),('arxiv_recent','https://arxiv.org'),('paper_v7','https://arxiv.org')]:
  p=Links();p.feed((ROOT/f'snapshots/{name}.html').read_text());found=[v for href in p.hrefs if(v:=canonical(urljoin(base,href)))];r[name]={'href_id_occurrences':len(found),'unique_family_count':len(set(x['family']for x in found)),'unique_families':sorted(set(x['family']for x in found))}
 urls=['https://arxiv.org/abs/1706.03762v7?utm_source=test','https://arxiv.org/pdf/1706.03762v6.pdf','https://huggingface.co/papers/1706.03762','https://www.alphaxiv.org/abs/1706.03762'];mapped=[canonical(u)for u in urls];emit('dedupe',{'real_anchor_extraction':r,'synthetic_alias_examples':mapped,'example_family_count':len(set(x['family']for x in mapped)),'example_version_key_count':len(set((x['family'],x['version'])for x in mapped)),'warning':'链接中论文ID出现/去重不代表全文已读、当日主榜成员或新论文唯一数量'})
def evidence():
 a=(ROOT/'snapshots/arxiv_about.txt').read_text();b=(ROOT/'snapshots/aa_method.txt').read_text();r=[{'claim':'arXiv本身不做同行评审','file':'snapshots/arxiv_about.txt','needle':'not peer-reviewed','matched':'not peer-reviewed'in a},{'claim':'当前AA混合价格按cache/input/output=7:2:1','file':'snapshots/aa_method.txt','needle':'7:2:1','matched':'7:2:1'in b},{'claim':'AA输出速率口径包含首token等待','file':'snapshots/aa_method.txt','needle':'includes time to first token','matched':'includes time to first token'in b}];emit('evidence',{'ledger':r,'scope':'只是已读方法文档的可定位文本证据；不验证榜单/论文结论/真实模型表现'})
def rank_spreads(intervals):
 if any(lo>hi for lo,hi in intervals.values()):raise ValueError('invalid CI')
 return {n:[1+sum(lo2>hi for k,(lo2,hi2)in intervals.items()if k!=n),1+sum(hi2>lo for k,(lo2,hi2)in intervals.items()if k!=n)]for n,(lo,hi)in intervals.items()}
def ranks():
 ci={'A':(100,120),'B':(105,125),'C':(70,90)};emit('ranks',{'synthetic_only':True,'intervals':ci,'rank_spreads':rank_spreads(ci),'note':'套用官方排名区间端点公式，不估计Arena原始分数/置信区间或显著性'})
def task_cost(tokens,prices):
 if any(x is None for x in tokens+prices):return None
 if any(isinstance(x,bool)or not isinstance(x,(int,float))or not math.isfinite(x)or x<0 for x in tokens+prices):raise ValueError('nonnegative finite values')
 return sum(n*p for n,p in zip(tokens,prices,strict=True))/1e6
def cost():
 prices=[.2,1.,4.];small=task_cost([700,200,100],prices);large=task_cost([700,200,1000],prices);emit('cost',{'synthetic_only':True,'order':['cached','uncached_input','output'],'USD_per_million':prices,'tokens_small':[700,200,100],'cost_small_USD':small,'tokens_large':[700,200,1000],'cost_large_USD':large,'missing_price':task_cost([700,200,100],[None,1,4]),'warning':'自选虚构价格与token，不是任何真实供应商报价或AA复测；缓存token只算一次'})
class Tests(unittest.TestCase):
 def test_channel_count(self):self.assertEqual(len(CHANNELS),7)
 def test_version(self):self.assertEqual(canonical('https://arxiv.org/pdf/1706.03762v7.pdf')['version'],'v7')
 def test_alias(self):self.assertEqual(canonical('https://huggingface.co/papers/1706.03762')['family'],'1706.03762')
 def test_unknown_host(self):self.assertIsNone(canonical('https://example.com/abs/1706.03762'))
 def test_unrelated_path(self):self.assertIsNone(canonical('https://arxiv.org/about'))
 def test_rank_a(self):self.assertEqual(rank_spreads({'A':(100,120),'B':(105,125),'C':(70,90)})['A'],[1,2])
 def test_rank_c(self):self.assertEqual(rank_spreads({'A':(100,120),'B':(105,125),'C':(70,90)})['C'],[3,3])
 def test_bad_interval(self):
  with self.assertRaises(ValueError):rank_spreads({'A':(2,1)})
 def test_cost_unit(self):self.assertAlmostEqual(task_cost([700,200,100],[.2,1,4]),.00074)
 def test_missing(self):self.assertIsNone(task_cost([700,200,100],[None,1,4]))
 def test_no_nan(self):
  with self.assertRaises(ValueError):task_cost([1,1,1],[math.nan,1,1])
 def test_long_output(self):self.assertGreater(task_cost([700,200,1000],[.2,1,4]),task_cost([700,200,100],[.2,1,4]))
def test():unittest.main(argv=['source_flow'],verbosity=2)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('step',choices=['catalog','dedupe','evidence','ranks','cost','test']);a=p.parse_args();globals()[a.step]()
