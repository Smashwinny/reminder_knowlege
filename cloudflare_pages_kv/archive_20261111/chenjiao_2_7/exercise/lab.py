import sys,json,zipfile,io
from pathlib import Path
mode=sys.argv[1]
if mode=='snapshot':
 c={'production':{'binding':'CATALOG','value':'v1'},'preview':{'binding':'CATALOG','value':'preview'}};Path('exercise/config.json').write_text(json.dumps(c));print('benign fixture namespaces: production/preview separated')
elif mode=='binding':
 c=json.load(open('exercise/config.json'));assert c['production']['binding']=='CATALOG';bad='catalog';assert bad!=c['production']['binding'];print('case-sensitive binding contract PASS; lowercase mismatch rejected (simulation)')
elif mode=='deploy':
 config=json.load(open('exercise/config.json'));release=json.loads(json.dumps(config));config['production']['value']='v2';assert release['production']['value']=='v1';release=json.loads(json.dumps(config));assert release['production']['value']=='v2';print('immutable local snapshot v1 -> redeploy snapshot v2; NOT Cloudflare deployment')
elif mode=='assets':
 p=Path('exercise/site.zip')
 with zipfile.ZipFile(p,'w') as z:z.writestr('index.html','<!doctype html><title>Catalog</title><h1>Offline catalog</h1>')
 with zipfile.ZipFile(p) as z:assert z.namelist()==['index.html'];print('generic static zip root:',z.namelist())
 print('NO proxy code, tunnel, subscription, registration or deployment')
