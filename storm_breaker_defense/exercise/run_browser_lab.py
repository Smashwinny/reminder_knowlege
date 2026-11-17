#!/usr/bin/env python3
"""Run a loopback-only Edge defensive lab with synthetic media/geolocation APIs."""
from __future__ import annotations

import datetime as dt
import functools
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = Path(__file__).resolve().parent


def find_edge() -> Path:
    candidates = [
        Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Microsoft/Edge/Application/msedge.exe",
        Path(os.environ.get("PROGRAMFILES", "")) / "Microsoft/Edge/Application/msedge.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft/Edge/Application/msedge.exe",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    discovered = shutil.which("msedge")
    if discovered:
        return Path(discovered)
    raise SystemExit("Microsoft Edge not found; browser lab did not run")


def main() -> int:
    edge = find_edge()
    requests_seen = []

    class Handler(SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'none'; img-src 'self' data:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
            self.send_header("Cache-Control", "no-store")
            super().end_headers()

        def do_GET(self):
            requests_seen.append({"method": "GET", "path": self.path, "client": self.client_address[0]})
            if self.path == "/favicon.ico":
                self.send_response(204)
                self.end_headers()
                return
            super().do_GET()

        def do_POST(self):
            requests_seen.append({"method": "POST", "path": self.path, "client": self.client_address[0]})
            self.send_response(403)
            self.end_headers()

        def log_message(self, fmt, *args):
            return

    handler = functools.partial(Handler, directory=str(HERE))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}/lab_page.html"
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    try:
        with tempfile.TemporaryDirectory(prefix="edge-defense-", dir=HERE) as profile:
            command = [
                str(edge), "--headless", "--disable-gpu", "--no-first-run",
                "--no-default-browser-check", "--dump-dom", "--virtual-time-budget=5000",
                f"--user-data-dir={profile}", url,
            ]
            completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    (HERE / "browser-stdout.txt").write_text(completed.stdout, encoding="utf-8")
    (HERE / "browser-stderr.txt").write_text(completed.stderr, encoding="utf-8")
    (HERE / "browser-dom.html").write_text(completed.stdout, encoding="utf-8")
    match = re.search(r'<pre id="results">(.*?)</pre>', completed.stdout, re.DOTALL)
    if not match:
        print("BROWSER_LAB FAIL: results element not found")
        print(f"edge_exit={completed.returncode}; see browser-stderr.txt")
        return 1
    result = json.loads(html.unescape(match.group(1)))
    result["run"] = {
        "started_at": started,
        "finished_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "edge_path": str(edge),
        "edge_exit_code": completed.returncode,
        "url": url,
        "command_redacted_profile": [str(edge), "--headless", "--disable-gpu", "--no-first-run", "--no-default-browser-check", "--dump-dom", "--virtual-time-budget=5000", "--user-data-dir=<temporary-local-profile>", url],
        "loopback_requests": requests_seen,
        "upstream_executed": False,
    }
    (HERE / "browser-results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    checks = {
        "edge_exit_zero": completed.returncode == 0,
        "script_done": result.get("status") == "DONE",
        "loopback_secure_context": result.get("secure_context", {}).get("isSecureContext") is True and result.get("secure_context", {}).get("loopback") is True,
        "synthetic_denial": result.get("media_denial", {}).get("passed") is True,
        "track_stopped": result.get("track_cleanup", {}).get("passed") is True,
        "synthetic_geolocation_only": result.get("geolocation_guard", {}).get("passed") is True,
        "csp_blocked_canary": result.get("csp_network_guard", {}).get("passed") is True,
        "canary_never_reached_server": not any(item["path"].startswith("/should-not-run") for item in requests_seen),
        "loopback_clients_only": all(item["client"] == "127.0.0.1" for item in requests_seen),
    }
    print(f"BROWSER_LAB status={result.get('status')} edge_exit={completed.returncode}")
    print(f"secure_context={result.get('secure_context', {})}")
    print(f"permission_queries={result.get('permission_queries', {})}")
    for name, passed in checks.items():
        print(f"{name}={'PASS' if passed else 'FAIL'}")
    print(f"loopback_requests={requests_seen}")
    print(f"output={(HERE / 'browser-results.json').resolve()}")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
