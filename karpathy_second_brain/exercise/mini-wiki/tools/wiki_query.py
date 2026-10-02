# -*- coding: utf-8 -*-
"""wiki_query.py — LLM-Wiki 的 Query 操作最小实现（确定性检索演示）。

真实场景：LLM 先读 index.md 找到相关页，再钻进去综合成带引用的答案。
本脚本演示"先索引后钻取"的打分排序：
  标题命中 x3 + 双链/related 命中 x2 + 正文命中 x1 + 入链数 x0.5

用法: python tools/wiki_query.py <关键词> [关键词2 ...]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
FRONT_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
LINK_RE = re.compile(r"\[\[([^\]|#]+)")


def main():
    if len(sys.argv) < 2:
        sys.exit("用法: python tools/wiki_query.py <关键词> [关键词2 ...]")
    terms = [t.lower() for t in sys.argv[1:]]

    index = WIKI / "index.md"
    print(f"[Query] 先读索引 {index.relative_to(ROOT)} ...")
    if index.exists():
        hits = [ln.strip() for ln in index.read_text(encoding="utf-8").splitlines()
                if any(t in ln.lower() for t in terms)]
        for h in hits[:5]:
            print(f"        索引命中: {h}")

    pages = [p for p in WIKI.rglob("*.md") if p.name not in ("index.md", "log.md")]
    names = {p.stem for p in pages}
    scored = []
    for p in pages:
        text = p.read_text(encoding="utf-8")
        low = text.lower()
        score = 0.0
        for t in terms:
            if t in p.stem.lower():
                score += 3
            fm = FRONT_RE.match(text)
            if fm and t in fm.group(1).lower():
                score += 2
            score += low.count(t)
        backlinks = sum(1 for q in pages
                        if q != p and any(l.strip() == p.stem
                                          for l in LINK_RE.findall(q.read_text(encoding="utf-8"))))
        score += 0.5 * backlinks
        if score > 0:
            scored.append((score, p, backlinks))

    scored.sort(reverse=True)
    print(f"\n[Query] 「{' '.join(terms)}」检索结果（{len(scored)} 页命中）:")
    print("-" * 62)
    for score, p, backlinks in scored[:8]:
        snippet = ""
        body = p.read_text(encoding="utf-8")
        for line in body.splitlines():
            if any(t in line.lower() for t in terms) and not line.startswith(("---", "#", "title:", "type:")):
                snippet = line.strip()[:48]
                break
        rel = p.relative_to(WIKI)
        print(f"  {score:6.1f}  {rel}  (入链 {backlinks})")
        if snippet:
            print(f"         └─ {snippet}")
    if not scored:
        print("  （无命中——好答案值得写回 wiki：这就是'查询成果回填'的时机）")


if __name__ == "__main__":
    main()
