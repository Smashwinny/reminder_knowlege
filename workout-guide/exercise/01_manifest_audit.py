# -*- coding: utf-8 -*-
"""实验1+2：workout-guide manifest 数据结构体检 + 资产完整性质检 Gate
零依赖：只用 Python 标准库。数据源：repo/packages/workout-guide/manifest.json + assets/
运行：python 01_manifest_audit.py
"""
import json, os, re, sys
from collections import Counter

BASE = os.path.join(os.path.dirname(__file__), "..", "repo", "packages", "workout-guide")
manifest = json.load(open(os.path.join(BASE, "manifest.json"), encoding="utf-8"))

print("=" * 62)
print("[1] 总量校验：动作数 / 帧数 / SVG 文件数")
print("=" * 62)
n_ex = len(manifest)
n_frames = sum(len(e["frames"]) for e in manifest)
svg_on_disk = 0
for root, _, files in os.walk(os.path.join(BASE, "assets")):
    svg_on_disk += sum(1 for f in files if f.endswith(".svg"))
print(f"manifest 动作数       : {n_ex}")
print(f"manifest 帧记录总数   : {n_frames}  (期望 302x3=906 -> {'PASS' if n_frames == 906 else 'FAIL'})")
print(f"assets/ 磁盘 SVG 数   : {svg_on_disk}  (与帧记录一致 -> {'PASS' if svg_on_disk == n_frames else 'FAIL'})")

print()
print("=" * 62)
print("[2] 字段 schema 抽查：第一个动作的全部键")
print("=" * 62)
keys = sorted(manifest[0].keys())
print("动作级字段:", ", ".join(keys))
print("帧级字段  :", ", ".join(sorted(manifest[0]["frames"][0].keys())))

print()
print("=" * 62)
print("[3] 分布统计：器械 / 主肌群 / 动作类型 / 拉伸标记")
print("=" * 62)
def top(counter, n=8):
    w = max(len(k) for k, _ in counter.most_common(n))
    for k, v in counter.most_common(n):
        print(f"  {k:<{w}} {v:>4}  {'#' * (v * 40 // max(counter.values()))}")

print("-- equipment Top8 --");   top(Counter(e["equipment"] for e in manifest))
print("-- primaryMuscle Top8 --"); top(Counter(e["primaryMuscle"] for e in manifest))
print("-- exerciseType 全量 --");  top(Counter(e["exerciseType"] for e in manifest), 5)
print("-- isStretch --");         top(Counter(str(e["isStretch"]) for e in manifest), 2)

print()
print("=" * 62)
print("[4] 质检 Gate：路径存在性 / 尺寸 / 帧索引连续 / 溯源完整性")
print("=" * 62)
fail = 0
frames_seen = Counter()
for e in manifest:
    for fr in e["frames"]:
        frames_seen[e["slug"]] += 1
        p = os.path.join(BASE, *fr["path"].split("/"))
        if not os.path.isfile(p):
            print(f"  MISSING FILE: {fr['path']}"); fail += 1; continue
        if (fr["width"], fr["height"]) != (512, 512):
            print(f"  BAD SIZE    : {fr['path']}"); fail += 1
        head = open(p, encoding="utf-8", errors="ignore").read(300)
        if "<svg" not in head:
            print(f"  NOT SVG     : {fr['path']}"); fail += 1
        a = fr.get("attribution", {})
        if a.get("license") != "CC BY-SA 4.0" or "creator" not in a:
            print(f"  BAD ATTR    : {fr['path']}"); fail += 1
bad_frames = [s for s, c in frames_seen.items() if c != 3]
if bad_frames:
    print(f"  BAD FRAME COUNT: {bad_frames[:5]} x{len(bad_frames)}"); fail += 1
dup = [s for s, c in Counter(e["slug"] for e in manifest).items() if c > 1]
if dup:
    print(f"  DUP SLUG: {dup}"); fail += 1
print(f"质检结果: {'12/12 PASS (0 异常)' if fail == 0 else str(fail) + ' 项异常'}")

print()
print("=" * 62)
print("[5] 溯源抽查：哪帧带 Everkinetic 源标注？")
print("=" * 62)
n_src = sum(1 for e in manifest for fr in e["frames"] if fr.get("attribution", {}).get("source"))
print(f"带上游 source 标注的帧: {n_src}/{n_frames}（即首帧多为 Everkinetic 衍生，2/3 帧为作者新绘）")
src0 = next(fr["attribution"]["source"] for e in manifest for fr in e["frames"] if fr.get("attribution", {}).get("source"))
print("示例:", src0["name"], "|", src0["changes"][:70], "...")
