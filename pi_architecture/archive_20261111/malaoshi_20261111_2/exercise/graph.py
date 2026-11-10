# Source: https://github.com/earendil-works/pi ; full SHAs in snapshots/provenance.json
# Only production dependencies. Not a module-import graph or runtime security proof.
from pathlib import Path
import json,hashlib
S=Path(__file__).parent/'snapshots';prov=json.loads((S/'provenance.json').read_text()); report={}
for version,meta in prov.items():
 root=S/version
 for name,want in meta['files_sha256'].items():
  assert hashlib.sha256((root/name).read_bytes()).hexdigest()==want,name
 pkgs={p['name']:p for f in (root/'packages').glob('*/package.json') for p in [json.loads(f.read_text())]}
 edges={name:sorted(d for d in p.get('dependencies',{}) if d in pkgs) for name,p in pkgs.items()}
 name='@earendil-works/pi-coding-agent';seen=set();todo=[name]
 while todo:
  n=todo.pop()
  if n in seen:continue
  seen.add(n);todo.extend(edges[n])
 short=lambda xs:[x.removeprefix('@earendil-works/') for x in sorted(xs)]
 report[version]={'sha':meta['sha'],'workspaces':len(pkgs),'non_private':sum(not p.get('private',False) for p in pkgs.values()),'product':pkgs[name]['version'],'direct':short(edges[name]),'closure':short(seen)}
 if version in ['1.2.0','audit-1.5.2','main-1.5.2']:
  assert not set(['@earendil-works/chord','@earendil-works/pi-durable','@earendil-works/pi-env'])&seen
 if version=='1.2.0':assert len(pkgs)==11 and len(seen)==7
 if '1.5.2' in version:assert len(pkgs)==12 and len(seen)==8
 print(json.dumps(report[version],ensure_ascii=False))
assert report['audit-1.5.2']['direct']==report['main-1.5.2']['direct']
(Path(__file__).parent/'graph-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('PASS: 4 pinned snapshots; manifest hashes and production-closure assertions')
