# ex1: 官方 SDK 内省取证——证明 Agents API 真实存在于 openai 官方 SDK（无 key，不发请求）
from openai import OpenAI
import inspect

c = OpenAI(api_key="sk-dummy-introspection-only")
ag = c.beta.agents

print("== beta.agents 资源命名空间 ==")
for name in ["agents", "sessions", "environments", "vaults"]:
    obj = getattr(ag, name, None)
    print(f"  {name}: {'OK' if obj else 'MISSING'}")

print("\n== sessions 子资源 ==")
for name in ["turns", "events", "items", "subagents", "artifacts", "traces", "stream"]:
    print(f"  {name}: {'OK' if hasattr(ag.sessions, name) else 'MISSING'}")

print("\n== sessions.create 签名 ==")
sig = inspect.signature(ag.sessions.create)
print(" ", sig)

print("\n== sessions.create 参数模型（model_fields）==")
import openai.types.beta as bt
import openai
mods = [m for m in dir(openai.types.beta) if 'agent' in m.lower()]
print("  openai.types.beta 中 agent 相关类型:", len(mods), "个")
for m in sorted(mods)[:25]:
    print("   -", m)
