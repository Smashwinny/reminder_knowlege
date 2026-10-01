# -*- coding: utf-8 -*-
"""实验 3：向量搜索 + payload 过滤——只在一部分点里搜。"""
import os
os.environ.setdefault("NO_PROXY", "localhost,127.0.0.1")

import numpy as np
from fastembed import TextEmbedding
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue

MODEL = "BAAI/bge-small-zh-v1.5"

model = TextEmbedding(MODEL)
client = QdrantClient(host="localhost", port=6333)

query = "关于动物的搞笑冒险"
print("查询：", query)
v = np.array(list(model.embed([query]))[0]).tolist()

print("\n[不过滤] Top3：")
res = client.query_points("movies", query=v, limit=3).points
for p in res:
    print(f"  {p.score:.4f}  {p.payload['title']}（{p.payload['genre']}，{p.payload['year']}）")

print("\n[过滤 genre=动画] Top3：")
anime = Filter(must=[FieldCondition(key="genre", match=MatchValue(value="动画"))])
res = client.query_points("movies", query=v, query_filter=anime, limit=3).points
for p in res:
    print(f"  {p.score:.4f}  {p.payload['title']}（{p.payload['genre']}，{p.payload['year']}）")

print("\n[过滤 year>=2015 的科幻片] Top3：")
recent_sf = Filter(must=[
    FieldCondition(key="genre", match=MatchValue(value="科幻")),
    FieldCondition(key="year", range={"gte": 2015}),
])
res = client.query_points("movies", query=v, query_filter=recent_sf, limit=3).points
for p in res:
    print(f"  {p.score:.4f}  {p.payload['title']}（{p.payload['genre']}，{p.payload['year']}）")
