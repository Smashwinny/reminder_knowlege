# 第6项：原创文案→Vibe动效+BGM
依赖沿用第4项Remotion4.0.542，代码基于旧组件改写；无模型调用。非商业学习评估，Remotion不是MIT，请读REMOTION-LICENSE.md。
在解包根目录创建research/resume和frames，exercise中npm ci恢复锁定依赖（本轮只复用已安装依赖，未重测新机安装）。Chrome/Node/Python3/ffmpeg/ffprobe须已安装。
```bash
mkdir -p research/resume frames
cd exercise
npm ci
python3 synth.py
npm run render
cd ..
ffmpeg -y -i silent-resume.mp4 -i exercise/bgm.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 128k -shortest vibe-resume.mp4
python3 exercise/verify.py
```
无音频文件随包：synth.py确定性生成。仅原创数学合成，不下载背景音乐、不做配音。verify不代表观众/听感/增长实测。
