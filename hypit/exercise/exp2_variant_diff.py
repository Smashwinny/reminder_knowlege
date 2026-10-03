# -*- coding: utf-8 -*-
"""实验2：变体对账 —— “换主持人/换特效/换话题，只改对应组件”到底改了多少？
对 reference.svml 与三个官方变体做行级 diff，并按“区块”归类改动落在哪：
  主持人相关(presenter/voice) / 话题台词(script) / 特效B-roll(broll/prompts) / 排行榜组件(ranking)。
零依赖。用法: python exp2_variant_diff.py <目录>
"""
import re
import sys
import difflib
from pathlib import Path

def classify(line):
    l = line.lower()
    if "presenter" in l or "voice" in l or "host" in l or "speaker" in l:
        return "主持人相关(presenter/voice)"
    if "broll" in l or "action" in l:
        return "特效/B-roll/动作(broll/action)"
    if "script" in l or re.search(r"<ronaldo>|<messi>|<host>", l):
        return "话题台词(script)"
    if "ranking" in l or "tier" in l or "board" in l:
        return "排行榜组件(ranking/board)"
    if "prompt" in l or "text:value" in l:
        return "图像提示(prompt)"
    if "import" in l:
        return "能力包导入(import)"
    return "其他(结构/资产引用)"

def main(d):
    d = Path(d)
    ref = (d / "reference.svml").read_text(encoding="utf-8").splitlines()
    print(f"基准: reference.svml ({len(ref)} 行)\n")
    for name in ["swap-host", "swap-topic", "swap-effect"]:
        other = (d / f"{name}.svml").read_text(encoding="utf-8").splitlines()
        sm = difflib.SequenceMatcher(None, ref, other)
        added = removed = 0
        buckets = {}
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            lines = (ref[i1:i2] if tag in ("delete", "replace") else []) + \
                    (other[j1:j2] if tag in ("insert", "replace") else [])
            added += j2 - j1
            removed += i2 - i1
            for ln in lines:
                buckets[classify(ln)] = buckets.get(classify(ln), 0) + 1
        same = sm.ratio() * 100
        print(f"=== {name}.svml vs reference ===")
        print(f"  相似度 {same:.1f}%  |  +{added} 行 / -{removed} 行")
        for k, v in sorted(buckets.items(), key=lambda x: -x[1]):
            bar = "#" * max(1, v // 3)
            print(f"    {k:<26} {v:>4} 行  {bar}")
        print()

if __name__ == "__main__":
    main(sys.argv[1])
