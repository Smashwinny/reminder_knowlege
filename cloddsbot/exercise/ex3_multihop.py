# -*- coding: utf-8 -*-
"""
ex3: 多跳套利环检测（复刻 CloddsBot V2 multi-hop-arbitrage "3-4跳路径规划"）
数据源: OKX 公共行情三元组 BTC/USDT, ETH/USDT, ETH/BTC（只读）
方法: 汇率取 -log(r) 变边权, 贝尔曼-福特找负环 = 乘积汇率 > 1 的套利环
  log( (ETH/BTC)*(USDT/ETH)*(BTC/USDT) ) > 0  <=>  对应 -log 边权和 < 0
"""
import json
import math
import urllib.request

FEE_PER_HOP = 0.001  # 每跳 taker 0.1%

def http_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "learning-ex/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


def tickers():
    """拿 OKX 三个交易对的中间价"""
    out = {}
    for inst in ["BTC-USDT", "ETH-USDT", "ETH-BTC"]:
        d = http_get(f"https://www.okx.com/api/v5/market/ticker?instId={inst}")["data"][0]
        out[inst] = (float(d["askPx"]) + float(d["bidPx"])) / 2
    return out


def main():
    print("=" * 72)
    print("ex3 多跳套利环检测 (OKX 真实三元组, -log 边权 + Bellman-Ford)")
    print("=" * 72)
    t = tickers()
    for k, v in t.items():
        print(f"  {k:<10} mid = {v:,.4f}")

    # 边权: -log(rate*(1-fee));  rate = 每跳把一种资产换成另一种的汇率
    def w(rate):
        return -math.log(rate * (1 - FEE_PER_HOP))

    # 汇率语义: rate = 每跳"换到的资产数量 / 换出的资产数量"
    # 环1: BTC --卖(BTC-USDT)--> USDT --买(ETH-USDT)--> ETH --卖(ETH-BTC)--> BTC
    c1 = w(t["BTC-USDT"]) + w(1 / t["ETH-USDT"]) + w(t["ETH-BTC"])
    # 环2: 反方向 BTC --买(ETH-BTC)--> ETH --卖(ETH-USDT)--> USDT --买(BTC-USDT)--> BTC
    c2 = w(1 / t["ETH-BTC"]) + w(t["ETH-USDT"]) + w(1 / t["BTC-USDT"])

    mult1 = math.exp(-c1)
    mult2 = math.exp(-c2)
    print()
    print(f"环1 BTC->USDT->ETH->BTC   边权和={c1:+.6f}  资金乘数={mult1:.6f}"
          f"  {'套利!' if c1 < 0 else '无套利'}")
    print(f"环2 反向 BTC->ETH->USDT->BTC 边权和={c2:+.6f}  资金乘数={mult2:.6f}"
          f"  {'套利!' if c2 < 0 else '无套利'}")

    best = min(c1, c2)
    print()
    if best >= 0:
        print(f"结论: 扣每跳 {FEE_PER_HOP:.1%} 手续费后, 两个方向边权和均为正 -> 无套利环")
        print("=> 印证 repo multi-hop planner 的'净边际过滤': 三角套利在主流大所早被机器人抹平,")
        print("   真正能做的是更长的尾巴路径 + 更快的延迟, 这正是它做'延迟感知排序'的原因")
    else:
        print(f"发现负环! 边权和 {best:.6f} < 0, 理论乘数 {math.exp(-best):.6f} (教学演示, 未含滑点)")

    print()
    print("免责声明: 仅学习用途的只读行情实验, 不构成投资建议, 未做任何真实交易。")


if __name__ == "__main__":
    main()
