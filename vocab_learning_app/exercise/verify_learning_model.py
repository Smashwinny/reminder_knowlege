"""Independent, stdlib-only checks for the vocabulary app's public algorithms.

This does not import upstream code. It verifies a small reference model and then
checks that the pinned upstream source still contains the corresponding rules.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import subprocess
import unicodedata
from pathlib import Path


def ebbinghaus(n: int, daily_items: int, offsets=(1, 2, 4, 7, 15)) -> dict:
    if n < 1 or daily_items < 1:
        raise ValueError("n and daily_items must be positive")
    batches = []
    for start in range(1, n + 1, daily_items):
        batches.append(list(range(start, min(start + daily_items, n + 1))))
    last_day = len(batches) + max(offsets)
    days = []
    for day in range(1, last_day + 1):
        new = batches[day - 1] if day <= len(batches) else []
        review = []
        for batch_day, batch in enumerate(batches, start=1):
            if day - batch_day in offsets:
                review.extend(batch)
        days.append({"day": day, "new": new, "review": review,
                     "all": sorted(set(new + review))})
    return {"batches": batches, "days": days}


def hulu(n: int, daily_items: int) -> list[list[int]]:
    if n < 1 or daily_items < 1:
        raise ValueError("n and daily_items must be positive")
    return [list(range(start, min(start + daily_items, n + 1)))
            for start in range(1, n + 1, daily_items)]


def lcs_length(a: str, b: str) -> int:
    previous = [0] * (len(b) + 1)
    for char_a in a:
        current = [0]
        for index, char_b in enumerate(b, start=1):
            current.append(previous[index - 1] + 1 if char_a == char_b
                           else max(previous[index], current[-1]))
        previous = current
    return previous[-1]


def spelling_score(a: str, b: str) -> float:
    return 2 * lcs_length(a, b) / (len(a) + len(b))


def normalize(word: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", word).strip().split()).casefold()


def word_id(word: str) -> str:
    return "w_" + hashlib.sha256(normalize(word).encode("utf-8")).hexdigest()[:20]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--log", type=Path, required=True)
    args = parser.parse_args()
    lines = []
    checks = []

    def emit(text: str) -> None:
        print(text)
        lines.append(text)

    def check(name: str, condition: bool, evidence: str) -> None:
        checks.append({"name": name, "passed": bool(condition), "evidence": evidence})
        emit(f"{'PASS' if condition else 'FAIL'} | {name} | {evidence}")
        if not condition:
            raise AssertionError(name)

    emit("Independent vocabulary learning model experiment")
    emit(f"Python: {platform.python_version()} (isolated mode -I; stdlib only)")
    commit = subprocess.run(["git", "-C", str(args.repo), "rev-parse", "HEAD"],
                            check=True, capture_output=True, text=True).stdout.strip()
    version = (args.repo / "VERSION").read_text(encoding="utf-8").strip()
    check("pinned upstream version", commit == "638ae84f97a04474cb63c6098eacfc6c83b813af" and version == "0.1.11",
          f"commit={commit}; VERSION={version}")

    plan = ebbinghaus(8, 3)
    check("ebbinghaus first-pass batches", plan["batches"] == [[1, 2, 3], [4, 5, 6], [7, 8]],
          json.dumps(plan["batches"]))
    day2 = plan["days"][1]
    day4 = plan["days"][3]
    check("day 2 combines new and day+1 review", day2["new"] == [4, 5, 6] and day2["review"] == [1, 2, 3],
          json.dumps(day2, ensure_ascii=False))
    check("day 4 combines offset+1 and offset+2 reviews", day4["review"] == [4, 5, 6, 7, 8],
          json.dumps(day4, ensure_ascii=False))
    new_ids = [item for day in plan["days"] for item in day["new"]]
    review_ids = [item for day in plan["days"] for item in day["review"]]
    check("new coverage and five reviews per item", new_ids == list(range(1, 9)) and len(review_ids) == 40
          and all(review_ids.count(item) == 5 for item in range(1, 9)),
          f"new={new_ids}; review_events={len(review_ids)}; last_day={plan['days'][-1]['day']}")

    hulu_plan = hulu(5, 2)
    check("hulu first-pass-only grouping", hulu_plan == [[1, 2], [3, 4], [5]],
          json.dumps(hulu_plan))
    check("hulu 80 percent page gate", 5 * 4 >= 4 * 5 and 5 * 3 < 4 * 5,
          "4/5=80% passes; 3/5=60% does not")

    scores = {pair: spelling_score(*pair) for pair in [("quiet", "quite"), ("cat", "cut"), ("planet", "planeta")]}
    check("LCS spelling threshold", abs(scores[("quiet", "quite")] - 0.8) < 1e-9
          and scores[("cat", "cut")] < 0.75 and scores[("planet", "planeta")] >= 0.75,
          json.dumps({f"{a}/{b}": round(score, 6) for (a, b), score in scores.items()}))
    check("stable normalized word IDs", word_id("  WORD ") == word_id("word") and word_id("word") != word_id("words"),
          f"word={word_id('word')}; words={word_id('words')}")

    spaced_source = (args.repo / "utils/scripts/spaced_repetition.py").read_text(encoding="utf-8")
    spelling_source = (args.repo / "utils/scripts/dictionary_spelling.py").read_text(encoding="utf-8")
    plan_source = (args.repo / "utils/scripts/dictionary_plans.py").read_text(encoding="utf-8")
    service_source = (args.repo / "applications/词汇星图/scripts/service.py").read_text(encoding="utf-8")
    app_readme = (args.repo / "applications/词汇星图/README.md").read_text(encoding="utf-8")
    check("static source: documented review offsets", "DEFAULT_REVIEW_OFFSETS = (1, 2, 4, 7, 15)" in spaced_source,
          "spaced_repetition.py contains (1, 2, 4, 7, 15)")
    check("static source: integer-exact LCS threshold", "8 * lcs >= 3 * total" in spelling_source
          and "longest_common_subsequence_length(left, right)" in spelling_source,
          "2*LCS/(len(a)+len(b)) >= 3/4 is implemented as 8*LCS >= 3*total")
    check("static source: deterministic shuffle and optimistic revisions",
          "sha256(f'{plan[\"planId\"]}:{round_[\"number\"]}:{day}'" in plan_source
          and "expected_revision" in plan_source,
          "planId+round+day seeds shuffle; updates check expected_revision")
    check("static source: loopback API and origin gate", 'ThreadingHTTPServer(("127.0.0.1", port)' in service_source
          and "不允许的请求来源" in service_source,
          "API binds 127.0.0.1 and rejects non-loopback Origin")
    check("static source: graph and study limitations", "首屏最多显示 500 个词条及占位节点" in app_readme
          and "至少 80%" in app_readme,
          "README states 500-node first-screen cap and 80% Hulu gate")

    package = json.loads((args.repo / "applications/词汇星图/package.json").read_text(encoding="utf-8"))
    check("frontend manifest", package["dependencies"]["react"] == "^19.1.1"
          and package["devDependencies"]["vite"] == "^6.3.5",
          f"React={package['dependencies']['react']}; Vite={package['devDependencies']['vite']}")

    result = {"schemaVersion": "1.0", "upstreamCommit": commit, "upstreamVersion": version,
              "python": platform.python_version(), "passed": len(checks), "failed": 0,
              "checks": checks,
              "scope": "Independent reference tests plus static source checks; not an upstream runtime smoke test."}
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    emit(f"SUMMARY | {len(checks)} passed, 0 failed | results={args.output}")
    args.log.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
