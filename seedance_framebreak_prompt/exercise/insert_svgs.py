# -*- coding: utf-8 -*-
"""为 seedance guide 的 Q2-Q10 补插内联 SVG（SVG 自检发现缺失）。"""
import re
from pathlib import Path

p = Path("F:/reminder/seedance_framebreak_prompt/seedance_framebreak_prompt-guide.html")
html = p.read_text(encoding="utf-8")

S = {}

S["q2"] = '''<div class="svgbox">
<svg width="640" height="185" viewBox="0 0 640 185">
  <g font-size="10" text-anchor="middle">
  <rect x="25" y="15" width="250" height="26" rx="7" fill="#ede9fe" stroke="#9333ea"/><text x="150" y="32" fill="#7e22ce" font-weight="bold">① 角色锚定层 Use @[char ref] + Preserve…</text>
  <rect x="25" y="47" width="250" height="26" rx="7" fill="#dbeafe" stroke="#2563eb"/><text x="150" y="64" fill="#1e40af" font-weight="bold">② 视觉目标层 MAIN VISUAL GOAL…</text>
  <rect x="25" y="79" width="250" height="26" rx="7" fill="#dcfce7" stroke="#16a34a"/><text x="150" y="96" fill="#166534" font-weight="bold">③ 合成顺序层 COMPOSITING ORDER…</text>
  <rect x="25" y="111" width="250" height="26" rx="7" fill="#fef3c7" stroke="#f59e0b"/><text x="150" y="128" fill="#92400e" font-weight="bold">④ 物理约束层 Keep bars equal and fixed…</text>
  <rect x="25" y="143" width="250" height="26" rx="7" fill="#fee2e2" stroke="#dc2626"/><text x="150" y="160" fill="#b91c1c" font-weight="bold">⑤ 节拍层 OPENING…</text>
  <path d="M275 95 L 330 95" stroke="#9333ea" stroke-width="3" marker-end="url(#sd2)"/>
  <defs><marker id="sd2" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#9333ea"/></marker></defs>
  <rect x="335" y="40" width="130" height="105" rx="12" fill="#9333ea"/>
  <text x="400" y="70" fill="#fff" font-weight="bold" font-size="11">Seedance 2.5</text>
  <text x="400" y="90" fill="#f3e8ff" font-size="9">按层消费：</text>
  <text x="400" y="105" fill="#f3e8ff" font-size="9">各层各管一件事</text>
  <text x="400" y="125" fill="#f3e8ff" font-size="9">3700/8250 字符</text>
  <rect x="480" y="55" width="140" height="70" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="550" y="82" fill="#166534" font-weight="bold" font-size="10.5">= 分镜规格书</text>
  <text x="550" y="100" fill="#166534" font-size="9">导演+摄影+合成</text>
  <text x="550" y="115" fill="#166534" font-size="9">三岗合一</text>
  </g>
</svg>
</div>'''

S["q3"] = '''<div class="svgbox">
<svg width="640" height="160" viewBox="0 0 640 160">
  <g font-size="10" text-anchor="middle">
  <rect x="60" y="15" width="360" height="130" fill="#111"/>
  <rect x="60" y="35" width="360" height="90" fill="#87ceeb"/>
  <rect x="60" y="15" width="360" height="20" fill="#111"/>
  <rect x="60" y="125" width="360" height="20" fill="#111"/>
  <rect x="150" y="45" width="180" height="70" fill="#c8e6c9"/>
  <text x="240" y="80" fill="#33691e" font-size="9">背景锁定在中央窗口</text>
  <circle cx="330" cy="62" r="16" fill="#f0c8a0"/>
  <path d="M314 78 L 346 78 L 352 125 L 308 125 Z" fill="#e05555"/>
  <path d="M344 66 L 415 40 L 421 47 L 350 74 Z" fill="#c0c8d0"/>
  <text x="505" y="35" fill="#7e22ce" font-weight="bold" font-size="10" text-anchor="start">COMPOSITING ORDER</text>
  <text x="505" y="55" fill="#7e22ce" font-size="10" text-anchor="start">BACK TO FRONT:</text>
  <text x="505" y="78" fill="#166534" font-size="10" text-anchor="start">③ 前景角色（最上）</text>
  <text x="505" y="98" fill="#92400e" font-size="10" text-anchor="start">② 黑边（被角色压住）</text>
  <text x="505" y="118" fill="#1e40af" font-size="10" text-anchor="start">① 背景（窗口内）</text>
  <text x="505" y="140" fill="#b91c1c" font-size="9" text-anchor="start">顺序错=效果崩</text>
  </g>
</svg>
</div>'''

S["q4"] = '''<div class="svgbox">
<svg width="640" height="130" viewBox="0 0 640 130">
  <g font-size="10" text-anchor="middle">
  <rect x="18" y="18" width="185" height="95" rx="10" fill="#fff7ed" stroke="#ea580c" stroke-width="2"/>
  <text x="110" y="42" fill="#c2410c" font-weight="bold" font-size="10.5">① 黑边尺寸模型自决</text>
  <text x="110" y="60" fill="#c2410c" font-size="9">指定百分比各代仍漂移</text>
  <text x="110" y="78" fill="#c2410c" font-size="9">布局参数不是硬约束</text>
  <rect x="213" y="18" width="185" height="95" rx="10" fill="#fff7ed" stroke="#ea580c" stroke-width="2"/>
  <text x="305" y="42" fill="#c2410c" font-weight="bold" font-size="10.5">② 运镜破坏黑边</text>
  <text x="305" y="60" fill="#c2410c" font-size="9">镜头一动黑边移位/变形</text>
  <text x="305" y="78" fill="#c2410c" font-size="9">效果与运镜冲突</text>
  <rect x="408" y="18" width="215" height="95" rx="10" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="515" y="42" fill="#b91c1c" font-weight="bold" font-size="10.5">③ 约束竞争（金句）</text>
  <text x="515" y="60" fill="#b91c1c" font-size="9">越强调黑边固定</text>
  <text x="515" y="78" fill="#b91c1c" font-size="9">越可能破坏弹出效果</text>
  <text x="515" y="96" fill="#991b1b" font-size="9">约束过强会杀死目标</text>
  <rect x="18" y="100" width="605" height="24" rx="12" fill="#fef3c7" stroke="#f59e0b"/>
  <text x="320" y="116" fill="#92400e" font-size="10" font-weight="bold">④ 代差门槛：2.0 尝试未达预期，2.5 成功——同提示词跨模型代不可迁移</text>
  </g>
</svg>
</div>'''

S["q5"] = '''<div class="svgbox">
<svg width="640" height="130" viewBox="0 0 640 130">
  <g font-size="10" text-anchor="middle">
  <text x="320" y="20" fill="#7e22ce" font-weight="bold" font-size="11">两支提示词长度构成（均值 5975 字符）</text>
  <rect x="70" y="35" width="75" height="26" fill="#ede9fe" stroke="#9333ea"/>
  <rect x="145" y="35" width="113" height="26" fill="#dbeafe" stroke="#2563eb"/>
  <rect x="258" y="35" width="150" height="26" fill="#dcfce7" stroke="#16a34a"/>
  <rect x="408" y="35" width="37" height="26" fill="#fef3c7" stroke="#f59e0b"/>
  <text x="107" y="52" fill="#7e22ce" font-size="9">角色清单20%</text>
  <text x="200" y="52" fill="#1e40af" font-size="9">z轴+黑边约束30%</text>
  <text x="333" y="52" fill="#166534" font-size="9">动作节拍分镜40%</text>
  <text x="426" y="52" fill="#92400e" font-size="9">画风10%</text>
  <rect x="60" y="80" width="520" height="30" rx="8" fill="#f3e8ff" stroke="#9333ea"/>
  <text x="320" y="99" fill="#7e22ce" font-size="10" font-weight="bold">不是话多——是把导演/摄影/合成三岗工作单合并成模型可执行规格书</text>
  </g>
</svg>
</div>'''

S["q6"] = '''<div class="svgbox">
<svg width="640" height="120" viewBox="0 0 640 120">
  <g font-size="10" text-anchor="middle">
  <rect x="20" y="25" width="280" height="70" rx="10" fill="#f0fdfa" stroke="#0f766e" stroke-width="2"/>
  <text x="160" y="50" fill="#115e59" font-weight="bold" font-size="11">Harness 论文 §7.3（文本 Agent）</text>
  <text x="160" y="70" fill="#0f766e" font-size="9">persona 宣言 · 禁令句式 · 反镀金指令</text>
  <rect x="340" y="25" width="280" height="70" rx="10" fill="#f5f3ff" stroke="#9333ea" stroke-width="2"/>
  <text x="480" y="50" fill="#7e22ce" font-weight="bold" font-size="11">Koda 提示词（视频模型）</text>
  <text x="480" y="70" fill="#9333ea" font-size="9">MAIN VISUAL GOAL 大写宣言 · NOT confined</text>
  <text x="480" y="86" fill="#9333ea" font-size="9">禁令句式 · do not break 反效果警告</text>
  <text x="320" y="112" fill="#6b7280" font-size="10" font-weight="bold">提示词修辞学在文本 Agent 与视频模型间通用</text>
  </g>
</svg>
</div>'''

S["q7"] = '''<div class="svgbox">
<svg width="640" height="120" viewBox="0 0 640 120">
  <g font-size="10" text-anchor="middle">
  <rect x="18" y="20" width="290" height="80" rx="10" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="163" y="45" fill="#b91c1c" font-weight="bold" font-size="11">未本机复现</text>
  <text x="163" y="65" fill="#b91c1c" font-size="9">Seedance 付费云端模型（作者自述不想烧 credits）</text>
  <text x="163" y="85" fill="#b91c1c" font-size="9">@[char ref] 为平台语法，离开需改写</text>
  <rect x="323" y="20" width="299" height="80" rx="10" fill="#fef3c7" stroke="#f59e0b" stroke-width="2"/>
  <text x="472" y="45" fill="#92400e" font-weight="bold" font-size="11">半可控状态</text>
  <text x="472" y="65" fill="#92400e" font-size="9">黑边控制仍需多次抽卡；第三支提示词</text>
  <text x="472" y="85" fill="#92400e" font-size="9">在更早帖中未收录本存档</text>
  </g>
</svg>
</div>'''

S["q8"] = '''<div class="svgbox">
<svg width="640" height="110" viewBox="0 0 640 110">
  <g font-size="10" text-anchor="middle">
  <rect x="20" y="20" width="150" height="70" rx="10" fill="#f5f3ff" stroke="#9333ea" stroke-width="2"/>
  <text x="95" y="47" fill="#7e22ce" font-weight="bold" font-size="10.5">五层骨架</text>
  <text x="95" y="65" fill="#9333ea" font-size="9">不依赖 Seedance</text>
  <text x="95" y="80" fill="#9333ea" font-size="9">Veo/即梦/Kling 可套用</text>
  <rect x="190" y="20" width="150" height="70" rx="10" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/>
  <text x="265" y="47" fill="#1e40af" font-weight="bold" font-size="10.5">约束竞争</text>
  <text x="265" y="65" fill="#2563eb" font-size="9">LLM 工具调用同样存在</text>
  <text x="265" y="80" fill="#2563eb" font-size="9">强格式约束损推理</text>
  <rect x="360" y="20" width="130" height="70" rx="10" fill="#fef9c3" stroke="#ca8a04" stroke-width="2"/>
  <text x="425" y="47" fill="#854d0e" font-weight="bold" font-size="10.5">[[图像提示八要素]]</text>
  <text x="425" y="65" fill="#854d0e" font-size="9">静态图像版</text>
  <text x="425" y="80" fill="#854d0e" font-size="9">本条为视频升级</text>
  <rect x="510" y="20" width="110" height="70" rx="10" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>
  <text x="565" y="47" fill="#166534" font-weight="bold" font-size="10.5">[[声明式视频源语言]]</text>
  <text x="565" y="65" fill="#16a34a" font-size="9">提示词→程序</text>
  <text x="565" y="80" fill="#16a34a" font-size="9">同趋势</text>
  </g>
</svg>
</div>'''

S["q9"] = '''<div class="svgbox">
<svg width="640" height="110" viewBox="0 0 640 110">
  <g font-size="10" text-anchor="middle">
  <rect x="18" y="20" width="120" height="70" rx="10" fill="#f5f3ff" stroke="#9333ea"/>
  <text x="78" y="47" fill="#7e22ce" font-weight="bold" font-size="10">五层骨架</text>
  <text x="78" y="65" fill="#9333ea" font-size="9">复杂效果标准格式</text>
  <rect x="152" y="20" width="120" height="70" rx="10" fill="#dcfce7" stroke="#16a34a"/>
  <text x="212" y="47" fill="#166534" font-weight="bold" font-size="10">z轴合成指令</text>
  <text x="212" y="65" fill="#16a34a" font-size="9">back-to-front 三层</text>
  <rect x="286" y="20" width="120" height="70" rx="10" fill="#fee2e2" stroke="#dc2626"/>
  <text x="346" y="47" fill="#b91c1c" font-weight="bold" font-size="10">约束竞争</text>
  <text x="346" y="65" fill="#b91c1c" font-size="9">过强约束杀目标</text>
  <rect x="420" y="20" width="100" height="70" rx="10" fill="#fff7ed" stroke="#ea580c"/>
  <text x="470" y="47" fill="#c2410c" font-weight="bold" font-size="10">代差门槛</text>
  <text x="470" y="65" fill="#c2410c" font-size="9">跨代不可迁移</text>
  <rect x="534" y="20" width="90" height="70" rx="10" fill="#dbeafe" stroke="#2563eb"/>
  <text x="579" y="47" fill="#1e40af" font-weight="bold" font-size="10">破框美学</text>
  <text x="579" y="65" fill="#2563eb" font-size="9">电影语言复用</text>
  </g>
</svg>
</div>'''

S["q10"] = '''<div class="svgbox">
<svg width="640" height="105" viewBox="0 0 640 105">
  <g font-size="10" text-anchor="middle">
  <circle cx="80" cy="28" r="13" fill="#16a34a"/><text x="80" y="33" fill="#fff" font-weight="bold">v</text>
  <text x="80" y="57" fill="#166534" font-size="9">2 支提示词</text>
  <circle cx="200" cy="28" r="13" fill="#16a34a"/><text x="200" y="33" fill="#fff" font-weight="bold">v</text>
  <text x="200" y="57" fill="#166534" font-size="9">五层全命中</text>
  <circle cx="320" cy="28" r="13" fill="#16a34a"/><text x="320" y="33" fill="#fff" font-weight="bold">v</text>
  <text x="320" y="57" fill="#166534" font-size="9">合成三层齐备</text>
  <circle cx="440" cy="28" r="13" fill="#16a34a"/><text x="440" y="33" fill="#fff" font-weight="bold">v</text>
  <text x="440" y="57" fill="#166534" font-size="9">四观察全录</text>
  <circle cx="560" cy="28" r="13" fill="#16a34a"/><text x="560" y="33" fill="#fff" font-weight="bold">v</text>
  <text x="560" y="57" fill="#166534" font-size="9">篇幅>1500字符</text>
  <rect x="140" y="75" width="360" height="24" rx="12" fill="#f3e8ff" stroke="#9333ea"/>
  <text x="320" y="91" fill="#7e22ce" font-weight="bold" font-size="10.5">parse_prompts.py 6/6 exit=0</text>
  </g>
</svg>
</div>'''

for qid, svg in S.items():
    pat = re.compile(r'(<div class="q[^"]*" id="' + qid + r'">\s*\n\s*<h2>.*?</h2>)', re.S)
    html, n = pat.subn(lambda m: m.group(1) + "\n  " + svg, html)
    if n != 1:
        print("WARN", qid, n)

p.write_text(html, encoding="utf-8")
print("inserted", len(S))
