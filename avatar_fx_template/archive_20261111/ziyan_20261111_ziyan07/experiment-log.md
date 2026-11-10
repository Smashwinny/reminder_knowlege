# 第7项真实实验日志

2026-11-11（Asia/Shanghai，UTC+8）；单一路按顺序完成。非商业学习，自检非独立审核。

复用Remotion项目真实渲染人物占位层+内容+动效；1正例/4负例检查、TypeScript、ffprobe通过，四张抽帧已读。

真实边界：真实数字人、音色克隆、Opus、身份/口型一致性均待验证；没有音频流。作者约100客资、矩阵起号与增长效果未独立核验，未发布。

原误标source-post.json隔离history后，按保存X原始响应的精确ID选取正确原帖与引用；逐字读完note_tweet/text，不把摘要当原文，未观看引用视频。未执行来源中“快试起号”“评论区咨询”等引导，没有发布或索取他人素材。

## 1. 实读文字并限定新增范围
目的：拆开技术主张与商业自述。
```bash
cd /workspace/reminder-batch/item07
# Read source-post.json两个完整post
# ID: 2110742894776885607 / 2110700648593600749
# 对照item04日志、item05提案、item06提案
# 保留原帖未公开视频/参数的边界
```
真实结果：按返回ID核对原帖/引用；错标旧JSON隔离。只补人物占位层接口，不重做底层渲染/BGM。
验证：sources.md给出原始响应路径、固定SHA与一手文档；客户数字不采信。

## 2. 定义三层配置并跑负例
目的：使占位与安全区成为显式合同。
```bash
cd /workspace/reminder-batch/item07/exercise
# src/template.json：占位人物、无声音、3×60帧
python3 validate_template.py
./node_modules/.bin/tsc --noEmit
```
真实结果：1个有效配置通过，4个坏输入预期拒绝；TS检查退出0。
验证：覆盖框重叠/真人mode/无标识/克隆声音；不是通用身份授权审核。

## 3. 复用旧项目真实渲染
目的：只验证本地组件，不冒称调用模型。
```bash
cd /workspace/reminder-batch/item07/exercise
./node_modules/.bin/remotion render src/index.tsx TemplateLab ../template-final.mp4 --concurrency=2 --browser-executable=/usr/bin/google-chrome
```
真实结果：最终数据驱动contentRect版本真实渲染180帧，退出0。
验证：原始CLI日志render-final.txt；另保留初版render.txt；未用付费API/密钥。

## 4. 验证规格及占位区确有动态
目的：把源代码意图与文件事实分开。
```bash
cd /workspace/reminder-batch/item07
python3 exercise/verify.py
ffprobe -v error -count_frames -show_streams -show_format -of json template-final.mp4
```
真实结果：1920×1080/30fps/180帧/6秒，0音频流；人物ROI字节变化约15.82%。
验证：ROI对比为0.8/1.3秒；只证明动效，不是口型、身份或声线实测。

## 5. 真实抽帧与人工自检
目的：核查占位字样、安全区及内容可读。
```bash
cd /workspace/reminder-batch/item07
ffmpeg -y -v error -i template-final.mp4 -vf "select='eq(n,24)+eq(n,59)+eq(n,84)+eq(n,144)',scale=640:360" -fps_mode vfr frames/scene-%02d.jpg
# 逐张Read scene-01到04.jpg
```
真实结果：四帧分别0.8/1.967/2.8/4.8秒；占位标识及未测条持续可见，人物和内容无相互遮挡。
验证：首幕第二帧用于检查入场完成；其余两幕见标题切换。不是全片逐帧或独立审核。

## 6. 打印、检查、输出候选包
目的：保留真实边界与重放代码。
```bash
cd /workspace/reminder-batch/item07
python3 research/build-guide.py
../item04/research/pdf-venv/bin/python -m weasyprint guide.html guide.pdf
mkdir -p pdf-pages
pdftoppm -scale-to 1200 -png guide.pdf pdf-pages/page
# 逐页Read后运行research/finish_delivery.py
```
真实结果：中文HTML、A4 PDF、练习ZIP、日志/提案/来源实际生成。
验证：全页Read记录、打包CRC与SHA清单见日志；轻量包不含视频/字体集。

## 实际原始输出

### ffprobe.json
```text
{
  "streams": [
    {
      "index": 0,
      "codec_name": "h264",
      "codec_long_name": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10",
      "profile": "High",
      "codec_type": "video",
      "codec_tag_string": "avc1",
      "codec_tag": "0x31637661",
      "width": 1920,
      "height": 1080,
      "coded_width": 1920,
      "coded_height": 1088,
      "closed_captions": 0,
      "film_grain": 0,
      "has_b_frames": 2,
      "sample_aspect_ratio": "1:1",
      "display_aspect_ratio": "16:9",
      "pix_fmt": "yuvj420p",
      "level": 40,
      "color_range": "pc",
      "color_space": "bt470bg",
      "chroma_location": "center",
      "field_order": "progressive",
      "refs": 4,
      "is_avc": "true",
      "nal_length_size": "4",
      "id": "0x1",
      "r_frame_rate": "30/1",
      "avg_frame_rate": "30/1",
      "time_base": "1/90000",
      "start_pts": 0,
      "start_time": "0.000000",
      "duration_ts": 540000,
      "duration": "6.000000",
      "bit_rate": "1229001",
      "bits_per_raw_sample": "8",
      "nb_frames": "180",
      "nb_read_frames": "180",
      "extradata_size": 51,
      "disposition": {
        "default": 1,
        "dub": 0,
        "original": 0,
        "comment": 0,
        "lyrics": 0,
        "karaoke": 0,
        "forced": 0,
        "hearing_impaired": 0,
        "visual_impaired": 0,
        "clean_effects": 0,
        "attached_pic": 0,
        "timed_thumbnails": 0,
        "non_diegetic": 0,
        "captions": 0,
        "descriptions": 0,
        "metadata": 0,
        "dependent": 0,
        "still_image": 0,
        "multilayer": 0
      },
      "tags": {
        "language": "und",
        "handler_name": "VideoHandler",
        "vendor_id": "[0][0][0][0]"
      },
      "side_data_list": [
        {
          "side_data_type": "ICC Profile"
        }
      ]
    }
  ],
  "format": {
    "filename": "/workspace/reminder-batch/item07/template-final.mp4",
    "nb_streams": 1,
    "nb_programs": 0,
    "nb_stream_groups": 0,
    "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
    "format_long_name": "QuickTime / MOV",
    "start_time": "0.000000",
    "duration": "6.000000",
    "size": "925284",
    "bit_rate": "1233712",
    "probe_score": 100,
    "tags": {
      "major_brand": "isom",
      "minor_version": "512",
      "compatible_brands": "isomiso2avc1mp41",
      "encoder": "Lavf61.7.100",
      "comment": "Made with Remotion 4.0.542"
    }
  }
}

```

### render-final.txt
```text
$ ./node_modules/.bin/remotion render src/index.tsx TemplateLab ../template-final.mp4 --concurrency=2 --browser-executable=/usr/bin/google-chrome
Bundling 6%
Bundling 21%
Bundling 32%
Bundling 54%
Bundling 65%
Bundling 71%
Bundling 76%
Bundling 81%
Bundling 87%
Bundling 92%
Bundling 98%
Bundling 100%
Getting composition
Composition          TemplateLab
Codec                h264
Output               ../template-final.mp4
Concurrency          2x
Rendered 0/180
Rendered 1/180, time remaining: 59s
Rendered 2/180, time remaining: 44s
Rendered 3/180, time remaining: 29s
Rendered 4/180, time remaining: 24s
Rendered 5/180, time remaining: 24s
Rendered 6/180, time remaining: 20s
Rendered 7/180, time remaining: 18s
Rendered 8/180, time remaining: 19s
Rendered 9/180, time remaining: 17s
Rendered 10/180, time remaining: 16s
Rendered 11/180, time remaining: 17s
Rendered 12/180, time remaining: 15s
Rendered 13/180, time remaining: 15s
Rendered 14/180, time remaining: 15s
Rendered 15/180, time remaining: 14s
Rendered 16/180, time remaining: 14s
Rendered 17/180, time remaining: 14s
Rendered 18/180, time remaining: 13s
Rendered 19/180, time remaining: 13s
Rendered 20/180, time remaining: 13s
Rendered 21/180, time remaining: 13s
Rendered 22/180, time remaining: 13s
Rendered 23/180, time remaining: 13s
Rendered 24/180, time remaining: 12s
Rendered 25/180, time remaining: 12s
Rendered 26/180, time remaining: 12s
Rendered 27/180, time remaining: 12s
Rendered 28/180, time remaining: 12s
Rendered 29/180, time remaining: 12s
Rendered 30/180, time remaining: 11s
Rendered 31/180, time remaining: 11s
Rendered 32/180, time remaining: 11s
Rendered 33/180, time remaining: 11s
Rendered 34/180, time remaining: 11s
Rendered 35/180, time remaining: 11s
Rendered 36/180, time remaining: 11s
Rendered 37/180, time remaining: 10s
Rendered 38/180, time remaining: 11s
Rendered 39/180, time remaining: 10s
Rendered 40/180, time remaining: 10s
Rendered 41/180, time remaining: 10s
Rendered 42/180, time remaining: 10s
Rendered 43/180, time remaining: 10s
Rendered 44/180, time remaining: 10s
Rendered 45/180, time remaining: 10s
Rendered 46/180, time remaining: 10s
Rendered 47/180, time remaining: 10s
Rendered 48/180, time remaining: 9s
Rendered 49/180, time remaining: 9s
Rendered 50/180, time remaining: 9s
Rendered 51/180, time remaining: 10s
Rendered 52/180, time remaining: 9s
Rendered 53/180, time remaining: 9s
Rendered 54/180, time remaining: 9s
Rendered 55/180, time remaining: 9s
Rendered 56/180, time remaining: 9s
Rendered 56/180, time remaining: 9s
Rendered 57/180, time remaining: 9s
Rendered 58/180, time remaining: 9s
Rendered 59/180, time remaining: 9s
Rendered 60/180, time remaining: 9s
Rendered 61/180, time remaining: 9s
Rendered 62/180, time remaining: 8s
Rendered 62/180, time remaining: 8s
Rendered 63/180, time remaining: 8s
Rendered 64/180, time remaining: 8s
Rendered 65/180, time remaining: 8s
Rendered 66/180, time remaining: 8s
Rendered 67/180, time remaining: 8s
Rendered 68/180, time remaining: 8s
Rendered 69/180, time remaining: 8s
Rendered 70/180, time remaining: 8s
Rendered 70/180, time remaining: 8s
Rendered 71/180, time remaining: 8s
Rendered 72/180, time remaining: 8s
Rendered 73/180, time remaining: 8s
Rendered 74/180, time remaining: 7s
Rendered 75/180, time remaining: 7s
Rendered 76/180, time remaining: 7s
Rendered 77/180, time remaining: 7s
Rendered 77/180, time remaining: 7s
Rendered 78/180, time remaining: 7s
Rendered 79/180, time remaining: 7s
Rendered 80/180, time remaining: 7s
Rendered 81/180, time remaining: 7s
Rendered 82/180, time remaining: 7s
Rendered 83/180, time remaining: 7s
Rendered 84/180, time remaining: 7s
Rendered 85/180, time remaining: 7s
Rendered 85/180, time remaining: 7s
Rendered 86/180, time remaining: 6s
Rendered 87/180, time remaining: 6s
Rendered 88/180, time remaining: 6s
Rendered 89/180, time remaining: 6s
Rendered 90/180, time remaining: 6s
Rendered 91/180, time remaining: 6s
Rendered 92/180, time remaining: 6s
Rendered 92/180, time remaining: 6s
Rendered 93/180, time remaining: 6s
Rendered 94/180, time remaining: 6s
Rendered 95/180, time remaining: 6s
Rendered 96/180, time remaining: 6s
Rendered 97/180, time remaining: 6s
Rendered 98/180, time remaining: 6s
Rendered 98/180, time remaining: 6s
Rendered 99/180, time remaining: 6s
Rendered 100/180, time remaining: 5s
Rendered 101/180, time remaining: 5s
Rendered 102/180, time remaining: 5s
Rendered 103/180, time remaining: 5s
Rendered 104/180, time remaining: 5s
Rendered 105/180, time remaining: 5s
Rendered 106/180, time remaining: 5s
Rendered 106/180, time remaining: 5s
Rendered 107/180, time remaining: 5s
Rendered 108/180, time remaining: 5s
Rendered 109/180, time remaining: 5s
Rendered 110/180, time remaining: 5s
Rendered 111/180, time remaining: 5s
Rendered 112/180, time remaining: 4s
Rendered 113/180, time remaining: 4s
Rendered 113/180, time remaining: 4s
Rendered 114/180, time remaining: 4s
Rendered 115/180, time remaining: 4s
Rendered 116/180, time remaining: 4s
Rendered 117/180, time remaining: 4s
Rendered 118/180, time remaining: 4s
Rendered 119/180, time remaining: 4s
Rendered 120/180, time remaining: 4s
Rendered 121/180, time remaining: 4s
Rendered 121/180, time remaining: 4s
Rendered 122/180, time remaining: 4s
Rendered 123/180, time remaining: 4s
Rendered 124/180, time remaining: 4s
Rendered 125/180, time remaining: 3s
Rendered 126/180, time remaining: 3s
Rendered 127/180, time remaining: 3s
Rendered 128/180, time remaining: 3s
Rendered 128/180, time remaining: 3s
Rendered 129/180, time remaining: 3s
Rendered 130/180, time remaining: 3s
Rendered 131/180, time remaining: 3s
Rendered 132/180, time remaining: 3s
Rendered 133/180, time remaining: 3s
Rendered 134/180, time remaining: 3s
Rendered 135/180, time remaining: 3s
Rendered 136/180, time remaining: 3s
Rendered 136/180, time remaining: 3s
Rendered 137/180, time remaining: 3s
Rendered 138/180, time remaining: 3s
Rendered 139/180, time remaining: 2s
Rendered 140/180, time remaining: 2s
Rendered 141/180, time remaining: 2s
Rendered 142/180, time remaining: 2s
Rendered 143/180, time remaining: 2s
Rendered 143/180, time remaining: 2s
Rendered 144/180, time remaining: 2s
Rendered 145/180, time remaining: 2s
Rendered 146/180, time remaining: 2s
Rendered 147/180, time remaining: 2s
Rendered 148/180, time remaining: 2s
Rendered 149/180, time remaining: 2s
Rendered 149/180, time remaining: 2s
Rendered 150/180, time remaining: 2s
Rendered 151/180, time remaining: 2s
Rendered 152/180, time remaining: 1s
Rendered 153/180, time remaining: 1s
Rendered 154/180, time remaining: 1s
Rendered 155/180, time remaining: 1s
Rendered 156/180, time remaining: 1s
Rendered 157/180, time remaining: 1s
Rendered 158/180, time remaining: 1s
Rendered 158/180, time remaining: 1s
Rendered 159/180, time remaining: 1s
Rendered 160/180, time remaining: 1s
Rendered 161/180, time remaining: 1s
Rendered 162/180, time remaining: 1s
Rendered 163/180, time remaining: 1s
Rendered 164/180, time remaining: 1s
Rendered 164/180, time remaining: 1s
Rendered 165/180, time remaining: 1s
Rendered 166/180, time remaining: 0s
Rendered 167/180, time remaining: 0s
Rendered 168/180, time remaining: 0s
Rendered 169/180, time remaining: 0s
Rendered 170/180, time remaining: 0s
Rendered 171/180, time remaining: 0s
Rendered 172/180, time remaining: 0s
Rendered 172/180, time remaining: 0s
Rendered 173/180, time remaining: 0s
Rendered 174/180, time remaining: 0s
Rendered 175/180, time remaining: 0s
Rendered 176/180, time remaining: 0s
Rendered 177/180, time remaining: 0s
Rendered 178/180, time remaining: 0s
Rendered 179/180, time remaining: 0s
Rendered 179/180, time remaining: 0s
Encoded 98/180
Encoded 144/180
Encoded 180/180
+                    ../template-final.mp4 925.3 kB

exit_code=0 (observed Shell)

```

### render.txt
```text
$ ./node_modules/.bin/remotion render src/index.tsx TemplateLab ../template.mp4 --concurrency=2 --browser-executable=/usr/bin/google-chrome
🧹 Webpack config change detected. Clearing cache... 
Bundling 6%
Bundling 21%
Bundling 43%
Bundling 54%
Bundling 65%
Bundling 71%
Bundling 76%
Bundling 81%
Bundling 87%
Bundling 92%
Bundling 98%
Bundling 100%
Getting composition
⚡️ Cached bundle. Subsequent renders will be faster.
Composition          TemplateLab
Codec                h264
Output               ../template.mp4
Concurrency          2x
Rendered 0/180
Rendered 1/180, time remaining: 1m 10s
Rendered 2/180, time remaining: 35s
Rendered 3/180, time remaining: 28s
Rendered 4/180, time remaining: 21s
Rendered 5/180, time remaining: 24s
Rendered 6/180, time remaining: 20s
Rendered 7/180, time remaining: 19s
Rendered 8/180, time remaining: 19s
Rendered 9/180, time remaining: 17s
Rendered 10/180, time remaining: 16s
Rendered 11/180, time remaining: 16s
Rendered 12/180, time remaining: 15s
Rendered 13/180, time remaining: 15s
Rendered 14/180, time remaining: 15s
Rendered 15/180, time remaining: 14s
Rendered 16/180, time remaining: 14s
Rendered 17/180, time remaining: 14s
Rendered 18/180, time remaining: 13s
Rendered 19/180, time remaining: 13s
Rendered 20/180, time remaining: 13s
Rendered 21/180, time remaining: 13s
Rendered 22/180, time remaining: 12s
Rendered 23/180, time remaining: 13s
Rendered 24/180, time remaining: 12s
Rendered 25/180, time remaining: 12s
Rendered 26/180, time remaining: 12s
Rendered 27/180, time remaining: 12s
Rendered 28/180, time remaining: 11s
Rendered 29/180, time remaining: 12s
Rendered 30/180, time remaining: 11s
Rendered 31/180, time remaining: 11s
Rendered 32/180, time remaining: 11s
Rendered 33/180, time remaining: 11s
Rendered 34/180, time remaining: 11s
Rendered 35/180, time remaining: 11s
Rendered 36/180, time remaining: 11s
Rendered 37/180, time remaining: 10s
Rendered 38/180, time remaining: 11s
Rendered 39/180, time remaining: 10s
Rendered 40/180, time remaining: 10s
Rendered 41/180, time remaining: 10s
Rendered 42/180, time remaining: 10s
Rendered 43/180, time remaining: 10s
Rendered 44/180, time remaining: 10s
Rendered 45/180, time remaining: 10s
Rendered 46/180, time remaining: 10s
Rendered 47/180, time remaining: 10s
Rendered 48/180, time remaining: 9s
Rendered 49/180, time remaining: 9s
Rendered 50/180, time remaining: 9s
Rendered 51/180, time remaining: 10s
Rendered 52/180, time remaining: 9s
Rendered 53/180, time remaining: 9s
Rendered 54/180, time remaining: 9s
Rendered 55/180, time remaining: 9s
Rendered 56/180, time remaining: 9s
Rendered 56/180, time remaining: 9s
Rendered 57/180, time remaining: 9s
Rendered 58/180, time remaining: 9s
Rendered 59/180, time remaining: 9s
Rendered 60/180, time remaining: 9s
Rendered 61/180, time remaining: 9s
Rendered 62/180, time remaining: 8s
Rendered 62/180, time remaining: 8s
Rendered 63/180, time remaining: 8s
Rendered 64/180, time remaining: 8s
Rendered 65/180, time remaining: 8s
Rendered 66/180, time remaining: 8s
Rendered 67/180, time remaining: 8s
Rendered 68/180, time remaining: 8s
Rendered 69/180, time remaining: 8s
Rendered 70/180, time remaining: 8s
Rendered 70/180, time remaining: 8s
Rendered 71/180, time remaining: 8s
Rendered 72/180, time remaining: 8s
Rendered 73/180, time remaining: 7s
Rendered 74/180, time remaining: 7s
Rendered 75/180, time remaining: 7s
Rendered 76/180, time remaining: 7s
Rendered 77/180, time remaining: 7s
Rendered 77/180, time remaining: 7s
Rendered 78/180, time remaining: 7s
Rendered 79/180, time remaining: 7s
Rendered 80/180, time remaining: 7s
Rendered 81/180, time remaining: 7s
Rendered 82/180, time remaining: 7s
Rendered 83/180, time remaining: 7s
Rendered 83/180, time remaining: 7s
Rendered 84/180, time remaining: 7s
Rendered 85/180, time remaining: 7s
Rendered 86/180, time remaining: 7s
Rendered 87/180, time remaining: 7s
Rendered 88/180, time remaining: 6s
Rendered 89/180, time remaining: 6s
Rendered 90/180, time remaining: 6s
Rendered 91/180, time remaining: 6s
Rendered 91/180, time remaining: 6s
Rendered 92/180, time remaining: 6s
Rendered 93/180, time remaining: 6s
Rendered 94/180, time remaining: 6s
Rendered 95/180, time remaining: 6s
Rendered 96/180, time remaining: 6s
Rendered 97/180, time remaining: 6s
Rendered 98/180, time remaining: 6s
Rendered 98/180, time remaining: 6s
Rendered 99/180, time remaining: 6s
Rendered 100/180, time remaining: 5s
Rendered 101/180, time remaining: 5s
Rendered 102/180, time remaining: 5s
Rendered 103/180, time remaining: 5s
Rendered 104/180, time remaining: 5s
Rendered 104/180, time remaining: 5s
Rendered 105/180, time remaining: 5s
Rendered 106/180, time remaining: 5s
Rendered 107/180, time remaining: 5s
Rendered 108/180, time remaining: 5s
Rendered 109/180, time remaining: 5s
Rendered 110/180, time remaining: 5s
Rendered 111/180, time remaining: 5s
Rendered 112/180, time remaining: 4s
Rendered 113/180, time remaining: 4s
Rendered 113/180, time remaining: 4s
Rendered 114/180, time remaining: 4s
Rendered 115/180, time remaining: 4s
Rendered 116/180, time remaining: 4s
Rendered 117/180, time remaining: 4s
Rendered 118/180, time remaining: 4s
Rendered 119/180, time remaining: 4s
Rendered 119/180, time remaining: 4s
Rendered 120/180, time remaining: 4s
Rendered 121/180, time remaining: 4s
Rendered 122/180, time remaining: 4s
Rendered 123/180, time remaining: 4s
Rendered 124/180, time remaining: 4s
Rendered 125/180, time remaining: 4s
Rendered 126/180, time remaining: 3s
Rendered 127/180, time remaining: 3s
Rendered 127/180, time remaining: 3s
Rendered 128/180, time remaining: 3s
Rendered 129/180, time remaining: 3s
Rendered 130/180, time remaining: 3s
Rendered 131/180, time remaining: 3s
Rendered 132/180, time remaining: 3s
Rendered 133/180, time remaining: 3s
Rendered 134/180, time remaining: 3s
Rendered 134/180, time remaining: 3s
Rendered 135/180, time remaining: 3s
Rendered 136/180, time remaining: 3s
Rendered 137/180, time remaining: 3s
Rendered 138/180, time remaining: 3s
Rendered 139/180, time remaining: 2s
Rendered 140/180, time remaining: 2s
Rendered 141/180, time remaining: 2s
Rendered 142/180, time remaining: 2s
Rendered 142/180, time remaining: 2s
Rendered 143/180, time remaining: 2s
Rendered 144/180, time remaining: 2s
Rendered 145/180, time remaining: 2s
Rendered 146/180, time remaining: 2s
Rendered 147/180, time remaining: 2s
Rendered 148/180, time remaining: 2s
Rendered 149/180, time remaining: 2s
Rendered 149/180, time remaining: 2s
Rendered 150/180, time remaining: 2s
Rendered 151/180, time remaining: 2s
Rendered 152/180, time remaining: 1s
Rendered 153/180, time remaining: 1s
Rendered 154/180, time remaining: 1s
Rendered 155/180, time remaining: 1s
Rendered 155/180, time remaining: 1s
Rendered 156/180, time remaining: 1s
Rendered 157/180, time remaining: 1s
Rendered 158/180, time remaining: 1s
Rendered 159/180, time remaining: 1s
Rendered 160/180, time remaining: 1s
Rendered 161/180, time remaining: 1s
Rendered 162/180, time remaining: 1s
Rendered 163/180, time remaining: 1s
Rendered 164/180, time remaining: 1s
Rendered 164/180, time remaining: 1s
Rendered 165/180, time remaining: 1s
Rendered 166/180, time remaining: 0s
Rendered 167/180, time remaining: 0s
Rendered 168/180, time remaining: 0s
Rendered 169/180, time remaining: 0s
Rendered 170/180, time remaining: 0s
Rendered 170/180, time remaining: 0s
Rendered 171/180, time remaining: 0s
Rendered 172/180, time remaining: 0s
Rendered 173/180, time remaining: 0s
Rendered 174/180, time remaining: 0s
Rendered 175/180, time remaining: 0s
Rendered 176/180, time remaining: 0s
Rendered 177/180, time remaining: 0s
Rendered 178/180, time remaining: 0s
Rendered 178/180, time remaining: 0s
Rendered 179/180, time remaining: 0s
Encoded 97/180
Encoded 144/180
Encoded 180/180
+                    ../template.mp4 925.3 kB

exit_code=0

```

### typecheck.txt
```text
$ ./node_modules/.bin/tsc --noEmit

exit_code=0

```

### validate.txt
```text
$ python3 validate_template.py
PASS valid placeholder config
EXPECTED_REJECT overlap rect overlap
EXPECTED_REJECT real_avatar only placeholder implemented; real identity not accepted
EXPECTED_REJECT no_label visible placeholder label required
EXPECTED_REJECT voice voice generation not implemented

exit_code=0

```

### verification.json
```text
{
  "spec": "1920x1080 30fps 180frames 6sec",
  "audio_streams": 0,
  "mode": "placeholder only; no digital human or voice",
  "safe_rects_disjoint": true,
  "timeline_contiguous": true,
  "avatar_roi_diff_fraction_at_0.8_1.3": 0.15816091954022987,
  "roi_sha256": [
    "13069ae33528b483c52325af1cb541a281c67f6972783fdb48844e37a93f70d5",
    "e09e5da4659f5eefae03734ae72beac04a3f24e1777e3a287dfe77f811104697"
  ],
  "caveat": "ROI difference proves change, not lip sync or human identity; geometry validation is not pixel text-bound audit"
}

```

### verify.txt
```text
{
  "spec": "1920x1080 30fps 180frames 6sec",
  "audio_streams": 0,
  "mode": "placeholder only; no digital human or voice",
  "safe_rects_disjoint": true,
  "timeline_contiguous": true,
  "avatar_roi_diff_fraction_at_0.8_1.3": 0.15816091954022987,
  "roi_sha256": [
    "13069ae33528b483c52325af1cb541a281c67f6972783fdb48844e37a93f70d5",
    "e09e5da4659f5eefae03734ae72beac04a3f24e1777e3a287dfe77f811104697"
  ],
  "caveat": "ROI difference proves change, not lip sync or human identity; geometry validation is not pixel text-bound audit"
}

```

## 真实打印与逐页自检
# 最终A4 PDF逐页Read自检
2026-11-11 Asia/Shanghai；WeasyPrint70.0打印11页A4，每页已pdftoppm转PNG并通过Read逐张查看；同一worker，不是独立审核。

|页|观察|PNG SHA256|
|---|---|---|
|1|封面重点、边界与来源完整|c1a06732047b4207298fea0adabb6d7a7401af340778a84937698c97bce4963d|
|2|Q01/02答案及SVG完整|27d1e15315ca730d0d5d1eee091b401469a6ecdc98e4932eb2a0065290ab45f2|
|3|Q03/04答案及SVG完整|454163940253c917f11f4939056299657c10df4a94c8f5d6274e35087389d08c|
|4|Q05/06答案及SVG完整|e2f139116cb0370a6fd8bc943ab656afced1b920161c730d914815605a0a7109|
|5|Q07/08答案及SVG完整|6ae3097e3409716172d91bba2a83afd9b2e21dff3ad6e9df6e5290c26a555d12|
|6|Q09/10答案及SVG完整|803e67cc1a2e9c45bcc00541582020bde470bb2addc1d1ad422070afed9cef89|
|7|4用途、去重增量与契约完整|b25c5dbf2c4e156f68a2c617cbe61346335326ec92605ee0b4ddd846d7f61faf|
|8|步骤1–2命令/结果/验证无截断|d61055fc1d9137daa31ef1907b702433a690e4c8a8c1a5c3b872d2b89d17b6cc|
|9|步骤3–4命令/结果/验证无截断|bd6c8a6188c3abefa1267ba49a0d719bc97f5652077e8b0b902e9c1c1a83fb68|
|10|步骤5–6长命令正确折行，无越界|63bed51512ba843b60c295884a4397a141f571f65d738975a9a85332636bd6f6|
|11|四张抽帧、验收与待验证文字完整|f115cf2c5a8ac009e392e992ef2f8b747dab42721275a1f19ae35f1591a6cc0f|

完整PNG留云端pdf-pages/，轻量包仅带逐页哈希。HTML不嵌字体集，仅低分辨率JPEG和内联SVG；PDF嵌字体子集、压缩流，保持中文可读。

## 实际打包命令
```bash
python3 research/finish_delivery.py /workspace/reminder-batch/item07
```
Python zipfile.DEFLATED level9；exercise和light均testzip；MANIFEST逐文件SHA256。脚本保留云端。视频不在轻量包；依赖锁文件可恢复，未把用户任务勾为完成。
