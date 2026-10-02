# -*- coding: utf-8 -*-
"""
ascii_loop.py — 文字版 generate→score→steer 自改进循环（Ass Bench 模式的真实收敛版）

上游 Ass-Bench 的 generate/score 都是 stub（hash 伪随机，永不收敛）。
本实验把它补成真的：
  generate : 确定性 ASCII 渲染器，prompt 里的 steer 注释就是渲染参数
  score    : 真实可测的启发式（对称性/比例/密度/纹理四维 rubric）
  steer    : 取最低分维度，追加修正注释（幂等去重，防 prompt 无限膨胀）
结果：分数逐轮爬升、两次运行完全一致（可复现）。

用法:  python ascii_loop.py [--rounds 7] [--weights-json '{"proportion":0.7,...}']
零依赖：仅标准库。
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

TARGET_WIDTH = 15  # proportion 维度的目标底宽（奇数）

# ---------- steer 注释 → 渲染参数 ----------
NOTE_CENTER = "center every row"
NOTE_GROW = "grow width toward 15"
NOTE_FILL = "fill the gaps"
NOTE_TEXTURE = "alternate texture characters"


def parse_params(prompt: str) -> dict:
    """generate 阶段第一步：从 prompt 里读出渲染参数（没提到的用最差默认值）"""
    return {
        "center": NOTE_CENTER in prompt,
        "width": TARGET_WIDTH if NOTE_GROW in prompt else 5,
        "fill": NOTE_FILL in prompt,
        "texture": NOTE_TEXTURE in prompt,
    }


# ---------- generate：确定性 ASCII 渲染 ----------
def generate(prompt: str) -> str:
    p = parse_params(prompt)
    width = p["width"] if p["width"] % 2 == 1 else p["width"] + 1
    height = (width + 1) // 2
    lines = []
    for i in range(height):
        blocks = min(2 * i + 1, width)
        chars = []
        for k in range(blocks):
            solid = p["fill"] or (k % 3 == 0)   # 不 fill 时只放稀疏几块
            if not solid:
                chars.append(" ")
            elif p["texture"] and k % 2 == 1:
                chars.append("+")               # 纹理：奇数位刻痕换字符
            else:
                chars.append("#")
        row = "".join(chars)
        if p["center"]:
            pad = (width - blocks) // 2
            line = " " * pad + row
        else:  # 不居中：全部左对齐（歪塔）
            line = row
        lines.append(line.rstrip())
    return "\n".join(lines)


# ---------- score：真实启发式四维 rubric ----------
def score(art: str) -> dict:
    lines = [l for l in art.splitlines() if l.strip()]
    width = max(len(l) for l in lines)

    # 1) 对称性：每行左右留白是否相等
    sym_ok = sum(1 for l in lines
                 if (len(l) - len(l.lstrip())) == (width - len(l.rstrip())))
    symmetry = sym_ok / len(lines)

    # 2) 比例：底宽离目标 15 有多远
    proportion = max(0.0, 1.0 - abs(width - TARGET_WIDTH) / TARGET_WIDTH)

    # 3) 密度：第 i 行期望 2i+1 块，实际非空格字符占比
    dens = []
    for i, l in enumerate(lines):
        expected = min(2 * i + 1, width)
        got = len(l.replace(" ", ""))
        dens.append(min(1.0, got / expected))
    density = sum(dens) / len(dens)

    # 4) 纹理：画面里是否出现 >=2 种刻痕字符（# 和 +）
    texture = 1.0 if ("#" in art and "+" in art) else 0.0

    return {"proportion": round(proportion, 4),
            "symmetry": round(symmetry, 4),
            "density": round(density, 4),
            "texture": round(texture, 4)}


# ---------- steer：最弱维度 → 修正注释（幂等去重） ----------
STEER_NOTES = {
    "proportion": NOTE_GROW,
    "symmetry": NOTE_CENTER,
    "density": NOTE_FILL,
    "texture": NOTE_TEXTURE,
}


def next_prompt(prompt: str, dims: dict, weights: dict,
                max_steers: int = 2) -> str:
    ranked = sorted(dims.items(),
                    key=lambda kv: kv[1]["value"] if isinstance(kv[1], dict) else kv[1])
    weakest = [(k, v) for k, v in ranked[:max_steers]]
    added = []
    for name, val in weakest:
        v = val["value"] if isinstance(val, dict) else val
        if v >= 0.95:            # 已达标，不再追加
            continue
        note = STEER_NOTES[name]
        if note in prompt:       # 幂等：注释已在 prompt 里就不重复
            continue
        added.append(note)
    if not added:
        return prompt
    return prompt.rstrip() + "\n" + "\n".join(added)


# ---------- loop ----------
def run(rounds: int, weights: dict, runs_dir: Path) -> None:
    prompt = "a tower of blocks"          # seed：什么参数都没提 → 最差渲染
    best_score, best_art, best_prompt = -1.0, "", prompt
    run_dir = runs_dir / time.strftime("%Y%m%d-%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)

    print(f"{'round':>5} {'proportion':>11} {'symmetry':>9} {'density':>8} "
          f"{'texture':>8} {'overall':>8}")
    for n in range(1, rounds + 1):
        art = generate(prompt)
        dims = {k: {"value": v} for k, v in score(art).items()}
        overall = round(sum(dims[k]["value"] * w for k, w in weights.items()), 4)
        print(f"{n:>5} {dims['proportion']['value']:>11.4f} "
              f"{dims['symmetry']['value']:>9.4f} {dims['density']['value']:>8.4f} "
              f"{dims['texture']['value']:>8.4f} {overall:>8.4f}")
        (run_dir / f"round_{n:03d}.json").write_text(json.dumps(
            {"round": n, "prompt": prompt, "art": art,
             "dimensions": dims, "overall_score": overall},
            ensure_ascii=False, indent=2), encoding="utf-8")
        if overall > best_score:
            best_score, best_art, best_prompt = overall, art, prompt
        prompt = next_prompt(prompt, dims, weights)
        if all(v["value"] >= 0.95 for v in dims.values()):
            print("  -> all dimensions >= 0.95, converged; stop early")
            break

    print(f"\nBest overall: {best_score:.4f}")
    print(f"Best prompt ({len(best_prompt)} chars):\n{best_prompt}")
    print("\n=== final art (best round) ===")
    print(best_art)
    print(f"\nLogs: {run_dir}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=7)
    ap.add_argument("--weights-json", type=str, default=None,
                    help='覆盖 rubric 权重，如 \'{"proportion":0.7,"symmetry":0.1,"density":0.1,"texture":0.1}\'')
    ap.add_argument("--runs-dir", type=str, default="runs")
    args = ap.parse_args()
    weights = json.loads(args.weights_json) if args.weights_json else {
        "proportion": 0.30, "symmetry": 0.25, "density": 0.25, "texture": 0.20}
    run(args.rounds, weights, Path(args.runs_dir))
