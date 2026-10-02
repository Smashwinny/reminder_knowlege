"""T3: 命令行入口。用法: python topwords.py file.txt -n 5"""
import argparse, sys
from src.tokenize import tokenize
from src.report import report

def main(argv=None):
    p = argparse.ArgumentParser(description="文本词频 Top-N")
    p.add_argument("file")
    p.add_argument("-n", type=int, default=5)
    a = p.parse_args(argv)
    text = open(a.file, encoding="utf-8").read()
    for word, count in report(tokenize(text), a.n):
        print(f"{count:5d}  {word}")

if __name__ == "__main__":
    main()
