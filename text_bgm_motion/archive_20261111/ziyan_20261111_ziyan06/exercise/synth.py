import wave,math,struct,json
sr=48000; duration=8; samples=[]
# 本地数学合成，120BPM；非采样商用音乐、无人声
for n in range(sr*duration):
 t=n/sr; phase=t%0.5; beat=int(t/0.5)
 kick=0.22*math.exp(-phase*32)*math.sin(2*math.pi*(70*phase-35*phase*phase))
 freq=[261.6256,329.6276,391.9954,523.2511][(beat//4)%4]
 tone=0.08*math.sin(2*math.pi*freq*t)*math.exp(-phase*7)
 fade=min(1,t/0.1,(duration-t)/0.3)
 samples.append((kick+tone)*max(0,fade))
with wave.open('bgm.wav','wb') as w:
 w.setparams((1,2,sr,0,'NONE','not compressed'))
 w.writeframes(b''.join(struct.pack('<h',round(x*32767)) for x in samples))
print(json.dumps({'sample_rate':sr,'samples':len(samples),'peak':max(abs(x) for x in samples),'bpm':120,'beat_frames_at_30fps':15}))
