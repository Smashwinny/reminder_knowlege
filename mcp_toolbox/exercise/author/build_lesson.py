from pathlib import Path
import html, json, hashlib, textwrap, re
from datetime import datetime, timezone
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, Color, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from lesson_data import *

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'deliverables'; OUT.mkdir(exist_ok=True)
DATA=json.loads((ROOT/'author/runtime_lesson.json').read_text())
E=html.escape
COLORS=['#5a32e6','#006bd6','#007d7a','#c32661','#b75400','#4655cf']
LIGHT=['#f2edff','#edf6ff','#e9f9f5','#fff0f6','#fff5e9','#f1f2ff']
source_ids={p:i+1 for i,(_,p) in enumerate(SOURCE_FILES)}

def svg(i,q):
    color=COLORS[i%6]
    nodes=''
    for j,l in enumerate(q['nodes']):
        x=12+j*204
        nodes+=f'<rect x="{x}" y="16" width="170" height="50" rx="12" fill="{color}"/><text x="{x+85}" y="46" text-anchor="middle" fill="white" font-size="14">{E(l)}</text>'
        if j<2:nodes+=f'<path d="M{x+177} 41 h20 m-5 -5 l5 5 -5 5" fill="none" stroke="{color}" stroke-width="3"/>'
    return f'<svg viewBox="0 0 600 90" role="img" aria-labelledby="svg-title-{i}"><title id="svg-title-{i}">{E(q["caption"])}</title>{nodes}</svg>'

toc=''.join(f'<li><a href="#q{i+1}">{E(q["title"])}</a></li>' for i,q in enumerate(QUESTIONS))
cards=''
for i,q in enumerate(QUESTIONS):
    refs='、'.join('S'+str(source_ids[p]) for p in q['refs'] if p in source_ids)
    cards+=f'''<article class="q" id="q{i+1}" style="--accent:{COLORS[i%6]};--pale:{LIGHT[i%6]}"><div class="qhead"><span class="qnum">{i+1:02d}</span><h2>{E(q['title'])}</h2></div><p class="lead">{E(q['lead'])}</p><p>{E(q['answer'])}</p><p class="term"><b>术语落地</b> {E(q['term'])}</p><p><b>看一个场景</b> {E(q['example'])}</p>{svg(i,q)}<p class="caption">{E(q['caption'])}</p><p class="source">依据：{refs}。本页解释中的建议不等于本次已验证功能。</p></article>'''
abilities=''.join(f'<li><b>{E(t)}</b><br>{E(a)}</li>' for t,a in ABILITIES)
uses=''.join(f'<li><b>{E(t)}</b><br>{E(a)}</li>' for t,a in USES)
steps=''
for i,s in enumerate(DATA['steps']):
    steps+=f'''<article class="step"><div class="qhead"><span class="qnum">{i+1}</span><h3>{E(s['title'])}</h3></div><p><b>目的</b> {E(s['purpose'])}</p><pre>{E(s['command'])}</pre><p><b>实现了什么</b> {E(s['result'])}</p><p class="expect"><b>验证标准与实际结果</b><br>{E(s['verify'])}</p></article>'''
srcs=''.join(f'<li id="s{i+1}"><a href="{BASE+p}">S{i+1} {E(n)}</a> · 固定源码路径 {E(p)}</li>' for i,(n,p) in enumerate(SOURCE_FILES))
knowledge=''.join(f'<li>{E(x)}</li>' for x in DATA['knowledge'])
observations=''.join(f'<li>{E(x)}</li>' for x in DATA['observations'])
html_out=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{TITLE}</title><style>
:root{{--ink:#17203b;--purple:#5a32e6;--cyan:#00bec7;--pink:#ee4182;--gold:#ffd448}}*{{box-sizing:border-box}}body{{margin:0;background:#f1f5ff;color:var(--ink);font:17px/1.8 system-ui,"Noto Sans CJK SC",sans-serif}}main{{max-width:1000px;margin:auto;padding:30px 24px 70px}}header{{background:linear-gradient(130deg,#5a32e6,#007dda);color:white;padding:42px;border-radius:24px}}.eyebrow{{font-size:14px;letter-spacing:.1em}}h1{{font-size:40px;line-height:1.3;margin:12px 0}}h2{{font-size:25px;line-height:1.4}}h3{{font-size:22px;margin:0}}.hero-note{{background:#fff3a6;color:#332600;border-radius:12px;padding:18px;font-weight:700}}.meta,.source{{font-size:12px;overflow-wrap:anywhere}}.panel{{background:white;border-radius:20px;padding:26px;margin:24px 0}}.toc{{columns:2;column-gap:36px;padding-left:25px}}.toc li{{break-inside:avoid;margin:7px 0}}a{{color:#4830b3;text-decoration-thickness:1px;text-underline-offset:3px}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:24px}}.list li{{margin-bottom:15px}}.q{{background:white;border:2px solid var(--accent);border-radius:22px;padding:27px;margin:26px 0;break-inside:avoid}}.qhead{{display:flex;gap:18px;align-items:center}}.qnum{{font:900 50px/1 system-ui,sans-serif;color:var(--accent,var(--purple))}}.lead{{font-size:21px;line-height:1.55;font-weight:850;background:var(--pale,#fff2b8);padding:14px;border-radius:10px}}.term{{border-left:5px solid var(--accent);padding-left:14px}}svg{{width:100%;height:auto;display:block;font-family:system-ui,"Noto Sans CJK SC",sans-serif}}.caption{{font-size:14px;margin:0;text-align:center}}.step{{background:white;border-radius:20px;border:2px solid #007d7a;padding:26px;margin:20px 0;break-inside:avoid}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.6 ui-monospace,monospace;background:#17203b;color:#eef4ff;border-radius:12px;padding:18px}}.expect{{padding:16px;background:#e5fff3;border-radius:12px}}.scope{{background:#fff4db;border-left:6px solid #f5a000;padding:18px}}.sources li{{font-size:12px;margin-bottom:8px;overflow-wrap:anywhere}}footer{{font-size:12px}}@page{{size:A4;margin:14mm}}@media print{{body{{background:white;font-size:11pt}}main{{padding:0}}header,.q,.panel,.step{{border-radius:9px}}.qnum{{font-size:32px}}h1{{font-size:27px}}h2{{font-size:18px}}.lead{{font-size:15px}}a{{color:inherit}}}}@media(max-width:650px){{main{{padding:12px}}header{{padding:24px}}h1{{font-size:30px}}.toc{{columns:1}}.grid{{grid-template-columns:1fr}}.q,.step{{padding:18px}}.qnum{{font-size:38px}}h2{{font-size:22px}}}}
</style></head><body><main><header><div class="eyebrow">数据库工具 · 协议 · 权限边界</div><h1>{TITLE}</h1><p>{SUBTITLE}</p><p class="hero-note">这次要看懂的核心：工具“看起来只读”和数据库“真的拒绝写入”，需要不同证据。</p><p class="meta">编制日期 2026-10-05 UTC · 分类：开源项目学习<br>源码观察 HEAD {HEAD}<br>实际运行 v1.13.1，发布提交 {RELEASE}</p></header>
<section class="panel"><h2>先看结论</h2><p>{E(DATA['summary'])}</p><div class="scope">{E(DATA['scope'])}</div><h2>疑问就是目录</h2><ol class="toc">{toc}</ol></section>
<section class="panel"><h2>这个项目给我什么</h2><div class="grid"><div><h3>5 项能力</h3><ol class="list">{abilities}</ol></div><div><h3>4 个具体用途</h3><ol class="list">{uses}</ol></div></div></section>{cards}
<section class="panel"><h2>六步主实验：让真实写调用撞上只读文件边界</h2><p>{E(DATA['setup'])}</p><p class="meta">实际执行：{E(DATA['started'])} 至 {E(DATA['ended'])}<br>{E(DATA['environment'])}</p><p class="scope">{E(DATA['safety'])}</p></section>{steps}
<section class="panel"><h2>实验结果与边界</h2><ul>{observations}</ul><h2>已有知识如何复用</h2><ul>{knowledge}</ul><p>知识笔记是待本机回迁核对的入库提案；没有修改 Windows vault，没有 Git 提交或推送。最终任务是否完成由本人确认。</p></section>
<section class="panel"><h2>证据入口与固定来源</h2><p>原始响应、命令、版本指纹和复跑脚本见练习 ZIP 与实验日志。PDF 直接用 ReportLab 生成，并逐页渲染验收；HTML 保留为可编辑图文源，仅完成结构检查，不宣称浏览器视觉验收。</p><ol class="sources">{srcs}</ol><p class="meta">发布版源码：<a href="https://github.com/googleapis/mcp-toolbox/tree/{RELEASE}">v1.13.1 固定提交</a>。上游许可：Apache-2.0；练习包保留相关许可及来源说明。</p></section><footer>学习的终点不是“启动成功”，而是能说明操作、证据、适用范围与尚未验证的部分。</footer></main></body></html>'''
(OUT/'02-guide.html').write_text(html_out,encoding='utf-8')

pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
W,H=A4
c=canvas.Canvas(str(OUT/'01-guide.pdf'),pagesize=A4,pageCompression=1)
c.setTitle(TITLE); c.setAuthor('学习报告'); c.setSubject('MCP Toolbox 数据库工具和 SQLite 只读文件边界实验')
PAGE=0
measurements=[]
def p(txt,x,y,w,size=10.5,leading=15,color='#17203b',bold=False):
    sty=ParagraphStyle('cn',fontName='STSong-Light',fontSize=size,leading=leading,textColor=HexColor(color),wordWrap='CJK',spaceAfter=0)
    text=E(txt.replace('·','/').replace('•','-')).replace('\n','<br/>')
    para=Paragraph(text,sty); _,h=para.wrap(w,1000); para.drawOn(c,x,y-h)
    return y-h
def rect(x,y,w,h,fill,r=8):
    c.setFillColor(HexColor(fill));c.roundRect(x,y,w,h,r,fill=1,stroke=0)
def new_page(section):
    global PAGE
    if PAGE:c.showPage()
    PAGE+=1
    c.setFillColor(HexColor('#17203b'));c.rect(0,H-42,W,42,fill=1,stroke=0)
    p('MCP TOOLBOX  /  '+section,34,H-13,W-68,9,12,'#ffffff')
    p('2026-10-05  ·  v1.13.1 实验  ·  公开源码与虚构数据',34,26,W-110,8,10,'#586279')
    p(f'{PAGE:02d}',W-57,26,25,9,11,'#586279')
    return H-65
def section_title(text,y):return p(text,35,y,W-70,21,28,'#17203b')-15
def diagram(q,x,y,w,color):
    nw=(w-44)/3
    for j,label in enumerate(q['nodes']):
        xx=x+j*(nw+22);rect(xx,y-43,nw,43,color,7)
        p(label,xx+5,y-12,nw-10,10,13,'#ffffff')
        if j<2:
            c.setStrokeColor(HexColor(color));c.setLineWidth(1.8)
            c.line(xx+nw+4,y-22,xx+nw+18,y-22)
            c.line(xx+nw+14,y-18,xx+nw+18,y-22)
            c.line(xx+nw+14,y-26,xx+nw+18,y-22)
    return p(q['caption'],x,y-50,w,8.8,12,'#56607a')-2
def qcard(i,q,top,height=345):
    x=34;w=W-68;color=COLORS[i%6];bg=LIGHT[i%6]
    rect(x,top-height,w,height,bg,10)
    yy=p(f'{i+1:02d}',x+13,top-14,39,27,30,color)
    yy=p(q['title'],x+60,top-14,w-76,14,19,'#17203b')-8
    yy=p(q['lead'],x+14,yy,w-28,12.1,16.5,color)-7
    yy=p(q['answer'],x+14,yy,w-28,10.4,14.6)-6
    yy=p('术语落地：'+q['term'],x+14,yy,w-28,9.9,13.8)-6
    yy=p('场景：'+q['example'],x+14,yy,w-28,9.9,13.8)-8
    yy=diagram(q,x+14,yy,w-28,color)
    refs='、'.join('S'+str(source_ids[t]) for t in q['refs'] if t in source_ids)
    yy=p('依据：'+refs,x+14,yy-2,w-28,8,10,'#63708a')
    measurements.append({'question':i+1,'bottom':yy,'limit':top-height+8,'ok':yy>=top-height+8})
    if yy<top-height+8:raise RuntimeError(f'Question {i+1} overflow {yy} vs {top-height+8}')

y=new_page('学习地图')
y=p(TITLE,35,y,W-70,27,36)-10
y=p(SUBTITLE,35,y,W-70,14,20,'#5a32e6')-22
y=p(DATA['summary'],35,y,W-70,13,19)-17
scope_top=y
rect(34,scope_top-89,W-68,89,'#fff2b8')
p(DATA['scope'],48,scope_top-13,W-96,10.8,16)
y=scope_top-110
y=p('疑问就是目录',35,y,W-70,18,24)-13
for i,q in enumerate(QUESTIONS):
    y=p(f'{i+1:02d}  '+q['title'],42,y,W-84,11.5,18)-4
y=p('阅读路径：先看第 7 问，再按六步实验复跑；最后对照结论的适用范围。',35,y-12,W-70,11,16,'#5a32e6')

y=new_page('能力与用途')
y=section_title('这个项目给我什么',y)
for i,(t,a) in enumerate(ABILITIES):
    y=p(f'{i+1}  {t}',36,y,W-72,13,19,COLORS[i%6])-3
    y=p(a,52,y,W-90,11,16)-12
y=p('4 个具体用途',35,y-6,W-70,18,25)-12
for i,(t,a) in enumerate(USES):
    y=p(f'{i+1}  {t}',36,y,W-72,12,18,'#007d7a')-2
    y=p(a,52,y,W-90,10.5,15)-10

for i in range(0,len(QUESTIONS),2):
    new_page(f'疑问 {i+1:02d} - {i+2:02d}')
    qcard(i,QUESTIONS[i],H-61,345)
    qcard(i+1,QUESTIONS[i+1],H-421,345)

for pair in range(3):
    y=new_page(f'动手实验 {2*pair+1} - {2*pair+2}')
    if pair==0:
        y=p('六步主实验',35,y,W-70,22,29)-8
        y=p(DATA['setup'],35,y,W-70,10.7,15)-10
    else:y=p('继续复跑并核对证据',35,y,W-70,20,27)-15
    for k in range(2):
        idx=2*pair+k;s=DATA['steps'][idx]
        y=p(f'{idx+1:02d}  '+s['title'],35,y,W-70,16,23,'#007d7a')-7
        y=p('目的：'+s['purpose'],35,y,W-70,10.5,15)-7
        lines=s['command'].splitlines()
        code_h=14*len(lines)+20
        rect(34,y-code_h,W-68,code_h,'#edf2ff',6)
        c.setFont('Courier',8.9);c.setFillColor(HexColor('#15234b'))
        for li,line in enumerate(lines):
            if c.stringWidth(line,'Courier',8.9)>W-94:raise RuntimeError('Command overflow: '+line)
            c.drawString(47,y-16-li*14,line)
        y-=code_h+10
        y=p('实现了什么：'+s['result'],35,y,W-70,10.5,15)-7
        y=p('验证标准与实际结果：'+s['verify'],35,y,W-70,10.5,15,'#005e55')-20
    if pair==0:
        y=p(DATA['safety'],35,y,W-70,9.6,13.5,'#704d00')-8
    if y<52:raise RuntimeError(f'Step page {pair} overflow {y}')

y=new_page('结论与知识连接')
y=section_title('真正得到哪些证据',y)
for row in DATA['observations']:y=p('• '+row,35,y,W-70,10.8,15.5)-9
y=p('已有知识如何复用',35,y-7,W-70,18,24)-12
for row in DATA['knowledge']:y=p('• '+row,35,y,W-70,10.4,15)-8
y=p('待本机收尾',35,y-8,W-70,15,21)-6
y=p('知识笔记仅为入库提案；没有修改 Windows vault，没有 Git 提交或推送。待本机回迁后，与最新笔记做同义查重和关联。任务是否完成由本人确认。',35,y,W-70,10.5,15)-10
y=p('实际运行：'+DATA['started']+' 至 '+DATA['ended'],35,y,W-70,9.2,13)-4
y=p(DATA['environment'],35,y,W-70,9.2,13)
if y<50:raise RuntimeError('Conclusion page overflow')

y=new_page('固定来源与复核入口')
y=section_title('来源与复核入口',y)
y=p('源码观察固定到 '+HEAD+'；实际二进制为 v1.13.1，对应发布提交 '+RELEASE+'。二者分别记录，不能把主分支文档当作发布版已测行为。',35,y,W-70,10.2,14.5)-14
for i,(label,path) in enumerate(SOURCE_FILES):
    y=p(f'S{i+1}  {label}',35,y,W-70,11,15,'#5a32e6')-2
    y=p(path,35,y,W-70,8.5,11.5,'#4c5570')-7
    c.linkURL(BASE+path,(35,y+3,W-35,y+31),relative=0,thickness=0)
y=p('上方来源标题可点击，均指向固定提交。完整 URL、许可证与本地证据清单同时保存在 HTML 和练习 ZIP。',35,y-3,W-70,9.8,14)-10
y=p('产物检查',35,y,W-70,15,21)-7
y=p('PDF 由 ReportLab 直接生成，按 A4 排版并逐页渲染检查。HTML 有 12 个疑问和 12 张内联 SVG，仅通过结构检查，没有声明浏览器视觉验收。练习 ZIP 不含大型二进制，提供官方来源、实测指纹、配置、测试脚本与复跑结果。',35,y,W-70,10.2,14.5)-8
y=p('上游许可 Apache-2.0。引用与随包源码保留原始许可证及版权声明；原创讲解、虚构数据与测试脚本不代表上游官方保证。',35,y,W-70,9.8,14)
if y<48:raise RuntimeError('Sources page overflow')
c.save()
(ROOT/'evidence/layout_checks.json').write_text(json.dumps({'pages':PAGE,'questions':measurements,'html_question_count':len(QUESTIONS),'svg_count':html_out.count('<svg '),'step_count':len(DATA['steps']),'html_browser_visual_check':False},ensure_ascii=False,indent=2))
print(json.dumps({'pages':PAGE,'pdf_bytes':(OUT/'01-guide.pdf').stat().st_size,'html_bytes':(OUT/'02-guide.html').stat().st_size,'layout_checks':measurements},ensure_ascii=False))
