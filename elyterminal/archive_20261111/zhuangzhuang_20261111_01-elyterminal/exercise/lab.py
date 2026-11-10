#!/usr/bin/env python3
"""自编驱动；PTY 内运行未改动上游 bash 集成；对比度为合成模型。"""
import argparse,os,pathlib,pty,subprocess,select,time,re,json,sys,hashlib,math
ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
def baseline():
    import platform
    print('系统:',platform.platform());print('Python:',platform.python_version())
    for cmd in [['bash','--version'],['rustc','--version'],['cargo','--version']]:
        p=subprocess.run(cmd,capture_output=True,text=True); print(p.stdout.splitlines()[0])
    for n in ['marks.rs','elyterminal.bash']:
        p=ROOT/'vendor'/n;print(n,'sha256',hashlib.sha256(p.read_bytes()).hexdigest())
    upstream=ROOT.parent/'upstream'
    if upstream.exists():
        for src,dst in [('src/term/marks.rs','marks.rs'),('assets/shell-integration/bash/elyterminal.bash','elyterminal.bash')]:
            assert (upstream/src).read_bytes()==(ROOT/'vendor'/dst).read_bytes()
        print('2 个上游副本字节一致：PASS')
    p=subprocess.run(['bash','-n',str(ROOT/'vendor/elyterminal.bash')]);assert p.returncode==0
    print('上游 Bash 语法检查：PASS')
def shell():
    home=OUT/'isolated-home';home.mkdir(exist_ok=True)
    # 只让上游读取这个空白自建 rc；不读取账户的 ~/.bashrc。
    (home/'.bashrc').write_text("PS1='LAB> '\nbind 'set enable-bracketed-paste off'\n")
    env={'PATH':'/usr/bin:/bin','HOME':str(home),'TERM':'xterm-256color','LC_ALL':'C.UTF-8','HISTFILE':'/dev/null'}
    master,slave=pty.openpty()
    proc=subprocess.Popen(['/bin/bash','--noprofile','--rcfile',str(ROOT/'vendor/elyterminal.bash'),'-i'],stdin=slave,stdout=slave,stderr=slave,env=env,cwd=OUT,start_new_session=True)
    os.close(slave);whole=bytearray()
    def read_prompt(timeout=5):
        buf=bytearray();deadline=time.monotonic()+timeout
        while time.monotonic()<deadline:
            ready,_,_=select.select([master],[],[],0.1)
            if ready:
                try:b=os.read(master,65536)
                except OSError:break
                if not b:break
                buf.extend(b)
                if b']133;B' in buf:break
        whole.extend(buf)
        if b']133;B' not in buf:raise RuntimeError('未收到完整输入标记，不能宣称通过')
        return bytes(buf)
    chunks=[]
    try:
        read_prompt()
        cases=[('成功命令',b"echo REAL_OK\n",b']133;D;0'),('失败命令',b'false\n',b']133;D;1'),('切换目录',b"mkdir -p 'space % dir'; cd 'space % dir'\n",b'/space %25 dir'),('光标编辑',b"printf 'EDIT_OKX'"+b'\x1b[D'+b'\x1b[D'+b'\x04'+b'\n',b'EDIT_OK')]
        for name,data,expected in cases:
            os.write(master,data);buf=read_prompt();assert expected in buf,(name,repr(buf));chunks.append({'name':name,'input_hex':data.hex(),'output_repr':repr(buf),'expected_repr':repr(expected),'pass':True}); print(name,'PASS',repr(expected))
        # 光标编辑只验证 Bash readline 接受箭头，不是 ELY 的点击 hit-test。
        assert b'EDIT_OKX\r\n' not in buf
        print('光标编辑边界：只证实 readline 接收方向键；未执行 ELY 鼠标定位')
        os.write(master,b'exit\n');proc.wait(timeout=5)
    finally:
        if proc.poll() is None:proc.terminate();proc.wait(timeout=5)
        os.close(master)
        (OUT/'pty.raw').write_bytes(whole)
        (OUT/'pty-readable.txt').write_text(repr(bytes(whole)))
    bodies=[m.decode() for m in re.findall(rb'\x1b\]133;([^\x07]*)\x07',whole)]
    (OUT/'bodies.txt').write_text('\n'.join(bodies)+'\n');(OUT/'shell-results.json').write_text(json.dumps(chunks,ensure_ascii=False,indent=2))
    print('捕获 OSC 133 标记数量:',len(bodies));print('捕获字节数:',len(whole)); print('完整二进制:',OUT/'pty.raw')
def contrast():
    def lum(rgb):
        c=[x/255 for x in rgb];c=[x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4 for x in c]
        return sum(x*w for x,w in zip(c,[.2126,.7152,.0722]))
    def cr(a,b):
        x,y=sorted([lum(a),lum(b)]);return (y+.05)/(x+.05)
    def mix(f,b,a):return tuple(a*x+(1-a)*y for x,y in zip(f,b))
    assert abs(cr((0,0,0),(255,255,255))-21)<1e-12
    assert abs(cr((128,128,128),(128,128,128))-1)<1e-12
    # 任意教学色板，不是 Ely 源码色值，也不是 macOS 合成器的测量。
    base=(245,247,255); indicator=(49,87,246);border=(20,30,80)
    rows=[];parts=[]
    for wallpaper in [(255,255,255),(30,35,55),(255,140,30)]:
        for alpha in [1,.6,.25]:
            bg=mix(base,wallpaper,alpha);selected=mix(indicator,bg,.18)
            ratio=cr(selected,bg);edge=cr(border,bg)
            row={'wallpaper':wallpaper,'opacity':alpha,'row_fill_contrast':ratio,'solid_edge_contrast':edge};rows.append(row)
            print(f'壁纸={wallpaper} 不透明度={alpha:.2f} 淡填充={ratio:.6f}:1 实线边={edge:.6f}:1')
            rgb=lambda c:','.join(f'{x:.3f}' for x in c)
            parts.append(f'<div style="background:rgb({rgb(bg)});padding:16px;margin:8px"><div style="background:rgb({rgb(selected)});padding:12px">仅淡填充 {ratio:.3f}:1</div><div style="border-left:6px solid rgb{border};padding:12px">实线+文字“已选中” {edge:.3f}:1</div></div>')
    assert all(r['row_fill_contrast']<3 for r in rows)
    (OUT/'contrast.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
    (OUT/'contrast-demo.html').write_text('<!doctype html><meta charset="utf-8"><title>合成透明度实验</title><h1>教学色板，不是 ELY 实机</h1>'+''.join(parts))
    print('9 个合成场景；两条数学端点断言通过；淡填充均不足 3:1。没有实机合规结论。')
def inventory():
    upstream=ROOT.parent/'upstream'
    p=subprocess.run(['cargo','metadata','--offline','--no-deps','--format-version','1'],cwd=upstream,capture_output=True,text=True)
    print('上游 cargo metadata 退出码:',p.returncode)
    if p.returncode:print(p.stderr)
    else:
        j=json.loads(p.stdout);pkg=j['packages'][0];print('上游包版本:',pkg['version'],'最低 Rust:',pkg['rust_version']);print('本环境 rustc 1.85.1 < 1.95：完整应用未构建；不下载新工具链、不冒称全量测试。')
    print('待验证：macOS 11+ Apple silicon 安装、macOS 27 透明背景、GUI 多会话/宠物、中文软折行的点击光标定位。')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('step',choices=['baseline','shell','contrast','inventory']);a=p.parse_args();globals()[a.step]()
