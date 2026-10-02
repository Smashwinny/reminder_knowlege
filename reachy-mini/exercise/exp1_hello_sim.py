"""实验1：连接 MuJoCo 仿真里的 Reachy Mini，完成第一组动作。

目的：验证"仿真守护进程 + Python SDK"全链路跑通，小白的第一步。
"""

import time

from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose

print("== 连接仿真守护进程 (localhost) ==")
with ReachyMini(media_backend="no_media") as mini:
    print("[OK] 已连接仿真 Reachy Mini")

    # 1. 读当前关节位置（头部 7 个关节 + 天线 2 个，弧度）
    head_joints, antenna_joints = mini.get_current_joint_positions()
    print(f"[状态] 头部关节数: {len(head_joints)}, 天线关节数: {len(antenna_joints)}")
    print(f"[状态] 天线当前角度(rad): {[round(a, 3) for a in antenna_joints]}")

    # 2. 读当前头部位姿 4x4 矩阵，平移在最后一列
    pose = mini.get_current_head_pose()
    print(f"[状态] 头部当前位置 xyz(mm): {[round(float(pose[i, 3]) * 1000, 1) for i in range(3)]}")

    # 3. 抬头 + 侧倾（goto_target 平滑插值）
    print("-> 抬头 20mm + 侧倾 15 度")
    mini.goto_target(head=create_head_pose(z=20, roll=15, degrees=True, mm=True), duration=1.0)
    time.sleep(1.2)

    # 4. 天线摆动两下
    print("-> 天线摆动")
    for _ in range(2):
        mini.goto_target(antennas=[0.6, -0.6], duration=0.3)
        time.sleep(0.35)
        mini.goto_target(antennas=[-0.6, 0.6], duration=0.3)
        time.sleep(0.35)

    # 5. 回休息位
    print("-> 回休息位")
    mini.goto_target(head=create_head_pose(), antennas=[0.0, 0.0], duration=1.0)
    time.sleep(1.2)

    pose = mini.get_current_head_pose()
    print(f"[收尾] 头部位置 xyz(mm): {[round(float(pose[i, 3]) * 1000, 1) for i in range(3)]}")
    print("[OK] 实验1完成")
