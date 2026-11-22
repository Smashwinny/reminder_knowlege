#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""提示词缓存经济学：明确费率和全命中假设的本地估算，不发 API 请求。

默认 0.1x 命中读价只是演示口径，不代表所有型号。可用参数切换为官方文档
列出的 0.05x 等费率。分词函数只用于估算，不能替代真实 tokenizer/账单。
"""
import argparse
import re
from pathlib import Path


def rough_tokens(text):
    """英文按词、其他非空白字符按字，再乘 1.3；仅作粗估。"""
    return max(1, int(len(re.findall(r"[a-zA-Z0-9_]+|\S", text)) * 1.3))


def total_cost(calls, prefix_tokens, new_tokens, read_price,
               cached_read_multiplier, write_multiplier, use_cache):
    """假设首次写入、之后每次全部命中；真实命中不足时须另算。"""
    total = 0.0
    for index in range(calls):
        call_input = prefix_tokens + new_tokens
        if not use_cache:
            total += call_input * read_price / 1e6
        elif index == 0:
            total += call_input * read_price * write_multiplier / 1e6
        else:
            total += (prefix_tokens * read_price * cached_read_multiplier
                      + new_tokens * read_price) / 1e6
    return total


def break_even(prefix_tokens, new_tokens, read_price,
               cached_read_multiplier, write_multiplier):
    for calls in range(1, 1000):
        cached = total_cost(calls, prefix_tokens, new_tokens, read_price,
                            cached_read_multiplier, write_multiplier, True)
        uncached = total_cost(calls, prefix_tokens, new_tokens, read_price,
                              cached_read_multiplier, write_multiplier, False)
        if cached <= uncached:
            return calls
    return None


def main():
    default_sample = Path(__file__).resolve().parents[2] / "vault" / "00-总览.md"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample", type=Path, default=default_sample)
    parser.add_argument("--calls", type=int, default=10)
    parser.add_argument("--new-tokens", type=int, default=200)
    parser.add_argument("--read-price", type=float, default=5.0,
                        help="普通输入美元/百万 token；默认仅演示")
    parser.add_argument("--cached-read-multiplier", type=float, default=0.1)
    parser.add_argument("--write-multiplier", type=float, default=1.25)
    args = parser.parse_args()
    if args.calls < 1 or args.new_tokens < 0 or args.read_price <= 0:
        parser.error("calls 须大于 0，new-tokens 不得为负，read-price 须大于 0")
    if not 0 < args.cached_read_multiplier <= 1 or args.write_multiplier <= 0:
        parser.error("缓存读价倍率须在 (0,1]，写入倍率须大于 0")

    prefix_tokens = rough_tokens(args.sample.read_text(encoding="utf-8"))
    common = (prefix_tokens, args.new_tokens, args.read_price,
              args.cached_read_multiplier, args.write_multiplier)
    uncached = total_cost(args.calls, *common, False)
    cached = total_cost(args.calls, *common, True)
    first_write = ((prefix_tokens + args.new_tokens) * args.read_price
                   * args.write_multiplier / 1e6)
    balance = break_even(*common)

    print(f"样本: {args.sample}")
    print(f"前缀粗估: {prefix_tokens:,} token（非真实 tokenizer）")
    print(f"口径: 普通读价 ${args.read_price:g}/M；命中读 {args.cached_read_multiplier:g}x；"
          f"30m 写入 {args.write_multiplier:g}x；后续调用假设全部命中")
    print(f"不缓存 {args.calls} 次: ${uncached:.4f}")
    print(f"缓存   {args.calls} 次: ${cached:.4f}（首次写入 ${first_write:.4f}）")
    print(f"节省: {(1-cached/uncached)*100:.1f}%  盈亏平衡: {balance} 次")
    print("边界: 变化点之后的前缀不能复用；TTL、路由、命中率与型号价格须看官方文档和真实回执")


if __name__ == "__main__":
    main()
