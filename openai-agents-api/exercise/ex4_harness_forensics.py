# ex4: openai/codex 开源 harness 源码取证——推文五大能力逐个找到源码坐标
import os, re, json

REPO = r"F:\reminder\openai-agents-api\repo"
RS = os.path.join(REPO, "codex-rs")

stats = {"crates": len(os.listdir(RS)), "rs_files": 0, "loc": 0}
for root, _, files in os.walk(RS):
    for f in files:
        if f.endswith(".rs"):
            stats["rs_files"] += 1
            try:
                with open(os.path.join(root, f), encoding="utf-8", errors="ignore") as fh:
                    stats["loc"] += sum(1 for _ in fh)
            except OSError:
                pass
print(f"== 仓库规模: {stats['crates']} crates / {stats['rs_files']} 个 .rs / {stats['loc']:,} 行 ==")

def first_hit(rel_paths, pattern):
    for rel in rel_paths:
        p = os.path.join(RS, rel)
        if not os.path.exists(p):
            continue
        try:
            with open(p, encoding="utf-8", errors="ignore") as fh:
                for i, line in enumerate(fh, 1):
                    if re.search(pattern, line, re.I):
                        return rel, i, line.strip()[:110]
        except OSError:
            continue
    return None, None, None

evidence = {
  "① 长任务上下文压缩": (["core/src/compact.rs", "core/src/tasks/compact.rs",
      "core/src/compact_token_budget.rs"], r"CompactionReason|auto_compact|token_budget"),
  "② 工具/MCP": (["rmcp-client/src/lib.rs", "tools/src/dynamic_tool.rs",
      "tools/src/code_mode.rs"], r"rmcp|McpTool|code_mode"),
  "③ Subagent 编排": (["core/src/agent/control/execution.rs",
      "core/src/agent/child_config.rs", "agent-roles/src/lib.rs"], r"subagent|concurrent|max_concurrent"),
  "④ 沙箱执行": (["sandboxing/src/lib.rs", "windows-sandbox-rs/src/lib.rs",
      "linux-sandbox/src/lib.rs", "mxc-sandbox/src/lib.rs"], r"pub fn|sandbox"),
  "⑤ 云端会话恢复": (["cloud-tasks/src/lib.rs", "rollout/src/lib.rs",
      "core/src/codex_thread.rs"], r"resume|rollout|thread"),
}
print("\n== 五能力 -> 源码坐标 ==")
out = {}
for cap, (paths, pat) in evidence.items():
    rel, ln, line = first_hit(paths, pat)
    ok = "FOUND" if rel else "MISS"
    print(f"  {cap}: [{ok}] {rel}:{ln}")
    if line: print(f"      > {line}")
    out[cap] = {"file": rel, "line": ln, "snippet": line}

# 关键 crate 家族清点
fams = {"sandbox 家族": [d for d in os.listdir(RS) if "sandbox" in d],
        "code-mode 家族": [d for d in os.listdir(RS) if "code-mode" in d],
        "agent 家族": [d for d in os.listdir(RS) if d.startswith("agent")],
        "compact 相关文件": [f for f in os.listdir(os.path.join(RS, "core/src")) if f.startswith("compact")]}
print("\n== 关键 crate 家族 ==")
for k, v in fams.items():
    print(f"  {k}: {v}")

with open("harness_forensics.json", "w", encoding="utf-8") as f:
    json.dump({"stats": stats, "evidence": {k: v for k, v in out.items()}, "families": fams},
              f, ensure_ascii=False, indent=2)
print("\n取证结果已存 harness_forensics.json")
