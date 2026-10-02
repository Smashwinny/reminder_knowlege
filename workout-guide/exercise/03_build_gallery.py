# -*- coding: utf-8 -*-
"""实验4：从 manifest.json 生成零依赖"302 动作图鉴浏览器"静态页
- 读取 repo 的 manifest，产出 exercise/exercise_gallery.html
- 资产用同目录 assets_svg/<slug>/frame-1..3.svg（矢量，2.3MB）
- 按主肌群/器械筛选；每张卡片 CSS 三帧步进动画（帧1→2→3→2 循环，模拟起-中-止）
运行：python 03_build_gallery.py
"""
import json, os
from collections import Counter

BASE = os.path.join(os.path.dirname(__file__), "..", "repo", "packages", "workout-guide")
manifest = json.load(open(os.path.join(BASE, "manifest.json"), encoding="utf-8"))

muscles = sorted({e["primaryMuscle"] for e in manifest})
equip = sorted({e["equipment"] for e in manifest})
CN = {"Chest": "胸", "Back": "背", "Shoulders": "肩", "Biceps": "二头", "Triceps": "三头",
      "Quads": "股四头", "Hamstrings": "腘绳", "Glutes": "臀", "Core": "核心", "Calves": "小腿",
      "Full Body": "全身", "Neck": "颈", "Forearms": "前臂", "Hip Flexors": "髋屈肌",
      "Cardio": "心肺", "Full body": "全身"}
def cn(s): return CN.get(s, s)

cards = []
for e in manifest:
    slug = e["slug"]
    base = f"assets_svg/{slug}/frame-{{f}}.svg"
    cards.append(f'''<div class="card" data-muscle="{e["primaryMuscle"]}" data-equip="{e["equipment"]}">
  <div class="anim"><img src="{base.format(f=1)}" alt="{e["name"]}"><img src="{base.format(f=2)}" alt=""><img src="{base.format(f=3)}" alt=""></div>
  <div class="name">{e["name"]}</div>
  <div class="tags"><span class="t1">{cn(e["primaryMuscle"])}</span><span class="t2">{e["equipment"]}</span><span class="t3">{e["exerciseType"]}</span></div>
</div>''')

html = """<!doctype html>
<html lang="zh"><head><meta charset="utf-8">
<title>302 动作图鉴浏览器 · workout-guide 实验</title>
<style>
:root{--p:#ff4d3a;--s:#ffb800;--g:#00c46a;--b:#2467ff;--ink:#16181d;--bg:#fff9f0}
*{box-sizing:border-box;margin:0}
body{font-family:"Segoe UI",system-ui,sans-serif;background:var(--bg);color:var(--ink);padding:24px}
h1{color:var(--p);font-size:28px}h1 small{color:var(--b);font-size:14px}
.bar{margin:14px 0;position:sticky;top:0;background:var(--bg);padding:8px 0;z-index:9}
select{margin-right:10px;padding:8px 12px;border:2px solid var(--b);border-radius:10px;font-size:14px;background:#fff}
#cnt{font-weight:700;color:var(--g)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px}
.card{background:#fff;border:2px solid #ffe0c2;border-radius:14px;padding:10px;break-inside:avoid}
.card:hover{border-color:var(--p)}
.anim{position:relative;width:100%;aspect-ratio:1;background:#181b22;border-radius:10px}
.anim img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;opacity:0}
.anim img:first-child{opacity:1}
@media (prefers-reduced-motion:no-preference){
.card:hover .anim img{animation:cyc 1.05s steps(1) infinite}
}
@keyframes cyc{0%{opacity:1}33%{opacity:0}40%{opacity:0}0%{opacity:0}}
.anim img:nth-child(1){animation:none}
@keyframes f1{0%,32%{opacity:1}33%,100%{opacity:0}}
@keyframes f2{0%,32%{opacity:0}33%,65%{opacity:1}66%,100%{opacity:0}}
@keyframes f3{0%,65%{opacity:0}66%,99%{opacity:1}100%{opacity:0}}
.card:hover .anim img:nth-child(1){animation:f1 1.2s steps(1) infinite}
.card:hover .anim img:nth-child(2){animation:f2 1.2s steps(1) infinite}
.card:hover .anim img:nth-child(3){animation:f3 1.2s steps(1) infinite}
.name{font-size:13px;font-weight:700;margin:6px 0 4px;min-height:2.4em}
.tags span{font-size:10px;padding:2px 7px;border-radius:99px;margin-right:4px;color:#fff;font-weight:700}
.t1{background:var(--p)}.t2{background:var(--b)}.t3{background:var(--g)}
</style></head><body>
<h1>🏋️ 302 动作图鉴 <small>bryllim/workout-guide · 本地 SVG 三帧起-中-止动画 · 悬停卡片播放</small></h1>
<div class="bar">
<select id="fm"><option value="">全部主肌群（__M__）</option>__FM__</select>
<select id="fe"><option value="">全部器械（__E__）</option>__FE__</select>
显示 <span id="cnt"></span> 个动作
</div>
<div class="grid">__CARDS__</div>
<script>
const cards=[...document.querySelectorAll('.card')];
function apply(){
  const m=fm.value,eq=fe.value;let n=0;
  cards.forEach(c=>{const ok=(!m||c.dataset.muscle===m)&&(!eq||c.dataset.equip===eq);
    c.style.display=ok?'':'none';if(ok)n++;});
  cnt.textContent=n;
}
fm.onchange=fe.onchange=apply;apply();
</script></body></html>"""
fm = "".join(f'<option value="{m}">{cn(m)} {m}</option>' for m in muscles)
fe = "".join(f'<option value="{x}">{x}</option>' for x in equip)
out = (html.replace("__M__", str(len(muscles))).replace("__E__", str(len(equip)))
       .replace("__FM__", fm).replace("__FE__", fe).replace("__CARDS__", "\n".join(cards)))
dst = os.path.join(os.path.dirname(__file__), "exercise_gallery.html")
open(dst, "w", encoding="utf-8").write(out)
print("生成:", dst, f"{os.path.getsize(dst)/1024:.0f} KB")
print("卡片数:", len(cards), "| 肌群:", len(muscles), "| 器械:", len(equip))
