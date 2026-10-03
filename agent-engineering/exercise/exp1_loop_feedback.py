# -*- coding: utf-8 -*-
"""
实验1：Loop Engineering —— 为什么"失败了，请重试"是最坏的反馈
模拟一个最小 agent loop：任务 = 读取 data.csv 求和，把结果写进 report.md
- 坏反馈模式：校验器只说"失败了，请重试" -> 策略每轮原样重跑 -> 烧满 max_rounds
- 好反馈模式：校验器返回结构化失败(哪步失败/缺什么/该改什么) -> 策略第2轮修正 -> 通过
模型用规则策略模拟（零 API、确定性），比的是"反馈信息量"这一个变量。
"""
import csv, os, json, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
MAX_ROUNDS = 5

# ---------- 环境 ----------
def make_data():
    path = os.path.join(HERE, "data.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["city", "sales"])
        for row in [("北京", 120), ("上海", 340), ("深圳", 80), ("杭州", 260)]:
            w.writerow(row)
    return path

class Env:
    """agent 的手脚：只有 read_csv / write_file 两个工具"""
    def __init__(self):
        self.wrote_report = False
        self.report_content = ""

    def act(self, action):
        if action["tool"] == "read_csv":
            with open(action["path"], encoding="utf-8") as f:
                return list(csv.reader(f))
        if action["tool"] == "write_file":
            self.wrote_report = True
            self.report_content = action["content"]
            with open(os.path.join(HERE, "report.md"), "w", encoding="utf-8") as f:
                f.write(action["content"])
            return "ok"
        return "unknown tool"

# ---------- 校验器：好坏两种人格 ----------
def validate(env):
    """返回 (passed, feedback_dict)。feedback_dict 结构化程度是本实验唯一变量。"""
    problems = []
    if not env.wrote_report:
        problems.append({"step": "write", "missing": "report.md 还没写", "fix": "先调 compute，再调 write_file"})
    else:
        if "TOTAL:" not in env.report_content:
            problems.append({"step": "compute", "missing": "报告里没有 TOTAL: 汇总数字", "fix": "用 read_csv 读数据，自己算 sales 列总和，写成 TOTAL: <数字>"})
        total = 120 + 340 + 80 + 260
        if "TOTAL:" in env.report_content and str(total) not in env.report_content:
            problems.append({"step": "compute", "missing": "TOTAL 数字算错（正确是 800）", "fix": "重新读 data.csv 逐行累加 sales 列"})

    if not problems:
        return True, None
    # ---- 坏反馈：把结构化信息全部扔掉 ----
    bad = {"step": "?", "missing": "", "fix": ""}
    # ---- 好反馈：原样返回 ----
    good = problems[0]
    return False, {"bad": bad, "good": good}

# ---------- 被测"模型"：规则策略，只对反馈内容做反应 ----------
def policy(round_no, env, feedback):
    """
    naive=True  : 无视反馈内容（模拟收到"失败了请重试"的 agent）——每轮都做同样的错事：
                  没算数直接写一份占位报告
    naive=False : 认真读结构化反馈，按 fix 字段逐轮修（round1 写占位->被告知缺 TOTAL，
                  round2 读 csv 算总和->被告知数字错, round3 写对）
    """
    if feedback is None:                       # 第一轮，还没有任何反馈
        env.act({"tool": "write_file", "content": "# 销售报告\nTODO\n"})
        return "写了占位报告（没算数）"
    if "fix" not in feedback or not feedback["fix"]:   # 坏反馈：内容为空，等于没说
        env.act({"tool": "write_file", "content": "# 销售报告\nTODO\n"})
        return "收到『失败了，请重试』-> 原样再写一遍占位报告"
    # 好反馈：按指哪修哪推进
    step = feedback["step"]
    if step == "write":
        env.act({"tool": "write_file", "content": "# 销售报告\nTOTAL: 0\n"})
        return "按反馈补写报告骨架（TOTAL 先占位 0）"
    if step == "compute" and "TOTAL: 0" in env.report_content:
        rows = env.act({"tool": "read_csv", "path": os.path.join(HERE, "data.csv")})
        total = sum(int(r[1]) for r in rows[1:])
        env.act({"tool": "write_file", "content": f"# 销售报告\nTOTAL: {total}\n"})
        return f"按反馈读 csv 算总和 -> TOTAL: {total}"
    if step == "compute":                       # 数字算错的情况
        rows = env.act({"tool": "read_csv", "path": os.path.join(HERE, "data.csv")})
        total = sum(int(r[1]) for r in rows[1:])
        env.act({"tool": "write_file", "content": f"# 销售报告\nTOTAL: {total}\n"})
        return f"按反馈重新逐行累加 -> TOTAL: {total}"
    return "无可行动"

def run_loop(naive_feedback):
    env = Env()
    trace = []
    feedback = None
    passed = False
    for r in range(1, MAX_ROUNDS + 1):
        note = policy(r, env, feedback)
        ok, prob = validate(env)
        if ok:
            passed = True
            trace.append(f"  round{r}: {note} -> ✅ 校验通过")
            break
        # 关键一行：naive_feedback=True 时把结构化反馈压扁成"失败了，请重试"
        fb = prob["bad"] if naive_feedback else prob["good"]
        trace.append(f"  round{r}: {note} -> ❌ 失败")
        feedback = fb
    return passed, trace

if __name__ == "__main__":
    make_data()
    print("=" * 62)
    print("实验1：坏反馈(失败了请重试) vs 好反馈(指明哪步/缺什么/怎么改)")
    print("=" * 62)
    p1, t1 = run_loop(naive_feedback=True)
    print("\n【A. 坏反馈组】校验器只说『失败了，请重试』")
    print("\n".join(t1))
    print(f"  -> 结果：{'通过' if p1 else f'✗ {MAX_ROUNDS} 轮全烧完，任务失败'}")
    p2, t2 = run_loop(naive_feedback=False)
    print("\n【B. 好反馈组】校验器返回结构化失败反馈")
    print("\n".join(t2))
    print(f"  -> 结果：{'✅ 通过' if p2 else '✗ 失败'}")
    print("\n结论：同一个'模型'、同一套工具，反馈从 0 比特变成结构化 3 要素，")
    print(f"      从 {MAX_ROUNDS} 轮全烧完变成 {len(t2)} 轮收敛 —— 这就是 Loop Engineering 的全部秘密。")
