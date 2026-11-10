import json,hashlib
from pathlib import Path
rows=json.loads(Path('source-manifest.json').read_text());out={'source_entries':len(rows),'read_ok':sum(r['status']=='read' for r in rows),'unique_repos':len(set(r['repo'] for r in rows)),'pinned':all(len(r.get('sha',''))==40 for r in rows),'core_sha256':hashlib.sha256(Path('core.js').read_bytes()).hexdigest()};print(json.dumps(out,indent=2));assert out['read_ok']==11 and out['pinned'];Path('audit-result.json').write_text(json.dumps(out,indent=2))
