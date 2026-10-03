# -*- coding: utf-8 -*-
"""
实验1：选题五项内审法评分器（零依赖，确定性）
复刻 Simon聊AI 文章第六节"选题内审法：开工前的5道严密安全阀"：
  1 热点时效（72h内有新进展） 2 痛点圈层（个案->普适）
  3 增量核查（一手硬材料>=2） 4 脱水测试（删情绪词后骨架还在）
  5 叙事匹配（不与上一期同类型）
任一阀不过 = 整题 pass（一票否决，对应文章"这种纯情绪题目我坚决不做"）。
"""
import json, re, sys
from pathlib import Path

EMO_WORDS = ["令人发指", "套路深", "惊天内幕", "离谱", "黑幕", "暴利", "震惊",
             "愤怒", "丧良心", "胆大包天", "触目惊心", "疯了", "抢钱"]

def gate1_freshness(card, now):
    """72 小时内必须有新进展。返回 (通过?, 说明)"""
    from datetime import datetime
    d = datetime.strptime(card["last_develop_date"], "%Y-%m-%d")
    hours = (now - d).total_seconds() / 3600
    return hours <= 72, f"最近进展距发布 {hours:.0f} 小时（要求<=72h）"

def gate2_audience(card):
    """个案特例必须能提炼成普适经验：scope 里要有'你/每年/多少'类泛化，
       且选题名不含具体小区/城市个案名。"""
    name = card["topic"]
    individual = re.search(r"[AB一-龥]{1,3}(市|区|县)?[^，。]{0,6}(小区|社区)", name)
    generalized = any(w in card["audience_hook"] for w in ["你", "每年", "多少", "所有"])
    return (generalized and not individual), f"泛化钩子={'有' if generalized else '无'}，个案地名={'有' if individual else '无'}"

def gate3_evidence(card):
    """增量材料硬度：>=2 条一手信源，每条要有链接+日期。"""
    srcs = card["sources"]
    ok_n = len(srcs) >= 2
    ok_q = all(s.get("url") and s.get("date") for s in srcs)
    return ok_n and ok_q, f"一手信源 {len(srcs)} 条，链接/日期齐全={ok_q}"

def gate4_dehydrate(card, min_ratio=0.70, min_facts=2):
    """情绪脱水测试：删掉情绪词后剩余比例>=min_ratio，且骨架里
       还留得住 >=min_facts 处数字/法条引用（事实密度）。"""
    text = card["outline"]
    hits = [w for w in EMO_WORDS if w in text]
    stripped = text
    for w in hits:
        stripped = stripped.replace(w, "")
    ratio = len(stripped.replace("，", "").replace("。", "")) / max(len(text.replace("，", "").replace("。", "")), 1)
    facts = len(re.findall(r"\d+(\.\d+)?%|第[一二三四五六七八九十百千零〇\d]+条|[0-9０-９]+", stripped))
    return (len(hits) == 0 or ratio >= min_ratio) and facts >= min_facts, \
           f"情绪词 {hits or '无'}，脱水后保留 {ratio:.0%}，事实/数字引用 {facts} 处"

def gate5_narrative(card, last_types):
    """叙事类型轮换：连续两期绝不能套同一种叙事模型。"""
    dup = card["narrative_type"] in last_types[-1:]
    return not dup, f"本期[{card['narrative_type']}] vs 上期[{last_types[-1] if last_types else '无'}]"

GATES = [("1热点时效", gate1_freshness), ("2痛点圈层", None), ("3增量核查", None),
         ("4脱水测试", None), ("5叙事匹配", None)]

def audit(card, now, last_types):
    results = []
    results.append(("1热点时效", *gate1_freshness(card, now)))
    results.append(("2痛点圈层", *gate2_audience(card)))
    results.append(("3增量核查", *gate3_evidence(card)))
    results.append(("4脱水测试", *gate4_dehydrate(card)))
    results.append(("5叙事匹配", *gate5_narrative(card, last_types)))
    verdict = all(ok for _, ok, _ in results)
    return verdict, results

def main():
    from datetime import datetime
    now = datetime(2026, 9, 17, 12, 0, 0)  # 固定"今天"保证确定性
    good = {
        "topic": "买房后这4笔物业暗扣，你每年多交了多少冤枉钱",
        "audience_hook": "所有交物业费的业主每年都多交了钱，你能自己查台账",
        "last_develop_date": "2026-09-16",
        "sources": [
            {"name": "民法典第九百四十三条 物业公开义务", "url": "flk.npc.gov.cn/detail2.html?ZmY4MDgwODE3NTNiNzMwYjAxNzU4ZjM0YzEzNjBmOGU", "date": "2021-01-01", "primary": True},
            {"name": "某市住建局物业服务收费管理办法（2026修订）", "url": "example.gov.cn/wuye-2026", "date": "2026-09-01", "primary": True},
        ],
        "outline": "物业费构成分三块：人员费用约占55%，公共能耗约占20%，管理费约占15%。核查依据是民法典第943条：业主有权要求物业公示年度收支台账。查验台账与合同履约对照，缺项即为多收线索。",
        "narrative_type": "按时间轴复盘蝴蝶效应",
    }
    bad = {
        "topic": "A市阳光花园小区物业跑路，业主愤怒：简直丧良心",
        "audience_hook": "这个小区的业主太惨了",
        "last_develop_date": "2026-05-01",
        "sources": [
            {"name": "网传业主群聊天记录", "url": "", "date": "", "primary": False},
        ],
        "outline": "这家物业令人发指，收费套路深，简直是惊天内幕，业主都气疯了，这事太离谱了。",
        "narrative_type": "顺藤摸瓜查账本",
    }
    report = {}
    for key, card in [("good_物业暗扣", good), ("bad_物业跑路情绪题", bad)]:
        verdict, results = audit(card, now, last_types=["顺藤摸瓜查账本"])
        report[key] = {"verdict": "PASS" if verdict else "REJECT（一票否决）",
                       "gates": [{"gate": g, "pass": ok, "detail": d} for g, ok, d in results]}
        print(f"\n=== {key} -> {report[key]['verdict']} ===")
        for g, ok, d in results:
            print(f"  [{'PASS' if ok else 'FAIL'}] {g}: {d}")

    out = Path(__file__).parent / "output"
    out.mkdir(exist_ok=True)
    (out / "ex1_audit_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # 自检断言
    assert report["good_物业暗扣"]["verdict"] == "PASS"
    assert report["bad_物业跑路情绪题"]["verdict"] == "REJECT（一票否决）"
    g = {x["gate"]: x["pass"] for x in report["bad_物业跑路情绪题"]["gates"]}
    assert g["1热点时效"] is False and g["2痛点圈层"] is False and g["3增量核查"] is False and g["4脱水测试"] is False and g["5叙事匹配"] is False
    print("\n断言全部通过：好题 5/5 PASS，纯情绪题 5/5 一票否决。")

if __name__ == "__main__":
    sys.exit(main())
