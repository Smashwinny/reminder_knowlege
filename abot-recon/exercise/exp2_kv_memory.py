# -*- coding: utf-8 -*-
"""
实验2：为什么 22000 帧只要 6.71 GiB——固定 12 帧窗口 vs 全序列 KV 显存账本
（纯 Python 计算，用仓库 config.json 里的真实参数）

关键事实（从仓库代码里挖出来的）：
  - config.json: input 504x280, local_window_frames=12, max_frames=22000
  - modeling/pi3: DINOv2 patch size 14 → 每帧 token 数 = (504/14) x (280/14) = 36 x 20 = 720
  - decoder_size='large'，gate_layers=list(range(36)) → 36 层 decoder 都参与窗口注意力
  - attention: 12 头，head_dim 64（ViT-L 标准）→ 每层每 token KV = 2 * 12 * 64
  - streaming 模式：只保留最近 12 帧的 KV（StreamingKVState / prune_window_carry）
"""
import json
import math
import pathlib

repo = pathlib.Path(__file__).resolve().parents[1] / "repo"
cfg = json.loads((repo / "config.json").read_text(encoding="utf-8"))
H, W = cfg["input_height"], cfg["input_width"]
WIN = cfg["local_window_frames"]
MAXF = 22_000

tokens_per_frame = (W // 14) * (H // 14)
num_layers = 36          # gate_layers=list(range(36))
num_heads = 12
head_dim = 64
kv_per_token_per_layer = 2 * num_heads * head_dim * 2  # 2=K和V, 2=bf16字节数

kv_window_bytes = WIN * tokens_per_frame * num_layers * kv_per_token_per_layer
kv_full_bytes = MAXF * tokens_per_frame * num_layers * kv_per_token_per_layer

print(f"输入分辨率: {W}x{H}  patch14 → 每帧 token = {(W//14)}x{(H//14)} = {tokens_per_frame}")
print(f"局部窗口 = {WIN} 帧 | 最大序列 = {MAXF} 帧 | decoder 层数 = {num_layers}")
print()
print(f"{'方案':<28}{'KV 缓存大小':>16}{'换算':>20}")
print("-" * 64)
print(f"{'普通全局注意力(22000帧)':<26}{kv_full_bytes/2**30:>13.1f} GiB{'≈ 显存爆炸':>16}")
print(f"{'ABot-Recon(12帧滑动窗口)':<26}{kv_window_bytes/2**20:>13.1f} MiB{'≈ 显存常量':>16}")
print()
print(f"省了 {kv_full_bytes/kv_window_bytes:,.0f} 倍 —— 这就是'无长程依赖'的账本：")
print(f"KV 缓存只随窗口大小(12帧)增长，与已处理序列长度(0~22000帧)完全无关。")
print(f"论文实测 KITTI-02: 24.45 FPS / 6.71 GiB（含权重+激活，KV 仅是其中固定一小块）")

# 顺带验证：仓库 config 强制 local_window_frames 必须是 12
import sys
sys.path.insert(0, str(repo))
from abot_recon.config import InferenceConfig
try:
    InferenceConfig(local_window_frames=11)
    print("\n[意外] local_window_frames=11 竟然通过了校验？")
except ValueError as e:
    print(f"\n[校验验证] InferenceConfig(local_window_frames=11) → ValueError: {e}")
ok = InferenceConfig(local_window_frames=12)
print(f"[校验验证] InferenceConfig(local_window_frames=12) → OK, max_frames={ok.max_frames}, 分辨率={ok.width}x{ok.height}")
