# 离线练习与复现

依赖：Python3、Pillow（若缺：python3 -m pip install Pillow），FFmpeg/ffprobe。geo.py为上游原样代码，MIT许可见LICENSE。

从ZIP解压后的、含exercise/的父目录运行，按次序：

```bash
python3 exercise/lab.py distance
python3 exercise/lab.py roundtrip
python3 exercise/lab.py angles
python3 exercise/lab.py frames && ffmpeg -y -hide_banner -loglevel error -framerate 24 -i exercise/frame-%03d.png -c:v libx264 -pix_fmt yuv420p exercise/synthetic-route.mp4 && ffprobe -v error -show_entries format=duration -of default=nw=1 exercise/synthetic-route.mp4
```

上游 geo.py： https://github.com/SpaceZephyr/map-motion/blob/65ab781832cace6e0f28d4c00452410a99f3a02c/scripts/geo.py 。

lab.py为本次自编教学夹具，不是作者项目实现；合成输入在代码内明确标注。没有账号、用户密钥、真实硬件或外部发布。局部数据库/图片/视频写入exercise/，回环HTTP监听127.0.0.1随机端口并关闭。运行第一个步骤会重建本项合成练习数据库（如有），不用于用户业务数据。

完整原始命令输出与边界随ZIP附experiment-log.md；来源随ZIP附sources.md。
