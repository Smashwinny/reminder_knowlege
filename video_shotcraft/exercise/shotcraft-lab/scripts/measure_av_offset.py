"""Dependency-free FFT cross-correlation for rendered audio offset probes.

Usage: python -I scripts/measure_av_offset.py rendered.wav name=source.wav=fromFrame ...
The source and render must be mono PCM s16le at the same sample rate.
"""
import array
import cmath
import json
import math
from pathlib import Path
import sys
import wave


def read_wav(path: Path):
    with wave.open(str(path), "rb") as wav:
        rate = wav.getframerate()
        channels = wav.getnchannels()
        width = wav.getsampwidth()
        raw = wav.readframes(wav.getnframes())
    if width != 2:
        raise ValueError("expected pcm_s16le")
    values = array.array("h", raw)
    if sys.byteorder != "little":
        values.byteswap()
    mono = [sum(values[i:i + channels]) / channels / 32768.0 for i in range(0, len(values), channels)]
    return rate, mono


def downsample(values, factor):
    return [sum(values[i:i + factor]) / len(values[i:i + factor]) for i in range(0, len(values), factor)]


def fft(values, inverse=False):
    n = len(values)
    if n == 0 or n & (n - 1):
        raise ValueError("FFT size must be a power of two")
    data = list(map(complex, values))
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            data[i], data[j] = data[j], data[i]
    length = 2
    while length <= n:
        angle = (2 if inverse else -2) * math.pi / length
        root = cmath.exp(1j * angle)
        for start in range(0, n, length):
            w = 1 + 0j
            half = length // 2
            for k in range(start, start + half):
                u = data[k]
                v = data[k + half] * w
                data[k] = u + v
                data[k + half] = u - v
                w *= root
        length *= 2
    if inverse:
        data = [v / n for v in data]
    return data


def valid_correlation(segment, source):
    valid = len(segment) - len(source) + 1
    if valid <= 0:
        raise ValueError("segment shorter than source")
    size = 1 << (len(segment) + len(source) - 1).bit_length()
    a = fft(segment + [0.0] * (size - len(segment)))
    b = fft(source + [0.0] * (size - len(source)))
    product = [a[i] * b[i].conjugate() for i in range(size)]
    corr = fft(product, inverse=True)
    return [v.real for v in corr[:valid]]


def self_test():
    corr = valid_correlation([0, 0, 1, 2, 3, 0], [1, 2, 3])
    assert max(range(len(corr)), key=corr.__getitem__) == 2, corr


def measure(render_path: Path, source_path: Path, from_frame: float):
    render_rate, render = read_wav(render_path)
    source_rate, source = read_wav(source_path)
    if render_rate != source_rate:
        raise ValueError("sample rates differ")
    factor = max(1, render_rate // 8000)
    rate = render_rate / factor
    render = downsample(render, factor)
    source = downsample(source, factor)
    expected = from_frame * rate / 30
    margin = round(rate * 0.3)
    start = max(0, round(expected) - margin)
    end = min(len(render), round(expected) + len(source) + margin)
    segment = render[start:end]
    corr = valid_correlation(segment, source)
    lag = max(range(len(corr)), key=corr.__getitem__)
    actual = start + lag
    numerator = corr[lag]
    denominator = math.sqrt(sum(v * v for v in segment[lag:lag + len(source)]) * sum(v * v for v in source))
    coefficient = numerator / denominator if denominator else 0
    offset_samples = actual - expected
    return {
        "source": source_path.name,
        "sequenceFromFrame": from_frame,
        "measuredStartFrame": round(actual * 30 / rate, 4),
        "outputOffsetSamplesAt48k": round(offset_samples * factor, 2),
        "outputOffsetFrames30fps": round(offset_samples * 30 / rate, 4),
        "normalizedCorrelation": round(coefficient, 5),
        "searchWindowSeconds": 0.3,
    }


if __name__ == "__main__":
    self_test()
    if len(sys.argv) < 3:
        raise SystemExit("usage: python -I scripts/measure_av_offset.py rendered.wav name=source.wav=fromFrame ...")
    render_path = Path(sys.argv[1])
    results = []
    for arg in sys.argv[2:]:
        name, source, frame = arg.split("=")
        results.append({"probe": name, **measure(render_path, Path(source), float(frame))})
    print(json.dumps(results, ensure_ascii=False, indent=2))
