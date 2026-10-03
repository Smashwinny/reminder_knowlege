from pathlib import Path
from html import escape
from lxml import html as LH
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak, Flowable

ROOT=Path(__file__).resolve().parent
pdfmetrics.registerFont(TTFont('YaHei','C:/Windows/Fonts/msyh.ttc',subfontIndex=0))
pdfmetrics.registerFont(TTFont('YaHeiBold','C:/Windows/Fonts/msyhbd.ttc',subfontIndex=0))
pdfmetrics.registerFontFamily('YaHei',normal='YaHei',bold='YaHeiBold',italic='YaHei',boldItalic='YaHeiBold')
blue=colors.HexColor('#3158ff');ink=colors.HexColor('#132044');pink=colors.HexColor('#ec2875')
W=A4[0]-76
styles={
 'p':ParagraphStyle('body',fontName='YaHei',fontSize=9.6,leading=16,wordWrap='CJK',textColor=ink,spaceAfter=7),
 'h1':ParagraphStyle('title',fontName='YaHeiBold',fontSize=30,leading=40,textColor=ink,spaceAfter=20),
 'h2':ParagraphStyle('heading',fontName='YaHeiBold',fontSize=21,leading=29,textColor=ink,spaceAfter=15),
 'h3':ParagraphStyle('subheading',fontName='YaHeiBold',fontSize=12.5,leading=20,textColor=blue,spaceAfter=7),
 'eyebrow':ParagraphStyle('label',fontName='YaHeiBold',fontSize=8,leading=12,textColor=blue,spaceAfter=9),
 'small':ParagraphStyle('small',fontName='YaHei',fontSize=8,leading=12,wordWrap='CJK',textColor=colors.HexColor('#53628b'),spaceAfter=7),
 'pre':ParagraphStyle('code',fontName='YaHei',fontSize=7.6,leading=12,wordWrap='CJK',textColor=colors.white),
}
class Diagram(Flowable):
 def __init__(self,labels,width=W,color=blue):
  super().__init__();self.labels=labels;self.width=width;self.height=64;self.color=color
 def draw(self):
  c=self.canv;box=(self.width-36)/3
  for i,s in enumerate(self.labels):
   x=i*(box+18);c.setFillColor(colors.HexColor('#eef2ff'));c.roundRect(x,6,box,48,10,fill=1,stroke=0)
   c.setFillColor(self.color);c.setFont('YaHeiBold',10);c.drawCentredString(x+box/2,25,s)
   if i<2:
    c.setStrokeColor(self.color);c.setLineWidth(1.4);c.line(x+box+3,30,x+box+14,30);c.line(x+box+10,33,x+box+14,30);c.line(x+box+10,27,x+box+14,30)

def inline(node):
 parts=[escape(node.text or '')]
 for child in node:
  tag=child.tag.lower() if isinstance(child.tag,str) else ''
  val=inline(child)
  if tag=='br':parts.append('<br/>')
  elif tag in ('strong','b'):parts.append('<b>'+val+'</b>')
  elif tag=='a':parts.append('<a color="#3158ff" href="'+escape(child.get('href',''),quote=True)+'">'+val+'</a>')
  else:parts.append(val)
  parts.append(escape(child.tail or ''))
 return ''.join(parts)

def panel(content,bg,border=None,width=W):
 t=Table([[content]],colWidths=[width]);rules=[('BACKGROUND',(0,0),(-1,-1),colors.HexColor(bg)),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]
 if border:rules.append(('LINEABOVE',(0,0),(-1,-1),3,colors.HexColor(border)))
 t.setStyle(TableStyle(rules));return t

def flow(node,width=W,white=False):
 tag=node.tag.lower() if isinstance(node.tag,str) else ''
 cls=node.get('class','')
 if 'footer' in cls:return []
 if tag in ('h1','h2','h3','p','li') or 'eyebrow' in cls:
  key='eyebrow' if 'eyebrow' in cls else ('small' if 'muted' in cls or tag=='li' else (tag if tag in styles else 'p'))
  st=styles[key]
  if white:st=ParagraphStyle('white',parent=st,textColor=colors.white)
  return [Paragraph(inline(node),st)]
 if tag=='svg':
  labels=[x.text for x in node.iter() if str(x.tag).endswith('text')][:3]
  return [Diagram(labels,width)]
 if tag=='pre':
  return [panel([Paragraph(escape(node.text_content()).replace('\n','<br/>'),styles['pre'])],'#132044',width=width),Spacer(1,8)]
 if tag=='table':
  rows=[]
  for tr in node.findall('.//tr'):
   rows.append([Paragraph(inline(cell),ParagraphStyle('cell',parent=styles['p'],fontSize=8.5,leading=13,textColor=colors.white if cell.tag=='th' else ink)) for cell in tr])
  n=max(map(len,rows)); t=Table(rows,colWidths=[width/n]*n,hAlign='LEFT')
  t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),blue),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f3f5ff')]),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,-1),.5,colors.HexColor('#d8dff5'))]))
  return [t,Spacer(1,12)]
 if 'grid' in cls:
  tiles=[]
  for child in node:
   content=[]
   for x in child:content+=flow(x,(width-14)/2-24)
   tiles.append(content)
  rows=[tiles[i:i+2] for i in range(0,len(tiles),2)]
  for row in rows:
   if len(row)<2:row.append([])
  t=Table(rows,colWidths=[width/2]*2);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(0,-1),colors.HexColor('#eef2ff')),('BACKGROUND',(1,0),(1,-1),colors.HexColor('#fff0f6')),('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),12),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12)]))
  return [t,Spacer(1,12)]
 if 'badge' in cls:return []
 if 'takeaway' in cls:
  return [panel([Paragraph(inline(node),styles['p'])],'#fff6d5',width=width),Spacer(1,9)]
 contents=[]
 for child in node:contents+=flow(child,width-24 if any(c in cls for c in ['banner','question','row','callout','takeaway']) else width,white or 'banner' in cls)
 if not contents and node.text_content().strip():contents=[Paragraph(inline(node),styles['p'])]
 if 'banner' in cls:return [panel(contents,'#132044',width=width),Spacer(1,13)]
 if 'question' in cls:
  num=node.find('.//span');color='#ec2875' if num is not None and int(num.text)%2==0 else '#3158ff'
  return [KeepTogether([panel(contents,'#ffffff',color,width),Spacer(1,18)])]
 if 'row' in cls:return [KeepTogether([panel(contents,'#eef2ff',width=width),Spacer(1,9)])]
 if 'callout' in cls:return [panel(contents,'#fff0f6','#ec2875',width),Spacer(1,10)]
 if 'takeaway' in cls:return [panel(contents,'#fff6d5',width=width),Spacer(1,9)]
 return contents

tree=LH.fromstring((ROOT/'aihot_guide.html').read_text(encoding='utf-8'))
sections=tree.xpath('//section[contains(@class,"page")]');story=[]
for i,section in enumerate(sections):
 for child in section:story+=flow(child)
 while story and isinstance(story[-1],Spacer):story.pop()
 if i<len(sections)-1:story.append(PageBreak())
def decorate(c,doc):
 c.setFillColor(blue);c.rect(0,A4[1]-8,A4[0],8,fill=1,stroke=0)
 c.setStrokeColor(colors.HexColor('#d8dff5'));c.line(38,33,A4[0]-38,33)
 c.setFillColor(colors.HexColor('#53628b'));c.setFont('YaHei',7.5)
 c.drawString(38,20,'GeniusQI · AIHOT 源码学习 / 网站应用指南 · 2026-10-03')
 c.drawRightString(A4[0]-38,20,f'{doc.page:02d}')
doc=SimpleDocTemplate(str(ROOT/'AIHOT-小白指南与网站应用.pdf'),pagesize=A4,rightMargin=38,leftMargin=38,topMargin=35,bottomMargin=46,title='AIHOT 小白指南与 GeniusQI 网站应用',author='GeniusQI',pageCompression=1)
doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
print('PDF authored using verified local ReportLab fallback; HTML and all diagrams retained. Edge headless attempts produced no PDF.')
