#!/usr/bin/env python3
# Self-written orchestration. Upstream coordinates/license: provenance.json / upstream/*/LICENSE.
from pathlib import Path
import subprocess,datetime,json,sys
E=Path(__file__).resolve().parent;prefix='node --import ./network-guard.mjs '
steps=[('1 固定身份与文件指纹','python3 identity.py'),('2 四桶 Token 计费',prefix+'buckets.mjs'),('3 长上下文边界与聚合反例',prefix+'threshold.mjs'),('4 币种倍率与未知价格',prefix+'currency.mjs'),('5 回退快照格式与拒绝分支',prefix+'--experimental-transform-types rewind-format.mjs'),('6 审查模型发送授权门',prefix+'approval.mjs')]
log=['# 真实实验日志：DSH 实用插件挑选','2026-11-11，全部时间 Asia/Shanghai UTC+8。自写夹具直接调用固定上游实现；不是上游全测试套件，也不是独立审核。下载源码为准备阶段，以下六步离线执行，不安装依赖或宿主。'];results=[]
for title,cmd in steps:
 t=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat();p=subprocess.run(cmd,shell=True,executable='/bin/bash',cwd=E,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 part=f'## {title}\n\n时间：{t}（Asia/Shanghai UTC+8）\n工作目录：`{E}`\n\n```bash\n{cmd}\n```\n\n真实输出：\n```text\n{p.stdout}\n```\n退出码：{p.returncode}\n'
 log.append(part);print(part);results.append({'step':title,'command':cmd,'output':p.stdout,'exit':p.returncode});(E.parent/'experiment-log.md').write_text('\n'.join(log));(E/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
 if p.returncode:sys.exit(p.returncode)
print('ALL SIX LOCAL COMPONENT STEPS COMPLETED. No paid model/real DSH session used.')
