"""仅在解压包根的tools/准备固定工具，不改系统配置；下载URL与哈希显式锁定。"""
from pathlib import Path
import hashlib,subprocess,tarfile,json
B=Path(__file__).resolve().parents[1];T=B/'tools';T.mkdir(exist_ok=True)
java_name='OpenJDK21U-jre_x64_linux_hotspot_21.0.13_9.tar.gz'
assets=[(java_name,'https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.13%2B9/'+java_name,'a535a1df9c6284d9618872984e026ae0352d1f7e9e0605425c0e6114f47351dd'),('tla2tools.jar','https://github.com/tlaplus/tlaplus/releases/download/v1.7.4/tla2tools.jar','936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88')]
for name,url,want in assets:
 p=T/name
 if not p.exists():subprocess.run(['curl','--fail','--location','--max-time','180','--output',str(p),url],check=True)
 actual=hashlib.sha256(p.read_bytes()).hexdigest();assert actual==want,(p,actual);print('SHA256匹配',name,actual)
jar=T/'tla2tools.jar';assert hashlib.sha1(jar.read_bytes()).hexdigest()=='bee4a54f3ee3d4afc347c3240ec2d9e93b075104';print('TLC release发布正文SHA1也匹配；SHA1不是签名认证。')
java=T/'jdk-21.0.13+9-jre/bin/java'
if not java.exists():
 with tarfile.open(T/java_name) as f:f.extractall(T,filter='data')
print('Java只在',java);subprocess.run([str(java),'-version'],check=True)
