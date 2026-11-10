# 段01 CPU练习

Python 3.13.5实测，无第三方依赖。解压后进入本目录：
```bash
python3 dance_lab.py synth
python3 dance_lab.py analyze
python3 dance_lab.py template
python3 dance_lab.py test
python3 -c "import json; print(json.load(open('output/analysis.json'))['detected_pulses'])"
```

输出25、12项自写检查通过；clicks.wav是原创合成PCM测试音，不是原歌曲。prompt.txt为未提交模型的简化导演模板，timeline.json只编码时间/机位，不包含真实身份图姿势图。validate是指定字段/区间的教学子集，不做完整schema、真实文件解码或语义/模型服从检查。无视频生成、无API、无用户密钥。build_guide.py需同目录output/analysis.json，生成父目录item01.html。
