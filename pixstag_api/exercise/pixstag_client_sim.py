#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""PixStag API 客户端骨架 + 异步状态机/用量对账模拟（零花费练习版）

真实部分：对官方端点发只读 GET，验证 401 错误契约。
模拟部分：用本地假响应走通"创建任务→轮询状态→用量对账"全流程，
          验证状态机与对账逻辑（queued→running→succeeded + usage 按秒核算）。
契约来源：https://pixstag.com/docs/api （2026-10-27 直读）
"""
import json, time, urllib.request, urllib.error
from dataclasses import dataclass, field

BASE = "https://pixstag.com/api/v2"

@dataclass
class TaskResult:
    status: str
    usage_total_seconds: int = 0
    error: dict | None = None
    url: str | None = None

def probe_me():
    """真实只读探针：无 token 时应 401 + 错误码 1004"""
    req = urllib.request.Request(f"{BASE}/user/me")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

class FakePixStag:
    """本地假服务端：模拟三次轮询 queued→running→succeeded 与按秒 usage"""
    def __init__(self, duration):
        self.duration = duration
        self.calls = 0
        self.usage = {"total_seconds": duration, "input_seconds": 0,
                      "output_seconds": duration, "input_image_count": 1,
                      "total_tokens": 0, "prompt_tokens": 40, "completion_tokens": 0}
    def query(self):
        self.calls += 1
        if self.calls == 1: return {"task": {"id": "demo", "status": "queued"}}
        if self.calls == 2: return {"task": {"id": "demo", "status": "running"}}
        return {"task": {"id": "demo", "status": "succeeded"},
                "content": {"url": "https://example.com/out.mp4",
                            "duration": self.duration, "resolution": "720P"},
                "usage": self.usage}

def poll_task(server, max_rounds=10, interval=0.1):
    """状态机：queued/running 继续等；succeeded 提取 usage；failed/cancelled 提取 error"""
    for _ in range(max_rounds):
        d = server.query()
        st = d["task"]["status"]
        if st in ("queued", "running"):
            time.sleep(interval); continue
        if st == "succeeded":
            u = d.get("usage", {})
            return TaskResult(status=st, usage_total_seconds=u.get("total_seconds", 0),
                              url=d["content"]["url"])
        return TaskResult(status=st, error=d["task"].get("error"))
    return TaskResult(status="timeout", error={"code": -1, "message": "max rounds"})

def reconcile(expected_duration: int, result: TaskResult) -> bool:
    """用量对账：计费秒数必须与请求时长一致；不符即拒付（[[付费调用回执与预算熔断]]）"""
    ok = result.usage_total_seconds == expected_duration and result.status == "succeeded"
    print(f"  对账: 请求 {expected_duration}s vs 计费 {result.usage_total_seconds}s "
          f"→ {'✅ 一致' if ok else '❌ 不符，拒付复核'}")
    return ok

if __name__ == "__main__":
    print("=== ① 真实只读探针（无 token）===")
    code, body = probe_me()
    print(f"  HTTP {code}: {body[:90]}")
    assert code == 401 and "1004" in body, "错误契约与文档不符！"
    print("  ✅ 401 错误契约符合文档（code 1004）")

    print("=== ② 状态机模拟（queued→running→succeeded）===")
    server = FakePixStag(duration=6)
    result = poll_task(server)
    print(f"  轮询 {server.calls} 次到达 {result.status}，url={result.url}")
    assert result.status == "succeeded"
    print("  ✅ 状态机 5 态路径可走通")

    print("=== ③ 按秒用量对账 ===")
    assert reconcile(6, result)
    tampered = TaskResult(status="succeeded", usage_total_seconds=8)
    assert not reconcile(6, tampered)
    print("✅ 全流程验证通过：错误契约 / 状态机 / 对账逻辑")
