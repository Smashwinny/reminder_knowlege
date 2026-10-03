# -*- coding: utf-8 -*-
"""实验1：拆开 Temps 的单二进制——workspace crate 解剖器
零依赖（仅标准库），输入 repo/Cargo.toml + crates/ 目录，输出架构分类与统计。
"""
import re, os, collections

REPO = os.path.join(os.path.dirname(__file__), '..', 'repo')
cargo = open(os.path.join(REPO, 'Cargo.toml'), encoding='utf-8').read()

# 1) workspace 成员
members = re.findall(r'"(crates/[\w-]+|apps/[\w-]+)"', cargo)
crates = [m for m in members if m.startswith('crates/')]
apps = [m for m in members if m.startswith('apps/')]
print(f'workspace 成员总数: {len(members)}  (crates: {len(crates)}, apps: {len(apps)})')

# 2) crate 按领域后缀分类
domains = collections.Counter()
by_domain = collections.defaultdict(list)
for c in crates:
    name = c.split('/')[-1].replace('temps-', '')
    if name.startswith('analytics'):
        dom = 'analytics(网站分析/会话回放/漏斗)'
    elif name.startswith('ai') or name in ('agents', 'agent', 'embeddings', 'agents-mcp-proxy', 'ai-agent-cli', 'ai-api-tools', 'ai-chat', 'ai-gateway'):
        dom = 'ai(网关/沙箱/MCP)'
    elif name.startswith('query-') or name in ('kv', 'blob', 'file-store', 'memory'):
        dom = 'resources(托管数据库/存储)'
    elif name.startswith('import-') or name == 'import':
        dom = 'import(平台迁移导入)'
    elif name in ('git', 'git-credential', 'deployer', 'deployments', 'presets', 'static-files', 'environments', 'projects', 'preview-gateway'):
        dom = 'deploy(Git 构建部署)'
    elif name in ('proxy', 'edge', 'dns', 'dns-resolver', 'domains', 'network', 'routes', 'wireguard', 'infra', 'providers'):
        dom = 'network(代理/DNS/TLS/边缘)'
    elif name in ('analytics-backend', 'clickhouse', 'logs', 'log-aggregator', 'metrics', 'otel', 'observability', 'telemetry', 'monitoring', 'status-page', 'geo', 'screenshots'):
        dom = 'observability(可观测性)'
    elif name in ('error-tracking', 'notifications', 'email', 'email-tracking', 'webhooks', 'captcha-wasm', 'vulnerability-scanner', 'audit', 'auth', 'teams'):
        dom = 'ops(错误追踪/邮件/安全/团队)'
    elif name in ('database', 'migrations', 'entities', 'core', 'config', 'queue', 'flags', 'plugin-sdk', 'external-plugins', 'backup', 'backup-core', 'cloud', 'cloud-client', 'cloud-protocol', 'sandbox', 'vm-agent', 'pty-agent', 'cli', 'revenue'):
        dom = 'core(platform 内核)'
    else:
        dom = 'other'
    domains[dom] += 1
    by_domain[dom].append(name)

print('\ncrate 领域分布:')
for dom, n in domains.most_common():
    print(f'  {dom}: {n} 个')

# 3) 二进制目标（main.rs）
bins = []
for c in sorted(crates):
    p = os.path.join(REPO, c, 'src', 'main.rs')
    if os.path.exists(p):
        bins.append(c.split('/')[-1])
print(f'\n含 main.rs 的二进制目标: {len(bins)} 个 -> {bins}')
print('（发布产物只有一个 temps 二进制：temps-cli 是"单一入口"委托 lib.rs run()）')

# 4) CLI 子命令（来自 crates/temps-cli/src/lib.rs enum Commands 的 doc 注释）
lib = open(os.path.join(REPO, 'crates', 'temps-cli', 'src', 'lib.rs'), encoding='utf-8').read()
m = re.search(r'enum Commands \{(.*?)\n\}', lib, re.S)
body = m.group(1) if m else ''
variants = re.findall(r'/// ([^\n]+)\n\s+(\w+)', body)
print(f'\ntemps 二进制的子命令（enum Commands 变体 + 注释）: {len(variants)} 个')
for doc, v in variants:
    print(f'  temps {v.lower()}: {doc.strip()[:60]}')
