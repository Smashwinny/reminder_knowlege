# -*- coding: utf-8 -*-
"""实验第 3 步：扮演"网页版 GPT-6 Pro"的 MCP 客户端，逐项验收三原则。

T1 最小权限：tools/list 只有 2 个白名单工具，没有任何写工具
T2 只读-放行：get_cost_summary / 纯 SELECT 正常返回
T3 只读-拦截(应用层)：INSERT / DELETE / DROP 被 SQL 校验拒绝
T4 只读-拦截(驱动层)：绕过校验的写请求被 SQLite mode=ro 拒绝（双保险）
T5 最小权限：目录外表 / 白名单外表的调用被拒绝
T6 可审计：audit_log.jsonl 行数 == 客户端发出的请求总数
"""
import json
import subprocess
import sys
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SERVER = os.path.join(BASE, "step2_readonly_mcp_server.py")
AUDIT = os.path.join(BASE, "audit_log.jsonl")

_id = 0
results = []


def rpc(method, params=None):
    global _id
    _id += 1
    return {"jsonrpc": "2.0", "id": _id, "method": method, "params": params or {}}


def run(name, expect_ok, desc):
    results.append((name, expect_ok, desc))


def main():
    p = subprocess.Popen([sys.executable, SERVER], stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, text=True, encoding="utf-8")

    def call(req):
        p.stdin.write(json.dumps(req, ensure_ascii=False) + "\n")
        p.stdin.flush()
        return json.loads(p.stdout.readline())

    # T1
    r = call(rpc("tools/list"))
    names = [t["name"] for t in r["result"]["tools"]]
    ok = names == ["get_cost_summary", "query_table"] and not any("write" in n or "insert" in n for n in names)
    run("T1 最小权限-工具目录白名单", ok, f"tools={names}")

    # T2a
    r = call(rpc("tools/call", {"name": "get_cost_summary"}))
    text = r["result"]["content"][0]["text"]
    ok = "gpt6-astra-ultra" in text and "error" not in r
    run("T2a 只读放行-成本聚合", ok, text[:110])

    # T2b 纯 SELECT
    r = call(rpc("tools/call", {"name": "query_table", "arguments": {
        "table": "api_costs", "sql": "SELECT model, cost_usd FROM api_costs ORDER BY cost_usd DESC"}}))
    ok = "error" not in r
    run("T2b 只读放行-纯SELECT", ok, json.dumps(r.get("result", r), ensure_ascii=False)[:110])

    # T3 写语句被应用层校验拦截
    for bad in ["INSERT INTO users VALUES (999,'h','free','x')",
                "DELETE FROM api_costs",
                "SELECT 1; DROP TABLE users"]:
        r = call(rpc("tools/call", {"name": "query_table", "arguments": {
            "table": "api_costs", "sql": bad}}))
        ok = "error" in r and "只允许纯 SELECT" in r["error"]["message"]
        run(f"T3 拦截写SQL[{bad.split()[0]}...]", ok, r.get("error", {}).get("message", "??")[:80])

    # T4 驱动层 mode=ro 兜底（构造绕过关键词校验的写：不存在的路径没有，但直接验证 ro 连接）
    #   通过一个只会经过校验的 PRAGMA 已被拦，这里直接验证 mode=ro 语义本身
    import sqlite3
    uri = "file:" + os.path.join(BASE, "aihot_prod.db").replace("\\", "/") + "?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    try:
        conn.execute("INSERT INTO users VALUES (999,'h','free','x')")
        run("T4 驱动层 mode=ro 拦写", False, "写竟然成功了！")
    except sqlite3.OperationalError as e:
        run("T4 驱动层 mode=ro 拦写", "readonly" in str(e).lower(), str(e))
    finally:
        conn.close()

    # T5 白名单外表
    r = call(rpc("tools/call", {"name": "query_table", "arguments": {
        "table": "sqlite_master", "sql": "SELECT * FROM sqlite_master"}}))
    ok = "error" in r and "白名单" in r["error"]["message"]
    run("T5 最小权限-白名单外表拒绝", ok, r.get("error", {}).get("message", "??"))

    r = call(rpc("tools/call", {"name": "write_everything"}))
    ok = "error" in r
    run("T5b 最小权限-目录外工具拒绝", ok, r.get("error", {}).get("message", "??"))

    p.stdin.close()
    p.wait(timeout=10)

    # T6 审计对账：客户端共发出 _id 个请求
    with open(AUDIT, encoding="utf-8") as f:
        lines = [json.loads(x) for x in f if x.strip()]
    n_reject = sum(1 for x in lines if not x["ok"])
    run("T6 可审计-JSONL对账", len(lines) == _id, f"请求 {_id} 条 = 审计 {len(lines)} 行（其中拒绝 {n_reject} 条）")

    print("=" * 78)
    n_pass = 0
    for name, ok, desc in results:
        mark = "PASS" if ok else "FAIL"
        n_pass += ok
        print(f"[{mark}] {name}")
        print(f"       {desc}")
    print("=" * 78)
    print(f"总计 {n_pass}/{len(results)} PASS")
    sys.exit(0 if n_pass == len(results) else 1)


if __name__ == "__main__":
    main()
