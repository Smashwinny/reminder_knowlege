"""T2: 排行 —— 次数降序、同频按字母序。"""
from collections import Counter

def report(words: list, n: int = 5) -> list:
    counts = Counter(words)
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:n]
