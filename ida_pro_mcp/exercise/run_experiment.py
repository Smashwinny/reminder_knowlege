"""一键重放：自编译 → Objdump → 本地 MCP 桩 → 调用图与结论回溯。"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
BINARY = ROOT / ("demo.exe" if os.name == "nt" else "demo")
DISASSEMBLY = ROOT / "disassembly.txt"
QUERY = ROOT / "ida_queries.py"
STUB = ROOT / "local_ida_stub.py"
TRACE = ROOT / "mcp_trace.jsonl"
RESULT = ROOT / "analysis_result.json"


def run(
    command: list[str], *, allow_exit: int = 0, echo_output: bool = True
) -> subprocess.CompletedProcess[str]:
    print("$ " + " ".join(command), flush=True)
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    if echo_output and completed.stdout:
        print(completed.stdout.rstrip(), flush=True)
    if echo_output and completed.stderr:
        print(completed.stderr.rstrip(), flush=True)
    print(f"exit={completed.returncode}", flush=True)
    if completed.returncode != allow_exit:
        raise RuntimeError(f"命令退出码异常: {completed.returncode}")
    return completed


class Utf8Tee:
    """终端原样显示，同时把实验证据稳定写成 UTF-8。"""

    def __init__(self, terminal, log_path: Path):
        self.terminal = terminal
        self.log = log_path.open("w", encoding="utf-8", newline="\n")

    def write(self, text: str) -> int:
        self.terminal.write(text)
        self.log.write(text)
        self.log.flush()
        return len(text)

    def flush(self) -> None:
        self.terminal.flush()
        self.log.flush()


class McpClient:
    def __init__(self) -> None:
        command = [
            sys.executable,
            "-I",
            str(STUB),
            "--binary",
            str(BINARY),
            "--disassembly",
            str(DISASSEMBLY),
            "--query",
            str(QUERY),
            "--trace",
            str(TRACE),
        ]
        print("$ " + " ".join(command) + "  # stdio MCP 子进程", flush=True)
        self.process = subprocess.Popen(
            command,
            cwd=ROOT,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            bufsize=1,
        )
        self.next_id = 1

    def request(self, method: str, params: dict | None = None) -> dict:
        request_id = self.next_id
        self.next_id += 1
        message = {"jsonrpc": "2.0", "id": request_id, "method": method}
        if params is not None:
            message["params"] = params
        assert self.process.stdin and self.process.stdout
        self.process.stdin.write(json.dumps(message, ensure_ascii=False) + "\n")
        self.process.stdin.flush()
        line = self.process.stdout.readline()
        if not line:
            raise RuntimeError("MCP 桩提前退出")
        response = json.loads(line)
        if "error" in response:
            raise RuntimeError(response["error"])
        print(f"MCP {method} id={request_id}: OK", flush=True)
        return response["result"]

    def notify(self, method: str) -> None:
        assert self.process.stdin
        self.process.stdin.write(json.dumps({"jsonrpc": "2.0", "method": method}) + "\n")
        self.process.stdin.flush()

    def call(self, name: str, arguments: dict | None = None) -> dict:
        result = self.request(
            "tools/call", {"name": name, "arguments": arguments or {}}
        )
        return result["structuredContent"]["result"]

    def close(self) -> None:
        assert self.process.stdin
        self.process.stdin.close()
        exit_code = self.process.wait(timeout=10)
        stderr = self.process.stderr.read() if self.process.stderr else ""
        if stderr:
            print(stderr.rstrip(), flush=True)
        if exit_code != 0:
            raise RuntimeError(f"MCP 桩退出码异常: {exit_code}")
        print(f"MCP stdio EOF: exit={exit_code}", flush=True)


def main() -> int:
    print("LOCAL_STUB_ONLY：不调用 IDA、idalib、Hex-Rays 反编译器或未知二进制。", flush=True)
    print(f"Python: {sys.version.split()[0]}; platform: {sys.platform}", flush=True)
    run(["gcc", "--version"])
    run(["objdump", "--version"])
    run(
        [
            "gcc",
            "-O0",
            "-g",
            "-fno-inline",
            "-fno-omit-frame-pointer",
            str(ROOT / "demo.c"),
            "-o",
            str(BINARY),
        ]
    )
    binary_hash = hashlib.sha256(BINARY.read_bytes()).hexdigest()
    print(f"SELF_COMPILED_SHA256={binary_hash}", flush=True)
    run([str(BINARY), "7"])
    run([str(BINARY), "27"], allow_exit=2)
    disassembly = run(
        ["objdump", "-d", "--no-show-raw-insn", str(BINARY)], echo_output=False
    ).stdout
    DISASSEMBLY.write_text(disassembly, encoding="utf-8", newline="\n")
    print(f"OBJDUMP_SAVED={DISASSEMBLY.name}; lines={len(disassembly.splitlines())}", flush=True)

    client = McpClient()
    try:
        client.request(
            "initialize",
            {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "local-learning-client", "version": "1.0"},
            },
        )
        client.notify("notifications/initialized")
        tools = client.request("tools/list")["tools"]
        names = [tool["name"] for tool in tools]
        expected = [
            "open_database",
            "execute_python",
            "reference",
            "list_databases",
            "save_database",
            "close_database",
        ]
        assert names == expected, names
        print("TOOLS=" + ",".join(names), flush=True)
        client.call("list_databases")
        opened = client.call("open_database", {"path": str(BINARY)})
        assert opened["backend"] == "local-objdump-stub"
        client.call("reference", {"query": "functions xrefs calls disassembly"})
        query_code = QUERY.read_bytes().decode("utf-8")
        execution = client.call("execute_python", {"code": query_code, "timeout": 30})
        analysis = execution["result"]
        assert analysis["input_sha256"] == binary_hash
        assert analysis["conclusion"]["supported"] is True
        expected_edges = {
            ("main", "authorize"),
            ("authorize", "check"),
            ("authorize", "mix"),
            ("check", "mix"),
        }
        evidence_edges = {
            (item["from"], item["to"])
            for item in analysis["conclusion"]["evidence"]
        }
        assert evidence_edges == expected_edges, evidence_edges
        assert len(analysis["conclusion"]["evidence"]) == 4
        for item in analysis["conclusion"]["evidence"]:
            assert item["instruction"] and "call" in item["instruction"]
            print(
                "EVIDENCE "
                + f"{item['from']}->{item['to']} @ {item['call_ea']}: {item['instruction']}",
                flush=True,
            )
        RESULT.write_text(
            json.dumps(analysis, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        client.call("close_database")
    finally:
        client.close()

    records = [json.loads(line) for line in TRACE.read_text(encoding="utf-8").splitlines()]
    call_ids = {r["call_id"] for r in records if r["event"] == "tool_call"}
    result_ids = {r["call_id"] for r in records if r["event"] == "tool_result"}
    assert call_ids == result_ids
    assert not [r for r in records if r["event"] == "tool_error"]
    print(
        f"PASS: 6 工具发现；4/4 预期直接调用边有地址证据；{len(call_ids)} 次工具调用均有结果追踪。",
        flush=True,
    )
    print("LIMIT: 仅本地桩和 Objdump 实测；未验证 IDA 实机、反编译、自动分析或 Nexus 租约。", flush=True)
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    tee = Utf8Tee(sys.stdout, ROOT / "experiment_log.txt")
    sys.stdout = tee
    sys.stderr = tee
    raise SystemExit(main())
