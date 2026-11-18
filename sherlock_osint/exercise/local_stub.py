"""Loopback-only HTTP fixture for the Sherlock learning exercise."""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

HOST = "127.0.0.1"
PORT = 8765
LOG_PATH = Path(__file__).with_name("request-log.jsonl")
WAF_BODY = '<html><span id="challenge-error-text">local challenge</span></html>'


class Handler(BaseHTTPRequestHandler):
    server_version = "SherlockLocalFixture/1.0"

    def log_message(self, fmt, *args):
        return

    def do_HEAD(self):
        self.respond(send_body=False)

    def do_GET(self):
        self.respond(send_body=True)

    def respond(self, send_body: bool):
        path = urlsplit(self.path).path
        username = unquote(path.rsplit("/", 1)[-1])
        status = 200
        body = "PROFILE_OK"
        headers = {}

        if path == "/health":
            body = "OK"
        elif username == "missing_demo":
            if path.startswith("/message/"):
                body = "PROFILE_NOT_FOUND"
            elif path.startswith("/redirect/"):
                status = 302
                headers["Location"] = "/login"
                body = "REDIRECT_TO_LOGIN"
            else:
                status = 404
                body = "NOT_FOUND"
        elif username == "limited_demo":
            # Ground truth: this local profile exists, but the fixture throttles it.
            status = 429
            body = "RATE_LIMIT"
            headers["Retry-After"] = "60"
        elif username == "waf_demo":
            status = 403
            body = WAF_BODY
        elif username == "slow_demo":
            time.sleep(1.2)

        event = {
            "time": datetime.now(timezone.utc).isoformat(),
            "method": self.command,
            "path": path,
            "username": username,
            "status": status,
            "user_agent": self.headers.get("User-Agent", ""),
        }
        # Log before writing the response: a timeout client may disconnect early.
        with LOG_PATH.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")

        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()
        if send_body:
            try:
                self.wfile.write(payload)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                pass


if __name__ == "__main__":
    LOG_PATH.write_text("", encoding="utf-8")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"LOOPBACK_ONLY http://{HOST}:{PORT} health=/health", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
