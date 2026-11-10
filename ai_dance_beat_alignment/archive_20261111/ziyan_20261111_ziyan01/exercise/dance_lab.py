"""Self-written CPU laboratory. Synthesized clicks, NOT original song or generated dance."""
import argparse,array,copy,json,math,statistics,sys,wave
from pathlib import Path
P=Path(__file__).resolve().parent; O=P/'output';O.mkdir(exist_ok=True)
SR=48000;D=10.876;BPM=132.5;BEAT=60/BPM
PHASES=[(0,2.15,'signature_close_pass'),(2.15,3.62,'full_body_hold'),(3.62,5.43,'full_body_hold'),(5.43,7.25,'short_lateral_then_settle'),(7.25,9.06,'hold_during_pivot'),(9.06,D,'full_body_settle')]
def save(name,obj):(O/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def synth():
 n=round(SR*D);a=array.array('h',[0])*n
 expected=[round(i*BEAT*SR) for i in range(math.floor(D/BEAT)+1)]
 for k in expected:
  for j in range(min(1440,n-k)):
   a[k+j]=round(24000*math.exp(-j/220)*math.sin(2*math.pi*1800*j/SR))
 if sys.byteorder!='little':a.byteswap()
 with wave.open(str(O/'clicks.wav'),'wb') as w:w.setparams((1,2,SR,n,'NONE','not compressed'));w.writeframes(a.tobytes())
 save('truth.json',{'sample_rate':SR,'samples':n,'onsets_samples':expected,'license':'original synthesized test fixture; CC0-1.0'})
 print(f'SYNTH samples={n} duration={n/SR:.6f}s pulses={len(expected)} BPM={BPM}; NOT original audio')
def analyze():
 with wave.open(str(O/'clicks.wav'),'rb') as w:
  sr=w.getframerate();n=w.getnframes();a=array.array('h');a.frombytes(w.readframes(n))
 if sys.byteorder!='little':a.byteswap()
 peaks=[];last=-sr
 for i,x in enumerate(a):
  if abs(x)>500 and i-last>int(.1*sr):peaks.append(i);last=i
 expected=json.loads((O/'truth.json').read_text())['onsets_samples']
 assert len(peaks)==len(expected)
 err=max(abs(a-b)/sr for a,b in zip(peaks,expected));tempo=60/(statistics.median(b-a for a,b in zip(peaks,peaks[1:]))/sr)
 r={'detected_pulses':len(peaks),'estimated_BPM':tempo,'max_onset_error_ms':err*1000,'beat_s':BEAT,'bar_s':4*BEAT,'phrase_s':8*BEAT,'phrase_anchors':[round(i*8*BEAT,6) for i in range(4)],'audio_duration':n/sr,'nearest_24fps_frames':round(n/sr*24),'nearest_24fps_duration':round(n/sr*24)/24,'duration_error_ms':(round(n/sr*24)/24-n/sr)*1000,'scope':'threshold onset detector on isolated synthetic clicks only; not a music beat tracker'}
 save('analysis.json',r);print(json.dumps(r,ensure_ascii=False,indent=2))
def validate(t):
 if t['identity_slot']!='Image 1' or t['pose_slot']!='Image 2' or t['audio_slot']!='Audio 1':raise ValueError('reference role collision')
 if t['pose_transfers_identity'] or t['lyric_actions']:raise ValueError('identity/lyric semantic leakage')
 if t['fps']!=24 or t['aspect']!='9:16':raise ValueError('output contract')
 cursor=0
 for p in t['phases']:
  if p['start']!=cursor or p['end']<=cursor:raise ValueError('gap/overlap')
  if p['start']>=2.15 and not p['full_body']:raise ValueError('feet/head/hands must remain visible')
  cursor=p['end']
 if cursor!=t['duration']:raise ValueError('duration coverage')
 if any(not 0<=x<t['duration'] for x in t['anchors']):raise ValueError('anchor outside audio')
 if t['segment']!=1 and t['phases'][0]['camera']=='signature_close_pass':raise ValueError('opening exception only segment01')
 return True
def template():
 t={'segment':1,'duration':D,'fps':24,'aspect':'9:16','identity_slot':'Image 1','pose_slot':'Image 2','audio_slot':'Audio 1','pose_transfers_identity':False,'lyric_actions':False,'anchors':[0,3.623,7.245,10.868],'phases':[{'start':a,'end':b,'camera':c,'full_body':a>=2.15} for a,b,c in PHASES]}
 validate(t);save('timeline.json',t)
 prompt='实验模板（未提交模型）\nImage 1: ONLY identity, face, body, outfit.\nImage 2: POSES ONLY; never transfer face, clothes or background.\nAudio 1: rhythm and accents only; lyrics are NOT action instructions.\n24fps; 9:16; original requested audio duration 10.876s; no audio stretch.\nTiming contract conflict: 261 full CFR frames last 10.875s; preserve audio master and resolve backend/container endpoint explicitly, do not silently stretch.\nNatural foot-led weight transfers, then hips/torso, then arms/hair. Hard cuts, not body morphs.\n'
 for a,b,c in PHASES:prompt+=f'{a:.3f}–{b:.3f}s: {c}; '+('unique opening exception; recover full body by 2.15s' if a==0 else 'head, hands and feet visible; continuous dance steps')+'\n'
 prompt+='No lyric acting, lip-sync, props from words, duplicate limbs, foot cropping, endless orbit or freeze before audio end.\nKeep subtle residual motion for continuation; generation and visual QC pending.\n'
 (O/'prompt.txt').write_text(prompt);print('TEMPLATE phases=6 references=3 VALID; no model invocation')
def tests():
 t=json.loads((O/'timeline.json').read_text());assert validate(t);count=1
 changes=[lambda x:x.update(identity_slot='Image 2'),lambda x:x.update(lyric_actions=True),lambda x:x.update(pose_transfers_identity=True),lambda x:x.update(fps=30),lambda x:x['phases'][1].update(start=2.16),lambda x:x['phases'][2].update(full_body=False),lambda x:x['anchors'].append(D+.1),lambda x:x.update(segment=2),lambda x:x.update(duration=11)]
 for i,fn in enumerate(changes,1):
  x=copy.deepcopy(t);fn(x)
  try:validate(x)
  except ValueError as e: print(f'REJECT negative{i}: {e}');count+=1
  else:raise AssertionError('negative accepted')
 r=json.loads((O/'analysis.json').read_text());assert r['detected_pulses']==25 and r['max_onset_error_ms']<1;count+=1
 assert abs(r['duration_error_ms']+1)<1e-8;count+=1
 print(f'PASS checks={count} (1 valid,9 rejected,2 numeric); VIDEO_NOT_GENERATED')
if __name__=='__main__':
 op=argparse.ArgumentParser();op.add_argument('step',choices=['synth','analyze','template','test']);a=op.parse_args();{'synth':synth,'analyze':analyze,'template':template,'test':tests}[a.step]()
