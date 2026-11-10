from pathlib import Path
import json,hashlib
r=Path(__file__).resolve().parent
m=json.loads((r/'vendor-manifest.json').read_text())
for p,h in m['files'].items():
 actual=hashlib.sha256((r/'vendor'/p).read_bytes()).hexdigest()
 assert actual==h,(p,actual)
 print('PASS 上游原样文件SHA256',p,actual)
print('仅校验随包副本与已记录哈希；不是远程签名认证。')
