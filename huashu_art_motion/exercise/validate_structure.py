# -*- coding: utf-8 -*-
"""huashu-art-motion 结构校验器 —— 学习实验。

校验 SKILL.md 宣称的仓库结构真实性：
  1. 风格配方 INDEX.md 的卡片表 = 35 张，逐张有对应场景文件 scripts/engine/scenes/<id>.js
  2. 解说视频语法 = 9 种（t1/t2/t3 + y1..y6），每种有对应 .md 配方文件
  3. 引擎工程存在完整骨架（engine.js/render.py/clip.html/clips/）
  4. SKILL.md 宣称的"确定性种子"在引擎源码里有真实实现
  5. clip.html 参数化片段可解析出合法 JSON spec（无浏览器，纯文本校验）

用法： python validate_structure.py
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent / "repo"


def check_index_cards():
    idx = (REPO / "references/风格配方/INDEX.md").read_text(encoding="utf-8")
    rows = re.findall(r"^\| (\d+_[a-z0-9_]+) \|", idx, re.M)
    scenes_dir = REPO / "scripts/engine/scenes"
    missing = [r for r in rows if not (scenes_dir / f"{r}.js").exists()]
    return rows, missing


def check_grammars():
    gdir = REPO / "references/动画语法"
    files = sorted(p.name for p in gdir.glob("*.md"))
    return files


def check_engine():
    eng = REPO / "scripts/engine"
    need = ["engine.js", "render.py", "clip.html", "clip.js", "eras.js",
            "compare.py", "demos", "clips", "lib"]
    return {n: (eng / n).exists() for n in need}


def check_seed_determinism():
    """种子确定性：lib/util.js 有 mulberry32 实现 + 全引擎 rng(seed)/U.rng(seed) 调用面。"""
    util = (REPO / "scripts/engine/lib/util.js").read_text(encoding="utf-8", errors="ignore")
    has_impl = "mulberry32" in util
    call_sites = 0
    for js in (REPO / "scripts/engine").rglob("*.js"):
        src = js.read_text(encoding="utf-8", errors="ignore")
        call_sites += len(re.findall(r"\brng\(\s*seed|U\.rng\(\s*seed", src))
    return has_impl, call_sites


def check_clip_specs():
    """examples/ 下的 JSON spec（每语法一个示范 spec）合法性。"""
    ex = REPO / "scripts/engine/examples"
    json_files = sorted(ex.glob("*.json"))
    ok = 0
    fails = {}
    for f in json_files:
        try:
            json.loads(f.read_text(encoding="utf-8"))
            ok += 1
        except Exception:
            fails[f.name] = "parse_fail"
    return len(json_files), ok, fails


def main():
    cases = []

    def check(name, ok, detail):
        cases.append((name, ok, detail))

    rows, missing = check_index_cards()
    check(f"T1 INDEX 卡片数={len(rows)}（宣称35）", len(rows) == 35, f"missing={missing}")
    check("T2 每个卡片有场景 js 文件", not missing, f"{len(rows)-len(missing)}/{len(rows)}")

    grams = check_grammars()
    check(f"T3 视频语法数={len(grams)}（宣称9）", len(grams) == 9, ",".join(grams))

    eng = check_engine()
    check("T4 引擎骨架完整", all(eng.values()), str(eng))

    has_impl, call_sites = check_seed_determinism()
    check(f"T5 种子确定性（mulberry32 实现={has_impl}，rng(seed) 调用面={call_sites} 处）",
          has_impl and call_sites >= 10, f"util.js 实现 + 全引擎 {call_sites} 处种子调用")

    total, okj, fails = check_clip_specs()
    check(f"T6 clips JSON spec 合法 {okj}/{total}", okj == total and total > 0, str(fails))

    passed = sum(1 for _, ok, _ in cases if ok)
    for name, ok, detail in cases:
        print(f"  {'✅' if ok else '❌'} {name}: {detail}")
    print(f"\n测试结果：{passed}/{len(cases)} 通过")
    print(f"\n引擎统计：scenes={len(list((REPO/'scripts/engine/scenes').glob('*.js')))} 个场景文件，"
          f"动画语法卡={len(grams)}，clips JSON={total}")
    return passed == len(cases)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
