# ex3 生成可打开的动效 demo 页（stagger 卡片入场），并做结构验收（零依赖）
import ex1_lexicon as L

css_b = L.generate({"selector": ".list .card", "primitive": "slide-up",
                    "easing": "ease-out", "duration_ms": 300,
                    "stagger_ms": 60, "count": 5})
html = f"""<!doctype html><html lang="zh"><head><meta charset="utf-8">
<title>动效描述 demo：5 卡片错峰入场</title>
<style>
body {{ font-family: system-ui, sans-serif; background: #FFF3E0; padding: 32px; }}
h1 {{ color: #E65100; }}
.list {{ display: flex; flex-direction: column; gap: 14px; max-width: 480px; }}
.card {{ background: #FF7043; color: #fff; padding: 20px; border-radius: 14px; font-size: 18px; font-weight: bold;
        box-shadow: 0 4px 14px rgba(230,81,0,.35); }}
{css_b}
button {{ margin-bottom: 20px; padding: 10px 22px; font-size: 16px; background: #00897B; color: #fff;
         border: none; border-radius: 8px; cursor: pointer; }}
</style></head><body>
<h1>动效描述词表 demo — 5 张卡片错峰入场（slide-up + ease-out + 300ms + stagger 60ms）</h1>
<button onclick="document.querySelectorAll('.card').forEach(c=>c.classList.toggle('enter'))">重播 / 隐藏</button>
<div class="list">
  <div class="card enter">1. 触发 trigger：页面加载 / 按钮点击</div>
  <div class="card enter">2. 对象 property：opacity + translateY</div>
  <div class="card enter">3. 缓动 easing：ease-out（快进慢出）</div>
  <div class="card enter">4. 时序 timing：300ms + stagger 60ms</div>
  <div class="card enter">5. 结构化描述 = AI 能精确执行的合同</div>
</div></body></html>"""
open("ex3_demo.html", "w", encoding="utf-8").write(html)

# 结构验收：不用浏览器也能检查的关键证据
content = open("ex3_demo.html", encoding="utf-8").read()
checks = {
    "含缓动 cubic-bezier(0, 0, 0.2, 1)": "cubic-bezier(0, 0, 0.2, 1)" in content,
    "含 duration 300ms":                  "300ms" in content,
    "含 4 级错峰 delay 60/120/180/240":    all(f"transition-delay: {d}ms" in content for d in (60, 120, 180, 240)),
    "含初始态 translateY(24px)":           "translateY(24px)" in content,
    "卡片有 .enter 结束态":                content.count("enter") >= 6,
}
for k, v in checks.items():
    print(("PASS " if v else "FAIL ") + k)
assert all(checks.values()), "验收未全过"
print(f"[OK] ex3_demo.html 已生成（{len(content)} 字节），5/5 结构验收全过")
