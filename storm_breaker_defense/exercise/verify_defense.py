#!/usr/bin/env python3
"""Deterministically verify static and browser evidence from the defensive lab."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
import socket
import urllib.parse

HERE = Path(__file__).resolve().parent


def main() -> int:
    static = json.loads((HERE / "static-audit.json").read_text(encoding="utf-8"))
    browser = json.loads((HERE / "browser-results.json").read_text(encoding="utf-8"))
    lab_port = urllib.parse.urlsplit(browser["run"]["url"]).port
    with socket.socket() as probe:
        probe.settimeout(1)
        server_still_open = probe.connect_ex(("127.0.0.1", lab_port)) == 0
    checks = {
        "static_commit_pinned": len(static["commit"]) == 40,
        "static_all_indicator_classes_present": not static["missing_expected_categories"],
        "upstream_never_executed": static["safety"]["upstream_code_executed"] is False and browser["run"]["upstream_executed"] is False,
        "no_real_sensor_or_location": browser["safety"]["real_sensor_access"] is False and browser["safety"]["real_geolocation_access"] is False,
        "loopback_secure_context": browser["secure_context"]["isSecureContext"] and browser["secure_context"]["loopback"],
        "denial_branch_understood": browser["media_denial"]["passed"],
        "cleanup_stops_track": browser["track_cleanup"]["passed"],
        "network_canary_blocked": browser["csp_network_guard"]["passed"] and not any(x["path"].startswith("/should-not-run") for x in browser["run"]["loopback_requests"]),
        "only_loopback_clients": all(x["client"] == "127.0.0.1" for x in browser["run"]["loopback_requests"]),
        "local_server_stopped": not server_still_open,
        "temporary_browser_profiles_removed": not any(HERE.glob("edge-defense-*")),
    }
    result = {
        "schema": "storm-breaker-defense-verification-v1",
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "all_passed": all(checks.values()),
        "limits": [
            "Permissions API queries were real browser calls but did not open prompts or grant access.",
            "Media and geolocation success/denial branches used explicit synthetic mocks, not hardware.",
            "No upstream PHP/Python server, tunnel, collector, lure, or third-party target was run.",
            "This is a local mechanism demonstration, not a cross-browser or enterprise detection certification."
        ]
    }
    (HERE / "verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    for name, passed in checks.items():
        print(f"{name}={'PASS' if passed else 'FAIL'}")
    print(f"RESULT={result['passed']}/{result['total']} PASS")
    return 0 if result["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
