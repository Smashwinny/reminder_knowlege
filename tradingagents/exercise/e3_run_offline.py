# -*- coding: utf-8 -*-
"""E3 主实验：零 API key、零网络、零真实资金，离线跑通 TradingAgents 全管线。

思路来自 repo 自带 tests/test_graph_end_to_end.py 的 ScriptedModel + offline
fixture：脚本化 LLM（每次先调用一遍所有绑定的工具，再回一段固定报告文本），
并把 7 家数据供应商全部替换为假数据。跑完后打印：
  - 每个分析师的报告片段
  - 投资计划 / 交易员提案 / 最终决策
  - 决策信号 signal 与五档 Rating
  - 记忆日志落盘内容

免责声明：本实验只验证框架的工程管线，LLM 是脚本假人、数据是假数，
输出"Overweight/BUY"不代表任何真实投资判断。
"""
import copy, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import pandas as pd
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.runnables import RunnableLambda
from pydantic import Field

from tradingagents.agents import context, schemas
from tradingagents.agents.analysts import sentiment_analyst
from tradingagents.dataflows import router
from tradingagents.dataflows.vendors.yahoo import market as yahoo_market, snapshot
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph import trading_graph

TRADE_DATE = "2026-01-09"
TEXT = "Report.\n\n**Rating**: Overweight\n\nFINAL TRANSACTION PROPOSAL: **BUY**"

STRUCTURED = {
    schemas.ResearchPlan: schemas.ResearchPlan(
        recommendation=schemas.PortfolioRating.OVERWEIGHT, rationale="r", strategic_actions="a"),
    schemas.TraderProposal: schemas.TraderProposal(action=schemas.TraderAction.BUY, reasoning="r"),
    schemas.PortfolioDecision: schemas.PortfolioDecision(
        rating=schemas.PortfolioRating.OVERWEIGHT, executive_summary="s", investment_thesis="t"),
    schemas.SentimentReport: schemas.SentimentReport(
        overall_band=schemas.SentimentBand.NEUTRAL, overall_score=5.0, confidence="low", narrative="n"),
}
ARGS = {"symbol": "NVDA", "ticker": "NVDA", "curr_date": TRADE_DATE, "start_date": "2026-01-02",
        "end_date": TRADE_DATE, "indicator": "rsi", "topic": "Fed rate cut", "freq": "quarterly"}


class ScriptedModel(BaseChatModel):
    """脚本假人：带工具时先把每个工具各调一遍，然后交报告文本。"""
    structured: bool = False
    tools: tuple = ()
    calls: list = Field(default_factory=list)
    threads: set = Field(default_factory=set)

    @property
    def _llm_type(self) -> str:
        return "scripted"

    def bind_tools(self, tools, **kwargs):
        return self.model_copy(update={"tools": tuple(tools)})

    def with_structured_output(self, schema, **kwargs):
        if not self.structured:
            raise NotImplementedError
        return RunnableLambda(lambda _: self._count() or STRUCTURED[schema])

    def _count(self):
        self.calls.append(1)

    def _generate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        self._count()
        if self.tools:
            import threading, time
            self.threads.add(threading.current_thread().name)
            time.sleep(0.05)
        if self.tools and not isinstance(messages[-1], ToolMessage):
            calls = [{"name": t.name, "id": f"call_{i}",
                      "args": {k: v for k, v in ARGS.items()
                               if k in t.tool_call_schema.model_json_schema()["properties"]}}
                     for i, t in enumerate(self.tools)]
            message = AIMessage(content="", tool_calls=calls)
        else:
            message = AIMessage(content=TEXT)
        return ChatResult(generations=[ChatGeneration(message=message)])


class _Client:
    def __init__(self, model): self.model = model
    def get_llm(self): return self.model


def make_offline(called):
    """把全部数据供应商方法替换为假数据（记录被命中的路由方法名）。"""
    for method, vendors in router.VENDOR_METHODS.items():
        for name in vendors:  # dict 迭代出的是供应商名（key）
            vendors[name] = (lambda *a, _m=method, **k: called.add(_m) or f"{_m} data")


if __name__ == "__main__":
    # --- 离线化：供应商假数据 ---
    called = set()
    make_offline(called)
    prices = pd.DataFrame({
        "Date": pd.bdate_range(end=TRADE_DATE, periods=60),
        "Open": 100.0, "High": 101.0, "Low": 99.0, "Close": 100.5, "Volume": 1_000_000,
    })
    snapshot.load_ohlcv = lambda *a, **k: called.add("ohlcv") or prices.copy()
    sentiment_analyst.fetch_stocktwits_messages = lambda *a, **k: "no posts"
    sentiment_analyst.fetch_reddit_posts = lambda *a, **k: "no posts"
    yahoo_market.yf.Ticker = lambda s: type("T", (), {"info": {"longName": "NVIDIA"}})()
    context._identity.cache_clear()

    # --- 组图：假 LLM 客户端 ---
    model = ScriptedModel()
    trading_graph.create_llm_client = lambda **k: _Client(model)

    cfg = copy.deepcopy(DEFAULT_CONFIG)
    cfg.update(results_dir=r"F:/reminder/tradingagents/exercise/out/results",
               data_cache_dir=r"F:/reminder/tradingagents/exercise/out/cache",
               memory_log_path=r"F:/reminder/tradingagents/exercise/out/memory_log.md",
               max_debate_rounds=1, max_risk_discuss_rounds=1)
    ta = trading_graph.TradingAgentsGraph(config=cfg, debug=False)

    state, signal = ta.propagate("NVDA", TRADE_DATE)

    print("=== 全管线离线跑通 ===")
    print("决策信号 signal:", signal)
    print("五档评级 final_rating:", state["final_rating"])
    print("LLM 调用次数:", len(model.calls))
    print("分析师并发线程:", sorted(model.threads))
    for key in ("market_report", "sentiment_report", "news_report", "fundamentals_report"):
        print(f"\n[{key}] ->", (state[key] or "").strip().splitlines()[0])
    print("\n[investment_plan]", state["investment_plan"].strip().splitlines()[0])
    print("[trader_investment_plan]", state["trader_investment_plan"].strip().splitlines()[0])
    print("[final_trade_decision]", state["final_trade_decision"].strip().splitlines()[0])

    print("\n=== 数据供应商路由方法（全部被命中）===")
    print(sorted(called))

    print("\n=== 记忆日志落盘 ===")
    for e in ta.memory_log.load_entries():
        print(e)

    assert signal == state["final_rating"] == "Overweight", "管线输出不符合预期"
    print("\n✅ 断言通过：signal == final_rating == 'Overweight'，全管线决策闭环成立")
