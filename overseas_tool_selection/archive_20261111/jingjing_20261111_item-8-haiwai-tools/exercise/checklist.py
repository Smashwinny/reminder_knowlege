#!/usr/bin/env python3
"""按阶段输出选型清单：默认只选少数工具，不一次采购全部。"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAGE_PICKS = {
    "一、市场机会与竞品调研": {
        "先用": ["沉浸式翻译", "Wayback Machine", "Google Trends", "Wappalyzer", "AITDK"],
        "按需再加": ["SiteData", "Similarweb", "Exploding Topics"],
        "原则": "先免费或低成本看原文、历史快照、趋势和技术栈；趋势曲线不能当成需求已经验证。",
    },
    "二、SEO 与内容资产": {
        "先用": ["Screaming Frog SEO Spider", "SEO Minion"],
        "按需再加（二选一）": ["Semrush", "Ahrefs"],
        "外链相关需人工审页": ["Moz Link Explorer", "Linkhouse", "Collaborator", "Fiverr", "Adsy"],
        "原则": "先修自己站点的技术问题。关键词套件作者说 Semrush 和 Ahrefs 选一个即可。外链采购只看相关性、真实流量和页面质量，不批量堆链接。Fiverr 与 Adsy 在原文里编号错位置于本章。",
    },
    "三、产品设计、AI 能力与演示": {
        "先用": ["Figma", "OpenRouter"],
        "按需再加": ["Framer", "Dify", "n8n", "Replicate", "IconPark", "Midjourney", "Ideogram", "Loom", "Screen Studio"],
        "原则": "先把五个关键页面连成可点击流程，再用真实任务比较模型成本和质量。Framer 不适合复杂大型 SaaS。带文字的生图必须人工校对。",
    },
    "四、建站、本地化与基础设施": {
        "先用": ["Cloudflare", "Vercel", "DeepL"],
        "按需再加": ["Weglot", "Lokalise"],
        "原则": "先保证访问和部署，再测一个语言市场；DeepL 只能出第一版，关键页要人工润色。",
    },
    "五、支付、跨境资金与合规": {
        "先用（先验证愿付）": ["Lemon Squeezy", "Paddle"],
        "需要自控订阅数据时": ["Stripe"],
        "资金账户与政策草稿": ["Starryblu", "Termly"],
        "原则": "作者建议用测试支付走完付款、退款、升级、取消和失败重试。本批只做官网可达探测，不发起任何真实或测试支付，不注册账户，不使用原文推荐码。Termly 生成的文本不是法律意见。",
    },
    "六、增长获客与渠道分发": {
        "先用": ["Product Hunt", "Typefully", "Beehiiv", "Loops"],
        "按需再加": ["Uneed", "Microlaunch", "BetaList", "Discord", "Disboard", "Toolify", "There's An AI For That", "Customer"],
        "原则": "提交到导航站不等于产品验证成功。社群先参与讨论。Customer 在原文只有简称，对应官网是推断。",
    },
    "七、数据分析与用户反馈": {
        "先用": ["Google Search Console", "Google Analytics 4", "PostHog"],
        "按需再加": ["Microsoft Clarity", "Crisp", "Cursorful", "Feedlog"],
        "原则": "注册了却没有第一份结果时，先改首次使用，不要继续投放。Feedlog 是作者自述的自己的产品，选型时单独标注利益关系。",
    },
}


def main() -> int:
    catalog = json.loads((HERE / "tools.json").read_text(encoding="utf-8"))
    by_chapter = defaultdict(list)
    for t in catalog["tools"]:
        by_chapter[t["chapter"]].append(t["name"])
    print("选型清单（默认少量组合，不必一次采购或接入全部）")
    print("依据：已读长文用法 + 编号缺陷记录。不是使用效果测评。")
    print()
    for chapter, advice in STAGE_PICKS.items():
        print(f"## {chapter}")
        print("原文提到：", "、".join(by_chapter[chapter]))
        for k, v in advice.items():
            if isinstance(v, list):
                print(f"  {k}: " + "、".join(v))
            else:
                print(f"  {k}: {v}")
        print()
    print("全局纪律：")
    print("  1. 不要把「作者整理了 56 个实战工具」理解成精确、无缺号的官方目录。")
    print("  2. 官网能打开 ≠ 工具适合你，更不是付费计划或效果已经验证。")
    print("  3. 不注册、不采购外链、不接入支付、不使用推荐码。")
    (HERE / "checklist-stages.json").write_text(
        json.dumps(STAGE_PICKS, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
