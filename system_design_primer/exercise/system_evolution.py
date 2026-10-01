# -*- coding: utf-8 -*-
"""系统演变模拟器：单机 -> 负载均衡 -> 缓存 -> 异步消息队列
零依赖（只用标准库），确定性输出（同输入同输出）。
用法: python system_evolution.py <stage>
  stage: single | lb | cache | burst | all
"""
import sys

REQ_MS = 2.0          # 一台应用服务器处理一个请求要 2ms -> 单机容量 500/s
DB_QUERY_MS = 1.0     # 数据库单机处理一个查询要 1ms -> DB 容量 1000/s

def latency(arrival_rps, capacity, service_ms):
    """简化排队模型（M/M/1 近似）：利用率 u = 到达率/容量"""
    u = arrival_rps / capacity
    if u >= 1.0:
        return None                      # 过载：请求堆积/被丢弃
    return service_ms / (1.0 - u)

def report(title, rows, capacity):
    print(f"\n=== {title} ===")
    print(f"{'到达RPS':>8} | {'容量':>6} | {'利用率':>6} | {'平均延迟':>9} | 状态")
    print("-" * 60)
    for rps in rows:
        lat = latency(rps, capacity, 2.0)
        u = rps / capacity
        if lat is None:
            lat_s, state = ">1000", "OVERLOAD 崩溃(请求被丢弃)"
        elif lat > 10:
            lat_s, state = f"{lat:8.1f}", "危险:利用率>80%,延迟非线性飙升"
        elif lat > 4:
            lat_s, state = f"{lat:8.1f}", "偏慢"
        else:
            lat_s, state = f"{lat:8.1f}", "健康"
        print(f"{rps:>8} | {capacity:>6.0f} | {u:>6.0%} | {lat_s:>7} ms | {state}")

if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"

    if stage in ("single", "all"):
        cap = 1000 / REQ_MS                      # 500/s
        report("single: 一台服务器(容量500/s)", [100, 250, 400, 450, 600], cap)
        print("\n结论: 利用率到 80% 延迟就翻 5 倍,超过 100% 直接崩溃")
        print("      -> 单机不是线性变慢,是断崖式崩塌,必须扩展")

    if stage in ("lb", "all"):
        cap = 4 * 1000 / REQ_MS                  # 2000/s
        report("lb: 负载均衡器 + 4 台服务器(容量2000/s)", [500, 1000, 1600, 1800, 2500], cap)
        print("\n结论: 同样的机器复制 4 份,过载点整体右移 4 倍")
        print("      -> 这就是'水平扩展':负载均衡器把流量摊到每台上")

    if stage in ("cache", "all"):
        req, db_cap = 10000, 1000                # DB 单机 1000/s
        print("\n=== cache: 10000/s 读请求, DB 单机容量 1000/s ===")
        print(f"{'命中率':>6} | {'打到DB的RPS':>12} | {'DB利用率':>8} | 状态")
        print("-" * 52)
        for h in (0, 0.8, 0.9, 0.95, 0.99):
            to_db = req * (1 - h)
            u = to_db / db_cap
            state = ("OVERLOAD DB崩溃" if u >= 1 else
                     "危险" if u > 0.8 else "健康")
            print(f"{h:>6.0%} | {to_db:>12.0f} | {u:>7.0%} | {state}")
        print("\n结论: 命中率 95% 时,打到 DB 的流量骤降 20 倍(10000->500)")
        print("      -> 缓存不是锦上添花,是让 DB 活下来的生命线")

    if stage in ("burst", "all"):
        base, spike = 1000, 10000                # 平时 1000/s, 洪峰 10 倍
        sync_cap = 4 * 1000 / REQ_MS             # 2000/s
        api_cap = 4 * 1000 / 0.2                 # API 只入队(0.2ms): 20000/s
        backlog = (spike - sync_cap) * 5         # 洪峰持续 5 秒
        drain = backlog / sync_cap
        print("\n=== burst: 流量洪峰(10倍)持续 5 秒 ===")
        print(f"同步架构: 4台容量 {sync_cap:.0f}/s, 洪峰 {spike}/s")
        print(f"  -> {spike/sync_cap:.0f} 倍过载, 全部请求超时, 用户看到报错")
        print(f"异步+消息队列: API 只负责收请求入队(单台 {1000/0.2:.0f}/s, 4台 {api_cap:.0f}/s)")
        print(f"  -> API 层容量 {api_cap:.0f}/s > 洪峰, 不崩; 后台 worker 按自己的")
        print(f"     速度 {sync_cap:.0f}/s 消费, 洪峰过后约 {drain:.0f} 秒排干积压")
        print("  -> 用户立刻得到'已受理', 而不是超时 —— 这就是异步削峰")
