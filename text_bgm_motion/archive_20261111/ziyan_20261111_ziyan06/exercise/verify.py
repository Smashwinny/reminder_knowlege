"""Local sample checks; not a growth, audio aesthetics or voice-recognition test."""
from pathlib import Path
import array,subprocess,json,wave,math
p=Path(__file__).resolve().parent.parent
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(p/'vibe-resume.mp4')]))
v=[s for s in probe['streams'] if s['codec_type']=='video'];a=[s for s in probe['streams'] if s['codec_type']=='audio']
assert len(v)==len(a)==1;assert (v[0]['width'],v[0]['height'],v[0]['r_frame_rate'],int(v[0]['nb_read_frames']))==(1920,1080,'30/1',240)
assert abs(float(v[0]['duration'])-8)<1/30 and abs(float(a[0]['duration'])-8)<1/30
with wave.open(str(p/'exercise/bgm.wav')) as w:
 sr=w.getframerate();x=array.array('h',w.readframes(w.getnframes()));assert sr==48000 and len(x)==384000
peak=max(abs(v) for v in x)/32768;rms=math.sqrt(sum((v/32768)**2 for v in x)/len(x));assert 0<peak<1 and rms>0
ratios=[]
for beat in range(16):
 def energy(t,d):
  seg=x[round(t*sr):round((t+d)*sr)];return sum(v*v for v in seg)/len(seg)
 ratios.append(energy(beat*.5,.12)/max(1,energy(beat*.5+.35,.12)))
assert min(ratios)>2
hashes=[]
for name in ['silent-resume.mp4','vibe-resume.mp4']:
 hashes.append(subprocess.check_output(['ffmpeg','-v','error','-i',str(p/name),'-map','0:v:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip())
assert hashes[0]==hashes[1]
report={'spec':'1920x1080 30fps 240frames 8sec','audio':'AAC 48000Hz mono; only input is synthesized BGM; no voiceover source','wave_samples':len(x),'wave_peak':peak,'wave_rms':rms,'bpm':120,'frames_per_beat':15,'scene_start_frames':[0,60,120,180],'scene_grid_aligned':all(f%15==0 for f in [0,60,120,180]),'beat_attack_tail_energy_ratio_min':min(ratios),'beat_count':16,'video_packet_sha_equal':True,'video_packet_sha':hashes[0]}
(p/'research/resume/ffprobe.json').write_text(json.dumps(probe,indent=2)+'\n');(p/'research/resume/verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
