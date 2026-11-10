from pathlib import Path
import sys,json,hashlib,platform
P=Path(__file__).parent
step=int(sys.argv[1])
def emit(**v):
 print(json.dumps(v,ensure_ascii=False,sort_keys=True))
 (P/f"result-{step}.json").write_text(json.dumps(v,ensure_ascii=False,indent=2))

# 自写板型清单审计，读取真实固定SHA的树；不下载/烧录固件。
if step==1:emit(python=platform.python_version(),scope='固件板目录审计与合成规格契约')
if step==2:
 tree=json.loads((P/'xiaozhi-tree.json').read_text());paths=[t['path'] for t in tree['tree'] if t['type']=='blob' and t['path'].startswith('main/boards/')]
 dirs=sorted({p.rsplit('/',1)[0] for p in paths});matches=[p for p in paths if any(k in p.lower() for k in ['lichuang','szpi','1.75','1_75'])]
 assert paths
 emit(board_files=len(paths),leaf_directories=len(dirs),matching_paths=matches[:20],sha=(P/'xiaozhi-sha.txt').read_text())
if step==3:
 import re
 def parse(s):
  m=re.fullmatch(r'N(\d+)R(\d+)',s)
  return {'flash_MiB':int(m[1]),'psram_MiB':int(m[2])} if m else None
 out={s:parse(s) for s in ['N16R8','N8R2','ESP32-S3']};assert out['N16R8']=={'flash_MiB':16,'psram_MiB':8};assert out['ESP32-S3'] is None
 emit(illustrative_suffix_parser=out,warning='商品缩写不证明真实容量，更不证明引脚兼容')
if step==4:
 support={'board-voice-demo':{'chip':'esp32s3','flash':16,'psram':8,'codec':'ES8311'}}
 fixtures=[{'chip':'esp32s3','flash':16,'psram':8,'codec':'ES8311'},{'chip':'esp32s3','flash':16,'psram':8,'codec':'other'}]
 ok=[x==support['board-voice-demo'] for x in fixtures];assert ok==[True,False]
 emit(synthetic_manifest_accepts=ok,conclusion='同芯片同容量但codec不同仍拒绝；清单不在场则未知')
