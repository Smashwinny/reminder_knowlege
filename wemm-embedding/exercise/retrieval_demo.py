# -*- coding: utf-8 -*-
"""WeMM-Embedding-2B 多模态检索实验（RTX 4070 真实推理）。

步骤：
1. 编码 5 张图库图片 -> 向量（L2 归一化）
2. 编码文本查询 -> 向量
3. 余弦相似度排序，看 Top-1 是否语义正确
4. Matryoshka 截断：同一查询在 64~2048 维下重排序，对比 Top-1 稳定性
"""
import argparse
import json
from pathlib import Path

import torch
import torch.nn.functional as F
from qwen_vl_utils import process_vision_info
from transformers import AutoModel, AutoProcessor

IMAGES = [
    ("fashion_dress", "a dress / 一条连衣裙"),
    ("shirts_shelf", "shirts on a shelf / 货架上的衬衫"),
    ("product_detail", "product detail page / 商品详情页"),
    ("chart_doc", "a chart document / 图表文档"),
    ("street_text", "street scene with text / 带文字的街景"),
]

QUERIES = [
    "an elegant red dress for a party",
    "a shelf full of folded shirts",
    "a document with a bar chart",
    "a photo of a busy street",
    "a pair of sneakers",
]


def encode(processor, model, messages, device, dimension=None):
    prompt = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
    images, videos, video_kwargs = process_vision_info(
        messages, image_patch_size=16, return_video_kwargs=True, return_video_metadata=True
    )
    inputs = processor(
        text=prompt, images=images, videos=videos,
        return_tensors="pt", **video_kwargs,
    ).to(device)
    with torch.inference_mode():
        emb = model.embedding(**inputs).float()
    if dimension is not None:
        emb = F.normalize(emb[..., :dimension], dim=-1)
    return emb.cpu()


def img_messages(path):
    return [{"role": "user", "content": [{"type": "image", "image": str(path)}]}]


def txt_messages(text):
    return [{"role": "user", "content": [{"type": "text", "text": text}]}]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=str(Path(__file__).parent / "model"))
    ap.add_argument("--images", default=str(Path(__file__).parent / "images"))
    ap.add_argument("--device", default="cuda")
    args = ap.parse_args()

    processor = AutoProcessor.from_pretrained(args.model, trust_remote_code=True)
    model = AutoModel.from_pretrained(args.model, trust_remote_code=True, dtype=torch.bfloat16)
    model = model.to(args.device).eval()
    dims = model.config.matryoshka_dimensions
    full_dim = dims[-1]
    print(f"[加载完成] 支持 Matryoshka 维度: {dims}, 完整维度: {full_dim}")

    # 1) 图库向量（完整维度）
    gallery = {}
    for name, desc in IMAGES:
        emb = encode(processor, model, img_messages(Path(args.images) / f"{name}.webp"), args.device)
        gallery[name] = emb
        print(f"[图库] {name:15s} ({desc}) -> shape {tuple(emb.shape)}, L2范数 {emb.norm(dim=-1).item():.4f}")

    # 2) 文本查询 + 完整维度检索
    print("\n===== 完整维度 (%d) 文本搜图 =====" % full_dim)
    full_results = {}
    for q in QUERIES:
        qe = encode(processor, model, txt_messages(q), args.device)
        sims = {n: F.cosine_similarity(qe, g, dim=-1).item() for n, g in gallery.items()}
        ranked = sorted(sims.items(), key=lambda x: -x[1])
        full_results[q] = ranked
        top = ", ".join(f"{n}={s:.3f}" for n, s in ranked)
        print(f"查询: {q!r}\n  排序: {top}")

    # 3) Matryoshka 截断：不同维度下 Top-1 对比
    print("\n===== Matryoshka 截断稳定性 =====")
    print(f"{'查询':40s}" + "".join(f"{d:>8d}" for d in dims))
    for q in QUERIES:
        qe_full = encode(processor, model, txt_messages(q), args.device)
        tops = []
        for d in dims:
            qe = F.normalize(qe_full[..., :d], dim=-1)
            best, best_s = None, -2
            for n, g in gallery.items():
                gd = F.normalize(g[..., :d], dim=-1)
                s = F.cosine_similarity(qe, gd, dim=-1).item()
                if s > best_s:
                    best, best_s = n, s
            tops.append(f"{best:>8s}")
        print(f"{q[:38]:40s}" + "".join(tops))
    print("\n注: 每列是该维度下 Top-1 图片名；观察从 64 维到 2048 维 Top-1 是否保持稳定。")


if __name__ == "__main__":
    main()
