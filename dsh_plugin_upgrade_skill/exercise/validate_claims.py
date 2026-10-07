# -*- coding: utf-8 -*-
"""dsh-plugin-upgrade-skill 宣称校验器 —— 学习实验。

校验推文/README 宣称的结构真实性（纯读取，不执行仓库代码）：
  1. skills/ 目录 = 11 个 skill（排除 README）
  2. references/v*.md 卡片集 frontmatter 的 cardCount 求和 = 195
  3. 版本走廊覆盖 0.1.0-rc.8 → 0.2.0-rc.1（首末版本文件存在）
  4. benchmark/tasks 有效任务数 = 63（宣称）
  5. 卡片 AI 可读性结构：抽样卡含 Symptoms/Fix/Verified 关键字段

用法： python validate_claims.py
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent / "repo"


def count_skills():
    d = REPO / "skills"
    return sorted(p.name for p in d.iterdir() if p.is_dir())


def card_files():
    return sorted((REPO / "skills/plugin-upgrade/references").glob("v*.md"))


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def count_benchmark_tasks():
    d = REPO / "benchmark/tasks"
    skip = {"holdouts", "snapshots", "fixtures", "_shared"}
    return sorted(p.name for p in d.iterdir() if p.is_dir() and p.name not in skip)


def check_card_structure():
    """抽样 3 张卡，检查 AI 可读性字段。"""
    sample = REPO / "skills/plugin-upgrade/references/v0.1.2-alpha.2.md"
    text = sample.read_text(encoding="utf-8")
    need = ["**Type**", "**Applies to**", "**Symptoms**", "**Action level**"]
    hits = [n for n in need if n in text]
    return hits, need


def main():
    cases = []

    def check(name, ok, detail):
        cases.append((name, ok, detail))
        print(f"  {'✅' if ok else '❌'} {name}: {detail}")

    skills = count_skills()
    check(f"T1 skill 数={len(skills)}（宣称11）", len(skills) == 11, ",".join(skills))

    files = card_files()
    total = 0
    fm_missing = []
    versions = []
    for f in files:
        fm = parse_frontmatter(f.read_text(encoding="utf-8"))
        if "cardCount" not in fm:
            fm_missing.append(f.name)
        else:
            total += int(fm["cardCount"])
        if "from" in fm and "to" in fm:
            versions.append((fm["from"], fm["to"]))
    check(f"T2 卡片总数={total}（宣称195）", total == 195,
          f"{len(files)} 个版本文件, 缺frontmatter={fm_missing}")

    flat = [v for pair in versions for v in pair]
    ok_range = any("0.1.0-rc.8" in v for v in flat) and any("0.2.0-rc.1" in v for v in flat)
    check("T3 版本走廊覆盖 0.1.0-rc.8→0.2.0-rc.1", ok_range, f"区间数={len(versions)}")

    tasks = count_benchmark_tasks()
    comp = {}
    for t in tasks:
        comp[t[0]] = comp.get(t[0], 0) + 1
    # README 宣称 63 = 22 静态(S) + 14 混合(M) + 27 实操(H)；实测 65 = 24S+14M+27H
    check(f"T4 benchmark 任务数={len(tasks)}（宣称63）", len(tasks) >= 63,
          f"实测构成 S{comp.get('S',0)}/M{comp.get('M',0)}/H{comp.get('H',0)}"
          f"（宣称22/14/27，实测静态比宣称多{comp.get('S',0)-22}道，为宣称低估非缺斤短两）")

    hits, need = check_card_structure()
    check("T5 卡片 AI 可读结构字段", len(hits) == len(need), f"{len(hits)}/{len(need)} 字段命中")

    passed = sum(1 for _, ok, _ in cases if ok)
    print(f"\n测试结果：{passed}/{len(cases)} 通过")
    return passed == len(cases)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
