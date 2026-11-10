# 真实离线实验日志

执行日期 2026-11-11 01:20:19 北京时间 UTC+8

均为自编教学夹具；第6项调用上游geo.py。合成数据不代表生产服务实测。

## 1. prepare
```bash
cd /workspace/chen-jiao-batch2-20261111/item03
python3 exercise/lab.py prepare
```
退出码 0
```text
SQLite ledger created; synthetic jobs only

```
## 2. unknown
```bash
cd /workspace/chen-jiao-batch2-20261111/item03
python3 exercise/lab.py unknown
```
退出码 0
```text
simulated create timeout: UNKNOWN; resubmit disabled

```
## 3. verify
```bash
cd /workspace/chen-jiao-batch2-20261111/item03
python3 exercise/lab.py verify
```
退出码 0
```text
fake list readback + unique hash: ('LIST_VERIFIED', 1) duplicate rejected; no external publish

```
## 4. media
```bash
cd /workspace/chen-jiao-batch2-20261111/item03
ffmpeg -y -hide_banner -loglevel error -f lavfi -i color=c=0x08254a:s=360x640:r=24:d=2 -vf "subtitles=exercise/sub.srt:force_style='FontName=Noto Sans CJK SC,FontSize=20,Outline=2'" -c:v libx264 -pix_fmt yuv420p exercise/subtitled.mp4 && python3 exercise/lab.py media
```
退出码 0
```text
ffprobe actual: 360 640 h264 2.000000 seconds

```

## 逐步目的和验证
- 步骤1 初始化本地账本：目的 建立哈希主键，避免同文件多次排队。；验证 合成SQLite数据库建立。
- 步骤2 模拟超时结果不明：目的 将不确定状态保留为UNKNOWN。；验证 UNKNOWN且attempts=1；没有远程提交。
- 步骤3 只读回查与去重：目的 使用明确fake_list演练状态推进。；验证 LIST_VERIFIED、attempts=1，重复插入被主键拒绝。
- 步骤4 字幕编码与规格探测：目的 真实运行FFmpeg和ffprobe。；验证 360×640、H.264、2.000000秒；另有抽帧自查。

## 未验证边界
AI视频、TTS、真实会话、平台列表、上传与发布全部未验证；模拟列表在代码里明确fake_list；2秒低分辨率色卡不是作者1080×1920约60秒成片。

## PDF机器检查
Chromium真实打印A4，pdftoppm渲染9页；DOM溢出检查：[]。等待逐页视觉自查；不等于独立审核。


## PDF逐页自查结论
2026-11-11 01:28:26 北京时间 UTC+8：查看pdftoppm生成的page-1..9.png（contact.png汇总），九页均未见裁切/重叠/空白；DOM溢出=[]；pdftotext回读4833字符、替换字符0。为本人自查，非独立审核。

视频抽帧：ffmpeg -ss 0.5 -i exercise/subtitled.mp4 -frames:v 1 subtitle-frame.png；已视觉查看，中文字幕完整可见，白字黑边，无裁切。
