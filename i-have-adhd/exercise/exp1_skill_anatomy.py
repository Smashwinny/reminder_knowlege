# -*- coding: utf-8 -*-
"""exp1: SKILL.md 解剖器——零依赖，验证技能包的结构契约。

问题：52.9k 星的项目本体只是一个 Markdown 文件，它的"代码"是什么？
答：是一份可机检的结构契约。本脚本把它当配置文件逐项验收。
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent / "repo"
SKILL = REPO / "skills" / "i-have-adhd" / "SKILL.md"

text = SKILL.read_text(encoding="utf-8")

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))


# --- 1. YAML frontmatter 存在且字段齐全 ---
m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
check("frontmatter 存在", bool(m))
fm = m.group(1) if m else ""
fields = {}
for line in fm.splitlines():
    mm = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
    if mm:
        fields[mm.group(1)] = mm.group(2).strip()
for f in ("name", "description", "license", "disable-model-invocation"):
    check(f"frontmatter 字段 {f}", f in fields, fields.get(f, "")[:60])
check("name 值正确", fields.get("name") == "i-have-adhd", fields.get("name", ""))
check(
    "disable-model-invocation=true（只在用户召唤时生效）",
    fields.get("disable-model-invocation") == "true",
    fields.get("disable-model-invocation", ""),
)

# --- 2. 持久化条款：关闭短语必须与扩展实现一致 ---
body = text[m.end():] if m else text
check(
    "Persistence 段存在",
    "## Persistence" in body,
)
stop = ["stop adhd mode", "normal mode"]
for s in stop:
    check(f"关闭短语 '{s}' 在 SKILL.md 中", s in text)

# 与 extensions/i-have-adhd.ts 的 STOP_PHRASES 逐字对账
ts = (REPO / "extensions" / "i-have-adhd.ts").read_text(encoding="utf-8")
ts_phrases = re.findall(r'STOP_PHRASES = new Set\(\[([^\]]*)\]\)', ts)
ts_set = set(re.findall(r'"([^"]+)"', ts_phrases[0])) if ts_phrases else set()
check(
    "SKILL.md 关闭短语 == 扩展 STOP_PHRASES 集合",
    ts_set == set(stop),
    f"SKILL={sorted(set(stop))} TS={sorted(ts_set)}",
)

# --- 3. 10 条规则逐条存在（### N. 标题）---
rule_heads = re.findall(r"^### (\d+)\.\s+(.+)$", body, re.M)
check("规则条数 == 10", len(rule_heads) == 10, f"实际 {len(rule_heads)}")
expect = [
    "Lead with the next action",
    "Number multi-step tasks",
    "End with one concrete next action",
    "Suppress tangents",
    "Restate state every turn",
    "Give specific time estimates",
    "Make completed work visible",
    "Matter-of-fact tone for errors",
    "Cap lists to 5 items",
    "No preamble, no recap, no closing pleasantries",
]
for i, (num, title) in enumerate(rule_heads, 1):
    check(f"规则 {i} 标题吻合", int(num) == i and title == expect[i - 1], title)

# --- 4. 逃生舱与发送前检查 ---
check("When to break the rules 段", "## When to break the rules" in body)
esc = re.findall(r"^\d+\.\s+", body.split("## When to break the rules")[1].split("## Pre-send check")[0], re.M)
check("逃生舱 6 条", len(esc) == 6, f"实际 {len(esc)}")
check("Pre-send check 段", "## Pre-send check" in body)
check(
    "终检句（只读首行末行能否知道下一步与刚才发生了什么）",
    "reads only the first line and the last line" in body,
)

# --- 5. 规则9 完整性红线：呈现限制不得伤分析 ---
check(
    "规则9 保留'Never omit relevant items'红线",
    "Never omit relevant items when completeness matters" in body,
)

# --- 6. 与 README 的 10 条简版对账 ---
readme = (REPO / "README.md").read_text(encoding="utf-8")
readme_rules = re.findall(r"^\d+\.\s+(.+)$", readme.split("## The rules")[1].split("## Tune it")[0], re.M)
check("README 简版 10 条", len(readme_rules) == 10, f"实际 {len(readme_rules)}")

ok = sum(1 for _, o, _ in results if o)
print(f"i-have-adhd SKILL.md 结构契约体检: {ok}/{len(results)} PASS\n")
for name, o, detail in results:
    print(f"{'PASS' if o else 'FAIL'}  {name}" + (f"  [{detail}]" if detail and not o else ""))
sys.exit(0 if ok == len(results) else 1)
