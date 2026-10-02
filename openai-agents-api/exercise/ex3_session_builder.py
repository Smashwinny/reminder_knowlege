# ex3: Session 请求体构造器 + 契约自校验（四概念 → 请求体 JSON 的映射，零 key 零费用）
import json

ENV_TYPES = {"none", "openai_hosted", "self_hosted"}
TOOL_TYPES = {"programmatic_tool_calling", "mcp", "web_search", "function", "browser"}

def build_session(model, instructions, env_type, tools, input_text,
                  multi_agent=None, workspace=None):
    assert env_type in ENV_TYPES, f"环境类型非法: {env_type}（只允许 {ENV_TYPES}）"
    agent = {"model": model, "instructions": instructions, "tools": []}
    for t in tools:
        assert t["type"] in TOOL_TYPES, f"工具类型非法: {t['type']}"
        agent["tools"].append(t)
    if multi_agent:
        agent["multi_agent"] = multi_agent
    body = {"agent": agent, "environment": {"type": env_type}, "input": input_text}
    if env_type == "self_hosted":
        assert workspace, "self_hosted 必须给 workspace_directory（executor 的根）"
        body["environment"]["workspace_directory"] = workspace
    return body

def validate(body):
    """契约检查：环境三态互斥、multi_agent 限并发、none 环境禁自带工作区"""
    errs = []
    env = body["environment"]
    if env["type"] not in ENV_TYPES:
        errs.append(f"环境类型 {env['type']} 不在三态枚举内")
    if env["type"] == "none" and "workspace_directory" in env:
        errs.append("none 环境没有工作区（无 Bash/apply-patch/executor MCP）")
    ma = body["agent"].get("multi_agent")
    if ma and (not isinstance(ma.get("max_concurrent_subagents"), int) or ma["max_concurrent_subagents"] < 1):
        errs.append("multi_agent.max_concurrent_subagents 必须为正整数")
    return errs

# --- 三个场景：对应官方文档三种架构 ---
cases = {
  "A 问答型(no sandbox)": build_session(
      "gpt-6-astra", "只回答问题，不执行代码", "none",
      [{"type": "web_search"}], "OpenAI Agents API 是什么？"),
  "B 编码型(openai_hosted沙箱)": build_session(
      "gpt-6-astra", "写代码、跑起来、报告真实输出", "openai_hosted",
      [{"type": "programmatic_tool_calling"}], "写 tree.py 并运行"),
  "C 私网型(self_hosted executor)": build_session(
      "gpt-6-astra", "操作内网数据库", "self_hosted",
      [{"type": "mcp", "server_label": "db", "transport": {"type": "http", "server_url": "http://10.0.0.5:8000/mcp"}}],
      "查最近10条订单", multi_agent={"enabled": True, "max_concurrent_subagents": 4},
      workspace="/workspace"),
}
for name, body in cases.items():
    errs = validate(body)
    print(f"[{name}] 契约检查: {'PASS' if not errs else 'FAIL ' + str(errs)}")

# --- 负向用例：构造非法请求体，验证校验器真的能拦 ---
bad = {"agent": {"model": "x", "instructions": "y", "tools": []},
       "environment": {"type": "none", "workspace_directory": "/ws"}, "input": "hi"}
errs = validate(bad)
assert errs, "校验器失效！"
print(f"[负向] none环境带工作区 -> 被拦截: {errs}")

with open("session_bodies.json", "w", encoding="utf-8") as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)
print("\n三份合法请求体已存 session_bodies.json")
print(json.dumps(cases["C 私网型(self_hosted executor)"], ensure_ascii=False, indent=2)[:400])
