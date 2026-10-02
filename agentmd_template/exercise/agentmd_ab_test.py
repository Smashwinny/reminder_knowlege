# -*- coding: utf-8 -*-
"""
AGENT.md 模板效果对比实验（A/B test）
问题：贴上这份"沟通/执行方式"规则后，模型输出行为真的变了吗？
方法：同一个任务，A 组裸系统提示，B 组加模板的沟通+执行方式+测试验证节选，
     各跑 3 次，用确定性正则规则打分（不靠人眼、不靠 LLM 裁判）。
用法：python agentmd_ab_test.py
"""
import os, re, json, time
from anthropic import Anthropic

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(HERE, "AGENT_md_template.md")

TEMPLATE = open(TEMPLATE_PATH, encoding="utf-8").read()
# 只取单轮对话适用的板块（工具与并行/规则来源是 agent harness 才生效的，实验里用不上）
def section(name):
    m = re.search(r"## " + name + r"\n(.*?)(?=\n## |\Z)", TEMPLATE, re.S)
    return "## " + name + "\n" + m.group(1).strip() + "\n"

SYSTEM_B = (
    "你是一个乐于助人的编程助手。\n\n"
    + section("沟通") + "\n" + section("执行方式") + "\n" + section("测试与验证")
)
SYSTEM_A = "你是一个乐于助人的编程助手。"

SCENARIOS = {
    # 场景1：常规写代码任务——测 沟通 板块（结论先行/列表克制）
    "merge_txt": {
        "task": "帮我写一个 Python 函数，把一个文件夹里所有 .txt 文件合并成一个大文件，按文件名排序。",
        "metrics": ["conclusion_first", "bullet_lines"],
    },
    # 场景2：琐碎可逆改动——测 测试与验证 板块（"琐碎改动不强制跑测试"）
    #   A 组预期：要求跑全套测试/CI；B 组预期：说明不需要额外动作
    "typo_fix": {
        "task": "我在自己的个人小项目里把 README.md 的一个错别字'配置文件'改成了'配置文件夹'，已经提交了。接下来我还需要做些什么？",
        "metrics": ["demand_tests", "advice_lines"],
    },
    # 场景3：本地玩具脚本——测 执行方式 板块（"不为假想风险加未经请求的警告"）
    #   A 组预期：主动加 SQL 注入警告；B 组预期：按需求写，不加未经请求的警告
    "sql_toy": {
        "task": "写个 Python 函数，把用户在命令行输入的名字直接拼进 SQL，去查我本机上的 SQLite 玩具数据库并打印结果。",
        "metrics": ["unsolicited_warning", "warn_terms"],
    },
}
TASK = SCENARIOS["merge_txt"]["task"]

FILLER = re.compile(r"^(好的|当然|没问题|收到|明白|好的，|当然可以|这是一个|你想要|你的需求)")
END_PUNCT = re.compile(r"[。！？]")
WARN = re.compile(r"免责|请注意|温馨提示|风险提示|注意[:：]|生产环境|慎用|谨慎|安全提示")
BULLET = re.compile(r"^\s*(?:[-*•]|\d+[.、)])\s+", re.M)
CJK = re.compile(r"[一-鿿]")

def split_prose_code(text):
    """把回复拆成 散文部分（markdown 代码围栏之外）和 代码部分"""
    parts = re.split(r"```.*?```", text, flags=re.S)
    prose = "".join(parts)
    code = "".join(re.findall(r"```(?:\w+)?\n(.*?)```", text, flags=re.S))
    return prose, code

DEMAND_TESTS = re.compile(r"跑(一下|一遍)?测试|测试套件|运行测试|单元测试|CI|回归测试|pytest")
ADVICE = re.compile(r"(建议|推荐|接下来|还可以|记得)")

def score(text):
    prose, code = split_prose_code(text)
    lines = [l for l in prose.strip().splitlines() if l.strip()]
    first = lines[0].strip() if lines else ""
    warn_hits = WARN.findall(prose)
    return {
        "conclusion_first": bool(first and END_PUNCT.search(first) and not FILLER.match(first)),
        "no_unsolicited_warning": not warn_hits,
        "warn_terms": sorted(set(warn_hits))[:4],
        "demand_tests": bool(DEMAND_TESTS.search(prose)),
        "advice_lines": sum(1 for l in lines if ADVICE.search(l)),
        "bullet_lines": len(BULLET.findall(prose)),
        "cjk_chars": len(CJK.findall(prose)),
        # 规则原文是"代码、命令和技术标识保持英文"——只查 def/类名等标识符，中文注释/docstring 不算违规
        "code_ascii_ident": all(a.isascii() for a in re.findall(r"def\s+(\w+)", code)),
        "first_line": first[:40],
    }

def run_arm(label, system, task, n):
    c = Anthropic(api_key=os.environ["ANTHROPIC_AUTH_TOKEN"],
                  base_url=os.environ["ANTHROPIC_BASE_URL"])
    out = []
    for i in range(n):
        r = c.messages.create(model="glm-4.6", max_tokens=2048, system=system,
                              messages=[{"role": "user", "content": task}])
        text = next(b.text for b in r.content if b.type == "text")
        s = score(text); s["arm"], s["trial"] = label, i + 1
        out.append(s)
        print(f"[{label}{i+1}] 结论先行={s['conclusion_first']} 要跑测试={s['demand_tests']} "
              f"加警告={not s['no_unsolicited_warning']} 警告词={s['warn_terms']} "
              f"列表行={s['bullet_lines']} | 首行: {s['first_line']}")
        time.sleep(1)
    return out

if __name__ == "__main__":
    all_detail, summary = [], {}
    for name, sc in SCENARIOS.items():
        print(f"\n########## 场景 {name} ##########")
        n = 3
        a = run_arm("A", SYSTEM_A, sc["task"], n)
        b = run_arm("B", SYSTEM_B, sc["task"], n)
        all_detail += a + b
        def avg(rows, k): return sum(r[k] for r in rows) / len(rows)
        summary[name] = {
            "A_裸提示": {
                "结论先行率": avg(a, "conclusion_first"),
                "要求跑测试率": avg(a, "demand_tests"),
                "未经请求警告率": avg(a, "no_unsolicited_warning"),
                "平均列表行数": avg(a, "bullet_lines"),
                "平均建议句数": avg(a, "advice_lines"),
            },
            "B_带AGENT模板": {
                "结论先行率": avg(b, "conclusion_first"),
                "要求跑测试率": avg(b, "demand_tests"),
                "未经请求警告率": avg(b, "no_unsolicited_warning"),
                "平均列表行数": avg(b, "bullet_lines"),
                "平均建议句数": avg(b, "advice_lines"),
            },
        }
        print(json.dumps(summary[name], ensure_ascii=False, indent=2))
    print("\n===== 总汇总 =====")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    json.dump({"detail": all_detail, "summary": summary},
              open(os.path.join(HERE, "ab_result.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("结果已存 ab_result.json")
