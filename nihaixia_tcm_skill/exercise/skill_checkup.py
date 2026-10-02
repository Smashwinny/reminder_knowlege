# -*- coding: utf-8 -*-
"""
实验：把中医 Agent Skill 当工程对象做"体检"（纯技术验证，不涉及医疗评价）
体检项：
  1. frontmatter 合规性（name/description/触发词，模拟 Claude Code 加载器解析）
  2. 结构盘点（README 宣称规模 vs 实际文件）
  3. SKILL.md 引用路径完整性（分层加载会不会踩空）
  4. 关键词检索功能测试（按需检索是否可用）
  5. token 估算（触发成本 vs 全量成本）
用法：python skill_checkup.py <repo路径>
"""
import re, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
repo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent / "repo"
skill = repo / "SKILL.md"
text = skill.read_text(encoding="utf-8")

def hr(title):
    print(f"\n{'='*56}\n[{title}]\n{'='*56}")

# ---------- 1. frontmatter ----------
hr("1. frontmatter 合规性（模拟加载器）")
m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
assert m, "FAIL: 没有 frontmatter"
fm = m.group(1)
name_m = re.search(r"^name:\s*(.+)$", fm, re.M)
desc_m = re.search(r"^description:\s*(.+)$", fm, re.M)
name = name_m.group(1).strip()
desc = desc_m.group(1).strip()
print(f"name        = {name}")
print(f"description 长度 = {len(desc)} 字符")
print(f"name 合规(小写连字符): {'PASS' if re.fullmatch(r'[a-z0-9-]+', name) else 'FAIL'}")
print(f"description 非空: {'PASS' if len(desc) > 20 else 'FAIL'}")

triggers = ["倪海厦", "海厦视角", "倪师", "经方思维"]
hit = [t for t in triggers if t in desc]
print(f"触发词在 description 中: {hit} -> {'PASS' if hit else 'WARN'}")

# ---------- 2. 结构盘点 ----------
hr("2. 结构盘点（README 宣称 vs 实际）")
checks = [
    ("modules/ 知识模块 14 个", sorted((repo/"modules").glob("*.md")), 14),
    ("cases/ 医案文件 7 个", sorted((repo/"cases").glob("*.md")), 7),
    ("references/distilled/ 速查 8 个", sorted((repo/"references"/"distilled").glob("*.md")), 8),
]
for label, files, expect in checks:
    status = "PASS" if len(files) == expect else f"实际 {len(files)}"
    print(f"{label}: {status}")
    for f in files[:3]:
        print(f"   e.g. {f.name}")
total_md = len(list(repo.rglob("*.md")))
total_mb = sum(f.stat().st_size for f in repo.rglob("*.md")) / 1e6
print(f"全仓 .md 文件数 = {total_md}，总大小 = {total_mb:.1f} MB")

# 宣称的知识条目抽查
spot = ["小建中汤", "炙甘草汤", "小柴胡汤", "真寒假热", "开阖枢"]
for kw in spot:
    n = text.count(kw)
    print(f"SKILL.md 内出现 '{kw}': {n} 次 {'PASS' if n>0 else 'FAIL'}")

# ---------- 3. 引用路径完整性 ----------
hr("3. SKILL.md 引用路径完整性（分层加载不踩空）")
ref_paths = set(re.findall(r"(?:modules|cases|references)/[\w\-./]+\.(?:md|txt)", text))
ok = bad = 0
for p in sorted(ref_paths):
    if (repo / p).exists():
        ok += 1
    else:
        bad += 1
        print(f"  MISSING: {p}")
print(f"SKILL.md 引用文件路径 {len(ref_paths)} 个，存在 {ok}，缺失 {bad} -> {'PASS' if bad==0 else 'FAIL'}")

# ---------- 4. 检索功能 ----------
hr("4. 关键词检索功能测试（模拟按需检索）")
queries = {
    "小柴胡汤": ["SKILL.md"] + [str(p.relative_to(repo)) for p in (repo/"modules").glob("*.md")] + [str(p.relative_to(repo)) for p in (repo/"cases").glob("*.md")],
    "真寒假热": ["SKILL.md"],
    "炙甘草汤": ["SKILL.md"],
}
for kw, files in queries.items():
    hits = []
    for rel in files:
        try:
            c = (repo/rel).read_text(encoding="utf-8").count(kw)
        except Exception:
            c = 0
        if c:
            hits.append((rel, c))
    hits.sort(key=lambda x: -x[1])
    print(f"\n查询 '{kw}' 命中 {len(hits)} 个文件，Top3:")
    for rel, c in hits[:3]:
        print(f"   {rel}: {c} 次")
    # 抽一条命中行证明可溯源
    if hits:
        target = repo / hits[0][0]
        for line in target.read_text(encoding="utf-8").splitlines():
            if kw in line:
                print(f"   溯源示例[{hits[0][0]}]: {line.strip()[:80]}")
                break

# ---------- 5. token 估算 ----------
hr("5. token 估算（触发成本 vs 全量）")
skill_chars = len(text)
all_chars = sum(len(f.read_text(encoding="utf-8", errors="ignore")) for f in repo.rglob("*.md"))
# 中文粗略 1 字≈1 token（混合文本 0.6~1.2），取 1.0 上界与 0.6 下界
print(f"SKILL.md 字符数 = {skill_chars:,}  ≈ {skill_chars*0.6/1000:.1f}k ~ {skill_chars/1000:.1f}k tokens（加载入口层）")
print(f"全库字符数     = {all_chars:,}  ≈ {all_chars*0.6/1e4:.0f}万 ~ {all_chars/1e4:.0f}万 tokens（不可能全塞上下文）")
print(f"=> 必须分层按需加载，入口层约占全库 {skill_chars/all_chars*100:.2f}%")

print("\n体检完成。")
