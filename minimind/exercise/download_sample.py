# -*- coding: utf-8 -*-
"""从魔搭流式采样 pretrain_t2t_mini.jsonl 的前 N 行，作为本机小步数实验子集。"""
import urllib.request
import json
import sys

URL = "https://www.modelscope.cn/datasets/gongjy/minimind_dataset/resolve/master/pretrain_t2t_mini.jsonl"
OUT = "dataset/pretrain_sample.jsonl"
N = 20000

count = 0
bytes_read = 0
with urllib.request.urlopen(URL, timeout=60) as resp, open(OUT, "w", encoding="utf-8") as f:
    for raw in resp:
        bytes_read += len(raw)
        line = raw.decode("utf-8", errors="ignore").strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if "text" not in obj:
            continue
        f.write(json.dumps({"text": obj["text"]}, ensure_ascii=False) + "\n")
        count += 1
        if count % 2000 == 0:
            print(f"sampled {count} lines, {bytes_read/1e6:.1f} MB streamed", flush=True)
        if count >= N:
            break

print(f"DONE: {count} samples -> {OUT}, total streamed {bytes_read/1e6:.1f} MB")
