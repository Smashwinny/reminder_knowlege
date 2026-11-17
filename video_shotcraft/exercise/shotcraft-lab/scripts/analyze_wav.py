"""Measure actual PCM WAV files: 10 ms RMS peak is not LUFS or true peak."""
import array
import json
import math
from pathlib import Path
import sys
import wave


def db(value: float) -> float:
    return 20 * math.log10(max(value, 1e-12))


def measure(path: Path) -> dict:
    with wave.open(str(path), "rb") as wav:
        rate = wav.getframerate()
        channels = wav.getnchannels()
        width = wav.getsampwidth()
        frames = wav.getnframes()
        raw = wav.readframes(frames)
    if width != 2:
        raise ValueError(f"{path}: expected pcm_s16le, got {width * 8}-bit")
    samples = array.array("h", raw)
    if sys.byteorder != "little":
        samples.byteswap()
    mono = []
    for i in range(0, len(samples), channels):
        mono.append(sum(samples[i:i + channels]) / channels / 32768.0)
    window = max(1, round(rate * 0.01))
    rms_windows = []
    for start in range(0, len(mono), window):
        part = mono[start:start + window]
        rms_windows.append(math.sqrt(sum(v * v for v in part) / len(part)))
    peak_index = max(range(len(rms_windows)), key=rms_windows.__getitem__)
    peak_seconds = (peak_index * window + window / 2) / rate
    overall = math.sqrt(sum(v * v for v in mono) / len(mono))
    return {
        "file": path.name,
        "sampleRate": rate,
        "channels": channels,
        "durationSeconds": round(len(mono) / rate, 6),
        "samplePeakDb": round(db(max(abs(v) for v in mono)), 3),
        "overallRmsDb": round(db(overall), 3),
        "peak10msRmsDb": round(db(rms_windows[peak_index]), 3),
        "peakLagSeconds": round(peak_seconds, 6),
        "peakLagFrames30fps": round(peak_seconds * 30, 3),
        "note": "10 ms RMS/sample peak are not LUFS or true peak; semantic landing still needs listening."
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: python -I scripts/analyze_wav.py file.wav [file.wav ...]")
    print(json.dumps([measure(Path(arg)) for arg in sys.argv[1:]], ensure_ascii=False, indent=2))
