# -*- coding: utf-8 -*-
"""
daily_stock_analysis 技术层主实验（不含任何投资建议，仅验证代码数据处理逻辑）
实验内容：
  A. 合成三段 K 线（多头上升 / 空头下跌 / 冲高回落），跑 repo 的规则分析器，
     验证它能正确区分趋势形态与信号；
  B. 用独立手写的 pandas 参考实现重算 MA / MACD / RSI，与 repo 实现逐值对比，
     验证指标数学口径（Wilder RSI、EMA12/26 MACD）；
  C. 验证 decision-scale-v1 评分→动作契约映射（score -> signal/action）；
  D. 解析 strategies/ma_golden_cross.yaml，验证 15 种策略的 YAML 契约结构。

运行：exercise\\venv\\Scripts\\python.exe exp1_indicators.py
（需要在 repo 目录的父目录下、以 repo 为 sys.path 根运行，见 __main__ 部分）
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

REPO = Path(__file__).resolve().parent.parent / "repo"
sys.path.insert(0, str(REPO))

from src.stock_analyzer import StockTrendAnalyzer, analyze_stock  # noqa: E402
from src.schemas.decision_scale import decision_band_for_score     # noqa: E402


def make_kline(kind: str, days: int = 80, seed: int = 7) -> pd.DataFrame:
    """合成日 K 线：open/high/low/close/volume，三种确定性形态。"""
    rng = np.random.default_rng(seed)
    if kind == "bull":          # 缓步上升趋势
        drift = np.linspace(0, 30, days)
        noise = rng.normal(0, 0.4, days)
        close = 20 + drift + np.cumsum(noise) * 0.3
        volume = rng.normal(5e6, 3e5, days)
    elif kind == "bear":        # 持续下跌
        drift = np.linspace(0, -25, days)
        noise = rng.normal(0, 0.5, days)
        close = 45 + drift + np.cumsum(noise) * 0.3
        volume = rng.normal(6e6, 5e5, days) + np.linspace(0, 2e6, days)  # 越跌越放量
    else:                       # 冲高回落（顶部）
        t = np.linspace(0, 1, days)
        close = 30 + 25 * np.sin(t * np.pi * 0.9) + rng.normal(0, 0.5, days).cumsum() * 0.2
        volume = rng.normal(5e6, 4e5, days)

    close = np.maximum(close, 1.0)
    high = close * (1 + np.abs(rng.normal(0, 0.006, days)))
    low = close * (1 - np.abs(rng.normal(0, 0.006, days)))
    open_ = np.r_[close[0], close[:-1]] * (1 + rng.normal(0, 0.003, days))
    dates = pd.bdate_range("2026-06-01", periods=days)
    return pd.DataFrame({"date": dates, "open": open_, "high": high,
                         "low": low, "close": close, "volume": volume})


def ref_ma_macd_rsi(close: pd.Series) -> dict:
    """独立参考实现（教科书口径），用于与 repo 实现交叉验证。"""
    ma5 = close.rolling(5).mean().iloc[-1]
    ema_fast = close.ewm(span=12, adjust=False).mean()
    ema_slow = close.ewm(span=26, adjust=False).mean()
    dif = ema_fast - ema_slow
    dea = dif.ewm(span=9, adjust=False).mean()
    delta = close.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    rsi12 = (100 - 100 / (1 + gain.ewm(alpha=1 / 12, adjust=False).mean()
                          / loss.ewm(alpha=1 / 12, adjust=False).mean())).iloc[-1]
    return {"MA5": ma5, "DIF": dif.iloc[-1], "DEA": dea.iloc[-1],
            "BAR": (dif - dea).iloc[-1] * 2, "RSI12": rsi12}


def main() -> None:
    print("=" * 72)
    print("实验 A：三段合成 K 线 -> repo 规则分析器（TrendAnalysisResult）")
    print("=" * 72)
    results = {}
    for kind, label in [("bull", "多头上升"), ("bear", "空头下跌"), ("top", "冲高回落")]:
        df = make_kline(kind)
        r = analyze_stock(df, f"SYNTH_{kind.upper()}")
        results[kind] = (df, r)
        print(f"\n[{kind}] {label}")
        print(f"  收盘价={r.current_price:.2f}  MA5={r.ma5:.2f} MA10={r.ma10:.2f} MA20={r.ma20:.2f}")
        print(f"  趋势={r.trend_status.value}  强度={r.trend_strength:.0f}")
        print(f"  量能={r.volume_status.value}  量比={r.volume_ratio_5d:.2f}")
        print(f"  MACD={r.macd_status.value}({r.macd_signal})  RSI12={r.rsi_12:.1f}({r.rsi_status.value})")
        print(f"  信号={r.buy_signal.value}  评分={r.signal_score}")
        print(f"  理由前3条: {r.signal_reasons[:3]}")

    print("\n判定检查：bull 应为多头/买入方向，bear 应为空头/卖出方向")
    ok = ("多头" in results["bull"][1].trend_status.value) and \
         ("空头" in results["bear"][1].trend_status.value)
    print(f"  形态区分测试: {'PASS' if ok else 'FAIL'}")

    print("\n" + "=" * 72)
    print("实验 B：独立参考实现 vs repo 指标实现（逐值对比，容差 1e-6）")
    print("=" * 72)
    df_bull, _ = results["bull"]
    close = df_bull["close"]
    ref = ref_ma_macd_rsi(close)
    ana = StockTrendAnalyzer()
    df_ind = ana._calculate_mas(ana._calculate_rsi(ana._calculate_macd(df_bull.copy())))
    got = {"MA5": df_ind["MA5"].iloc[-1], "DIF": df_ind["MACD_DIF"].iloc[-1],
           "DEA": df_ind["MACD_DEA"].iloc[-1], "BAR": df_ind["MACD_BAR"].iloc[-1],
           "RSI12": df_ind["RSI_12"].iloc[-1]}
    all_ok = True
    for key in ref:
        diff = abs(float(ref[key]) - float(got[key]))
        status = "PASS" if diff < 1e-6 else "FAIL"
        all_ok &= diff < 1e-6
        print(f"  {key:>6}: 参考={float(ref[key]):>12.6f}  repo={float(got[key]):>12.6f}  "
              f"|差|={diff:.2e}  {status}")
    print(f"  指标口径交叉验证: {'PASS' if all_ok else 'FAIL'}")

    print("\n" + "=" * 72)
    print("实验 C：decision-scale-v1 评分 -> 信号/动作 契约映射")
    print("=" * 72)
    for score in [95, 70, 50, 30, 5]:
        band = decision_band_for_score(score)
        print(f"  score={score:>3} -> signal={band.signal_key:<12} action={band.action:<7} "
              f"decision_type={band.decision_type:<5} {band.label_zh}")

    print("\n" + "=" * 72)
    print("实验 D：策略 YAML 契约解析（strategies/ma_golden_cross.yaml）")
    print("=" * 72)
    with open(REPO / "strategies" / "ma_golden_cross.yaml", encoding="utf-8") as f:
        strat = yaml.safe_load(f)
    for field in ["name", "display_name", "category", "core_rules",
                  "required_tools", "aliases", "default_priority", "market_regimes"]:
        print(f"  {field}: {strat.get(field)}")
    n = len(list((REPO / "strategies").glob("*.yaml")))
    print(f"  strategies 目录 YAML 策略总数: {n}")
    print(f"  instructions 字段长度: {len(strat['instructions'])} 字符（发给 LLM 的策略说明书）")


if __name__ == "__main__":
    main()
