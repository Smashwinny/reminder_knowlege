"""只下载课程公开示例并校验，不导入/运行它。使用公开下载确认链接，不使用账户。"""
from pathlib import Path
import urllib.request,hashlib
p=Path(__file__).resolve().parents[1]/'coding_agent_from_scratch.py'
u='https://drive.usercontent.google.com/download?id=1DxKa_autBOu9s8DvItodgUAwH_pBg7aR&export=download&confirm=t'
b=urllib.request.urlopen(u,timeout=30).read()
expected='a70a9bece7952abb6b466eb16ece51ae1716d177d0a1a85c5e017de85ebce2b4'
assert hashlib.sha256(b).hexdigest()==expected,'公开文件变化或下载非源码，拒绝使用'
p.write_bytes(b);print('verified source',len(b),expected)
