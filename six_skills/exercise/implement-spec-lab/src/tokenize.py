"""T1: 分词 —— 仅保留字母并小写化。"""
import re

def tokenize(text: str) -> list:
    return re.findall(r"[a-z]+", text.lower())
