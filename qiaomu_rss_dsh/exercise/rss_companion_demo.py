#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""RSS 伴读范围实验：默认解析合成 RSS 夹具，不联网。

背景超过上限时明确标为“背景摘录”与 truncated=True，不能冒充整篇；
选段是请求范围，引用约束只是提示纪律，仍需实际回答核验。
"""
import argparse
import html
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


def clean_markup(value):
    text = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def parse_feed(data):
    root = ET.fromstring(data)
    channel = root.find("channel")
    if channel is None:
        raise ValueError("夹具必须是 RSS 2.0 channel 格式")
    items = [{"title": item.findtext("title") or "无标题",
              "description": item.findtext("description") or ""}
             for item in channel.findall("item")]
    return {"title": channel.findtext("title") or "无标题源", "items": items}


def build_scope(content, background_limit=1500):
    if background_limit <= 0:
        raise ValueError("background_limit 必须大于 0")
    background = content[:background_limit]
    paragraphs = [part.strip() for part in re.split(r"(?<=[。.!?])\s", content) if len(part.strip()) > 40]
    selected = paragraphs[0] if paragraphs else content[:300]
    return {"background": background, "background_limit": background_limit,
            "total_chars": len(content), "truncated": len(content) > background_limit,
            "selected": selected, "selected_chars": len(selected)}


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "rss-scope-learn/2.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--feed-url", help="可选真实 RSS URL；不提供则不联网")
    parser.add_argument("--fixture", type=Path, default=Path(__file__).with_name("fixtures") / "python-insider-sample.xml")
    parser.add_argument("--background-limit", type=int, default=1500)
    args = parser.parse_args()
    data = fetch(args.feed_url) if args.feed_url else args.fixture.read_bytes()
    feed = parse_feed(data)
    if not feed["items"]:
        raise ValueError("RSS 没有 item")
    print(f"订阅源：{feed['title']}（读取 {min(5, len(feed['items']))} 篇）")
    for index, item in enumerate(feed["items"][:5], 1):
        print(f"  [{index}] {item['title'][:60]}")
    content = clean_markup(feed["items"][0]["description"])
    scope = build_scope(content, args.background_limit)
    print("\n=== 伴读范围组装 ===")
    print(f"[背景摘录] {len(scope['background'])}/{scope['total_chars']} 字符；truncated={scope['truncated']}")
    print(f"[请求范围-选段] {scope['selected'][:120]}")
    print("纪律：背景只提供语境，选段才是请求范围；实际回答仍须检查引用是否越界")


if __name__ == "__main__":
    main()
