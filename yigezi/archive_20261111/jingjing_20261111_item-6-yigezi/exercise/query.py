#!/usr/bin/env python3
"""Query the yigezi single-page snapshot and verify published counts.

Does not redistribute fonts or the full 1.7MB page. Default snapshot path is
the read-only copy already fetched in this batch.
"""
from __future__ import annotations
import argparse, json, re, sys, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_HTML = Path("/workspace/reminder-batch-2026-11-11/sources/yigezi-index.html")
CLAIMS = {
    "seal": 10249,
    "oracle": 1425,
    "shuowen": 9815,
    "series": 740,
}

def extract_json_object(src: str, needle: str) -> dict:
    i = src.find(needle)
    if i < 0:
        raise SystemExit(f"missing {needle}")
    j = src.find("{", i)
    depth = 0
    for k, ch in enumerate(src[j:]):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                raw = src[j:j+k+1]
                return json.loads(raw)
    raise SystemExit(f"unclosed {needle}")

def extract_template_chars(src: str, name: str) -> str:
    m = re.search(rf"{name}=`([^`]*)`", src)
    if not m:
        raise SystemExit(f"missing template {name}")
    # keep unique CJK / listed characters, preserve original string for includes()
    return m.group(1)

def load(path: Path):
    text = path.read_text("utf-8")
    sw = extract_json_object(text, "const SW=")
    xs = extract_json_object(text, "XS=")
    xz = extract_json_object(text, "const XZ=")
    ts = extract_json_object(text, "TS=")
    seal = extract_template_chars(text, "HAS_SEAL")
    orac = extract_template_chars(text, "HAS_ORAC")
    return {"sw": sw, "xs": xs, "xz": xz, "ts": ts, "seal": seal, "orac": orac, "html_sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "html_bytes": path.stat().st_size}

def lookup(db, raw: str):
    m = re.search(r"[\u4e00-\u9fff]", raw or "")
    if not m:
        return None
    s = m.group(0)
    trads = [ch for ch in (db["ts"].get(s) or "")]
    t = next((x for x in trads if x in db["sw"] or x in db["orac"]), None) or (trads[0] if trads else s)
    sw = db["sw"].get(t) or db["sw"].get(s)
    seal = t if t in db["seal"] else (s if s in db["seal"] else None)
    orac = t if t in db["orac"] else (s if s in db["orac"] else None)
    # phonetic series: key is the 声符
    series_key = None
    series = []
    if t in db["xs"]:
        series_key, series = t, db["xs"][t]
    elif s in db["xs"]:
        series_key, series = s, db["xs"][s]
    else:
        for k, members in db["xs"].items():
            if t in members or s in members or t == k or s == k:
                series_key, series = k, members
                break
    rec = {
        "query": s,
        "traditional": t,
        "seal": seal or "—",
        "oracle": orac or "—",
        "has_seal": bool(seal),
        "has_oracle": bool(orac),
        "shuowen": (sw or {}).get("e") if sw else "—",
        "pinyin": (sw or {}).get("p") if sw else "—",
        "fanqie": (sw or {}).get("f") if sw else "—",
        "radical": (sw or {}).get("r") if sw else "—",
        "volume": (sw or {}).get("v") if sw else "—",
        "mc": (sw or {}).get("mc") if sw else "—",
        "mc_pos": (sw or {}).get("pos") if sw else "—",
        "oc": (sw or {}).get("oc") if sw else "—",
        "ocsrc": (sw or {}).get("ocsrc") if sw else "—",
        "correction": (db["xz"].get(t) or db["xz"].get(s) or {}).get("t") if (t in db["xz"] or s in db["xz"]) else None,
        "series_key": series_key,
        "series_size": len(series) if series_key else 0,
        "series_sample": (series[:8] if series else []),
    }
    return rec

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["query", "verify"], nargs="?", default="query")
    ap.add_argument("--html", type=Path, default=DEFAULT_HTML)
    args = ap.parse_args()
    db = load(args.html)
    counts = {
        "seal": len(db["seal"]),
        "oracle": len(db["orac"]),
        "shuowen": len(db["sw"]),
        "series": len(db["xs"]),
        "corrections": len(db["xz"]),
        "trad_map": len(db["ts"]),
    }
    samples = ["江", "水", "木", "为", "射", "龙", "氵"]  # 氵 is a radical, expect dash-heavy
    looked = [lookup(db, ch) for ch in samples]
    out = {
        "source_html": str(args.html),
        "html_sha256": db["html_sha256"],
        "html_bytes": db["html_bytes"],
        "counts": counts,
        "readme_claims": CLAIMS,
        "count_match": {k: counts[k] == CLAIMS[k] for k in CLAIMS},
        "lookups": looked,
        "dash_policy": "missing glyph or entry rendered as — ; no invented readings",
    }
    dest = ROOT / "results.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print("html", args.html, "sha256", db["html_sha256"], "bytes", db["html_bytes"])
    print("counts", json.dumps(counts, ensure_ascii=False))
    print("match", out["count_match"])
    for rec in looked:
        print(f"LOOKUP {rec['query']}: seal={rec['seal']} oracle={rec['oracle']} py={rec['pinyin']} mc={rec['mc']} oc={rec['oc']} ocsrc={rec['ocsrc']} series={rec['series_key']}:{rec['series_size']} shuowen={(rec['shuowen'][:20]+'…') if rec['shuowen'] and rec['shuowen']!='—' else rec['shuowen']}")
        if rec["correction"]:
            print("  XZ:", rec["correction"][:80])
    if args.cmd == "verify":
        failed = []
        if not all(out["count_match"].values()):
            failed.append("count_match")
        jiang = looked[0]
        if jiang["query"] != "江" or jiang["shuowen"] == "—" or not jiang["has_seal"]:
            failed.append("jiang")
        wei = next(r for r in looked if r["query"]=="为")
        if not wei["correction"]:
            failed.append("wei_correction")
        she = next(r for r in looked if r["query"]=="射")
        if not she["correction"]:
            failed.append("she_correction")
        radical = looked[-1]
        # radical may or may not be in the database; the policy is to show — when missing, never invent
        invented = any(
            r["pinyin"] not in ("—",) and r["shuowen"] == "invented"
            for r in looked
        )
        if invented:
            failed.append("invented")
        print("verify_failed", failed or 0)
        if failed:
            sys.exit(1)
        print("VERIFY PASS")

if __name__ == "__main__":
    main()
