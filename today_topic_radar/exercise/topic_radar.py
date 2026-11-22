#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""选题雷达原型：直接公开信号→五项启发式评分→只产草稿。

默认读取明确标注的合成夹具，不联网；--live 才访问 GitHub/HN 公开 API。
五项各 1 分：时效、目标受众、直接信号、标题脱水初筛、叙事轮换。
分数只用于排序，不证明事实、质量、传播效果或发布许可。
"""
import argparse
import datetime
import json
import urllib.request
from pathlib import Path

HYPE_WORDS = ["震惊", "疯了", "绝杀"]
AUDIENCE_WORDS = ["ai", "agent", "llm", "model"]


def get_json(url):
    request = urllib.request.Request(url, headers={"User-Agent": "topic-radar-learn/2.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def infer_topic(text):
    lowered = text.lower()
    for key, words in {
        "agent-safety": ["safe", "security", "guard", "risk"],
        "agent-tools": ["agent", "mcp", "tool"],
        "ai-video": ["video", "movie", "film"],
        "ai-models": ["llm", "model", "gpt"],
    }.items():
        if any(word in lowered for word in words):
            return key
    return "other"


def score(candidate, today, recent_topics):
    """返回可解释的五分制启发式结果，不篡改输入。"""
    reasons = []
    try:
        published = datetime.date.fromisoformat(candidate["published_at"][:10])
        age = (today - published).days
        timely = 0 <= age <= 7
        reasons.append(("时效", timely, f"发布 {published}，距基准日 {age} 天"))
    except (KeyError, ValueError):
        timely = False
        reasons.append(("时效", False, "缺少有效发布日期"))

    text = (candidate.get("title", "") + " " + candidate.get("desc", "")).lower()
    audience = any(word in text for word in AUDIENCE_WORDS)
    reasons.append(("目标受众", audience, "命中 AI/agent/llm/model 关键词" if audience else "未命中当前 AI 受众关键词"))

    direct = candidate.get("direct_signal") is True
    reasons.append(("直接信号", direct, candidate.get("source", "未标来源")))

    dehydrated = not any(word in candidate.get("title", "") for word in HYPE_WORDS)
    reasons.append(("标题脱水初筛", dehydrated, "未命中少量标题情绪词" if dehydrated else "命中标题情绪词"))

    topic = candidate.get("topic_key") or infer_topic(text)
    rotated = topic not in set(recent_topics)
    reasons.append(("叙事轮换", rotated, f"主题 {topic} " + ("未见于所给近期历史" if rotated else "已见于近期历史")))
    return {"score": sum(bool(item[1]) for item in reasons), "reasons": reasons, "topic_key": topic}


def live_candidates(today):
    week_ago = today - datetime.timedelta(days=7)
    candidates = []
    github = get_json(f"https://api.github.com/search/repositories?q=created:>{week_ago}&sort=stars&order=desc&per_page=8")
    for item in github.get("items", [])[:5]:
        text = item["full_name"] + " " + (item.get("description") or "")
        candidates.append({
            "title": item["full_name"], "signal": f"GitHub 新开 {item['stargazers_count']}★",
            "url": item["html_url"], "desc": (item.get("description") or "")[:120],
            "source": "GitHub Search API（直接仓库信号）", "direct_signal": True,
            "published_at": item["created_at"], "topic_key": infer_topic(text),
        })
    ids = get_json("https://hacker-news.firebaseio.com/v0/topstories.json")[:6]
    for item_id in ids:
        story = get_json(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json")
        if story and story.get("title"):
            candidates.append({
                "title": story["title"], "signal": f"HN {story.get('score', 0)} 分/{story.get('descendants', 0)} 评",
                "url": story.get("url", f"https://news.ycombinator.com/item?id={item_id}"),
                "desc": "", "source": "HN API（直接讨论信号，非原报道核验）", "direct_signal": True,
                "published_at": datetime.datetime.fromtimestamp(story["time"], datetime.timezone.utc).isoformat(),
                "topic_key": infer_topic(story["title"]),
            })
    return candidates


def render(candidates, today, recent_topics):
    ranked = []
    for candidate in candidates:
        ranked.append({"candidate": candidate, "evaluation": score(candidate, today, recent_topics)})
    ranked.sort(key=lambda item: item["evaluation"]["score"], reverse=True)
    lines = ["# 选题雷达草稿 v2（只产草稿，人工定夺）",
             f"> 基准日 {today}｜五项启发式各 1 分；分数不证明事实、质量或传播效果\n"]
    for index, item in enumerate(ranked[:6], 1):
        candidate, evaluation = item["candidate"], item["evaluation"]
        reasons = "；".join(f"{name}{'✓' if passed else '✗'}({detail})" for name, passed, detail in evaluation["reasons"])
        lines.extend([f"## 候选{index}：{candidate['title']}",
                      f"- 信号：{candidate.get('signal', '未提供')}",
                      f"- 评分：{evaluation['score']}/5；{reasons}",
                      f"- 来源：{candidate['url']}（{candidate.get('source', '未提供')}）",
                      f"- 草稿角度：{candidate.get('desc') or '见来源讨论；发布前必须回源核对'}"])
    return "\n\n".join(lines) + "\n", ranked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="访问公开 GitHub/HN API；默认不联网")
    parser.add_argument("--fixture", type=Path, default=Path(__file__).with_name("fixtures") / "topic_candidates.json")
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("radar-draft-v2.md"))
    parser.add_argument("--today", type=datetime.date.fromisoformat, default=datetime.date.today())
    args = parser.parse_args()
    if args.live:
        candidates, recent_topics = live_candidates(args.today), []
    else:
        fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
        candidates, recent_topics = fixture["candidates"], fixture.get("recent_topics", [])
    document, ranked = render(candidates, args.today, recent_topics)
    args.output.write_text(document, encoding="utf-8")
    print(f"候选 {len(candidates)} 条 → 五项启发式排序 → {args.output}")
    for item in ranked[:3]:
        print(f"- {item['candidate']['title']}: {item['evaluation']['score']}/5")
    print("只产草稿；来源逐条保留；评分不替代回源、事实核查和人工发布决定")


if __name__ == "__main__":
    main()
