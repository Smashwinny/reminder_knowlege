# -*- coding: utf-8 -*-
"""实验3：解剖官方安装器 deploy.sh（4417 行 TUI 向导）——验证"一个 Rust 二进制 + 一个 Postgres"
零依赖（仅标准库）。输入 exercise/deploy_downloaded.sh。
"""
import re, os

src = open(os.path.join(os.path.dirname(__file__), 'deploy_downloaded.sh'), encoding='utf-8').read()
print(f'deploy.sh 总行数: {src.count(chr(10)) + 1}')

steps = re.findall(r'^(step_\w+)\(\)', src, re.M)
print(f'\nTUI 向导步骤函数: {len(steps)} 个')
for s in steps:
    print(f'  {s}')

# 装了哪些东西？
print('\n安装清单证据:')
for pat, label in [
    (r'timescale/timescaledb-ha:(\w+)', 'Postgres 容器镜像'),
    (r'releases/download/(\$version|\{?\$?version\}?)/temps-\$target\.tar\.gz', 'Temps 二进制下载模板'),
    (r'docker run -d', 'docker run 调用'),
    (r'\[Unit\]', 'systemd 服务单元'),
    (r'CAP_NET_BIND_SERVICE', '特权端口能力授予'),
]:
    hits = re.findall(pat, src)
    print(f'  {label}: {len(hits)} 处匹配 {hits[:3] if hits else ""}')

# 关键行摘录
m = re.search(r'local url="(https://github[^"]+)"', src)
print('\n二进制下载 URL 模板:', m.group(1) if m else '未找到')
m2 = re.search(r'docker pull ([\w/.:-]+timescaledb[\w/.:-]*)', src)
print('TimescaleDB 镜像:', m2.group(1) if m2 else '未找到')
print('\n结论: 安装器只装两样东西——① GitHub Releases 的单一 temps 二进制（systemd 托管）')
print('      ② 一个 TimescaleDB(Postgres) 容器；其余(Docker/SSL/TLS)是运行前提。')
