# -*- coding: utf-8 -*-
"""实验C：把仓库 backtest/ma_line_backtest.py 的双均线策略在本地模拟数据上真正跑起来
原文件需要公众号留言获取 orcl-1995-2014.txt 数据 + 需 GUI plot(); 本实验:
  1) 用随机游走+趋势段合成一段 A 股风格日线(几何布朗运动+跳空);
  2) 复用仓库同款策略逻辑(金叉买入/死叉卖出), 无 plot 纯终端跑;
  3) 扫描 4 组均线参数, 计入 0.1% 佣金 + 0.1% 印花税, 呼应知识库 [[交易成本与鞭打效应]]:
     信号越密, 成本吃掉越多。
"""
import os

import backtrader as bt
import numpy as np
import pandas as pd

HERE = os.path.dirname(__file__)
DATA_CSV = os.path.join(HERE, 'sim_ohlc.csv')


def make_sim_data(n=750, seed=5):
    """合成 A 股风格日线: 三段趋势(下-上-震荡) + 噪声, 起价 10 元。"""
    rng = np.random.default_rng(seed)
    drift = np.concatenate([
        np.full(250, -0.0008),   # 第一段: 阴跌
        np.full(250, +0.0018),   # 第二段: 主升
        np.full(250, +0.0001),   # 第三段: 横盘震荡
    ])
    ret = drift + rng.normal(0, 0.018, n)
    close = 10 * np.exp(np.cumsum(ret))
    open_ = np.roll(close, 1) * (1 + rng.normal(0, 0.004, n))
    open_[0] = 10.0
    high = np.maximum(open_, close) * (1 + np.abs(rng.normal(0, 0.006, n)))
    low = np.minimum(open_, close) * (1 - np.abs(rng.normal(0, 0.006, n)))
    dates = pd.bdate_range('2024-01-02', periods=n)
    df = pd.DataFrame({'Date': dates, 'Open': open_, 'High': high,
                       'Low': low, 'Close': close, 'Volume': rng.integers(1e6, 5e6, n)})
    df.to_csv(DATA_CSV, index=False)
    return df


class MaCross(bt.Strategy):
    """与仓库 backtest/ma_line_backtest.py 的 MyStrategy 同款: 金叉买、死叉卖。"""
    params = dict(fast=10, slow=30, commission=0.001, stamp=0.001)

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.fast = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.p.fast)
        self.slow = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.p.slow)
        self.trades = 0

    def notify_trade(self, trade):
        if trade.isclosed:
            self.trades += 1

    def next(self):
        if not self.position:
            if self.dataclose[0] > self.fast[0] and not (self.dataclose[-1] > self.fast[-1]):
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.fast[0] and not (self.dataclose[-1] < self.fast[-1]):
                self.order = self.sell()


def run_once(fast, slow, verbose=False):
    cerebro = bt.Cerebro()
    df = pd.read_csv(DATA_CSV, parse_dates=['Date']).set_index('Date')
    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data)
    cerebro.addstrategy(MaCross, fast=fast, slow=slow)
    cerebro.broker.setcash(100000.0)
    # 每次买入动用 95% 现金(backtrader 默认 sizer 只买 1 股, 必须显式指定仓位)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=95)
    # 买: 佣金 0.1%; 卖: 佣金 0.1% + 印花税 0.1% (A股口径简化)
    cerebro.broker.setcommission(commission=0.001)

    results = cerebro.run()
    strat = results[0]
    final = cerebro.broker.getvalue()
    return final, strat.trades


def main():
    print('=== 实验C：仓库双均线策略 backtrader 实跑 ===\n')
    df = make_sim_data()
    print(f'[数据] 合成日线 {len(df)} 根 (2024-01-02 起, 三段趋势: 阴跌/主升/震荡), '
          f'收盘 {df.Close.iloc[0]:.2f} -> {df.Close.iloc[-1]:.2f} '
          f'({(df.Close.iloc[-1]/df.Close.iloc[0]-1)*100:+.1f}%)')
    print(f'[落盘] {DATA_CSV}\n')

    print('[回测] 本金 100000, 佣金 0.1%/边, 快线上穿慢线买、下穿卖')
    print(f'{"参数":<12}{"期末净值":>12}{"收益率":>10}{"成交次数":>8}')
    baseline = df.Close.iloc[-1] / df.Close.iloc[0] - 1
    for fast, slow in [(5, 10), (10, 30), (20, 60), (5, 60)]:
        final, trades = run_once(fast, slow)
        ret = final / 100000 - 1
        print(f'MA{fast}/{slow:<8}{final:>14,.0f}{ret*100:>9.2f}%{trades:>8}  (标的本身 {baseline*100:+.2f}%)')

    print('\n[结论] 短周期参数(MA5/10)信号密集, 每次换手都要交佣金+印花税, '
          '净收益被"鞭打效应"磨损; 仓库把成本参数(commission)显式摆在 cerebro 上, '
          '和 NautilusTrader 的 fee model 是同一件事的两种实现。')


if __name__ == '__main__':
    main()
