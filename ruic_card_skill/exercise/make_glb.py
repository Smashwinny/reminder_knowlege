# -*- coding: utf-8 -*-
"""实验3：零依赖手写最小 card.glb —— 只履行 viewer 的几何/材质名契约。
契约(SKILL.md)：材质名 web_front / web_back 必须存在，viewer 会用自己的
shader 材质替换它们，所以几何本身只要是一块 2:3 平面即可。
正面: 7.2 x 10.8 平面朝 +Z (材质 web_front)
背面: 同一平面绕 Y 转 180 度 (材质 web_back)，翻转卡片时可见。
"""
import json, struct, sys
from pathlib import Path

CARD_W, CARD_H = 7.2, 10.8

def plane(w, h):
    hw, hh = w / 2, h / 2
    pos = [-hw, -hh, 0, hw, -hh, 0, hw, hh, 0, -hw, hh, 0]
    uv = [0, 1, 1, 1, 1, 0, 0, 0]  # three.js PlaneGeometry 约定：v=1 在上
    idx = [0, 1, 2, 0, 2, 3]       # 从 +Z 看逆时针 => 正面
    return pos, uv, idx

def build():
    fp, fu, fi = plane(CARD_W, CARD_H)
    bp, bu, bi = plane(CARD_W, CARD_H)
    bin_parts, views, accs = [], [], []

    def add_view(data, fmt, count, type_, comp_size, aligned=4):
        fmts = {'f': ('f', 4), 'H': ('H', 2)}
        code, size = fmts[fmt]
        blob = b''.join(struct.pack('<' + code, v) for v in data)
        pad = (-len(blob)) % aligned
        blob += b'\0' * pad
        off = sum(len(p) for p in bin_parts)
        bin_parts.append(blob)
        views.append({'buffer': 0, 'byteOffset': off, 'byteLength': len(blob) - pad})
        acc = {'bufferView': len(views) - 1, 'componentType':
               {'f': 5126, 'H': 5123}[fmt], 'count': count, 'type': type_}
        if type_ == 'VEC3':
            xs = data[0::3]; ys = data[1::3]; zs = data[2::3]
            acc['min'] = [min(xs), min(ys), min(zs)]
            acc['max'] = [max(xs), max(ys), max(zs)]
        accs.append(acc)

    for pos, uv, idx in [(fp, fu, fi), (bp, bu, bi)]:
        add_view(pos, 'f', 4, 'VEC3', 4)
        add_view(uv, 'f', 4, 'VEC2', 4)
        add_view(idx, 'H', 6, 'SCALAR', 2)

    gltf = {
        'asset': {'version': '2.0', 'generator': 'exercise make_glb.py'},
        'scene': 0,
        'scenes': [{'nodes': [0]}],
        'nodes': [
            {'children': [1, 2]},
            {'mesh': 0},
            {'mesh': 1, 'rotation': [0, 1, 0, 0]},  # 绕Y转180度 = 背面
        ],
        'meshes': [
            {'primitives': [{'attributes': {'POSITION': 0, 'TEXCOORD_0': 1},
                             'indices': 2, 'material': 0}]},
            {'primitives': [{'attributes': {'POSITION': 3, 'TEXCOORD_0': 4},
                             'indices': 5, 'material': 1}]},
        ],
        'materials': [
            {'name': 'web_front', 'pbrMetallicRoughness': {'baseColorFactor': [1, 1, 1, 1]}},
            {'name': 'web_back', 'pbrMetallicRoughness': {'baseColorFactor': [1, 1, 1, 1]}},
        ],
        'accessors': accs,
        'bufferViews': views,
        'buffers': [{'byteLength': sum(len(p) for p in bin_parts)}],
    }
    js = json.dumps(gltf, separators=(',', ':')).encode()
    js += b' ' * ((4 - len(js) % 4) % 4)
    bin_blob = b''.join(bin_parts)
    total = 12 + 8 + len(js) + 8 + len(bin_blob)
    out = struct.pack('<III', 0x46546C67, 2, total)
    out += struct.pack('<II', len(js), 0x4E4F534A) + js
    out += struct.pack('<II', len(bin_blob), 0x004E4942) + bin_blob
    return out

if __name__ == '__main__':
    dst = Path(sys.argv[1]); dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(build())
    print(f'GLB written: {dst.resolve()} ({dst.stat().st_size} bytes)')
