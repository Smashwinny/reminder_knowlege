# -*- coding: utf-8 -*-
"""E4: 辩论路由器 ConditionalLogic 微实验（纯逻辑，无 LLM 无网络）。
   E5: 记忆日志 TradingMemoryLog 存储 + 结算幂等性实验（无 LLM）。

E4 验证：
  - 多空辩论：Bull 说完接 Bear，Bear 说完接 Bull，计数到 2*rounds 交给 Research Manager
  - 风险辩论：Aggressive→Conservative→Neutral 三方轮转，3*rounds 后交 Portfolio Manager
E5 验证：
  - store_decision 落盘 markdown、状态 pending
  - 同一 (date,ticker) 重复 store 被幂等挡掉
  - settle 后条目带 raw/alpha 回报，状态不再 pending
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import tempfile, os

from tradingagents.agents.state import AgentState
from tradingagents.graph.conditional_logic import ConditionalLogic

print("========== E4 辩论路由器 ==========")
cl = ConditionalLogic(max_debate_rounds=1, max_risk_discuss_rounds=1)

def debate_state(count, speaker):
    return {"investment_debate_state": {"count": count, "current_response": speaker},
            "risk_debate_state": {"count": count, "latest_speaker": speaker}}

# 多空辩论走查：从 Bull 开场，看路由序列
seq, count, speaker = [], 0, "Bull"
for _ in range(10):
    nxt = cl.should_continue_debate(debate_state(count, speaker))
    if nxt == "Research Manager":
        seq.append("Research Manager"); break
    seq.append(nxt)
    speaker = "Bull" if nxt.startswith("Bull") else "Bear"
    count += 1
print("max_debate_rounds=1 时的路由序列:", " -> ".join(seq))
assert seq == ["Bear Researcher", "Bull Researcher", "Research Manager"], seq
print("✅ Bull→Bear→Bull（每人1次，2*1=2 计满）→ Research Manager")

# 风险辩论走查（Trader 先固定咨询 Aggressive，它说完 count=1）
seq, count, speaker = [], 1, "Aggressive"
for _ in range(12):
    nxt = cl.should_continue_risk_analysis(debate_state(count, speaker))
    if nxt == "Portfolio Manager":
        seq.append("Portfolio Manager"); break
    seq.append(nxt)
    speaker = nxt.replace(" Analyst", "")
    count += 1
print("max_risk_discuss_rounds=1 时的路由序列:", " -> ".join(seq))
assert seq == ["Conservative Analyst", "Neutral Analyst", "Portfolio Manager"], seq
print("✅ Aggressive 开场后 Conservative→Neutral（3*1=3 计满）→ Portfolio Manager")

print("\n========== E5 记忆日志 ==========")
from tradingagents.memory import TradingMemoryLog

with tempfile.TemporaryDirectory() as tmp:
    log_path = os.path.join(tmp, "log.md")
    mem = TradingMemoryLog({"memory_log_path": log_path})

    mem.store_decision("NVDA", "2026-01-09", "DECISION:\nBUY, Overweight. FINAL TRANSACTION PROPOSAL: **BUY**",
                       rating="Overweight")
    mem.store_decision("NVDA", "2026-01-09", "DECISION:\n重复写入应被挡掉", rating="Overweight")  # 幂等
    entries = mem.load_entries()
    print("写入 2 次后条目数:", len(entries), "（幂等性：应为 1）")
    assert len(entries) == 1
    print("条目状态:", entries[0]["pending"], "| rating:", entries[0]["rating"])

    mem.update_with_outcome("NVDA", "2026-01-09", raw_return=0.031, alpha_return=0.012,
                            holding_days=5, reflection="教训：样本窗口太短，别把周线波动当日线信号。")
    entries = mem.load_entries()
    e = entries[0]
    print(f"结算后: pending={e['pending']} raw={e['raw']} alpha={e['alpha']} holding={e['holding']}")
    assert e["pending"] is False and e["alpha"] == "+1.2%" and e["raw"] == "+3.1%"

    print("\n落盘 markdown 原文：")
    print(open(log_path, encoding="utf-8").read())

print("✅ E5 通过：存储→幂等挡重→结算→状态翻转 全链路成立")
