# -*- coding: utf-8 -*-
"""实验2：用官方 JSON Schema 校验自编候选（含反例测试）"""
import json, sys
from jsonschema import Draft202012Validator, RefResolver
sys.stdout.reconfigure(encoding="utf-8")

base = r"F:/reminder/archify/repo/archify/schemas/"
store = {}
for name in ["common.schema.json", "workflow.schema.json"]:
    s = json.load(open(base + name, encoding="utf-8"))
    store[s.get("$id", name)] = s

schema = store[[k for k in store if "workflow" in k][0]]
resolver = RefResolver(base_uri="", referrer=schema, store=store)

def check(path, label):
    cand = json.load(open(path, encoding="utf-8"))
    v = Draft202012Validator(schema, resolver=resolver)
    errs = sorted(v.iter_errors(cand), key=lambda e: e.path)
    print(f"[{label}] 错误数: {len(errs)}")
    for e in errs[:5]:
        print("   ", list(e.path), "->", e.message[:110])
    return len(errs)

ok = check(r"F:/reminder/archify/exercise/shiyi-pipeline.workflow.json", "正例: 拾遗流水线")
# 反例1: 删掉必填的 lanes
cand = json.load(open(r"F:/reminder/archify/exercise/shiyi-pipeline.workflow.json", encoding="utf-8"))
cand.pop("lanes"); cand["nodes"][0].pop("lane")
json.dump(cand, open(r"F:/reminder/archify/exercise/_bad1.json", "w", encoding="utf-8"), ensure_ascii=False)
bad1 = check(r"F:/reminder/archify/exercise/_bad1.json", "反例1: 删 lanes + node.lane")
# 反例2: 非法 node type
cand2 = json.load(open(r"F:/reminder/archify/exercise/shiyi-pipeline.workflow.json", encoding="utf-8"))
cand2["nodes"][0]["type"] = "magic-box"
json.dump(cand2, open(r"F:/reminder/archify/exercise/_bad2.json", "w", encoding="utf-8"), ensure_ascii=False)
bad2 = check(r"F:/reminder/archify/exercise/_bad2.json", "反例2: 非法 type=magic-box")
print()
print("结论: 正例通过" if ok == 0 else "结论: 正例未通过，需修复")
print(f"门禁生效验证: 反例1 被拦({bad1>0}), 反例2 被拦({bad2>0})")
