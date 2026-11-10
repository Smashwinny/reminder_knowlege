import sys,json
mode=sys.argv[1]
if mode=='bom':
 parts={'board':[25,36],'mic':[4,9],'amp':[3,6],'speaker':[5,5],'breadboard_per_unit':[1.5,5],'wires':[5,7]}
 low=sum(v[0] for k,v in parts.items())+1.5;high=sum(v[1] for k,v in parts.items())+5
 assert (low,high)==(45.0,73)
 print('author-quote arithmetic, 2 breadboards: mandatory=',low,high,'CNY; optional OLED ->',low+5,high+7,'; NOT current price')
elif mode=='clock':
 fs=16000;slots=2;bits=32;bclk=fs*slots*bits;pcm_bytes=fs*2*10
 assert bclk==1024000 and pcm_bytes==320000
 print('fixture fs=16000 stereo slots=2 slotwidth=32: BCLK=',bclk,'Hz; mono PCM16 10s=',pcm_bytes,'bytes')
elif mode=='buffer':
 w,h=320,240;frame=w*h*2;double=frame*2
 assert double==307200
 print('RGB565 320x240 single=',frame,'double=',double,'bytes; 40-line partial=',320*40*2,'bytes')
elif mode=='compat':
 board={'chip':'ESP32-S3','flash':16,'psram':8,'mic':'i2s','amp':'i2s','pins_confirmed':False}
 assert board['flash']==16 and board['psram']==8;allowed=all([board['pins_confirmed']]);assert not allowed
 print(json.dumps({'memory_spec_ok':True,'flash_authorized':False,'reason':'pin map, voltage and exact board not verified'},ensure_ascii=False))
