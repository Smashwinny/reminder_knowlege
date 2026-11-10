"""Validate implemented placeholder-only interface; no real-avatar/voice capability implied."""
from pathlib import Path
import json,copy,sys
p=Path(__file__).parent

def validate(c):
 assert c['avatar']['mode']=='placeholder','only placeholder implemented; real identity not accepted'
 assert c['voice']=='none','voice generation not implemented'
 assert '占位' in c['avatar']['label'] and '非真人' in c['avatar']['label'],'visible placeholder label required'
 assert c['fps']==30 and c['durationFrames']==180
 a=c['avatar']['rect'];b=c['contentRect']
 for x,y,w,h in [a,b]:assert x>=0 and y>=0 and w>0 and h>0 and x+w<=c['width'] and y+h<=c['height'],'rect outside frame'
 assert a[0]+a[2]<=b[0] or b[0]+b[2]<=a[0] or a[1]+a[3]<=b[1] or b[1]+b[3]<=a[1],'rect overlap'
 end=0
 for s in c['sections']:
  assert s['from']==end and s['duration']>0,'timeline gap/overlap';end+=s['duration']
 assert end==c['durationFrames'],'duration mismatch'
 return True
if __name__=='__main__':
 c=json.loads((p/'src/template.json').read_text());validate(c);print('PASS valid placeholder config')
 for name,patch in [('overlap',lambda d:d['avatar'].update(rect=[700,250,440,580])),('real_avatar',lambda d:d['avatar'].update(mode='real')),('no_label',lambda d:d['avatar'].update(label='')),('voice',lambda d:d.update(voice='cloned'))]:
  bad=copy.deepcopy(c);patch(bad)
  try:validate(bad)
  except AssertionError as e:print('EXPECTED_REJECT',name,str(e))
  else:raise AssertionError('negative case wrongly accepted '+name)
