import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.report import report

assert report(["b", "a", "b"], n=2) == [("b", 2), ("a", 1)]
assert report(["b", "a"], n=5) == [("a", 1), ("b", 1)]  # 同频按字母序
print("T2 tests: PASS")
