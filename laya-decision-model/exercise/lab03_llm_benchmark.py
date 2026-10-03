# -*- coding: utf-8 -*-
"""实验 3（主实验·对比侧）：同一套 24 题喂给云端大模型（claude CLI，本机配置 kimi-for-coding）。
复现推主"本地小模型 vs 云端"评测的另一条腿：准确率 + 耗时对比。
跑法：python lab03_llm_benchmark.py  （约 24 次 CLI 调用，串行 3~5 分钟）
"""
import json
import statistics
import subprocess
import time

from lab02_laya_benchmark import TESTSET

PROMPT = ("You are a support-ticket triage classifier. Read the ticket and answer with ONLY a JSON object, "
          "no other text, exactly this shape: {{\"department\":\"billing\"|\"technical\"|\"other\",\"urgency\":0|1|2,"
          "\"churn_risk\":\"yes\"|\"no\"}}. Definitions: department billing=invoices/payments/refunds/charges, "
          "technical=bugs/crashes/outages/errors/access, other=general/sales/feature requests. urgency 0=not urgent, "
          "1=soon, 2=blocking or business stops. churn_risk yes iff the user threatens to cancel or switch to a "
          "competitor. Ticket: {state} JSON:")

def ask(state: str):
    prompt = PROMPT.format(state=state.replace('"', "'"))
    t0 = time.perf_counter()
    p = subprocess.run(
        [r"C:\Users\Windows\AppData\Roaming\npm\claude.cmd", "-p", prompt],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180,
    )
    ms = (time.perf_counter() - t0) * 1000
    txt = (p.stdout or "").strip()
    try:
        j = txt[txt.index("{"): txt.rindex("}") + 1]
        d = json.loads(j)
        return d.get("department"), int(d.get("urgency", -1)), str(d.get("churn_risk", "")).lower(), ms
    except Exception:
        return None, -1, "?", ms

def main():
    rows, lat = [], []
    for i, (state, d, u, c) in enumerate(TESTSET):
        gd, gu, gc, ms = ask(state)
        gcy = 1 if gc in ("yes", "1", "true") else 0
        lat.append(ms)
        hit = {"dept": gd == d, "urg": gu == u, "churn": gcy == c}
        rows.append({"id": i + 1, "lang": "en" if i < 12 else "zh", "ms": round(ms),
                     "dept": [hit["dept"], d, gd], "urg": [hit["urg"], u, gu], "churn": [hit["churn"], c, gcy],
                     "raw": gc})
        print(f"[{i+1:02d}/24] {ms:7.0f}ms dept={'Y' if hit['dept'] else 'N('+str(gd)+')'} "
              f"urg={gu}({'Y' if hit['urg'] else 'N,want '+str(u)}) churn={'Y' if hit['churn'] else 'N'}")
    n = len(TESTSET)
    acc = {k: sum(r[k][0] for r in rows) / n for k in ("dept", "urg", "churn")}
    acc["all3"] = sum(r["dept"][0] and r["urg"][0] and r["churn"][0] for r in rows) / n
    s = sorted(lat)
    print("\n==== 云端大模型（claude CLI / kimi-for-coding）====")
    print(f"dept {acc['dept']:.2%}  urgency {acc['urg']:.2%}  churn {acc['churn']:.2%}  三题全对 {acc['all3']:.2%}")
    print(f"延迟 median={statistics.median(lat):.0f}ms  p95={s[int(len(s)*0.95)-1]:.0f}ms  min={min(lat):.0f}ms max={max(lat):.0f}ms")
    with open("llm_results.json", "w", encoding="utf-8") as f:
        json.dump({"acc": acc, "rows": rows}, f, ensure_ascii=False, indent=1)
    print("已写 llm_results.json")

if __name__ == "__main__":
    main()
