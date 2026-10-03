# ex1: 果蝇全脑连接组数据解剖（零 Brian2，仅 pandas/numpy）
# 数据: philshiu/Drosophila_brain_model 自带的 FlyWire v630 / v783 真实连接组
import pandas as pd, numpy as np, os

BASE = os.path.join(os.path.dirname(__file__), '..', 'repo')

print('=== 1. v783 神经元清单 ===')
comp = pd.read_csv(os.path.join(BASE, 'Completeness_783.csv'), index_col=0)
print('Completeness_783.csv 列:', list(comp.columns))
print('神经元总数:', len(comp))

print('\n=== 2. v783 连接表 ===')
con = pd.read_parquet(os.path.join(BASE, 'Connectivity_783.parquet'))
print('连接表形状:', con.shape)
print('列名:', list(con.columns))
print('总连接条目:', len(con))
print('突触数合计(权重求和):', int(con['Excitatory x Connectivity'].sum()))

print('\n=== 3. 度分布抽查 ===')
out_deg = con.groupby('Presynaptic_ID')['Excitatory x Connectivity'].sum()
in_deg = con.groupby('Postsynaptic_ID')['Excitatory x Connectivity'].sum()
print('出度(top5 突触数最多的上游神经元):')
print(out_deg.sort_values(ascending=False).head(5).to_string())
print('入度(top5):')
print(in_deg.sort_values(ascending=False).head(5).to_string())
print('中位出度:', float(out_deg.median()), ' 中位入度:', float(in_deg.median()))

print('\n=== 4. 论文示例通路核查: 糖感知神经元 -> MN9 运动神经元 ===')
# phase0.py 用的 21 个糖感知神经元 (v630 ID) 与 MN9 (v630 ID 720575940660219265)
neu_sugar = [720575940624963786,720575940630233916,720575940637568838,720575940638202345,
 720575940617000768,720575940630797113,720575940632889389,720575940621754367,720575940621502051,
 720575940640649691,720575940639332736,720575940616885538,720575940639198653,720575940620900446,
 720575940617937543,720575940632425919,720575940633143833,720575940612670570,720575940628853239,
 720575940629176663,720575940611875570]
id_mn9 = 720575940660219265

con630 = pd.read_parquet(os.path.join(BASE, '2023_03_23_connectivity_630_final.parquet'))
comp630 = pd.read_csv(os.path.join(BASE, '2023_03_23_completeness_630_final.csv'), index_col=0)
print('v630 神经元总数:', len(comp630), ' 连接条目:', len(con630))

sub = con630[con630['Postsynaptic_ID'] == id_mn9]
direct = sub[sub['Presynaptic_ID'].isin(neu_sugar)]
print('MN9 的上游连接条目:', len(sub), ' 来自糖感知神经元的直接连接:', len(direct))
print('糖感知神经元直接突触到 MN9 合计权重:', int(direct['Excitatory x Connectivity'].sum()) if len(direct) else 0)

# BFS: 糖感知神经元 2 跳内能到 MN9 吗（真实布线 vs 打乱布线对照）
flyid2i = {f: i for i, f in enumerate(comp630.index)}
pre = con630['Presynaptic_ID'].map(flyid2i).values
post = con630['Postsynaptic_ID'].map(flyid2i).values
src = np.array([flyid2i[f] for f in neu_sugar]); tgt = flyid2i[id_mn9]

reach1 = set(post[np.isin(pre, src)])
frontier = reach1 | set(src)
reach2 = set(post[np.isin(pre, list(frontier))])
print('1 跳可达神经元数:', len(reach1), '  2 跳可达:', len(reach2), '  MN9 在 2 跳内:', tgt in reach2)

rng = np.random.default_rng(42)
hits = 0
for s in range(20):
    post_s = rng.permutation(post)
    r1 = set(post_s[np.isin(pre, src)])
    fr = r1 | set(src)
    r2 = set(post_s[np.isin(pre, list(fr))])
    if tgt in r2: hits += 1
print(f'打乱布线 20 次对照: MN9 仍在 2 跳内的次数 = {hits}/20 (真实布线则是确定性的)')
print('\nEX1 DONE')
