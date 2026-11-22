#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""提取/重学加固参数的玩具记忆模型；不是人类被试复现或效应证据。

Karpicke & Roediger 2008 的真实人类结果单独报告，不能由本模型推出。
"""
import argparse
import random


def simulate(mode, n=300, seed=7, delay_days=7, restudy_gain=1.25,
             test_success_gain=1.45, test_failure_gain=1.1,
             daily_decay=0.98, delay_decay=0.72, rng=None):
    if mode not in {"restudy", "test"}:
        raise ValueError("未知练习模式")
    if n <= 0 or delay_days < 0:
        raise ValueError("n 必须为正，延迟天数不得为负")
    if not 0 <= delay_decay <= 1 or not 0 <= daily_decay <= 1:
        raise ValueError("衰减系数须在 [0,1]")
    if min(restudy_gain, test_success_gain, test_failure_gain) < 0:
        raise ValueError("加固系数不得为负")
    rng = rng or random.Random(seed)
    recalled = 0
    for _ in range(n):
        strength = 1.0
        for _day in range(3):
            if mode == "test":
                if rng.random() < min(1, strength):
                    strength *= test_success_gain
                else:
                    strength *= test_failure_gain
            else:
                strength *= restudy_gain
            strength *= daily_decay
        probability = min(1, strength * (delay_decay ** delay_days))
        if rng.random() < probability:
            recalled += 1
    return recalled / n


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=300)
    parser.add_argument("--delay-decay", type=float, default=0.72)
    parser.add_argument("--restudy-gain", type=float, default=1.25)
    parser.add_argument("--test-success-gain", type=float, default=1.45)
    parser.add_argument("--test-failure-gain", type=float, default=1.1)
    args = parser.parse_args()
    rng = random.Random(7)
    common = dict(n=args.n, delay_decay=args.delay_decay,
                  restudy_gain=args.restudy_gain,
                  test_success_gain=args.test_success_gain,
                  test_failure_gain=args.test_failure_gain)
    restudy = simulate("restudy", rng=rng, **common)
    testing = simulate("test", rng=rng, **common)
    print("真实论文（K&R 2008，40 个斯瓦希里语—英语词对，一周后）：")
    print("  重复测试 80% vs 无重复测试 36%（跨后续学习条件平均）")
    print("\n本地玩具模型（不是论文复现）：")
    print(f"  重学参数输出: {restudy:.1%}")
    print(f"  测试参数输出: {testing:.1%}")
    print(f"  参数差: {(testing-restudy)*100:+.1f} 个百分点")
    print("边界：测试/重学加固参数由我们预设；输出方向和数值都不是人类效应证据")


if __name__ == "__main__":
    main()
