# -*- coding: utf-8 -*-
"""
实验2：分句 TTS 配音 + 精确时间轴（对标文章"调用配音与合成渲染"工序）
做法：口播稿逐句各生成一段 edge-tts 音频，逐段实测时长，
     累加成 timeline.json —— 字幕/画面的出入点全部由真实音频时长驱动，
     而不是拍脑袋定秒数（与知识库 [[词锚定语义时间]] 呼应：锚内容不锚秒）。
edge-tts 免费零 key；时长用 imageio-ffmpeg 自带二进制解析（PATH 无 ffmpeg）。
"""
import asyncio, json, subprocess
from pathlib import Path
import edge_tts
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)

# 口播稿：物业费核查（事实+法条，已过 ex1 脱水测试的写法）
SENTENCES = [
    "物业费到底花在了哪里？我们先看合同里约定的收费构成。",
    "第一部分是人员费用，保安、保洁和绿化，通常占物业费的一半以上。",
    "第二部分是公共能耗，电梯和水泵的电费，按面积分摊到每一户。",
    "核查的办法只有一种：要求物业公示年度收支台账。",
    "依据是民法典第九百四十三条，业主有权查阅公开的收费项目。",
]

VOICE = "zh-CN-YunxiNeural"

def audio_duration(path: Path) -> float:
    r = subprocess.run([FF, "-i", str(path)], capture_output=True, text=True,
                       encoding="utf-8", errors="ignore")
    for line in r.stderr.splitlines():
        if "Duration:" in line:
            h, m, s = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    raise RuntimeError(f"拿不到时长: {path}")

async def synth(text: str, path: Path):
    tts = edge_tts.Communicate(text, VOICE)
    await tts.save(str(path))

async def main():
    seg_files = []
    for i, sent in enumerate(SENTENCES):
        f = OUT / f"seg_{i}.mp3"
        await synth(sent, f)
        seg_files.append(f)

    # 拼接成整条旁白
    list_file = OUT / "concat.txt"
    list_file.write_text("".join(f"file '{f.as_posix()}'\n" for f in seg_files), encoding="utf-8")
    narration = OUT / "narration.mp3"
    subprocess.run([FF, "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
                    "-c", "copy", str(narration)], check=True, capture_output=True)

    # 逐段时长 -> 时间轴
    timeline, t = [], 0.0
    for i, (sent, f) in enumerate(zip(SENTENCES, seg_files)):
        d = round(audio_duration(f), 3)
        timeline.append({"index": i, "text": sent, "start": round(t, 3),
                         "end": round(t + d, 3), "dur": d})
        t += d
    total = audio_duration(narration)
    data = {"voice": VOICE, "sentences": timeline, "total": round(total, 3)}
    (OUT / "timeline.json").write_text(json.dumps(data, ensure_ascii=False, indent=2),
                                       encoding="utf-8")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    # 自检：分段时长和与整条时长误差 < 0.5s；每段时长 > 1s
    assert abs(total - t) < 0.5, f"拼接前后时长不一致 {total} vs {t}"
    assert all(s["dur"] > 1 for s in timeline)
    print(f"\n断言通过：{len(SENTENCES)} 段共 {t:.2f}s，整条实测 {total:.2f}s。")

if __name__ == "__main__":
    asyncio.run(main())
