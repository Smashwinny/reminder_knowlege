# -*- coding: utf-8 -*-
"""yichen-skills 主实验：全合成微信快照，走通 windows-reader 五步链路 + 两个负向验证。

隐私红线：所有 wxid/昵称/消息均为本脚本虚构（fixture_factory 自带合成数据），
不触碰本机任何真实微信数据，不联网，不访问任何 Weixin 进程。
"""
import json
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_TESTS = HERE.parent / "repo" / "yichen-wechat-windows-reader" / "tests"
sys.path.insert(0, str(REPO_TESTS))
from fixture_factory import build, fixture_chat_id, DEFAULT_SNAPSHOT_ID  # noqa: E402

READER = HERE.parent / "repo" / "yichen-wechat-windows-reader" / "scripts" / "snapshot_reader.py"
WORK = HERE / "snapshot_demo"

def run(*args):
    cmd = [sys.executable, str(READER), "--snapshot", str(WORK), *args]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return r.returncode, (r.stdout + r.stderr).strip()

def step(n, title):
    print(f"\n{'='*62}\n第{n}步 {title}\n{'='*62}")

# ── 准备：全合成快照 ────────────────────────────────────────────
if WORK.exists():
    shutil.rmtree(WORK)
info = build(WORK)
group_id = info["group_id"]
print(f"[准备] 合成快照已生成: {WORK}")
print(f"[准备] snapshot_id={DEFAULT_SNAPSHOT_ID}")
print(f"[准备] 群会话 chat_id(派生)={group_id}")

# ── 第1步 validate：快照契约校验 ───────────────────────────────
step(1, "validate 快照契约校验（期望 PASS）")
code, out = run("validate")
print(f"exit={code}\n{out[:600]}")
assert code == 0, "validate 应通过"

# ── 第2步 chats：列会话拿 chat_id ─────────────────────────────
step(2, "chats 列会话（期望列出 fixture_group@chatroom）")
code, out = run("chats")
print(f"exit={code}\n{out[:800]}")
assert "测试群" in out  # 注意：输出用 display_name，原始 username 被脱敏——这是设计
data = json.loads(out)
chat_id = next(c["chat_id"] for c in data["chats"] if c["kind"] == "group")
print(f">> 取到 chat_id = {chat_id}（与本地派生一致: {chat_id == group_id}）")
assert chat_id == group_id

# ── 第3步 history：按精确 chat_id 查历史 ──────────────────────
step(3, "history 按 chat_id 查历史（期望 3 条合成消息）")
code, out = run("history", chat_id)
print(f"exit={code}\n{out[:1200]}")
assert code == 0

# ── 第4步 search：压缩正文关键词检索 ──────────────────────────
step(4, "search 关键词检索 zstd 压缩正文（期望命中 星河）")
code, out = run("search", chat_id, "星河")
print(f"exit={code}\n{out[:800]}")
assert "星河" in out, "应解压并命中压缩正文关键词"

# ── 第5步 export：导出 Markdown ──────────────────────────────
step(5, "export 导出 Markdown 报告")
code, out = run("export", chat_id)
print(f"exit={code}\n{out[:800]}")
assert code == 0
exports = list((WORK.parent / "exports_demo" if False else WORK).glob("**/*.md"))
# export 默认写 LocalAppData，这里看 CLI 输出里的路径即可

# ── 负向A：WAL sidecar 必须被拒 ───────────────────────────────
step("6A", "负向验证：塞入 message_0.db-wal sidecar（期望 validate 拒绝）")
wal = WORK / "message" / "message_0.db-wal"
con = sqlite3.connect(WORK / "message" / "message_0.db")
con.execute("PRAGMA wal_checkpoint(TRUNCATE)").fetchall()
con.close()
wal.write_bytes(b"\x00" * 32)  # 伪造 sidecar 文件
code, out = run("validate")
print(f"exit={code}\n{out[:500]}")
print(">> 拒绝了 WAL sidecar" if code != 0 else "!! 未拒绝——异常")
assert code != 0, "有 WAL sidecar 时 validate 必须失败"
wal.unlink()

# ── 负向B：坏 UUIDv4 manifest 必须被拒 ────────────────────────
step("6B", "负向验证：manifest 改成非 UUIDv4（期望 validate 拒绝）")
manifest = WORK / "snapshot-manifest.json"
good = manifest.read_text(encoding="utf-8")
manifest.write_text(json.dumps({"snapshot_id": "not-a-uuid"}), encoding="utf-8")
code, out = run("validate")
print(f"exit={code}\n{out[:500]}")
print(">> 拒绝了非法 snapshot_id" if code != 0 else "!! 未拒绝——异常")
assert code != 0
manifest.write_text(good, encoding="utf-8")

# ── 恢复后再验证一次，确认契约可恢复 ──────────────────────────
step("7", "修复后重新 validate（期望恢复 PASS）")
code, out = run("validate")
print(f"exit={code}\n{out[:300]}")
assert code == 0

print("\n" + "=" * 62)
print("ALL 7 STEPS PASSED — 合成数据全链路跑通，红线未破（无真实微信触碰）")
