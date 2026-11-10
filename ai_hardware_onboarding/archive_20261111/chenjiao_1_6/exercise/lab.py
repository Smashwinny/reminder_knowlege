from pathlib import Path
import sys,json,hashlib,platform
P=Path(__file__).parent
step=int(sys.argv[1])
def emit(**v):
 print(json.dumps(v,ensure_ascii=False,sort_keys=True))
 (P/f"result-{step}.json").write_text(json.dumps(v,ensure_ascii=False,indent=2))

# 自写合成固件文件校验，绝不接串口或读取用户备份。
if step==1:emit(python=platform.python_version(),scope='合成4096字节镜像；不是实际ESP32固件')
if step==2:
 data=bytes(range(256))*16;(P/'demo-firmware.bin').write_bytes(data);(P/'backup.bin').write_bytes(data);h=hashlib.sha256(data).hexdigest();(P/'expected.sha256').write_text(h)
 emit(bytes=len(data),sha256=h,backup_equal=(P/'backup.bin').read_bytes()==data)
if step==3:
 data=bytearray((P/'demo-firmware.bin').read_bytes());data[100]^=1;(P/'changed.bin').write_bytes(data);h=hashlib.sha256(data).hexdigest();expected=(P/'expected.sha256').read_text();assert h!=expected
 emit(corrupt_sha256=h,expected_sha256=expected,gate='REJECT',changed_bytes=1)
if step==4:
 # 复制回候选文件，不覆盖备份。
 (P/'restored.bin').write_bytes((P/'backup.bin').read_bytes());h=hashlib.sha256((P/'restored.bin').read_bytes()).hexdigest();assert h==(P/'expected.sha256').read_text()
 emit(restored_sha256=h,restored=True,physical_flash='未执行',note='校验值证明一致性，不证明来源真实性/设备可启动')
