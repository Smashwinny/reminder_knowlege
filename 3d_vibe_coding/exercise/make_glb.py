# -*- coding: utf-8 -*-
"""实验1第1步：零依赖手写两个 GLB（照 paperroute 实验先例）。

mesh A 光滑球面（连续曲面 -> 减面应该砍得动）
mesh B 格构塔（细长钢梁拼的埃菲尔式结构 -> 减面应该砍不动）
材质统一 metalness=1（供实验2复现"PBR 白底死黑"坑）。

用书里 §04 的口径：面数 = indices.count / 3，直接数索引数组。
"""
import json, struct, math, sys, io

def build_glb(positions, indices, name):
    positions = [float(x) for p in positions for x in p]
    minb = [min(positions[i::3]) for i in range(3)]
    maxb = [max(positions[i::3]) for i in range(3)]
    # pad bin to 4-byte alignment
    pos_bytes = struct.pack('<%df' % len(positions), *positions)
    if len(pos_bytes) % 4:
        pos_bytes += b'\x00' * (4 - len(pos_bytes) % 4)
    idx_bytes = struct.pack('<%dI' % len(indices), *indices)
    if len(idx_bytes) % 4:
        idx_bytes += b'\x00' * (4 - len(idx_bytes) % 4)
    bin_data = pos_bytes + idx_bytes
    gltf = {
        "asset": {"version": "2.0", "generator": "reminder-exercise make_glb.py"},
        "scene": 0, "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": name}],
        "meshes": [{"primitives": [{"attributes": {"POSITION": 1}, "indices": 0,
                     "material": 0, "mode": 4}], "name": name}],
        "materials": [{
            "name": "chrome",
            "pbrMetallicRoughness": {
                "baseColorFactor": [0.85, 0.88, 0.92, 1.0],
                "metallicFactor": 1.0, "roughnessFactor": 0.25
            }
        }],
        "buffers": [{"byteLength": len(bin_data)}],
        "bufferViews": [
            {"buffer": 0, "byteOffset": 0, "byteLength": len(pos_bytes), "target": 34962},
            {"buffer": 0, "byteOffset": len(pos_bytes), "byteLength": len(idx_bytes), "target": 34963},
        ],
        "accessors": [
            {"bufferView": 1, "componentType": 5125, "count": len(indices),
             "type": "SCALAR", "max": [int(max(indices))], "min": [0]},
            {"bufferView": 0, "componentType": 5126, "count": len(positions)//3,
             "type": "VEC3", "min": minb, "max": maxb},
        ],
    }
    js = json.dumps(gltf, separators=(',', ':')).encode('utf-8')
    if len(js) % 4:
        js += b' ' * (4 - len(js) % 4)
    total = 12 + 8 + len(js) + 8 + len(bin_data)
    out = struct.pack('<III', 0x46546C67, 2, total)
    out += struct.pack('<II', len(js), 0x4E4F534A) + js
    out += struct.pack('<II', len(bin_data), 0x004E4942) + bin_data
    return out

def uv_sphere(seg_u=24, seg_v=16, r=1.0):
    """连续曲面代表：一个普通 UV 球。"""
    pos, idx = [], []
    for v in range(seg_v + 1):
        phi = math.pi * v / seg_v
        for u in range(seg_u + 1):
            th = 2 * math.pi * u / seg_u
            pos.append((r*math.sin(phi)*math.cos(th), r*math.cos(phi), r*math.sin(phi)*math.sin(th)))
    for v in range(seg_v):
        for u in range(seg_u):
            a = v*(seg_u+1)+u; b = a+1; c = a+seg_u+1; d = c+1
            if v != 0: idx += [a, c, b]
            if v != seg_v-1: idx += [b, c, d]
    return pos, idx

def beam(p0, p1, w):
    """一根长方体钢梁：8 顶点 12 三角。细长结构 = 顶点少、合并即塌。"""
    import itertools
    ax, ay, az = p0; bx, by, bz = p1
    dx, dy, dz = bx-ax, by-ay, bz-az
    L = math.sqrt(dx*dx+dy*dy+dz*dz)
    if L == 0: return [], []
    dx, dy, dz = dx/L, dy/L, dz/L
    # 任取一个不平行的轴做叉积
    up = (0, 0, 1) if abs(dz) < 0.9 else (1, 0, 0)
    rx = dy*up[2]-dz*up[1]; ry = dz*up[0]-dx*up[2]; rz = dx*up[1]-dy*up[0]
    rl = math.sqrt(rx*rx+ry*ry+rz*rz); rx, ry, rz = rx/rl*w, ry/rl*w, rz/rl*w
    ux = dy*rz-dz*ry; uy = dz*rx-dx*rz; uz = dx*ry-dy*rx
    corners = []
    for (s, t) in itertools.product((-w, w), (-w, w)):
        for e in (0, 1):
            p = (p0, p1)[e]
            corners.append((p[0]+s*rx+t*ux, p[1]+s*ry+t*uy, p[2]+s*rz+t*uz))
    quads = [(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]
    pos, idx = corners, []
    base = 0
    for q in quads:
        a, b, c, d = q
        idx += [base+a, base+b, base+c, base+a, base+c, base+d]
    return pos, idx

def lattice_tower(h=3.0, base=1.0, levels=8, w=0.02):
    """格构塔：4 根主柱逐层收窄 + 每层水平环梁 + 两个立面 X 撑。"""
    pos, idx = [], []
    def add(p, i):
        base = len(pos); pos.extend(p); idx.extend(base+x for x in i); return base
    for lv in range(levels):
        z0 = h*lv/levels; z1 = h*(lv+1)/levels
        s0 = base*(1 - 0.7*lv/levels)/2; s1 = base*(1 - 0.7*(lv+1)/levels)/2
        corners0 = [(-s0,-s0,z0),(s0,-s0,z0),(s0,s0,z0),(-s0,s0,z0)]
        corners1 = [(-s1,-s1,z1),(s1,-s1,z1),(s1,s1,z1),(-s1,s1,z1)]
        for k in range(4):  # 主柱
            p, i = beam(corners0[k], corners1[k], w); add(p, i)
        for k in range(4):  # 水平环梁
            p, i = beam(corners1[k], corners1[(k+1) % 4], w); add(p, i)
        # X 撑（两个对面立面）
        for (k, m) in ((0, 1), (2, 3)):
            p, i = beam(corners0[k], corners1[m], w*0.8); add(p, i)
            p, i = beam(corners0[m], corners1[k], w*0.8); add(p, i)
    return pos, idx

def count_faces(path):
    """书里 §04 的口径：面数 = indices.count/3。独立第二通道对账。"""
    d = open(path, 'rb').read()
    off, js, bin_ = 12, None, None
    while off < len(d):
        clen, ctype = struct.unpack('<II', d[off:off+8])
        chunk = d[off+8:off+8+clen]
        if ctype == 0x4E4F534A: js = json.loads(chunk)
        elif ctype == 0x004E4942: bin_ = chunk
        off += 8 + clen
    tri = 0
    for m in js['meshes']:
        for p in m['primitives']:
            acc = js['accessors'][p['indices']]
            tri += acc['count'] // 3
    return tri, js['accessors'][1]['count']  # (三角面, 顶点)

if __name__ == '__main__':
    outdir = sys.argv[1] if len(sys.argv) > 1 else '.'
    for name, fn in [('sphere_smooth', uv_sphere), ('tower_lattice', lattice_tower)]:
        pos, idx = fn()
        data = build_glb(pos, idx, name)
        path = outdir + '/' + name + '.glb'
        open(path, 'wb').write(data)
        tri, nv = count_faces(path)
        print('%s.glb  bytes=%d  tris=%d  verts=%d  (indices.count/3=%d)'
              % (path, len(data), tri, nv, len(idx)//3))
