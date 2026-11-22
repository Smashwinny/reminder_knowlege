#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""固定连接器目录的离线结构审计；不执行连接器、不读取凭据或发起网络请求。"""
import argparse
import json
from pathlib import Path

EXPECTED_COMMIT = "0ffbcc02876c6fc1e3cc25c9f46356c49a7f11bf"
REQUIRED = {"auth": "## Auth", "hosts": "catalog_hosts", "rules": "## Operating Rules",
            "files": "## Files", "maturity": "## Maturity"}


def maturity(text):
    section = text.split("## Maturity", 1)
    if len(section) != 2:
        return "missing"
    body = section[1].split("\n## ", 1)[0]
    if "Live-tested" in body:
        return "live-tested-specific-commands"
    if "Draft:" in body:
        return "draft"
    return "unknown"


def inspect_skill(path):
    text = path.read_text(encoding="utf-8")
    return {"id": path.parent.name,
            "missing_sections": [name for name, marker in REQUIRED.items() if marker not in text],
            "maturity": "template" if path.parent.name.startswith("_") else maturity(text)}


def audit(root):
    files = sorted(root.glob("*/SKILL.md"))
    records = [inspect_skill(path) for path in files]
    counts = {}
    for record in records:
        counts[record["maturity"]] = counts.get(record["maturity"], 0) + 1
    return {"schema": "muse-catalog-static-audit-v1", "expected_commit": EXPECTED_COMMIT,
            "skill_files": len(records),
            "connector_entries": sum(record["maturity"] != "template" for record in records),
            "maturity_counts": counts,
            "fully_structured": sum(not record["missing_sections"] for record in records),
            "records": records,
            "scope": "静态结构/标签审计；Live-tested仅指条目列出的具体命令与环境，不证明整个连接器"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).parents[1] / "repo" / "connectors")
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("catalog-audit-v2.json"))
    args = parser.parse_args()
    result = audit(args.root)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"SKILL.md={result['skill_files']}；连接器={result['connector_entries']}；五段完整={result['fully_structured']}；成熟度={result['maturity_counts']}")
    print(f"输出：{args.output}")
    print("边界：未执行任何连接器；Live-tested不等于整个工具已验证")


if __name__ == "__main__":
    main()
