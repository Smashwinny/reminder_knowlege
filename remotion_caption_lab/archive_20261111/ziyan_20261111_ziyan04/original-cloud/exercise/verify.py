"""Read real ffprobe output; no mocks or self-issued independent review."""
from pathlib import Path
import json,subprocess
p=Path(__file__).resolve().parent.parent
x=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p/'caption-lab.mp4')]))
v=[s for s in x['streams'] if s['codec_type']=='video'];a=[s for s in x['streams'] if s['codec_type']=='audio']
checks={'one_video':len(v)==1,'1080p':(v[0]['width'],v[0]['height'])==(1920,1080),'30fps':v[0]['r_frame_rate']=='30/1','12s':float(x['format']['duration'])==12.0,'360frames':v[0]['nb_frames']=='360','no_audio':not a}
for k,value in checks.items():print(k,'PASS' if value else 'FAIL')
assert all(checks.values())
