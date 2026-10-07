# -*- coding: utf-8 -*-
"""AI 工程面试题库分析器 —— ai-engineering-interview-questions-company-wise 学习实验。

功能：
1. stats   解析仓库 README.md，统计题目数、分区分布、答案覆盖率、公司提及榜
2. quiz    按主题抽题生成自测卷（Markdown + 彩色 HTML），种子可复现

只依赖 Python 标准库。用法：
    python quiz_generator.py stats
    python quiz_generator.py quiz --topic "RAG" --count 5 --seed 42
"""
import argparse
import html
import random
import re
import sys
from collections import Counter
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "repo" / "README.md"


def parse_questions():
    """把 README 解析成 [{section, topic, text, asked_at[], answer(bool)}]。"""
    skip_sections = {"Table of Contents", "How to use this"}
    questions = []
    section = topic = ""
    current = None
    for line in README.read_text(encoding="utf-8").splitlines():
        m2 = re.match(r"^## (.+)$", line)
        m3 = re.match(r"^### (.+)$", line)
        if m2:
            section, topic = m2.group(1).strip(), ""
            continue
        if m3:
            topic = m3.group(1).strip()
            continue
        if line.startswith("- ") and section not in skip_sections:
            current = {
                "section": section, "topic": topic,
                "text": line[2:].strip(), "asked_at": [], "has_answer": False,
            }
            questions.append(current)
        elif current is not None:
            m_ask = re.match(r"\s+- Asked at: (.+)$", line)
            m_ans = re.match(r"\s+- Answer: ", line)
            if m_ask:
                companies = re.findall(r"\[([^\]]+)\]", m_ask.group(1))
                current["asked_at"].extend(companies)
            elif m_ans:
                current["has_answer"] = True
    return questions


def cmd_stats(_args):
    qs = parse_questions()
    total = len(qs)
    with_ans = sum(1 for q in qs if q["has_answer"])
    company_counter = Counter(c for q in qs for c in q["asked_at"])
    print("=" * 60)
    print("AI 工程面试题库 · 统计报告")
    print(f"源文件: {README}")
    print("=" * 60)
    print(f"题目总数：{total}")
    print(f"带答案链接：{with_ans}（{with_ans / total * 100:.1f}%）")
    print(f"被标注'哪些公司问过'的题目：{sum(1 for q in qs if q['asked_at'])}")
    print("\n按大类（## 分区）题目分布：")
    for sec, n in Counter(q["section"] for q in qs).most_common():
        print(f"  {sec:<50} {n:4d} 题")
    print("\n公司提及榜（Asked at 次数 Top 12）：")
    for company, n in company_counter.most_common(12):
        bar = "█" * n
        print(f"  {company:<28} {n:3d}  {bar}")
    if not company_counter:
        print("  （无 Asked at 数据）")
    return qs


def cmd_quiz(args):
    qs = parse_questions()
    pool = [q for q in qs if args.topic.lower() in (q["topic"] + " " + q["section"]).lower()]
    if not pool:
        print(f"主题 '{args.topic}' 无匹配题目。可选主题：")
        for t in sorted({q["topic"] for q in qs if q["topic"]}):
            print("  -", t)
        sys.exit(1)
    rng = random.Random(args.seed)
    picked = rng.sample(pool, min(args.count, len(pool)))
    md_lines = [f"# 自测卷：{args.topic}（{len(picked)} 题，seed={args.seed}）", ""]
    rows = ""
    for i, q in enumerate(picked, 1):
        asked = "、".join(q["asked_at"]) if q["asked_at"] else "未标注"
        flag = "🈶答案" if q["has_answer"] else "🈚答案"
        md_lines.append(f"{i}. {q['text']}")
        md_lines.append(f"   - 分区：{q['section']} / {q['topic']}；问过：{asked}；{flag}")
        md_lines.append("")
        rows += (f"<tr><td>{i}</td><td>{html.escape(q['text'])}</td>"
                 f"<td>{html.escape(q['topic'])}</td><td>{html.escape(asked)}</td>"
                 f"<td>{flag}</td></tr>")
    out_md = Path(__file__).resolve().parent / f"quiz_{args.topic.replace(' ', '_')}.md"
    out_md.write_text("\n".join(md_lines), encoding="utf-8")
    out_html = Path(__file__).resolve().parent / f"quiz_{args.topic.replace(' ', '_')}.html"
    out_html.write_text(f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<title>自测卷 {html.escape(args.topic)}</title><style>
body{{font-family:"Microsoft YaHei";margin:32px;background:#eef2ff}}
h1{{color:#4338ca}}table{{border-collapse:collapse;background:#fff;width:100%}}
th{{background:#4f46e5;color:#fff;padding:8px}}td{{border:1px solid #c7d2fe;padding:8px}}
tr:nth-child(even){{background:#e0e7ff}}</style></head><body>
<h1>自测卷：{html.escape(args.topic)}（{len(picked)} 题，seed={args.seed}）</h1>
<table><tr><th>#</th><th>题目</th><th>主题</th><th>问过的公司</th><th>答案</th></tr>{rows}</table>
</body></html>""", encoding="utf-8")
    print(f"抽题 {len(picked)}/{len(pool)} 完成：")
    for i, q in enumerate(picked, 1):
        print(f"  {i}. {q['text'][:60]}{'…' if len(q['text']) > 60 else ''}")
    print(f"\n已生成：{out_md.name} / {out_html.name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("stats")
    q = sub.add_parser("quiz")
    q.add_argument("--topic", required=True)
    q.add_argument("--count", type=int, default=5)
    q.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    {"stats": cmd_stats, "quiz": cmd_quiz}[args.cmd](args)


if __name__ == "__main__":
    main()
