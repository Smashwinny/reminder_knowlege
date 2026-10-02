"""T1 验收测试：只测外部行为。运行: python tests/test_t1.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.tokenize import tokenize

assert tokenize("The cat, the dog!") == ["the", "cat", "the", "dog"], tokenize("The cat, the dog!")
assert tokenize("123 456") == []
print("T1 tests: PASS")
