from pathlib import Path
import struct,json,hashlib
rows=[]
for f in sorted(Path('upstream/kestrel-k1/assets').rglob('*.glb')):
 d=f.read_bytes();magic,version,total=struct.unpack_from('<III',d,0);assert magic==0x46546c67 and version==2 and total==len(d);n,t=struct.unpack_from('<II',d,12);assert t==0x4e4f534a;j=json.loads(d[20:20+n]);rows.append({'file':str(f),'bytes':len(d),'nodes':len(j.get('nodes',[])),'meshes':len(j.get('meshes',[])),'skins':len(j.get('skins',[])),'animations':len(j.get('animations',[])),'generator':j.get('asset',{}).get('generator'),'sha256':hashlib.sha256(d).hexdigest()})
out={'files':rows,'total_nodes':sum(r['nodes']for r in rows),'total_meshes':sum(r['meshes']for r in rows)};print(json.dumps(out,indent=2));Path('assets-result.json').write_text(json.dumps(out,indent=2));assert len(rows)==4 and all(r['skins']==0 and r['animations']==0 for r in rows)
