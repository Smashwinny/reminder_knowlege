# -*- coding: utf-8 -*-
"""
主实验：用 NautilusTrader 跑一个 AUD/USD 的 EMA 双均线交叉回测（真实数据 + 自己的策略代码）。

数据：repo/test_data/truefx/audusd-ticks.csv（100,000 条真实 tick 报价）
用法：python ema_cross_backtest.py [fast] [slow]
  例：python ema_cross_backtest.py 10 20
"""
import sys
from pathlib import Path

import pandas as pd

from nautilus_trader.backtest.engine import BacktestEngine
from nautilus_trader.backtest.models import MakerTakerFeeModel
from nautilus_trader.config import MakerTakerFeeModelConfig
from nautilus_trader.config import BacktestEngineConfig
from nautilus_trader.config import RiskEngineConfig
from nautilus_trader.config import StrategyConfig
from nautilus_trader.indicators import ExponentialMovingAverage
from nautilus_trader.model.data import BarType
from nautilus_trader.model.data import QuoteTick
from nautilus_trader.model.enums import AccountType
from nautilus_trader.model.enums import OmsType
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.identifiers import TraderId
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.objects import Currency
from nautilus_trader.model.objects import Money
from nautilus_trader.model.objects import Quantity
from nautilus_trader.persistence.wranglers import QuoteTickDataWrangler
from nautilus_trader.test_kit.providers import TestInstrumentProvider
from nautilus_trader.trading.strategy import Strategy

DATA_CSV = Path(__file__).resolve().parents[1] / "repo" / "test_data" / "truefx" / "audusd-ticks.csv"
SIM = Venue("SIM")


def load_ticks() -> tuple[object, list[QuoteTick]]:
    """CSV -> pandas -> QuoteTickDataWrangler -> list[QuoteTick]（纳秒级时间戳）。"""
    instrument = TestInstrumentProvider.default_fx_ccy("AUD/USD", venue=SIM)
    raw = pd.read_csv(DATA_CSV)
    ts = pd.to_datetime(raw["timestamp"], format="mixed", utc=True)
    df = pd.DataFrame(
        {
            "timestamp": ts,
            "bid_price": raw["bid"].astype(float),
            "ask_price": raw["ask"].astype(float),
            "bid_size": 100_000.0,  # truefx 数据没有量，补一个常量
            "ask_size": 100_000.0,
        }
    )
    df = df[~df["timestamp"].duplicated(keep="first")]  # CSV 里有重复时间戳
    df = df.set_index("timestamp")
    wrangler = QuoteTickDataWrangler(instrument=instrument)
    ticks = wrangler.process(df)
    return instrument, ticks


class EMACrossConfig(StrategyConfig, frozen=True):
    instrument_id: str
    bar_type: str
    fast_ema_period: int = 10
    slow_ema_period: int = 20
    trade_size: int = 100_000


class EMACross(Strategy):
    """快线上穿慢线做多，下穿做空；每次信号先平仓再反手。"""

    def __init__(self, config: EMACrossConfig) -> None:
        super().__init__(config)
        self.instrument_id = InstrumentId.from_str(config.instrument_id)
        self.bar_type = BarType.from_str(config.bar_type)
        self.trade_size = Quantity(config.trade_size, 0)
        self.fast_ema = ExponentialMovingAverage(config.fast_ema_period)
        self.slow_ema = ExponentialMovingAverage(config.slow_ema_period)
        self.register_indicator_for_bars(self.bar_type, self.fast_ema)
        self.register_indicator_for_bars(self.bar_type, self.slow_ema)
        self.prev_diff: float | None = None
        self.signal_count = 0

    def on_start(self) -> None:
        self.subscribe_bars(self.bar_type)

    def on_bar(self, bar) -> None:
        if not (self.fast_ema.initialized and self.slow_ema.initialized):
            return
        diff = self.fast_ema.value - self.slow_ema.value
        if self.prev_diff is None:
            self.prev_diff = diff
            return
        crossed_up = self.prev_diff <= 0 < diff
        crossed_down = self.prev_diff >= 0 > diff
        self.prev_diff = diff
        if crossed_up or crossed_down:
            self.signal_count += 1
            self.close_all_positions(instrument_id=self.instrument_id)
            side = OrderSide.BUY if crossed_up else OrderSide.SELL
            order = self.order_factory.market(
                instrument_id=self.instrument_id,
                order_side=side,
                quantity=self.trade_size,
            )
            self.submit_order(order)

    def on_stop(self) -> None:
        self.close_all_positions(instrument_id=self.instrument_id)


def money_sum(series) -> float:
    """报表里的 Money 列是 '123.45 USD' 字符串（个别是单元素列表），正则提取数字求和。"""
    import re

    total = 0.0
    for x in series:
        m = re.search(r"-?\d+\.?\d*", str(x))
        if m:
            total += float(m.group(0))
    return round(total, 2)


def run(fast: int, slow: int) -> dict:
    instrument, ticks = load_ticks()

    config = BacktestEngineConfig(
        trader_id=TraderId("BACKTESTER-001"),
        risk_engine=RiskEngineConfig(bypass=True),
    )
    engine = BacktestEngine(config=config)
    USD = Currency.from_str("USD")
    engine.add_venue(
        venue=SIM,
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        base_currency=USD,
        starting_balances=[Money(1_000_000, USD)],
        # 手续费率用合约自带的 maker/taker=0.00002（ MakerTakerFeeModel 从合约读取）
        fee_model=MakerTakerFeeModel(MakerTakerFeeModelConfig()),
    )
    engine.add_instrument(instrument)
    engine.add_data(ticks)

    strategy = EMACross(
        EMACrossConfig(
            instrument_id=str(instrument.id),
            bar_type="AUD/USD.SIM-1-MINUTE-MID-INTERNAL",
            fast_ema_period=fast,
            slow_ema_period=slow,
            trade_size=100_000,
        ),
    )
    engine.add_strategy(strategy)
    engine.run()

    fills = engine.trader.generate_order_fills_report()
    positions = engine.trader.generate_positions_report()
    account = engine.trader.generate_account_report(SIM)

    result = {
        "fast": fast,
        "slow": slow,
        "ticks": len(ticks),
        "first_ts_ns": int(ticks[0].ts_event),
        "signals": strategy.signal_count,
        "fills": len(fills),
        "closed_positions": len(positions),
        "realized_pnl": money_sum(positions["realized_pnl"]) if len(positions) else 0.0,
        "commissions": money_sum(positions["commissions"]) if len(positions) else 0.0,
        "final_balance": money_sum(account["total"].iloc[-1:]) if len(account) else None,
    }
    engine.reset()
    engine.dispose()
    return result


if __name__ == "__main__":
    fast = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    slow = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    r = run(fast, slow)
    print("=== EMA 交叉回测结果 ===")
    for k, v in r.items():
        print(f"{k:>16}: {v}")
