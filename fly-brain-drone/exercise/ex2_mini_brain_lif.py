# ex2: 零依赖迷你全脑 LIF 仿真 —— 真实布线 vs 打乱布线（复刻 Shiu 2024 核心机制 + 无人机仓库 shuffle 对照思想）
# LIF 动力学与参数完全照抄 philshiu/Drosophila_brain_model model.py default_params，
# 只是把 Brian2 换成手写 numpy 稀疏仿真（解释性验证，不追求逐尖峰一致）。
import pandas as pd, numpy as np, os, time

BASE = os.path.join(os.path.dirname(__file__), '..', 'repo')
comp = pd.read_csv(os.path.join(BASE, '2023_03_23_completeness_630_final.csv'), index_col=0)
con = pd.read_parquet(os.path.join(BASE, '2023_03_23_connectivity_630_final.parquet'))
flyid2i = {f: i for i, f in enumerate(comp.index)}
N = len(comp)
print('v630 神经元:', N, ' 连接条目:', len(con))

# --- 全脑 LIF 参数（照抄 model.py） ---
v0, vrst, vth = -52.0, -52.0, -45.0     # mV
tau, t_rfc, t_dly = 5.0, 2.2, 1.8       # ms
w_syn, f_poi = 0.275, 250               # mV / 无量纲
dt = 0.1                                # ms 步长（model.py timestep 0.1ms）
T = 500.0                               # 仿真 500 ms 生物时间

pre = con['Presynaptic_Index'].values
post = con['Postsynaptic_Index'].values
w = con['Excitatory x Connectivity'].values.astype(np.float64) * w_syn

# 糖感知神经元（论文 phase0 的 21 个 v630 ID），刺激 1 秒里的前 500ms
neu_sugar = [720575940624963786,720575940630233916,720575940637568838,720575940638202345,
 720575940617000768,720575940630797113,720575940632889389,720575940621754367,720575940621502051,
 720575940640649691,720575940639332736,720575940616885538,720575940639198653,720575940620900446,
 720575940617937543,720575940632425919,720575940633143833,720575940612670570,720575940628853239,
 720575940629176663,720575940611875570]
id_mn9 = flyid2i[720575940660219265]
src = np.array([flyid2i[f] for f in neu_sugar])
drive_rate = 100.0  # Hz Poisson -> 每 dt 概率
p_drive = drive_rate / 1000.0 * dt

def simulate(post_arr, label):
    t0 = time.time()
    v = np.full(N, v0); g = np.zeros(N); rfc = np.zeros(N)
    order = np.argsort(post_arr)
    pre_s, post_s, w_s = pre[order], post_arr[order], w[order]
    starts = np.searchsorted(post_s, np.arange(N), 'left')
    ends = np.searchsorted(post_s, np.arange(N), 'right')
    mn9_spikes = 0; total = 0
    delay_steps = max(1, int(round(t_dly / dt)))
    g_inbuf = np.zeros((delay_steps, N), dtype=np.float32)
    spike_hist = np.zeros(delay_steps, dtype=bool)
    nsteps = int(T / dt)
    for step in range(nsteps):
        t_ms = step * dt
        # 泊松驱动糖感知神经元
        fired_in = (np.random.random(len(src)) < p_drive)
        g_inbuf[step % delay_steps, src[fired_in]] += w_syn * f_poi
        # 1.8ms 突触延迟: 把 delay_steps 步前的缓冲投入 g
        d = (step + 1) % delay_steps
        g += g_inbuf[d]; g_inbuf[d] = 0.0
        can = rfc <= 0
        v[can] += (v0 - v[can] + g[can]) * (dt / tau)
        g[~can] *= (1 - dt / tau); g[can] *= (1 - dt / tau)
        spk = can & (v > vth)
        if spk.any():
            idx = np.nonzero(spk)[0]
            total += len(idx)
            if id_mn9 in idx: mn9_spikes += 1
            v[idx] = vrst; g[idx] = 0.0
            rfc[idx] = t_rfc
            nxt = (step + delay_steps) % delay_steps
            np.add.at(g_inbuf[nxt], pre_s[np.isin(pre_s, idx)], 0)  # 占位(下面按出边传播)
            # 把尖峰沿突触传播（延迟 d 步后加到目标 g 缓冲）
            tgt = np.isin(pre_s, idx)
            np.add.at(g_inbuf[nxt], post_s[tgt], w_s[tgt])
        rfc = np.maximum(rfc - dt, 0)
    print(f'[{label}] {T:.0f}ms 仿真 耗时 {time.time()-t0:.1f}s | 全脑总发放 {total} | '
          f'MN9 发放 {mn9_spikes} 次 ({mn9_spikes/(T/1000):.1f} Hz)')
    return mn9_spikes

print('\n--- 真实布线: 刺激糖感知神经元 ---')
s_real = simulate(post, 'real')
print('\n--- 打乱布线(保强度保符号, 只换目标; shuffle_seed=1 同无人机仓库) ---')
rng = np.random.default_rng(1)
s_shuf = simulate(rng.permutation(post), 'shuffle1')

print(f'\n结论对照: 真实布线 MN9 {s_real} 次发放 vs 打乱布线 {s_shuf} 次 —— '
      + ('行为差异由布线特异性携带' if s_real != s_shuf else '本轮无差异, 详见日志讨论'))
print('EX2 DONE')
