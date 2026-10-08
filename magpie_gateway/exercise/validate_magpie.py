# -*- coding: utf-8 -*-
"""magpie 宣称校验器 —— 学习实验。

校验推文/README 宣称的结构真实性（纯读取，Go 工具链本机未装不跑测试）：
  1. 四种协议处理器存在：OpenAI Chat(chat.go)/Responses(responses.go)/Anthropic(anthropic.go)/Gemini(gemini.go)
  2. 本地网关端口 3425 在 agent 适配器中引用
  3. 订阅共享实现：claude_subscription.go + claudebridge/mcp.go（MCP 桥接）
  4. 供应商预设含国产模型（balance.go DeepSeek/Kimi 等按 host 识别）
  5. 原子化配置手术：agent 包内各 Agent 适配器存在（cindy 等 40+）
  6. 工程规模：测试文件数（宣称高密度）

用法： python validate_magpie.py
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent / "repo"


def check(name, ok, detail):
    print(f"  {'✅' if ok else '❌'} {name}: {detail}")
    return (name, ok, detail)


def main():
    gw = REPO / "internal/gateway"
    cases = []

    protos = {
        "OpenAI Chat": gw / "chat.go",
        "OpenAI Responses": gw / "responses.go",
        "Anthropic": gw / "anthropic.go",
        "Gemini": gw / "gemini.go",
    }
    hits = [k for k, p in protos.items() if p.exists() and p.stat().st_size > 2000]
    cases.append(check(f"T1 四协议处理器 {len(hits)}/4", len(hits) == 4, ",".join(hits)))

    port_refs = list((REPO / "internal/agent").rglob("*.go"))
    n3425 = sum(1 for f in port_refs if "3425" in f.read_text(encoding="utf-8", errors="ignore"))
    cases.append(check("T2 端口 3425 在 agent 适配器引用", n3425 >= 3, f"{n3425} 个文件引用"))

    sub_ok = (gw / "claude_subscription.go").exists() and (REPO / "internal/claudebridge/mcp.go").exists()
    mcp_size = (REPO / "internal/claudebridge/mcp.go").stat().st_size if (REPO / "internal/claudebridge/mcp.go").exists() else 0
    cases.append(check("T3 订阅共享(MCP桥)", sub_ok, f"claude_subscription.go + mcp.go({mcp_size}B)"))

    bal = (REPO / "internal/provider/balance.go").read_text(encoding="utf-8", errors="ignore")
    providers = re.findall(r'api\.(deepseek\.com|moonshot\.cn|openrouter\.ai|siliconflow\.cn)', bal)
    cases.append(check(f"T4 供应商 host 识别 {len(set(providers))} 家", len(set(providers)) >= 3,
                       ",".join(sorted(set(providers)))))

    agent_dir = REPO / "internal/agent"
    adapters = [f for f in agent_dir.glob("*.go")
                if not f.name.endswith("_test.go") and f.name[0].islower()]
    cases.append(check(f"T5 Agent 适配器 {len(adapters)} 个", len(adapters) >= 30,
                       f"例:{sorted(a.name for a in adapters)[:5]}"))

    tests = list(REPO.rglob("*_test.go"))
    cases.append(check(f"T6 测试文件 {len(tests)} 个", len(tests) >= 1000, f"全仓 {len(tests)}"))

    passed = sum(1 for _, ok, _ in cases if ok)
    print(f"\n测试结果：{passed}/{len(cases)} 通过")
    go_files = list(REPO.rglob("*.go"))
    print(f"工程统计：Go 文件 {len(go_files)}，测试 {len(tests)}，internal 包 {len(list((REPO/'internal').iterdir()))} 个")
    return passed == len(cases)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
