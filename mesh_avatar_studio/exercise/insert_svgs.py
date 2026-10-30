# -*- coding: utf-8 -*-
"""为 mesh_avatar guide 的 Q1/Q3-Q5/Q7-Q10 补插入内联 SVG（q2 已有）。"""
import re
from pathlib import Path

p = Path("F:/reminder/mesh_avatar_studio/mesh_avatar_studio-guide.html")
html = p.read_text(encoding="utf-8")

S = {}

S["q1"] = '''<div class="svgbox">
<svg width="640" height="120" viewBox="0 0 640 120">
  <g font-size="10" text-anchor="middle">
  <rect x="20" y="25" width="110" height="70" rx="10" fill="#fdf2f8" stroke="#db2777" stroke-width="2"/>
  <text x="75" y="52" fill="#be185d" font-weight="bold" font-size="11">一张插画</text>
  <text x="75" y="70" fill="#db2777" font-size="9">正面半身透明底 PNG</text>
  <path d="M130 60 L 175 60" stroke="#db2777" stroke-width="3" marker-end="url(#ma1)"/>
  <defs><marker id="ma1" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#db2777"/></marker></defs>
  <rect x="180" y="15" width="170" height="90" rx="12" fill="#db2777"/>
  <text x="265" y="45" fill="#fff" font-weight="bold" font-size="12">Mesh Avatar Studio</text>
  <text x="265" y="67" fill="#fce7f3" font-size="9.5">Agent 备料 + 编辑器微调</text>
  <text x="265" y="85" fill="#fce7f3" font-size="9.5">MIT · 540星 · v0.1.0</text>
  <path d="M350 60 L 395 60" stroke="#db2777" stroke-width="3" marker-end="url(#ma1b)"/>
  <defs><marker id="ma1b" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#db2777"/></marker></defs>
  <rect x="400" y="25" width="220" height="70" rx="10" fill="#fef9c3" stroke="#f59e0b" stroke-width="2"/>
  <text x="510" y="50" fill="#92400e" font-weight="bold" font-size="11">会动的 2D 头像</text>
  <text x="510" y="68" fill="#92400e" font-size="9.5">眨眼 · 说话口型 · 转头 · 呼吸 · 摆发</text>
  <text x="510" y="84" fill="#92400e" font-size="9">VTuber/AI 主播即用</text>
  </g>
</svg>
</div>'''

S["q3"] = '''<div class="svgbox">
<svg width="640" height="140" viewBox="0 0 640 140">
  <g font-size="10" text-anchor="middle">
  <rect x="25" y="20" width="270" height="100" rx="12" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="160" y="45" fill="#166534" font-weight="bold" font-size="12">docs/agent-guide.md（201 行）</text>
  <text x="160" y="68" fill="#166534" font-size="9.5">顺序执行 · 每步带检查</text>
  <text x="160" y="84" fill="#166534" font-size="9.5">"不要跳过检查：质量取决于</text>
  <text x="160" y="98" fill="#166534" font-size="9.5"> 查看自己的输出并修正"</text>
  <text x="160" y="114" fill="#166534" font-size="9.5">projects/ 永不提交</text>
  <path d="M295 70 L 345 70" stroke="#7c3aed" stroke-width="2.5" marker-end="url(#ma3)"/>
  <defs><marker id="ma3" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#7c3aed"/></marker></defs>
  <rect x="350" y="20" width="270" height="100" rx="12" fill="#ede9fe" stroke="#7c3aed" stroke-width="2"/>
  <text x="485" y="45" fill="#5b21b6" font-weight="bold" font-size="12">资质声明制</text>
  <text x="485" y="68" fill="#7c3aed" font-size="9.5">先报告自己是什么模型</text>
  <text x="485" y="84" fill="#7c3aed" font-size="9.5">不在推荐清单（Opus 5.5/GPT-6.1 Sol）</text>
  <text x="485" y="100" fill="#7c3aed" font-size="9.5">→ 明说"可能不达标"并询问是否继续</text>
  </g>
</svg>
</div>'''

S["q4"] = '''<div class="svgbox">
<svg width="640" height="130" viewBox="0 0 640 130">
  <g font-size="10" text-anchor="middle">
  <rect x="25" y="25" width="170" height="80" rx="10" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
  <text x="110" y="50" fill="#1e40af" font-weight="bold" font-size="11">① vision-check make</text>
  <text x="110" y="68" fill="#1e40af" font-size="9">生成带编号标记的标定图</text>
  <text x="110" y="90" fill="#1e40af" font-size="9">agent 读图写 JSON 答案</text>
  <path d="M195 65 L 245 65" stroke="#f59e0b" stroke-width="2.5" marker-end="url(#ma4)"/>
  <defs><marker id="ma4" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#f59e0b"/></marker></defs>
  <rect x="250" y="25" width="140" height="80" rx="10" fill="#fef3c7" stroke="#f59e0b" stroke-width="2"/>
  <text x="320" y="50" fill="#92400e" font-weight="bold" font-size="11">② score 评分</text>
  <text x="320" y="68" fill="#92400e" font-size="9">量化"这个模型读坐标准不准"</text>
  <text x="320" y="90" fill="#92400e" font-size="9">10 秒完成能力标定</text>
  <path d="M390 65 L 440 65" stroke="#dc2626" stroke-width="2.5" marker-end="url(#ma4b)"/>
  <defs><marker id="ma4b" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#dc2626"/></marker></defs>
  <rect x="445" y="25" width="175" height="80" rx="10" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="532" y="50" fill="#b91c1c" font-weight="bold" font-size="11">③ 不达标就停</text>
  <text x="532" y="68" fill="#b91c1c" font-size="9">"读坐标可能偏，大部分要手工修"</text>
  <text x="532" y="90" fill="#b91c1c" font-size="9">返工成本变成 10 秒标定</text>
  </g>
</svg>
</div>'''

S["q5"] = '''<div class="svgbox">
<svg width="640" height="120" viewBox="0 0 640 120">
  <g font-size="10" text-anchor="middle">
  <rect x="30" y="20" width="180" height="80" rx="10" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>
  <text x="120" y="45" fill="#166534" font-weight="bold" font-size="11">左：部件列表</text>
  <text x="120" y="65" fill="#15803d" font-size="9">选中部件 → 图上高亮关键点</text>
  <text x="120" y="83" fill="#15803d" font-size="9">拖到对的位置</text>
  <path d="M210 60 L 250 60" stroke="#16a34a" stroke-width="2.5" marker-end="url(#ma5)"/>
  <defs><marker id="ma5" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#16a34a"/></marker></defs>
  <rect x="255" y="20" width="160" height="80" rx="10" fill="#7c3aed"/>
  <text x="335" y="45" fill="#fff" font-weight="bold" font-size="11">右：实时预览</text>
  <text x="335" y="65" fill="#e9d5ff" font-size="9">Pose test 转头/闭眼</text>
  <text x="335" y="83" fill="#e9d5ff" font-size="9">Lip sync 元音口型核对</text>
  <path d="M415 60 L 455 60" stroke="#7c3aed" stroke-width="2.5" marker-end="url(#ma5b)"/>
  <defs><marker id="ma5b" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#7c3aed"/></marker></defs>
  <rect x="460" y="20" width="160" height="80" rx="10" fill="#fef3c7" stroke="#f59e0b" stroke-width="2"/>
  <text x="540" y="45" fill="#92400e" font-weight="bold" font-size="11">改切割值弹横幅</text>
  <text x="540" y="65" fill="#92400e" font-size="9">眼/手轮廓、发罩区域</text>
  <text x="540" y="83" fill="#92400e" font-size="9">→ 保存并重建图层(几秒)</text>
  </g>
</svg>
</div>'''

S["q7"] = '''<div class="svgbox">
<svg width="640" height="125" viewBox="0 0 640 125">
  <g font-size="10" text-anchor="middle">
  <rect x="18" y="18" width="185" height="90" rx="10" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="110" y="42" fill="#b91c1c" font-weight="bold" font-size="11">模型门槛</text>
  <text x="110" y="60" fill="#b91c1c" font-size="9">仅认证 Opus 5.5/GPT-6.1 Sol</text>
  <text x="110" y="78" fill="#b91c1c" font-size="9">弱视觉模型=大量手工修</text>
  <text x="110" y="96" fill="#b91c1c" font-size="9">输入限正面半身透明PNG</text>
  <rect x="218" y="18" width="185" height="90" rx="10" fill="#ffedd5" stroke="#ea580c" stroke-width="2"/>
  <text x="310" y="42" fill="#c2410c" font-weight="bold" font-size="11">Windows 专章</text>
  <text x="310" y="60" fill="#c2410c" font-size="9">ZIP 要解锁 Properties</text>
  <text x="310" y="78" fill="#c2410c" font-size="9">projects/ 目录权限继承</text>
  <text x="310" y="96" fill="#c2410c" font-size="9">README 有整节排障</text>
  <rect x="418" y="18" width="200" height="90" rx="10" fill="#ede9fe" stroke="#7c3aed" stroke-width="2"/>
  <text x="518" y="42" fill="#5b21b6" font-weight="bold" font-size="11">许可分层</text>
  <text x="518" y="60" fill="#5b21b6" font-size="9">代码 MIT ✅</text>
  <text x="518" y="78" fill="#5b21b6" font-size="9">样例角色 Miko 作者保留 ❌</text>
  <text x="518" y="96" fill="#5b21b6" font-size="9">vendor/mediapipe Apache 2.0</text>
  </g>
</svg>
</div>'''

S["q8"] = '''<div class="svgbox">
<svg width="640" height="130" viewBox="0 0 640 130">
  <g font-size="10" text-anchor="middle">
  <rect x="20" y="35" width="130" height="60" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="85" y="58" fill="#166534" font-weight="bold" font-size="10.5">bead_pattern</text>
  <text x="85" y="76" fill="#16a34a" font-size="9">照片→像素图纸</text>
  <rect x="170" y="35" width="130" height="60" rx="10" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
  <text x="235" y="58" fill="#1e40af" font-weight="bold" font-size="10.5">sprite_gen</text>
  <text x="235" y="76" fill="#2563eb" font-size="9">立绘→游戏精灵</text>
  <rect x="320" y="35" width="130" height="60" rx="10" fill="#7c3aed"/>
  <text x="385" y="58" fill="#fff" font-weight="bold" font-size="10.5">mesh_avatar(本条)</text>
  <text x="385" y="76" fill="#e9d5ff" font-size="9">插画→动头像</text>
  <rect x="470" y="35" width="150" height="60" rx="10" fill="#fef3c7" stroke="#f59e0b" stroke-width="2"/>
  <text x="545" y="58" fill="#92400e" font-weight="bold" font-size="10.5">新增子系统</text>
  <text x="545" y="76" fill="#92400e" font-size="9">能力校准(vision-check)</text>
  <text x="320" y="118" fill="#6b7280" font-size="10" font-weight="bold">"单图→可用资产"三部曲 + harness 论文七子系统之外的新增位置</text>
  </g>
</svg>
</div>'''

S["q9"] = '''<div class="svgbox">
<svg width="640" height="110" viewBox="0 0 640 110">
  <g font-size="10" text-anchor="middle">
  <rect x="20" y="22" width="140" height="66" rx="10" fill="#ede9fe" stroke="#7c3aed"/>
  <text x="90" y="47" fill="#5b21b6" font-weight="bold">四步管线</text>
  <text x="90" y="65" fill="#7c3aed" font-size="9">A→人查→人修→A</text>
  <rect x="175" y="22" width="140" height="66" rx="10" fill="#dbeafe" stroke="#2563eb"/>
  <text x="245" y="47" fill="#1e40af" font-weight="bold">能力前置验证</text>
  <text x="245" y="65" fill="#2563eb" font-size="9">先标定再开工</text>
  <rect x="330" y="22" width="140" height="66" rx="10" fill="#dcfce7" stroke="#16a34a"/>
  <text x="400" y="47" fill="#166534" font-weight="bold">2D网格机理</text>
  <text x="400" y="65" fill="#16a34a" font-size="9">切层+关键点+物理</text>
  <rect x="485" y="22" width="140" height="66" rx="10" fill="#fef3c7" stroke="#f59e0b"/>
  <text x="555" y="47" fill="#92400e" font-weight="bold">许可分层</text>
  <text x="555" y="65" fill="#92400e" font-size="9">代码/资产分开写</text>
  </g>
</svg>
</div>'''

S["q10"] = '''<div class="svgbox">
<svg width="640" height="110" viewBox="0 0 640 110">
  <g font-size="10" text-anchor="middle">
  <rect x="60" y="25" width="500" height="34" rx="8" fill="#dcfce7"/>
  <rect x="60" y="25" width="477" height="34" rx="8" fill="#16a34a"/>
  <text x="298" y="47" fill="#fff" font-weight="bold" font-size="11">102 passed / 107（95.3%）</text>
  <text x="580" y="47" fill="#166534" font-weight="bold" font-size="10" text-anchor="start">5 失败</text>
  <text x="320" y="82" fill="#6b7280" font-size="10">失败全部 = Windows symlink EPERM 权限族（测试用符号链接构造路径逃逸攻击样本）</text>
  <text x="320" y="99" fill="#6b7280" font-size="10">非代码缺陷 · e2e 未跑 · 端到端头像未生成（如实声明）</text>
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
