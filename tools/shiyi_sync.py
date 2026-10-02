# -*- coding: utf-8 -*-
"""拾遗 (reminder.geniusqi.com) 任务同步工具。

用法（token 从环境变量 SHIYI_TOKEN 读取）:
  python tools/shiyi_sync.py list                 # 列出全部未完成任务
  python tools/shiyi_sync.py viewed <task_id>     # 标记为已查看(state=1，等同"开始任务")
  python tools/shiyi_sync.py done <task_id>       # 标记为已完成(state=3，等同"标记完成")
  python tools/shiyi_sync.py login <user> <pass>  # 登录并打印 token（供设置 SHIYI_TOKEN）

token 也可以放在仓库根目录 tools/.shiyi_token 文件里（已被 .gitignore 排除则优先级低于环境变量）。
"""
import json
import os
import sys
import time
import urllib.request

BASE = "https://reminder.geniusqi.com"
TOKEN_FILE = os.path.join(os.path.dirname(__file__), ".shiyi_token")


def get_token():
    tok = os.environ.get("SHIYI_TOKEN", "").strip()
    if tok:
        return tok
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            tok = f.read().strip()
        if tok:
            return tok
    print("错误：未提供 token。请设置环境变量 SHIYI_TOKEN 或写入 tools/.shiyi_token", file=sys.stderr)
    sys.exit(1)


def api(path, payload=None, token=None):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(payload).encode("utf-8") if payload is not None else None,
        headers={
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            **({"authorization": "Bearer " + token} if token else {}),
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def download_tasks(token):
    result = api("/api/sync", {"mode": "download", "tasks": []}, token)
    # 兼容两种返回结构：{tasks: [...]} 或直接 [...]
    return result.get("tasks", result) if isinstance(result, dict) else result


def upload_task(token, task):
    return api("/api/sync", {"mode": "upload", "tasks": [task]}, token)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"

    if cmd == "login":
        result = api("/api/auth/login", {"username": sys.argv[2], "password": sys.argv[3]})
        print(result["token"])
        return

    token = get_token()
    tasks = download_tasks(token)

    if cmd == "list":
        live = [t for t in tasks if not t.get("deleted") and t.get("state") != 3]
        live.sort(key=lambda t: t.get("createdAt", 0))
        for t in live:
            state = {0: "未开始", 1: "进行中", 2: "暂停"}.get(t.get("state"), t.get("state"))
            print(f"[{t['id']}] state={state} 查看{t.get('viewCount', 0)}次 {t['createdAt'] and time.strftime('%Y-%m-%d', time.localtime(t['createdAt']/1000))}")
            print(f"    {t['text'][:120]}")
        print(f"-- 共 {len(live)} 条未完成 --")
    elif cmd == "viewed":
        tid = sys.argv[2]
        t = next(t for t in tasks if t["id"] == tid)
        if t.get("state") != 3:
            t["state"] = 1
            t["viewCount"] = t.get("viewCount", 0)
            t["lastViewedAt"] = t["updatedAt"] = int(time.time() * 1000)
            upload_task(token, t)
        print(f"已标记为已查看: {t['text'][:60]}")
    elif cmd == "done":
        tid = sys.argv[2]
        t = next(t for t in tasks if t["id"] == tid)
        t["state"] = 3
        t["updatedAt"] = int(time.time() * 1000)
        upload_task(token, t)
        print(f"已完成: {t['text'][:60]}")
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
