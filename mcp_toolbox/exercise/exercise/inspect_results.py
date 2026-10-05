#!/usr/bin/env python3
"""Print and assert selected actual MCP evidence; never simulates Toolbox."""
import json, sys
from pathlib import Path

groups={
 'discovery': ['prebuilt toolset exposes','SQLite native URI','prebuilt table discovery','prebuilt SELECT'],
 'boundary': ['native read-only rejects','read still works','readonly main database byte hash'],
 'binding': ['custom manifest exposes','parameterized lookup','SQL-looking parameter','wrong parameter type','unconfigured tool call'],
 'control': ['negative control advertises','hint alone','negative control write really','SQLite readOnly field','final readonly database']
}
if len(sys.argv)!=3 or sys.argv[2] not in groups:
    sys.exit('Usage: python3 inspect_results.py EVIDENCE_DIR discovery|boundary|binding|control')
data=json.loads((Path(sys.argv[1])/'results.json').read_text())
assert data['status']=='passed'
selected=[x for x in data['checks'] if any(x['name'].startswith(p) for p in groups[sys.argv[2]])]
assert selected and all(x['passed'] for x in selected)
print('GROUP:',sys.argv[2])
for check in selected:
    print('PASS:', check['name'])
    if check['detail'] is not None:
        print(json.dumps(check['detail'],ensure_ascii=False,indent=2))
print('SELECTED:',len(selected),'passed; COMPLETE RUN:',data['passed_checks'],'/',data['total_checks'])
if sys.argv[2]=='control':
    print('LIMITS:')
    print('\n'.join(data['limitations']))
