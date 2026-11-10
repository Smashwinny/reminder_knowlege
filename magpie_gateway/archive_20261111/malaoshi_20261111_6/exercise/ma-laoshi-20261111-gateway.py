#!/usr/bin/env python3
"""Teaching implementation, NOT magpie nor a Kiro adapter. No credentials.
Concept sources (read-only, not copied):
https://github.com/yetone/magpie/blob/a54dddd9671a0646708df01364882c38cbb2decf/internal/gateway/anthropic.go#L137-L241
https://platform.claude.com/docs/en/api/messages/create (read 2026-11-11 Asia/Shanghai).
Only Python stdlib. Hardcoded loopback upstream. Never reads environment or accounts.
"""
import json, http.client
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

ROUTES = {"study/fast": "mock-fast-v1", "study/deep": "mock-deep-v1"}

def post(port, path, obj):
    c = http.client.HTTPConnection("127.0.0.1", port, timeout=2)
    try:
        c.request("POST", path, json.dumps(obj), {"Content-Type":"application/json"})
        r = c.getresponse(); status = r.status; data = json.loads(r.read())
        return status, data
    finally:
        c.close()

def text(value):
    if isinstance(value, str): return value
    if isinstance(value, list) and all(isinstance(b, dict) and b.get("type") == "text" and isinstance(b.get("text"), str) for b in value):
        return "\n".join(b["text"] for b in value)
    raise ValueError("only string/text blocks supported")

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args): pass
    def send(self, status, obj, headers=None):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(status); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        for k,v in (headers or {}).items(): self.send_header(k,v)
        self.end_headers(); self.wfile.write(body)
    def read(self):
        n=int(self.headers.get("Content-Length", "0"))
        if n < 1 or n > 65536: raise ValueError("body length must be 1..65536")
        return json.loads(self.rfile.read(n))

class Mock(Handler):
    def do_POST(self):
        b=self.read(); self.server.seen.append(b)
        if any("__fail503__" in m["content"] for m in b["messages"]):
            return self.send(503,{"error":"injected local failure"})
        # Fixed synthetic counts, NOT a real model tokenizer or bill.
        count=sum(len(m["content"].split()) for m in b["messages"])
        self.send(200,{"model":b["model"],"choices":[{"message":{"content":"mock answer"},"finish_reason":"stop"}],"usage":{"prompt_tokens":count,"completion_tokens":2}})

class Gateway(Handler):
    def do_GET(self):
        if self.path != "/usage": return self.send(404,{"error":"not found"})
        self.send(200,self.server.meter)
    def reject(self,status,reason):
        self.server.meter["rejected"]+=1
        self.send(status,{"type":"error","error":{"type":"study_error","message":reason}})
    def do_POST(self):
        if self.path != "/v1/messages": return self.reject(404,"unknown path")
        if self.headers.get("Authorization") or self.headers.get("x-api-key"):
            return self.reject(400,"credentials forbidden in this exercise")
        try:
            b=self.read()
            if not isinstance(b,dict): raise ValueError("body must be object")
            if b.get("model") not in ROUTES: return self.reject(404,"unknown model")
            if b.get("stream"): return self.reject(501,"stream not implemented")
            if any(k not in {"model","messages","system","max_tokens","stream"} for k in b):
                raise ValueError("unsupported field; no silent dropping")
            if type(b.get("max_tokens")) is not int or b["max_tokens"]<=0: raise ValueError("max_tokens must be positive integer")
            if not isinstance(b.get("messages"),list) or not b["messages"]: raise ValueError("nonempty messages required")
            messages=[]
            if "system" in b: messages.append({"role":"system","content":text(b["system"])})
            for m in b["messages"]:
                if not isinstance(m,dict) or m.get("role") not in {"user","assistant"}: raise ValueError("unsupported role")
                messages.append({"role":m["role"],"content":text(m.get("content"))})
        except (ValueError,TypeError,KeyError) as e: return self.reject(400,str(e))
        wire={"model":ROUTES[b["model"]],"messages":messages,"max_tokens":b["max_tokens"]}
        self.server.meter["upstream_attempts"]+=1
        try:
            status,out=post(self.server.upstream,"/chat/completions",wire)
            if status != 200: return self.send(502,{"type":"error","error":{"type":"upstream_error","message":"local mock returned "+str(status)}})
            u=out["usage"]; content=out["choices"][0]["message"]["content"]
        except (OSError,ValueError,KeyError) as e:
            return self.send(502,{"type":"error","error":{"type":"upstream_error","message":type(e).__name__}})
        self.server.meter["success"]+=1
        for k,v in [("input_units",u["prompt_tokens"]),("output_units",u["completion_tokens"])]: self.server.meter[k]+=v
        self.send(200,{"id":"msg_study_mock","type":"message","role":"assistant","model":b["model"],"content":[{"type":"text","text":content}],"stop_reason":"end_turn","stop_sequence":None,"usage":{"input_tokens":u["prompt_tokens"],"output_tokens":u["completion_tokens"]}}, {"X-Study-Provider":"local-mock","X-Study-Upstream-Model":out["model"]})

def start(handler):
    s=ThreadingHTTPServer(("127.0.0.1",0),handler)
    s.daemon_threads=True
    t=Thread(target=s.serve_forever,daemon=True); t.start()
    return s,t
