import pathlib,json,re,hashlib,urllib.request
p=pathlib.Path(__file__).resolve().parents[1]/'sources';mp=p/'skill-manifest.json';m=json.loads((mp if mp.exists() else pathlib.Path(__file__).parent/'source-manifest.json').read_text());out=[]
for a in m:
 f=p/a['name']/'SKILL.md';b=f.read_bytes() if f.exists() else urllib.request.urlopen('https://raw.githubusercontent.com/'+a['repo']+'/'+a['sha']+'/'+a['path'],timeout=30).read();t=b.decode();assert re.search(r'^name:\s*'+re.escape(a['name'])+r'\s*$',t,re.M);assert re.fullmatch('[0-9a-f]{40}',a['sha']);out.append({'name':a['name'],'sha':a['sha'],'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
r={'skills_verified':len(out),'all_current_path_reads':all(a['status']=='current' for a in m),'installed_skills':0,'model_calls':0,'files':out};(pathlib.Path(__file__).parent/'source-result.json').write_text(json.dumps(r,indent=2));print(json.dumps({k:v for k,v in r.items() if k!='files'}))
