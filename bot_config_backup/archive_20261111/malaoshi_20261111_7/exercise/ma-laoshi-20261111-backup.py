#!/usr/bin/env python3
"""原创教学实现，不是作者脚本；只支持本目录的合成 sandbox。
需求来源 https://x.com/i/status/2110638135642313069 （2026-11-11读取）
公开知识基线 https://github.com/Smashwinny/reminder_knowlege/tree/a8674777e18302b8804b137212b1396cbfe5a747
安全参考 https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection
"""
from pathlib import Path
import os, subprocess, re, json, hashlib, shutil, sys
ROOT=Path(__file__).resolve().parent/'sandbox'
SRC=ROOT/'synthetic-source'; WORK=ROOT/'snapshot'; REMOTE=ROOT/'remote.git'
# 不读取真实 home/global git 配置、凭证；任何 git transport 只允许 file。
ENV={**os.environ,'GIT_CONFIG_GLOBAL':'/dev/null','GIT_CONFIG_NOSYSTEM':'1',
     'GIT_TERMINAL_PROMPT':'0','GIT_ALLOW_PROTOCOL':'file'}
def git(*args,cwd=ROOT):
    p=subprocess.run(['git','-c','credential.helper=','-c','core.hooksPath=/dev/null',*map(str,args)],cwd=cwd,env=ENV,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    print('$ git '+' '.join(map(str,args))+'\n'+p.stdout,end='')
    if p.returncode: raise RuntimeError('git failed '+str(p.returncode))
    return p.stdout.strip()
def findings(text):
    # 教学正则，不是完整 secret scanner；无有效凭证、无网络校验。
    rules=[r'ghp_[A-Za-z0-9]{20,}',r'github_pat_[A-Za-z0-9_]{20,}',r'sk-[A-Za-z0-9_-]{20,}',r'AKIA[0-9A-Z]{16}',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
    return [i+1 for i,p in enumerate(rules) if re.search(p,text)]
def selected():
    result={}
    for folder,ext in [('config','.json'),('skills','.md'),('notes','.md'),('docs','.md')]:
        base=SRC/folder
        if base.is_symlink() or not base.is_dir(): continue
        for current,dirs,files in os.walk(base,followlinks=False):
            dirs[:]=[d for d in dirs if d not in {'.git','secrets','vault','credentials','node_modules','venv','cookies','chat'} and not (Path(current)/d).is_symlink() and not d.startswith('.')]
            for name in sorted(files):
                p=Path(current)/name
                if p.is_symlink() or p.suffix!=ext or name.startswith('.') or any(t in name.lower() for t in ('token','credential','cookie','secret','chat')): continue
                if p.stat().st_size>65536: raise ValueError('file too large')
                result[p.relative_to(SRC).as_posix()]=p.read_bytes()
    return dict(sorted(result.items()))
def backup():
    # remote 固定为当前合成目录内 bare repo；不接受 URL，也不读取真实配置。
    if ROOT.is_symlink() or SRC.is_symlink() or WORK.is_symlink() or REMOTE.is_symlink(): raise ValueError('symlink root')
    data=selected(); hits=[]
    for name,body in data.items():
        if findings(body.decode('utf-8')): hits.append(name)
    if hits:
        print('BLOCKED before add/commit/push; paths only: '+', '.join(hits)); return 23
    print('SCAN PASS; selected files='+str(len(data))+' bytes='+str(sum(map(len,data.values()))))
    WORK.mkdir(exist_ok=True)
    if not (WORK/'.git').exists():
        git('init','-b','main',WORK)
        git('config','user.name','Synthetic Backup Lab',cwd=WORK)
        git('config','user.email','sandbox@example.invalid',cwd=WORK)
    # 历史扫描：已有合成快照每次也逐 blob 检查，不只看工作树。
    rev=git('rev-list','--all','--objects',cwd=WORK)
    for line in rev.splitlines():
        oid=line.split()[0]
        typ=git('cat-file','-t',oid,cwd=WORK)
        if typ=='blob':
            # 不打印 blob 内容（日志里同样不能泄露真实值）。
            body=subprocess.check_output(['git','cat-file','blob',oid],cwd=WORK,env=ENV)
            if findings(body.decode('utf-8')): print('BLOCKED historical blob'); return 24
    for p in WORK.iterdir():
        if p.name=='.git': continue
        if p.is_dir(): shutil.rmtree(p)
        else: p.unlink()
    for name,body in data.items():
        p=WORK/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(body)
    manifest={k:hashlib.sha256(v).hexdigest() for k,v in data.items()}
    (WORK/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    git('add','--all',cwd=WORK)
    diff=subprocess.run(['git','diff','--cached','--quiet'],cwd=WORK,env=ENV).returncode
    if diff==1: git('commit','-m','Synthetic approved snapshot',cwd=WORK)
    elif diff==0: print('NO CHANGE: no new commit')
    else: raise RuntimeError('diff failed')
    git('push',REMOTE,'HEAD:refs/heads/main',cwd=WORK)
    return 0
if __name__=='__main__': sys.exit(backup())
