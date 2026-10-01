# -*- coding: utf-8 -*-
"""实验 1：把 16 部电影的简介变成向量，存进 Qdrant。"""
import os
os.environ.setdefault("NO_PROXY", "localhost,127.0.0.1")

import numpy as np
from fastembed import TextEmbedding
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from movies_data import MOVIES

MODEL = "BAAI/bge-small-zh-v1.5"

# 第 1 步：加载本地 embedding 模型（首次运行会自动下载，之后走缓存）
print("加载模型", MODEL, "...")
model = TextEmbedding(MODEL)

# 第 2 步：把每部电影的简介编码成 512 维向量
texts = [f"{m['title']}（{m['genre']}，{m['year']}）：{m['desc']}" for m in MOVIES]
vectors = np.array(list(model.embed(texts)))
print(f"已编码 {len(vectors)} 条文本，每条 {vectors.shape[1]} 维")

# 第 3 步：连接 Qdrant，重建集合
client = QdrantClient(host="localhost", port=6333)
if client.collection_exists("movies"):
    client.delete_collection("movies")
client.create_collection(
    collection_name="movies",
    vectors_config=VectorParams(size=vectors.shape[1], distance=Distance.COSINE),
)

# 第 4 步：把向量 + 元数据（payload）一起写入
points = [
    PointStruct(id=m["id"], vector=vectors[i].tolist(),
                payload={"title": m["title"], "genre": m["genre"], "year": m["year"], "desc": m["desc"]})
    for i, m in enumerate(MOVIES)
]
client.upsert(collection_name="movies", points=points)

info = client.get_collection("movies")
print(f"集合 movies 建好：{info.points_count} 个点，状态 = {info.status}")
