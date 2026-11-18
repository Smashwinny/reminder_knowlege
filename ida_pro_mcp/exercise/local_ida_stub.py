"""本地、只读、限制输入的 IDA/MCP 教学桩。

它不是 IDA，不调用 idalib，也不提供反编译。输入仅限实验运行器生成的自编译
二进制、Objdump 文本和固定查询脚本；execute_python 只接受该脚本的精确哈希。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

FUNCTION_RE = re.compile(r"^([0-9a-fA-F]+)\s+<([^>]+)>:\s*$")
INSTRUCTION_RE = re.compile(r"^\s*([0-9a-fA-F]+):\s+(.*\S)\s*$")
CALL_RE = re.compile(r"\bcall\s+([0-9a-fA-F]+)\s+<([^>]+)>")


@dataclass
class Instruction:
    ea: int
    text: str


@dataclass
class Function:
    start_ea: int
    end_ea: int
    name: str
    instructions: list[Instruction]


@dataclass
class XRefType:
    name: str


@dataclass
class XRef:
    from_ea: int
    to_ea: int
    type: XRefType


class FunctionsAPI:
    def __init__(self, functions: list[Function]):
        self._functions = functions

    def get_all(self):
        return iter(self._functions)

    def __iter__(self):
        return iter(self._functions)

    def get_name(self, func: Function) -> str:
        return func.name

    def get_at(self, ea: int) -> Function | None:
        return next((f for f in self._functions if f.start_ea <= ea < f.end_ea), None)

    def get_disassembly(self, func: Function) -> list[str]:
        return [f"{ins.ea:x}: {ins.text}" for ins in func.instructions]


class InstructionsAPI:
    def __init__(self, functions: list[Function]):
        self._instructions = {
            ins.ea: ins for func in functions for ins in func.instructions
        }

    def get_at(self, ea: int) -> Instruction | None:
        return self._instructions.get(ea)

    def get_disassembly(self, instruction: Instruction | None) -> str | None:
        return instruction.text if instruction else None


class XRefsAPI:
    def __init__(self, xrefs: list[XRef]):
        self._xrefs = xrefs

    def calls_to_ea(self, ea: int):
        return (
            xref
            for xref in self._xrefs
            if xref.to_ea == ea and xref.type.name == "CALL"
        )

    def to_ea(self, ea: int):
        return (xref for xref in self._xrefs if xref.to_ea == ea)

    def from_ea(self, ea: int):
        return (xref for xref in self._xrefs if xref.from_ea == ea)


class LocalDatabase:
    def __init__(self, binary: Path, functions: list[Function], xrefs: list[XRef]):
        self.binary = binary
        self.sha256 = hashlib.sha256(binary.read_bytes()).hexdigest()
        self.functions = FunctionsAPI(functions)
        self.instructions = InstructionsAPI(functions)
        self.xrefs = XRefsAPI(xrefs)


def parse_objdump(text: str) -> tuple[list[Function], list[XRef]]:
    labels: list[tuple[int, str]] = []
    bodies: dict[int, list[Instruction]] = {}
    current: int | None = None
    for line in text.splitlines():
        label = FUNCTION_RE.match(line)
        if label:
            current = int(label.group(1), 16)
            labels.append((current, label.group(2)))
            bodies[current] = []
            continue
        instruction = INSTRUCTION_RE.match(line)
        if instruction and current is not None:
            bodies[current].append(
                Instruction(int(instruction.group(1), 16), instruction.group(2))
            )

    labels.sort()
    functions = []
    for index, (start, name) in enumerate(labels):
        instructions = bodies[start]
        if not instructions:
            continue
        end = labels[index + 1][0] if index + 1 < len(labels) else instructions[-1].ea + 1
        # 32 位 MinGW 给 C 符号加前导下划线；只归一化本实验自有函数。
        if name.startswith("_") and name[1:] in {"mix", "check", "authorize", "main"}:
            name = name[1:]
        functions.append(Function(start, end, name, instructions))
    by_address = {func.start_ea: func for func in functions}
    xrefs = []
    for func in functions:
        for instruction in func.instructions:
            call = CALL_RE.search(instruction.text)
            if not call:
                continue
            target = int(call.group(1), 16)
            if target in by_address:
                xrefs.append(XRef(instruction.ea, target, XRefType("CALL")))
    return functions, xrefs


TOOL_NAMES = [
    "open_database",
    "execute_python",
    "reference",
    "list_databases",
    "save_database",
    "close_database",
]
SAFE_BUILTINS = {
    "all": all,
    "dict": dict,
    "hex": hex,
    "len": len,
    "list": list,
    "set": set,
    "sorted": sorted,
    "str": str,
    "tuple": tuple,
}


class StubServer:
    def __init__(self, args: argparse.Namespace):
        self.binary = args.binary.resolve()
        self.disassembly = args.disassembly.resolve()
        self.query_path = args.query.resolve()
        self.query_bytes = self.query_path.read_bytes()
        self.query_hash = hashlib.sha256(self.query_bytes).hexdigest()
        self.trace_path = args.trace.resolve()
        self.db: LocalDatabase | None = None
        self.closed = False

    def trace(self, event: str, **fields: Any) -> None:
        record = {
            "schema": 1,
            "ts": datetime.now(UTC).isoformat(),
            "event": event,
            **fields,
        }
        with self.trace_path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")

    def tools_list(self) -> dict[str, Any]:
        schemas = {
            "open_database": {"path": {"type": "string"}},
            "execute_python": {"code": {"type": "string"}},
            "reference": {"query": {"type": "string"}},
            "list_databases": {},
            "save_database": {},
            "close_database": {},
        }
        return {
            "tools": [
                {
                    "name": name,
                    "description": f"LOCAL STUB ONLY: {name}; no IDA or decompiler is invoked.",
                    "inputSchema": {
                        "type": "object",
                        "properties": schemas[name],
                        "required": list(schemas[name]),
                        "additionalProperties": True,
                    },
                }
                for name in TOOL_NAMES
            ]
        }

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name == "open_database":
            supplied = Path(arguments["path"]).resolve()
            if supplied != self.binary:
                raise ValueError("本地桩只允许打开本次自编译二进制")
            functions, xrefs = parse_objdump(self.disassembly.read_text(encoding="utf-8"))
            self.db = LocalDatabase(self.binary, functions, xrefs)
            self.closed = False
            return {
                "instance_id": "local-stub-1",
                "backend": "local-objdump-stub",
                "status": "current",
                "recovery": "none",
                "log_path": str(self.trace_path),
                "mcp_id": None,
                "hint": "LOCAL STUB ONLY: call reference, then execute the fixed query script.",
            }
        if name == "list_databases":
            return {
                "instances": [
                    {
                        "path": str(self.binary),
                        "backend": "local-objdump-stub",
                        "status": "current" if self.db and not self.closed else "available",
                        "instance_id": "local-stub-1" if self.db and not self.closed else None,
                        "error": None,
                    }
                ],
                "hint": "This is a local stub, not IDA database discovery.",
            }
        if name == "reference":
            query = arguments["query"].lower()
            if not any(word in query for word in ("function", "xref", "call", "disassembl")):
                raise ValueError("教学桩只提供 function/xref/call/disassembly 参考")
            return {
                "result": (
                    "Official ida-domain shapes (documentation-derived): "
                    "db.functions.get_all(); db.functions.get_at(ea); "
                    "db.functions.get_name(func); db.xrefs.calls_to_ea(ea); "
                    "db.instructions.get_at(ea); db.instructions.get_disassembly(insn). "
                    "The local stub implements only this read-only subset."
                ),
                "source": "https://github.com/HexRaysSA/ida-domain/blob/main/docs/migration-guide.md",
            }
        if name == "execute_python":
            if self.db is None or self.closed:
                raise ValueError("请先 open_database")
            code = arguments["code"].encode("utf-8")
            if hashlib.sha256(code).hexdigest() != self.query_hash:
                raise ValueError("安全教学桩拒绝固定查询脚本以外的代码")
            namespace: dict[str, Any] = {"__builtins__": SAFE_BUILTINS}
            exec(compile(self.query_bytes, str(self.query_path), "exec"), namespace)
            result = namespace["run"](self.db)
            return {"result": result, "stdout": "", "stderr": ""}
        if name == "save_database":
            raise ValueError("只读教学桩不支持保存数据库")
        if name == "close_database":
            if self.db is None:
                return {"closed": False, "final_lease": False, "idb_path": ""}
            self.closed = True
            return {
                "closed": True,
                "final_lease": True,
                "idb_path": "LOCAL_STUB_NO_IDB",
            }
        raise ValueError(f"未知工具: {name}")

    def handle(self, request: dict[str, Any]) -> dict[str, Any] | None:
        method = request.get("method")
        request_id = request.get("id")
        if method == "notifications/initialized":
            return None
        if request_id is None:
            return None
        response: dict[str, Any] = {"jsonrpc": "2.0", "id": request_id}
        try:
            if method == "initialize":
                response["result"] = {
                    "protocolVersion": request["params"]["protocolVersion"],
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "local-ida-stub", "version": "1.0.0"},
                    "instructions": "LOCAL STUB ONLY; no IDA/idalib/decompiler; fixed local inputs only.",
                }
            elif method == "tools/list":
                response["result"] = self.tools_list()
            elif method == "tools/call":
                params = request["params"]
                name = params["name"]
                arguments = params.get("arguments") or {}
                self.trace("tool_call", call_id=str(request_id), tool=name, input=arguments)
                result = self.call_tool(name, arguments)
                self.trace("tool_result", call_id=str(request_id), tool=name, output=result)
                text = json.dumps(result, ensure_ascii=False)
                response["result"] = {
                    "content": [{"type": "text", "text": text}],
                    "structuredContent": {"result": result},
                    "isError": False,
                }
            else:
                raise ValueError(f"不支持的方法: {method}")
        except Exception as error:
            self.trace(
                "tool_error",
                call_id=str(request_id),
                error={"type": type(error).__name__, "message": str(error)},
            )
            response["error"] = {"code": -32602, "message": str(error)}
        return response

    def serve(self) -> int:
        for line in sys.stdin.buffer:
            request = json.loads(line.decode("utf-8"))
            response = self.handle(request)
            if response is not None:
                encoded = json.dumps(response, ensure_ascii=False) + "\n"
                sys.stdout.buffer.write(encoded.encode("utf-8"))
                sys.stdout.buffer.flush()
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--disassembly", type=Path, required=True)
    parser.add_argument("--query", type=Path, required=True)
    parser.add_argument("--trace", type=Path, required=True)
    args = parser.parse_args()
    args.trace.write_text("", encoding="utf-8")
    return StubServer(args).serve()


if __name__ == "__main__":
    raise SystemExit(main())
