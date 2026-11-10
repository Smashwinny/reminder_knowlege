import json,re,sys,hashlib
from pathlib import Path
from html.parser import HTMLParser
P=Path(__file__).parent;S=P.parent/'sources';stage=sys.argv[1]
if stage=='prepare':
 m=json.loads((P.parent/'source-manifest.json').read_text());rows=[x for x in m if x['file'].endswith('.html')];assert len(rows)==7;print([(x['file'],x.get('status'),x.get('bytes')) for x in rows]);(P/'pages.json').write_text(json.dumps(rows))
elif stage=='extract':
 rows=[]
 for p in S.glob('*.html'):
  ids=sorted(set(re.findall(r'(?:abs/|papers/)(\d{4}\.\d{4,5})(?:v\d+)?',p.read_text())))
  rows.extend({'source':p.name,'id':i} for i in ids)
 (P/'paper-links.json').write_text(json.dumps(rows));print('link observations=',len(rows),'unique papers=',len({x['id'] for x in rows}));assert rows
elif stage=='dedupe':
 canon=lambda s:re.search(r'\d{4}\.\d{4,5}',s).group()
 sample=['https://arxiv.org/abs/2611.12865v1','https://arxiv.org/abs/2611.12865v2','https://huggingface.co/papers/2611.12865'];keys=set(map(canon,sample));assert len(keys)==1;print('3 synthetic links =>',len(keys),'canonical paper; versions must also be recorded separately')
elif stage=='audit':
 rows=json.loads((P/'paper-links.json').read_text());print('sources_with_paper_ids=',sorted(set(x['source'] for x in rows)));print('HTTP 200 != paper reviewed; rankings != universal quality; no schedule created')
