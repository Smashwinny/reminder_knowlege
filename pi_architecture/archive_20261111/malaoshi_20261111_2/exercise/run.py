#!/usr/bin/env python3
"""Run only public package preparation + local component assertions. No models/keys.
Upstream code provenance: snapshots/provenance.json. License: snapshots/LICENSE-pi.
"""
from pathlib import Path
import subprocess,datetime,json,sys
E=Path(__file__).resolve().parent;L=E/'lab';L.mkdir(exist_ok=True)
log=['# Pi 架构：真实主实验日志','时间均为 Asia/Shanghai UTC+8。未启动 Pi 主 CLI，未调用模型；步骤 1 仅公共 npm 下载。']
steps=[('1 准备精确发布物',L,'node --version && npm --version && npm pack @earendil-works/pi-coding-agent@0.84.2 --ignore-scripts --json > pack.json && tar -xzf earendil-works-pi-coding-agent-0.84.2.tgz && node -e "const p=require(\'./package/package.json\'); console.log(p.name+\'@\'+p.version)"'),('2 发布物身份与旧功能边界',L,'node manifest.mjs'),('3 四快照生产依赖闭包',E,'python3 graph.py'),('4 真实开关函数十用例',L,'node switch.mjs'),('5 真实编译方法+mock请求五分支',L,'node ping-mock.mjs'),('6 输入完整性及范围复核',E,'python3 final-check.py')]
results=[]
for title,cwd,cmd in steps:
 now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
 p=subprocess.run(cmd,cwd=cwd,shell=True,executable='/bin/bash',text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 entry=f'## {title}\n\n时间：{now}（Asia/Shanghai）\n\n工作目录：`{cwd}`\n\n```bash\n{cmd}\n```\n\n真实输出：\n```text\n{p.stdout}\n```\n\n退出码：{p.returncode}\n'
 log.append(entry);print(entry);results.append({'step':title,'exit':p.returncode,'output':p.stdout})
 (E.parent/'experiment-log.md').write_text('\n'.join(log))
 (E/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
 if p.returncode:sys.exit(p.returncode)
print('ALL SIX STEPS COMPLETED; component tests only, not end-to-end.')
