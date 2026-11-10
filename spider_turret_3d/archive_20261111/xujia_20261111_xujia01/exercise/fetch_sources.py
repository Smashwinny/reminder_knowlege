"""Download immutable public files only. No git checkout, credentials or execution."""
import pathlib,urllib.request,hashlib
SHA='e5f92a8b99f2cbeef6a87ad12c142b0ccf34a99b'
e=pathlib.Path(__file__).resolve().parent
base='https://raw.githubusercontent.com/thebuggeddev/spider-turret/'+SHA+'/'
for name in ['AnimationStateMachine.js','TurretController.js','LegIKSolver.js','QuadrupedGaitController.js','tslMaterials.js']:
 p=e/'upstream'/name;p.parent.mkdir(exist_ok=True);p.write_bytes(urllib.request.urlopen(base+'src/spider/'+name).read());print(name,hashlib.sha256(p.read_bytes()).hexdigest())
(e/'upstream/package.json').write_text('{"type":"module"}')
p=e.parent/'sources/spider_turret.glb';p.parent.mkdir(exist_ok=True);p.write_bytes(urllib.request.urlopen(base+'spider_turret.glb').read())
assert hashlib.sha256(p.read_bytes()).hexdigest()=='b3c28c34e609e430911207a9aaf3b2adef47b2893017503f01176482d833d22f'
print('GLB SHA256 verified')
