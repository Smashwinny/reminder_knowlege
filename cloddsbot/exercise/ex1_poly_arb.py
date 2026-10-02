# -*- coding: utf-8 -*-
"""
ex1: 复刻 CloddsBot 套利检测流水线（技术层，零投资）
数据源: Polymarket 公共 API（gamma-api 拿市场, clob 拿订单簿），只读，无需任何 key
逻辑对应 repo src/arbitrage/index.ts 的 Cross-Platform Arbitrage Service:
  市场扫描 -> 价格比较(YES+NO) -> 边际计算 -> 机会打分 -> 风控过滤
负风险套利(negative risk): 买 YES ask + 买 NO ask < 1.00 -> 无论结果如何拿回 $1
"""
import json
import time
import urllib.request

GAMMA = "https://gamma-api.polymarket.com/markets"
CLOB_BOOK = "https://clob.polymarket.com/book"

FEES = {"taker_fee_rate": 0.0, "slippage_buffer": 0.005}  # Polymarket 目前 taker 费 0，留 0.5% 滑点缓冲
MIN_LIQUIDITY = 5000.0   # 风控过滤1: 最低市场流动性 $
MIN_EDGE = 0.005         # 风控过滤2: 扣滑点后最小净边际
MAX_EDGE = 0.15          # 风控过滤3: "好得不像真"过滤——边际异常高多半是解析错误


def http_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "learning-ex/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


def best_ask(book):
    """订单簿里最低卖价（我们买入的成本）"""
    asks = book.get("asks") or []
    prices = [(float(a["price"]), float(a["size"])) for a in asks]
    if not prices:
        return None, 0.0
    price, size = min(prices, key=lambda x: x[0])
    return price, size


def main():
    print("=" * 72)
    print("ex1 Polymarket 负风险套利扫描（复刻 CloddsBot arbitrage 流水线, 只读）")
    print("=" * 72)

    # 1. 市场扫描: 按24h成交量拿最活跃的未收盘二元市场
    markets = http_get(GAMMA + "?closed=false&archived=false&active=true"
                       "&order=volume24hr&ascending=false&limit=40")
    # 坑实测: gamma API 的 clobTokenIds 是 JSON 字符串不是数组, 需再 parse 一次
    def tokens(m):
        v = m.get("clobTokenIds")
        if isinstance(v, str):
            try:
                v = json.loads(v)
            except Exception:
                v = None
        return v

    binary = [m for m in markets
              if tokens(m) and len(tokens(m)) == 2]
    print(f"[1] 市场扫描: 拉到 {len(markets)} 个活跃市场, 其中二元市场 {len(binary)} 个")

    opps = []
    for m in binary[:25]:
        yes_id, no_id = tokens(m)[0], tokens(m)[1]
        try:
            byes = http_get(CLOB_BOOK + "?token_id=" + yes_id)
            bno = http_get(CLOB_BOOK + "?token_id=" + no_id)
        except Exception as e:
            print(f"    skip {m['question'][:40]}: {e}")
            continue
        yes_ask, yes_sz = best_ask(byes)
        no_ask, no_sz = best_ask(bno)
        if yes_ask is None or no_ask is None:
            continue
        cost = yes_ask + no_ask
        edge = 1.0 - cost
        liq = float(m.get("liquidity") or 0)
        opps.append({
            "question": m["question"], "cost": cost, "edge": edge,
            "liq": liq, "yes_ask": yes_ask, "no_ask": no_ask,
            "fill_sz": min(yes_sz, no_sz),
        })
        time.sleep(0.15)

    print(f"[2] 价格比较: 成功拿到 {len(opps)} 个市场的 YES/NO 双边最优卖价")

    # 3. 风控过滤（对应 RiskEngine 思路：门槛 + 流动性 + sanity check）
    passed = [o for o in opps
              if o["liq"] >= MIN_LIQUIDITY
              and o["edge"] - FEES["slippage_buffer"] >= MIN_EDGE
              and o["edge"] <= MAX_EDGE]
    opps.sort(key=lambda o: -o["edge"])
    passed.sort(key=lambda o: -(o["edge"] - FEES["slippage_buffer"]))

    print(f"[3] 风控过滤: 流动性>={MIN_LIQUIDITY}$ 且 净边际>={MIN_EDGE} 且 边际<={MAX_EDGE}"
          f" -> 通过 {len(passed)}/{len(opps)}")
    print()
    print(f"{'市场':<38} {'YES卖价':>7} {'NO卖价':>7} {'合计':>7} {'毛边际':>8} {'流动性$':>10}")
    print("-" * 84)
    for o in opps[:12]:
        flag = " <== 通过风控" if o in passed[:6] else ""
        print(f"{o['question'][:36]:<38} {o['yes_ask']:>7.3f} {o['no_ask']:>7.3f}"
              f" {o['cost']:>7.3f} {o['edge']:>8.3f} {o['liq']:>10,.0f}{flag}")

    print()
    if passed:
        best = passed[0]
        net = best["edge"] - FEES["slippage_buffer"]
        print(f"[4] 最优通过机会: {best['question'][:60]}")
        print(f"    买 YES@{best['yes_ask']} + 买 NO@{best['no_ask']} = {best['cost']:.3f}"
              f" -> 毛边际 {best['edge']*100:.2f}%, 扣滑点净边际 {net*100:.2f}%")
        print(f"    $100 无风险回 $100 (无论结果), 理论毛利 ${100*best['edge']:.2f}")
    else:
        print("[4] 当前前25大热门市场没有通过风控的负风险机会 —— 市场有效，这正是常态")

    print()
    print("免责声明: 本实验仅复刻检测逻辑用于学习, 不构成投资建议, 未做任何真实交易。")


if __name__ == "__main__":
    main()
