"""End-to-end, credential-free CLIProxyAPI experiment.

Run from any directory:
    python -I F:/reminder/cli_proxy_api/exercise/run_experiment.py

It starts only loopback listeners, uses fake keys, and never calls a real model.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from urllib.error import HTTPError
from urllib.request import Request, urlopen

PROJECT = Path(__file__).resolve().parent.parent
EXERCISE = PROJECT / "exercise"
RUNTIME = EXERCISE / "runtime"
BINARY = EXERCISE / "bin" / "cli-proxy-api.exe"
ARCHIVE = RUNTIME / "download" / "CLIProxyAPI_8.0.47_windows_amd64.zip"
EXPECTED_SHA256 = "8e23cbb2f9f695411b7df46320855820b352fb886c3c3bdf45ab4634f2f14632"
MOCK_PORT = 19001
PROXY_PORT = 19317
CLIENT_KEY = "local-client-key"
LOG_PATH = EXERCISE / "experiment_log.txt"
RESULTS_PATH = EXERCISE / "experiment_results.json"
UPSTREAM_CAPTURE = RUNTIME / "upstream_requests.jsonl"
CONFIG_PATH = RUNTIME / "config.yaml"
MOCK_STDOUT = RUNTIME / "mock_stdout.log"
PROXY_STDOUT = RUNTIME / "proxy_stdout.log"

LOG_LINES: list[str] = []
RESULTS: dict = {
    "schema": "cliproxyapi-local-experiment-v1",
    "started_at": datetime.now(timezone.utc).isoformat(),
    "real_external_model_calls": 0,
    "fake_credentials_only": True,
}


def log(message: str) -> None:
    print(message, flush=True)
    LOG_LINES.append(message)


def command_text(parts: list[str]) -> str:
    return subprocess.list2cmdline([str(part) for part in parts])


def run_command(parts: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    log(f"\n$ {command_text(parts)}")
    completed = subprocess.run(
        parts, cwd=cwd, text=True, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )
    log(completed.stdout.rstrip())
    log(f"[exit_code={completed.returncode}]")
    return completed


def wait_http(url: str, process: subprocess.Popen[str], log_file: Path, attempts: int = 100) -> None:
    last_error = ""
    for _ in range(attempts):
        if process.poll() is not None:
            break
        try:
            with urlopen(url, timeout=0.4) as response:
                response.read()
                return
        except Exception as exc:  # startup polling records the final concrete error
            last_error = f"{type(exc).__name__}: {exc}"
            time.sleep(0.1)
    tail = log_file.read_text(encoding="utf-8", errors="replace")[-6000:] if log_file.exists() else ""
    raise RuntimeError(f"service did not become ready: {url}; {last_error}\n{tail}")


def http_call(method: str, url: str, headers: dict[str, str] | None = None, payload: dict | None = None) -> tuple[int, str]:
    raw = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request_headers = dict(headers or {})
    if raw is not None:
        request_headers["Content-Type"] = "application/json"
    request = Request(url, data=raw, headers=request_headers, method=method)
    try:
        with urlopen(request, timeout=20) as response:
            return response.status, response.read().decode("utf-8")
    except HTTPError as exc:
        return exc.code, exc.read().decode("utf-8")


def config(strategy: str) -> str:
    return f"""config-version: 8
server:
  host: "127.0.0.1"
  port: {PROXY_PORT}
  response-compression:
    enabled: false
management:
  allow-remote: false
  secret-key: ""
  disable-control-panel: true
access:
  api-keys:
    - "{CLIENT_KEY}"
oauth:
  auth-dir: "auths"
routing:
  strategy: "{strategy}"
  retry:
    request-retry: 0
    max-retry-credentials: 0
    max-retry-interval: 0
requests:
  proxy-url: "direct"
api-keys:
  openai-compatibility:
    - name: "local-mock"
      base-url: "http://127.0.0.1:{MOCK_PORT}/v1"
      keys:
        - api-key: "upstream-A"
        - api-key: "upstream-B"
      models:
        - name: "mock-model"
          alias: "demo-alias"
          display-name: "Local deterministic mock"
          input-modalities: [text]
          output-modalities: [text]
observability:
  logs:
    debug: false
    logging-to-file: false
    request-log: false
  usage:
    usage-statistics-enabled: false
"""


def start_proxy(strategy: str, log_handle) -> subprocess.Popen[str]:
    CONFIG_PATH.write_text(config(strategy), encoding="utf-8")
    parts = [str(BINARY), "--config", str(CONFIG_PATH), "--local-model"]
    log(f"\n$ (working_directory={RUNTIME}) {command_text(parts)}")
    process = subprocess.Popen(
        parts, cwd=RUNTIME, stdout=log_handle, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace",
    )
    wait_http(f"http://127.0.0.1:{PROXY_PORT}/", process, PROXY_STDOUT)
    log(f"PROXY_READY strategy={strategy} url=http://127.0.0.1:{PROXY_PORT}")
    return process


def stop_process(process: subprocess.Popen[str], name: str) -> None:
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
    log(f"{name}_STOPPED exit_code={process.returncode}")


def record_call(name: str, method: str, path: str, headers: dict[str, str], payload: dict | None = None) -> tuple[int, dict | str]:
    url = f"http://127.0.0.1:{PROXY_PORT}{path}"
    printable = {"method": method, "url": url, "headers": headers, "json": payload}
    log(f"\nCLIENT_REQUEST {name}\n{json.dumps(printable, ensure_ascii=False, indent=2)}")
    status, body = http_call(method, url, headers, payload)
    log(f"CLIENT_RESPONSE {name} status={status}\n{body}")
    try:
        parsed: dict | str = json.loads(body)
    except json.JSONDecodeError:
        parsed = body
    RESULTS[name] = {"status": status, "response": parsed}
    return status, parsed


def main() -> None:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    (RUNTIME / "auths").mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text("", encoding="utf-8")
    RESULTS["environment"] = {
        "platform": platform.platform(),
        "python": sys.version,
        "proxy_port": PROXY_PORT,
        "mock_port": MOCK_PORT,
        "listeners": "127.0.0.1 only",
    }
    log("CLIProxyAPI local experiment: no real provider account, no external model call")
    log(f"Python: {sys.version.split()[0]}; platform: {platform.platform()}")

    digest = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
    RESULTS["release"] = {"version": "8.0.47", "archive": ARCHIVE.name, "sha256": digest,
                          "matches_github_release_digest": digest == EXPECTED_SHA256}
    log(f"RELEASE_SHA256 {digest} matches={digest == EXPECTED_SHA256}")
    assert digest == EXPECTED_SHA256

    version = run_command([str(BINARY), "--help"])
    assert version.returncode == 0 and "Version: 8.0.47" in version.stdout

    mock_log_handle = MOCK_STDOUT.open("w", encoding="utf-8")
    proxy_log_handle = PROXY_STDOUT.open("w", encoding="utf-8")
    mock = None
    proxy = None
    try:
        mock_parts = [sys.executable, "-I", str(EXERCISE / "mock_upstream.py"),
                      "--port", str(MOCK_PORT), "--log", str(UPSTREAM_CAPTURE)]
        log(f"\n$ {command_text(mock_parts)}")
        mock = subprocess.Popen(mock_parts, cwd=RUNTIME, stdout=mock_log_handle,
                                stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
        wait_http(f"http://127.0.0.1:{MOCK_PORT}/health", mock, MOCK_STDOUT)
        log(f"MOCK_READY http://127.0.0.1:{MOCK_PORT}/health")

        proxy = start_proxy("round-robin", proxy_log_handle)
        status, unauth = record_call("unauthorized_models", "GET", "/v1/models", {})
        assert status == 401, (status, unauth)

        auth = {"Authorization": f"Bearer {CLIENT_KEY}"}
        status, models = record_call("authorized_models", "GET", "/v1/models", auth)
        assert status == 200 and isinstance(models, dict)
        matching = [item for item in models.get("data", []) if item.get("id") == "demo-alias"]
        assert matching, "demo-alias missing from model catalog"
        RESULTS["authorized_models"]["matching_model"] = matching
        log("AUTHORIZED_MODEL_MATCH " + json.dumps(matching, ensure_ascii=False))

        claude_payload = {
            "model": "demo-alias", "max_tokens": 64,
            "system": "你是协议演示助手",
            "messages": [{"role": "user", "content": [{"type": "text", "text": "Claude 口径进，OpenAI 口径出"}]}],
            "stream": False,
        }
        status, claude = record_call(
            "claude_to_openai", "POST", "/v1/messages",
            {"x-api-key": CLIENT_KEY, "anthropic-version": "2023-06-01"}, claude_payload,
        )
        assert status == 200 and isinstance(claude, dict) and claude.get("type") == "message"
        assert claude["content"][0]["type"] == "text" and "mock-A" in claude["content"][0]["text"]

        openai_texts = []
        for index in range(2):
            status, response = record_call(
                f"round_robin_chat_{index + 1}", "POST", "/v1/chat/completions", auth,
                {"model": "demo-alias", "messages": [{"role": "user", "content": f"round-{index + 1}"}], "stream": False},
            )
            assert status == 200
            openai_texts.append(response["choices"][0]["message"]["content"])
        assert "mock-B" in openai_texts[0] and "mock-A" in openai_texts[1], openai_texts
        RESULTS["round_robin_observation"] = [claude["content"][0]["text"], *openai_texts]

        status, stream_body = record_call(
            "claude_stream", "POST", "/v1/messages",
            {"x-api-key": CLIENT_KEY, "anthropic-version": "2023-06-01"},
            {"model": "demo-alias", "max_tokens": 64, "stream": True,
             "messages": [{"role": "user", "content": "流式事件也要翻译"}]},
        )
        assert status == 200 and isinstance(stream_body, str)
        for event in ("message_start", "content_block_delta", "message_delta", "message_stop"):
            assert event in stream_body, f"missing Claude SSE event {event}"
        assert "mock-B" in stream_body

        stop_process(proxy, "PROXY_ROUND_ROBIN")
        proxy = start_proxy("fill-first", proxy_log_handle)
        fill_texts = []
        for index in range(2):
            status, response = record_call(
                f"fill_first_chat_{index + 1}", "POST", "/v1/chat/completions", auth,
                {"model": "demo-alias", "messages": [{"role": "user", "content": f"fill-{index + 1}"}], "stream": False},
            )
            assert status == 200
            fill_texts.append(response["choices"][0]["message"]["content"])
        assert all("mock-A" in text for text in fill_texts), fill_texts
        RESULTS["fill_first_observation"] = fill_texts

        captures = [json.loads(line) for line in UPSTREAM_CAPTURE.read_text(encoding="utf-8").splitlines() if line.strip()]
        RESULTS["upstream_summary"] = [
            {"sequence": item["sequence"], "account": item["account"], "model": item["payload"].get("model"),
             "stream": item["payload"].get("stream"), "roles": [m.get("role") for m in item["payload"].get("messages", [])]}
            for item in captures
        ]
        first = captures[0]["payload"]
        assert first["model"] == "mock-model"
        assert first["max_tokens"] == 64
        assert [m["role"] for m in first["messages"]] == ["system", "user"]
        assert first["messages"][1]["content"][0]["text"] == "Claude 口径进，OpenAI 口径出"
        assert len(captures) == 6
        RESULTS["assertions"] = {
            "release_sha256_verified": True,
            "client_auth_401_then_200": True,
            "alias_mapped_to_upstream_model": True,
            "claude_system_and_user_translated": True,
            "claude_nonstream_response_translated": True,
            "claude_sse_lifecycle_observed": True,
            "round_robin_A_B_A_B_observed": True,
            "fill_first_A_A_observed_after_restart": True,
            "upstream_request_count": len(captures),
        }
        RESULTS["success"] = True
        log("\nALL_ASSERTIONS_PASSED " + json.dumps(RESULTS["assertions"], ensure_ascii=False))
    except Exception as exc:
        RESULTS["success"] = False
        RESULTS["error"] = f"{type(exc).__name__}: {exc}"
        log(f"EXPERIMENT_FAILED {type(exc).__name__}: {exc}")
        raise
    finally:
        if proxy is not None:
            stop_process(proxy, "PROXY_FINAL")
        if mock is not None:
            stop_process(mock, "MOCK")
        mock_log_handle.close()
        proxy_log_handle.close()
        RESULTS["finished_at"] = datetime.now(timezone.utc).isoformat()
        RESULTS_PATH.write_text(json.dumps(RESULTS, ensure_ascii=False, indent=2), encoding="utf-8")
        LOG_PATH.write_text("\n".join(LOG_LINES) + "\n", encoding="utf-8")
        print(f"LOG={LOG_PATH}\nRESULTS={RESULTS_PATH}", flush=True)


if __name__ == "__main__":
    main()
