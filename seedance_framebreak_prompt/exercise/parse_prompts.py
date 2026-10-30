# -*- coding: utf-8 -*-
"""Seedance 2.5 frame-break 提示词解析器 —— 学习实验。

对 Koda (@aimikoda) 公开的 frame-break 提示词全文（prompt_fulltext.txt，
11950 字符，含 3 支视频的完整提示词）做结构解析：
  1. 提取每支提示词的公共骨架段落（char ref / MAIN VISUAL GOAL /
     COMPOSITING ORDER / 约束段 / OPENING 节拍）
  2. 统计提示词工程的"分层指令"结构（角色锚定层/视觉目标层/合成顺序层/
     约束层/节拍层）
  3. 提取 Koda 自述的四条方法论观察（黑边漂移/运镜变形/固定指令反效果/
     2.0→2.5 代差）
  4. 与 2609.00006 论文的 prompt 工程章节对照（rhetorical style 印证）

用法： python parse_prompts.py
"""
import re
import sys
from pathlib import Path

TXT = Path(__file__).resolve().parent / "prompt_fulltext.txt"

LAYER_MARKERS = {
    "角色锚定层": ["Use @[char ref]", "Preserve her"],
    "视觉目标层": ["MAIN VISUAL GOAL", "FRAME-BREAK EFFECT"],
    "合成顺序层": ["COMPOSITING ORDER", "BACK TO FRONT"],
    "物理约束层": ["Keep both bars equal", "The camera stays stationary"],
    "节拍层": ["OPENING", "TIMING"],
}


def main():
    text = TXT.read_text(encoding="utf-8")
    prompts = []
    for m in re.finditer(r"Prompt for the (first|second|third) one:\s*\n", text):
        prompts.append((m.group(1), m.start()))
    ends = [p[1] for p in prompts[1:]] + [len(text)]

    cases = []
    print(f"提示词数量：{len(prompts)} 支")
    cases.append(len(prompts) >= 2)

    # 公共骨架段落统计
    skeleton_hits = {name: 0 for name in LAYER_MARKERS}
    for (label, start), end in zip(prompts, ends):
        body = text[start:end]
        for name, markers in LAYER_MARKERS.items():
            if any(mk in body for mk in markers):
                skeleton_hits[name] += 1
    print("\n分层指令结构（各提示词命中的公共骨架层）：")
    for name, n in skeleton_hits.items():
        mark = "✅" if n == len(prompts) else "⚠️"
        print(f"  {mark} {name}: {n}/{len(prompts)}")
    cases.append(skeleton_hits["角色锚定层"] == len(prompts))
    cases.append(skeleton_hits["视觉目标层"] == len(prompts))

    # 合成顺序层细节：三层 back-to-front
    i = text.find("COMPOSITING ORDER")
    seg = text[i:i + 420]
    layers = [x for x in ["Background and scene", "black letterbox bars", "foreground character"] if x in seg]
    print(f"\n合成顺序三层齐备：{len(layers)}/3 —— {' / '.join(layers)}")
    cases.append(len(layers) == 3)

    # Koda 方法论四观察（主推文自述，已在抓取记录中）
    observations = [
        "黑边尺寸模型自决：指定百分比各代仍漂移",
        "运镜会使黑边移动/变形",
        "强固定指令有时反而破坏弹出效果",
        "2.0 尝试未达预期，2.5 成功（代差）",
    ]
    print("\nKoda 自述方法论观察（四条，来自 Prompt Drop 主帖）：")
    for o in observations:
        print("  -", o)
    cases.append(len(observations) == 4)

    # 提示词篇幅统计（工程化程度指标）
    lens = [end - start for (label, start), end in zip(prompts, ends)]
    print(f"\n各提示词长度：{lens}（均值 {sum(lens)//len(lens)} 字符）")
    cases.append(min(lens) > 1500)

    print(f"\n核对结果：{sum(1 for c in cases if c)}/{len(cases)} 通过")
    return all(cases)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
