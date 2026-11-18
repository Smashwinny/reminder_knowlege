"""IDA Domain 风格查询：同一代码可交给官方 execute_python，也可在本地桩运行。

本次只实际验证了本地桩；IDA/idalib 实机执行尚未验证。
"""

OWN_NAMES = ("mix", "check", "authorize", "main")
REQUIRED_EDGES = (
    ("main", "authorize"),
    ("authorize", "check"),
    ("authorize", "mix"),
    ("check", "mix"),
)


def run(db):
    functions = [
        func
        for func in db.functions.get_all()
        if db.functions.get_name(func) in OWN_NAMES
    ]
    by_name = {db.functions.get_name(func): func for func in functions}

    calls = []
    for target in functions:
        target_name = db.functions.get_name(target)
        for xref in db.xrefs.calls_to_ea(target.start_ea):
            caller = db.functions.get_at(xref.from_ea)
            if caller is None:
                continue
            caller_name = db.functions.get_name(caller)
            if caller_name not in OWN_NAMES:
                continue
            instruction = db.instructions.get_at(xref.from_ea)
            calls.append(
                {
                    "from": caller_name,
                    "to": target_name,
                    "call_ea": hex(xref.from_ea),
                    "target_ea": hex(target.start_ea),
                    "instruction": db.instructions.get_disassembly(instruction),
                }
            )

    calls = sorted(calls, key=lambda item: (item["from"], item["to"], item["call_ea"]))
    observed_edges = {(item["from"], item["to"]) for item in calls}
    evidence = [
        item for item in calls if (item["from"], item["to"]) in REQUIRED_EDGES
    ]
    return {
        "input_sha256": db.sha256,
        "functions": sorted(
            [
                {
                    "name": db.functions.get_name(func),
                    "start_ea": hex(func.start_ea),
                }
                for func in functions
            ],
            key=lambda item: item["start_ea"],
        ),
        "calls": calls,
        "conclusion": {
            "text": "main 直接调用 authorize；authorize 直接调用 check 和 mix；check 直接调用 mix。",
            "supported": all(edge in observed_edges for edge in REQUIRED_EDGES),
            "scope": "仅证明自建二进制中的直接静态调用边，不证明运行时必达、数据流或语义正确性。",
            "evidence": evidence,
        },
    }
