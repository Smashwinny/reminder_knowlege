"""实验3：给机器人一段"表情序列" —— 用 goto_target 编排 3 个情感动作。

目的：体会"表情机器人"的编程模型 —— 运动序列 = 一串 (目标姿态, 时长, 插值方法)。
这是 Reachy Mini emotions library 的最小内核。
"""

import time

from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose
from reachy_mini.utils.interpolation import InterpolationTechnique

# (名字, head参数, 天线, 时长, 插值方法)
EMOTION_SEQ = [
    ("好奇抬头", dict(z=25, pitch=-10, degrees=True, mm=True), [0.5, 0.5], 0.8, InterpolationTechnique.MIN_JERK),
    ("害羞侧倾", dict(z=-10, roll=20, degrees=True, mm=True), [-0.8, -0.8], 0.8, InterpolationTechnique.EASE_IN_OUT),
    ("开心转圈", dict(z=0, yaw=15, degrees=True, mm=True), [0.9, -0.9], 0.6, InterpolationTechnique.CARTOON),
    ("回正", dict(), [0.0, 0.0], 1.0, InterpolationTechnique.MIN_JERK),
]


def main() -> None:
    print("== 表情序列播放 ==")
    with ReachyMini(media_backend="no_media") as mini:
        for name, head_kw, antennas, duration, method in EMOTION_SEQ:
            print(f"  -> {name} (时长 {duration}s, 插值 {method.value})")
            mini.goto_target(
                head=create_head_pose(**head_kw),
                antennas=antennas,
                duration=duration,
                method=method,
            )
            time.sleep(duration + 0.2)
    print("[OK] 实验3完成")


if __name__ == "__main__":
    main()
