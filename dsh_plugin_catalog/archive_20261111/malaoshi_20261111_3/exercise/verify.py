from pathlib import Path
import hashlib,json
r=Path(__file__).resolve().parent.parent
j=json.loads((r/'exercise/manifest.json').read_text())
for p,h in j.items():assert hashlib.sha256((r/p).read_bytes()).hexdigest()==h,p
print(f'PASS {len(j)} SHA-256 source/input fingerprints; no registry/model/SSH connection')
