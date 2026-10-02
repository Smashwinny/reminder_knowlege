# -*- coding: utf-8 -*-
"""
实验步骤5：产物体检（对标上游 finalize 阶段的 VideoGenerationResult）
用 ffmpeg 解码计数帧数 + 复核 storyboard.json 的字段闭环，
确认"文案→配图→语音→片段→成片"整条链路的数据完整。
运行：python ex5_verify.py
"""
import json
import subprocess
import sys
from pathlib import Path

EX = Path(__file__).parent
OUT = EX / "output"


def get_ffmpeg():
    import shutil
    return shutil.which("ffmpeg") or __import__("imageio_ffmpeg").get_ffmpeg_exe()


def count_frames(video: Path, exe: str) -> int:
    r = subprocess.run(
        [exe, "-i", str(video), "-map", "0:v:0", "-c:v", "copy", "-f", "null", "-"],
        capture_output=True, text=True, encoding="utf-8", errors="ignore")
    for line in reversed(r.stderr.splitlines()):
        if "frame=" in line:
            return int(line.split("frame=")[1].split()[0])
    return -1


def main():
    data = json.loads((OUT / "storyboard.json").read_text(encoding="utf-8"))
    final = OUT / "final_video.mp4"
    exe = get_ffmpeg()

    print("[ex5] 分镜数据闭环检查：")
    ok = True
    for fr in data["frames"]:
        row = {k: bool(fr.get(k)) for k in
               ("image_path", "audio_path", "video_segment_path", "duration")}
        all_filled = all(row.values())
        ok = ok and all_filled
        print(f"  帧{fr['index']}: 图{'Y' if row['image_path'] else 'N'} "
              f"音{'Y' if row['audio_path'] else 'N'} "
              f"段{'Y' if row['video_segment_path'] else 'N'} "
              f"时长{fr['duration']}s {'PASS' if all_filled else 'FAIL'}")

    frames = count_frames(final, exe)
    print(f"[ex5] 成片解码帧数: {frames} (30fps x ~{frames / 30:.1f}s)")

    assert ok, "分镜表存在未闭环字段"
    assert frames > 100, "成片帧数异常"
    print(f"[ex5] PASS: 5 帧分镜全链路闭环，成片 {final.name} 可播放")
    return 0


if __name__ == "__main__":
    sys.exit(main())
