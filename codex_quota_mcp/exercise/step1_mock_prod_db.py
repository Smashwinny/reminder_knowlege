# -*- coding: utf-8 -*-
"""实验第 1 步：造一个模拟的"生产数据库"（AIHOT 站点：用户表 + API 成本表）。

真实场景里这是卡兹克的线上业务库；实验里我们用 SQLite 本地模拟，
后面的只读 MCP Server 将以 mode=ro 方式挂载它。
"""
import sqlite3
import os
import random

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "aihot_prod.db")
if os.path.exists(DB):
    os.remove(DB)  # 可重复实验：每次重建

conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.executescript(
    """
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        nickname TEXT,
        plan TEXT,             -- free / pro
        created_at TEXT
    );
    CREATE TABLE api_costs (
        id INTEGER PRIMARY KEY,
        model TEXT,            -- gpt6-astra-high / gpt6-astra-ultra / ...
        endpoint TEXT,
        tokens INTEGER,
        cost_usd REAL,
        called_at TEXT
    );
    """
)

random.seed(42)
plans = ["free"] * 8 + ["pro"] * 2
models = ["gpt6-astra-high", "gpt6-astra-ultra", "gpt6-pro-web", "embedding-s"]
eps = [" /v1/chat", " /v1/plan", " /v1/embed"]

for i in range(1, 201):
    cur.execute(
        "INSERT INTO users VALUES (?,?,?,?)",
        (i, f"user_{i:03d}", random.choice(plans), f"2026-0{random.randint(1,9)}-{random.randint(10,28)}"),
    )

rid = 0
for day in range(1, 15):  # 两周成本流水
    for _ in range(random.randint(8, 15)):
        rid += 1
        m = random.choice(models)
        # ultra 一次规划贵 25 倍（对应正文：Ultra 规划一次烧掉周额度 10%）
        tok = random.randint(2000, 6000) * (25 if "ultra" in m else 1)
        cost = tok * 1e-5
        cur.execute(
            "INSERT INTO api_costs VALUES (?,?,?,?,?,?)",
            (rid, m, random.choice(eps), tok, round(cost, 4), f"2026-09-{day:02d} 1{random.randint(0,9)}:{random.randint(10,59)}"),
        )

conn.commit()
conn.close()
print(f"[OK] 模拟生产库已生成: {DB}")
print(f"     users=200 行, api_costs={rid} 行")
