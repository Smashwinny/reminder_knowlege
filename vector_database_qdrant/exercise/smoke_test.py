# -*- coding: utf-8 -*-
"""冒烟测试：创建集合 -> 插入向量 -> 相似度搜索，验证 Qdrant 全链路可用。"""
from qdrant_client import QdrantClient

client = QdrantClient(host="localhost", port=6333)

# 1. 建集合：4 维向量，余弦相似度
if client.collection_exists("smoke"):
    client.delete_collection("smoke")
client.create_collection(
    collection_name="smoke",
    vectors_config={"size": 4, "distance": "Cosine"},
)
print("集合已创建:", client.get_collections().collections[0].name if client.get_collections().collections else "?")

# 2. 插入 3 个"文档"（这里直接手写向量代表 embedding）
from qdrant_client.models import PointStruct, VectorParams, Distance
client.upsert(
    collection_name="smoke",
    points=[
        PointStruct(id=1, vector=[0.9, 0.1, 0.0, 0.0], payload={"text": "猫吃鱼"}),
        PointStruct(id=2, vector=[0.8, 0.2, 0.1, 0.0], payload={"text": "小猫捕食鱼类"}),
        PointStruct(id=3, vector=[0.0, 0.0, 0.9, 0.8], payload={"text": "今天股市大涨"}),
    ],
)

# 3. 搜索：用"猫吃鱼"的向量找最相似的
hits = client.query_points("smoke", query=[0.9, 0.1, 0.0, 0.0], limit=3).points
for h in hits:
    print(f"id={h.id} score={h.score:.4f} text={h.payload['text']}")
