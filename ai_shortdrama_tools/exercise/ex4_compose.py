# -*- coding: utf-8 -*-
"""
实验步骤4：ffmpeg 合成成片（对标 produce_assets 的片段合成 + post_production 的拼接/BGM）
流程复刻上游 services/video.py：
  1) 每帧：静态图 loop + 音频 -> 单帧视频段（-shortest：段长=语音长度）
  2) concat demuxer 无损拼接全部片段
  3) BGM（上游 bgm/default.mp3）amix 混音，音量压到 0.15
运行：python ex4_compose.py
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import ffmpeg

EX = Path(__file__).parent
OUT = EX / "output"
REPO_BGM = EX.parent / "repo" / "bgm" / "default.mp3"


def get_ffmpeg():
    """ffmpeg 可执行文件：优先 PATH，否则用 imageio-ffmpeg 自带的静态二进制"""
    exe = shutil.which("ffmpeg")
    return exe or __import__("imageio_ffmpeg").get_ffmpeg_exe()


def audio_duration(path: Path, exe: str) -> float:
    """用 ffmpeg -i 的 stderr 解析时长（imageio-ffmpeg 不带 ffprobe，这里用等价办法）"""
    r = subprocess.run([exe, "-i", str(path)], capture_output=True, text=True, encoding="utf-8", errors="ignore")
    for line in r.stderr.splitlines():
        if "Duration:" in line:
            h, m, s = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    raise RuntimeError(f"拿不到时长: {path}")


def main():
    exe = get_ffmpeg()
    print(f"[ex4] ffmpeg = {exe}")
    sb_path = OUT / "storyboard.json"
    data = json.loads(sb_path.read_text(encoding="utf-8"))

    # --- 1) 逐帧合成视频段 ---
    seg_paths = []
    for fr in data["frames"]:
        seg = OUT / f"segment_{fr['index']}.mp4"
        pic = ffmpeg.input(fr["image_path"], loop=1, framerate=30)
        aud = ffmpeg.input(fr["audio_path"])
        (
            ffmpeg
            .output(pic.video, aud.audio, str(seg), vcodec="libx264", pix_fmt="yuv420p",
                    acodec="aac", shortest=None, r=30, s="1080x1920")
            .overwrite_output()
            .run(cmd=exe, quiet=True)
        )
        fr["video_segment_path"] = str(seg)
        fr["duration"] = round(audio_duration(seg, exe), 2)
        seg_paths.append(seg)
        print(f"[ex4] 片段{fr['index']} -> {seg.name} ({fr['duration']}s)")
    sb_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    # --- 2) concat demuxer 拼接 ---
    concat_list = OUT / "concat.txt"
    concat_list.write_text(
        "".join(f"file '{p.as_posix()}'\n" for p in seg_paths), encoding="utf-8")
    joined = OUT / "joined.mp4"
    (
        ffmpeg
        .input(str(concat_list), format="concat", safe=0)
        .output(str(joined), vcodec="copy", acodec="copy")
        .overwrite_output()
        .run(cmd=exe, quiet=True)
    )
    print(f"[ex4] 拼接 -> joined.mp4")

    # --- 3) 混入 BGM（音量 0.15，-shortest 跟主音轨对齐）---
    final = OUT / "final_video.mp4"
    bgm = REPO_BGM if REPO_BGM.exists() else None
    if bgm:
        voice = ffmpeg.input(str(joined))
        music = ffmpeg.input(str(bgm)).audio.filter("volume", 0.15)
        mixed = ffmpeg.filter([voice.audio, music], "amix", inputs=2, duration="first")
        (
            ffmpeg
            .output(voice.video, mixed, str(final), vcodec="copy", acodec="aac")
            .overwrite_output()
            .run(cmd=exe, quiet=True)
        )
        print(f"[ex4] BGM 混音（{bgm.name} @0.15）-> final_video.mp4")
    else:
        shutil.copy(joined, final)
        print("[ex4] 未找到上游 BGM，跳过混音")

    # --- 验证 ---
    total = sum(fr["duration"] for fr in data["frames"])
    final_dur = audio_duration(final, exe)
    print(f"[ex4] 预期总时长≈{total:.2f}s，成片实际 {final_dur:.2f}s")
    assert abs(final_dur - total) < 1.5, "成片时长与分段之和不符"
    assert final.stat().st_size > 100_000, "成片太小"
    print(f"[ex4] PASS -> {final} ({final.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
