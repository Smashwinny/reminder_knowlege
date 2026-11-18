#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ship-page DIFF GATE 本地复刻（示例数据练习版）
规则来自 ChatSEO 六技能之 ship-page：发布前必须列出旧版有而新版丢失的元素，
全部经人工确认后才允许发布。零依赖，HTML 用正则粗解析（练习用途）。
用法: python diff_gate.py old.html new.html
退出码: 0=无丢失; 7=有丢失(fail-closed，与 content_guard 同款)
"""
import re, sys

def inventory(path):
    html = open(path, encoding='utf-8').read()
    return {
        'tables':    re.findall(r'<table[^>]*id="([^"]+)"', html) or [f'table#{i}' for i in range(len(re.findall(r'<table', html)))],
        'forms':     len(re.findall(r'<form', html)),
        'images':    re.findall(r'<img[^>]*src="([^"]+)"', html),
        'links':     sorted(set(re.findall(r'<a[^>]*href="([^"]+)"', html))),
        'h1_count':  len(re.findall(r'<h1', html)),
    }

def main():
    old, new = inventory(sys.argv[1]), inventory(sys.argv[2])
    lost = []
    for t in old['tables']:
        if t not in new['tables']: lost.append(f'表格 {t}')
    if new['forms'] < old['forms']: lost.append(f'表单 x{old["forms"]-new["forms"]}')
    for src in old['images']:
        if src not in new['images']: lost.append(f'图片 {src}')
    for href in old['links']:
        if href not in new['links']: lost.append(f'链接 {href}')
    if old['h1_count'] and not new['h1_count']: lost.append('H1 标题')
    if lost:
        print('❌ DIFF GATE 拦截：旧版有而新版丢失的元素：')
        for x in lost: print('  -', x)
        print('须人工逐项确认后才可发布（fail-closed exit 7）')
        sys.exit(7)
    print('✅ DIFF GATE 通过：无丢失元素')

if __name__ == '__main__':
    main()
