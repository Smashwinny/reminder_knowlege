from pathlib import Path
import urllib.request,json,concurrent.futures,hashlib
SHA='286d56ccbbb924c10812fc5e6cabb11906454afc'
paths=['README.md','LICENSE','kestrel-k1/README.md','kestrel-k1/index.html','kestrel-k1/assets/index-BWjJCO7Y.js','kestrel-k1/assets/index-CqPE8GzT.css','kestrel-k1/assets/body/head.glb','kestrel-k1/assets/body/limbs.glb','kestrel-k1/assets/body/torso.glb','kestrel-k1/assets/shells.glb','kestrel-k1/assets/ibm-plex-mono-latin-400-normal-DMJ8VG8y.woff2','kestrel-k1/assets/ibm-plex-mono-latin-500-normal-DSY6xOcd.woff2','kestrel-k1/assets/ibm-plex-mono-latin-ext-400-normal-BmRBH3aV.woff2','kestrel-k1/assets/ibm-plex-mono-latin-ext-500-normal-CAhNIIs5.woff2','kestrel-k1/assets/inter-tight-latin-400-normal-iW8qmuJY.woff2','kestrel-k1/assets/inter-tight-latin-600-normal-BgSTtRxb.woff2','kestrel-k1/assets/inter-tight-latin-ext-400-normal-DN7wyBvd.woff2','kestrel-k1/assets/inter-tight-latin-ext-600-normal-BgMgWFts.woff2']
def get(path):
 f=Path('upstream')/path;f.parent.mkdir(parents=True,exist_ok=True);d=urllib.request.urlopen(f'https://raw.githubusercontent.com/thtbee/waggles/{SHA}/{path}',timeout=30).read();f.write_bytes(d);return {'path':path,'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()}
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=5)as ex:r=list(ex.map(get,paths))
 Path('download-manifest.json').write_text(json.dumps(r,indent=2));expected=Path('expected-manifest.json');assert not expected.exists() or json.loads(expected.read_text())==r, 'fixed input mismatch';print(json.dumps({'commit':SHA,'files':len(r),'bytes':sum(x['bytes']for x in r)},indent=2))
