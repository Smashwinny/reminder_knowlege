# -*- coding: utf-8 -*-
"""mini_ingest.py — 把 LLM-Wiki 的 Ingest 簿记工作写成确定性脚本（演示用）。

真实场景：Ingest 由 Claude Code 等 LLM agent 完成（读原文 -> 写摘要页 ->
更新概念页 -> 更新 index -> 追加 log）。这里用零依赖 Python 演示同样的
簿记动作，让你看清一次 ingest 到底动了哪些文件。

用法: python tools/mini_ingest.py raw/<file>.md
"""
import re
import sys
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent   # mini-wiki/
WIKI = ROOT / "wiki"
TODAY = datetime.date.today().isoformat()

# 简单中英停用词（演示够用）
STOP = set("的 了 是 在 和 与 之 一 个 这 那 我们 你们 他们 它 而 及 或 就 都 也 被 把 "
           "the a an of to in on for and or is are was were be been it its this that "
           "with as by at from not you your i we they he she".split())


def slug(text: str) -> str:
    """标题 -> 文件名：保留中英数字，空格转连字符。"""
    s = re.sub(r"[^\w一-鿿-]+", "-", text.strip())
    return re.sub(r"-{2,}", "-", s).strip("-")


def parse_source(path: Path):
    text = path.read_text(encoding="utf-8")
    title_m = re.search(r"^# (.+)$", text, re.M)
    title = title_m.group(1).strip() if title_m else path.stem
    concepts = [m.strip() for m in re.findall(r"^## (.+)$", text, re.M)]
    # 取第一个引用块或第一段当 TL;DR
    tldr_m = re.search(r"^> (.+)$", text, re.M)
    tldr = tldr_m.group(1).strip() if tldr_m else (concepts[0] if concepts else title)
    keywords = [
        w for w in re.findall(r"[一-鿿]{2,4}|[A-Za-z][\w-]{2,}", text)
        if w.lower() not in STOP
    ]
    freq = {}
    for w in keywords:
        freq[w] = freq.get(w, 0) + 1
    top = [w for w, _ in sorted(freq.items(), key=lambda x: -x[1])[:8]]
    return title, concepts, tldr, top


def write_page(path: Path, front: dict, body: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    fm = "---\n"
    for k, v in front.items():
        if isinstance(v, list):
            fm += f"{k}:\n" + "".join(f"  - \"{x}\"\n" for x in v)
        else:
            fm += f'{k}: "{v}"\n'
    fm += "---\n"
    path.write_text(fm + "\n" + body, encoding="utf-8")


def rebuild_index(pages: dict):
    lines = ["# index.md — 内容目录\n",
             "> LLM 每次 ingest 后重建。查询时先读这里，再钻进具体页。\n"]
    groups = {}
    for name, (ptype, summ) in pages.items():
        groups.setdefault(ptype, []).append((name, summ))
    for ptype in sorted(groups):
        lines.append(f"\n## {ptype}\n")
        for name, summ in sorted(groups[ptype]):
            lines.append(f"- [[{name}]] — {summ}")
    (WIKI / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    if len(sys.argv) != 2:
        sys.exit("用法: python tools/mini_ingest.py raw/<file>.md")
    raw_rel = sys.argv[1]
    raw_path = ROOT / raw_rel
    if not raw_path.exists():
        sys.exit(f"找不到源文件: {raw_path}")

    title, concepts, tldr, top = parse_source(raw_path)
    src_slug = slug(title)

    # 1) 源摘要页
    src_body = (f"# {title}\n\n"
                f"**TL;DR**: {tldr}\n\n"
                f"## 关键概念\n\n"
                + "".join(f"- [[{slug(c)}]] — {c}\n" for c in concepts)
                + f"\n**高频词**: {', '.join(top)}\n")
    write_page(WIKI / "sources" / f"{src_slug}.md",
               {"title": title, "type": "source-summary", "sources": [raw_rel],
                "related": [slug(c) for c in concepts], "created": TODAY},
               src_body)
    print(f"[1/4] 源摘要页  wiki/sources/{src_slug}.md")

    # 2) 概念页（原子性：一页一概念，互链兄弟概念）
    for i, c in enumerate(concepts):
        siblings = [slug(x) for x in concepts if x != c]
        body = (f"# {c}\n\n"
                f"> [!NOTE] 本页由 ingest 自动建立的原子页（stub）：真实场景中"
                f" LLM 会把原文里关于「{c}」的内容蒸馏进这里。\n\n"
                f"**来源**: [[{src_slug}]]（raw/{Path(raw_rel).name}）\n\n"
                f"**相关概念**: " + (", ".join(f"[[{s}]]" for s in siblings) or "（暂无）") + "\n")
        write_page(WIKI / "concepts" / f"{slug(c)}.md",
                   {"title": c, "type": "concept", "sources": [raw_rel],
                    "related": [src_slug] + siblings, "created": TODAY},
                   body)
        print(f"[2/4] 概念页    wiki/concepts/{slug(c)}.md")

    # 3) 重建 index.md
    pages = {}
    for p in (WIKI / "sources").glob("*.md"):
        pages[p.stem] = ("source-summary", "raw 源的摘要页")
    for p in (WIKI / "concepts").glob("*.md"):
        pages[p.stem] = ("concept", p.stem)
    rebuild_index(pages)
    print(f"[3/4] 索引重建  wiki/index.md（共 {len(pages)} 页）")

    # 4) 追加 log.md（统一前缀 -> grep 可解析）
    log = WIKI / "log.md"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as f:
        f.write(f"## [{TODAY}] ingest | {title}（{len(concepts)} 概念页）\n")
    print(f"[4/4] 日志追加  wiki/log.md")


if __name__ == "__main__":
    main()
