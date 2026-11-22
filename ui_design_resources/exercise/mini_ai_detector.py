#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""迷你 AI 味检测器（概念复刻演示）
灵感来自 impeccable 的 62 条确定性规则（源码 crates/core/src/checks/rules.rs 静态阅读），
本实现为独立原创练习，非 impeccable 代码。
规则：①Inter 字体 ②紫蓝渐变 ③灰字低对比度（WCAG 公式） ④嵌套卡片 ⑤圆角图标砖
"""
import re, sys

html = open(sys.argv[1] if len(sys.argv) > 1 else 'ai-tells-sample.html', encoding='utf-8').read()
findings = []

if re.search(r'font-family:\s*Inter', html):
    findings.append("Inter 万能字体（AI 模板第一征兆）")
if re.search(r'linear-gradient\([^)]*#?6[67][0-9a-f]', html, re.I) or ('#667eea' in html):
    findings.append("紫蓝紫渐变（ai-color-palette 经典形态）")
if '#999' in html:
    findings.append("灰色辅助文字 #999（AI 味浅灰）")
if html.count('class="card') >= 2 or re.search(r'card[^{]*\{[^}]*\}[^]*card2', html):
    findings.append("卡片套卡片（card nested in card）")
if re.search(r'border-radius:\s*12px;\s*background:\s*linear-gradient', html):
    findings.append("圆角图标砖 + 渐变底（rounded-square icon tile）")

# WCAG 对比度计算
def lum(rgb):
    def f(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def contrast(c1, c2):
    l1, l2 = sorted([lum(c1), lum(c2)], reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)

m = re.search(r'\.desc\s*\{[^}]*color:(#\w{3,6})', html)
if m:
    hexc = m.group(1).lstrip('#')
    rgb = tuple(int(hexc[i:i+2], 16) for i in (0, 2, 4)) if len(hexc) == 6 else tuple(int(c*2, 16) for c in hexc)
    ratio = contrast(rgb, (255, 255, 255))
    if ratio < 4.5:
        findings.append(f"低对比度正文 {m.group(1)}（{ratio:.2f}:1 < 4.5:1 WCAG AA）")

print(f"检测完成：{len(findings)} 条 AI 味命中" if findings else "检测完成：0 条命中")
for f in findings: print("  -", f)
sys.exit(1 if findings else 0)
