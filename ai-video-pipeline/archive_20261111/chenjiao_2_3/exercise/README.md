# 离线练习与复现

依赖：Python3、带libass字幕过滤器和libx264的FFmpeg/ffprobe、系统Noto Sans CJK SC字体。

从ZIP解压后的、含exercise/的父目录运行，按次序：

```bash
python3 exercise/lab.py prepare
python3 exercise/lab.py unknown
python3 exercise/lab.py verify
ffmpeg -y -hide_banner -loglevel error -f lavfi -i color=c=0x08254a:s=360x640:r=24:d=2 -vf "subtitles=exercise/sub.srt:force_style='FontName=Noto Sans CJK SC,FontSize=20,Outline=2'" -c:v libx264 -pix_fmt yuv420p exercise/subtitled.mp4 && python3 exercise/lab.py media
```

lab.py为本次自编教学夹具，不是作者项目实现；合成输入在代码内明确标注。没有账号、用户密钥、真实硬件或外部发布。局部数据库/图片/视频写入exercise/，回环HTTP监听127.0.0.1随机端口并关闭。运行第一个步骤会重建本项合成练习数据库（如有），不用于用户业务数据。

完整原始命令输出与边界随ZIP附experiment-log.md；来源随ZIP附sources.md。
