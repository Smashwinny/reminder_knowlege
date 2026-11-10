import sys,json,hashlib,importlib.util,xml.etree.ElementTree as ET
from pathlib import Path
P=Path(__file__).resolve().parent;B=P.parent;O=P/'out';O.mkdir(exist_ok=True)
def save(n,x): (O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2))
def init():
 items=[('1','AI开源编辑器更新','https://example.org/a'),('1','AI开源编辑器更新','https://example.org/a'),('2','AI开源资料 广告','https://example.org/b'),('3','AI摄影技巧','https://example.org/c'),('4','开源RSS更新','https://example.org/d'),('5','AI开源发布','https://example.org/e')]
 root=ET.Element('rss',version='2.0');ch=ET.SubElement(root,'channel');ET.SubElement(ch,'title').text='合成选题夹具，非实时新闻'
 for guid,title,url in items:
  el=ET.SubElement(ch,'item')
  for tag,v in [('guid',guid),('title',title),('link',url)]: ET.SubElement(el,tag).text=v
 ET.ElementTree(root).write(O/'fixture.xml',encoding='utf-8',xml_declaration=True)
 (O/'keywords.txt').write_text('[GLOBAL_FILTER]\n广告\n\n[WORD_GROUPS]\n+AI\n开源\n')
 print('created RSS fixture: 6 items (synthetic); 1 duplicate; no external feed or private data')
def collect():
 root=ET.parse(O/'fixture.xml');seen=set();out=[]
 for el in root.findall('./channel/item'):
  row={x.tag:x.text for x in el};key=row['guid']
  if key not in seen:seen.add(key);out.append(row)
 save('collected.json',out);assert len(out)==5
 print('parsed RSS 6 -> deduplicated 5 (GUID scope=single feed; duplicate titles not globally merged)')
def select():
 src=B/'upstream/TrendRadar/trendradar/core/frequency.py';spec=importlib.util.spec_from_file_location('frequency',src);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 groups,filters,globalf=m.load_frequency_words(str(O/'keywords.txt'));rows=json.loads((O/'collected.json').read_text());selected=[x for x in rows if m.matches_word_groups(x['title'],groups,filters,globalf)]
 save('selected.json',selected);assert [x['guid'] for x in selected]==['1','5']
 (O/'article.md').write_text('# AI开源观察（合成示例）\n\n> 仅作流程教学，不是实时新闻，也不证明热度。\n\n'+''.join('## '+x['title']+'\n\n来源：'+x['link']+'\n\n' for x in selected))
 print('real TrendRadar frequency.py: 5 -> 2; IDs=1,5; require AI AND 开源; global exclude 广告')
def audit():
 html=(O/'article-inline.html').read_text();assert '<script' not in html and 'style=' in html and '合成' in html
 route=(B/'upstream/RSSHub/lib/routes/github/issue.ts').read_text();assert '.filter((item) => item.pull_request === undefined)' in route
 save('manifest.json',{str(f.relative_to(B)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [O/'fixture.xml',O/'selected.json',O/'article-inline.html',B/'upstream/TrendRadar/trendradar/core/frequency.py',B/'upstream/md/packages/core/src/utils/markdownHelpers.ts',B/'upstream/RSSHub/lib/routes/github/issue.ts']})
 print('PASS local HTML 3 checks; RSSHub route static contract: PR entries excluded (not executed); SHA256 manifest saved')
if __name__=='__main__':globals()[sys.argv[1]]()
