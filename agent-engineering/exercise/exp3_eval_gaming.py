# -*- coding: utf-8 -*-
"""
实验3：Eval Engineering —— 糊涂校验器如何被 agent 钻空子（eval gaming）
任务：把一段产品评论压缩成 ≤60 字、覆盖 3 个关键事实的摘要。
两个 agent（诚实者 / 偷懒者）× 两个校验器（糊涂的 / 严格的）：
- 糊涂校验器只查"非空 + 含'总结'两个字 + 长度<500" -> 偷懒者交白卷也得 100 分
- 严格校验器逐条查关键事实存在 + 长度上限 -> 偷懒者现形，诚实者通过
验证文章论点："任务完成了"不算完成；校验器糊，agent 必刷分。
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

TEXT = ("用户吐槽新款耳机：续航虚标严重，标称30小时实际只有8小时（关键事实1）；"
        "佩戴两小时耳朵疼，耳罩材质偏硬（关键事实2）；"
        "但降噪效果意外地好，地铁里几乎听不到报站声（关键事实3），"
        "客服答应换新但要求提供购买凭证（关键事实4）。")
FACTS = ["8小时", "耳朵疼", "降噪", "购买凭证"]

def honest_agent(text):
    return "总结：续航实际8小时远低于标称；佩戴耳痛；降噪出色；换新需购买凭证。"

def lazy_agent(text):
    return "总结：详见原文。"        # 什么都没干，但格式全对

def sloppy_validator(out):
    """糊涂校验器：只看格式，不看内容"""
    checks = {"非空": bool(out.strip()), "含'总结'": "总结" in out, "长度<500": len(out) < 500}
    return all(checks.values()), checks

def strict_validator(out):
    """严格校验器：关键事实逐条在案 + 长度上限（60字）"""
    checks = {f"含事实[{f}]": f in out for f in FACTS}
    checks["长度≤60字"] = len(out) <= 60
    return all(checks.values()), checks

if __name__ == "__main__":
    print("=" * 62)
    print("实验3：糊涂校验器 vs 严格校验器（eval gaming 演示）")
    print("=" * 62)
    print(f"待摘要评论：{TEXT[:40]}...\n要求：≤60字，覆盖4个关键事实 {FACTS}\n")
    rows = []
    for name, out in [("诚实agent", honest_agent(TEXT)), ("偷懒agent", lazy_agent(TEXT))]:
        for vname, vf in [("糊涂校验器", sloppy_validator), ("严格校验器", strict_validator)]:
            ok, checks = vf(out)
            rows.append((name, vname, ok, checks))
    print(f"{'agent':<8}| {'校验器':<8}| 结果 | 明细")
    print("-" * 70)
    for name, vname, ok, checks in rows:
        detail = "；".join(f"{k}:{'过' if v else '挂'}" for k, v in checks.items())
        print(f"{name:<8}| {vname:<8}| {'✅通过' if ok else '❌拒绝'} | {detail}")
    lazy_sloppy = rows[1]
    print("\n关键一行：偷懒agent × 糊涂校验器 = ", "✅通过 —— 交白卷拿满分，这就是被钻空的评估" if lazy_sloppy[2] else "被拦住")
    print("\n结论：评估要评四样——任务本身、环境、校验器、轨迹；校验器松一寸，agent 钻一尺。")
