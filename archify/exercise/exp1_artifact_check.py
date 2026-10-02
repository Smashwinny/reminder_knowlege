# -*- coding: utf-8 -*-
"""实验1：静态体检 archify 官方示例产物 HTML —— 验证"自包含"承诺"""
import re, os, json, sys
sys.stdout.reconfigure(encoding="utf-8")

targets = [
    r"F:/reminder/archify/repo/examples/web-app-rendered.html",
    r"F:/reminder/archify/repo/examples/sequence-cache-miss-request.html",
]
for t in targets:
    html = open(t, encoding="utf-8").read()
    size_kb = os.path.getsize(t) // 1024
    ext_scripts = re.findall(r'<script[^>]+src=["\'](?!data:)([^"\']+)["\']', html)
    ext_links  = re.findall(r'<link[^>]+href=["\'](?!data:|#)([^"\']+)["\']', html)
    ext_imgs   = re.findall(r'<img[^>]+src=["\'](?!data:)([^"\']+)["\']', html)
    svg_count  = html.count("<svg")
    print(f"== {os.path.basename(t)} ==")
    print(f"  大小: {size_kb} KB")
    print(f"  外部 <script src> (非data:): {ext_scripts or '无 ✓'}")
    print(f"  外部 <link href> (非data:): {ext_links or '无 ✓'}")
    print(f"  外部 <img src> (非data:): {ext_imgs or '无 ✓'}")
    print(f"  内联 <svg> 数量: {svg_count}")
    feats = {
        "主题切换(dark/light)": "theme" in html.lower(),
        "导出PNG/canvas": "toBlob" in html or "toDataURL" in html,
        "Route Probe(路径探测)": "route" in html.lower(),
        "Node Finder(搜索)": "finder" in html.lower() or "search" in html.lower(),
        "键盘可达(keyboard)": "keydown" in html,
        "URL深链(hashchange)": "hashchange" in html,
        "Reduced motion尊重": "prefers-reduced-motion" in html,
        "provenance(来源戳)": "provenance" in html.lower(),
    }
    for k, v in feats.items():
        print(f"  [{'✓' if v else '✗'}] {k}")
    print()
