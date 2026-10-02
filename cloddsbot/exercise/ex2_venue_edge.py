# -*- coding: utf-8 -*-
"""
ex2: 跨交易所价差 -> 净边际计算（复刻 CloddsBot V2 venue-arbitrage "双腿执行计划"）
数据源: OKX + Kraken 公共行情（只读），Binance 实测被地域限制（ Restricted Location ）
对应 repo docs/V2_HFT_ARBITRAGE.md:
  1. 选买入所/卖出席位  2. 扣手续费/延迟/陈旧报价惩罚  3. 净边际不过门槛就拒绝  4. 输出双腿计划
"""
import json
import urllib.request

FEE = {"okx_taker": 0.001, "kraken_taker": 0.0026}  # 两家公开 taker 费率
MIN_NET_EDGE = 0.0005  # 0.05%: 净边际门槛, 不过就拒绝执行


def http_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "learning-ex/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


def okx_btc():
    d = http_get("https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT")["data"][0]
    return float(d["askPx"]), float(d["bidPx"])


def kraken_btc():
    r = http_get("https://api.kraken.com/0/public/Ticker?pair=XBTUSDT")["result"]["XBTUSDT"]
    return float(r["a"][0]), float(r["b"][0])  # ask, bid


def main():
    print("=" * 72)
    print("ex2 跨所 BTC/USDT 价差 -> 净边际 -> 双腿执行计划 (OKX x Kraken, 只读)")
    print("=" * 72)
    okx_ask, okx_bid = okx_btc()
    kr_ask, kr_bid = kraken_btc()
    print(f"OKX    ask={okx_ask:,.1f}  bid={okx_bid:,.1f}")
    print(f"Kraken ask={kr_ask:,.1f}  bid={kr_bid:,.1f}")

    # 场景A: Kraken 便宜 -> Kraken 买入, OKX 卖出 (taker 双腿)
    edge_a_raw = (okx_bid - kr_ask) / kr_ask
    edge_a_net = edge_a_raw - FEE["okx_taker"] - FEE["kraken_taker"]
    # 场景B: OKX 便宜 -> OKX 买入, Kraken 卖出
    edge_b_raw = (kr_bid - okx_ask) / okx_ask
    edge_b_net = edge_b_raw - FEE["okx_taker"] - FEE["kraken_taker"]

    print()
    print(f"{'方向':<28} {'毛边际':>9} {'双taker费':>10} {'净边际':>9}  决策")
    print("-" * 72)
    for name, raw, net in [("A: Kraken买 -> OKX卖", edge_a_raw, edge_a_net),
                           ("B: OKX买 -> Kraken卖", edge_b_raw, edge_b_net)]:
        decision = ("执行 (净边际过门槛)" if net >= MIN_NET_EDGE
                    else f"拒绝 (< 门槛 {MIN_NET_EDGE:.2%})")
        print(f"{name:<28} {raw:>9.4%} {FEE['okx_taker']+FEE['kraken_taker']:>10.4%}"
              f" {net:>9.4%}  {decision}")

    best = max(edge_a_net, edge_b_net)
    print()
    print(f"毛价差只有 {(kr_ask-okx_ask)/okx_ask:.4%} 量级, 扣掉两次 taker 手续费后"
          f" {'有' if best>=MIN_NET_EDGE else '没有'}可执行空间")
    print("=> 印证 repo 净边际过滤存在的意义: 大多数'看起来有价差'的机会过不了手续费这道门")
    print()
    print("免责声明: 仅学习用途的只读行情实验, 不构成投资建议, 未做任何真实交易。")


if __name__ == "__main__":
    main()
