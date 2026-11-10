from pathlib import Path
import hashlib,json
p=Path('portfolio.html');s=p.read_text();r={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'external_src':s.count('src="http'),'svg':s.count('<svg'),'has_reduced_motion':'prefers-reduced-motion' in s,'has_viewport':'name="viewport"' in s};print(json.dumps(r,ensure_ascii=False,indent=2));assert r['external_src']==0 and r['svg']==1 and r['has_viewport'];Path('audit-result.json').write_text(json.dumps(r,indent=2))
