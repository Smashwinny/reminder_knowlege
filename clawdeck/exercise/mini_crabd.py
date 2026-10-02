"""mini_crabd —— SideCrab(Claw'deck) 数据管线的 150 行复刻（学习实验用）

复刻上游 companion/crabd.py 的核心思想，但只保留最小闭环：
  Claude Code hooks (HTTP POST)  ->  本服务状态机  ->  GET /v1/state 单一 JSON 馈送
                                                  ->  GET /panel/   轮询面板页

只用标准库（对应知识库 [[零依赖编程]]）。运行:
    python mini_crabd.py 2799
模拟 hook 事件:
    curl -X POST http://127.0.0.1:2799/v1/hook/session-start -d "{\"session_id\":\"s1\",\"cwd\":\"F:/reminder\"}"
    curl -X POST http://127.0.0.1:2799/v1/hook/prompt         -d "{\"session_id\":\"s1\"}"
    curl -X POST http://127.0.0.1:2799/v1/hook/stop           -d "{\"session_id\":\"s1\"}"
    curl http://127.0.0.1:2799/v1/state
"""

from __future__ import annotations

import json
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 2799
DONE_DROP_SEC = 600          # 上游同款：done/failed 会话 10 分钟后从面板退役
STATE_ORDER = {"needs_input": 0, "failed": 1, "working": 2, "idle": 3, "done": 4}

sessions: dict[str, dict] = {}


def burn_from_transcript(path: str) -> dict:
    """只读解析 Claude Code 的 JSONL 会话转录，累计输出 token（上游同思路）。
    关联知识库 [[JSONL事件日志与折叠模型]]。"""
    out_tokens = entries = 0
    try:
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            entries += 1
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            usage = (rec.get("message") or {}).get("usage") or {}
            out_tokens += int(usage.get("output_tokens") or 0)
    except OSError:
        pass
    return {"jsonlEntries": entries, "outputTokens": out_tokens}


def apply_hook(event: str, payload: dict) -> None:
    sid = payload.get("session_id") or "unknown"
    s = sessions.setdefault(sid, {
        "sessionId": sid, "state": "idle", "title": None, "question": None,
        "subagents": 0, "since": time.time(), "burn": None,
    })
    s["since"] = time.time()
    if payload.get("cwd") and not s["title"]:
        s["title"] = Path(payload["cwd"]).name or payload["cwd"]
    if payload.get("transcript_path"):
        s["burn"] = burn_from_transcript(payload["transcript_path"])

    if event == "session-start":
        s["state"] = "idle"
    elif event == "prompt":            # UserPromptSubmit：开跑，清掉问题与失败
        s["state"], s["question"] = "working", None
    elif event == "notification":      # Notification：需要人来看一眼
        s["state"] = "needs_input"
        if payload.get("message"):
            s["question"] = str(payload["message"])[:120]
    elif event == "permission":        # PermissionRequest：也是一种等输入
        s["state"], s["question"] = "needs_input", "permission request"
    elif event == "stop":              # Stop：本轮收工
        s["state"] = "done"
    elif event == "stop-failure":      # StopFailure：API 错误，自己回不来了
        s["state"] = "failed"
        s["question"] = "API error"
    elif event == "subagent-start":
        s["subagents"] += 1
    elif event == "subagent-stop":
        s["subagents"] = max(0, s["subagents"] - 1)
    elif event == "session-end":
        sessions.pop(sid, None)        # gone：立即退役（上游是宽限一段时间）

    now = time.time()
    for k in [k for k, v in sessions.items()
              if v["state"] in ("done", "failed") and now - v["since"] > DONE_DROP_SEC]:
        del sessions[k]


def build_state() -> dict:
    live = sorted(sessions.values(), key=lambda s: (STATE_ORDER.get(s["state"], 9), -s["since"]))
    waiting = any(s["state"] == "needs_input" for s in live)
    total_out = sum((s["burn"] or {}).get("outputTokens", 0) for s in live)
    return {
        "schema": 5,                                   # 上游策略：破坏性变更才升号，新字段按存在性探测
        "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()) + "Z",
        "mood": "alert" if waiting else "calm",        # 螃蟹心情即状态（数据过期时上游会变 worried）
        "sessions": live,
        "totals": {"sessions": len(live), "waiting": sum(s["state"] == "needs_input" for s in live),
                   "outputTokensToday": total_out},
    }


PANEL_HTML = """<!doctype html><meta charset="utf-8"><title>mini-crabd panel</title>
<style>
 body{margin:0;background:#101828;color:#e6edf7;font:16px/1.4 'Segoe UI',sans-serif}
 #mood{font-size:64px} .card{border:2px solid #2b3b57;border-radius:12px;padding:10px 14px;margin:8px 0}
 .needs_input{border-color:#ff9f1c;background:#3a2a10}
 .working{border-color:#6f94cc} .done{border-color:#2ea86f} .failed{border-color:#e5484d}
 b{color:#ffd166}
</style><div id="mood">🦀</div><div id="cards"></div><script>
async function tick(){
  try{
    const st = await (await fetch('/v1/state')).json();
    mood.textContent = st.mood==='alert' ? '🦀⚠️ 有会话在等你' : '🦀 一切安好';
    cards.innerHTML = st.sessions.map(s=>
      `<div class="card ${s.state}"><b>${s.title||s.sessionId}</b> — ${s.state}` +
      (s.question?`：${s.question}`:'') +
      (s.burn?` · 燃烧 ${s.burn.outputTokens} tok (${s.burn.jsonlEntries} 行)`:'') + `</div>`).join('');
  }catch(e){ mood.textContent='🦀😵 数据馈送失联（worried）'; }
}
setInterval(tick,1000); tick();
</script>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body=b"", ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):  # hook 入口：永远 204 无正文，fail-open，绝不阻塞会话
        n = int(self.headers.get("Content-Length") or 0)
        try:
            payload = json.loads(self.rfile.read(n) or b"{}")
        except json.JSONDecodeError:
            payload = {}
        event = self.path.rsplit("/", 1)[-1]
        apply_hook(event, payload)
        self._send(204)

    def do_GET(self):
        if self.path == "/v1/state":
            self._send(200, json.dumps(build_state(), ensure_ascii=False).encode())
        elif self.path == "/panel/":
            self._send(200, PANEL_HTML.encode(), "text/html; charset=utf-8")
        else:
            self._send(404, b"{}")

    def log_message(self, *a):  # 静默，实验输出只看 curl
        pass


if __name__ == "__main__":
    print(f"mini-crabd listening on http://127.0.0.1:{PORT}  (panel: /panel/)")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
