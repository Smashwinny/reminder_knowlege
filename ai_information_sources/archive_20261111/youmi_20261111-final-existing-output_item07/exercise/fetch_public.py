"""仅下载公开页面，无认证、订阅、表单或模型API调用。"""
from pathlib import Path
import urllib.request,concurrent.futures,json,hashlib,datetime
ROOT=Path(__file__).resolve().parents[1]
SOURCES=[('ai_news','https://news.smol.ai'),('the_batch','https://www.deeplearning.ai/the-batch/'),('hf_papers','https://huggingface.co/papers/date/2026-09-18'),('alphaxiv','https://www.alphaxiv.org/'),('arxiv_recent','https://arxiv.org/list/cs.AI/recent'),('arena_home','https://arena.ai/'),('aa_method','https://artificialanalysis.ai/methodology'),('arena_rank','https://arena.ai/blog/ranking-method'),('arena_factuality','https://arena.ai/blog/factuality-in-arena'),('arxiv_about','https://docs.arxiv.org/about/'),('paper_v7','https://arxiv.org/abs/1706.03762v7')]
def fetch(row):
 name,url=row;x={'name':name,'url':url,'access':datetime.datetime.now().astimezone().isoformat()}
 try:
  with urllib.request.urlopen(url,timeout=30)as h:b=h.read();x.update(status=h.status,final_url=h.url,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
  (ROOT/f'snapshots/{name}.html').write_bytes(b)
 except Exception as e:x.update(error=str(e))
 return x
if __name__=='__main__':
 (ROOT/'snapshots').mkdir(exist_ok=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=5)as e:rows=list(e.map(fetch,SOURCES))
 (ROOT/'source-manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(json.dumps(rows,ensure_ascii=False,indent=2))
