# -*- coding: utf-8 -*-
"""实验1：SVML 解剖器 —— 亲手拆一份“复刻爆款”的源文件
零依赖（仅 Python 标准库）。解析 Hypit 的 SVML 源文件，验证两个宣传口径：
  A. “画面/字幕/B-roll 锚定在词上，而不是秒上”  → 统计内联锚点 @{...} 与停顿 || 的数量
  B. “一套可以继续修改和复用的 Workflow”        → 统计 import 的能力包与生成节点
用法: python exp1_svml_anatomy.py <svml文件路径>
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import Counter

def parse(path):
    src = Path(path).read_text(encoding="utf-8")
    # 去掉注释，避免把注释里的示例也算进去
    code = re.sub(r"<!--.*?-->", "", src, flags=re.S)
    stats = {}
    # --- A. 语义锚点：@{event-id} 词 @{/event-id}，以及 || 停顿标记 ---
    opens = re.findall(r"@\{([a-zA-Z0-9_-]+)\}", code)
    closes = re.findall(r"@\{/([a-zA-Z0-9_-]+)\}", code)
    stats["锚点开启 @{id}"] = len(opens)
    stats["锚点关闭 @{/id}"] = len(closes)
    stats["锚点配对成功"] = len(opens) == len(closes) and Counter(opens) == Counter(closes)
    stats["独立事件数(去重)"] = len(set(opens))
    stats["停顿标记 ||"] = code.count("||")
    stats["读音可选 <X|Y>"] = len(re.findall(r"<[A-Za-z0-9' ]+\s*\|[^>]+>", code))
    # --- B. 结构：import 能力包、生成节点、秒数硬编码 ---
    stats["import 能力包"] = len(re.findall(r"<import\b", code))
    pkgs = re.findall(r'from="(@hypit/[^"]+)"', code)
    stats["  ├─ 来自 @hypit 官方"] = len(pkgs)
    stats["  └─ 本地组件包(source=./)"] = len(re.findall(r'source="\./', code))
    # SVML 的 Script 文本里允许裸 < | > 等非 XML 字符（方言特性），ET 解析不可靠 —— 改用标签正则统计
    tags = Counter(m.group(1).split(":")[-1] for m in re.finditer(r"<([a-zA-Z][\w:.-]*)[\s>/]", code))
    stats["XML 元素总数"] = sum(tags.values())
    stats["  ├─ 生成类节点(Image/Audio/Video)"] = tags.get("Image", 0) + tags.get("Audio", 0) + tags.get("Video", 0)
    stats["  └─ 文本提示 Value"] = tags.get("Value", 0)
    # --- C. “锚词不锚秒”的铁证：找所有以秒为单位的硬编码时间 ---
    sec_attrs = re.findall(r'\b[a-z-]+="([0-9.]+s)"', code)
    stats["硬编码秒数值(属性=Ns)"] = len(sec_attrs)
    # 每个锚点事件的“反应词”示例
    samples = []
    for m in re.finditer(r"@\{([a-zA-Z0-9_-]+)\}\s*([^@]{5,40}?)@\{/", code):
        samples.append((m.group(1), m.group(2).strip()[:24]))
    return stats, sorted(set(opens)), samples[:6]

if __name__ == "__main__":
    path = sys.argv[1]
    stats, events, samples = parse(path)
    print(f"=== SVML 解剖报告: {Path(path).name} ===")
    for k, v in stats.items():
        mark = "PASS" if v is True else ("FAIL" if v is False else "")
        print(f"  {k:<28} {v} {mark}")
    print(f"  事件清单(前12): {', '.join(events[:12])}{' ...' if len(events) > 12 else ''}")
    print("  锚点示例(事件 → 触发词):")
    for ev, words in samples:
        print(f"    @{ev:<18} ← “{words}”")
