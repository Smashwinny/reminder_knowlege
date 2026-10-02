# -*- coding: utf-8 -*-
"""wiki_lint.py — LLM-Wiki 的 Lint 操作（健康体检），零依赖确定性实现。

Karpathy gist 里 Lint 是让 LLM 做健康检查（矛盾/过时/孤儿页/断链）。
本脚本实现其中**可确定性判定**的部分：
  1. frontmatter 必填字段
  2. [[断链]]（链接指向不存在的页）
  3. 孤儿页（没有任何入链、也不是 index/log）
  4. index.md 覆盖率（每个页面都应被目录收录）
  5. log.md 每条都有统一前缀 `## [日期] 操作 | 说明`
  6. frontmatter 里的 sources 路径必须真实存在于 raw/

用法: python tools/wiki_lint.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"
FRONT_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
LINK_RE = re.compile(r"\[\[([^\]|#]+)")
LOG_RE = re.compile(r"^## \[\d{4}-\d{2}-\d{2}\] (ingest|query|lint) \| .+", re.M)
REQUIRED = ["title", "type", "sources", "related", "created"]

problems, stats = [], {"pages": 0, "links": 0, "broken": 0, "orphans": 0}

pages = [p for p in WIKI.rglob("*.md") if p.name not in ("index.md", "log.md")]
names = {p.stem for p in pages}
inbound = {n: 0 for n in names}

print("=" * 62)
print(" mini-wiki 体检报告 (Lint)")
print("=" * 62)

for p in pages:
    stats["pages"] += 1
    text = p.read_text(encoding="utf-8")
    rel = p.relative_to(WIKI)
    # 1. frontmatter
    m = FRONT_RE.match(text)
    if not m:
        problems.append(f"❌ {rel}: 缺 frontmatter")
        continue
    fm = m.group(1)
    missing = [k for k in REQUIRED if not re.search(rf"^{k}:", fm, re.M)]
    if missing:
        problems.append(f"❌ {rel}: frontmatter 缺字段 {missing}")
    # 6. sources 存在性
    for s in re.findall(r"^\s+- \"(raw/[^\"]+)\"", fm, re.M):
        if not (ROOT / s).exists():
            problems.append(f"❌ {rel}: sources 指向不存在的 {s}")
    # 2. 断链 + 入链统计
    for target in LINK_RE.findall(text):
        t = target.strip()
        stats["links"] += 1
        if t not in names and t != "index":
            stats["broken"] += 1
            problems.append(f"❌ {rel}: 断链 [[{t}]]（目标页不存在）")
        elif t in inbound:
            inbound[t] += 1

# 3. 孤儿页
for name, cnt in inbound.items():
    if cnt == 0:
        stats["orphans"] += 1
        problems.append(f"⚠️  孤儿页: {name}（没有任何页面链接它）")

# 4. index 覆盖率
index_text = (WIKI / "index.md").read_text(encoding="utf-8") if (WIKI / "index.md").exists() else ""
unindexed = [n for n in names if f"[[{n}]]" not in index_text]
for n in unindexed:
    problems.append(f"❌ index.md 未收录页面: {n}")

# 5. log 格式
log_path = WIKI / "log.md"
if log_path.exists():
    log_text = log_path.read_text(encoding="utf-8")
    bad = [ln for ln in log_text.splitlines()
           if ln.startswith("## [") and not LOG_RE.match(ln + "\n")]
    for ln in bad:
        problems.append(f"❌ log.md 格式非法: {ln!r}")
else:
    problems.append("⚠️  wiki/log.md 不存在（还没执行过任何操作？）")

# 汇总
print(f"页面总数: {stats['pages']}   双链总数: {stats['links']}   "
      f"断链: {stats['broken']}   孤儿页: {stats['orphans']}")
if problems:
    print(f"\n发现 {len(problems)} 个问题:")
    for pr in problems:
        print(" ", pr)
    sys.exit(1)
else:
    print("\n✅ 全部通过：frontmatter / 断链 / 孤儿页 / index 覆盖 / log 格式 / sources 路径")
