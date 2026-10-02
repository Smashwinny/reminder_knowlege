# -*- coding: utf-8 -*-
"""实验1：解析全部 DESIGN.md，验证"纯文本规范=机器可读 token 源"的声称。
输出：tokens_summary.json（每站点的 token 统计）+ 控制台汇总表。
零依赖：只用标准库（yaml 部分手写极简解析 frontmatter 不现实 → 用正则提取关键 token）。
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent / "repo" / "design-md"
OUT = pathlib.Path(__file__).resolve().parent / "tokens_summary.json"

def parse(path: pathlib.Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return None
    fm = m.group(1)
    colors = re.findall(r'^\s{2}([a-z0-9\-]+):\s*"(#[0-9a-fA-F]{3,8})"', fm, re.M)
    fonts = sorted(set(re.findall(r'fontFamily:\s*([^\n]+)', fm)))
    tm = re.search(r'^typography:\s*\n(.*?)(?=^\S|\Z)', fm, re.S | re.M)
    type_keys = re.findall(r'^ {2}([a-z0-9\-]+):\s*$', tm.group(1), re.M) if tm else []
    return {
        "site": path.parent.name,
        "name": (re.search(r'^name:\s*(.+)$', fm, re.M) or [None, "?"])[1].strip(),
        "hex_colors": len(colors),
        "sample_colors": [c for _, c in colors[:5]],
        "primary": (re.search(r'^\s{2}primary:\s*"(#[0-9a-fA-F]{3,8})"', fm, re.M) or [None, None])[1],
        "fonts": fonts,
        "type_scale_keys": len(type_keys),
        "markdown_lines": len(text.splitlines()),
    }

def main():
    results, failed = [], []
    for p in sorted(ROOT.iterdir()):
        dm = p / "DESIGN.md"
        if not dm.exists():
            continue
        r = parse(dm)
        if r:
            results.append(r)
        else:
            failed.append(p.name)
    ok = len(results)
    total = ok + len(failed)
    print(f"DESIGN.md 总数: {total}")
    print(f"frontmatter 解析成功: {ok} ({ok/total:.0%})")
    print(f"解析失败: {failed if failed else '无'}")
    print(f"全库十六进制色值 token 总数: {sum(r['hex_colors'] for r in results)}")
    print(f"全库字体家族种类: {sorted(set(f for r in results for f in r['fonts']))[:20]}")
    print(f"平均每套字号层级数: {sum(r['type_scale_keys'] for r in results)/ok:.1f}")
    print("\n抽样 8 站点（站点 / primary / 色值数 / 字体数 / 字号层级 / 行数）:")
    for r in [results[i] for i in range(0, ok, max(1, ok//8))][:8]:
        print(f"  {r['site']:<14} {str(r['primary']):<9} {r['hex_colors']:>3} 色  {len(r['fonts'])} 字体  {r['type_scale_keys']:>2} 层  {r['markdown_lines']} 行")
    OUT.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n已写出 {OUT.name}（{len(results)} 条）")

if __name__ == "__main__":
    sys.exit(main())
