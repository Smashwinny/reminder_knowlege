# -*- coding: utf-8 -*-
"""
实验4：Token/成本账单核算器（对标文章第九节"做 AI 视频到底要花多少钱"）
1. 复算文章的账：$100/月 ÷ 60 条 = $1.67/条 vs ÷ 10 条 = $10/条 —— 出片密度决定边际成本
2. 算我们这条本地流水线的真实成本：edge-tts ¥0、Remotion 个人免费、耗时用真实实测值
3. 推导"单条成本-月产量"曲线数据（写进 PDF 的图）
"""
import json
from pathlib import Path

OUT = Path(__file__).parent / "output"

def per_video_cost(monthly_usd: float, videos: int) -> float:
    return monthly_usd / videos

def main():
    # 1. 复算文章的账
    assert round(per_video_cost(100, 60), 2) == 1.67, "文章的 $1.67 复算不符"
    assert per_video_cost(100, 10) == 10.0, "文章的 $10 复算不符"
    curve = [{"videos": n, "per_video_usd": round(per_video_cost(100, n), 2)}
             for n in [5, 10, 20, 30, 40, 50, 60]]
    print("[1] 文章账单复算通过：$100/月 ÷60条=$1.67 ÷10条=$10.00")
    print("    单条成本-月产量曲线:", curve)

    # 2. 本地流水线实测成本（读取 ex2/ex3 的真实产物）
    timeline = json.loads((OUT.parent / "output" / "timeline.json").read_text(encoding="utf-8"))
    total_sec = timeline["total"]
    chars = sum(len(s["text"]) for s in timeline["sentences"])
    demo_mp4 = OUT.parent / "remotion_app" / "out" / "demo.mp4"
    size_mb = demo_mp4.stat().st_size / 1024 / 1024
    local = {
        "旁白时长_秒": total_sec,
        "口播字数": chars,
        "TTS": "edge-tts 7.2.7（免费，0 API key）成本 ¥0",
        "渲染": f"Remotion 4.0.532 本机渲染 {size_mb:.1f}MB mp4，个人/3人以下小团队免费",
        "LLM": "口播稿本实验为人写（离线复刻不带 LLM）；生产版走 Claude 订阅，计入库",
    }
    print("\n[2] 本地流水线实测：", json.dumps(local, ensure_ascii=False, indent=2))

    # 3. 订阅档位对比（文章给的参考价）
    tiers = {"Pro $20/月": 20, "Max $100/月": 100}
    for name, usd in tiers.items():
        for v in (10, 60):
            print(f"    {name} ÷ {v} 条/月 = ${usd/v:.2f}/条（≈¥{usd/v*7.2:.0f}）")

    (OUT / "ex4_cost_report.json").write_text(json.dumps(
        {"article_check": "PASS", "curve": curve, "local": local},
        ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n断言全部通过，报告已写 output/ex4_cost_report.json")

if __name__ == "__main__":
    main()
