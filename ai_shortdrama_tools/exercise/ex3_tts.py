# -*- coding: utf-8 -*-
"""
实验步骤3：edge-tts 语音合成（对标 produce_assets 阶段的 TTS 环节）
与上游同款库同版本：edge-tts==7.2.7（上游 pyproject.toml 锁定此版本）。
音色 zh-CN-XiaoxiaoNeural 对应上游 tts_voices.py 的本地音色路线（免费、无需 key）。
运行：python ex3_tts.py
"""
import asyncio
import json
import sys
from pathlib import Path

import edge_tts

EX = Path(__file__).parent
OUT = EX / "output"
VOICE = "zh-CN-XiaoxiaoNeural"  # 上游默认女声音色之一


async def synth(text: str, out_path: Path):
    tts = edge_tts.Communicate(text, VOICE, rate="+8%")
    await tts.save(str(out_path))


def main():
    sb_path = OUT / "storyboard.json"
    data = json.loads(sb_path.read_text(encoding="utf-8"))

    async def run_all():
        for fr in data["frames"]:
            p = OUT / f"audio_{fr['index']}.mp3"
            await synth(fr["narration"], p)
            fr["audio_path"] = str(p)

    asyncio.run(run_all())
    sb_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    for fr in data["frames"]:
        size = Path(fr["audio_path"]).stat().st_size
        assert size > 1000, f"audio_{fr['index']}.mp3 太小: {size}B"
        print(f"[ex3] 帧{fr['index']} {VOICE} -> audio_{fr['index']}.mp3 ({size} bytes)")
    print("[ex3] PASS: 5 段真实微软 TTS 语音合成")
    return 0


if __name__ == "__main__":
    sys.exit(main())
