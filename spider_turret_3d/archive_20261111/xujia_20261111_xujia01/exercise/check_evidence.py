from pathlib import Path
import json, hashlib
p=Path(__file__).resolve().parent
m=json.loads((p/'manifest.json').read_text())
for name, expected in m.items():
    actual=hashlib.sha256((p/name).read_bytes()).hexdigest()
    assert actual==expected, name
    print('PASS',name)
print('EVIDENCE_OK',len(m),'files; VIDEO_NOT_RUN; ARTICLE_BODY_MISSING')
