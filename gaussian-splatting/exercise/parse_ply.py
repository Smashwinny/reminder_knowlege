# -*- coding: utf-8 -*-
"""
实验 1b：不依赖任何第三方库，手写解析 3DGS 的二进制 PLY
目的：验证"一个高斯 = 62 个 float32 = 248 字节"的数据结构理解是否正确
运行：python parse_ply.py synthetic_scene.ply
"""
import struct
import sys
import math

def sigmoid(x): return 1 / (1 + math.exp(-x))

def parse_ply(path):
    with open(path, "rb") as fp:
        # --- 手工读 header，直到 end_header ---
        header, line = [], b""
        while line.strip() != b"end_header":
            line = fp.readline()
            header.append(line.decode("ascii").strip())
        n_vertex = int([l for l in header if l.startswith("element vertex")][0].split()[-1])
        props = [l.split()[-1] for l in header if l.startswith("property float")]
        # --- 一次性读入全部点 ---
        data = fp.read(n_vertex * len(props) * 4)
    return n_vertex, props, data

n, props, data = parse_ply(sys.argv[1])
vals = struct.unpack(f"<{n * len(props)}f", data)
print(f"[header] vertex 数 = {n}, 每点 {len(props)} 个 float32 属性 = {len(props)*4} 字节")
print(f"[payload] {len(data)} 字节 = {n} x {len(props)*4} ？ {len(data) == n*len(props)*4}")
assert len(props) == 62, "3DGS 标准输出应为 62 个属性"
assert len(data) == n * 62 * 4, "字节数与 header 声明不符"

idx = {name: i for i, name in enumerate(props)}
C0 = 0.28209479177387814

def row(vi):
    return vals[vi * 62: (vi + 1) * 62]

# --- 还原前 3 个高斯的"真实物理量"（演示存储格式 -> 可读参数）---
for vi in range(3):
    r = row(vi)
    pos = (r[idx['x']], r[idx['y']], r[idx['z']])
    color = tuple(round(0.5 + C0 * r[idx[f'f_dc_{c}']], 3) for c in range(3))
    scale = tuple(round(math.exp(r[idx[f'scale_{s}']]), 4) for s in range(3))
    opac = round(sigmoid(r[idx['opacity']]), 3)
    quat = tuple(round(r[idx[f'rot_{q}']], 3) for q in range(4))
    print(f"高斯#{vi}: 位置={pos} 颜色RGB={color} 三轴尺度={scale} 不透明度={opac} 四元数={quat}")

# --- 全局统计 ---
xs = vals[idx['x']::62]; ys = vals[idx['y']::62]; zs = vals[idx['z']::62]
print(f"[统计] 包围盒 x[{min(xs):.2f},{max(xs):.2f}] y[{min(ys):.2f},{max(ys):.2f}] z[{min(zs):.2f},{max(zs):.2f}]")
print("OK: 解析通过 —— 一个 3DGS 高斯 = 62 个 float32（62属性 x 4字节 = 248 字节/个）")
