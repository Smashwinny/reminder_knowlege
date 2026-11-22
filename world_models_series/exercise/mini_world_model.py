#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""迷你世界模型演示：8x8 网格弹跳球
复现世界模型三要素：①压缩表征(64→48 隐空间) ②想象训练(自回归滚动)
③想象误差随步数变化。环境是完全确定的周期系统，故发散缓慢——
真实物理环境的发散要快得多，这是本演示的诚实边界。
"""
import numpy as np
np.random.seed(42)
G = 8
def make_frame(pos):
    f = np.zeros(G*G); f[pos[0]*G+pos[1]] = 1.0; return f
def simulate(steps, p0=(1,1), v0=(1,1)):
    pos, vel = list(p0), list(v0); frames = []
    for _ in range(steps):
        for d in (0,1):
            pos[d] += vel[d]
            if pos[d] < 0 or pos[d] >= G: pos[d] -= 2*vel[d]; vel[d] = -vel[d]
        frames.append(make_frame(pos))
    return frames
def roll_data(n, steps=12):
    X, Y = [], []
    for _ in range(n):
        p0 = (np.random.randint(0,G), np.random.randint(0,G))
        v0 = (np.random.choice([-1,1]), np.random.choice([-1,1]))
        fr = simulate(steps, p0, v0)
        X += fr[:-1]; Y += fr[1:]
    return np.array(X), np.array(Y)

X, Y = roll_data(3000)
H = 48
W1 = np.random.randn(G*G, H)*0.3; b1 = np.zeros(H)
W2 = np.random.randn(H, G*G)*0.3; b2 = np.zeros(G*G)
def forward(x):
    h = np.tanh(x @ W1 + b1); return h @ W2 + b2
lr = 0.02
for epoch in range(400):
    idx = np.random.permutation(len(X))[:512]
    for i in idx:
        x, y = X[i], Y[i]
        h = np.tanh(x @ W1 + b1)
        pred = h @ W2 + b2
        err = pred - y
        gh = (err @ W2.T) * (1 - h*h)
        W2 -= lr*np.outer(h, err); b2 -= lr*err
        W1 -= lr*np.outer(x, gh); b1 -= lr*gh

one = [np.mean((forward(X[i]) - Y[i])**2) for i in range(500)]
print(f"单步预测 MSE: {np.mean(one):.4f}")
fr = simulate(12, (2,3), (1,-1))
cur = fr[0].copy(); errs = []
for t in range(1, 12):
    nxt = forward(cur); errs.append(np.mean((nxt - fr[t])**2)); cur = (nxt > 0.3).astype(float)
print("想象滚动逐步 MSE:", " ".join(f"{e:.3f}" for e in errs))
print("三要素：压缩表征(64→48) / 想象训练(自回归) / 误差随步数变化")
