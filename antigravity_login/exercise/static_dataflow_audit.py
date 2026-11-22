#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""固定第三方仓库的离线数据流标记审计；不读取真实 token/配置或执行上游代码。"""
import argparse
import json
from pathlib import Path

MANAGER_COMMIT = "0067fe045ddd77f4462ea8e2c25384839d869f32"
BRIDGE_COMMIT = "2c8c12d7f515873e011a8c7a8d40c3a250a4a1a0"
PATTERNS = ["daily-cloudcode-pa.googleapis.com", "cloudcode-pa.googleapis.com",
            "cloudcode-pa.sandbox.googleapis.com", "antigravity-oauth-token"]


def scan(root):
    matches = {pattern: [] for pattern in PATTERNS}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts or path.suffix not in {".rs", ".toml", ".md", ".json", ".ts", ".js"}:
            continue
        if path.stat().st_size > 2_000_000:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in PATTERNS:
            if pattern in text:
                matches[pattern].append(str(path.relative_to(root)))
    license_text = (root / "LICENSE").read_text(encoding="utf-8")
    return {"manager_commit": MANAGER_COMMIT, "bridge_commit": BRIDGE_COMMIT,
            "matches": matches,
            "license_is_cc_by_nc_sa": "Attribution-NonCommercial-ShareAlike 4.0 International" in license_text,
            "scope": "只匹配源码标记与许可；不读取真实凭据，不证明运行行为或所有数据流"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manager-root", type=Path, default=Path(__file__).parents[1] / "repo-manager")
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("dataflow-audit-v2.json"))
    args = parser.parse_args()
    result = scan(args.manager_root)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("标记命中：", {key: len(value) for key, value in result["matches"].items()})
    print("CC-BY-NC-SA：", result["license_is_cc_by_nc_sa"])
    print("边界：静态标记不等于完整运行数据流；Bridge README 自述另行标注")


if __name__ == "__main__":
    main()
