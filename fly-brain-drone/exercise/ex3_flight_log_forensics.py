# ex3: 无人机飞行日志取证 —— 用 drone_repo 自带的真实仿真输出现场验证"果蝇大脑会开无人机"
# 数据来源: ClutchMedia775/fly-brain-drone results/ (phase3 开环, phase4 真布线vs打乱, phase56_summary.json)
import pandas as pd, numpy as np, os, json, glob

BASE = os.path.join(os.path.dirname(__file__), '..', 'drone_repo', 'results')

def min_dist(path):
    df = pd.read_csv(path)
    return float(df['dist'].min()), len(df)

print('=== 1. phase3 开环: 有脑 vs 无脑 (looming 威胁从 az+30 来) ===')
for f in ['loom_az+30_brain.csv', 'loom_az+30_nobrain.csv', 'loom_az-30_brain.csv', 'loom_az-30_nobrain.csv']:
    md, n = min_dist(os.path.join(BASE, 'phase3', f))
    print(f'  {f:28s} 最近距离 min(dist) = {md:6.2f} m   记录 {n} 帧')

print('\n=== 2. 脑在做什么: 有脑试次的 DN 发放时刻 ===')
df = pd.read_csv(os.path.join(BASE, 'phase3', 'loom_az+30_brain.csv'))
hot = df[df['DN_all_right'] > 0]
print(f'  右侧 DN_all 发放>0 的帧: {len(hot)}/{len(df)}; 首次响应 t = {float(hot["t"].iloc[0]) if len(hot) else None:.2f}s')
print(f'  turn 指令峰值 = {df["turn"].max():.2f}; gf(逃跑 climbing) 峰值 = {df["gf"].max():.2f}')
nb = pd.read_csv(os.path.join(BASE, 'phase3', 'loom_az+30_nobrain.csv'))
print(f'  无脑对照: turn 峰值 = {nb["turn"].max():.2f}, gf 峰值 = {nb["gf"].max():.2f} (应全 0)')

print('\n=== 3. phase4: 真布线 vs 打乱布线 (同场景 az±30) ===')
rows = []
for cond in ['real', 'shuffle1', 'shuffle2']:
    for az in ['az+30', 'az-30']:
        md, _ = min_dist(os.path.join(BASE, 'phase4', f'loom_{az}_{cond}.csv'))
        rows.append((cond, az, md))
        print(f'  {cond:9s} {az:6s} min(dist) = {md:6.2f} m')
r = pd.DataFrame(rows, columns=['cond', 'az', 'min_dist'])
print(f'  真布线平均 {r[r.cond=="real"].min_dist.mean():.2f} m vs 打乱平均 {r[r.cond!="real"].min_dist.mean():.2f} m')

print('\n=== 4. phase56_summary.json 官方 n=20 统计对账 ===')
s = json.load(open(os.path.join(BASE, 'phase56_summary.json')))
for c in s['main']:
    print(f"  {c['cond']:9s} n={c['n']:3d}  平均最近距离 {c['mean_min_dist']:.2f} m  CI[{c['ci'][0]:.2f},{c['ci'][1]:.2f}]  逃避率 {c['evade_rate']:.0%}  正确侧率 {c['correct_side_rate']:.0%}")

print('\n=== 5. 消融: 摘掉哪些下行神经元会让避障失效 ===')
for a in s['ablate']:
    print(f"  {a['variant']:22s} min_dist {a['mean_min_dist']:.2f} m  peak_turn {a['mean_peak_turn']:.2f}")
print('\nEX3 DONE')
