# -*- coding: utf-8 -*-
"""exp2: 「去埋葬」体检器——把 SKILL.md 的 Pre-send check 从提示词翻译成确定性代码。

问题：规则10 + 发送前五删检查是写给 LLM 的软约束，机器能执行多少？
做法：用正则实现五删检查 + 首行行动性启发式，拿 README 官方 Before/After
两个样本做对照（Before 必须被抓、After 必须放行），再加自造正反例各一。
"""
import re

# ---------- 五删检查（对应 SKILL.md Pre-send check 1~5） ----------
OPENERS = [  # 删1：预告自己要做什么的开场
    r"^\s*Great question\b", r"^\s*Let me\b", r"^\s*I'll\b", r"^\s*Sure!?\b",
    r"^\s*Looking at your\b", r"^\s*To answer your question\b",
    r"^\s*Let's think about\b",
]
CLOSERS = [  # 删2：问还要吗/复述刚做了什么
    r"\bLet me know if\b", r"\bHope (this|that) helps\b", r"\bHappy to clarify\b",
    r"\bFeel free to ask\b", r"\banything else\b", r"^\s*I'?ve (now )?(made|done)\b.*\bwhich means\b",
]
SIDEBARS = [r"\b[Bb]y the way\b", r"\b[Aa]s an? aside\b"]           # 删3
HEDGES = [r"\b[Pp]erhaps\b", r"\bmight possibly\b", r"\b[Cc]ould possibly\b",
          r"\byou (?:might|may) want to\b"]                          # 删4
IDIOMS = [r"\bcircle back\b", r"\bget the ball rolling\b",
          r"\bon the same page\b", r"\btouch base\b"]                # 删5

FIRST_ACTION = re.compile(  # 首行行动性启发式：命令/编号/路径/动词祈使
    r"^(\s*\d+\.|Run |Open |Edit |Replace |Delete |Paste |Try |npm |git |python|node |pip )",
    re.I,
)


def lint(reply: str):
    findings = []
    lines = reply.strip().splitlines()
    if lines:
        first = lines[0]
        if any(re.search(p, first) for p in OPENERS):
            findings.append("删1 开场白预告（首行是'我要做什么'不是'你做什么'）")
        elif not FIRST_ACTION.match(first):
            findings.append("首行非行动（启发式：无命令/编号/祈使动词开头）")
    full = reply
    for p in CLOSERS:
        if re.search(p, full):
            findings.append("删2 结尾客套/复盘")
            break
    for p in SIDEBARS:
        if re.search(p, full):
            findings.append("删3 'by the way' 支线插播")
            break
    for p in HEDGES:
        if re.search(p, full):
            findings.append("删4 无信息量对冲词")
            break
    for p in IDIOMS:
        if re.search(p, full):
            findings.append("删5 比喻习语")
            break
    # 规则9：顶层列表 > 5 项且未分组
    top_items = re.findall(r"^\d+\.\s", full, re.M)
    if len(top_items) > 5 and not re.search(r"^\*\*|^#{1,4}\s", full, re.M):
        findings.append(f"规则9 顶层编号列表 {len(top_items)} 项 > 5 未分组")
    return findings


BEFORE = """Great question! Let me think about this. Your auth flow has a few moving pieces: the middleware, the token verification, and the cookie handling. Looking at src/auth.ts, the verifyToken function (around lines 42-58) seems to be using an older jsonwebtoken API. One approach would be to update the package and rewrite that function. After making the change, you'd want to run the auth tests to confirm nothing breaks. By the way, you might also want to look at your dependency versions overall. Hope this helps! Let me know if you want to dig deeper."""

AFTER = """Run `npm install jsonwebtoken@latest`, then edit `src/auth.ts:42`.

1. Open `src/auth.ts`
2. Replace `verifyToken` (lines 42 to 58) with the snippet below
3. Run `npm test -- auth.spec.ts`

Next: paste the first failing line if any test fails."""

SELF_BAD = """Sure! I'll take a look at your config. To answer your question, the issue might possibly be a stale cache — let's circle back to that. As for the rest, I've now made some changes which means things should work. Feel free to ask if anything else comes up!"""

SELF_GOOD = """1. Open `config/cache.ts`
2. Set `ttl: 3600` (was 0)
3. Restart the dev server

About 5 minutes. Next: reload the page and check the response header for `x-cache: HIT`."""


def report(name, text, expect_block):
    f = lint(text)
    verdict = "抓下(FAIL)" if f else "放行(PASS)"
    ok = (not f) == (not expect_block)
    tag = "OK " if ok else "ERR"
    print(f"[{tag}] {name}: {verdict}")
    for x in f:
        print(f"       - {x}")
    return ok


allok = True
allok &= report("README 官方 Before（应被抓）", BEFORE, expect_block=True)
allok &= report("README 官方 After（应放行）", AFTER, expect_block=False)
allok &= report("自造坏回复（应被抓）", SELF_BAD, expect_block=True)
allok &= report("自造好回复（应放行）", SELF_GOOD, expect_block=False)

# 终检句演示：只留首行+末行
print("\n终检句模拟（只读首行+末行）——After 版：")
al = AFTER.strip().splitlines()
print(f"  首行: {al[0]!r}")
print(f"  末行: {al[-1]!r}")
print("  => (a) 下一步: 跑 npm install+编辑  (b) 刚发生: 无隐含叙事，干净")
print("\n总体:", "PASS" if allok else "FAIL")
raise SystemExit(0 if allok else 1)
