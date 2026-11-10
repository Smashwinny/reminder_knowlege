"""Official dial-indicator browser check + TCP teaching figure check."""
from __future__ import annotations
import hashlib, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "vendor"))
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
import tcp_model

P = pathlib.Path(__file__).resolve().parent
CHROME = "/usr/bin/google-chrome"
EXPECTED = {
    0: tcp_model.snapshot(0),
    1: tcp_model.snapshot(1),
    2: tcp_model.snapshot(2),
    3: tcp_model.snapshot(3),
}


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_dial():
    html = P / "upstream/examples/dial-indicator/dial-indicator-light.html"
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, headless=True)
        pg = b.new_page(viewport={"width": 1000, "height": 800}, reduced_motion="reduce")
        network, errors = [], []
        pg.on("pageerror", lambda err: errors.append(str(err)))
        pg.route("http://**/*", lambda r: (network.append(r.request.url), r.abort()))
        pg.route("https://**/*", lambda r: (network.append(r.request.url), r.abort()))
        pg.goto(html.as_uri())
        stage = pg.locator(".iso-stage")
        stage.focus()
        rows = []
        for key, want in [("Home", 18), ("ArrowLeft", 14), ("End", 10)]:
            stage.press(key)
            pg.wait_for_function(
                '(v)=>document.querySelector(".iso-stage").getAttribute("aria-valuenow")===String(v)',
                arg=want,
                timeout=10000,
            )
            pg.wait_for_timeout(700)
            row = {
                "key": key,
                "want": want,
                "aria": stage.get_attribute("aria-valuenow"),
                "readout": pg.locator("[data-readout]").inner_text(),
                "needle": pg.locator('[data-part="needle"]').get_attribute("d"),
            }
            rows.append(row)
            pg.screenshot(path=str(P / f"pose-{want}.png"))
        out = {"rows": rows, "errors": errors, "network_attempts": network, "paths": pg.locator("svg path").count()}
        (P / "browser-results.json").write_text(json.dumps(out, indent=2))
        print(json.dumps(out, indent=2))
        b.close()
    return out


def verify_dial():
    r = json.loads((P / "browser-results.json").read_text())
    assert not r["errors"], r["errors"]
    assert not r["network_attempts"], r["network_attempts"]
    assert r["paths"] > 30
    assert [int(x["aria"]) for x in r["rows"]] == [18, 14, 10]
    assert len(set(x["needle"] for x in r["rows"])) == 3
    assert ImageChops.difference(
        Image.open(P / "pose-18.png").convert("RGB"),
        Image.open(P / "pose-10.png").convert("RGB"),
    ).getbbox()
    print("PASS dial 6 checks: no JS errors, no HTTP attempts, path count, 3 readouts, 3 needle paths, different rendered poses; not a mechanical accuracy or pedagogy audit")


def run_tcp():
    html = P / "tcp-handshake.html"
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, headless=True)
        pg = b.new_page(viewport={"width": 1100, "height": 820}, reduced_motion="reduce")
        network, errors = [], []
        pg.on("pageerror", lambda err: errors.append(str(err)))
        pg.route("http://**/*", lambda r: (network.append(r.request.url), r.abort()))
        pg.route("https://**/*", lambda r: (network.append(r.request.url), r.abort()))
        pg.goto(html.as_uri())
        stage = pg.locator("#stage")
        stage.focus()
        rows = []
        # Reset then step 0,1,2,3
        stage.press("Home")
        pg.wait_for_function('()=>document.querySelector("#stage").dataset.step==="0"', timeout=8000)
        for key, want in [("Home", 0), ("ArrowRight", 1), ("ArrowRight", 2), ("End", 3)]:
            if key != "Home" or want == 0:
                if not (key == "Home" and want == 0):
                    stage.press(key)
            if key == "Home" and want == 0:
                pass
            pg.wait_for_function(
                '(v)=>document.querySelector("#stage").dataset.step===String(v)',
                arg=want,
                timeout=8000,
            )
            pg.wait_for_timeout(200)
            ds = pg.locator("#stage")
            row = {
                "key": key,
                "want": want,
                "step": ds.get_attribute("data-step"),
                "client": ds.get_attribute("data-client"),
                "server": ds.get_attribute("data-server"),
                "segment": ds.get_attribute("data-segment"),
                "readout": ds.get_attribute("data-readout"),
            }
            rows.append(row)
            pg.screenshot(path=str(P / f"tcp-step-{want}.png"), full_page=True)
        out = {
            "rows": rows,
            "errors": errors,
            "network_attempts": network,
            "title": pg.title(),
        }
        (P / "tcp-results.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
        print(json.dumps(out, indent=2, ensure_ascii=False))
        b.close()
    return out


def verify_tcp():
    r = json.loads((P / "tcp-results.json").read_text())
    assert not r["errors"], r["errors"]
    assert not r["network_attempts"], r["network_attempts"]
    assert r["title"] == "邮筒索道 · TCP 三次握手教学模型"
    for row, step in zip(r["rows"], range(4)):
        exp = tcp_model.snapshot(step)
        assert int(row["step"]) == step
        assert row["client"] == exp["client"], (row, exp)
        assert row["server"] == exp["server"], (row, exp)
        assert row["segment"] == tcp_model.format_segment(exp["segment"]), (row["segment"], exp)
        assert row["readout"] == tcp_model.format_readout(exp)
        print(f"PASS tcp-step-{step} {row['readout']}")
    # Asymmetric state at step 2 is the teaching point
    assert r["rows"][2]["client"] == "ESTABLISHED" and r["rows"][2]["server"] == "SYN-RECEIVED"
    img0 = Image.open(P / "tcp-step-0.png").convert("RGB")
    img3 = Image.open(P / "tcp-step-3.png").convert("RGB")
    assert ImageChops.difference(img0, img3).getbbox()
    print("PASS tcp checks: no JS errors, no HTTP, 4 RFC 793 Fig 6 states, asymmetric step 2, different screenshots")


def hashes():
    files = [
        P / "upstream/examples/dial-indicator/build.mjs",
        P / "upstream/kit/iso-kit.mjs",
        P / "upstream/examples/dial-indicator/dial-indicator-light.html",
        P / "tcp_model.py",
        P / "tcp-handshake.html",
    ]
    for f in files:
        print(sha(f), str(f.relative_to(P)))


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("dial", "all"):
        run_dial()
    if mode in ("verify-dial", "all"):
        verify_dial()
    if mode == "model":
        raise SystemExit(tcp_model.test())
    if mode in ("tcp", "all"):
        run_tcp()
    if mode in ("verify-tcp", "all"):
        verify_tcp()
    if mode in ("hash", "all"):
        hashes()
