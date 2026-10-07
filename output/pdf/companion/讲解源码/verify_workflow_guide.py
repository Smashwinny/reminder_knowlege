from pathlib import Path
import json, hashlib, re
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader

root=Path(__file__).resolve().parents[3]
folder=root/'tmp/pdfs/workflow-guide'
out=root/'output/pdf'
pdf=out/'拾遗到知识网络-架构与搭建指南.pdf'
reader=PdfReader(pdf)
assert len(reader.pages)==36
text='\n'.join(p.extract_text() or '' for p in reader.pages)
assert '\ufffd' not in text
for term in ['阿里云','Ubuntu','Windows','Dot','Obsidian','SHA256','sourceHash','完整分析','复习','PowerShell','Git']:
    assert term in text,term
for i,p in enumerate(reader.pages):
    assert len(p.extract_text())>190,(i,len(p.extract_text()))
paths=sorted(folder.glob('page-*.png'))
assert len(paths)==36,len(paths)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
for start in range(0,len(paths),4):
    pics=[Image.open(p).convert('RGB') for p in paths[start:start+4]]
    w,h=pics[0].size
    sheet=Image.new('RGB',(w*2+30,h*2+84),'#DCE5F0')
    d=ImageDraw.Draw(sheet)
    for j,pic in enumerate(pics):
        x=10+(j%2)*(w+10);y=30+(j//2)*(h+37)
        sheet.paste(pic,(x,y));d.text((x,y-24),f'PAGE {start+j+1:02d}',font=font,fill='#16233D')
    sheet.save(folder/f'contact_{start//4+1:02}.jpg',quality=94)
report={'pages':36,'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
        'bytes':pdf.stat().st_size,'textCharacters':len(text),'requiredTermsFound':True,
        'layoutChecks':json.loads((out/'source/layout_qa.json').read_text(encoding='utf-8')),
        'allPagesRendered':True,'visualReview':'pending','servicesModified':False}
(out/'source/document_qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='layoutChecks'},ensure_ascii=False))
