"""One local coordinator for shared vault/index/Git/site writes."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone, timedelta
import json
from pathlib import Path
import sqlite3
import time


def connect(root):
    folder = Path(root).resolve() / "完成/.pipeline"
    folder.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(folder / "coordination.sqlite3", timeout=15)
    db.row_factory = sqlite3.Row
    db.execute("CREATE TABLE IF NOT EXISTS coordinator (id INTEGER PRIMARY KEY CHECK(id=1), owner TEXT NOT NULL, lease_until REAL NOT NULL)")
    db.commit()
    return db


@contextmanager
def transaction(root):
    db = connect(root)
    try:
        db.execute("BEGIN IMMEDIATE")
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def acquire(root, owner, ttl=7200):
    if not owner.strip() or ttl < 60:
        raise ValueError("owner 不能为空，租约至少 60 秒")
    with transaction(root) as db:
        row = db.execute("SELECT * FROM coordinator WHERE id=1").fetchone()
        if row:
            raise RuntimeError(f"协调者已由 {row['owner']} 领取；到期也不自动抢占，请原协调者 release 或人工确认已停止后清理。")
        db.execute("INSERT INTO coordinator VALUES (1,?,?)", (owner, time.time() + ttl))
    return status(root)


def require_owner(root, owner):
    with transaction(root) as db:
        row = db.execute("SELECT * FROM coordinator WHERE id=1").fetchone()
        if not row or row["owner"] != owner or row["lease_until"] < time.time():
            raise RuntimeError("当前操作者没有有效全局协调者租约；先领取/续约，再修改共享状态。")


def renew(root, owner, ttl=7200):
    with transaction(root) as db:
        row = db.execute("SELECT * FROM coordinator WHERE id=1").fetchone()
        if not row or row["owner"] != owner:
            raise RuntimeError("只有原协调者可以续约")
        db.execute("UPDATE coordinator SET lease_until=? WHERE id=1", (time.time() + ttl,))
    return status(root)


def release(root, owner):
    with transaction(root) as db:
        row = db.execute("SELECT * FROM coordinator WHERE id=1").fetchone()
        if row and row["owner"] != owner:
            raise RuntimeError("不能释放其他协调者的租约")
        db.execute("DELETE FROM coordinator WHERE id=1")
    return status(root)


def status(root):
    db = connect(root)
    try:
        row = db.execute("SELECT * FROM coordinator WHERE id=1").fetchone()
        if not row:
            return {"owner": None}
        return {"owner": row["owner"], "lease_until": datetime.fromtimestamp(
            row["lease_until"], timezone(timedelta(hours=8))).isoformat(),
            "expired": row["lease_until"] < time.time()}
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    for name in ("acquire", "renew", "release"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--owner", required=True)
        if name != "release":
            cmd.add_argument("--ttl", type=int, default=7200)
    args = parser.parse_args()
    try:
        value = (status(args.root) if args.command == "status" else
                 release(args.root, args.owner) if args.command == "release" else
                 globals()[args.command](args.root, args.owner, args.ttl))
        print(json.dumps(value, ensure_ascii=False))
    except (ValueError, RuntimeError) as error:
        parser.exit(2, f"错误：{error}\n")
