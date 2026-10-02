# -*- coding: utf-8 -*-
"""ex1: OpenArm 多仓库组织盘点 —— 用脚本真实统计各子仓库的开源范围。"""
import os, json

SUBS = ["openarm_can", "openarm_mujoco", "openarm_description",
        "openarm_dataset", "openarm_teleop", "openarm_hardware"]
BASE = os.path.join(os.path.dirname(__file__), "..", "repo", "subs")
PORTAL = os.path.join(os.path.dirname(__file__), "..", "repo")

SKIP = {".git", ".github"}

def survey(path):
    n_files, exts, total = 0, {}, 0
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for f in files:
            fp = os.path.join(root, f)
            n_files += 1
            total += os.path.getsize(fp)
            ext = os.path.splitext(f)[1].lower() or "(无扩展名)"
            exts[ext] = exts.get(ext, 0) + 1
    top3 = sorted(exts.items(), key=lambda kv: -kv[1])[:4]
    return n_files, total, top3

def first_license_line(path):
    for name in os.listdir(path):
        if name.lower().startswith("license"):
            with open(os.path.join(path, name), encoding="utf-8", errors="ignore") as fh:
                return " ".join(fh.read().split())[:90]
    return "(仓库根无 LICENSE 文件)"

print(f"{'子仓库':<22}{'文件数':>6}{'体积':>10}  主要文件类型 / 许可证开头")
print("-" * 100)
n, t, _ = survey(PORTAL)
print(f"{'openarm(门户)':<22}{n:>6}{t/1024:>9.0f}K  Docusaurus 文档站 / Apache-2.0")
rows = {}
for s in SUBS:
    p = os.path.join(BASE, s)
    n, t, top3 = survey(p)
    rows[s] = dict(files=n, bytes=t, top3=[e for e, _ in top3],
                   license=first_license_line(p))
    print(f"{s:<22}{n:>6}{t/1024:>9.0f}K  {top3} / {rows[s]['license'][:48]}")

# 硬件仓库重点：数一数 STEP/STL 等 CAD 文件
hw = os.path.join(BASE, "openarm_hardware")
cad = {}
for root, dirs, files in os.walk(hw):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for f in files:
        e = os.path.splitext(f)[1].lower()
        if e in (".step", ".stp", ".stl", ".f3d", ".f3z", ".dxf"):
            cad[e] = cad.get(e, 0) + 1
print("\nopenarm_hardware 中的 CAD 制造文件统计:", json.dumps(cad, ensure_ascii=False))

# MuJoCo 三代模型清单
mj = os.path.join(BASE, "openarm_mujoco")
gens = sorted({root.replace(mj, "").split(os.sep)[1]
               for root, _, _ in os.walk(mj) if root != mj and ".git" not in root})
print("openarm_mujoco 模型代际目录:", gens)
