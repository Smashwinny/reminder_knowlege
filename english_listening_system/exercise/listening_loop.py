"""Offline, deterministic demonstration of the article's listening feedback loop.

The input transcript/retell values are synthetic learner fixtures, not human
performance data. Metrics are proxies, not CEFR or comprehension measurements.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

MATERIAL_TITLE = "A clearer project update"
TARGET_CHUNKS = ("runs late", "which task blocked me", "makes the conversation clearer")
KEY_POINTS = (
    ("project", "late"),
    ("task", "blocked"),
    ("conversation", "clearer"),
)
ALLOWED_ERROR_CATEGORIES = {
    "声音边界", "词尾与弱读", "连读或弱读", "单词不认识",
    "熟词反应慢", "句子结构", "篇章理解", "短期记忆",
}


def words(text: str) -> list[str]:
    return re.findall(r"[a-z]+(?:'[a-z]+)?", text.lower())


def edit_distance(reference: list[str], heard: list[str]) -> int:
    previous = list(range(len(heard) + 1))
    for i, ref_word in enumerate(reference, 1):
        current = [i]
        for j, heard_word in enumerate(heard, 1):
            current.append(min(
                previous[j] + 1,
                current[j - 1] + 1,
                previous[j - 1] + (ref_word != heard_word),
            ))
        previous = current
    return previous[-1]


def word_metrics(reference_text: str, transcript: str) -> dict[str, float | int]:
    reference = words(reference_text)
    heard = words(transcript)
    if not reference:
        raise ValueError("Reference material has no English words.")
    distance = edit_distance(reference, heard)
    wer = distance / len(reference)
    return {
        "reference_words": len(reference),
        "transcript_words": len(heard),
        "word_edits": distance,
        "word_error_rate": round(wer, 4),
        "word_accuracy_proxy": round(max(0.0, 1.0 - wer), 4),
    }


def key_point_coverage(retell: str) -> dict[str, object]:
    tokens = set(words(retell))
    hits = [all(word in tokens for word in point) for point in KEY_POINTS]
    return {
        "hits": hits,
        "score_proxy": round(sum(hits) / len(KEY_POINTS), 4),
    }


def chunk_recycling(responses: list[str]) -> dict[str, object]:
    combined = " ".join(responses).lower()
    hits = [chunk in combined for chunk in TARGET_CHUNKS]
    return {
        "hits": dict(zip(TARGET_CHUNKS, hits)),
        "score_proxy": round(sum(hits) / len(TARGET_CHUNKS), 4),
    }


def validate_errors(material: str, transcript: str, errors: list[dict[str, str]]) -> None:
    material_tokens = words(material)
    transcript_tokens = words(transcript)
    for error in errors:
        if error["category"] not in ALLOWED_ERROR_CATEGORIES:
            raise ValueError(f"Unknown error category: {error['category']}")
        if error["original"] not in material_tokens:
            raise ValueError(f"Original word absent from material: {error['original']}")
        if error["heard"] not in transcript_tokens:
            raise ValueError(f"Heard word absent from transcript: {error['heard']}")


def build_review_questions(
    errors: list[dict[str, str]],
    recycled: dict[str, object],
    retell: dict[str, object],
) -> list[str]:
    questions = [f"闭眼听原句：{e['original']} 与 {e['heard']} 的声音差异是什么？" for e in errors]
    for chunk, hit in recycled["hits"].items():
        if not hit:
            questions.append(f"不看提示，用一个工作场景主动说出语块：{chunk}")
    for point, hit in zip(("项目延迟", "阻塞原因", "沟通结果"), retell["hits"]):
        if not hit:
            questions.append(f"不复读原文，用一句英语复述关键点：{point}")
    return (questions + ["半句预测：Now I explain which task ... 后半句是什么？"])[:3]


def render_note(material: str, session: dict[str, object], metrics: dict[str, object]) -> str:
    errors = session["errors"]
    error_lines = [f"- {e['original']} → 听成 {e['heard']}｜{e['category']}" for e in errors] or ["- 本次合成样本未记录误听"]
    review_lines = [f"{i}. {q}" for i, q in enumerate(metrics["review_questions"], 1)]
    return "\n".join([
        "---",
        f"date: {session['date']}",
        "source: local SAPI audio + self-authored material",
        f"topic: {session['topic']}",
        f"level: {session['level']}",
        f"listening_accuracy_proxy: {metrics['word_metrics']['word_accuracy_proxy']}",
        f"retell_score_proxy: {metrics['retell']['score_proxy']}",
        "---",
        "",
        f"# 英语听力｜{session['date']}｜{MATERIAL_TITLE}",
        "",
        "## 今天听了什么",
        "",
        f"- 材料：{MATERIAL_TITLE}",
        "- 音频：material.wav（Windows SAPI 合成）",
        f"- 原文：{material}",
        "",
        "## 我听错的地方",
        "",
        *error_lines,
        "",
        "## 今天的三个语块",
        "",
        *[f"{i}. {chunk}" for i, chunk in enumerate(TARGET_CHUNKS, 1)],
        "",
        "## 我的复述",
        "",
        str(session["retell"]),
        "",
        "## 主动调用情况",
        "",
        f"- 新场景语块命中代理：{metrics['recycling']['score_proxy']:.1%}",
        "",
        "## 明天复习",
        "",
        *review_lines,
        "",
        "> 指标仅描述这份合成夹具，不是人类听力、CEFR 等级或长期进步证明。",
        "",
    ])


def run(material_path: Path, session_path: Path, out_dir: Path) -> dict[str, object]:
    material = material_path.read_text(encoding="utf-8").strip()
    session = json.loads(session_path.read_text(encoding="utf-8"))
    validate_errors(material, str(session["transcript"]), session["errors"])
    recycling = chunk_recycling(session["scenario_responses"])
    retell = key_point_coverage(str(session["retell"]))
    metrics = {
        "word_metrics": word_metrics(material, str(session["transcript"])),
        "retell": retell,
        "recycling": recycling,
        "review_questions": build_review_questions(session["errors"], recycling, retell),
    }
    result = {
        "session_id": session["session_id"],
        "fixture_notice": "Synthetic learner fixture; not a human learning outcome.",
        "metrics": metrics,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = str(session["session_id"])
    (out_dir / f"{stem}-result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out_dir / f"{stem}-note.md").write_text(render_note(material, session, metrics), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--material", type=Path, required=True)
    parser.add_argument("--session", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.material, args.session, args.out_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
