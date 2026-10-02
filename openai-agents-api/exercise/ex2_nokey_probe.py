# ex2: 无 key 真请求——验证 /v1/agents/sessions 端点真实存在（期待 401，而非 404）
import httpx, json, os

url = "https://api.openai.com/v1/agents/sessions"
body = {
    "agent": {"model": "gpt-6-astra", "instructions": "ping"},
    "environment": {"type": "none"},
    "input": "hello",
}

print("== 探测1：完全不带 Authorization ==")
r = httpx.post(url, headers={"OpenAI-Beta": "agents=v1"}, json=body, timeout=30)
print("  HTTP", r.status_code, "->", r.text.strip()[:200])

print("== 探测2：带假 key ==")
r2 = httpx.post(url, headers={"OpenAI-Beta": "agents=v1", "Authorization": "Bearer sk-fake-xxxx"},
                json=body, timeout=30)
print("  HTTP", r2.status_code, "->", r2.text.strip()[:200])

print("== 探测3：对照组——同 key 打不存在的端点 ==")
r3 = httpx.post("https://api.openai.com/v1/nonexistent-agents-xyz",
                headers={"OpenAI-Beta": "agents=v1", "Authorization": "Bearer sk-fake-xxxx"},
                json=body, timeout=30)
print("  HTTP", r3.status_code, "->", r3.text.strip()[:200])
