"""Deterministic local OpenAI-compatible upstream for CLIProxyAPI experiments.

Only stdlib is used. The two credentials are fake test labels, not real secrets.
"""
from __future__ import annotations

import argparse
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class MockState:
    def __init__(self, log_path: Path) -> None:
        self.log_path = log_path
        self.lock = threading.Lock()
        self.counter = 0

    def record(self, path: str, authorization: str, payload: dict) -> tuple[int, str]:
        with self.lock:
            self.counter += 1
            sequence = self.counter
            account = "A" if authorization == "Bearer upstream-A" else (
                "B" if authorization == "Bearer upstream-B" else "UNKNOWN"
            )
            entry = {
                "sequence": sequence,
                "path": path,
                "authorization": authorization,
                "account": account,
                "payload": payload,
            }
            with self.log_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
            return sequence, account


class MockHandler(BaseHTTPRequestHandler):
    server_version = "LocalMockUpstream/1.0"

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"[mock] {self.client_address[0]} {fmt % args}", flush=True)

    def do_GET(self) -> None:  # noqa: N802 - stdlib HTTP handler API
        if self.path == "/health":
            self.send_json(200, {"status": "ok", "server": "local-mock"})
            return
        self.send_json(404, {"error": {"message": "not found"}})

    def do_POST(self) -> None:  # noqa: N802 - stdlib HTTP handler API
        if self.path != "/v1/chat/completions":
            self.send_json(404, {"error": {"message": f"unexpected path: {self.path}"}})
            return
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length).decode("utf-8"))
        sequence, account = self.server.state.record(  # type: ignore[attr-defined]
            self.path, self.headers.get("Authorization", ""), payload
        )
        user_texts = [
            part.get("text", "") if isinstance(part, dict) else str(part)
            for message in payload.get("messages", [])
            if message.get("role") == "user"
            for part in (message.get("content", []) if isinstance(message.get("content"), list) else [message.get("content", "")])
        ]
        text = f"mock-{account} 已收到: {' | '.join(user_texts)}"
        response_id = f"chatcmpl-local-{sequence:03d}"
        created = 1_760_000_000 + sequence
        model = payload.get("model", "mock-model")
        if payload.get("stream"):
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "close")
            self.end_headers()
            chunks = [
                {"id": response_id, "object": "chat.completion.chunk", "created": created, "model": model,
                 "choices": [{"index": 0, "delta": {"role": "assistant", "content": ""}, "finish_reason": None}]},
                {"id": response_id, "object": "chat.completion.chunk", "created": created, "model": model,
                 "choices": [{"index": 0, "delta": {"content": text}, "finish_reason": None}]},
                {"id": response_id, "object": "chat.completion.chunk", "created": created, "model": model,
                 "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
                 "usage": {"prompt_tokens": 11, "completion_tokens": 7, "total_tokens": 18}},
            ]
            for chunk in chunks:
                self.wfile.write(("data: " + json.dumps(chunk, ensure_ascii=False) + "\n\n").encode("utf-8"))
                self.wfile.flush()
            self.wfile.write(b"data: [DONE]\n\n")
            self.wfile.flush()
            self.close_connection = True
            return
        self.send_json(200, {
            "id": response_id,
            "object": "chat.completion",
            "created": created,
            "model": model,
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": text},
                "finish_reason": "stop",
            }],
            "usage": {"prompt_tokens": 11, "completion_tokens": 7, "total_tokens": 18},
        })

    def send_json(self, status: int, payload: dict) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=19001)
    parser.add_argument("--log", type=Path, required=True)
    args = parser.parse_args()
    args.log.parent.mkdir(parents=True, exist_ok=True)
    args.log.write_text("", encoding="utf-8")
    server = ThreadingHTTPServer(("127.0.0.1", args.port), MockHandler)
    server.state = MockState(args.log)  # type: ignore[attr-defined]
    print(f"MOCK_READY http://127.0.0.1:{args.port}/health log={args.log}", flush=True)
    try:
        server.serve_forever(poll_interval=0.1)
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
