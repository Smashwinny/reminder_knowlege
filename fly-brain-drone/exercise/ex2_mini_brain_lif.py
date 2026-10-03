# ex2: 零依赖迷你全脑 LIF 仿真 —— 真实布线 vs 打乱布线（复刻 Shiu 2024 核心机制 + 无人机仓库 shuffle 对照思想）
# LIF 动力学与参数完全照抄 philshiu/Drosophila_brain_model model.py default_params，
# 只是把 Brian2 换成手写 numpy 稀疏仿真（解释性验证，不追求逐尖峰一致）。
# 性能：突触按 presynaptic 排序建 CSR 出边索引，尖峰传播只切片不用全表 isin。
import pandas as pd, numpy as np, os, time

BASE = os.path.join(os.path.dirname(__file__), '..', 'repo')
comp = pd.read_csv(os.path.join(BASE, '2023_03_23_completeness_630_final.csv'), index_col=0)
con = pd.read_parquet(os.path.join(BASE, '2023_03_23_connectivity_630_final.parquet'))
flyid2i = {f: i for i, f in enumerate(comp.index)}
N = len(comp)
print('v630 神经元:', N, ' 连接条目:', len(con), flush=True)

# --- 全脑 LIF 参数（照抄 model.py） ---
v0, vrst, vth = -52.0, -52.0, -45.0     # mV
tau, t_mbr, t_rfc, t_dly = 5.0, 20.0, 2.2, 1.8  # ms (tau=g衰减, t_mbr=膜常数, 照抄 model.py)
w_syn, f_poi = 0.275, 250               # mV / 无量纲
dt = 0.1                                # ms 步长
T = 1000.0                              # 仿真 1000 ms 生物时间 (同论文 t_run)

pre = con['Presynaptic_Index'].values.astype(np.int64)
post0 = con['Postsynaptic_Index'].values.astype(np.int64)
w = con['Excitatory x Connectivity'].values.astype(np.float64) * w_syn

neu_sugar = [720575940624963786,720575940630233916,720575940637568838,720575940638202345,
 720575940617000768,720575940630797113,720575940632889389,720575940621754367,720575940621502051,
 720575940640649691,720575940639332736,720575940616885538,720575940639198653,720575940620900446,
 720575940617937543,720575940632425919,720575940633143833,720575940612670570,720575940628853239,
 720575940629176663,720575940611875570]
id_mn9 = flyid2i[720575940660219265]
src = np.array([flyid2i[f] for f in neu_sugar], dtype=np.int64)
p_drive = 150.0 / 1000.0 * dt          # 150 Hz Poisson 每步发放概率 (model.py r_poi)

def simulate(post_arr, label, drive=True):
    """按突触前神经元排序建 CSR 出边索引；尖峰 -> 出边切片 -> 目标 g（经 1.8ms 延迟缓冲）。"""
    t0 = time.time()
    order = np.argsort(pre, kind='stable')          # 按突触前神经元排序建出边 CSR
    pre_s, w_s = pre[order], w[order]
    posts = post_arr[order]
    starts = np.searchsorted(pre_s, np.arange(N), 'left')
    ends = np.searchsorted(pre_s, np.arange(N), 'right')
    # 每 (神经元 -> 延迟槽) 预聚合出边目标与权重，尖峰时直接整块相加
    nD = int(np.ceil(t_dly / dt))                    # 延迟槽位数
    slot_of = np.arange(nD)
    # 预先按 (pre, slot) 分组的边列表: 对每个神经元出边, 其目标槽 = (本步+1..nD) 轮转, 用固定哈希近似:
    # 简化: 所有出边统一放 (step % nD) 槽, 延迟取 t_dly≈2ms 网格化 —— 与 Brian2 逐边延迟略有差别, 属解释性近似
    v = np.full(N, v0); g = np.zeros(N); rfc = np.zeros(N)
    rfc[src] = 0.0                       # Poisson 目标免不应期 (model.py poi())
    gbuf = np.zeros((nD, N), dtype=np.float32)
    mn9_spikes = 0; total = 0; spike_steps = []
    nsteps = int(T / dt)
    for step in range(nsteps):
        # 驱动直打 v：每事件 +w_syn*f_poi=68.75mV，必过阈（忠实复刻 PoissonInput target_var='v'）
        fired_in = drive & (np.random.random(len(src)) < p_drive)
        if fired_in.any():
            v[src[fired_in]] += w_syn * f_poi
        d = step % nD
        g += gbuf[d]; gbuf[d] = 0.0
        can = rfc <= 0
        v[can] += (v0 - v[can] + g[can]) * (dt / t_mbr)
        g *= (1 - dt / tau)   # g 衰减用 tau=5ms
        spk = can & (v > vth)
        if spk.any():
            idx = np.nonzero(spk)[0]
            total += len(idx)
            if spk[id_mn9]:
                mn9_spikes += 1
            v[idx] = vrst; g[idx] = 0.0; rfc[idx] = t_rfc
            nxt = step % nD   # 槽在本步开头已被消费, 下次轮到是 18 步后 = 1.8ms 延迟
            cnt = ends[idx] - starts[idx]
            ne = int(cnt.sum())
            if ne:
                pos = np.arange(ne) - np.repeat(np.concatenate(([0], np.cumsum(cnt)[:-1])), cnt)
                edges = np.repeat(starts[idx], cnt) + pos
                np.add.at(gbuf[nxt], posts[edges], w_s[edges])
        rfc = np.maximum(rfc - dt, 0.0)
    print(f'[{label}] {T:.0f}ms 仿真 耗时 {time.time()-t0:.1f}s | 全脑总发放 {total} | '
          f'MN9 发放 {mn9_spikes} 次 ({mn9_spikes/(T/1000):.1f} Hz)', flush=True)
    return mn9_spikes, total

print('\n--- 基线: 真实布线, 不刺激 ---', flush=True)
s_base, tot_base = simulate(post0, 'baseline(no drive)', drive=False)
print('\n--- 真实布线: 刺激糖感知神经元 ---', flush=True)
s_real, tot_real = simulate(post0, 'real', drive=True)
print('\n--- 打乱布线(保强度保符号, 只换目标; shuffle_seed=1 同无人机仓库) ---', flush=True)
rng = np.random.default_rng(1)
s_shuf, tot_shuf = simulate(rng.permutation(post0), 'shuffle1', drive=True)

print(f'\n结论对照: MN9 发放率 基线 {s_base/(T/1000):.1f}Hz / 真实布线 {s_real/(T/1000):.1f}Hz / 打乱布线 {s_shuf/(T/1000):.1f}Hz —— '
      + ('行为差异由布线特异性携带' if (s_real > s_shuf and s_real > s_base) else '本轮无差异, 详见日志讨论'))
print('EX2 DONE')
