# -*- coding: utf-8 -*-
"""为 magpie_guide.html 的 Q1-Q10 各插入一张内联 SVG（审核打回补图）。"""
import re
from pathlib import Path

p = Path("F:/reminder/magpie_gateway/magpie_gateway-guide.html")
html = p.read_text(encoding="utf-8")

Q1 = '''<div class="svgbox">
<svg width="640" height="170" viewBox="0 0 640 170">
  <g font-size="11" text-anchor="middle">
  <rect x="15" y="25" width="70" height="30" rx="8" fill="#ede9fe" stroke="#7c3aed"/><text x="50" y="44" fill="#5b21b6">Claude Code</text>
  <rect x="15" y="62" width="70" height="30" rx="8" fill="#ede9fe" stroke="#7c3aed"/><text x="50" y="81" fill="#5b21b6">Codex</text>
  <rect x="15" y="99" width="70" height="30" rx="8" fill="#ede9fe" stroke="#7c3aed"/><text x="50" y="118" fill="#5b21b6">Gemini CLI</text>
  <rect x="15" y="136" width="70" height="26" rx="8" fill="#f5f3ff" stroke="#a78bfa"/><text x="50" y="153" fill="#7c3aed" font-size="9.5">+37 个 Agent</text>
  <path d="M85 95 L 145 95" stroke="#7c3aed" stroke-width="3" marker-end="url(#mq1)"/>
  <defs><marker id="mq1" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#7c3aed"/></marker></defs>
  <rect x="150" y="40" width="150" height="110" rx="14" fill="#7c3aed"/>
  <text x="225" y="68" fill="#fff" font-weight="bold" font-size="13">magpie 网关</text>
  <text x="225" y="90" fill="#e9d5ff" font-size="10.5">127.0.0.1:3425</text>
  <text x="225" y="108" fill="#e9d5ff" font-size="10">四协议互译 + 路由</text>
  <text x="225" y="126" fill="#e9d5ff" font-size="10">菜单栏一键换模型</text>
  <path d="M300 95 L 360 95" stroke="#7c3aed" stroke-width="3" marker-end="url(#mq1b)"/>
  <defs><marker id="mq1b" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#7c3aed"/></marker></defs>
  <rect x="365" y="25" width="90" height="30" rx="8" fill="#dbeafe" stroke="#2563eb"/><text x="410" y="44" fill="#1e40af">Claude 订阅</text>
  <rect x="365" y="62" width="90" height="30" rx="8" fill="#dbeafe" stroke="#2563eb"/><text x="410" y="81" fill="#1e40af">ChatGPT Plus</text>
  <rect x="365" y="99" width="90" height="30" rx="8" fill="#dbeafe" stroke="#2563eb"/><text x="410" y="118" fill="#1e40af">Gemini / Grok</text>
  <rect x="365" y="136" width="90" height="26" rx="8" fill="#eff6ff" stroke="#60a5fa"/><text x="410" y="153" fill="#2563eb" font-size="9.5">API key 供应商x26</text>
  <rect x="480" y="60" width="145" height="70" rx="12" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="552" y="86" fill="#166534" font-weight="bold">效果</text>
  <text x="552" y="104" fill="#166534" font-size="10">任一 Agent 用任一模型</text>
  <text x="552" y="119" fill="#166534" font-size="10">限流自动切下一家</text>
  </g>
</svg>
</div>'''

Q2 = '''<div class="svgbox">
<svg width="640" height="180" viewBox="0 0 640 180">
  <text x="140" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#dc2626">旧世界：MxN（每个 Agent 单独接每个模型）</text>
  <g stroke="#fca5a5" stroke-width="1.5">
    <path d="M70 45 L70 150 M110 45 L110 150 M150 45 L150 150 M190 45 L190 150"/>
    <path d="M45 60 L215 60 M45 90 L215 90 M45 120 L215 120 M45 150 L215 150"/>
  </g>
  <g font-size="9.5" fill="#991b1b" text-anchor="middle">
    <text x="70" y="40">ClaudeCode</text><text x="130" y="40">Codex</text><text x="190" y="40">Gemini</text>
    <text x="30" y="63">Kimi</text><text x="30" y="93">DeepSeek</text><text x="30" y="123">GLM</text><text x="30" y="153">+23家</text>
  </g>
  <g fill="#fee2e2"><circle cx="70" cy="60" r="4"/><circle cx="130" cy="60" r="4"/><circle cx="190" cy="60" r="4"/><circle cx="70" cy="90" r="4"/><circle cx="130" cy="90" r="4"/><circle cx="190" cy="90" r="4"/><circle cx="70" cy="120" r="4"/><circle cx="130" cy="120" r="4"/><circle cx="190" cy="120" r="4"/></g>
  <path d="M255 95 L 315 95" stroke="#16a34a" stroke-width="3" marker-end="url(#mq2)"/>
  <defs><marker id="mq2" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#16a34a"/></marker></defs>
  <text x="330" y="22" font-size="13" font-weight="bold" fill="#16a34a">magpie：M+N（一切代理化）</text>
  <g font-size="9.5" fill="#166534" text-anchor="middle">
    <rect x="330" y="40" width="60" height="24" rx="6" fill="#dcfce7" stroke="#16a34a"/><text x="360" y="56">Agentx40</text>
    <rect x="330" y="76" width="60" height="24" rx="6" fill="#7c3aed"/><text x="360" y="92" fill="#fff">网关</text>
    <rect x="330" y="112" width="60" height="24" rx="6" fill="#dbeafe" stroke="#2563eb"/><text x="360" y="128" fill="#1e40af">供应商x26</text>
    <path d="M360 64 L360 76 M360 100 L360 112" stroke="#16a34a" stroke-width="2"/>
  </g>
  <text x="500" y="80" font-size="11" fill="#166534" font-weight="bold">40x26 = 1040 条接线</text>
  <text x="500" y="100" font-size="11" fill="#16a34a" font-weight="bold">压成 40+26 = 66 个适配器</text>
  <text x="500" y="125" font-size="10" fill="#6b7280">新增一个 Agent 或一家供应商</text>
  <text x="500" y="140" font-size="10" fill="#6b7280">只需写一个适配器，其余零改动</text>
</svg>
</div>'''

Q3 = '''<div class="svgbox">
<svg width="640" height="150" viewBox="0 0 640 150">
  <g font-size="10" text-anchor="middle">
  <rect x="10" y="30" width="100" height="26" rx="7" fill="#dbeafe" stroke="#2563eb"/><text x="60" y="47" fill="#1e40af">OpenAI Chat</text>
  <rect x="10" y="62" width="100" height="26" rx="7" fill="#dbeafe" stroke="#2563eb"/><text x="60" y="79" fill="#1e40af">OpenAI Resp.</text>
  <rect x="10" y="94" width="100" height="26" rx="7" fill="#dbeafe" stroke="#2563eb"/><text x="60" y="111" fill="#1e40af">Anthropic</text>
  <rect x="10" y="126" width="100" height="20" rx="7" fill="#eff6ff" stroke="#60a5fa"/><text x="60" y="140" fill="#2563eb" font-size="9">Gemini</text>
  <path d="M110 88 L 165 88" stroke="#7c3aed" stroke-width="2.5" marker-end="url(#mq3)"/>
  <defs><marker id="mq3" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#7c3aed"/></marker></defs>
  <rect x="170" y="50" width="130" height="76" rx="12" fill="#7c3aed"/>
  <text x="235" y="78" fill="#fff" font-weight="bold" font-size="12">归一化内部表示</text>
  <text x="235" y="98" fill="#e9d5ff" font-size="9.5">消息/工具/流式/推理字段</text>
  <text x="235" y="114" fill="#e9d5ff" font-size="9.5">1425 个测试守保真</text>
  <path d="M300 88 L 355 88" stroke="#7c3aed" stroke-width="2.5" marker-end="url(#mq3b)"/>
  <defs><marker id="mq3b" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#7c3aed"/></marker></defs>
  <rect x="360" y="30" width="120" height="26" rx="7" fill="#dcfce7" stroke="#16a34a"/><text x="420" y="47" fill="#166534">Claude 订阅</text>
  <rect x="360" y="62" width="120" height="26" rx="7" fill="#dcfce7" stroke="#16a34a"/><text x="420" y="79" fill="#166534">Kimi / DeepSeek key</text>
  <rect x="360" y="94" width="120" height="26" rx="7" fill="#dcfce7" stroke="#16a34a"/><text x="420" y="111" fill="#166534">Gemini / Grok 订阅</text>
  <rect x="360" y="126" width="120" height="20" rx="7" fill="#f0fdf4" stroke="#4ade80"/><text x="420" y="140" fill="#15803d" font-size="9">+21 家供应商</text>
  <text x="545" y="70" font-size="10.5" fill="#6b7280">同构回译：</text>
  <text x="545" y="88" font-size="10.5" fill="#6b7280">响应按调用方</text>
  <text x="545" y="105" font-size="10.5" fill="#6b7280">协议流式返回</text>
  </g>
</svg>
</div>'''

Q4 = '''<div class="svgbox">
<svg width="640" height="160" viewBox="0 0 640 160">
  <g font-size="10" text-anchor="middle">
  <rect x="15" y="20" width="120" height="34" rx="9" fill="#fef3c7" stroke="#f59e0b"/><text x="75" y="35" fill="#92400e" font-weight="bold">你的 Claude 订阅</text><text x="75" y="48" fill="#92400e" font-size="8.5">已登录的 Claude Code</text>
  <rect x="15" y="63" width="120" height="34" rx="9" fill="#fef3c7" stroke="#f59e0b"/><text x="75" y="78" fill="#92400e" font-weight="bold">ChatGPT Plus</text><text x="75" y="91" fill="#92400e" font-size="8.5">已登录的 Codex</text>
  <rect x="15" y="106" width="120" height="34" rx="9" fill="#fef3c7" stroke="#f59e0b"/><text x="75" y="121" fill="#92400e" font-weight="bold">Gemini/Copilot/Grok</text><text x="75" y="134" fill="#92400e" font-size="8.5">登录态</text>
  <path d="M135 80 L 195 80" stroke="#f59e0b" stroke-width="2.5" marker-end="url(#mq4)"/>
  <defs><marker id="mq4" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#f59e0b"/></marker></defs>
  <rect x="200" y="35" width="150" height="92" rx="12" fill="#7c3aed"/>
  <text x="275" y="60" fill="#fff" font-weight="bold" font-size="12">凭证转 provider</text>
  <text x="275" y="80" fill="#e9d5ff" font-size="9.5">驱动真实 claude 二进制</text>
  <text x="275" y="95" fill="#e9d5ff" font-size="9.5">MCP 桥接调用方工具</text>
  <text x="275" y="113" fill="#e9d5ff" font-size="9.5">多账号排队·配额尽自动切</text>
  <path d="M350 80 L 410 80" stroke="#7c3aed" stroke-width="2.5" marker-end="url(#mq4b)"/>
  <defs><marker id="mq4b" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#7c3aed"/></marker></defs>
  <rect x="415" y="20" width="105" height="30" rx="8" fill="#ede9fe" stroke="#7c3aed"/><text x="467" y="39" fill="#5b21b6">Codex 借 Claude</text>
  <rect x="415" y="58" width="105" height="30" rx="8" fill="#ede9fe" stroke="#7c3aed"/><text x="467" y="77" fill="#5b21b6">Cursor 借 Plus</text>
  <rect x="415" y="96" width="105" height="30" rx="8" fill="#ede9fe" stroke="#7c3aed"/><text x="467" y="115" fill="#5b21b6">任意 Agent 借任意订阅</text>
  <rect x="545" y="45" width="85" height="62" rx="10" fill="#fee2e2" stroke="#dc2626"/>
  <text x="587" y="68" fill="#b91c1c" font-weight="bold" font-size="10">ToS 灰区</text>
  <text x="587" y="84" fill="#b91c1c" font-size="8.5">订阅条款大概率</text>
  <text x="587" y="97" fill="#b91c1c" font-size="8.5">禁止共享/自动化</text>
  </g>
</svg>
</div>'''

Q5 = '''<div class="svgbox">
<svg width="640" height="150" viewBox="0 0 640 150">
  <g font-size="10">
  <rect x="15" y="18" width="260" height="115" rx="10" fill="#1f2937"/>
  <text x="30" y="38" fill="#fbbf24" font-size="10" font-family="monospace"># 我的 Claude 配置</text>
  <text x="30" y="56" fill="#a7f3d0" font-family="monospace" font-size="9.5">base_url = https://api.anthropic.com</text>
  <text x="30" y="72" fill="#6b7280" font-family="monospace" font-size="9.5"># 公司代理，别动这行</text>
  <text x="30" y="88" fill="#a7f3d0" font-family="monospace" font-size="9.5">proxy = http://corp:8080</text>
  <text x="30" y="106" fill="#6b7280" font-family="monospace" font-size="9.5"># 手工调的超时，勿删</text>
  <text x="30" y="122" fill="#a7f3d0" font-family="monospace" font-size="9.5">timeout = 120</text>
  <path d="M285 76 L 345 76" stroke="#16a34a" stroke-width="3" marker-end="url(#mq5)"/>
  <defs><marker id="mq5" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#16a34a"/></marker></defs>
  <rect x="350" y="45" width="120" height="62" rx="10" fill="#16a34a"/>
  <text x="410" y="70" fill="#fff" text-anchor="middle" font-weight="bold" font-size="11">配置手术</text>
  <text x="410" y="88" fill="#dcfce7" text-anchor="middle" font-size="9">只改 base_url 一行</text>
  <text x="410" y="102" fill="#dcfce7" text-anchor="middle" font-size="9">注释/格式/顺序全保留</text>
  <path d="M475 76 L 535 76" stroke="#16a34a" stroke-width="3" marker-end="url(#mq5b)"/>
  <defs><marker id="mq5b" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#16a34a"/></marker></defs>
  <rect x="540" y="18" width="90" height="115" rx="10" fill="#1f2937"/>
  <text x="550" y="38" fill="#fbbf24" font-size="9" font-family="monospace"># 我的 Claude 配置</text>
  <text x="550" y="56" fill="#a7f3d0" font-family="monospace" font-size="8.5">base_url = 127.0.0.1:3425</text>
  <text x="550" y="72" fill="#6b7280" font-family="monospace" font-size="8.5"># 公司代理，别动这行</text>
  <text x="550" y="88" fill="#a7f3d0" font-family="monospace" font-size="8.5">proxy = http://corp:8080</text>
  <text x="550" y="106" fill="#6b7280" font-family="monospace" font-size="8.5"># 手工调的超时…</text>
  <text x="550" y="122" fill="#a7f3d0" font-family="monospace" font-size="8.5">timeout = 120</text>
  </g>
</svg>
</div>'''

Q6 = '''<div class="svgbox">
<svg width="640" height="140" viewBox="0 0 640 140">
  <text x="320" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#7c3aed">测试密度：1425 / 2162 = 66% 的 Go 文件是测试</text>
  <rect x="60" y="45" width="380" height="34" rx="6" fill="#ddd6fe"/>
  <rect x="60" y="45" width="251" height="34" rx="6" fill="#7c3aed"/>
  <text x="185" y="67" fill="#fff" font-size="11" text-anchor="middle" font-weight="bold">测试 1425</text>
  <text x="375" y="67" fill="#5b21b6" font-size="11" text-anchor="middle">源码 737</text>
  <g font-size="10" fill="#6b7280">
    <text x="60" y="105">account_cap（配额上限）</text>
    <text x="60" y="122">groups_rules（路由规则）</text>
    <text x="240" y="105">quota_served（用量服务）</text>
    <text x="240" y="122">anthropic_cache_ttl（缓存语义）</text>
    <text x="430" y="105">providers_decide（供应商选择）</text>
    <text x="430" y="122">协议形状保真系列</text>
  </g>
  <text x="585" y="60" font-size="10" fill="#16a34a" font-weight="bold" text-anchor="middle">测试名</text>
  <text x="585" y="75" font-size="10" fill="#16a34a" font-weight="bold" text-anchor="middle">即规格</text>
</svg>
</div>'''

Q7 = '''<div class="svgbox">
<svg width="640" height="130" viewBox="0 0 640 130">
  <g font-size="10" text-anchor="middle">
  <rect x="15" y="20" width="145" height="95" rx="12" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="87" y="45" fill="#b91c1c" font-weight="bold" font-size="12">ToS 灰区</text>
  <text x="87" y="65" fill="#b91c1c">订阅共享=账号共享</text>
  <text x="87" y="82" fill="#b91c1c">自动化使用嫌疑</text>
  <text x="87" y="99" fill="#b91c1c">封号风险自担</text>
  <rect x="175" y="20" width="145" height="95" rx="12" fill="#ffedd5" stroke="#ea580c" stroke-width="2"/>
  <text x="247" y="45" fill="#c2410c" font-weight="bold" font-size="12">凭证集中</text>
  <text x="247" y="65" fill="#c2410c">所有 key+登录态</text>
  <text x="247" y="82" fill="#c2410c">汇集在一个网关</text>
  <text x="247" y="99" fill="#c2410c">被入侵=全部失守</text>
  <rect x="335" y="20" width="145" height="95" rx="12" fill="#fef3c7" stroke="#f59e0b" stroke-width="2"/>
  <text x="407" y="45" fill="#b45309" font-weight="bold" font-size="12">翻译损耗</text>
  <text x="407" y="65" fill="#b45309">四协议互译有边角</text>
  <text x="407" y="82" fill="#b45309">复杂工具调用</text>
  <text x="407" y="99" fill="#b45309">需实测保真</text>
  <rect x="495" y="20" width="130" height="95" rx="12" fill="#ede9fe" stroke="#7c3aed" stroke-width="2"/>
  <text x="560" y="45" fill="#5b21b6" font-weight="bold" font-size="12">单作者依赖</text>
  <text x="560" y="65" fill="#5b21b6">迭代极快 =</text>
  <text x="560" y="82" fill="#5b21b6">breaking change</text>
  <text x="560" y="99" fill="#5b21b6">风险自担</text>
  </g>
</svg>
</div>'''

Q8 = '''<div class="svgbox">
<svg width="640" height="160" viewBox="0 0 640 160">
  <g font-size="10" text-anchor="middle">
  <rect x="20" y="95" width="120" height="45" rx="9" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
  <text x="80" y="115" fill="#1e40af" font-weight="bold">BYOK</text>
  <text x="80" y="131" fill="#1e40af" font-size="9">自带 key 的网关</text>
  <rect x="165" y="60" width="130" height="45" rx="9" fill="#ede9fe" stroke="#7c3aed" stroke-width="2"/>
  <text x="230" y="80" fill="#5b21b6" font-weight="bold">+ BYSOL</text>
  <text x="230" y="96" fill="#5b21b6" font-size="9">订阅凭证化（magpie 首发）</text>
  <rect x="320" y="25" width="150" height="45" rx="9" fill="#7c3aed"/>
  <text x="395" y="45" fill="#fff" font-weight="bold">+ 四协议翻译</text>
  <text x="395" y="61" fill="#e9d5ff" font-size="9">OpenAIx2/Anthropic/Gemini 互译</text>
  <path d="M140 110 L165 92 M295 82 L320 60" stroke="#9ca3af" stroke-width="2"/>
  <rect x="500" y="25" width="125" height="115" rx="10" fill="#f9fafb" stroke="#d1d5db"/>
  <text x="562" y="45" fill="#374151" font-weight="bold" font-size="11">同类对照</text>
  <text x="562" y="65" fill="#6b7280" font-size="9.5">LiteLLM（Python）</text>
  <text x="562" y="82" fill="#6b7280" font-size="9.5">One-API / New-API</text>
  <text x="562" y="99" fill="#6b7280" font-size="9.5">cc-switch（轻量）</text>
  <text x="562" y="121" fill="#16a34a" font-size="9.5" font-weight="bold">magpie 差异化：</text>
  <text x="562" y="135" fill="#16a34a" font-size="9">订阅共享 + 40+Agent</text>
  </g>
</svg>
</div>'''

Q9 = '''<div class="svgbox">
<svg width="640" height="120" viewBox="0 0 640 120">
  <g font-size="10" text-anchor="middle">
  <rect x="20" y="25" width="135" height="70" rx="10" fill="#ede9fe" stroke="#7c3aed"/>
  <text x="87" y="50" fill="#5b21b6" font-weight="bold">架构观</text>
  <text x="87" y="68" fill="#7c3aed" font-size="9">MxN 压成 M+N</text>
  <text x="87" y="83" fill="#7c3aed" font-size="9">一切代理化</text>
  <rect x="175" y="25" width="135" height="70" rx="10" fill="#dbeafe" stroke="#2563eb"/>
  <text x="242" y="50" fill="#1e40af" font-weight="bold">协议翻译</text>
  <text x="242" y="68" fill="#2563eb" font-size="9">归一化内部表示</text>
  <text x="242" y="83" fill="#2563eb" font-size="9">流式/工具保真</text>
  <rect x="330" y="25" width="135" height="70" rx="10" fill="#dcfce7" stroke="#16a34a"/>
  <text x="397" y="50" fill="#166534" font-weight="bold">凭证谱系</text>
  <text x="397" y="68" fill="#16a34a" font-size="9">key 到 OAuth 到登录态</text>
  <text x="397" y="83" fill="#16a34a" font-size="9">到订阅凭证化</text>
  <rect x="485" y="25" width="135" height="70" rx="10" fill="#fef3c7" stroke="#f59e0b"/>
  <text x="552" y="50" fill="#b45309" font-weight="bold">工程纪律</text>
  <text x="552" y="68" fill="#b45309" font-size="9">配置手术可回滚</text>
  <text x="552" y="83" fill="#b45309" font-size="9">1425 测试即规格</text>
  </g>
</svg>
</div>'''

Q10 = '''<div class="svgbox">
<svg width="640" height="120" viewBox="0 0 640 120">
  <g font-size="10" text-anchor="middle">
  <circle cx="45" cy="35" r="13" fill="#16a34a"/><text x="45" y="40" fill="#fff" font-weight="bold">v</text>
  <text x="45" y="65" fill="#166534" font-size="9">四协议 4/4</text>
  <circle cx="145" cy="35" r="13" fill="#16a34a"/><text x="145" y="40" fill="#fff" font-weight="bold">v</text>
  <text x="145" y="65" fill="#166534" font-size="9">端口 3425</text>
  <circle cx="245" cy="35" r="13" fill="#16a34a"/><text x="245" y="40" fill="#fff" font-weight="bold">v</text>
  <text x="245" y="65" fill="#166534" font-size="9">订阅 MCP 桥</text>
  <circle cx="345" cy="35" r="13" fill="#16a34a"/><text x="345" y="40" fill="#fff" font-weight="bold">v</text>
  <text x="345" y="65" fill="#166534" font-size="9">供应商 >=3</text>
  <circle cx="445" cy="35" r="13" fill="#16a34a"/><text x="445" y="40" fill="#fff" font-weight="bold">v</text>
  <text x="445" y="65" fill="#166534" font-size="9">80 适配器</text>
  <circle cx="545" cy="35" r="13" fill="#16a34a"/><text x="545" y="40" fill="#fff" font-weight="bold">v</text>
  <text x="545" y="65" fill="#166534" font-size="9">1425 测试文件</text>
  <rect x="120" y="85" width="400" height="26" rx="13" fill="#f5f3ff" stroke="#7c3aed"/>
  <text x="320" y="102" fill="#5b21b6" font-weight="bold" font-size="11">validate_magpie.py 6/6 exit=0（独立审核者复跑一致）</text>
  </g>
</svg>
</div>'''

svgs = {"q1": Q1, "q2": Q2, "q3": Q3, "q4": Q4, "q5": Q5,
        "q6": Q6, "q7": Q7, "q8": Q8, "q9": Q9, "q10": Q10}

for qid, svg in svgs.items():
    pat = re.compile(r'(<div class="q[^"]*" id="' + qid + r'">\s*\n\s*<h2>.*?</h2>)', re.S)
    html, n = pat.subn(lambda m: m.group(1) + "\n  " + svg, html)
    if n != 1:
        print("WARN", qid, n)

p.write_text(html, encoding="utf-8")
print("inserted", len(svgs))
