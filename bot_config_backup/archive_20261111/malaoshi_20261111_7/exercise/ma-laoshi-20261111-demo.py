#!/usr/bin/env python3
"""顺序运行五步：python3 ma-laoshi-20261111-demo.py 1（至5）。
只读写同目录 sandbox；真实账号、密钥、云电脑配置一律不接触。
来源/基线见 ma-laoshi-20261111-backup.py 首部。
"""
import importlib.util,sys,json,hashlib,subprocess
from pathlib import Path
spec=importlib.util.spec_from_file_location('backup',Path(__file__).with_name('ma-laoshi-20261111-backup.py'))
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
s=int(sys.argv[1]);print('STEP',s)
if s==1:
    assert not b.ROOT.exists(),'请使用新的解压目录，不覆盖已有实验'
    b.ROOT.mkdir();b.SRC.mkdir()
    entries={'config/settings.json':'{"theme":"cyan","language":"zh-CN"}\n','skills/writing.md':'# 合成写作技能\n只用作演示。\n','notes/study.md':'合成公开学习笔记。\n','notes/planted.md':'fake = '+'ghp_'+'X'*36+'\n','secrets/ignored.txt':'合成敏感目录占位，不是真凭证。\n','cookies/session.json':'{}\n','chat/history.md':'合成聊天，不应入库。\n','node_modules/pkg/index.js':'// 可重装依赖\n','config/.env':'SYNTHETIC=1\n','docs/RESTORE.md':'# 合成配置恢复说明\n1. 在新空目录读取 MANIFEST.json。\n2. 仅将 config、skills、notes、docs 与清单 hash 对比。\n3. 使用 dry-run 目录预览，不覆盖任何真实路径。\n4. 凭证和登录态未备份，真实恢复需重新通过官方授权。\n5. 不自动安装或执行恢复的技能；人工检查后再导入。\n'}
    for n,t in entries.items():
        p=b.SRC/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t)
    (b.SRC/'notes'/'link.md').symlink_to('../secrets/ignored.txt')
    b.git('init','--bare','--initial-branch=main',b.REMOTE)
    print('SEEDED 10 synthetic regular files + 1 symlink; remote empty')
elif s==2:
    rc=b.backup();assert rc==23
    refs=b.git('show-ref',cwd=b.REMOTE) if (b.REMOTE/'refs/heads/main').exists() else ''
    assert not refs and not b.WORK.exists()
    print('PASS: rc=23; no staging repository, commit, or remote ref')
elif s==3:
    (b.SRC/'notes/planted.md').unlink()
    assert b.backup()==0
    files=b.git('ls-tree','--name-only','-r','main',cwd=b.REMOTE).splitlines()
    assert files==['MANIFEST.json','config/settings.json','docs/RESTORE.md','notes/study.md','skills/writing.md']
    print('PASS: remote has exactly 5 approved files; symlink/excluded paths absent')
elif s==4:
    before=b.git('rev-parse','main',cwd=b.REMOTE)
    assert b.backup()==0
    assert before==b.git('rev-parse','main',cwd=b.REMOTE)
    examples=['ghp_'+'Y'*36,'github_pat_'+'Y'*40,'sk-'+'Y'*24,'AKIA'+'Y'*16,'-----BEGIN PRIVATE KEY-----']
    assert all(b.findings(x) for x in examples)
    print('PASS: idempotent commit; 5/5 synthetic secret-pattern positive controls')
elif s==5:
    dest=b.ROOT/'restore-preview';assert not dest.exists()
    b.git('clone','--branch','main',b.REMOTE,dest)
    manifest=json.loads((dest/'MANIFEST.json').read_text())
    for n,h in manifest.items():
        assert hashlib.sha256((dest/n).read_bytes()).hexdigest()==h
        print('HASH MATCH',n)
    assert not (dest/'secrets').exists()
    print('PASS: dry-run restore 4/4 file hashes; no real configuration overwritten')
else: raise ValueError('1..5')
