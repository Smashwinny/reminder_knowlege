"""Real execution: same checks for both implementations; standard library only.
Run from this folder: python3 test_lookup.py
Never imports or executes the upstream reference excerpt.
"""
import ast
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sqlite3

import minimal
import layered

ROOT = Path(__file__).resolve().parent
ROWS = [
    (1, "alice", "a@x.com"),
    (2, "bob", "b@x.com"),
    (3, "O'Brien", "quote@example.test"),
    (4, "陈小云", "unicode@example.test"),
    (5, "x" * 64, "limit@example.test"),
]

def fresh():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, email TEXT)")
    conn.executemany("INSERT INTO users VALUES (?, ?, ?)", ROWS)
    conn.commit()
    return conn

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def raises(expected_type, call, message=None):
    try:
        call()
    except expected_type as exc:
        if message is not None:
            require(str(exc) == message, f"wrong message: {exc}")
    else:
        raise AssertionError(f"expected {expected_type.__name__}")

# The same check list, same setup, and same assertions run for each implementation.
def checks(fn):
    results = []
    def check(name, action):
        action()
        results.append(name)
        print(f"  PASS {name}")
    with closing(fresh()) as conn:
        check("functional.existing", lambda: require(fn(conn, "alice") == ROWS[0], "wrong row"))
        check("functional.missing", lambda: require(fn(conn, "missing") is None, "missing must be None"))
        check("functional.quote", lambda: require(fn(conn, "O'Brien") == ROWS[2], "quoted username"))
        check("functional.unicode", lambda: require(fn(conn, "陈小云") == ROWS[3], "Unicode username"))
        check("boundary.length64", lambda: require(fn(conn, "x" * 64) == ROWS[4], "boundary length"))
        check("boundary.type", lambda: raises(TypeError, lambda: fn(conn, None), "username must be a string"))
        check("boundary.integer", lambda: raises(TypeError, lambda: fn(conn, 1), "username must be a string"))
        check("boundary.empty", lambda: raises(ValueError, lambda: fn(conn, ""), "username must contain 1..64 characters without NUL"))
        check("boundary.length65", lambda: raises(ValueError, lambda: fn(conn, "x" * 65), "username must contain 1..64 characters without NUL"))
        check("boundary.nul", lambda: raises(ValueError, lambda: fn(conn, "a\x00b"), "username must contain 1..64 characters without NUL"))
        for index, payload in enumerate(["x' OR '1'='1", "' OR 1=1 --", "alice'; DROP TABLE users; --"], 1):
            check(f"security.injection{index}", lambda p=payload: require(fn(conn, p) is None, "payload returned data"))
        check("security.readonly", lambda: require(conn.execute("SELECT * FROM users ORDER BY id").fetchall() == ROWS, "data changed"))
        check("usability.repeat", lambda: require(fn(conn, "bob") == fn(conn, "bob") == ROWS[1], "repeat calls"))
        check("usability.connection_owned_by_caller", lambda: require(conn.execute("SELECT 1").fetchone() == (1,), "connection was closed"))
        conn.execute("INSERT INTO users VALUES (?, ?, ?)", (99, "pending", "pending@example.test"))
        check("usability.no_implicit_commit", lambda: require(fn(conn, "pending")[0] == 99 and conn.in_transaction, "transaction committed"))
        conn.rollback()
        check("usability.rollback_preserved", lambda: require(fn(conn, "pending") is None, "transaction ownership lost"))
        conn.row_factory = sqlite3.Row
        check("usability.tuple_result", lambda: require(type(fn(conn, "alice")) is tuple and fn(conn, "alice") == ROWS[0], "unstable return type"))
    closed = fresh()
    closed.close()
    check("errors.closed_connection", lambda: raises(sqlite3.ProgrammingError, lambda: fn(closed, "alice")))
    with closing(sqlite3.connect(":memory:")) as conn:
        check("errors.missing_table", lambda: raises(sqlite3.OperationalError, lambda: fn(conn, "alice")))
    return results

def unsafe_negative_control(conn, username):
    # INTENTIONALLY UNSAFE. Only used below against disposable fake in-memory rows.
    return conn.execute("SELECT id, username, email FROM users WHERE username = '" + username + "'").fetchone()

def metrics(path):
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    return {
        "bytes": path.stat().st_size,
        "nonblank_noncomment_lines_including_docstrings": sum(bool(line.strip()) and not line.lstrip().startswith("#") for line in source.splitlines()),
        "classes": sum(isinstance(node, ast.ClassDef) for node in ast.walk(tree)),
        "functions_including_methods": sum(isinstance(node, ast.FunctionDef) for node in ast.walk(tree)),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }

def main():
    print("PONYTAIL LOCAL ENGINEERING COMPARISON - NOT AN AGENTIC BENCHMARK REPLICATION")
    print("UTC", datetime.now(timezone.utc).isoformat())
    print("Python", platform.python_version(), "SQLite", sqlite3.sqlite_version)
    print("upstream_commit e15862bb04d04285233a164460ced063941d9ef5")
    print("upstream_task benchmarks/agentic/tasks.py :: sql-user")
    print("fixture :memory:, fake records only, API calls 0, third-party packages 0")
    completed = {}
    for label, module in [("minimal", minimal), ("layered", layered)]:
        print("IMPLEMENTATION", label)
        completed[label] = checks(module.get_user)
    require(completed["minimal"] == completed["layered"], "unequal contract test lists")
    with closing(fresh()) as conn:
        require(unsafe_negative_control(conn, "alice") == ROWS[0], "negative control must pass happy path")
        leaked = unsafe_negative_control(conn, "x' OR '1'='1")
        require(leaked is not None, "negative control unexpectedly safe")
        print("NEGATIVE CONTROL caught: happy path passed but injection leaked fake user id", leaked[0])
    report = {name: metrics(ROOT / f"{name}.py") for name in completed}
    print("METRICS", json.dumps(report, ensure_ascii=False, sort_keys=True))
    print(f"RESULT PASS: {len(completed['minimal'])} shared checks per implementation; {sum(map(len, completed.values()))} passing implementation checks; 1 unsafe negative control detected")
    print("LIMIT: finite local contract checks only; no authentication, authorization, production DB, concurrency, timing, API cost, model, or full security evaluation")

if __name__ == "__main__":
    main()
