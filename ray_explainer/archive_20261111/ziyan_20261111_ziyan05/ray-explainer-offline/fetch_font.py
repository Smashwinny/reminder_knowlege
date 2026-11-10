"""Optional public pinned font fetch. No credentials, no model or API calls."""
from pathlib import Path
import hashlib, urllib.request
url='https://raw.githubusercontent.com/imraywang/rayskills/ca254f09a17e2e2c0aba7651c36688c322b1f2b2/skills/ray-explainer/assets/huashu/lib/fonts/NotoSansSC-700.woff'
expected='dd0d39a9780eb995c499af0c20cca93b1dfdda865da70871a20890b3e406b968'
p=Path(__file__).resolve().parent/'upstream/assets/huashu/lib/fonts/NotoSansSC-700.woff'
if p.exists():
    assert hashlib.sha256(p.read_bytes()).hexdigest()==expected, 'existing font differs; not overwritten'
    print('font already verified')
else:
    data=urllib.request.urlopen(url,timeout=60).read()
    assert hashlib.sha256(data).hexdigest()==expected,'font hash mismatch'
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    print('font saved, SHA256',expected)
