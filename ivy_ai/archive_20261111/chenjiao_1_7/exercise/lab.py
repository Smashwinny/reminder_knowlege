from pathlib import Path
import sys,json,hashlib,platform
P=Path(__file__).parent
step=int(sys.argv[1])
def emit(**v):
 print(json.dumps(v,ensure_ascii=False,sort_keys=True))
 (P/f"result-{step}.json").write_text(json.dumps(v,ensure_ascii=False,indent=2))

# GPL上游arena原件主机测试 + 自写预算算术；无模型/设备。
if step==1:emit(python=platform.python_version(),scope='真实上游C arena测试 + 教学内存预算')
if step==2:
 import subprocess
 cmd=['gcc','-std=c11','-Wall','-Wextra','-Iupstream/components/story_core/include','-Iupstream/host','-Iupstream/host/stubs','upstream/host/test_arena.c','upstream/components/story_core/story_arena.c','-o','test_arena']
 r=subprocess.run(cmd,cwd=P,text=True,capture_output=True);print(r.stdout+r.stderr);assert r.returncode==0
 emit(command=cmd,compile_exit=r.returncode)
if step==3:
 import subprocess
 r=subprocess.run(['./test_arena'],cwd=P,text=True,capture_output=True);print(r.stdout+r.stderr);assert r.returncode==0 and 'test_arena OK' in r.stdout
 emit(exit_code=r.returncode,upstream_test='test_arena OK',not_tested=['模型推理','ESP-IDF固件','麦克风','PSRAM时序'])
if step==4:
 sizes={'STT':5.4,'LLM':6.5,'TTS':2.5};simultaneous=sum(sizes.values());peak=max(sizes.values());assert simultaneous>8 and peak<=7
 emit(illustrative_MB=sizes,simultaneous_MB=simultaneous,sequential_peak_MB=peak,arena_MB=7,headroom_MB=round(7-peak,1),warning='十进制教学近似；不含全部系统常驻内存，非ESP32测量')
