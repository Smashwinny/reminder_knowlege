# -*- coding: utf-8 -*-
"""
E1: Headless 资产流水线微缩版 —— PaperRoute 方法论复现
论文出处: paperroute.lol/devlog checkpoint 16 "Replace playable house bodies with
authored Blender asset families"；推文第 2 条 "资产流: 让 AI 写 Python 脚本，
Headless 跑 Blender 批量生成建筑群的 GLB 模型"。

本机无 Blender，用纯 Python 直接写出二进制 glTF(GLB) 复刻同一模式:
  脚本(参数) --批处理--> 一批 GLB 文件 --校验器--> 通过/打回
机制流(游戏手感)完全不需要知道这些文件怎么来的，只要 GLB 在 assets/ 里。
"""
import json, struct, math, os, sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)

# ---- 参数化"户型族"(对应 devlog 的 four-family house board) ----
FAMILIES = {
    "cottage":  dict(w=4.0, d=3.5, wall_h=2.6, roof_rise=1.8, color=(0.92, 0.75, 0.55)),
    "townhouse": dict(w=3.2, d=4.2, wall_h=5.2, roof_rise=1.2, color=(0.80, 0.62, 0.70)),
    "shop":     dict(w=5.0, d=4.0, wall_h=3.0, roof_rise=0.6, color=(0.62, 0.78, 0.85)),
    "villa":    dict(w=6.0, d=5.0, wall_h=3.4, roof_rise=2.4, color=(0.95, 0.90, 0.72)),
}
VARIANTS = 3  # 每族 3 栋(尺寸抖动)，共 12 栋

def box_faces(cx, cy, cz, w, h, d):
    """返回一个长方体的 8 顶点 + 12 三角索引(最小可渲染网格)"""
    x0, x1 = cx-w/2, cx+w/2; y0, y1 = cy, cy+h; z0, z1 = cz-d/2, cz+d/2
    v = [(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1),
         (x0,y1,z0),(x1,y1,z0),(x1,y1,z1),(x0,y1,z1)]
    idx = [0,1,2, 0,2,3, 4,6,5, 4,7,6, 0,4,5, 0,5,1,
           1,5,6, 1,6,2, 2,6,7, 2,7,3, 3,7,4, 3,4,0]
    return v, idx

def prism_roof(cx, cz, w, d, y_base, rise):
    """三棱柱屋顶: 6 顶点 + 8 三角"""
    x0, x1 = cx-w/2, cx+w/2; z0, z1 = cz-d/2, cz+d/2; yt = y_base + rise
    v = [(x0,y_base,z0),(x1,y_base,z0),(x1,y_base,z1),(x0,y_base,z1),
         (cx,yt,z0),(cx,yt,z1)]
    idx = [0,1,4, 1,5,4, 1,2,5, 2,3,5, 3,0,4, 0,4,5, 2,1,0, 0,3,2]
    return v, idx

def build_house(family, seed):
    import random
    rng = random.Random(seed)
    p = dict(FAMILIES[family])
    p["w"] *= rng.uniform(0.9, 1.1); p["d"] *= rng.uniform(0.9, 1.1)
    positions, indices = [], []
    vw, vi = box_faces(0, 0, 0, p["w"], p["wall_h"], p["d"])
    rv, ri = prism_roof(0, 0, p["w"]*1.05, p["d"]*1.05, p["wall_h"], p["roof_rise"])
    for v in vw + rv: positions.extend(v)
    off = len(vw)
    indices = vi + [i + off for i in ri]
    # glTF 2.0 最小 JSON: 一个 mesh 一个 primitive，材质给基色
    material = {"pbrMetallicRoughness": {"baseColorFactor": [*p["color"], 1.0],
                                         "metallicFactor": 0.0, "roughnessFactor": 0.9}}
    gltf = {
        "asset": {"version": "2.0", "generator": "paperroute-exercise/house_factory"},
        "scene": 0, "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": f"{family}_{seed:02d}"}],
        "meshes": [{"primitives": [{"attributes": {"POSITION": 0}, "indices": 1,
                                     "material": 0, "mode": 4}]}],
        "materials": [material],
        "buffers": [{"byteLength": 0}],  # 占位，下面补
        "bufferViews": [], "accessors": [],
    }
    pos_bin = struct.pack(f"<{len(positions)}f", *positions)
    idx_bin = struct.pack(f"<{len(indices)}I", *indices)
    bin_data = pos_bin + idx_bin
    gltf["bufferViews"] = [
        {"buffer": 0, "byteOffset": 0, "byteLength": len(pos_bin), "target": 34962},
        {"buffer": 0, "byteOffset": len(pos_bin), "byteLength": len(idx_bin), "target": 34962},
    ]
    gltf["accessors"] = [
        {"bufferView": 0, "componentType": 5126, "count": len(positions)//3,
         "type": "VEC3", "min": [min(positions[0::3]), min(positions[1::3]), min(positions[2::3])],
         "max": [max(positions[0::3]), max(positions[1::3]), max(positions[2::3])]},
        {"bufferView": 1, "componentType": 5125, "count": len(indices), "type": "SCALAR"},
    ]
    gltf["buffers"][0]["byteLength"] = len(bin_data)
    return gltf, bin_data

def pack_glb(gltf, bin_data):
    js = json.dumps(gltf, separators=(",", ":")).encode()
    pad = (4 - len(js) % 4) % 4; js += b" " * pad
    bin_pad = (4 - len(bin_data) % 4) % 4; bin_data += b"\x00" * bin_pad
    total = 12 + 8 + len(js) + 8 + len(bin_data)
    return (struct.pack("<III", 0x46546C67, 2, total)           # magic glTF, ver2
            + struct.pack("<II", len(js), 0x4E4F534A)            # JSON chunk
            + js
            + struct.pack("<II", len(bin_data), 0x004E4942)      # BIN chunk
            + bin_data)

def main():
    made = []
    for fam in FAMILIES:
        for k in range(1, VARIANTS + 1):
            seed = list(FAMILIES).index(fam) * 10 + k
            gltf, bin_data = build_house(fam, seed)
            path = os.path.join(OUT, f"house_{fam}_{k}.glb")
            with open(path, "wb") as f:
                f.write(pack_glb(gltf, bin_data))
            made.append((path, len(gltf["meshes"][0]["primitives"][0] and bin_data)))
    print(f"[house_factory] 批量生成 {len(made)} 栋房屋 GLB -> {OUT}")
    for p, _ in made: print("   ", os.path.basename(p), os.path.getsize(p), "bytes")
    return 0

if __name__ == "__main__":
    sys.exit(main())
