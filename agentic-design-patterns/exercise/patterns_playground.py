# -*- coding: utf-8 -*-
"""
patterns_playground.py — 用确定性 FakeLLM 离线复现《Agentic Design Patterns》书中
5 个代表性设计模式。零 API 依赖（FakeLLM 是规则版"假大模型"，同输入必同输出），
模式结构与书中一致：换掉 FakeLLM 就是真 Agent。

运行: python patterns_playground.py
"""
import json
from concurrent.futures import ThreadPoolExecutor
from pydantic import BaseModel, Field, ValidationError

# ============ 基础设施：FakeLLM（规则版大模型，确定性） ============

class FakeLLM:
    """规则驱动的假 LLM：模拟'收到提示词→返回文本'的接口形状。
    真实场景替换为 ChatOpenAI / Gemini 即可，模式代码一行不改。"""

    def __init__(self):
        self.calls = 0  # 统计调用量（资源感知实验要用）

    def __call__(self, prompt: str, system: str = "") -> str:
        self.calls += 1
        key = (system, prompt)
        if key in RESPONSES:
            return RESPONSES[key]
        # 兜底：按 system 角色给一个确定回复
        return f"[{system or 'assistant'}] 收到：{prompt[:40]}"

LLM = FakeLLM()

# ============ 模式 1：Prompt Chaining 提示链（Ch1） ============
# 固定流水线：三站顺序执行，站与站之间用 JSON 契约交接，不给模型自主权。

def pattern_1_prompt_chaining():
    print("=" * 62)
    print("模式1 Prompt Chaining 提示链：市场简报三站流水线")
    print("=" * 62)

    def station_1_extract(raw_topic: str) -> str:
        """站1：抽关键词 → JSON"""
        return json.dumps({"keywords": raw_topic.lower().split()},
                          ensure_ascii=False)

    def station_2_outline(keywords_json: str) -> str:
        """站2：关键词 → 大纲（每关键词一节）"""
        kw = json.loads(keywords_json)["keywords"]
        return json.dumps({"outline": [f"第{i+1}节：关于「{k}」的趋势与数据"
                                       for i, k in enumerate(kw)]},
                          ensure_ascii=False)

    def station_3_brief(outline_json: str) -> str:
        """站3：大纲 → 最终简报（书里 Ch1 的输出形状：trends 数组）"""
        outline = json.loads(outline_json)["outline"]
        return json.dumps(
            {"trends": [{"trend_name": o.split("「")[1].split("」")[0],
                         "supporting_data": "确定性数据源（FakeLLM 版）"}
                        for o in outline]},
            ensure_ascii=False)

    raw = "Agent Memory Routing"
    s1 = station_1_extract(raw)
    s2 = station_2_outline(s1)
    s3 = station_3_brief(s2)
    print(f"输入: {raw!r}")
    print(f"站1 抽词  -> {s1}")
    print(f"站2 大纲  -> {s2[:76]}...")
    print(f"站3 简报  -> {s3}")
    assert json.loads(s3)["trends"][0]["trend_name"] == "agent"
    print(">> PASS：三站 JSON 契约接力，输出可断言（确定性流水线的好处）\n")

# ============ 模式 2：Routing 路由（Ch2） ============
# 分类器在前面分诊，专科工位各自处理。对照 LangGraph 条件边。

def pattern_2_routing():
    print("=" * 62)
    print("模式2 Routing 路由：客服工单分诊")
    print("=" * 62)
    routes = {
        "billing": "计费专员：查账单、退差额，话术=安抚+截图凭证",
        "tech":    "技术专员：跑诊断脚本，话术=复现步骤+版本号",
        "sales":   "销售顾问：发报价单，话术=案例+试用链接",
    }

    def classify(ticket: str) -> str:
        """路由器：规则分类器（书中为 LLM 分类，这里规则版确定性）"""
        if any(w in ticket for w in ["发票", "退款", "账单", "扣费"]):
            return "billing"
        if any(w in ticket for w in ["报错", "崩溃", "闪退", "bug"]):
            return "tech"
        return "sales"

    tickets = ["我上个月被重复扣费了，要求退款", "App 打开就闪退，什么情况",
               "你们企业版多少钱，有案例吗"]
    for t in tickets:
        cat = classify(t)
        print(f"工单 {t!r:34s} -> [{cat}] {routes[cat]}")
    assert classify(tickets[0]) == "billing" and classify(tickets[2]) == "sales"
    print(">> PASS：先分诊后专科，每个工单只走一条路由（省 token 且可测）\n")

# ============ 模式 3：Parallelization 并行化（Ch3） ============
# 三种形态之一：Governing（并行 Critic + 总裁合成）。ThreadPoolExecutor 真并发。

def pattern_3_parallelization():
    print("=" * 62)
    print("模式3 Parallelization 并行化：三方 Critic + 总裁合成")
    print("=" * 62)
    doc = "我们产品本月新增用户 5 万，投诉率降为 0，所有用户都爱我们。"

    critics = {
        "事实核查": lambda d: " critic(事实): 投诉率为0不可信，需数据来源" if "0" in d else "ok",
        "文风审查": lambda d: " critic(文风): '所有用户都爱'是绝对化表述，建议改'多数好评'",
        "安全审查": lambda d: " critic(安全): 无敏感内容，放行",
    }

    def run(name, fn):
        return name, fn(doc)   # 三个 critic 互不依赖，天然可并行

    with ThreadPoolExecutor(max_workers=3) as ex:
        results = list(ex.map(lambda kv: run(*kv), critics.items()))

    print(f"原文: {doc}")
    for name, note in results:
        print(f"  [{name}]{note}")
    merged = "总裁合成: 事实需补来源；文风去绝对化；安全放行。"
    print(f"  {merged}")
    assert len(results) == 3
    print(">> PASS：三个独立视角同时跑，总裁一次合成（书中 Governing 形态）\n")

# ============ 模式 4：Reflection 反思循环（Ch4） ============
# 生成→批评→修订循环，带两大停止条件：分数达标 early-stop / 最大轮数保险丝。

def pattern_4_reflection():
    print("=" * 62)
    print("模式4 Reflection 反思循环：文案逐轮打磨")
    print("=" * 62)
    DRAFTS = ["这个产品很好用。",                       # 轮1：无数据
              "这个产品很好用，效率提升50%。",            # 轮2：有数据无来源
              "据用户调研(n=1200)，效率提升50%。"]        # 轮3：数据+来源
    SCORES = [4, 7, 9]   # FakeLLM 的确定性评分

    def generate(round_no: int) -> str:
        return DRAFTS[round_no]

    def critique(text: str) -> tuple:
        """返回 (分数, 意见)。书中为 LLM 当批评家。"""
        i = DRAFTS.index(text)
        reasons = {4: "缺量化数据", 7: "数据无来源", 9: "合格"}
        return SCORES[i], reasons[SCORES[i]]

    MAX_ROUNDS, THRESHOLD = 5, 8
    text, hist = "", []
    for r in range(MAX_ROUNDS):
        text = generate(r)
        score, note = critique(text)
        hist.append((r + 1, score, note))
        print(f"  轮{r+1}: {text!r} -> 分数 {score}（{note}）")
        if score >= THRESHOLD:
            print(f">> PASS：第{r+1}轮达标提前停（early-stop，省下 {MAX_ROUNDS-r-1} 轮调用）")
            break
    else:
        print(">> 达到最大轮数保险丝，取当前最优")
    assert hist[-1][1] >= THRESHOLD
    print(">> 两道停止条件（阈值 early-stop + 最大轮数保险丝）缺一不可：前者省调用，后者防无限循环烧钱\n")

# ============ 模式 5：Guardrails 护栏（Ch18） ============
# Pydantic schema 硬门：LLM 输出先过类型校验，坏输出打回重试。
# 对照书中 Appendix Pydantic 与 Ch18 "validate tool"。

class ToolCall(BaseModel):
    """Agent 想调用工具时必须产出的 JSON 契约"""
    tool: str = Field(pattern="^(search|calc|send_email)$")   # 白名单
    args: dict
    confidence: float = Field(ge=0.0, le=1.0)                  # 置信度封顶 1.0

def pattern_5_guardrails():
    print("=" * 62)
    print("模式5 Guardrails 护栏：Pydantic 协议门 + 打回重试")
    print("=" * 62)
    attempts = [
        {"tool": "delete_db", "args": {}, "confidence": 0.9},      # 越权工具名
        {"tool": "search", "args": {"q": "gdp"}, "confidence": 1.7},# 置信度越界
        {"tool": "calc", "args": {"expr": "1+1"}, "confidence": 0.95},
    ]
    ok = False
    for i, raw in enumerate(attempts, 1):
        try:
            call = ToolCall.model_validate(raw)
            print(f"  第{i}次 {raw} -> ✅ 放行: {call.tool}({call.args})")
            ok = True
            break
        except ValidationError as e:
            first = str(e.errors()[0]["msg"])
            print(f"  第{i}次 {raw} -> ⛔ 协议门拒收（{first}），带错误信息打回重试")
    assert ok
    print(">> PASS：坏输出进不了执行层；拒收理由回流 = 反思循环的素材（Ch4×Ch18 组合拳）\n")

if __name__ == "__main__":
    pattern_1_prompt_chaining()
    pattern_2_routing()
    pattern_3_parallelization()
    pattern_4_reflection()
    pattern_5_guardrails()
    print("ALL 5 PATTERNS PASSED — 确定性 FakeLLM，可重复运行结果一致")
