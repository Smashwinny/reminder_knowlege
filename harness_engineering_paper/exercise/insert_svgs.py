# -*- coding: utf-8 -*-
"""为 harness guide 的 Q1-Q10 各插入一张内联 SVG（SVG 自检后补齐）。"""
import re
from pathlib import Path

p = Path("F:/reminder/harness_engineering_paper/harness_engineering_paper-guide.html")
html = p.read_text(encoding="utf-8")

S = {}

S["q1"] = '''<div class="svgbox">
<svg width="640" height="130" viewBox="0 0 640 130">
  <g font-size="10" text-anchor="middle">
  <rect x="15" y="25" width="120" height="80" rx="12" fill="#f1f5f9" stroke="#64748b" stroke-width="2"/>
  <text x="75" y="55" fill="#334155" font-weight="bold" font-size="12">论文</text>
  <text x="75" y="75" fill="#475569" font-size="9.5">arXiv:2609.00006</text>
  <text x="75" y="90" fill="#475569" font-size="9">不 benchmark 只解剖</text>
  <path d="M135 65 L 180 65" stroke="#0f766e" stroke-width="3" marker-end="url(#he1)"/>
  <defs><marker id="he1" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#0f766e"/></marker></defs>
  <rect x="185" y="15" width="180" height="100" rx="12" fill="#0f766e"/>
  <text x="275" y="45" fill="#fff" font-weight="bold" font-size="13">11 个生产级 harness</text>
  <text x="275" y="68" fill="#ccfbf1" font-size="9.5">Claude Code/Codex/Gemini CLI</text>
  <text x="275" y="84" fill="#ccfbf1" font-size="9.5">OpenHands/Aider/Mini-SWE…</text>
  <text x="275" y="103" fill="#99f6e4" font-size="9">+ Omnigent 元对照</text>
  <path d="M365 65 L 410 65" stroke="#0f766e" stroke-width="3" marker-end="url(#he1b)"/>
  <defs><marker id="he1b" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#0f766e"/></marker></defs>
  <rect x="415" y="25" width="210" height="80" rx="12" fill="#fef3c7" stroke="#f59e0b" stroke-width="2"/>
  <text x="520" y="52" fill="#92400e" font-weight="bold" font-size="12">产出</text>
  <text x="520" y="72" fill="#92400e" font-size="10">七子系统解剖 · 13 横切观察</text>
  <text x="520" y="89" fill="#92400e" font-size="10">29 设计模式 · 双缺席实证</text>
  </g>
</svg>
</div>'''

S["q2"] = '''<div class="svgbox">
<svg width="640" height="120" viewBox="0 0 640 120">
  <g font-size="10.5" text-anchor="middle">
  <rect x="30" y="20" width="150" height="55" rx="10" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
  <text x="105" y="43" fill="#1e40af" font-weight="bold" font-size="12">模型</text>
  <text x="105" y="60" fill="#1e40af" font-size="9">推理能力在这里</text>
  <text x="205" y="52" fill="#334155" font-size="18" font-weight="bold">+</text>
  <rect x="230" y="20" width="230" height="55" rx="10" fill="#0f766e" stroke="#115e59" stroke-width="2"/>
  <text x="345" y="43" fill="#fff" font-weight="bold" font-size="12">harness（运行时）</text>
  <text x="345" y="60" fill="#99f6e4" font-size="9">循环/工具/上下文/安全/编排/扩展</text>
  <path d="M230 75 L 230 95 M460 75 L 460 95" stroke="#94a3b8" stroke-width="1.5"/>
  <path d="M230 95 L 460 95" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="345" y="110" fill="#334155" font-size="10.5" font-weight="bold">= Agent（能干活的东西）</text>
  <rect x="500" y="20" width="120" height="55" rx="10" fill="#fee2e2" stroke="#dc2626"/>
  <text x="560" y="43" fill="#b91c1c" font-weight="bold" font-size="10.5">harness 不是</text>
  <text x="560" y="60" fill="#b91c1c" font-size="9">benchmark/排名工具</text>
  <text x="560" y="74" fill="#b91c1c" font-size="9">回答"怎么建"不回答"谁强"</text>
  </g>
</svg>
</div>'''

S["q4"] = '''<div class="svgbox">
<svg width="640" height="150" viewBox="0 0 640 150">
  <g font-size="10" text-anchor="middle">
  <rect x="20" y="20" width="290" height="115" rx="12" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="165" y="45" fill="#b91c1c" font-weight="bold" font-size="12">缺席 1：无 agentic 框架</text>
  <text x="165" y="68" fill="#b91c1c" font-size="9.5">400 万行代码 0 处导入</text>
  <text x="165" y="84" fill="#b91c1c" font-size="9.5">LangChain/LangGraph/AutoGen…</text>
  <text x="165" y="103" fill="#b91c1c" font-size="9.5">Gemini CLI 连 Google 自家的都不用</text>
  <text x="165" y="122" fill="#991b1b" font-size="9">全部手写 async 循环</text>
  <rect x="330" y="20" width="290" height="115" rx="12" fill="#ffedd5" stroke="#ea580c" stroke-width="2"/>
  <text x="475" y="45" fill="#c2410c" font-weight="bold" font-size="12">缺席 2：无向量代码检索</text>
  <text x="475" y="68" fill="#c2410c" font-size="9.5">0 个系统用向量嵌入查代码</text>
  <text x="475" y="87" fill="#c2410c" font-size="9.5">全靠确定性检索：</text>
  <text x="475" y="106" fill="#c2410c" font-size="9.5">ripgrep · tree-sitter · glob · MD 上下文</text>
  <text x="475" y="122" fill="#9a3412" font-size="9">三次语料扩充后依然成立</text>
  </g>
</svg>
</div>'''

S["q5"] = '''<div class="svgbox">
<svg width="640" height="150" viewBox="0 0 640 150">
  <g font-size="10" text-anchor="middle">
  <rect x="25" y="30" width="160" height="70" rx="12" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="105" y="55" fill="#166534" font-weight="bold" font-size="11">Mini-SWE-Agent</text>
  <text x="105" y="72" fill="#166534" font-size="9.5">~100 行 · 七子系统全实现</text>
  <text x="105" y="87" fill="#166534" font-size="9.5">while+模板+1工具+2限制</text>
  <path d="M185 65 L 250 65" stroke="#94a3b8" stroke-width="2" stroke-dasharray="5,4"/>
  <text x="218" y="55" fill="#6b7280" font-size="9">同区间成绩</text>
  <rect x="255" y="30" width="160" height="70" rx="12" fill="#f1f5f9" stroke="#64748b" stroke-width="2"/>
  <text x="335" y="55" fill="#334155" font-weight="bold" font-size="11">SWE-bench Verified</text>
  <text x="335" y="72" fill="#334155" font-size="9.5">与大 3 个数量级的系统</text>
  <text x="335" y="87" fill="#334155" font-size="9.5">成绩同区间（自报）</text>
  <path d="M415 65 L 480 65" stroke="#dc2626" stroke-width="2.5" marker-end="url(#he5)"/>
  <defs><marker id="he5" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#dc2626"/></marker></defs>
  <rect x="485" y="20" width="140" height="100" rx="12" fill="#7c3aed"/>
  <text x="555" y="45" fill="#fff" font-weight="bold" font-size="11">差距不在任务</text>
  <text x="555" y="68" fill="#e9d5ff" font-size="9.5">安全/恢复/成本</text>
  <text x="555" y="84" fill="#e9d5ff" font-size="9.5">扩展性/平台面</text>
  <text x="555" y="105" fill="#e9d5ff" font-size="9">论文§16 给 90 行 MVA</text>
  </g>
</svg>
</div>'''

S["q6"] = '''<div class="svgbox">
<svg width="640" height="140" viewBox="0 0 640 140">
  <g font-size="10" text-anchor="middle">
  <text x="320" y="22" font-size="12" fill="#334155" font-weight="bold">扩展标准采用率（11 系统）</text>
  <rect x="80" y="38" width="330" height="26" rx="6" fill="#0f766e"/>
  <text x="90" y="56" fill="#fff" font-weight="bold" font-size="10.5" text-anchor="start">SKILL.md 技能　9/11</text>
  <rect x="80" y="74" width="293" height="26" rx="6" fill="#2563eb"/>
  <text x="90" y="92" fill="#fff" font-weight="bold" font-size="10.5" text-anchor="start">MCP　8/11</text>
  <text x="440" y="56" fill="#0f766e" font-weight="bold" font-size="11" text-anchor="start">领先</text>
  <text x="440" y="92" fill="#2563eb" font-weight="bold" font-size="11" text-anchor="start">紧随</text>
  <rect x="60" y="110" width="520" height="24" rx="12" fill="#fef3c7" stroke="#f59e0b"/>
  <text x="320" y="126" fill="#92400e" font-size="10" font-weight="bold">"Skills versus MCP: the tie has broken"——平局已破；ACP 进入 6 系统并新增 harness 托管角色</text>
  </g>
</svg>
</div>'''

S["q7"] = '''<div class="svgbox">
<svg width="640" height="140" viewBox="0 0 640 140">
  <g font-size="10" text-anchor="middle">
  <rect x="20" y="40" width="110" height="50" rx="10" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
  <text x="75" y="62" fill="#1e40af" font-weight="bold">CLI</text>
  <text x="75" y="78" fill="#1e40af" font-size="9">终端工具</text>
  <path d="M130 65 L 190 65" stroke="#0f766e" stroke-width="3" marker-end="url(#he7)"/>
  <defs><marker id="he7" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#0f766e"/></marker></defs>
  <rect x="195" y="40" width="130" height="50" rx="10" fill="#0f766e"/>
  <text x="260" y="62" fill="#fff" font-weight="bold">harness</text>
  <text x="260" y="78" fill="#99f6e4" font-size="9">长成框架</text>
  <text x="320" y="25" fill="#334155" font-size="11" font-weight="bold">平台转向四信号：</text>
  <rect x="345" y="38" width="130" height="24" rx="7" fill="#dcfce7" stroke="#16a34a"/><text x="410" y="54" fill="#166534" font-size="9">① 技能=声明式程序</text>
  <rect x="345" y="66" width="130" height="24" rx="7" fill="#dcfce7" stroke="#16a34a"/><text x="410" y="82" fill="#166534" font-size="9">② hooks/事件总线基底</text>
  <rect x="345" y="94" width="130" height="24" rx="7" fill="#dcfce7" stroke="#16a34a"/><text x="410" y="110" fill="#166534" font-size="9">③ 工具≈工作流</text>
  <rect x="485" y="38" width="130" height="24" rx="7" fill="#dcfce7" stroke="#16a34a"/><text x="550" y="54" fill="#166534" font-size="9">④ harness=服务面</text>
  <rect x="485" y="66" width="130" height="52" rx="7" fill="#fef3c7" stroke="#f59e0b"/>
  <text x="550" y="86" fill="#92400e" font-size="9" font-weight="bold">配套经济学：</text>
  <text x="550" y="100" fill="#92400e" font-size="9">市场/切换成本/治理</text>
  <text x="550" y="114" fill="#92400e" font-size="9">harness 吞掉框架之问</text>
  </g>
</svg>
</div>'''

S["q8"] = '''<div class="svgbox">
<svg width="640" height="130" viewBox="0 0 640 130">
  <g font-size="10" text-anchor="middle">
  <rect x="20" y="30" width="180" height="70" rx="10" fill="#ede9fe" stroke="#7c3aed" stroke-width="2"/>
  <text x="110" y="55" fill="#5b21b6" font-weight="bold" font-size="11">vault 既有概念</text>
  <text x="110" y="73" fill="#7c3aed" font-size="9">AgentHarness智能体挽具</text>
  <text x="110" y="88" fill="#7c3aed" font-size="9">工具目录膨胀/Compaction…</text>
  <path d="M200 65 L 250 65" stroke="#0f766e" stroke-width="3" marker-end="url(#he8)"/>
  <defs><marker id="he8" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#0f766e"/></marker></defs>
  <rect x="255" y="20" width="170" height="90" rx="12" fill="#0f766e"/>
  <text x="340" y="48" fill="#fff" font-weight="bold" font-size="12">本论文</text>
  <text x="340" y="70" fill="#99f6e4" font-size="9.5">体系化升级：</text>
  <text x="340" y="86" fill="#99f6e4" font-size="9.5">七子系统+五轴权衡</text>
  <text x="340" y="101" fill="#99f6e4" font-size="9.5">+双缺席实证</text>
  <path d="M425 65 L 475 65" stroke="#16a34a" stroke-width="3" marker-end="url(#he8b)"/>
  <defs><marker id="he8b" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#16a34a"/></marker></defs>
  <rect x="480" y="30" width="145" height="70" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="552" y="55" fill="#166534" font-weight="bold" font-size="11">正名效果</text>
  <text x="552" y="73" fill="#166534" font-size="9">vault harness 品味区</text>
  <text x="552" y="88" fill="#166534" font-size="9">获论文级背书</text>
  </g>
</svg>
</div>'''

S["q9"] = '''<div class="svgbox">
<svg width="640" height="120" viewBox="0 0 640 120">
  <g font-size="10" text-anchor="middle">
  <rect x="20" y="25" width="140" height="70" rx="10" fill="#ede9fe" stroke="#7c3aed"/>
  <text x="90" y="50" fill="#5b21b6" font-weight="bold">解剖眼</text>
  <text x="90" y="68" fill="#7c3aed" font-size="9">七子系统+缺位也是位置</text>
  <rect x="175" y="25" width="140" height="70" rx="10" fill="#dbeafe" stroke="#2563eb"/>
  <text x="245" y="50" fill="#1e40af" font-weight="bold">光谱思维</text>
  <text x="245" y="68" fill="#2563eb" font-size="9">每部件最小↔最大解</text>
  <rect x="330" y="25" width="140" height="70" rx="10" fill="#fee2e2" stroke="#dc2626"/>
  <text x="400" y="50" fill="#b91c1c" font-weight="bold">双缺席</text>
  <text x="400" y="68" fill="#b91c1c" font-size="9">框架/向量缺席是实证</text>
  <rect x="485" y="25" width="140" height="70" rx="10" fill="#dcfce7" stroke="#16a34a"/>
  <text x="555" y="50" fill="#166534" font-weight="bold">安全即架构</text>
  <text x="555" y="68" fill="#166534" font-size="9">运行时层非提示词</text>
  </g>
</svg>
</div>'''

S["q10"] = '''<div class="svgbox">
<svg width="640" height="110" viewBox="0 0 640 110">
  <g font-size="10" text-anchor="middle">
  <circle cx="60" cy="30" r="13" fill="#16a34a"/><text x="60" y="35" fill="#fff" font-weight="bold">v</text>
  <text x="60" y="60" fill="#166534" font-size="9">11 系统</text>
  <circle cx="160" cy="30" r="13" fill="#16a34a"/><text x="160" y="35" fill="#fff" font-weight="bold">v</text>
  <text x="160" y="60" fill="#166534" font-size="9">七子系统</text>
  <circle cx="260" cy="30" r="13" fill="#16a34a"/><text x="260" y="35" fill="#fff" font-weight="bold">v</text>
  <text x="260" y="60" fill="#166534" font-size="9">双缺席 1</text>
  <circle cx="360" cy="30" r="13" fill="#16a34a"/><text x="360" y="35" fill="#fff" font-weight="bold">v</text>
  <text x="360" y="60" fill="#166534" font-size="9">双缺席 2</text>
  <circle cx="460" cy="30" r="13" fill="#16a34a"/><text x="460" y="35" fill="#fff" font-weight="bold">v</text>
  <text x="460" y="60" fill="#166534" font-size="9">扩展标准</text>
  <circle cx="560" cy="30" r="13" fill="#16a34a"/><text x="560" y="35" fill="#fff" font-weight="bold">v</text>
  <text x="560" y="60" fill="#166534" font-size="9">100 行证明+方法论</text>
  <rect x="140" y="78" width="360" height="26" rx="13" fill="#f0fdfa" stroke="#0f766e"/>
  <text x="320" y="95" fill="#115e59" font-weight="bold" font-size="11">verify_claims.py 7/7 原句级命中 exit=0（T2 实体修正实录保留）</text>
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
