# -*- coding: utf-8 -*-
"""实验2：验证 "69 个命令组、440+ 条 CLI 命令" 的说法——从 npm CLI 源码统计
零依赖（仅标准库）。apps/temps-cli/src/commands/ 每个子目录一个命令组。
"""
import os, re, json

CMDS = os.path.join(os.path.dirname(__file__), '..', 'repo', 'apps', 'temps-cli', 'src', 'commands')
groups = sorted(d for d in os.listdir(CMDS) if os.path.isdir(os.path.join(CMDS, d)))
print(f'命令组（commands/ 子目录）: {len(groups)} 个')
print('  ' + ', '.join(groups))

# 统计每个组里的 .ts 命令文件（排除 .test.ts）
total = 0
per = {}
for g in groups:
    ts = [f for f in os.listdir(os.path.join(CMDS, g))
          if f.endswith('.ts') and not f.endswith('.test.ts')]
    per[g] = len(ts)
    total += len(ts)
print(f'\n命令实现文件总数（不含测试）: {total}')
top = sorted(per.items(), key=lambda x: -x[1])[:10]
print('最大的 10 个命令组:', ', '.join(f'{g}({n})' for g, n in top))

# openapi.json 端点数（REST 面）
spec = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'repo', 'apps', 'temps-cli', 'openapi.json'), encoding='utf-8'))
sentry_style = [p for p in spec['paths'] if p.startswith('/0/')]
print(f'\nOpenAPI 路径总数: {len(spec["paths"])}（其中 Sentry 兼容错误追踪风格 /0/...: {len(sentry_style)} 条）')

# skills 目录（drop-in Claude Code 技能包）
SK = os.path.join(os.path.dirname(__file__), '..', 'repo', 'skills')
skills = sorted(d for d in os.listdir(SK) if os.path.isdir(os.path.join(SK, d)))
print(f'\n官方 drop-in skills（放进 .claude/skills/ 即用）: {len(skills)} 个 -> {", ".join(skills)}')
