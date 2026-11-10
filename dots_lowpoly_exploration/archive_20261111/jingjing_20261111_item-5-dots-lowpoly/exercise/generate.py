#!/usr/bin/env python3
"""Deterministic procedural low-poly theme rotator.

This is NOT OpenAI Dots, NOT Blender, and NOT a quality claim about AI meshes.
It only demonstrates: rotate themes -> emit .obj/.glb -> render a preview ->
leave a human-review checklist. Face counts are counted from the files we write.
"""
from __future__ import annotations
import argparse, json, math, struct, hashlib, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "out"
THEMES = ["tree", "house", "crystal", "robot", "boat", "cactus", "lantern", "mushroom"]
COLORS = {
    "tree": (6, 140, 90),
    "house": (37, 99, 235),
    "crystal": (6, 182, 212),
    "robot": (80, 90, 120),
    "boat": (20, 90, 160),
    "cactus": (40, 160, 70),
    "lantern": (249, 115, 22),
    "mushroom": (200, 70, 60),
}

def box(cx, cy, cz, sx, sy, sz):
    hx, hy, hz = sx/2, sy/2, sz/2
    v = [
        (cx-hx, cy-hy, cz-hz), (cx+hx, cy-hy, cz-hz),
        (cx+hx, cy+hy, cz-hz), (cx-hx, cy+hy, cz-hz),
        (cx-hx, cy-hy, cz+hz), (cx+hx, cy-hy, cz+hz),
        (cx+hx, cy+hy, cz+hz), (cx-hx, cy+hy, cz+hz),
    ]
    f = [
        (0,1,2), (0,2,3), (4,6,5), (4,7,6),
        (0,4,5), (0,5,1), (2,6,7), (2,7,3),
        (0,3,7), (0,7,4), (1,5,6), (1,6,2),
    ]
    return v, f

def pyramid(cx, cy, cz, sx, sy, sz):
    hx, hy, hz = sx/2, sy/2, sz/2
    v = [
        (cx-hx, cy-hy, cz-hz), (cx+hx, cy-hy, cz-hz),
        (cx+hx, cy-hy, cz+hz), (cx-hx, cy-hy, cz+hz),
        (cx, cy+hy, cz),
    ]
    f = [(0,1,4),(1,2,4),(2,3,4),(3,0,4),(0,3,2),(0,2,1)]
    return v, f

def merge(parts):
    verts, faces = [], []
    for v, f in parts:
        off = len(verts)
        verts.extend(v)
        faces.extend([(a+off, b+off, c+off) for a,b,c in f])
    return verts, faces

def theme_mesh(name: str):
    if name == "tree":
        return merge([box(0, 0.35, 0, 0.22, 0.7, 0.22), pyramid(0, 1.15, 0, 1.2, 0.9, 1.2), pyramid(0, 1.55, 0, 0.8, 0.6, 0.8)])
    if name == "house":
        return merge([box(0, 0.45, 0, 1.4, 0.9, 1.1), pyramid(0, 1.15, 0, 1.6, 0.5, 1.3), box(0.45, 0.35, 0.56, 0.25, 0.45, 0.04)])
    if name == "crystal":
        return merge([pyramid(0, 0.7, 0, 0.7, 1.4, 0.7), pyramid(0, -0.05, 0, 0.5, 0.5, 0.5)])
    if name == "robot":
        return merge([
            box(0, 1.15, 0, 0.55, 0.45, 0.5), box(0, 0.6, 0, 0.8, 0.7, 0.5),
            box(-0.65, 0.6, 0, 0.25, 0.7, 0.25), box(0.65, 0.6, 0, 0.25, 0.7, 0.25),
            box(-0.25, 0.05, 0, 0.28, 0.4, 0.28), box(0.25, 0.05, 0, 0.28, 0.4, 0.28),
        ])
    if name == "boat":
        return merge([box(0, 0.15, 0, 1.8, 0.3, 0.7), pyramid(0, 0.05, 0, 2.0, 0.2, 0.8), box(0, 0.7, 0, 0.08, 0.9, 0.08), pyramid(0.35, 0.7, 0, 0.7, 0.7, 0.08)])
    if name == "cactus":
        return merge([box(0, 0.7, 0, 0.35, 1.4, 0.35), box(-0.4, 0.85, 0, 0.5, 0.25, 0.25), box(-0.58, 1.1, 0, 0.22, 0.5, 0.22), box(0.38, 0.55, 0, 0.4, 0.22, 0.22), box(0.52, 0.8, 0, 0.2, 0.45, 0.2)])
    if name == "lantern":
        return merge([box(0, 0.85, 0, 0.7, 0.8, 0.7), box(0, 1.35, 0, 0.85, 0.16, 0.85), box(0, 0.4, 0, 0.85, 0.16, 0.85), box(0, 1.55, 0, 0.12, 0.3, 0.12)])
    if name == "mushroom":
        return merge([box(0, 0.35, 0, 0.3, 0.7, 0.3), pyramid(0, 0.95, 0, 1.3, 0.55, 1.3)])
    raise ValueError(name)

def write_obj(path: Path, verts, faces, name, note):
    lines = [f"# procedural low-poly {name}", f"# {note}", "o " + name]
    for x,y,z in verts:
        lines.append(f"v {x:.6f} {y:.6f} {z:.6f}")
    for a,b,c in faces:
        lines.append(f"f {a+1} {b+1} {c+1}")
    path.write_text("\n".join(lines) + "\n")

def parse_obj(path: Path):
    v, f = [], []
    for line in path.read_text().splitlines():
        if line.startswith("v "):
            v.append(tuple(map(float, line.split()[1:4])))
        elif line.startswith("f "):
            idx = [int(p.split("/")[0]) - 1 for p in line.split()[1:]]
            if len(idx) != 3:
                raise ValueError(f"non-triangle face in {path}")
            f.append(tuple(idx))
    return v, f

def _align4(b: bytes) -> bytes:
    return b + (b" " * ((4 - len(b) % 4) % 4))

def write_glb(path: Path, verts, faces):
    # Minimal glTF 2.0 / GLB: one mesh, POSITION + indices, Y-up already.
    vbytes = b"".join(struct.pack("<fff", x, y, z) for x,y,z in verts)
    ibytes = b"".join(struct.pack("<HHH", a, b, c) for a,b,c in faces)
    if len(verts) >= 65536:
        raise ValueError("need 32-bit indices")
    xmin = [min(p[i] for p in verts) for i in range(3)]
    xmax = [max(p[i] for p in verts) for i in range(3)]
    voff, ioff = 0, len(vbytes)
    blob = vbytes + ibytes
    j = {
        "asset": {"version": "2.0", "generator": "item5-procedural-not-dots"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0}],
        "meshes": [{"primitives": [{"attributes": {"POSITION": 0}, "indices": 1}]}],
        "buffers": [{"byteLength": len(blob)}],
        "bufferViews": [
            {"buffer": 0, "byteOffset": voff, "byteLength": len(vbytes), "target": 34962},
            {"buffer": 0, "byteOffset": ioff, "byteLength": len(ibytes), "target": 34963},
        ],
        "accessors": [
            {"bufferView": 0, "componentType": 5126, "count": len(verts), "type": "VEC3",
             "min": xmin, "max": xmax},
            {"bufferView": 1, "componentType": 5123, "count": len(faces)*3, "type": "SCALAR"},
        ],
    }
    jb = _align4(json.dumps(j, separators=(",", ":")).encode())
    blob4 = blob + (b"\x00" * ((4 - len(blob) % 4) % 4))
    glb = b"glTF" + struct.pack("<II", 2, 12 + 8 + len(jb) + 8 + len(blob4))
    glb += struct.pack("<II", len(jb), 0x4E4F534A) + jb
    glb += struct.pack("<II", len(blob4), 0x004E4942) + blob4
    path.write_bytes(glb)

def parse_glb_counts(path: Path):
    data = path.read_bytes()
    assert data[:4] == b"glTF"
    version, length = struct.unpack_from("<II", data, 4)
    assert version == 2
    jlen, jtype = struct.unpack_from("<II", data, 12)
    assert jtype == 0x4E4F534A
    meta = json.loads(data[20:20+jlen])
    acc = meta["accessors"]
    nvert = acc[0]["count"]
    nidx = acc[1]["count"]
    assert nidx % 3 == 0
    return nvert, nidx // 3

def project(p, w, h):
    x, y, z = p
    # isometric-ish
    sx = (x - z) * 0.866
    sy = y + (x + z) * 0.15
    return int(w/2 + sx * (w*0.28)), int(h*0.72 - sy * (h*0.38))

def render_preview(path: Path, verts, faces, color, title):
    w, h = 480, 360
    img = Image.new("RGB", (w, h), (232, 250, 255))
    dr = ImageDraw.Draw(img)
    dr.rectangle([0, 0, w, 36], fill=(37, 99, 235))
    dr.text((12, 8), title, fill=(255, 255, 255))
    # painter's algorithm by average depth
    tris = []
    for a,b,c in faces:
        pa, pb, pc = verts[a], verts[b], verts[c]
        depth = (pa[0]+pb[0]+pc[0])/3 + (pa[2]+pb[2]+pc[2])/3
        tris.append((depth, pa, pb, pc))
    tris.sort(key=lambda t: t[0])
    fill = color
    line = (18, 40, 71)
    for _, pa, pb, pc in tris:
        pts = [project(pa,w,h), project(pb,w,h), project(pc,w,h)]
        dr.polygon(pts, fill=fill, outline=line)
    img.save(path)
    # non-background pixels
    bg = (232, 250, 255)
    n = sum(1 for px in img.getdata() if px != bg and px != (37, 99, 235))
    return n

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()

def cmd_generate():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    note = "procedural recipe; not a Dots or Blender export"
    for i, theme in enumerate(THEMES):
        verts, faces = theme_mesh(theme)
        obj = OUT / f"{i:02d}-{theme}.obj"
        glb = OUT / f"{i:02d}-{theme}.glb"
        png = OUT / f"{i:02d}-{theme}.png"
        write_obj(obj, verts, faces, theme, note)
        write_glb(glb, verts, faces)
        painted = render_preview(png, verts, faces, COLORS[theme], f"{theme}  {len(faces)} tris")
        ov, of = parse_obj(obj)
        gv, gf = parse_glb_counts(glb)
        rec = {
            "index": i, "theme": theme, "obj": obj.name, "glb": glb.name, "png": png.name,
            "vertices": len(verts), "faces": len(faces),
            "obj_vertices": len(ov), "obj_faces": len(of),
            "glb_vertices": gv, "glb_faces": gf,
            "preview_painted_pixels": painted,
            "lowpoly": len(faces) < 200,
            "sha256_obj": sha256(obj), "sha256_glb": sha256(glb),
        }
        manifest.append(rec)
    (OUT / "manifest.json").write_text(json.dumps({"generator": "procedural-not-dots", "themes": THEMES, "items": manifest}, ensure_ascii=False, indent=2))
    print(f"generated {len(manifest)} models; themes={THEMES}; real dots runs=0; blender=0")
    for r in manifest:
        print(f"  {r['theme']}: faces={r['faces']} obj={r['obj_faces']} glb={r['glb_faces']} paint={r['preview_painted_pixels']}")

def cmd_verify():
    man = json.loads((OUT / "manifest.json").read_text())
    items = man["items"]
    asserts = []
    def check(name, ok, detail):
        asserts.append((name, bool(ok), detail))
        print(("PASS" if ok else "FAIL"), name, detail)
    check("count", len(items)==8, f"n={len(items)}")
    check("unique_themes", [it["theme"] for it in items]==THEMES, [it["theme"] for it in items])
    check("rotation", [it["theme"] for it in items] != [THEMES[0]]*8, "themes change across the batch")
    for it in items:
        check(f"{it['theme']}_files", all((OUT/it[k]).is_file() for k in ("obj","glb","png")), "obj+glb+png")
        check(f"{it['theme']}_counts", it["faces"]==it["obj_faces"]==it["glb_faces"] and it["vertices"]==it["obj_vertices"]==it["glb_vertices"], it)
        check(f"{it['theme']}_lowpoly", it["lowpoly"] and it["faces"] < 200, f"faces={it['faces']}")
        check(f"{it['theme']}_preview", it["preview_painted_pixels"] > 500, it["preview_painted_pixels"])
        # hash lock
        check(f"{it['theme']}_obj_hash", sha256(OUT/it["obj"])==it["sha256_obj"], "obj unchanged")
    failed = [a for a in asserts if not a[1]]
    print(f"assertions={len(asserts)} failed={len(failed)} dots_quality_claimed=0")
    if failed:
        sys.exit(1)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["generate", "verify", "all"], nargs="?", default="all")
    args = p.parse_args()
    if args.cmd in ("generate", "all"):
        cmd_generate()
    if args.cmd in ("verify", "all"):
        cmd_verify()

if __name__ == "__main__":
    main()
