#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
# Source https://github.com/earendil-works/pi/commit/b30d54b8aebe6408e02d1473446d25f8083da68f
SHA=b30d54b8aebe6408e02d1473446d25f8083da68f
if [ ! -d ../repo/.git ]; then
 git init ../repo
 git -C ../repo fetch --depth 1 https://github.com/earendil-works/pi "$SHA"
 git -C ../repo checkout --detach FETCH_HEAD
fi
[ "$(git -C ../repo rev-parse HEAD)" = "$SHA" ]
npm ci --ignore-scripts --no-audit --no-fund
python3 - <<'PY2'
import pathlib,json
p=pathlib.Path.cwd(); r=p.parent/'repo'; n=p/'node_modules'
if not (r/'node_modules').exists(): (r/'node_modules').symlink_to(n)
(n/'@earendil-works').mkdir(exist_ok=True)
for name in ['durable','chord','ai','codemode','schema','telemetry']:
 d=json.loads((r/'packages'/name/'package.json').read_text()); t=n/d['name']
 if not t.exists(): t.symlink_to(r/'packages'/name)
PY2
node_modules/.bin/vitest run --config ma-laoshi-20261111-vitest.config.ts --reporter verbose
