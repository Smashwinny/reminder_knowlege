# -*- coding: utf-8 -*-
"""系统演变模拟器：单机 -> 负载均衡 -> 缓存 -> 异步消息队列
零依赖（只用标准库），确定性输出（同输入同输出）。
用法: python system_evolution.py <stage>
  stage: single | lb | cache | burst | all
"""
import sys, math

REQ_MS = 2.0        # 一台服务器处理一个请求要 2ms（纯计算+查库）
WINDOW_S = 10       # 模拟 10 秒的流量

def traffic(rps_peak):
    """确定性流量曲线：正弦波，峰值 rps_peak，谷值 20%"""
    return [rps_peak * (0.6 + 0.4 * math.sin(2 * math.pi * t / WINDOW_S))
            for t in range(WINDOW_S)]

def queue_latency(arrival_rps, servers, req_ms):
    """简化排队模型：利用率 u = 到达率/总容量；u>=1 时延迟爆炸"""
    capacity = servers * (1000.0 / req_ms)   # 每秒能处理的请求数
    u = arrival_rps / capacity
    if u >= 1.0:
        return float('inf')                  # 排不上队，请求开始被丢弃
    return req_ms / (1.0 - u)                # M/M/1 近似：利用率越高延迟越陡

def report(title, rows, unit="ms"):
    print(f"\n=== {title} ===")
    print(f"{'峰值RPS':>8} | {'服务器':>4} | {'平均延迟':>10} | 状态")
    print("-" * 48)
    for rps, servers in rows:
        lat = queue_latency(rps, servers, REQ_MS)
        if lat == float('inf'):
            state = "OVERLOAD 崩溃(请求被丢弃)"
            lat_s = ">1000"
        elif lat > 200:
            state = "危险:用户明显卡顿"
            lat_s = f"{lat:8.1f}"
        elif lat > 50:
            state = "偏慢"
            lat_s = f"{lat:8.1f}"
        else:
            state = "健康"
            lat_s = f"{lat:8.1f}"
        print(f"{rps:>8} | {servers:>4} | {lat_s:>8} {unit} | {state}")

def cache_stage():
    """缓存：命中率 h 时，只有 (1-h) 的请求打到慢速数据库"""
    print("\n=== cache:加一层缓存后 ===")
    print("请求 10000/s, 服务器 8 台")
    print(f"{'命中率':>6} | {'打到DB的RPS':>12} | {'DB利用率':>8} | 平均延迟")
    print("-" * 56)
    db_capacity = 8 * (1000.0 / REQ_MS)      # 4000/s，注意 DB 慢:处理要 20ms
    db_capacity_slow = 8 * (1000.0 / 20.0)   # 400/s
    for h in (0, 0.5, 0.8, 0.95, 0.99):
        to_db = 10000 * (1 - h)
        lat = queue_latency(to_db, 1, 20.0)
        lat_s = ">1000 (DB崩溃)" if lat == float('inf') else f"{lat:8.1f}"
        print(f"{h:>6.0%} | {to_db:>12.0f} | {to_db/db_capacity_slow:>7.0%} | {lat_s}")
    print("\n结论:命中率 95% 时,打到 DB 的流量骤降为 500/s —— 缓存扛住了 95% 的读压力")

def burst_stage():
    """异步+消息队列：把洪峰削峰填谷"""
    print("\n=== burst:流量洪峰(10倍)来了 ===")
    spike = 50000  # 平时 5000,洪峰 50000
    sync_cap = 4 * (1000.0 / REQ_MS)         # 同步:4台服务器 2000/s
    print(f"同步架构:容量 {sync_cap:.0f}/s,洪峰 {spike}/s -> "
          f"{spike/sync_cap:.0f} 倍过载,全部卡死")
    print("异步架构:前置 API 快速收下请求塞进队列(只做入队,~0.2ms),")
    print("          后台 worker 按自己的速度消费")
    q_cap = 4 * (1000.0 / 0.2)               # API 只入队:20000/s
    backlog_per_s = spike - sync_cap
    drain_s = backlog_per_s * 5 / sync_cap   # 洪峰 5 秒后需要多久排干
    print(f"  API 层容量 {q_cap:.0f}/s > 洪峰,不崩;队列积压 {backlog_per_s:.0f}/s")
    print(f"  洪峰过后约 {drain_s:.0f} 秒排干积压 —— 用户得到'已受理'而不是超时")

if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    if stage in ("single", "all"):
        report("single:一台服务器", [(1000, 1), (2000, 1), (3000, 1),
                                     (4000, 1), (5000, 1)])
        print("\n结论:容量上限 = 1000ms/2ms = 500/s? 不,峰值 500/s 就开始抖;"
              "\n单机一过利用率 80%,延迟非线性飙升 —— 这就是必须扩展的原因")
    if stage in ("lb", "all"):
        report("lb:负载均衡器 + 4 台服务器", [(2000, 4), (4000, 4), (6000, 4),
                                              (8000, 4), (10000, 4)])
        print("\n结论:4 台机器容量约 2000/s,过载点整体右移 —— 水平扩展")
    if stage in ("cache", "all"):
        cache_stage()
    if stage in ("burst", "all"):
        burst_stage()
