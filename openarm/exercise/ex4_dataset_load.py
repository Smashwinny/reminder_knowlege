# -*- coding: utf-8 -*-
"""ex4: 用 pip 安装的 openarm_dataset 加载仓库自带的真实采样数据（LeRobot v3.0 格式）。"""
import os
import openarm_dataset

FIX = os.path.join(os.path.dirname(__file__), "..", "repo", "subs",
                   "openarm_dataset", "tests", "fixture", "dataset_0.3.0")
ds = openarm_dataset.Dataset(FIX)

print("== 数据集元信息 ==")
print(f"episode 列表: {ds.meta.episodes}")
print(f"task 列表:    {ds.meta.tasks}")
print(f"num_episodes = {ds.num_episodes}")

obs = ds.load_obs(ds.meta.episodes[0])  # 本版 API 取 episode dict（README 的 load_obs(0) 是旧版签名）
print("\n== episode 0 的观测键（主从双臂+升降台）==")
for k in obs:
    print(f"  {k:<22} shape={obs[k].shape}")

print("\n== 右臂 qpos 前 3 帧（7 关节 + 1 夹爪，单位 rad）==")
print(obs["arms/right/qpos"].head(3).to_string())

act = ds.load_action(ds.meta.episodes[0])
print("\n== 动作键 ==", list(act.keys()))
q_r = obs["arms/right/qpos"]
import numpy as np
print("\n== 右臂 8 维关节全程行程（max-min）==")
for col, rng in zip(q_r.columns, np.ptp(q_r.values, axis=0)):
    print(f"  {col:<10} {rng:.4f} rad")
print(f"\n采样帧数 = {len(q_r)}, 每帧间隔约 "
      f"{(q_r.index[-1] - q_r.index[0]).total_seconds() / (len(q_r) - 1) * 1000:.1f} ms")
