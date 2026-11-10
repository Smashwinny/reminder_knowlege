import json,struct,pathlib,hashlib
p=pathlib.Path(__file__).resolve().parents[1]/'sources/spider_turret.glb'
b=p.read_bytes(); magic,version,total=struct.unpack_from('<4sII',b)
assert magic==b'glTF' and version==2 and total==len(b)
n,t=struct.unpack_from('<II',b,12); d=json.loads(b[20:20+n]); names={x.get('name') for x in d.get('nodes',[])}
required=['RobotRoot','ChassisBase','TurretYawPivot','TurretPitchPivot']+[f'Leg{k}_{i}' for i in ['FL','FR','RL','RR'] for k in ['HipYaw','FemurPitch','TibiaPitch','AnklePitch','FootTip']]
missing=[x for x in required if x not in names];assert not missing,missing
r={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'generator':d['asset'].get('generator'),'nodes':len(d.get('nodes',[])),'meshes':len(d.get('meshes',[])),'skins':len(d.get('skins',[])),'animations':len(d.get('animations',[])),'required_nodes':len(required),'missing':missing}
pathlib.Path(__file__).with_name('asset-result.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
