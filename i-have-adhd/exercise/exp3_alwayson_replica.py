# -*- coding: utf-8 -*-
"""exp3: always-on SessionStart hook 的 Python 等价复刻 + 边界夹具。

上游 hooks/always-on.mjs 的逻辑只有三步：
  1) 旗标文件 $CLAUDE_CONFIG_DIR/.i-have-adhd-always 存在才干活（默认静默 exit 0）
  2) 读 skills/i-have-adhd/SKILL.md，剥掉开头 YAML frontmatter
  3) stdout 输出「ADHD MODE ACTIVE ... + 规则全文」，任何异常都 exit 0 不阻塞会话

本脚本用 Python 复刻 2)+3)，用自造夹具验证边界；上游 .mjs 因安全策略未直接执行
（[Code from External] 拦截），以源码逐行对照为准。
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent / "repo"
SKILL_PATH = REPO / "skills" / "i-have-adhd" / "SKILL.md"

# 上游正则（逐字移植自 always-on.mjs）：
#   /^---[^\S\r\n]*\r?\n[\s\S]*?\r?\n---[^\S\r\n]*(?:\r?\n|$)/  再去尾部空行
FM_RE = re.compile(r"^---[^\S\r\n]*\r?\n[\s\S]*?\r?\n---[^\S\r\n]*(?:\r?\n|$)")
TRAIL_NL = re.compile(r"(?:\r?\n)+$")

HEADER = (
    "ADHD MODE ACTIVE (always-on). The ruleset below applies to every response. "
    '"stop adhd mode" turns it off for this session; '
    "delete {flag} to turn always-on off for good.\n\n"
)


def replica(skill_text: str, flag_path: str):
    """返回 hook 应输出到 stdout 的字符串；旗标不存在时返回 None（exit 0 无输出）。"""
    if not flag_path:  # 旗标不存在 → 上游 process.exit(0)
        return None
    body = FM_RE.sub("", skill_text, count=1)
    body = TRAIL_NL.sub("", body)
    return HEADER.format(flag=flag_path) + body + "\n"


results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))


text = SKILL_PATH.read_text(encoding="utf-8")

# --- 主路径：真实 SKILL.md ---
out = replica(text, "C:/fake/.i-have-adhd-always")
check("旗标存在时输出非空", out and len(out) > 3000, f"{len(out) if out else 0} 字符")
check("输出以 ADHD MODE ACTIVE 开头", out.startswith("ADHD MODE ACTIVE (always-on)"))
check("frontmatter 已剥净（无 name:/disable-model-invocation）",
      "disable-model-invocation" not in out and not out.split("\n", 1)[1].startswith("---"))
check("规则正文保留（10. No preamble 在）", "No preamble, no recap" in out)
content_lines = [ln for ln in out.strip().splitlines() if ln.strip()]
check("正文标题 # i-have-adhd 是第一个内容行",
      content_lines[1] == "# i-have-adhd", content_lines[1])

# --- 边界夹具 ---
cases = [
    ("CRLF frontmatter", "---\r\nname: x\r\n---\r\nBODY\r\n", True, "BODY"),
    ("无 frontmatter 纯正文", "BODY\n", True, "BODY"),
    ("正文里出现 --- 分隔线（不误删）", "---\nname: x\n---\nA\n---\nB\n", True, "A\n---\nB"),
    ("只有 frontmatter 没正文", "---\nname: x\n---\n", True, ""),
]
for name, fixture, flag, want in cases:
    o = replica(fixture, "C:/fake/.flag" if flag else None)
    if not flag:
        check(f"夹具[{name}] 旗标缺失→无输出", o is None)
    else:
        got = (o.split("\n\n", 1)[1].rstrip("\n")) if o else None
        check(f"夹具[{name}] 剥离结果正确", got == want, f"got={got!r}")

# 旗标缺失主路径
check("真实 SKILL + 无旗标 → None", replica(text, None) is None)

ok = sum(1 for _, o, _ in results if o)
print(f"always-on hook 复刻体检: {ok}/{len(results)} PASS\n")
for name, o, detail in results:
    print(f"{'PASS' if o else 'FAIL'}  {name}" + (f"  [{detail}]" if detail and not o else ""))
sys.exit(0 if ok == len(results) else 1)
