# -*- coding: utf-8 -*-
"""
SLAM-Former 代码契约对拍：论文/宣传里的关键机制，是否真的写在开源代码里？
零依赖（仅标准库），对 repo 源码做逐条 PASS/FAIL 检查。
运行: python contract_check.py
"""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "repo")
REPO = os.path.normpath(REPO)

def read(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8", errors="ignore") as f:
        return f.read()

def exists(rel):
    return os.path.exists(os.path.join(REPO, rel))

checks = []  # (名称, 证据出处, lambda: bool)

# ---- 1. 模型本体 ----
sf = read("src/slamformer/models/slamformer.py")
checks += [
    ("单一 Transformer 类 SLAMFormer 存在", "src/slamformer/models/slamformer.py",
     lambda: "class SLAMFormer(nn.Module" in sf),
    ("默认 KV 保留率 retention_ratio=0.5（论文 γ）", "slamformer.py:35",
     lambda: re.search(r"retention_ratio\s*=\s*0\.5", sf) is not None),
    ("DivPrune 多样性剪枝（余弦距离贪心选 token）", "slamformer.py:215",
     lambda: "divprune" in sf.lower() and "cosine" in sf.lower()),
    ("只剪 token 流、缓存剪枝索引（流式 KV 复用）", "slamformer.py:174-176",
     lambda: "_prune_idx_cache" in sf),
    ("ConvHead 点图头（point_head）", "models/layers/conv_head.py",
     lambda: "ConvHead(" in sf and exists("src/slamformer/models/layers/conv_head.py")),
    ("每帧输出局部点图+置信度+位姿（local_points/conf/camera_poses）", "slamformer.py:434-461",
     lambda: all(k in sf for k in ["local_points", "conf", "camera_poses"])),
    ("后端周期 bn_every（全注意力精化全部 map tokens）", "slamformer.py",
     lambda: "bn_every" in sf),
    ("Pi3/DINOv2 图像编码器", "models/dinov2/",
     lambda: exists("src/slamformer/models/dinov2")
             and re.search(r"pi3|dinov2", sf, re.I) is not None),
]

# ---- 2. SLAM 流水线 ----
demo = read("slam/demo.py")
checks += [
    ("前端关键帧阈值 kf_th（增量跟踪）", "slam/demo.py:50",
     lambda: "kf_th" in demo),
    ("后端每 bn_every=10 关键帧运行一次", "slam/demo.py:53",
     lambda: re.search(r"bn_every\s*=\s*10", demo) is not None),
    ("CLI 暴露 --retention_ratio（KV 剪枝保留率）", "slam/demo.py:516",
     lambda: "--retention_ratio" in demo and "KV Pruning" in demo),
    ("输出稠密结果 final.ply + 轨迹 final_traj.txt", "README.md",
     lambda: "final.ply" in read("README.md")),
]

# ---- 3. 血统与开源事实 ----
readme = read("README.md")
checks += [
    ("CroCo 训练底座代码在仓库（src/croco）", "src/croco/",
     lambda: exists("src/croco/models/croco.py")),
    ("HuggingFace 发布权重 checkpoint", "README.md",
     lambda: "huggingface.co" in readme),
    ("ECCV 2026 接收标注", "README.md",
     lambda: "ECCV 2026" in readme),
    ("SLAMFormer-∞ 后续作已挂链接（2026-08-08）", "README.md Updates",
     lambda: "SLAMFormer" in readme and "Infinity" in readme
             or "∞" in readme),
    ("BSD-3-Clause 许可证", "LICENSE",
     lambda: "BSD 3-Clause" in read("LICENSE") or "BSD-3-Clause" in read("LICENSE")),
    ("评测栈依赖：evo(ATE)/gsplat(渲染)/rerun(可视化)", "requirements.txt",
     lambda: all(d in read("requirements.txt") for d in ["evo", "gsplat", "rerun-sdk"])),
]

# ---- 运行 ----
print("=" * 72)
print("SLAM-Former 代码契约对拍 contract_check.py（无 GPU，纯源码检查）")
print("repo @", end=" ")
import subprocess
head = subprocess.run(["git", "-C", REPO, "log", "--oneline", "-1"],
                      capture_output=True, text=True).stdout.strip()
print(head)
print("=" * 72)
npass = 0
for name, where, fn in checks:
    try:
        ok = bool(fn())
    except Exception as e:
        ok = False
        where += f" (err: {e})"
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  <<{where}>>")
    npass += ok
print("=" * 72)
print(f"结果: {npass}/{len(checks)} PASS")
sys.exit(0 if npass == len(checks) else 1)
