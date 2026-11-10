import sys,math,json,importlib.util
from pathlib import Path
p=Path(__file__).parent/'geo.py';s=importlib.util.spec_from_file_location('geo',p);geo=importlib.util.module_from_spec(s);s.loader.exec_module(geo)
mode=sys.argv[1]
if mode=='distance':
 d=geo.hav([0,0],[1,0]);assert abs(d-111.1949266)<1e-5;print('upstream hav equator 1 degree:',round(d,7),'km; spherical not road distance')
elif mode=='roundtrip':
 a=[121.4737,31.2304];b=geo.unmerc(geo.merc(a));err=max(abs(x-y) for x,y in zip(a,b));assert err<1e-10;print('Mercator roundtrip max degree error=',err)
elif mode=='angles':
 b=geo.lerp_ang(350,10,.5);assert b==360;assert geo.smooth(-1)==0 and geo.smooth(2)==1;print('350->10 midpoint=',b,'degrees (wrap=0); easing clamped endpoints PASS')
elif mode=='frames':
 from PIL import Image,ImageDraw
 dest={'c':[121.4737,31.2304],'z':12,'p':45,'b':10};frames=[]
 for k in range(48):
  u=k/47;c=geo.dive(u,dest);frames.append(geo.frame(c));im=Image.new('RGB',(360,640),'#08254a');d=ImageDraw.Draw(im);d.line((30,500,330,200),fill='#06b6d4',width=5);d.ellipse((25+300*u,495-300*u,35+300*u,505-300*u),fill='#f97316');d.text((20,30),'SYNTHETIC ROUTE - NOT MAP',fill='white');im.save(f'exercise/frame-{k:03d}.png')
 assert frames[-1][:2]==dest['c'];Path('exercise/camera.json').write_text(json.dumps(frames));print('upstream geo.dive/frame generated=',len(frames),'frames; last=',frames[-1],'; drawn path is synthetic, no map tiles/DEM fetched')
