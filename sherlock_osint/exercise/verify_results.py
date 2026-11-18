"""Assert the local Sherlock exercise results and loopback-only request evidence."""
from __future__ import annotations

import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"

expected = {
    ("learner_demo", "LocalStatus"): ("Claimed", "200"),
    ("learner_demo", "LocalMessage"): ("Claimed", "200"),
    ("learner_demo", "LocalRedirect"): ("Claimed", "200"),
    ("learner_demo", "LocalRegex"): ("Claimed", "200"),
    ("learner_demo", "LocalSlow"): ("Claimed", "200"),
    ("learner_demo", "LocalWaf"): ("Claimed", "200"),
    ("missing_demo", "LocalStatus"): ("Available", "404"),
    ("missing_demo", "LocalMessage"): ("Available", "200"),
    ("missing_demo", "LocalRedirect"): ("Available", "302"),
    ("missing_demo", "LocalRegex"): ("Available", "404"),
    ("missing_demo", "LocalSlow"): ("Available", "404"),
    ("missing_demo", "LocalWaf"): ("Claimed", "404"),
    ("limited_demo", "LocalStatus"): ("Available", "429"),
    ("limited_demo", "LocalMessage"): ("Claimed", "429"),
    ("limited_demo", "LocalRedirect"): ("Available", "429"),
    ("limited_demo", "LocalRegex"): ("Available", "429"),
    ("limited_demo", "LocalSlow"): ("Available", "429"),
    ("limited_demo", "LocalWaf"): ("Claimed", "429"),
    ("slow_demo", "LocalStatus"): ("Unknown", "?"),
    ("slow_demo", "LocalMessage"): ("Unknown", "?"),
    ("slow_demo", "LocalRedirect"): ("Unknown", "?"),
    ("slow_demo", "LocalRegex"): ("Unknown", "?"),
    ("slow_demo", "LocalSlow"): ("Unknown", "?"),
    ("slow_demo", "LocalWaf"): ("Unknown", "?"),
    ("waf_demo", "LocalWaf"): ("WAF", "403"),
    ("bad name", "LocalRegex"): ("Illegal", ""),
}

actual = {}
for csv_path in sorted(RESULTS.glob("*.csv")):
    with csv_path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            key = (row["username"], row["name"])
            actual[key] = (row["exists"], row["http_status"])

if actual != expected:
    for key in sorted(set(expected) | set(actual)):
        if actual.get(key) != expected.get(key):
            print(f"MISMATCH {key}: expected={expected.get(key)!r} actual={actual.get(key)!r}")
assert actual == expected, "CSV results differ from expected local ground truth"

def single_row(folder: str):
    with (HERE / folder / "slow_demo.csv").open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 1
    return rows[0]

ab_fast = single_row("results-timeout-04")
ab_slow = single_row("results-timeout-2")
assert (ab_fast["exists"], ab_fast["http_status"]) == ("Unknown", "?")
assert (ab_slow["exists"], ab_slow["http_status"]) == ("Claimed", "200")

events = [json.loads(line) for line in (HERE / "request-log.jsonl").read_text(encoding="utf-8").splitlines() if line]
probes = [event for event in events if event["path"] != "/health"]
assert len(probes) == 27, f"Expected 27 local probes, got {len(probes)}"
assert all(event["path"].startswith("/") for event in probes)
assert not any(event["username"] == "bad name" for event in probes), "Illegal username should not trigger HTTP"
assert any(event["method"] == "HEAD" for event in probes), "status_code should use HEAD by default"
assert any(event["method"] == "GET" for event in probes), "message/response_url should use GET"
assert any(event["status"] == 429 for event in probes), "429 fixture missing"

print(f"PASS: {len(actual)} CSV verdicts match local ground truth")
print("PASS: timeout A/B changed slow_demo from Unknown (0.4s) to Claimed (2s)")
print(f"PASS: {len(probes)} probes were emitted only by the loopback fixture")
print("PASS: 429, HEAD/GET, timeout, WAF and zero-request ILLEGAL cases verified")
