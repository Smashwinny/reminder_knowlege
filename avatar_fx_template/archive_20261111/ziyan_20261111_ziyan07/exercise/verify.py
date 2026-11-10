from pathlib import Path
import json,subprocess,hashlib
from validate_template import validate
p=Path(__file__).resolve().parents[1];c=json.loads((p/'exercise/src/template.json').read_text());validate(c)
f=p/'template-final.mp4';r=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(f)]));v=[s for s in r['streams'] if s['codec_type']=='video'];a=[s for s in r['streams'] if s['codec_type']=='audio']
assert len(v)==1 and len(a)==0;assert (v[0]['width'],v[0]['height'],v[0]['r_frame_rate'],int(v[0]['nb_read_frames']))==(1920,1080,'30/1',180);assert abs(float(v[0]['duration'])-6)<1/30
rois=[]
for t in [.8,1.3]:
 b=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(f),'-frames:v','1','-vf','crop=440:580:100:250,scale=220:290','-f','rawvideo','-pix_fmt','rgb24','-']);rois.append(b)
assert len(rois[0])==len(rois[1]);diff=sum(a!=b for a,b in zip(*rois))/len(rois[0]);assert diff>.001
out={'spec':'1920x1080 30fps 180frames 6sec','audio_streams':0,'mode':'placeholder only; no digital human or voice','safe_rects_disjoint':True,'timeline_contiguous':True,'avatar_roi_diff_fraction_at_0.8_1.3':diff,'roi_sha256':[hashlib.sha256(b).hexdigest() for b in rois],'caveat':'ROI difference proves change, not lip sync or human identity; geometry validation is not pixel text-bound audit'}
(p/'research/resume/ffprobe.json').write_text(json.dumps(r,indent=2)+'\n');(p/'research/resume/verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
