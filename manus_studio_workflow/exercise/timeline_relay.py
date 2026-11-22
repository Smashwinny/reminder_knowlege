#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""本地分层时间轴交接协议实验，不是 Manus Studio 内部实现或 API 复刻。

验证一个保守设计：人工修改的元素由本地协议标记 locked；尊重锁定时 AI
二轮跳过，删除这条保护时同一人工值会被覆盖。未连接 Manus，也未生成视频。
"""
import argparse
import copy


def ai_draft(brand):
    return {"brand": brand, "layers": {
        "shots": [{"id": f"s{i}", "value": f"clip{i}.mp4", "note": "AI 初稿"} for i in range(3)],
        "texts": [{"id": "t1", "value": brand["slogan"], "note": "AI 初稿"}],
        "motion": [{"id": "m1", "value": "ease-out", "note": "AI 初稿"}],
        "audio": [{"id": "a1", "value": "brand-bgm.mp3", "note": "AI 初稿"}],
    }}


def human_edit(timeline, layer, element_id, new_value):
    for element in timeline["layers"][layer]:
        if element["id"] == element_id:
            element.update(value=new_value, note="人工修改", locked=True)
            return timeline
    raise ValueError(f"找不到元素 {layer}/{element_id}")


def ai_polish(timeline, respect_locks=True):
    touched, skipped = [], []
    for layer, elements in timeline["layers"].items():
        for element in elements:
            if respect_locks and element.get("locked"):
                skipped.append(f"{layer}/{element['id']}")
            else:
                element["value"] = "AI 二轮统一润色版本"
                element["note"] = "AI 二轮润色"
                touched.append(f"{layer}/{element['id']}")
    return timeline, touched, skipped


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slogan", default="让世界更顺滑")
    parser.add_argument("--replacement", default="换成用户实拍素材.mp4")
    args = parser.parse_args()

    original = ai_draft({"name": "Cue", "slogan": args.slogan, "tone": "克制/高级"})
    edited = human_edit(copy.deepcopy(original), "shots", "s2", args.replacement)
    protected, touched, skipped = ai_polish(copy.deepcopy(edited), respect_locks=True)
    assert protected["layers"]["shots"][2]["value"] == args.replacement
    assert protected["layers"]["shots"][2]["note"] == "人工修改"
    assert skipped == ["shots/s2"] and len(touched) == 5

    unprotected, _, _ = ai_polish(copy.deepcopy(edited), respect_locks=False)
    assert unprotected["layers"]["shots"][2]["value"] == "AI 二轮统一润色版本"
    assert unprotected["layers"]["shots"][2]["value"] != args.replacement

    print("① 初稿层：", {key: len(value) for key, value in original["layers"].items()})
    print("② 人工修改：shots/s2 =", args.replacement)
    print("③ 尊重锁定：润色", len(touched), "个元素；跳过", skipped)
    print("   PASS：人工值与备注均保留")
    print("④ 删除保护：shots/s2 =", unprotected["layers"]["shots"][2]["value"])
    print("   PASS：人工值确实被覆盖，破坏测试有效")
    print("边界：这是自写本地协议，不证明 Manus 产品存在 locked 字段或相同行为")


if __name__ == "__main__":
    main()
