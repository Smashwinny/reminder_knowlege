"""实验2：插值方法对比 —— 记录真实轨迹，量化 LINEAR / MINJERK / EASE_IN_OUT / CARTOON 差异。

做法：对头部位姿不做硬件读取之外的假设 —— 用 goto_target 发目标，
以 100Hz 采样 get_current_head_pose() 的 z 平移，得到真实运动曲线。
最后输出每个方法的：到达时间、最大速度、是否过冲（超过目标后又回落）。
"""

import time

import numpy as np

from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose
from reachy_mini.utils.interpolation import InterpolationTechnique

TARGET_Z_MM = 20.0
DURATION = 1.0
SAMPLE_HZ = 100


def record_goto(mini, method) -> np.ndarray:
    """发出 goto 目标，同时以 SAMPLE_HZ 采样真实 z 位置，返回采样序列(mm)。"""
    samples: list[float] = []
    t0 = time.perf_counter()
    # goto_target 是阻塞式平滑插值，先开采样线程式循环不可行，
    # 所以改为：set_target 循环 + 自己按插值公式？不 —— 正确做法是 daemon 端插值，
    # SDK 端 goto_target 阻塞期间我们无法采样。因此用"先采样再补发"策略：
    # goto_target 内部是分帧 set_target，采样线程与之并行。
    done = False

    def worker():
        nonlocal done
        mini.goto_target(
            head=create_head_pose(z=TARGET_Z_MM, degrees=True, mm=True),
            duration=DURATION,
            method=method,
        )
        done = True

    import threading

    th = threading.Thread(target=worker)
    th.start()
    while not done or len(samples) < 2:
        pose = mini.get_current_head_pose()
        samples.append(float(pose[2, 3]) * 1000.0)
        time.sleep(1.0 / SAMPLE_HZ)
        if time.perf_counter() - t0 > DURATION * 3 + 1.0:  # 保险丝
            break
    th.join(timeout=2.0)
    return np.array(samples)


def main() -> None:
    with ReachyMini(media_backend="no_media") as mini:
        print(f"{'方法':<14} {'到达时间(s)':>10} {'最大速度(mm/s)':>14} {'过冲量(mm)':>10} {'终点误差(mm)':>12}")
        print("-" * 66)
        for method in InterpolationTechnique:
            # 先回零
            mini.goto_target(head=create_head_pose(), duration=0.5)
            time.sleep(0.7)
            z = record_goto(mini, method)
            dt = 1.0 / SAMPLE_HZ
            vel = np.abs(np.diff(z)) / dt
            # 到达时间：首次进入目标 ±1mm 且不再离开
            within = np.abs(z - TARGET_Z_MM) <= 1.0
            arrival_idx = int(np.argmax(within)) if within.any() else len(z) - 1
            overshoot = float(np.max(z) - TARGET_Z_MM)
            print(
                f"{method.value:<14} {arrival_idx * dt:>10.2f} {float(np.max(vel)):>14.1f} "
                f"{overshoot:>10.2f} {abs(z[-1] - TARGET_Z_MM):>12.2f}"
            )
            np.save(f"trace_{method.value}.npy", z)

        # 回休息位
        mini.goto_target(head=create_head_pose(), duration=1.0)
    print("[OK] 实验2完成，轨迹已存 trace_*.npy")


if __name__ == "__main__":
    main()
