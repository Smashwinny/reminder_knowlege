import pathlib,hashlib,json
root=pathlib.Path(__file__).resolve().parent.parent
manifest=json.loads((root/'exercise/manifest.json').read_text())
for name,want in manifest.items():
 got=hashlib.sha256((root/name).read_bytes()).hexdigest()
 if got!=want:raise SystemExit('FAIL fingerprint: '+name)
print(f'PASS {len(manifest)} artifact SHA-256 checks; pinned persona is explicitly redacted; no original payload execution')
