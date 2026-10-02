# -*- coding: utf-8 -*-
"""
E1b: 资产流"质检门"——对应 PaperRoute 方法论"拆任务、建测试、隔离实验"。
机制流只消费通过校验门的 GLB；校验不过 = 资产流打回重跑，不污染游戏代码。
校验项: GLB 魔数 / 版本 / 块长度自洽 / JSON 可解析 / POSITION accessor 存在 / 三角索引非空。
"""
import json, struct, os, sys

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

def validate(path):
    data = open(path, "rb").read()
    if len(data) < 20: return False, "file too small"
    magic, version, total = struct.unpack_from("<III", data, 0)
    if magic != 0x46546C67: return False, f"bad magic {magic:#x}"
    if version != 2: return False, f"bad version {version}"
    if total != len(data): return False, f"length mismatch header={total} file={len(data)}"
    off = 12
    clen, ctype = struct.unpack_from("<II", data, off); off += 8
    if ctype != 0x4E4F534A: return False, "first chunk not JSON"
    try:
        gltf = json.loads(data[off:off+clen])
    except Exception as e:
        return False, f"JSON parse fail: {e}"
    off += clen
    blen, btype = struct.unpack_from("<II", data, off); off += 8
    if btype != 0x004E4942: return False, "second chunk not BIN"
    if off + blen > len(data): return False, "BIN chunk overruns file"
    prim = gltf["meshes"][0]["primitives"][0]
    if "POSITION" not in prim["attributes"]: return False, "no POSITION"
    acc = gltf["accessors"][prim["indices"]]
    if acc["count"] % 3 != 0 or acc["count"] == 0: return False, "bad triangle indices"
    if gltf["asset"]["version"] != "2.0": return False, "asset version not 2.0"
    n_tri = acc["count"] // 3
    return True, f"ok: {acc['count']//3} tri, baseColor={gltf['materials'][0]['pbrMetallicRoughness']['baseColorFactor'][:3]}"

def main():
    files = sorted(f for f in os.listdir(ASSETS) if f.endswith(".glb"))
    passed = 0
    for f in files:
        ok, msg = validate(os.path.join(ASSETS, f))
        print(("PASS " if ok else "FAIL ") + f"{f:28s} {msg}")
        passed += ok
    print(f"\n[glb_gate] {passed}/{len(files)} 通过质检门")
    return 0 if passed == len(files) else 1

if __name__ == "__main__":
    sys.exit(main())
