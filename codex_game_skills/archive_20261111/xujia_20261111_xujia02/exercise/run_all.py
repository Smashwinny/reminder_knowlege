from pathlib import Path
import subprocess,datetime,json,re,os,signal
p=Path(__file__).resolve().parent;root=p.parent;qa=root/'qa';qa.mkdir(exist_ok=True)
log=['# 五步真实实验日志','',datetime.datetime.now().astimezone().isoformat()+'（Asia/Shanghai）','原创JS教学实现，不是Codex/引擎/平台端到端成功。此前Chrome无头启动分别45s、30s、25s超时；PDF命令也未生成文件。','']
cmds=[['python3','source_audit.py'],['node','lab.mjs','contracts'],['node','lab.mjs','ui'],['node','lab.mjs','feel'],['python3','build_demo.py']]
for i,c in enumerate(cmds):
 a=subprocess.run(c,cwd=p,text=True,capture_output=True);assert a.returncode==0,a.stderr
 log+=['## 步骤'+str(i+1)+' 已执行'+('（仅页面生成；浏览器执行见下）' if i==4 else ''),'工作目录：解压后的item02/exercise','```bash',' '.join(c),'```','真实输出：','```text',a.stdout.strip(),a.stderr.strip(),'exit_code='+str(a.returncode),'```','']
 (root/'experiment-log.md').write_text('\n'.join(log))
chrome=['google-chrome','--headless','--disable-extensions','--no-first-run','--disable-gpu','--disable-dev-shm-usage','--user-data-dir='+str(qa/'final-demo-profile'),'--window-size=1100,800','--screenshot='+str(qa/'demo.png'),'--dump-dom',(p/'demo.html').as_uri()+'?test=1']
log+=['## 步骤5浏览器部分：运行待验证','```bash',' '.join(chrome),'```'];out=qa/'browser-dom.html';err=qa/'browser-stderr.txt'
with out.open('w') as fo,err.open('w') as fe:
 proc=subprocess.Popen(chrome,cwd=p,stdout=fo,stderr=fe,start_new_session=True)
 try:rc=proc.wait(timeout=15)
 except subprocess.TimeoutExpired:
  os.killpg(proc.pid,signal.SIGKILL);proc.wait();rc=124
try:
 match=re.search(r'<pre id="result">(.*?)</pre>',out.read_text(),re.S);d=json.loads(match.group(1)) if match else None
except Exception:d=None
if rc==0 and d and d.get('browser_checks')==4:
 log+=['真实结果：',json.dumps(d,ensure_ascii=False),'exit_code=0'];(p/'browser-result.json').write_text(json.dumps(d,indent=2))
else:
 log+=['结果：exit_code='+str(rc)+'；timeout=15秒；没有取得有效自测DOM或截图，浏览器部分受阻/待验证。','不得将build_demo成功当成网页运行成功；源代码内自测的预期结果不是实测。'];d={'status':'受阻','exit_code':rc,'verified_browser_checks':0};(p/'browser-result.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
log+=['','## 待验证','Codex宿主8技能加载、Unity/Unreal/Godot适配、Three.js/移动/手柄、真人试玩与Higgsfield生成部署均未执行。','没有账号、密钥、付费模型、外发或公开部署；没有FPS/提效百分比结论。','主实验步骤1—4本地真实通过；步骤5文件生成通过，Chrome执行失败。','PDF：无头Chrome未生成guide.pdf，标未渲染；没有PDF逐页图像，不能声称视觉验收通过。','参考排查：官方https://developer.chrome.com/docs/chromium/headless确认headless用法；一次公开网页检索及X检索未找到可直接验证的安全修复。未修改代理/系统安全配置/其他助手会话。']
(root/'experiment-log.md').write_text('\n'.join(log));print(json.dumps({'node_python_steps':4,'html_generated':True,'browser':d},ensure_ascii=False))
