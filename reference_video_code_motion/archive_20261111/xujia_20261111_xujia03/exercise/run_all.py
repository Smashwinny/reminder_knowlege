from pathlib import Path
import subprocess,datetime,json,time
p=Path(__file__).resolve().parent;log=['# 第3项真实实验日志','',datetime.datetime.now().astimezone().isoformat()+'（Asia/Shanghai）','教学代码为原创CPU三维投影/音频实验，不是作者源码或Opus输出，未执行onetake渲染脚本。','']
for i,mode in enumerate(['source_audit','timeline','audio','render','encode'],1):
 cmd=['python3','lab.py',mode];t=time.monotonic();a=subprocess.run(cmd,cwd=p,text=True,capture_output=True)
 log+=['## 步骤'+str(i)+' '+('已执行' if a.returncode==0 else '受阻'),'```bash','cd '+str(p),' '.join(cmd),'```','```text',a.stdout.strip(),a.stderr.strip(),'exit_code='+str(a.returncode),'elapsed_wall_seconds='+str(round(time.monotonic()-t,3)),'```',''];(p.parent/'experiment-log.md').write_text('\n'.join(log));print(mode,a.returncode,a.stdout.strip(),flush=True)
 if a.returncode:break
log+=['## 待验证','Opus 5.5/NotionAI输入参考视频→自动理解→索要素材→生成代码的作者工作流：没有调用，待验证。','Blender人物建模、Three.js/WebGL真实运行、上游onetake渲染、4K60性能和真人观感：均未实测。','作者原始工程、素材、提示及渲染日志未公开，不能声称独立复现或效果一致。','Chrome已按用户要求仅清理本任务残留，独立profile、--no-sandbox --disable-gpu、更长105s超时；结果另见qa/clean-chrome.stderr。未停止其他助手浏览器。'];(p.parent/'experiment-log.md').write_text('\n'.join(log))
