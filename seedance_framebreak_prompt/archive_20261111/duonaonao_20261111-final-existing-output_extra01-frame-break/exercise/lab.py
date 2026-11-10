from pathlib import Path
import sys,json,math,csv,subprocess,hashlib,shlex
from PIL import Image,ImageDraw,ImageChops
P=Path(__file__).resolve().parent;O=P/'out';O.mkdir(exist_ok=True);W,H=480,270

def save(n,x): (O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2))
def init():
 matrix=[dict(bar_ratio=r,overlap=o,camera_pan_px=c,prompt_strength='not simulated') for r in [.10,.18,.25] for o in [False,True] for c in [0,16]]
 save('variables.json',matrix)
 with (O/'variables.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=matrix[0]);w.writeheader();w.writerows(matrix)
 (O/'prompt-candidate.txt').write_text('原创几何人偶，手和头越过上下黑色遮幅，黑边固定于画布坐标。镜头先静止，动作缓慢，保留人物完整轮廓。每条黑边目标18%高。此提示为本轮自拟，非作者公开提示的逐字复刻；比例与固定约束在Seedance中待验证。')
 print('12 deterministic cases: 3 per-bar ratios x 2 overlap states x 2 background pan levels; prompt strength NOT simulated')
def compose(ratio,overlap,pan=0,t=0):
 b=round(H*ratio);bg=Image.new('RGBA',(W,H),(24,85,150,255));d=ImageDraw.Draw(bg)
 for x in range(-30,W+31,30):d.line((x+pan,0,x+pan,H),fill=(38,130,180,255),width=1)
 bars=Image.new('RGBA',(W,H));bd=ImageDraw.Draw(bars);bd.rectangle((0,0,W-1,b-1),fill='black');bd.rectangle((0,H-b,W-1,H-1),fill='black')
 base=Image.alpha_composite(bg,bars);subject=Image.new('RGBA',(W,H));sd=ImageDraw.Draw(subject);cx=W//2+round(12*math.sin(2*math.pi*t));col=(255,139,29,255)
 sd.ellipse((cx-25,12,cx+25,62),fill=col);sd.rounded_rectangle((cx-30,65,cx+30,166),radius=14,fill=col)
 sd.line((cx-20,80,cx-85,35),fill=col,width=17);sd.line((cx+20,80,cx+88,42),fill=col,width=17)
 sd.line((cx-15,157,cx-48,254),fill=col,width=18);sd.line((cx+15,157,cx+48,254),fill=col,width=18)
 alpha=subject.getchannel('A');bar_mask=bars.getchannel('A');cross=ImageChops.multiply(alpha,bar_mask)
 intended=sum(1 for v in cross.getdata() if v)
 if not overlap:
  middle=Image.new('L',(W,H));ImageDraw.Draw(middle).rectangle((0,b,W-1,H-b-1),fill=255);subject.putalpha(ImageChops.multiply(alpha,middle))
 out=Image.alpha_composite(base,subject).convert('RGB')
 visible=sum(1 for v in ImageChops.multiply(subject.getchannel('A'),bar_mask).getdata() if v)
 return out,dict(bar_px=b,intended_cross_pixels=intended,visible_cross_pixels=visible)
def render():
 cases=json.loads((O/'variables.json').read_text());results=[]
 for i,c in enumerate(cases):
  im,m=compose(c['bar_ratio'],c['overlap'],c['camera_pan_px']);im.save(O/f'case-{i:02d}.png');results.append(dict(case=i,**c,**m))
 save('measurements.json',results)
 frames=O/'frames';frames.mkdir(exist_ok=True)
 for i in range(144):
  r=[.10,.18,.25][i//48];a,_=compose(r,False,round(16*math.sin(2*math.pi*i/48)),i/48);b,_=compose(r,True,round(16*math.sin(2*math.pi*i/48)),i/48);pair=Image.new('RGB',(W*2,H+30),'white');pair.paste(a,(0,30));pair.paste(b,(W,30));d=ImageDraw.Draw(pair);d.text((10,8),f'CLIPPED  per-bar={r:.0%}',fill='black');d.text((W+10,8),f'FRAME-BREAK  per-bar={r:.0%}',fill='black');pair.save(frames/f'{i:03d}.png')
 print('rendered 12 PNG cases + 144 comparison frames (960x300); all character art self-drawn; no model inference')
def encode():
 cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-framerate','24','-i',str(O/'frames/%03d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-crf','23',str(P.parent/'frame-break-demo.mp4')]
 print(shlex.join(cmd));subprocess.run(cmd,check=True);print('exit=0; encoded frame-break-demo.mp4 (not Seedance output)')
def validate():
 rows=json.loads((O/'measurements.json').read_text());assert len(rows)==12
 for x in rows:assert (x['visible_cross_pixels']>0)==x['overlap'];assert x['bar_px']==round(H*x['bar_ratio'])
 assert compose(.18,True,16)[0].getpixel((0,0))==(0,0,0)
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','stream=width,height,nb_read_frames,r_frame_rate','-show_entries','format=duration','-of','json',str(P.parent/'frame-break-demo.mp4')]))
 assert info['streams'][0]['nb_read_frames']=='144';assert float(info['format']['duration'])==6
 save('validation.json',{'case_count':12,'clipped_zero_overlap':True,'front_nonzero_overlap':True,'bar_geometries':[27,49,68],'probe':info})
 print(json.dumps({'cases':12,'overlap_invariants':'PASS','bar_px':[27,49,68],'frames':144,'fps':24,'duration_s':6},ensure_ascii=False))
def audit():
 fs=[P/'lab.py',O/'variables.csv',O/'measurements.json',O/'validation.json',P.parent/'frame-break-demo.mp4'];save('manifest.json',{str(f.relative_to(P.parent)):hashlib.sha256(f.read_bytes()).hexdigest() for f in fs});print('5 SHA256 fingerprints saved; model generation/account/credits NOT used; prompt-strength effects await real testing')
if __name__=='__main__':globals()[sys.argv[1]]()
