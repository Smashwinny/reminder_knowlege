"""Vector PDF and matching editable HTML/Markdown. No service or queue changes."""
from pathlib import Path
from html import escape
import json, math, re, hashlib, zipfile, shutil
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4, landscape

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'output/pdf'
SRC = OUT / 'source'
OUT.mkdir(parents=True, exist_ok=True)
SRC.mkdir(parents=True, exist_ok=True)
W,H = landscape(A4)
COL = dict(ink='#16233D', muted='#52647C', line='#DCE5F0', paper='#F4F7FD',
           mobile='#009F8B', cloud='#F07822', dot='#764FE3', windows='#2875EA',
           ubuntu='#D74554', knowledge='#087B68', git='#333E57', amber='#A66700')
TINT = dict(mobile='#E6F8F3', cloud='#FFF0E4', dot='#F0EAFF', windows='#EAF2FF',
            ubuntu='#FDECEF', knowledge='#E7F6EF', git='#EEF1F7', amber='#FFF4D8')
pdfmetrics.registerFont(TTFont('CN', 'C:/Windows/Fonts/msyh.ttc'))
pdfmetrics.registerFont(TTFont('CN-B', 'C:/Windows/Fonts/msyhbd.ttc'))
pdfmetrics.registerFont(TTFont('Mono', 'C:/Windows/Fonts/consola.ttf'))
PDF = OUT / '拾遗到知识网络-架构与搭建指南.pdf'
CV = canvas.Canvas(str(PDF), pagesize=(W,H), pageCompression=1)
CV.setTitle('拾遗到知识网络 | Reminder × Dot × learn-project')
CV.setAuthor('Reminder 项目 / Codex')
CV.setSubject('彩色工作流、私密授权、各终端搭建、知识入库与每日复习')
svgs, markdown_pages, qa = [], [], []
parts=[]
page_num=0
current_md=[]

def rect(x,y,w,h,fill,stroke=None,r=10):
    CV.setFillColor(HexColor(fill))
    CV.setStrokeColor(HexColor(stroke or fill))
    CV.roundRect(x,H-y-h,w,h,r,fill=1,stroke=bool(stroke))
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke or fill}"/>')

def txt(x,y,s,size=11,color=None,bold=False,mono=False):
    f='Mono' if mono else ('CN-B' if bold else 'CN')
    color=color or COL['ink']
    CV.setFont(f,size); CV.setFillColor(HexColor(color)); CV.drawString(x,H-y-size*.83,str(s))
    width=pdfmetrics.stringWidth(str(s),f,size)
    if x+width>W-25.5: qa.append({'page':page_num,'issue':'text_right_edge','text':str(s),'end':x+width})
    if y+size>H-10: qa.append({'page':page_num,'issue':'text_bottom_edge','text':str(s),'y':y})
    family='Consolas,monospace' if mono else 'Microsoft YaHei,Arial,sans-serif'
    parts.append(f'<text x="{x}" y="{y+size*.83}" fill="{color}" font-size="{size}" font-family="{family}" font-weight="{700 if bold else 400}">{escape(str(s))}</text>')

def wrap(s,width,size=11,bold=False):
    font='CN-B' if bold else 'CN'
    out=[]
    for para in str(s).split('\n'):
        line=''
        for token in re.findall(r'[A-Za-z0-9_./:\\@%$=\-]+|.',para):
            if pdfmetrics.stringWidth(line+token,font,size)>width and line:
                out.append(line.rstrip()); line=token.lstrip()
            else: line+=token
            if pdfmetrics.stringWidth(line,font,size)>width:
                rem=''
                for char in line:
                    if pdfmetrics.stringWidth(rem+char,font,size)>width and rem:
                        out.append(rem);rem=char
                    else: rem+=char
                line=rem
        out.append(line.rstrip())
    return out

def para(x,y,w,s,size=10.5,color=None,bold=False,leading=None):
    leading=leading or size*1.55
    lines=wrap(s,w,size,bold)
    for i,line in enumerate(lines): txt(x,y+i*leading,line,size,color,bold)
    return y+len(lines)*leading

def badge(x,y,label,key='dot',w=None):
    w=w or pdfmetrics.stringWidth(label,'CN-B',8.8)+20
    rect(x,y,w,23,TINT[key],r=6);txt(x+10,y+6,label,8.8,COL[key],True)

def line(points,color=None,dashed=False,arrow=True,label=None,lx=None,ly=None):
    color=color or COL['muted']
    CV.setStrokeColor(HexColor(color));CV.setLineWidth(1.65)
    CV.setDash([5,3] if dashed else [])
    p=CV.beginPath();p.moveTo(points[0][0],H-points[0][1])
    for x,y in points[1:]:p.lineTo(x,H-y)
    CV.drawPath(p);CV.setDash([])
    parts.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in points)}" fill="none" stroke="{color}" stroke-width="1.65"'+(' stroke-dasharray="5 3"' if dashed else '')+'/>')
    if arrow:
        x,y=points[-1]; px,py=points[-2];a=math.atan2(y-py,x-px)
        verts=[(x,y),(x-8*math.cos(a)+4*math.sin(a),y-8*math.sin(a)-4*math.cos(a)),(x-8*math.cos(a)-4*math.sin(a),y-8*math.sin(a)+4*math.cos(a))]
        p=CV.beginPath();p.moveTo(verts[0][0],H-verts[0][1])
        for ax,ay in verts[1:]:p.lineTo(ax,H-ay)
        p.close();CV.setFillColor(HexColor(color));CV.drawPath(p,fill=1,stroke=0)
        parts.append(f'<polygon points="{" ".join(f"{ax},{ay}" for ax,ay in verts)}" fill="{color}"/>')
    if label:
        lw=pdfmetrics.stringWidth(label,'CN',8.7)+12
        rect(lx-6,ly-2,lw,17,'#FFFFFF',r=3);txt(lx,ly,label,8.7,color)

def box(x,y,w,h,title,body,key='dot',role=None,size=10.3):
    rect(x,y,w,h,TINT[key],COL[key],10)
    rect(x,y,5,h,COL[key],r=2)
    title_end=para(x+16,y+14,w-31,title,14,COL[key],True,leading=19)
    yy=title_end+4
    if role: txt(x+16,yy,role,8.8,COL[key],True);yy+=21
    end=para(x+16,yy,w-31,body,size)
    if end>y+h-8:qa.append({'page':page_num,'issue':'box_overflow','title':title,'end':end,'limit':y+h-8})
    current_md.extend(['### '+title,('运行位置：'+role if role else ''),body,''])

def note(y,title,body,key='amber',h=60):
    y=min(y,464)
    h=max(h,64)
    rect(40,y,W-80,h,TINT[key],r=8)
    txt(54,y+11,title,10.4,COL[key],True)
    end=para(54,y+29,W-110,body,9.5,COL['ink'])
    if end>y+h-4:qa.append({'page':page_num,'issue':'note_overflow','title':title,'end':end,'limit':y+h-4})
    current_md.extend(['> '+title,'> '+body,''])

def code(x,y,w,s,label='命令',size=8.8):
    rows=s.strip('\n').splitlines(); leading=size*1.52
    h=34+len(rows)*leading
    rect(x,y,w,h,'#16233D',r=8);txt(x+14,y+10,label,8.5,'#7ED7DF',True)
    for i,row in enumerate(rows):
        f='CN' if re.search(r'[^\x00-\x7f]',row) else 'Mono'
        measured=pdfmetrics.stringWidth(row,f,size)
        if measured>w-28:qa.append({'page':page_num,'issue':'code_overflow','text':row,'width':measured,'limit':w-28})
        txt(x+14,y+29+i*leading,row,size,'#FFFFFF',mono=f=='Mono')
    current_md.extend(['**运行位置 / 操作：'+label+'**','```',s.strip('\n'),'```',''])
    return y+h

def table(x,y,width,headers,rows,widths=None,fs=10,row_h=None):
    widths=widths or [width/len(headers)]*len(headers)
    rect(x,y,width,30,COL['ink'],r=6)
    xx=x
    for i,h in enumerate(headers): txt(xx+11,y+9,h,9.5,'#FFFFFF',True);xx+=widths[i]
    yy=y+30
    for idx,row in enumerate(rows):
        ls=[wrap(str(v),widths[i]-22,fs) for i,v in enumerate(row)]
        rh=max(row_h or 0,max(len(a) for a in ls)*fs*1.5+17)
        rect(x,yy,width,rh,'#FFFFFF' if idx%2==0 else '#EDF2FA',r=0)
        xx=x
        for i,v in enumerate(row): para(xx+11,yy+8,widths[i]-22,str(v),fs,leading=fs*1.5);xx+=widths[i]
        yy+=rh
    if yy>H-46:qa.append({'page':page_num,'issue':'table_bottom','end':yy})
    current_md.extend([' | '.join(headers),' | '.join(['---']*len(headers))]+[' | '.join(str(a) for a in row) for row in rows]+[''])
    return yy

def page(section,title,subtitle='',key='dot',source=None):
    global parts,page_num,current_md
    if page_num: end_page()
    page_num+=1;parts=[];current_md=['## '+str(page_num).zfill(2)+' '+title,'',subtitle,'']
    rect(0,0,W,H,'#FFFFFF',r=0);rect(0,0,10,H,COL[key],r=0)
    txt(40,23,'REMINDER / PERSONAL LEARNING SYSTEM',8.5,COL['muted'],True)
    badge(W-222,17,section,key,w=182)
    txt(40,52,title,24,COL['ink'],True)
    if subtitle:para(40,87,W-80,subtitle,10.3,COL['muted'],leading=15)
    CV.bookmarkPage('p'+str(page_num));CV.addOutlineEntry(title,'p'+str(page_num),0)
    rect(40,H-33,W-80,1,COL['line'],r=0)
    txt(40,H-25,'核验基线 2026-10-05 14:07 CST | 实线=已有路径；虚线=待打通 / 建议配置',7.7,COL['muted'])
    txt(W-86,H-25,f'{page_num:02d} / 36',8.5,COL['ink'],True)
    if source: txt(40,H-49,'依据：'+source,7.5,COL['muted'])

def end_page():
    svgs.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+str(W)+' '+str(H)+'" role="img">'+''.join(parts)+'</svg>')
    markdown_pages.append('\n'.join(current_md));CV.showPage()

# 01 - Cover
page('项目介绍 · 架构 · 搭建','把收藏，变成可掌握的能力','Reminder × Dot × learn-project × Obsidian',key='dot')
txt(40,141,'一个链接的价值，',36,COL['ink'],True)
txt(40,192,'在它进入你的知识网络之后。',30,COL['dot'],True)
para(42,250,410,'手机随手记录 → 核实原始来源 → 云端真实实验与图文讲解 → 私有报告 → 本机知识入库 → Git 备份 → 主动复习。',15,leading=25)
box(537,139,265,185,'这份指南回答四个问题','它做到了什么？\n数据和智能体在哪里运行？\n如何从零搭建并验证？\n如何把结果变成自己的能力？','windows',size=12)
for i,(title,key) in enumerate([('捕获','mobile'),('核实','cloud'),('学习','dot'),('沉淀','windows'),('复习','knowledge')]):
    x=42+i*151;box(x,374,132,73,title,'记录 → 证据' if i==0 else ['','证据 → 判断','实验 → 能力','笔记 → 关联','回忆 → 应用'][i],key,size=9.2)
    if i<4:line([(x+132,409),(x+151,409)],COL[key])
note(465,'阅读约定','前半部适合向伙伴展示；后半部是逐终端搭建手册。事实、当前限制与未来路线分别标注。本 PDF 不包含任何密码、令牌、私有 SSH 连接信息或私人任务正文。',h=62)

# 02
page('01 / 项目价值','把“存了很多”转成“真的会用”','这是一套个人学习流水线：连接已有工具，并给每次学习建立可回溯的交付标准。',source='AGENTS.md；learn-project；三项公开学习提交')
for x,title,body,k in [(40,'输入不再零散','手机看到链接时只需保存。原帖、摘要、来源和后续产物保持同一条任务的关联。','mobile'),(298,'理解不只靠摘要','围绕你的知识储备列疑问，用图和例子讲原理，实际运行实验，明确能力边界。','dot'),(556,'知识不再孤立','新概念查重，项目笔记链接已有概念；可在 Obsidian 沿关联复习和迁移到下一项目。','knowledge')]:box(x,133,246,160,title,body,k)
table(40,315,W-80,['已经证明的能力','实际证据','尚不能据此证明'],[
 ('跨端完整学习闭环','3 个项目已网站交付、回迁、入库并推送 Git','所有链接都可读取；全流程永久无人值守'),
 ('云端连续推进','第 4 项 Colab 完整报告已存；Metrik 正在学习','每 15 分钟完成一份报告'),
 ('可核查的交付质量','真实实验日志、逐页 PDF 与独立审核','AI 报告等于本人已掌握')],[235,255,272],fs=10)
note(463,'向伙伴解释时的一句话','“我把随手收集的项目，交给云端智能体做有证据的学习资料；再把新知识合并到自己的知识网，并用练习和复习检验是否掌握。”',h=58,key='dot')

# 03
page('阅读地图','先看框图，再照终端动手','颜色代表运行环境；状态标记代表实际完成程度。不要把位置、权限和成功状态混在一起。',key='windows')
table(40,132,410,['页码','阅读目标'],[('04–10','看清架构、来源、权限、分类与调度'),('11–17','看清 skill、实验、回迁、知识网与复习'),('18–27','从零准备各终端并完成一次私有备份'),('28–32','验收、入库、Git、复习与系统联调'),('33–36','工具、故障、演进路线和依据')],[77,333],fs=11)
for i,(key,label) in enumerate([('mobile','手机：记录与本人确认'),('cloud','阿里云：数据与权限服务'),('dot','Dot 云端：分析与实验'),('windows','Windows：备份与知识协调'),('ubuntu','Ubuntu 本地：网站运维'),('knowledge','Obsidian / 知识网络')]):badge(483,136+i*45,label,key,w=318)
note(459,'三种读者路线','只体验：第 6、15、16、30 页。接入已有网站：从第 23 页开始。自建独立实例：从第 18 页开始；需要私有网站源码权限、服务器和自己的 Dot 资格。',h=66)

# 04
page('核心架构图','六个位置，一条学习主链','箭头标明连接方式和传递对象；Ubuntu 的 SSH 运维通道与 Dot 的学习通道相互独立。',source='网站部署文件；RUNNING_IN_DOT.md；备份脚本')
box(40,145,174,121,'手机 / Android','复制 X、抖音链接\n粘贴保存，登录同步\n用户自己点任务完成','mobile',role='本人手机',size=10.2)
box(300,145,236,121,'Reminder 私有服务','账户任务 + 允许列表\nOAuth、租约、报告、六原件\n/data 命名数据卷持久化','cloud',role='阿里云 ECS / Docker',size=10.2)
box(628,145,174,121,'本人 Dot','读链接和公开知识\n按 skill 分析、实验、审核\n保存私有报告和分析标签','dot',role='Dot 的云端电脑',size=9.7)
line([(214,197),(300,197)],COL['mobile'],label='HTTPS 同步',lx=219,ly=179)
line([(536,192),(628,192)],COL['dot'],label='MCP / OAuth',lx=544,ly=173)
line([(628,235),(536,235)],COL['cloud'],label='报告 + 产物',lx=550,ly=239)
box(40,367,174,113,'Ubuntu 运维机','私有网站代码与版本核对\nSSH 部署、备份、故障处理\nIssue #1 脱敏协作','ubuntu',role='另一台 Ubuntu 本地',size=9.7)
box(300,367,236,113,'GitHub 知识仓库','仅公开学习指南、实验、笔记\n版本历史与可读的知识索引\n私有网站代码是另一个仓库','git',role='GitHub 远端',size=9.7)
box(628,367,174,113,'Windows 协调端','校验下载 → 唯一协调者\n合并 vault → 审核 → Git\nObsidian 打开本机 vault','windows',role='Windows 本地',size=9.5)
line([(136,367),(136,315),(355,315),(355,266)],COL['ubuntu'],label='SSH：代码 / 备份',lx=169,ly=290)
line([(701,367),(701,303),(490,303),(490,266)],COL['windows'],label='HTTPS：本机拉取私有副本',lx=488,ly=308)
line([(628,426),(536,426)],COL['git'],label='只推学习成果',lx=544,ly=435)
line([(536,384),(584,384),(584,288),(715,288),(715,266)],COL['knowledge'],label='固定版本知识参考',lx=585,ly=339)
para(40,495,W-80,'电脑离线：Dot 仍可云端学习，报告先留网站。本机再次在线：备份脚本拉取；知识入库和 Git 需要协调者接续。原生自动唤醒当前未通过。',9.8,COL['muted'])

# 05
page('职责表','每个终端到底运行什么','“Ubuntu 本地”是管理员电脑；“阿里云服务器”即使运行 Linux，也不是这台本地 Ubuntu。',key='ubuntu')
table(40,130,W-80,['位置','运行模块 / 文件','输入与输出','谁负责'],[
 ('手机','拾遗 Android App；或手机浏览器','链接 / 简短想法 → 同账号任务','本人'),
 ('阿里云服务器','Docker reminder_app；/opt/reminder；/data','任务、列表、OAuth、报告和原件持久化','Ubuntu 运维者'),
 ('Dot 云端','本人 Dot + MCP 插件 + 云端实验目录','获准任务 → 分类 / 真实学习 / 六类原件','云端学习者 + 独立审核者'),
 ('Ubuntu 本地','私有网站 Git 副本、SSH、异机备份检查','已审核代码 → 部署；服务器备份 → 私有副本','唯一网站维护者'),
 ('Windows 本地','tools/；完成/.pipeline/；项目目录；vault/','云端原件 → 校验副本 → 入库与公开 Git','唯一知识协调者'),
 ('GitHub 远端','reminder 私有代码仓；reminder_knowlege 公开仓','代码发布与运维协作；学习成果版本化','两类仓库分别管理')],[116,254,280,112],fs=9.6)
note(459,'Obsidian 的位置','当前 Obsidian 使用 Windows 的 F:\\reminder\\vault。Ubuntu 不是另一份可同时写入的最终知识库；多设备学习前必须协调任务租约和唯一写入者。',h=65,key='knowledge')

# 06
page('手机记录入口','从 X 或抖音开始：先把链接留住','本项目已核对的手机入口是复制后粘贴；当前 Android Manifest 没有原生 ACTION_SEND 分享接收器。',key='mobile',source='AndroidManifest.xml；网站 onlyUrl / fetchPage 代码')
for x,title,body in [(40,'01 · 复制原始链接','在 X 或抖音选择复制链接。保存作者、主题和你想学什么，避免以后只剩一条无法辨认的短链。'),(298,'02 · 在拾遗保存','手机 App 或网站登录本人账号，粘贴并保存。若想触发站点自动摘要，任务正文需是单个纯 HTTP(S) 链接。'),(556,'03 · 进入允许列表','在网站 /dot 管理页把任务加入本人获准清单。是否自动加入今后新增未开始记录，需要单独配置并回读。')]:box(x,139,246,166,title,body,'mobile',size=11)
line([(286,220),(298,220)],COL['mobile']);line([(544,220),(556,220)],COL['mobile'])
box(40,338,367,103,'X：可读取文字 ≠ 已核实全部内容','站点摘要有第三方 X 文本接口作为候选读取途径；Dot 仍需核对作者、帖子中的真实出链及官方仓库。','cloud',size=10.4)
box(428,338,374,103,'抖音：短链 ≠ 自动转录视频','当前站点读公开网页文字，没有已验收的视频下载 / ASR 流程。受阻时补字幕、笔记或明确的项目链接，保留待核实。','amber',size=10.4)
note(463,'第一次试用的成功标准','在手机保存一条你确实有权分享、来源可读的学习链接；在电脑网站同一账号能回读同一条记录。不要用“摘要已显示”作为视频内容完整读取的证明。',h=63)

# 07
page('权限与私密性','服务端限制范围，不靠一句“请保密”','当前授权边界是本人同意的私有 OAuth 连接，不是可认证的“唯一 Dot 身份”。',key='cloud',source='DOT_INTEGRATION.md；官方 OAuth 文档 [S3]')
box(40,137,230,132,'本人同意','登录自己的 Reminder 账户\n选择一个服务端列表\n确认三个 scope 后 OAuth 同意','mobile',size=11)
box(306,137,230,132,'服务端执行范围','固定 canonical 账户 ID\n绑定 listId / resource / 期限\n每次工具请求检查权限','cloud',size=11)
box(572,137,230,132,'Dot 只拿必要工具','records.read：读取\nanalysis.write：分类报告\nlearning.write：完整产物','dot',size=11)
line([(270,202),(306,202)],COL['cloud']);line([(536,202),(572,202)],COL['dot'])
table(40,310,W-80,['数据类型','网站 / 本机','公开知识 Git'],[
 ('私密任务正文、分类报告、授权和运行账本','私有存储；按权限访问','不提交'),
 ('脱敏后的 PDF、HTML、实验与合并知识笔记','保留原件及审核记录','明确检查后才提交'),
 ('密码、会话 token、OAuth 凭据、服务配置','各自环境内保管；不可进入报告','不提交')],[335,222,205],fs=10.2)
note(464,'额外电脑连接是另一个权限','官方支持 Dot 连接个人电脑，但它扩大了能力范围。网站只准访问某个列表，并不能约束 Dot 在其他已连接应用或电脑中的全部权限。',h=61)

# 08
page('两段大模型链路','网站摘要与 Dot 完整学习：目的不同','网站摘要帮助找回“这是什么”；Dot 的学习流程帮助回答“我能理解并运用什么”。',key='cloud',source='server.js 摘要队列；learn-project')
box(40,138,177,125,'原始链接','手机保存\n进入本人任务\n记录来源版本','mobile',size=11)
box(289,138,513,125,'路径 A · 站点摘要','阿里云抓取公开网页文本；X 可尝试第三方文本接口 → 配置了 Kimi Key 时调用摘要模型 → 写中文摘要。失败保留任务或回退网页摘录。','cloud',role='运行：阿里云服务；模型请求：Kimi API',size=11)
line([(217,183),(289,183)],COL['cloud'],label='纯链接',lx=225,ly=164)
box(289,319,513,139,'路径 B · 深度学习','Dot 经 OAuth/MCP 读取获准任务 → 再核实原文和官方来源 → 调用学习方法 → 执行实验与独立审核 → 保存完整报告。不会只把摘要再改写一遍当作学习完成。','dot',role='运行：Dot 云端电脑',size=11)
line([(127,263),(127,388),(289,388)],COL['dot'],label='获准列表的任务',lx=140,ly=365)
note(479,'费用与准确性分别控制','摘要 API 有站点日限额；Dot 学习还受账户额度、工具与实验环境影响。摘要额度不能作为完整学习成本上限，第三方文本也不能代替作者或官方证据。',h=48)

# 09
page('分类与任务状态','先路由，再学习；“完成”仍由本人决定','分类阶段必须记录来源、判断依据、已有知识关联、下一步和未确认事项。',key='dot')
table(40,132,W-80,['分类','具体判据','下一步'],[
 ('learning / 学习','知识、教程、论文、原理或项目已核实','可领取且有权限时进入完整学习'),
 ('non_learning / 非学习','实质内容已读，确无本次学习主题','保存理由与相应标签'),
 ('duplicate / 重复增补','已学过相同内容，但需核对版本和差异','关联既有指南，只分析增补价值'),
 ('needs_review / 证据不足','原文 / 目标身份 / 出链未确认','补证据，不强行绑定搜索命中'),
 ('blocked / 环境受阻','目标明确，但执行或审核条件不足','写具体阻碍；同源不重复启动'),
 ('non_link / 非链接','原记录没有 HTTP(S)/www 链接','按正文处理；不等于无学习价值')],[190,340,232],fs=10)
note(462,'两条状态轴','分析标签：已完成完整分析 / 初步判定非项目学习类 / 非链接类，以及待核实等补充标签。任务状态：未开始 / 进行中 / 用户完成。智能体不调用旧 publish、done、viewed 来勾选任务。',h=66,key='cloud')

# 10
page('云端调度与互斥','十五分钟检查，不等于十五分钟学完','当前日程已保存并实际运行；它接续已派发票据，没有覆盖所有待分类和未来新增记录。',source='14:07 状态核对；日程回读；共享队列规则')
nodes=[('检查身份','本人账户 / 列表 / scope','cloud'),('筛选当前源','无保护 / 无他人 owner','dot'),('领取租约','每轮新唯一 owner','dot'),('学习并续约','同源 / 同项目串行','dot'),('保存并释放','回读报告和标签','cloud')]
for i,(t,b,k) in enumerate(nodes):
    x=40+i*155;box(x,147,142,112,t,b,k,size=9.7)
    if i<4:line([(x+142,203),(x+155,203)],COL[k])
table(40,301,W-80,['机制','当前作用','容易误会的地方'],[
 ('网站任务租约','保护 Dot 与本地后备执行者不同时写同一任务','过期仍不能随便抢占；409 要跳过'),
 ('本机 SQLite 队列','本目录内 owner、项目资源锁及验收台账','多个 Git 克隆并不共用这把锁'),
 ('唯一协调者租约','序列化 vault、纲要、网站标签与 Git 收尾','改名不能绕过别人持有的资源')],[172,295,295],fs=10)
note(464,'当前批次范围','已派发 18 张票中，MCP Toolbox 与 Colab 已云端交付；另 16 张尚未完整交付，其中 Metrik 正在执行。30 条待分类和今后新记录未派入此批。原本机十五分钟分类任务保持暂停。',h=62)

# 11
page('learn-project 方法','skill 把“读资料”拆成可交付的学习','skill 是可复用的作业方法，不是另一个模型，也不是自动授予权限的程序。',source='.claude/skills/learn-project/SKILL.md；云端执行说明')
steps=[('0 · 路由与初始化','确定类别；建目录；固定代码版本','dot'),('1–2 · 知识与摸底','读已发布笔记；看入口和最小示例','dot'),('3–4 · 疑问与讲解','10–15 个分层疑问；图 / 例子 / 故事','dot'),('5–6 · 能力与实验','3–6 个用途；3–7 步真实实验','dot'),('7 · 彩色产物与审核','PDF / HTML；逐页渲染；独立审核','dot'),('8–9 · 入库与 Git','概念合并 + MOC；明确文件提交推送','windows')]
for i,(t,b,k) in enumerate(steps):
    row=i//3;col=i%3;x=40+col*260;y=137+row*188
    box(x,y,242,130 if row else 139,t,b,k,role='Dot 云端' if k=='dot' else '本机唯一协调者',size=11)
    if col<2:line([(x+242,y+70),(x+260,y+70)],COL[k])
line([(661,276),(661,305),(161,305),(161,325)],COL['dot'],label='审核门槛贯穿每步',lx=294,ly=283)
note(483,'为什么更容易掌握','疑问决定讲解顺序，已有知识决定讲解深度，真实实验给出可验证反馈，能力清单说明可用场景，概念关联把一次学习接到下一次学习。',h=46,key='knowledge')

# 12
page('实验与六类交付','“跑过、看过、审过”必须有证据','六个文件是交付载体；文件检查能防缺件，不能证明内容正确或实验真实。',key='dot')
table(40,132,465,['原件角色','应该包含什么'],[
 ('guide_pdf','彩色图文指南；真实逐页渲染检查'),('guide_html','可编辑讲解源码；HTML 视觉检查单独记录'),('exercise_archive','真实自建练习 ZIP；不带依赖 / 密钥 / 模型'),('experiment_log','环境、时间、完整命令、输出、结果与限制'),('knowledge_notes','概念、关联、查重范围与入库提案'),('review_log','真实独立审核者及具体意见')],[161,304],fs=10.2)
box(533,135,269,149,'实验的四个问题','怎么操作？完整命令。\n为什么做？验证一个假设。\n看到了什么？实际输出。\n怎么算通过？成功与负对照。','dot',size=11)
box(533,304,269,132,'独立审核','另一个实际审核者检查来源、实验日志和 PDF。改个 owner 名字，不能替代独立复跑或阅读。','windows',size=11)
note(464,'云端限制要写在报告里','当前网站六类文件合计上限 1 MB。HTML 浏览器预览受阻时，不冒充视觉通过；可用实际可执行的 PDF 生成工具并记录路径。超限或缺审核能力保留受阻。',h=62)

# 13
page('Dot 如何使用 skill','方法和知识以固定版本传到云端','本机 F:\\reminder 不是 Dot 云端磁盘。读取方法、执行工具与连接本机，是三个不同动作。',source='RUNNING_IN_DOT.md；reminder_dot_reference.py；官方说明 [S1]')
box(40,139,223,134,'已发布知识仓库','固定 commit 的 SKILL.md\n按标题和指纹生成索引\n只包含已发布概念 / 项目笔记','git',size=10.5)
box(306,139,223,134,'Dot 读方法','reminder_learning_guide\n读取原 skill 和相关笔记\n记录实际读到的版本及依据','dot',size=10.5)
box(572,139,230,134,'Dot 执行方法','在云端新建项目目录\n按实有工具配置实验\n不照抄 Windows 专属命令','dot',size=10.5)
line([(263,208),(306,208)],COL['knowledge']);line([(529,208),(572,208)],COL['dot'])
box(40,320,368,118,'索引不是最新本机知识库','未提交的 Obsidian 手动笔记、私密记录和整台电脑不在云端索引。云端查重先给范围声明；回迁后本机再次查重合并。','knowledge',size=11)
box(430,320,372,118,'读不到 raw 网页时怎么办','记录原失败，再通过实际可用的 Git 对象完整读取同一固定文件；用 commit、blob、SHA256 追溯。不能把搜索摘要当作 skill 已完整读取。','git',size=11)
note(463,'“安装了 skill”不能凭口头确认','官方指出本地 skills 需要连接电脑。当前云端方案是把方法作为可追溯输入读取，并实际执行；本次不声称本机 skill 已自动挂载到 Dot。',h=64)

# 14
page('云端成果回迁','先复制校验，再入库，最后推送 Git','这五个成功状态分别记账；其中任何一步等待，都不能称“全部完成”。',key='windows',source='reminder_dot_backup.py；handoff；confirm-analysis')
for i,(t,b,k) in enumerate([('网站保存','私有报告 + 六原件','cloud'),('本机备份','校验 SHA256 / 范围','windows'),('知识入库','概念查重 + MOC','knowledge'),('Git 提交','审核后明确文件','git'),('Git 推送','远端 SHA 回读','git')]):
    x=40+i*155;box(x,145,142,110,t,b,k,size=9.8)
    if i<4:line([(x+142,200),(x+155,200)],COL[k])
box(40,309,367,131,'固定脚本：只负责搬运','用户登录 Windows 时拉取私有副本，验证文件、来源和账户列表，更新 handoff.json。重复拉取不重复计数，不删除云端原件。','windows',role='tools/reminder_dot_on_login.ps1',size=10.2)
box(430,309,372,131,'协调者：负责理解与交付','核对当前 sourceHash 与原 owner，把练习整理到现有项目目录，合并 vault，独立审核并 confirm-analysis，再按明确清单完成 Git 收尾。','knowledge',role='Windows 的唯一知识协调者',size=10.2)
note(464,'目前尚未打通的最后一公里','Dot 向当前本机既有聊天的正式投递返回 placement-v1 / NOT_FOUND，自动唤醒未通过。登录备份已运行，不代表本机智能体会自动合并知识或推送。',h=62)

# 15
page('Obsidian 知识网络','同一个概念，连接多个项目','下图依据现有 MCP Toolbox 项目笔记中的关联绘制；是讲解布局，不是软件截图。',key='knowledge',source='vault/项目笔记/mcp_toolbox.md；Obsidian 官方 [S4][S5]')
box(40,169,204,102,'项目笔记 / mcp_toolbox','用途、实验、版本和局限\n连接五条已有概念笔记','windows',size=10)
box(337,131,242,88,'MCP 协议','解释工具如何被模型发现和调用','knowledge',size=10)
box(337,271,242,88,'只读闸门三原则','用真实拒绝证明边界有效','knowledge',size=10)
box(337,411,242,88,'代码管边界，提示词管判断','工具注解不等于强制访问权限','knowledge',size=9.8)
box(640,200,162,106,'下一次新项目','查旧概念 → 找差异\n用新实验增补证据\n保留版本和来源','dot',size=9.8)
line([(244,190),(288,190),(288,175),(337,175)],COL['knowledge'],label='[[链接]]',lx=251,ly=154)
line([(244,235),(285,235),(285,315),(337,315)],COL['knowledge'])
line([(244,257),(270,257),(270,455),(337,455)],COL['knowledge'])
line([(579,175),(613,175),(613,226),(640,226)],COL['dot'])
line([(579,315),(613,315),(613,267),(640,267)],COL['dot'])
para(640,353,161,'同义概念：合并 + 别名。\n相关概念：互相链接。\n项目：连接概念和实验。\n总览：给导航和主题主线。',10.3,leading=19)
para(40,333,206,'图谱里的“边”来自笔记中的 [[内部链接]]。节点数量不能代表掌握程度；看能否说清关系和完成迁移任务。',10.4,COL['muted'])

# 16
page('每日巩固框架','让本人回忆，再让 AI 给反馈','已存在每日复习日程的历史记录；本次未复核其时间、内容或评分回写。以下为建议的完整复习设计。',key='knowledge',source='既有日程记录；主动回忆研究 [S8]；建议模板')
for i,(t,b) in enumerate([('挑 3–5 个概念','来源明确、近期新学 / 上次薄弱'),('闭卷说清楚','定义、为什么、机制、反例'),('动手做一小步','改参数 / 负对照 / 迁移场景'),('对照证据反馈','标出错因；回链笔记和实验'),('保存复习结果','本人确认评分；安排下一次')]):
    x=40+i*155;box(x,145,142,125,t,b,'knowledge',size=9.8)
    if i<4:line([(x+142,207),(x+155,207)],COL['knowledge'],dashed=True)
box(40,321,366,126,'轻量评分：0 / 1 / 2','0：说不清，先看证据并次日重试。\n1：能解释但不会用，补一个小实验。\n2：能独立迁移，下次复习间隔拉长。','knowledge',size=11)
box(430,321,372,126,'示例节奏：1 / 3 / 7 / 14 / 30 天','这是可调整的排程例子，不是本项目已经实现的复习算法，也不承诺统一最优。每天 10–15 分钟；用实际答题质量调整。','dot',size=11)
note(471,'资料生成与本人掌握是两件事','看完 PDF 可算阅读；能复述、实验和迁移才是掌握。Dot 在电脑离线时可基于公开笔记提问，但私有本机评分和未提交笔记需要上线后由本人 / 协调者合并。',h=54)

# 17
page('已验证进展','一条真实交付链，四项云端报告','以下为 2026-10-05 14:07 的核验快照；不是未来完成率、速度或 SLA 承诺。',key='windows',source='网站真实回读 / 私有备份；公开 Git 远端')
table(40,132,W-80,['项目','云端完整报告保存（北京时间）','本机 / Git 状态'],[
 ('HowToLiveBetter','11:56；11 页 PDF','入库并推送：35530fb'),('Ponytail','12:23；10 页 PDF','入库并推送：cffbee0'),('MCP Toolbox','13:00；13 页 PDF','入库并推送：109ffa9'),('Google Colab CLI','13:47；六类真实原件','完整性校验备份；待本机内容复核和 Git'),('Metrik','14:02 左右领取 full，源码已固定','正在学习；未交付完整报告')],[199,285,278],fs=10.4)
box(40,396,365,114,'代码与学习成果分开看','本机配套工具提交 8536dae 尚未推送。公开知识 main 已实际回读为 109ffa9。不要把本机 commit 当成远端已更新。','git',size=10.5)
box(430,396,372,114,'质量证据也分运行位置','MCP Toolbox 的 Linux 程序在云端运行并独立复跑；Windows 校验包、源码、日志和 PDF。没有把云端实验计为 Windows 实验。','dot',size=10.5)

# 18
page('搭建 00 / 先准备','先决定复用服务，还是自建一套','本手册示例沿用本人实例；朋友可先体验公开学习成果，接入私人任务需要独立权限配置。',key='windows')
table(40,130,W-80,['需要准备','为什么需要','先验收什么'],[
 ('网站源码访问权','reminder 是私有仓库，未授权会 404 / 拒绝访问','仓库拥有者确认只读 / 部署权限'),('阿里云 ECS + 域名 / HTTPS','保存正式任务与 MCP 服务','SSH 登录；服务入口配置'),('合资格 Dot 账户','使用云端电脑、插件和日程','本人可创建 / 使用 Dot；工具可实际运行'),('Windows：Git / Python / PowerShell 7','拉取私有副本和知识协调','版本可查询；路径可写'),('Obsidian + 公开知识仓库','打开 vault，建立链接与复习','能打开现有 Markdown 笔记'),('无凭据的配套工具包','当前公开 main 没有最新 pipeline / Dot 工具','只安装显式工具，不复制运行数据')],[222,286,254],fs=10)
note(462,'新手命令的边界','以下命令按源码、CLI help 和官方文档核对；本次没有替读者新建云服务器、安装软件或重部署生产。占位符必须替换；成功标准写在每页，不能把未运行的命令当成已验收。',h=65)

# 19
page('搭建 01 / Ubuntu 本地','准备运维终端与服务器连接','Ubuntu 保管网站代码与运维连接；它不会把 Windows 的最终知识目录当服务器的数据目录。',key='ubuntu')
y=code(40,137,452,r'''git --version
ssh -V
node --version
git clone https://github.com/Smashwinny/reminder.git
cd reminder
git status --short
git log -1 --oneline''',label='Ubuntu 本地 / Bash',size=9.2)
box(524,138,278,150,'每组命令做什么','检查 Git / SSH / Node。\n克隆已获权限的私有网站仓库。\n确认工作区与当前版本。\nNode 22 对应当前容器版本。','ubuntu',size=10.8)
y=code(40,y+17,452,r'''node --test sync-server/server.test.js
ssh -i /PRIVATE/PATH/key ADMIN@ECS_HOST''',label='先测代码，再进入阿里云；连接信息自行替换',size=8.9)
box(524,310,278,135,'预期结果 / 故障处理','测试通过后再准备部署。\nSSH 成功看到服务器主机名。\n仓库 404 先核权限，不找旧公网入口。\n有未提交改动先保留，不能自动 reset。','ubuntu',size=10.5)
note(476,'版本与已有生产','当前生产曾验收固定版本 97ef3cc；新建时使用负责人确认的含 Dot 集成版本。生产已有数据时先完整备份和核对差异，不能照抄“首次部署”覆盖现有目录。',h=49)

# 20
page('搭建 02 / 阿里云服务器','安装 Docker 与 Compose v2','只在全新、获准运维的 Ubuntu ECS 执行。已有 Docker 时先检查版本，不混装或删除现有服务。',key='cloud',source='Docker 官方 Ubuntu 安装步骤 [S6]；项目使用 Compose v2')
code(40,130,W-80,r'''sudo apt update
sudo apt install -y ca-certificates curl git
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo docker compose version
sudo docker run --rm hello-world''',label='阿里云服务器 / Bash · 官方 APT 仓库安装',size=8.6)
note(462,'预期结果','docker compose version 返回 v2 或更新的官方插件；hello-world 给出成功输出。容器端口仍按本项目绑定 127.0.0.1，不通过开放 8787 公网端口解决连通问题。',h=62,key='cloud')

# 21
page('搭建 03 / 阿里云服务器','部署站点，先让手机与网页同步','下面以新目录 /opt/reminder 为例；先完成普通站点，再配置 Dot 四项门控变量。',key='cloud',source='deploy/install.sh；docker-compose.yml；.env.example')
code(40,133,484,r'''sudo install -d -m 0750 -o "$USER" /opt/reminder
git clone https://github.com/Smashwinny/reminder.git /opt/reminder
cd /opt/reminder
umask 077
cp deploy/.env.example deploy/.env
openssl rand -hex 24
nano deploy/.env
touch deploy/kimi.key
chmod 600 deploy/.env deploy/kimi.key
sudo docker compose -f deploy/docker-compose.yml up -d --build
sudo docker compose -f deploy/docker-compose.yml ps
curl -fsS http://127.0.0.1:8787/api/healthz''',label='阿里云服务器 / Bash',size=8.65)
box(547,136,255,180,'必须人工填写','把随机邀请码填入 .env。\nKimi 摘要可选：Key 仅填 kimi.key。\nDot 账户和 callback 等下一步确定。\n不要把随机值、Key 或 .env 发到 Issue / Git。','cloud',size=11)
box(547,335,255,124,'预期结果','容器 reminder_app 健康。\n数据在 reminder_data 卷。\n本机 healthz 返回成功。\n外网稍后经 HTTPS 入口访问。','cloud',size=10.4)
note(480,'两种首次部署方式选一种','也可在已配置好 .env 的新实例运行 sudo sh deploy/install.sh：会创建缺失的空 kimi.key 并检查容器 / 端口冲突。发现已有实例则停止，转入负责人审核的更新流程。',h=46)

# 22
page('搭建 04 / 阿里云服务器','把 HTTPS 入口和备份接好','当前实例使用 Cloudflare 命名隧道；新读者可采用自己的隧道或 Nginx / 证书，二选一。',key='cloud')
box(40,133,363,131,'入口配置：Cloudflare 路线','在 Cloudflare 配置自己的域名与命名隧道，服务指向 http://127.0.0.1:8787。官方安装 cloudflared；私密 token 文件按服务模板路径保存并限制权限。','cloud',size=10.8)
box(431,133,371,131,'入口配置：Nginx 路线','参考 deploy/nginx-reminder.conf.example，换成本人域名与已取得的有效证书；nginx -t 通过后加载。已有入口由原运维者维护，不新增第二个正式数据源。','ubuntu',size=10.8)
code(40,291,762,r'''cd /opt/reminder
sudo cp deploy/reminder-backup.service deploy/reminder-backup.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now reminder-backup.timer
sudo sh deploy/backup.sh
sudo systemctl status reminder-backup.timer
curl -fsS https://YOUR_DOMAIN/api/healthz''',label='服务器备份和公网验证 / Bash · YOUR_DOMAIN 换成自己的域名',size=9.0)
note(449,'备份验收与时区','保留压缩备份及 .sha256，复制到独立私有位置并测试恢复。模板 OnCalendar=03:20 使用服务器时区并带随机延迟；查 timedatectl 后确定实际时间，不把同机卷副本当异机备份。',h=70)

# 23
page('搭建 05 / 浏览器 + 阿里云','用私有 MCP / OAuth 连接本人 Dot','这一步在界面中完成，不存在本项目已经验证的“一条 CLI 命令连接 Dot”。',key='dot',source='连接本人 Dot 流程；官方 OAuth [S3]')
table(40,131,W-80,['在哪里','操作','核对结果'],[
 ('ChatGPT 桌面 / 浏览器','创建私有 MCP 应用；MCP URL 为 https://reminder.geniusqi.com/mcp','自建实例替换自己的域名'),('同一应用配置界面','选择预定义自定义 OAuth 公共客户端；确定 client ID；复制精确 callback','callback 不能猜、不能沿用别人草稿'),('阿里云 deploy/.env','填写 DOT_ALLOWED_USER_ID / DOT_PUBLIC_ORIGIN / DOT_OAUTH_CLIENT_ID / DOT_OAUTH_REDIRECT_URI','账户用 canonical UUID；四项齐备才开放'),('网站 /dot 管理页','本人登录；选择获准列表及是否自动加入以后新增记录','列表真实成员和 future auto-add 分别确认'),('本人 OAuth 同意页','核对账户、列表与三个 scope；本人确认同意','records.read + analysis.write + learning.write'),('Dot 私密对话','调用 reminder_identity 并实际回读','身份 / listId / 权限 / 模式符合本人选择')],[153,367,242],fs=9.4)
note(474,'配置变更后的验收','运维者审核配置后更新 Reminder app，再检查 discovery 与真实 OAuth；未授权 MCP POST 应拒绝。临时哨兵 ID 被拒绝不能证明真实跨账户 / 跨列表隔离，需要用受控测试账户验证。',h=53)

# 24
page('搭建 06 / Dot 云端','让 Dot 先证明会学习，再保存日程','先做一条真实、来源可读的小项目；连接成功与完整学习成功分别验收。',key='dot')
box(40,135,368,154,'交给 Dot 的材料','当前 README / 学习指南、原 learn-project 方法、固定版本知识索引、明确允许列表和本批次任务范围。没有把 F: 盘作为云端路径，也没有把本机 token 发给 Dot。','dot',size=11)
box(431,135,371,154,'首条实测','identity → preliminary 领取 / 来源核实 / 保存 / 回读 / 释放 → full 领取 / 真实实验 / PDF / 独立审核 → 六原件保存 / 标签回读 / 释放。','dot',size=11)
rect(40,314,W-80,143,TINT['dot'],r=9)
txt(56,329,'可复制给 Dot 的启动指令（摘要版）',12,COL['dot'],True)
para(56,355,W-112,'请先核对拾遗插件的本人账户、一个允许列表和三个权限。读取学习指南及固定版本 learn-project；只学习来源已核实、无其他 owner 的记录。按方法做真实实验、彩色 PDF、知识提案和独立审核，保存六类原件并回读标签，完成勾选留给我。首条全部验收后，再确认保存每 15 分钟、Asia/Shanghai 的日程，明确本批范围，异常单独记录，同一故障不反复通知。',11.4,leading=20)
current_md.extend(['### 可复制给 Dot 的启动指令','请先核对拾遗插件的本人账户、一个允许列表和三个权限。读取学习指南及固定版本 learn-project；只学习来源已核实、无其他 owner 的记录。按方法做真实实验、彩色 PDF、知识提案和独立审核，保存六类原件并回读标签，完成勾选留给我。首条全部验收后，再确认保存每 15 分钟、Asia/Shanghai 的日程，明确本批范围，异常单独记录，同一故障不反复通知。',''])
note(476,'日程必须实际 list 回读','确认 enabled、时区、周期、保存的完整指令和目标环境。一次 run_now 成功不保证长期调度、严格时点或跨回合绝对串行；日程范围不能自动扩大到清单外任务。',h=49)

# 25
page('搭建 07 / Windows 本地','先准备知识仓库与配套工具','以下假设新机器 F:\\reminder 不存在。已有目录只检查状态，不覆盖、重置或重新 clone 到里面。',key='windows',source='WinGet 官方 [S7]；公共仓库文件清单；配套包')
code(40,132,470,r'''winget install --id Git.Git -e
winget search --id Microsoft.PowerShell -e
winget search --id Python.Python.3.12 -e
winget install --id Microsoft.PowerShell -e
winget install --id Python.Python.3.12 -e
# 关闭并重开 PowerShell 7，检查实际解释器
git --version
pwsh --version
python --version
git clone https://github.com/Smashwinny/reminder_knowlege.git F:\reminder
Set-Location F:\reminder''',label='Windows / PowerShell 7 · 软件许可提示由本人处理',size=8.5)
box(533,133,269,157,'为什么还有配套包','当前公开 main 只有历史 tools。本次附最新无凭据工具的白名单快照；不能只 clone 后就假定已有 pipeline / Dot 回迁命令。','windows',size=11)
box(533,311,269,148,'安装工具的顺序','先解压随附包到临时目录。\n阅读本机工具补齐/README.md。\n只在新干净 clone 中复制明确文件。\n已有工作区逐文件比较，由协调者合并。','windows',size=10.5)
note(482,'预期结果','Git、Python、pwsh 均可查询版本；tools/reminder_dot_backup.py 与 reminder_pipeline.py 存在。这里只准备备份环境，不启动旧本机周期学习。',h=44)

# 26
page('搭建 08 / Windows 本地','私密配置账户、列表和本机凭据','Dot OAuth 与本机网站会话是两种凭据；本机凭据从已有环境变量或私有 token 文件读取。',key='windows')
code(40,133,465,r'''Set-Location F:\reminder
New-Item -ItemType Directory -Force 完成/.pipeline
Copy-Item reminder-dot/dot-backup-config.example.json `
  完成/.pipeline/dot-backup-config.json
notepad 完成/.pipeline/dot-backup-config.json
# 在私密终端输入已有本机网站会话 token
$reminderSecret = Read-Host '网站会话 token' -AsSecureString
$env:SHIYI_TOKEN = `
  [System.Net.NetworkCredential]::new('', $reminderSecret).Password
python tools/reminder_dot_backup.py --help''',label='Windows / PowerShell 7 · 不把 token 写在命令参数中',size=8.6)
box(529,135,273,157,'配置文件只填写两项','accountId：identity 核对的 canonical 账户 UUID。\nlistId：本人允许列表 UUID。\n来自私密授权回读，不能按名字猜或复制本人的值给朋友。','windows',size=11)
box(529,312,273,137,'没有既有 token 时','在本人私密终端通过网站正式登录建立本机会话。配套包提供 getpass 登录示例，拒绝重定向且不打印 token；不要使用旧 login 命令把密码写到命令行。','cloud',size=10.4)
note(474,'会话保存的范围','临时 SHIYI_TOKEN 只在当前进程生效，不能供以后登录任务复用。需要自动登录备份时，将正式取得的会话安全保存到 tools/.shiyi_token 并限制本机读取权限；它不授予 Dot 电脑权限。',h=53)

# 27
page('搭建 09 / Windows 本地','执行一次备份，再注册登录触发','触发器名为 Reminder-Dot-Backup-OnLogon；它只复制产物，不启动模型、vault 合并或 Git。',key='windows',source='install_reminder_dot_backup_trigger.ps1；备份入口')
code(40,136,470,r'''Set-Location F:\reminder
& ./tools/reminder_dot_on_login.ps1
& ./tools/install_reminder_dot_backup_trigger.ps1 -WhatIf
& ./tools/install_reminder_dot_backup_trigger.ps1
Get-ScheduledTask -TaskName Reminder-Dot-Backup-OnLogon
Get-ScheduledTaskInfo -TaskName Reminder-Dot-Backup-OnLogon
python tools/reminder_pipeline.py status''',label='Windows / PowerShell 7',size=8.9)
box(534,138,268,157,'一次备份的通过标准','账户 / 列表一致。\n报告 Markdown 与六原件 SHA256 一致。\n重复备份新增 0，不覆盖冲突副本。\ncloudDeleted 为 false。','windows',size=11)
box(534,315,268,135,'到哪里找文件','完成/.pipeline/dot/账户/列表/\nreports/：私有报告与文件\nexports/：原始导出\nhandoff.json：各阶段交接账本','windows',size=9.9)
note(464,'启动方式必须分别验收','首次手动备份成功，再看注册触发器回读和真实登录执行结果。机器离线、会话过期或配置缺失时保留待同步；一次创建成功不等于每次启动都可靠。',h=64)

# 28
page('搭建 10 / 本机协调者','把备份变成合格的知识交付','以下是操作骨架；manifest、审核意见和确认回执必须来自实际产物，不能填占位值骗过验收。',key='windows')
code(40,131,762,r'''python tools/reminder_coordinator.py status
python tools/reminder_coordinator.py acquire --owner coordinator_example
python tools/reminder_pipeline.py sync
python tools/reminder_pipeline.py status --task TASK
# 仅已 classify 为 learning；已有 start 票据跳过 claim/start
python tools/reminder_pipeline.py claim --task TASK --owner ORIGINAL_OWNER
python tools/reminder_pipeline.py start --task TASK --owner ORIGINAL_OWNER --project PROJECT
# 整理真实文件、合并 vault、由另一位审核者审阅
python tools/reminder_pipeline.py ready --task TASK --owner ORIGINAL_OWNER `
  --manifest PROJECT/manifest.json
python tools/reminder_pipeline.py review --task TASK --owner ORIGINAL_OWNER `
  --reviewer REVIEWER --notes "实际审核意见"
python tools/reminder_pipeline.py confirm-analysis --task TASK --owner ORIGINAL_OWNER `
  --coordinator coordinator_example --receipt PRIVATE_RECEIPT.json
python tools/reminder_pipeline.py render
# 保持协调者租约：下一页 Git 收尾后再 release''',label='协调者操作骨架 / PowerShell 7 · Bash 换行使用反斜杠',size=8.8)
para(40,429,762,'manifest：topic、project_dir、pdf、html、exercise_dir、experiment_log、vault_note、source_urls；使用真实仓库相对路径。',9.4)
para(40,459,762,'receipt：schema、accountId、listId、taskId、reportId、sourceHash、backupBundle、backupSha256、handoff；只留私有 .pipeline。',9.4)
para(40,490,762,'已有 start 票据不再次 claim / start；原 owner 续约。确认只读网站来源并释放资源。真实独立审核必须先完成，任务勾选仍留给本人。',10,COL['windows'],True)
current_md.extend(['manifest：topic、project_dir、pdf、html、exercise_dir、experiment_log、vault_note、source_urls；使用真实仓库相对路径。','receipt：schema、accountId、listId、taskId、reportId、sourceHash、backupBundle、backupSha256、handoff；只留私有 .pipeline。','已有 start 票据不再次 claim / start；原 owner 续约。新任务先通过初步分类。配套命令手册给出 classify 与续租命令。真实独立审核必须先完成，任务勾选留给本人；协调者租约保持到 Git 收尾。',''])

# 29
page('搭建 11 / 本机 Git 协调','只提交审核过的学习成果','当前使用独立公开知识发布副本隔离私有网站历史；不把整个工作分支直接推到公开仓库。',key='git')
code(40,132,510,r'''git -C 完成/.pipeline/knowledge-publication status --short
git -C 完成/.pipeline/knowledge-publication diff --cached --name-only
# 暂存区归属明确且已知；按本次审核文件逐个列出
git -C 完成/.pipeline/knowledge-publication add -- `
  PROJECT/guide.pdf PROJECT/guide.html `
  PROJECT/exercise/main.py PROJECT/experiment_log.txt `
  vault/项目笔记/PROJECT.md vault/概念/CONCEPT.md vault/00-总览.md
git -C 完成/.pipeline/knowledge-publication diff --cached --stat
git -C 完成/.pipeline/knowledge-publication diff --cached
git -C 完成/.pipeline/knowledge-publication commit -m "learn: 项目指南与实测知识入库"
git -C 完成/.pipeline/knowledge-publication push origin main
git -C 完成/.pipeline/knowledge-publication rev-parse HEAD
git -C 完成/.pipeline/knowledge-publication ls-remote origin refs/heads/main
python tools/reminder_coordinator.py release --owner coordinator_example''',label='Windows 唯一协调者 / PowerShell · 文件名按真实交付替换',size=7.6)
box(574,134,228,162,'通过标准','已核对指南、日志、笔记不含私密原记录。\n提交 hooks 通过。\n推送后的远端 main SHA 与本次 commit 相同。\n账本再记 pushed + SHA。','git',size=10.4)
box(574,317,228,130,'出现拒绝或冲突','保留本次文件与提交，先核对远端。\n共享工作区不自动 rebase / reset。\n不强推，不跳 hooks，不全仓 add。','amber',size=10.3)
note(478,'独立发布副本的初始化','先 clone 已确认的公开知识仓库到上述目录；仅复制明确审核文件。新手自己 fork 时更新远端目标，核对仓库可见性，不能将私人学习内容默认公开。',h=47)

# 30
page('搭建 12 / Obsidian 与换机','打开 vault，让概念成为可点击的网络','Obsidian 的 vault 是一个本地文件夹；没有“上传到 Obsidian 服务器”这个必需步骤。',key='knowledge',source='Obsidian 内部链接与图谱 [S4][S5]')
box(40,133,366,143,'Windows 界面步骤','安装并打开 Obsidian → 打开已有文件夹为 vault → 选择 F:\\reminder\\vault → 打开 00-总览.md → 点项目笔记和 [[概念链接]] → 打开图谱 / 当前笔记局部图谱。','knowledge',size=11)
box(430,133,372,143,'知识入库的四个动作','新概念写一句话定义和证据。\n同义概念合并，保留别名。\n相关概念互链，注明关系。\n项目笔记链接指南、实验并更新总览。','knowledge',size=11)
code(40,307,762,r'''git clone https://github.com/Smashwinny/reminder_knowlege.git REMINDER_NEW_DEVICE
cd REMINDER_NEW_DEVICE
git status --short
git pull --ff-only
# Obsidian 里打开 REMINDER_NEW_DEVICE/vault''',label='换机首次 clone；已克隆且工作区干净才 pull / Bash 或 PowerShell',size=9.0)
note(442,'同步与写入纪律','Git 同步 Markdown 和已审核学习文件；私人备份另走安全渠道。未提交的手动笔记先保留并明确合并，不能靠 pull 覆盖。换机阅读可以；多台同时学习或写 vault 需要重新协调唯一写入者。',h=77)

# 31
page('搭建 13 / 每日复习','把复习责任交给 Dot，把评分留给本人','下面是建议的日程指令；本次只交付手册，未修改已有复习日程或新增自动化。',key='knowledge')
rect(40,131,478,220,TINT['knowledge'],r=9)
txt(55,147,'给 Dot 的可复制复习指令',12,COL['knowledge'],True)
para(55,177,448,'每天北京时间 20:30，基于已发布且能实际读取的知识笔记，挑 3–5 个近期概念或我上次答错的概念，先只给问题，不给答案。问定义、原理、一个反例和一个迁移用途；我回答后再用原笔记和真实实验证据反馈。请生成带日期的复习草稿，记录我的原回答、0/1/2 评分建议、错因和下次日期，待我确认。本机离线只留云端草稿；上线后由唯一协调者合并 vault。不要读取获准范围外的私密记录，也不要把评分写进任务完成状态。请确认日程实际保存结果。',11.3,leading=20)
current_md.extend(['### 可复制给 Dot 的复习指令（建议，尚未实施）','每天北京时间 20:30，基于已发布且能实际读取的知识笔记，挑 3–5 个近期概念或我上次答错的概念，先只给问题，不给答案。问定义、原理、一个反例和一个迁移用途；我回答后再用原笔记和真实实验证据反馈。请生成带日期的复习草稿，记录我的原回答、0/1/2 评分建议、错因和下次日期，待我确认。本机离线只留云端草稿；上线后由唯一协调者合并 vault。不要读取获准范围外的私密记录，也不要把评分写进任务完成状态。请确认日程实际保存结果。',''])
box(547,134,255,148,'建议新增的笔记','vault/复习/日期.md\n概念链接 + 问题\n本人回答 + 错因\n评分建议 + 本人确认\n下一次复习日期','knowledge',size=10.7)
box(547,302,255,128,'日程回读要看','Asia/Shanghai / 每日时点\n复习来源和范围\n是否等待本人回答\n通知方式与无变化时静默','dot',size=10.7)
note(454,'与十五分钟学习日程分开','学习调度负责加工新资料；复习日程负责检验本人能否回忆和应用。本机评分数据库与间隔算法尚未验收，模板需首次答题和写回验证后才能称已运行。',h=68)

# 32
page('系统联调验收','用一条真实链接走通十个检查点','这是一份可执行的验收清单；仅在本人受控账户和允许列表里试运行。',key='windows')
table(40,131,W-80,['检查点','实际通过标准'],[
 ('1 · 手机保存 / 同账号回读','电脑网站能看到同一任务；正文与 ID 一致'),('2 · HTTPS / 服务健康','域名健康端点成功；数据卷可持续保留'),('3 · 身份 / 范围 / 隔离','identity 与本人范围一致；受控清单外 / 他人账户真实测试被拒绝'),('4 · 初步分类','实际读原来源；有理由、知识关联、下一步；回读后释放'),('5 · full 领取与互斥','同源、同项目无并行；唯一 owner；已有租约不抢占'),('6 · 实验 / PDF / 独立审核','真实命令日志；逐页无排版问题；独立检查记录'),('7 · 网站完整报告','六原件及完整标签可回读；任务 state 不由智能体更改'),('8 · 本机备份','全部 SHA256 相同；重复拉取新增 0；云端原件保留'),('9 · 入库 / Git','概念关联可点击；远端 SHA 确认；私密原文不公开'),('10 · 本人复习与完成','先答题看反馈；由本人点击任务完成；标签仍保留')],[219,543],fs=9.3)

# 33
page('附录 A / 工具介绍','每个工具的优势与本项目边界','工具负责不同环节；“连了工具”仍需要业务规则、权限和验收。',key='git')
table(40,131,W-80,['工具','在本系统里的优势','使用边界'],[
 ('Reminder / 拾遗','低摩擦记录；手机网页同账号；任务和报告关联','网站是正式源，旧本机服务不能重新成为第二源'),('Dot','云端电脑与长任务协调；机器关机仍可云端工作','实际工具、权限、额度与环境会限制任务'),('learn-project skill','统一疑问、讲解、能力、实验、产物和知识沉淀','方法本身不是执行引擎；必须真的运行'),('MCP + OAuth','把限定工具和授权范围提供给智能体','工具提示不是安全权限；服务端逐请求检查'),('Obsidian','本地 Markdown、双链、局部图谱、可迁移','图谱是笔记关联视图，不能证明本人掌握'),('Git / GitHub','版本历史、可回溯变更、多设备传递学习成果','公开仓库不是私密备份；不能替代任务租约'),('Docker / Compose','可移植的站点运行配置与独立数据卷','卷需要异机备份；多副本不能直接共享 JSON 写入')],[142,303,317],fs=9.7)

# 34
page('附录 B / 排错与维护','先定位失败环节，再做对应修复','失败时保留原件和已有状态，不把缓存当本次网站真值，不用新 owner 绕开旧租约。',key='amber')
table(40,131,W-80,['现象','优先核对','下一步'],[
 ('链接只有壳 / 视频读不到','原文、作者、出链 / 字幕是否真实可访问','标证据不足；补公开来源或本人笔记'),('OAuth / MCP 503','四项 Dot 门控配置是否齐备并已生效','唯一运维者修配置；健康与 discovery 回读'),('401 / 授权失效','对应凭据类别、过期、scope 与 resource','正式私密重新连接；不打印 token'),('409 / 已有租约','任务、同源、项目和原 owner','跳过或原 owner 续约；不自动抢占'),('上传超出 1 MB','实际六类文件总大小','保留受阻；不能删关键证据伪装完整'),('备份通过但 Git 未更新','handoff 的知识入库 / commit / push 状态','协调者继续审核与明确文件推送'),('Git 暂存归属不明 / 远端拒绝','暂存清单、远端变更、当前协调者','保留现场；不 reset / 强推 / 自动 rebase'),('Dot 不能唤醒本机聊天','设备在线、正式路由与 PING / PONG 回执','当前 NOT_FOUND 未通过；不要归因于 OAuth'),('Obsidian 链接断了','vault 打开位置、笔记名、相对路径','修正 Markdown 链接；不重复生成同义概念')],[184,299,279],fs=9.1)

# 35
page('面向伙伴 / 演进路线','从个人闭环，走向可复制的产品','这是演进建议与验证指标；没有把个人实验包装成已验证的企业多租户平台。',key='dot')
for x,title,body,k in [(40,'现在 · 证明端到端价值','已拿到真实云端报告、实验证据、独立审核、本机知识与 Git。用一条真实学习项目演示，可让伙伴直接看到输入与产出。','dot'),(298,'下一步 · 补齐自动收尾','原生本机唤醒、票据续约、新记录派发、知识索引更新、复习写回都需明确验收。解决“报告完成后仍等协调者”的断点。','windows'),(556,'再扩展 · 才谈团队规模','多账户授权隔离、事务租约、分块产物存储、稳定事件触发、成本审计和恢复演练。现单进程 JSON 存储不直接扩成多副本。','cloud')]:box(x,132,246,193,title,body,k,size=11)
table(40,353,W-80,['向伙伴 / 投资人展示的指标','应该怎样测'],[
 ('来源核实率 / 可学习比例','真实输入中多少能确认目标；不可读与非学习分开'),('复现通过率 / 审核退回率','以实际实验和独立审核计算，不以文件存在计算'),('回迁与推送时延 / 恢复成功率','分别记录网站保存、本机入库、远端 push 的时间'),('七天后可解释和可迁移的比例','本人闭卷回答和小实验；没有实际数据不填提升百分比')],[347,415],fs=10.2)
para(40,519,W-80,'成本账：云服务器 / 域名、Dot 账户额度、摘要 API、实验资源、审核与协调投入分别记录；本手册没有给未经核对的价格或投资回报承诺。',8.7,COL['muted'])

# 36
page('附录 C / 依据与配套文件','这份讲解如何被核对和复用','报告为 2026-10-05 的架构与搭建快照；工具会变化，实际部署以负责人确认的版本为准。',key='git')
refs=[
 ('S1 · Dot 电脑与应用','https://learn.chatgpt.com/docs/dots/computers-and-apps'),
 ('S2 · Dot 任务与日程','https://learn.chatgpt.com/docs/dots/tasks-and-memory'),
 ('S3 · 官方 MCP / OAuth','https://developers.openai.com/plugins/build/auth'),
 ('S4 · Obsidian 内部链接','https://help.obsidian.md/links'),
 ('S5 · Obsidian 图谱','https://help.obsidian.md/plugins/graph'),
 ('S6 · Docker / Ubuntu','https://docs.docker.com/engine/install/ubuntu/'),
 ('S7 · Windows WinGet','https://learn.microsoft.com/en-us/windows/package-manager/winget/install'),
 ('S8 · 主动回忆原研究','https://pubmed.ncbi.nlm.nih.gov/16507066/')]
for i,(title,url) in enumerate(refs):
    yy=132+i*36;txt(40,yy,title,9.8,COL['git'],True);txt(233,yy,url,9.1,COL['windows'])
    CV.linkURL(url,(233,H-yy-13,W-40,H-yy+2),relative=0,thickness=0)
box(40,438,368,86,'项目依据','AGENTS.md、CLAUDE.md、原 learn-project、tools 工作流及 Dot 接入源码；最新状态按真实网站 / Git 回读覆盖旧文档的历史段落。','git',size=9.4)
box(430,438,372,86,'可编辑和可复制','随附 HTML / Markdown / 36 张 SVG 框图、白名单本机工具与命令文本。PDF 为矢量生成并逐页渲染验收；本次不修改网站或日程。','windows',size=9.4)

end_page()
assert page_num==36, page_num
CV.save()
(OUT/'拾遗到知识网络-架构与搭建指南.md').write_text('# 拾遗到知识网络：架构与搭建指南\n\n核验基线：2026-10-05 14:07 Asia/Shanghai。\n\n'+'\n\n---\n\n'.join(markdown_pages),encoding='utf-8')
html='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>拾遗到知识网络</title><style>@page{size:A4 landscape;margin:0}*{box-sizing:border-box}body{margin:0;background:#e7ecf5}.page{width:297mm;height:210mm;margin:12px auto;background:white;break-after:page;box-shadow:0 3px 18px #16233d22}.page svg{width:100%;height:100%}@media print{body{background:white}.page{margin:0;box-shadow:none}}@media screen and (max-width:1000px){.page{width:100%;height:auto;aspect-ratio:297/210}}</style><body>'''
html+=''.join('<section class="page" id="p'+str(i+1)+'">'+s+'</section>' for i,s in enumerate(svgs))+'</body></html>'
(OUT/'workflow_guide.html').write_text(html,encoding='utf-8')
(SRC/'diagrams').mkdir(exist_ok=True)
for i,s in enumerate(svgs):(SRC/'diagrams'/f'page_{i+1:02}.svg').write_text(s,encoding='utf-8')
(SRC/'layout_qa.json').write_text(json.dumps({'pages':page_num,'issues':qa,'pdf':PDF.name},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'pages':page_num,'pdf':str(PDF),'layoutIssues':qa},ensure_ascii=False))
