# Sources + exact commit coordinates: provenance.json / repositories.json
from pathlib import Path
import json,hashlib
E=Path(__file__).parent;p=json.loads((E/'provenance.json').read_text())
for name,m in p.items():assert hashlib.sha256((E/name).read_bytes()).hexdigest()==m['sha256'],name
r=json.loads((E/'repositories.json').read_text());assert len(r)==5
for x in r:print(x['repo'],x['sha'],x['package']+'@'+x['version'])
print('PASS: 5 repository identities; '+str(len(p))+' unmodified upstream files hash-verified')
