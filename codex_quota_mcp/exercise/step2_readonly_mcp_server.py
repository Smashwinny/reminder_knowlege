# -*- coding: utf-8 -*-
"""实验第 2 步：只读、最小权限、可审计的"生产数据 MCP Server"（stdio JSON-RPC 版）。

对应文章核心步骤：让 Codex 写一个供网页版 GPT-6 Pro 调用的生产业务数据
只读 MCP Server。三原则在本实现里的落点：
  只读     -> SQLite 以 file:...?mode=ro 打开（物理只读，写 SQL 直接抛异常）
              + SQL 白名单校验（只放行 SELECT，拦 INSERT/UPDATE/DELETE/DROP/ATTACH）
  最小权限 -> 工具目录只有 2 个白名单工具；表名白名单；无任何写工具存在
  可审计   -> 每个进来的请求（含被拒绝的）都追加写 audit_log.jsonl

协议：每行一个 JSON-RPC 2.0 消息（MCP stdio 传输的最小子集）。
"""
import sqlite3
import json
import sys
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DB_URI = "file:" + os.path.join(BASE, "aihot_prod.db").replace("\\", "/") + "?mode=ro"
AUDIT = os.path.join(BASE, "audit_log.jsonl")

# ---------- 最小权限：白名单 ----------
ALLOWED_TABLES = {"users", "api_costs"}
WRITE_KEYWORDS = ("INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE",
                  "ATTACH", "PRAGMA", "REPLACE", "VACUUM", "REINDEX")

TOOLS = [
    {
        "name": "get_cost_summary",
        "description": "按模型聚合近两周 API 成本（只读，无参数）",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "query_table",
        "description": "对白名单表执行只读 SELECT，最多返回 20 行",
        "inputSchema": {
            "type": "object",
            "properties": {
                "table": {"type": "string", "enum": ["users", "api_costs"]},
                "sql": {"type": "string", "description": "SELECT 语句"},
            },
            "required": ["table", "sql"],
        },
    },
]


def audit(method: str, params: dict, ok: bool, note: str):
    """可审计：JSONL 只追加，一行一次调用（含被拒的）。"""
    rec = {"ok": ok, "method": method, "note": note, "params": params}
    with open(AUDIT, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def get_conn():
    # 只读的第一道闸：URI mode=ro，驱动层面拒绝写
    return sqlite3.connect(DB_URI, uri=True)


def sql_is_readonly(sql: str) -> bool:
    # 只读的第二道闸：关键词白名单（第一道是 mode=ro，双保险）
    head = sql.strip().split()[0].upper() if sql.strip() else ""
    return head == "SELECT" and not any(k in sql.upper() for k in WRITE_KEYWORDS)


def tool_get_cost_summary(_args):
    conn = get_conn()
    rows = conn.execute(
        "SELECT model, COUNT(*) n, SUM(cost_usd) usd "
        "FROM api_costs GROUP BY model ORDER BY usd DESC"
    ).fetchall()
    conn.close()
    return {"rows": [{"model": m, "calls": n, "cost_usd": round(u, 2)} for m, n, u in rows]}


def tool_query_table(args):
    table, sql = args.get("table", ""), args.get("sql", "")
    if table not in ALLOWED_TABLES:
        raise PermissionError(f"表不在白名单: {table}")
    if not sql_is_readonly(sql):
        raise PermissionError("只允许纯 SELECT（拦截写关键词）")
    conn = get_conn()
    try:
        cur = conn.execute(sql)
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchmany(20)]
    finally:
        conn.close()
    return {"rows": rows}


TOOL_IMPL = {"get_cost_summary": tool_get_cost_summary, "query_table": tool_query_table}


def dispatch(req: dict) -> dict:
    method = req.get("method", "")
    rid = req.get("id")
    params = req.get("params", {}) or {}
    try:
        if method == "initialize":
            result = {"protocolVersion": "2025-06-18",
                      "serverInfo": {"name": "aihot-readonly-prod", "version": "0.1.0"}}
        elif method == "tools/list":
            result = {"tools": TOOLS}
        elif method == "tools/call":
            name = params.get("name")
            if name not in TOOL_IMPL:  # 最小权限：目录外工具不存在
                raise PermissionError(f"未知工具: {name}")
            out = TOOL_IMPL[name](params.get("arguments", {}) or {})
            result = {"content": [{"type": "text", "text": json.dumps(out, ensure_ascii=False)}]}
        else:
            raise KeyError(f"method not found: {method}")
        audit(method, params, True, "ok")
        return {"jsonrpc": "2.0", "id": rid, "result": result}
    except Exception as e:
        audit(method, params, False, f"rejected: {e}")
        return {"jsonrpc": "2.0", "id": rid,
                "error": {"code": -32603, "message": str(e)}}


if __name__ == "__main__":
    if os.path.exists(AUDIT):
        os.remove(AUDIT)  # 可重复实验
    for line in sys.stdin:  # stdio 传输：stdout 即协议
        line = line.strip()
        if not line:
            continue
        resp = dispatch(json.loads(line))
        sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
        sys.stdout.flush()
