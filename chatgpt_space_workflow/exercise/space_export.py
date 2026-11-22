#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""自定义 HTML 模拟块→静态 Markdown 的单向导出实验。

这不是 ChatGPT Space 的真实页面格式或导出器，不证明 Space 的实际导出行为；
只验证我们自己选择的静态降级标记。没有“往返转换”。
"""
import argparse
import html
import re
from pathlib import Path

PATTERN = re.compile(r"<(h1|p|viz|ref|file)[^>]*>(.*?)</\1>", re.S)


def export_document(document):
    blocks = []
    for match in PATTERN.finditer(document):
        kind = match.group(1)
        body = html.unescape(re.sub(r"<[^>]+>", "", match.group(2))).strip()
        if kind == "h1":
            blocks.append(f"# {body}\n")
        elif kind == "p":
            blocks.append(f"{body}\n")
        elif kind == "viz":
            blocks.append(f"```viz（本地模拟：静态导出仅保留占位）\n{body}\n```\n")
        elif kind == "ref":
            blocks.append(f"> 引用行（本地模拟：不带实时聊天上下文）: {body}\n")
        elif kind == "file":
            blocks.append(f"附件引用（本地模拟：未复制或修改原文件）: {body}\n")
    return "\n".join(blocks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path(__file__).with_name("space-demo.html"))
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("space-demo-export-v2.md"))
    args = parser.parse_args()
    document = args.input.read_text(encoding="utf-8")
    exported = export_document(document)
    args.output.write_text(exported, encoding="utf-8")
    assert "本地模拟：静态导出仅保留占位" in exported
    assert "不带实时聊天上下文" in exported
    assert "未复制或修改原文件" in exported
    print(f"导出完成：{args.output}")
    print("PASS：viz/ref/file 三种自定义块都有显式降级标记")
    print("边界：这是单向本地模拟，不代表 Space 的真实导出能力")


if __name__ == "__main__":
    main()
