# -*- coding: utf-8 -*-
"""E2: 导出 TradingAgents 的 LangGraph 顶层拓扑（节点/边/mermaid），零网络零 API key。

原理：GraphSetup.setup_graph() 只在接线时需要 LLM 对象（存进各节点工厂），
不真正调用。我们传一个哑模型即可编译出整张图，然后用 LangGraph 的
get_graph() 反射出拓扑结构。
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult


class DummyModel(BaseChatModel):
    """从未被真正调用的哑模型（只用于接线）。"""
    @property
    def _llm_type(self) -> str:
        return "dummy"

    def _generate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=""))])


from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph.trading_graph import TradingAgentsGraph

config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openai"  # 不触网；客户端由下面 monkeypatch 顶掉
import tradingagents.graph.trading_graph as tg

class _Client:
    def __init__(self, model): self.model = model
    def get_llm(self): return self.model

tg.create_llm_client = lambda **k: _Client(DummyModel())

ta = TradingAgentsGraph(config=config, debug=False)
g = ta.graph.get_graph()

nodes = sorted(g.nodes)
edges = [(e.source, e.target, getattr(e, "conditional", False) and "cond" or "") for e in g.edges]

print(f"节点数: {len(nodes)}")
for n in nodes:
    print("  -", n)
print(f"\n边数: {len(edges)}")
for s, t, kind in edges:
    print(f"  {s} -> {t} {('[条件边]' if kind else '')}")

mermaid = g.draw_mermaid()
with open(r"F:/reminder/tradingagents/exercise/graph_topology.mmd", "w", encoding="utf-8") as f:
    f.write(mermaid)
print("\nmermaid 已存 exercise/graph_topology.mmd，前 12 行：")
print("\n".join(mermaid.splitlines()[:12]))
