from pathlib import Path
import json,hashlib
E=Path(__file__).parent;P=E/'lab/package/package.json'
p=json.loads(P.read_text());assert p['version']=='0.84.2'
assert p['name']=='@earendil-works/pi-coding-agent'
packed=(E/'lab/earendil-works-pi-coding-agent-0.84.2.tgz').read_bytes()
assert hashlib.sha1(packed).hexdigest()=='e4d4c1e769963c816959f5cea02a0a10ccc0495a'
r=json.loads((E/'graph-results.json').read_text());assert len(r)==4
print('PASS: tarball SHA1 e4d4c1e769963c816959f5cea02a0a10ccc0495a; 4 snapshots present')
print('LIMIT: no CLI session, provider, MCP interop, server privacy, or user machine tested')
