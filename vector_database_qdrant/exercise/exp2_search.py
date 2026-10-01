# -*- coding: utf-8 -*-
"""实验 2：语义搜索 vs 关键词搜索——Qdrant 高光时刻。"""
import os
os.environ.setdefault("NO_PROXY", "localhost,127.0.0.1")

import numpy as np
from fastembed import TextEmbedding
from qdrant_client import QdrantClient
from movies_data import MOVIES

MODEL = "BAAI/bge-small-zh-v1.5"

model = TextEmbedding(MODEL)
client = QdrantClient(host="localhost", port=6333)

QUERIES = [
    "机器有了自我意识，人类活在虚假世界里",
    "在星空深处寻找人类未来的希望",
    "一个傻乎乎但心地善良的人的一生",
]


def keyword_search(query, k=3):
    """朴素关键词搜索：简介里包含查询词的任意连续片段才算命中。"""
    hits = [m for m in MOVIES if query in f"{m['title']} {m['desc']}"]
    return hits[:k]


def semantic_search(query, k=3):
    v = list(model.embed([query]))[0]
    res = client.query_points("movies", query=np.array(v).tolist(), limit=k).points
    return [(p.payload["title"], p.score) for p in res]


for q in QUERIES:
    print("=" * 62)
    print("查询：", q)
    kw = keyword_search(q)
    print(f"  [关键词搜索] 命中 {len(kw)} 条：" + (", ".join(m["title"] for m in kw) if kw else "（0 条——没有一个字相同）"))
    print("  [语义搜索] Top3：")
    for title, score in semantic_search(q):
        print(f"      {score:.4f}  {title}")
