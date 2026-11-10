# 第6项真实实验日志

2026-11-11（Asia/Shanghai，UTC+8）；单一路按顺序完成。非商业学习，自检非独立审核。

真实重渲染1920×1080、30fps、240帧；120BPM合成BGM；混流前后视频流SHA256一致，4张成片抽帧已读。

真实边界：仅验证本地制作与数值接口；没有复制热门作品、没有发布。引用涨粉/点赞、Opus效果、观众阅读和音乐听感均待验证。

原误标source-post.json隔离history后，按保存X原始响应的精确ID选取正确原帖与引用；逐字读完note_tweet/text，不把摘要当原文，未观看引用视频。未执行来源中“快试起号”“评论区咨询”等引导，没有发布或索取他人素材。

## 1. 核对来源并复用基线
目的：确定增量范围，不重复做第4项。
```bash
cd /workspace/reminder-batch/item06
# Read: research/x-original-and-quotes.txt及x-quote-direct.txt
# 核对post ID 2110570608375497107与2110554196953170106
# 对照第4项experiment-log及第5项knowledge-proposal
node --version
./exercise/node_modules/.bin/remotion --version
```
真实结果：原帖/引用文字完整已读；旧误标source-post.json隔离后更正。沿用Remotion4.0.542与第4项运行依赖。
验证：sources.md列出固定vault/Remotion SHA、阅读范围；未观看引用视频。

## 2. 生成原创文案与BGM
目的：避免外部音乐授权与配音依赖。
```bash
cd /workspace/reminder-batch/item06/exercise
# src/index.tsx已保存4句原创学习文案、60帧/幕
python3 synth.py
./node_modules/.bin/tsc --noEmit
```
真实结果：384000样本、48kHz、8秒、120BPM；TypeScript检查退出0。
验证：合成代码无语音/下载调用；声音输入仅bgm.wav。

## 3. 复用组件真实渲染
目的：先输出纯视频，不冒称模型生成。
```bash
cd /workspace/reminder-batch/item06/exercise
./node_modules/.bin/remotion render src/index.tsx VibeLab ../silent-resume.mp4 --concurrency=2 --browser-executable=/usr/bin/google-chrome
```
真实结果：本轮真实重渲染240帧静音视频，退出0；原旧文件保留。
验证：research/resume/render.txt保留CLI输出；没有付费API或新云代理。

## 4. 混入合成音乐
目的：显式选流，保留视频压缩数据。
```bash
cd /workspace/reminder-batch/item06
ffmpeg -y -v error -i silent-resume.mp4 -i exercise/bgm.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 128k -shortest vibe-resume.mp4
```
真实结果：实际产出带AAC的8秒MP4，混流退出0。
验证：后续检查前后视频流SHA256，避免把copy参数当证据。

## 5. 数值与抽帧核验
目的：检查音画、节奏与可读性。
```bash
cd /workspace/reminder-batch/item06
python3 exercise/verify.py
ffmpeg -y -v error -i vibe-resume.mp4 -vf "select='eq(n,30)+eq(n,90)+eq(n,150)+eq(n,210)',scale=640:360" -fps_mode vfr frames/resume-%02d.jpg
ffmpeg -hide_banner -i vibe-resume.mp4 -af volumedetect -vn -f null -
```
真实结果：8秒1080p/30fps/240帧，1视频+1音频；PCM峰值0.27475，16拍包络；前后视频流哈希相同。
验证：四张JPEG逐张Read；阅读速度、听感和增长仍未测试。

## 6. 打印并轻量打包
目的：让学习成果可读可重放。
```bash
cd /workspace/reminder-batch/item06
python3 research/build-guide.py
../item04/research/pdf-venv/bin/python -m weasyprint guide.html guide.pdf
mkdir -p pdf-pages
pdftoppm -scale-to 1200 -png guide.pdf pdf-pages/page
# 逐页Read后，Python zipfile生成exercise.zip及命名light.zip
```
真实结果：单文件中文HTML、A4 PDF、代码ZIP及日志真实生成。
验证：每页检查与包哈希见experiment-log.md；轻量包不含视频/整套字体。

## 实际原始输出

### audio-level.txt
```text
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'vibe-resume.mp4':
  Metadata:
    major_brand     : isom
    minor_version   : 512
    compatible_brands: isomiso2avc1mp41
    encoder         : Lavf61.7.103
    comment         : Made with Remotion 4.0.542
  Duration: 00:00:08.00, start: 0.000000, bitrate: 1275 kb/s
  Stream #0:0[0x1](und): Video: h264 (High) (avc1 / 0x31637661), yuvj420p(pc, bt470bg/unknown/unknown, progressive), 1920x1080 [SAR 1:1 DAR 16:9], 1139 kb/s, 30 fps, 30 tbr, 90k tbn (default)
      Metadata:
        handler_name    : VideoHandler
        vendor_id       : [0][0][0][0]
      Side data:
        ICC Profile
  Stream #0:1[0x2](und): Audio: aac (LC) (mp4a / 0x6134706D), 48000 Hz, mono, fltp, 125 kb/s (default)
      Metadata:
        handler_name    : SoundHandler
        vendor_id       : [0][0][0][0]
[Parsed_volumedetect_0 @ 0x559eee0fa700] n_samples: 0
Stream mapping:
  Stream #0:1 -> #0:0 (aac (native) -> pcm_s16le (native))
Press [q] to stop, [?] for help
Output #0, null, to 'pipe:':
  Metadata:
    major_brand     : isom
    minor_version   : 512
    compatible_brands: isomiso2avc1mp41
    comment         : Made with Remotion 4.0.542
    encoder         : Lavf61.7.103
  Stream #0:0(und): Audio: pcm_s16le, 48000 Hz, mono, s16, 768 kb/s (default)
      Metadata:
        handler_name    : SoundHandler
        vendor_id       : [0][0][0][0]
        encoder         : Lavc61.19.101 pcm_s16le
[Parsed_volumedetect_0 @ 0x7fa3d0002e00] n_samples: 384000
[Parsed_volumedetect_0 @ 0x7fa3d0002e00] mean_volume: -29.4 dB
[Parsed_volumedetect_0 @ 0x7fa3d0002e00] max_volume: -11.2 dB
[Parsed_volumedetect_0 @ 0x7fa3d0002e00] histogram_11db: 361
[Parsed_volumedetect_0 @ 0x7fa3d0002e00] histogram_12db: 383
[out#0/null @ 0x559eee02ae80] video:0KiB audio:750KiB subtitle:0KiB other streams:0KiB global headers:0KiB muxing overhead: unknown
size=N/A time=00:00:08.00 bitrate=N/A speed= 960x    

```

### environment.txt
```text
v24.22.1
@remotion/cli 4.0.542
© 2026 Remotion AG

Available commands:

remotion studio <entry-point>?
Start the Remotion Studio.
https://www.remotion.dev/docs/cli/studio

remotion render [<entry-point|serve-url>] [<composition-id>] [<output-location>]
Render video, audio or an image sequence.
https://www.remotion.dev/docs/cli/render

remotion still <serve-url|entry-point>? [<composition-id>] [<output-location>]
Render a still frame and save it as an image.
https://www.remotion.dev/docs/cli/still

remotion compositions <serve-url|entry-file>?
Print the available compositions.
https://www.remotion.dev/docs/cli/compositions

remotion lambda <command>
Control Remotion Lambda.
https://www.remotion.dev/docs/lambda/cli

remotion bundle <serve-url|entry-file>?
Create a Remotion bundle to be deployed to the web.
https://www.remotion.dev/docs/cli/bundle

remotion browser <command>
Ensure Remotion has a browser it can use for rendering.
https://www.remotion.dev/docs/cli/browser

remotion cloudrun <command>
Control Remotion Cloud Run.
https://www.remotion.dev/docs/cloudrun/cli

remotion benchmark [<entry-point>] [composition-ids]
Benchmark rendering one or more compositions.
https://www.remotion.dev/docs/cli/benchmark

remotion skills <add | update>
Install or update skills from remotion-dev/skills.
https://www.remotion.dev/docs/cli/skills

remotion versions
Print and validate versions of all Remotion packages.
https://www.remotion.dev/docs/cli/versions

remotion upgrade
Ensure Remotion is on the newest version.
https://www.remotion.dev/docs/cli/upgrade

remotion add <package-name...>
Add Remotion packages with the correct version.
https://www.remotion.dev/docs/cli/add

remotion elements <command>
Install Elements from Element Libraries.
https://www.remotion.dev/docs/cli/elements

remotion gpu
Print information about how Chrome uses the GPU.
https://www.remotion.dev/docs/cli/gpu

remotion ffmpeg <arguments...>
Execute FFmpeg with all arguments forwarded.
https://www.remotion.dev/docs/cli/ffmpeg

remotion ffprobe <arguments...>
Execute FFprobe with all arguments forwarded.
https://www.remotion.dev/docs/cli/ffprobe

remotion help <command...>
Print available commands and flags for the Remotion CLI.
https://www.remotion.dev/docs/cli/help

Visit https://www.remotion.dev/docs/cli for browsable CLI documentation.

```

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
      "duration_ts": 720000,
      "duration": "8.000000",
      "bit_rate": "1139458",
      "bits_per_raw_sample": "8",
      "nb_frames": "240",
      "nb_read_frames": "240",
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
    },
    {
      "index": 1,
      "codec_name": "aac",
      "codec_long_name": "AAC (Advanced Audio Coding)",
      "profile": "LC",
      "codec_type": "audio",
      "codec_tag_string": "mp4a",
      "codec_tag": "0x6134706d",
      "sample_fmt": "fltp",
      "sample_rate": "48000",
      "channels": 1,
      "channel_layout": "mono",
      "bits_per_sample": 0,
      "initial_padding": 0,
      "id": "0x2",
      "r_frame_rate": "0/0",
      "avg_frame_rate": "0/0",
      "time_base": "1/48000",
      "start_pts": 0,
      "start_time": "0.000000",
      "duration_ts": 384000,
      "duration": "8.000000",
      "bit_rate": "125678",
      "nb_frames": "376",
      "nb_read_frames": "375",
      "extradata_size": 5,
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
        "handler_name": "SoundHandler",
        "vendor_id": "[0][0][0][0]"
      }
    }
  ],
  "format": {
    "filename": "/workspace/reminder-batch/item06/vibe-resume.mp4",
    "nb_streams": 2,
    "nb_programs": 0,
    "nb_stream_groups": 0,
    "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
    "format_long_name": "QuickTime / MOV",
    "start_time": "0.000000",
    "duration": "8.000000",
    "size": "1275762",
    "bit_rate": "1275762",
    "probe_score": 100,
    "tags": {
      "major_brand": "isom",
      "minor_version": "512",
      "compatible_brands": "isomiso2avc1mp41",
      "encoder": "Lavf61.7.103",
      "comment": "Made with Remotion 4.0.542"
    }
  }
}

```

### mux.txt
```text

exit_code=0

```

### render.txt
```text
$ ./node_modules/.bin/remotion render src/index.tsx VibeLab ../silent-resume.mp4 --concurrency=2 --browser-executable=/usr/bin/google-chrome
Bundling 6%
Bundling 32%
Bundling 42%
Bundling 65%
Bundling 71%
Bundling 76%
Bundling 81%
Bundling 87%
Bundling 92%
Bundling 98%
Bundling 100%
Getting composition
Composition          VibeLab
Codec                h264
Output               ../silent-resume.mp4
Concurrency          2x
Rendered 0/240
Rendered 1/240, time remaining: 1m 19s
Rendered 2/240, time remaining: 1m 1s
Rendered 3/240, time remaining: 40s
Rendered 4/240, time remaining: 35s
Rendered 5/240, time remaining: 32s
Rendered 6/240, time remaining: 27s
Rendered 7/240, time remaining: 24s
Rendered 8/240, time remaining: 25s
Rendered 9/240, time remaining: 22s
Rendered 10/240, time remaining: 21s
Rendered 11/240, time remaining: 22s
Rendered 12/240, time remaining: 20s
Rendered 13/240, time remaining: 20s
Rendered 14/240, time remaining: 21s
Rendered 15/240, time remaining: 19s
Rendered 16/240, time remaining: 19s
Rendered 17/240, time remaining: 19s
Rendered 18/240, time remaining: 18s
Rendered 19/240, time remaining: 18s
Rendered 20/240, time remaining: 18s
Rendered 21/240, time remaining: 17s
Rendered 22/240, time remaining: 17s
Rendered 23/240, time remaining: 18s
Rendered 24/240, time remaining: 17s
Rendered 25/240, time remaining: 17s
Rendered 26/240, time remaining: 17s
Rendered 27/240, time remaining: 16s
Rendered 28/240, time remaining: 16s
Rendered 29/240, time remaining: 17s
Rendered 30/240, time remaining: 16s
Rendered 31/240, time remaining: 16s
Rendered 32/240, time remaining: 16s
Rendered 33/240, time remaining: 15s
Rendered 34/240, time remaining: 15s
Rendered 35/240, time remaining: 16s
Rendered 36/240, time remaining: 15s
Rendered 37/240, time remaining: 15s
Rendered 38/240, time remaining: 15s
Rendered 39/240, time remaining: 15s
Rendered 40/240, time remaining: 15s
Rendered 41/240, time remaining: 15s
Rendered 42/240, time remaining: 14s
Rendered 43/240, time remaining: 14s
Rendered 44/240, time remaining: 15s
Rendered 45/240, time remaining: 14s
Rendered 46/240, time remaining: 14s
Rendered 47/240, time remaining: 14s
Rendered 48/240, time remaining: 14s
Rendered 49/240, time remaining: 14s
Rendered 50/240, time remaining: 14s
Rendered 51/240, time remaining: 14s
Rendered 52/240, time remaining: 13s
Rendered 53/240, time remaining: 14s
Rendered 54/240, time remaining: 13s
Rendered 55/240, time remaining: 13s
Rendered 56/240, time remaining: 13s
Rendered 57/240, time remaining: 13s
Rendered 58/240, time remaining: 13s
Rendered 59/240, time remaining: 13s
Rendered 60/240, time remaining: 13s
Rendered 61/240, time remaining: 13s
Rendered 62/240, time remaining: 13s
Rendered 63/240, time remaining: 12s
Rendered 64/240, time remaining: 12s
Rendered 65/240, time remaining: 13s
Rendered 66/240, time remaining: 12s
Rendered 67/240, time remaining: 12s
Rendered 68/240, time remaining: 12s
Rendered 69/240, time remaining: 12s
Rendered 70/240, time remaining: 12s
Rendered 70/240, time remaining: 12s
Rendered 71/240, time remaining: 12s
Rendered 72/240, time remaining: 12s
Rendered 73/240, time remaining: 12s
Rendered 74/240, time remaining: 12s
Rendered 75/240, time remaining: 12s
Rendered 76/240, time remaining: 11s
Rendered 76/240, time remaining: 11s
Rendered 77/240, time remaining: 11s
Rendered 78/240, time remaining: 11s
Rendered 79/240, time remaining: 11s
Rendered 80/240, time remaining: 11s
Rendered 81/240, time remaining: 11s
Rendered 82/240, time remaining: 11s
Rendered 83/240, time remaining: 11s
Rendered 84/240, time remaining: 11s
Rendered 84/240, time remaining: 11s
Rendered 85/240, time remaining: 11s
Rendered 86/240, time remaining: 11s
Rendered 87/240, time remaining: 11s
Rendered 88/240, time remaining: 10s
Rendered 89/240, time remaining: 11s
Rendered 90/240, time remaining: 10s
Rendered 91/240, time remaining: 10s
Rendered 91/240, time remaining: 10s
Rendered 92/240, time remaining: 10s
Rendered 93/240, time remaining: 10s
Rendered 94/240, time remaining: 10s
Rendered 95/240, time remaining: 10s
Rendered 96/240, time remaining: 10s
Rendered 97/240, time remaining: 10s
Rendered 97/240, time remaining: 10s
Rendered 98/240, time remaining: 10s
Rendered 99/240, time remaining: 10s
Rendered 100/240, time remaining: 10s
Rendered 101/240, time remaining: 10s
Rendered 102/240, time remaining: 9s
Rendered 103/240, time remaining: 9s
Rendered 104/240, time remaining: 9s
Rendered 105/240, time remaining: 9s
Rendered 105/240, time remaining: 9s
Rendered 106/240, time remaining: 9s
Rendered 107/240, time remaining: 9s
Rendered 108/240, time remaining: 9s
Rendered 109/240, time remaining: 9s
Rendered 110/240, time remaining: 9s
Rendered 111/240, time remaining: 9s
Rendered 112/240, time remaining: 9s
Rendered 112/240, time remaining: 9s
Rendered 113/240, time remaining: 9s
Rendered 114/240, time remaining: 9s
Rendered 115/240, time remaining: 8s
Rendered 116/240, time remaining: 8s
Rendered 117/240, time remaining: 8s
Rendered 118/240, time remaining: 8s
Rendered 119/240, time remaining: 8s
Rendered 120/240, time remaining: 8s
Rendered 120/240, time remaining: 8s
Rendered 121/240, time remaining: 8s
Rendered 122/240, time remaining: 8s
Rendered 123/240, time remaining: 8s
Rendered 124/240, time remaining: 8s
Rendered 125/240, time remaining: 8s
Rendered 126/240, time remaining: 8s
Rendered 127/240, time remaining: 8s
Rendered 127/240, time remaining: 8s
Rendered 128/240, time remaining: 8s
Rendered 129/240, time remaining: 7s
Rendered 130/240, time remaining: 7s
Rendered 131/240, time remaining: 7s
Rendered 132/240, time remaining: 7s
Rendered 133/240, time remaining: 7s
Rendered 133/240, time remaining: 7s
Rendered 134/240, time remaining: 7s
Rendered 135/240, time remaining: 7s
Rendered 136/240, time remaining: 7s
Rendered 137/240, time remaining: 7s
Rendered 138/240, time remaining: 7s
Rendered 139/240, time remaining: 7s
Rendered 140/240, time remaining: 7s
Rendered 141/240, time remaining: 7s
Rendered 141/240, time remaining: 7s
Rendered 142/240, time remaining: 6s
Rendered 143/240, time remaining: 6s
Rendered 144/240, time remaining: 6s
Rendered 145/240, time remaining: 6s
Rendered 146/240, time remaining: 6s
Rendered 147/240, time remaining: 6s
Rendered 148/240, time remaining: 6s
Rendered 148/240, time remaining: 6s
Rendered 149/240, time remaining: 6s
Rendered 150/240, time remaining: 6s
Rendered 151/240, time remaining: 6s
Rendered 152/240, time remaining: 6s
Rendered 153/240, time remaining: 6s
Rendered 154/240, time remaining: 5s
Rendered 155/240, time remaining: 5s
Rendered 156/240, time remaining: 5s
Rendered 156/240, time remaining: 5s
Rendered 157/240, time remaining: 5s
Rendered 158/240, time remaining: 5s
Rendered 159/240, time remaining: 5s
Rendered 160/240, time remaining: 5s
Rendered 161/240, time remaining: 5s
Rendered 162/240, time remaining: 5s
Rendered 163/240, time remaining: 5s
Rendered 163/240, time remaining: 5s
Rendered 164/240, time remaining: 5s
Rendered 165/240, time remaining: 5s
Rendered 166/240, time remaining: 5s
Rendered 167/240, time remaining: 5s
Rendered 168/240, time remaining: 5s
Rendered 169/240, time remaining: 4s
Rendered 169/240, time remaining: 4s
Rendered 170/240, time remaining: 4s
Rendered 171/240, time remaining: 4s
Rendered 172/240, time remaining: 4s
Rendered 173/240, time remaining: 4s
Rendered 174/240, time remaining: 4s
Rendered 175/240, time remaining: 4s
Rendered 176/240, time remaining: 4s
Rendered 177/240, time remaining: 4s
Rendered 178/240, time remaining: 4s
Rendered 178/240, time remaining: 4s
Rendered 179/240, time remaining: 4s
Rendered 180/240, time remaining: 4s
Rendered 181/240, time remaining: 4s
Rendered 182/240, time remaining: 4s
Rendered 183/240, time remaining: 3s
Rendered 184/240, time remaining: 3s
Rendered 184/240, time remaining: 3s
Rendered 185/240, time remaining: 3s
Rendered 186/240, time remaining: 3s
Rendered 187/240, time remaining: 3s
Rendered 188/240, time remaining: 3s
Rendered 189/240, time remaining: 3s
Rendered 190/240, time remaining: 3s
Rendered 191/240, time remaining: 3s
Rendered 192/240, time remaining: 3s
Rendered 192/240, time remaining: 3s
Rendered 193/240, time remaining: 3s
Rendered 194/240, time remaining: 3s
Rendered 195/240, time remaining: 3s
Rendered 196/240, time remaining: 3s
Rendered 197/240, time remaining: 2s
Rendered 198/240, time remaining: 2s
Rendered 199/240, time remaining: 2s
Rendered 199/240, time remaining: 2s
Rendered 200/240, time remaining: 2s
Rendered 201/240, time remaining: 2s
Rendered 202/240, time remaining: 2s
Rendered 203/240, time remaining: 2s
Rendered 204/240, time remaining: 2s
Rendered 205/240, time remaining: 2s
Rendered 206/240, time remaining: 2s
Rendered 207/240, time remaining: 2s
Rendered 207/240, time remaining: 2s
Rendered 208/240, time remaining: 2s
Rendered 209/240, time remaining: 2s
Rendered 210/240, time remaining: 2s
Rendered 211/240, time remaining: 2s
Rendered 212/240, time remaining: 1s
Rendered 213/240, time remaining: 1s
Rendered 214/240, time remaining: 1s
Rendered 214/240, time remaining: 1s
Rendered 215/240, time remaining: 1s
Rendered 216/240, time remaining: 1s
Rendered 217/240, time remaining: 1s
Rendered 218/240, time remaining: 1s
Rendered 219/240, time remaining: 1s
Rendered 220/240, time remaining: 1s
Rendered 220/240, time remaining: 1s
Rendered 221/240, time remaining: 1s
Rendered 222/240, time remaining: 1s
Rendered 223/240, time remaining: 1s
Rendered 224/240, time remaining: 1s
Rendered 225/240, time remaining: 1s
Rendered 226/240, time remaining: 0s
Rendered 227/240, time remaining: 0s
Rendered 228/240, time remaining: 0s
Rendered 228/240, time remaining: 0s
Rendered 229/240, time remaining: 0s
Rendered 230/240, time remaining: 0s
Rendered 231/240, time remaining: 0s
Rendered 232/240, time remaining: 0s
Rendered 233/240, time remaining: 0s
Rendered 234/240, time remaining: 0s
Rendered 235/240, time remaining: 0s
Rendered 235/240, time remaining: 0s
Rendered 236/240, time remaining: 0s
Rendered 237/240, time remaining: 0s
Rendered 238/240, time remaining: 0s
Rendered 239/240, time remaining: 0s
Encoded 142/240
Encoded 192/240
Encoded 240/240
+                    ../silent-resume.mp4 1.1 MB

exit_code=0

```

### synth.txt
```text
$ python3 synth.py
{"sample_rate": 48000, "samples": 384000, "peak": 0.2747612368283126, "bpm": 120, "beat_frames_at_30fps": 15}

exit_code=0

```

### typecheck.txt
```text
$ ./node_modules/.bin/tsc --noEmit

exit_code=0

```

### verification.json
```text
{
  "spec": "1920x1080 30fps 240frames 8sec",
  "audio": "AAC 48000Hz mono; only input is synthesized BGM; no voiceover source",
  "wave_samples": 384000,
  "wave_peak": 0.274749755859375,
  "wave_rms": 0.03388352669688955,
  "bpm": 120,
  "frames_per_beat": 15,
  "scene_start_frames": [
    0,
    60,
    120,
    180
  ],
  "scene_grid_aligned": true,
  "beat_attack_tail_energy_ratio_min": 50.87604868615443,
  "beat_count": 16,
  "video_packet_sha_equal": true,
  "video_packet_sha": "SHA256=d3679f98f8f644791bebd1749c5ba77656442c3bf2bf66e41736ff2d3c405fab"
}

```

### verify.txt
```text
{
  "spec": "1920x1080 30fps 240frames 8sec",
  "audio": "AAC 48000Hz mono; only input is synthesized BGM; no voiceover source",
  "wave_samples": 384000,
  "wave_peak": 0.274749755859375,
  "wave_rms": 0.03388352669688955,
  "bpm": 120,
  "frames_per_beat": 15,
  "scene_start_frames": [
    0,
    60,
    120,
    180
  ],
  "scene_grid_aligned": true,
  "beat_attack_tail_energy_ratio_min": 50.87604868615443,
  "beat_count": 16,
  "video_packet_sha_equal": true,
  "video_packet_sha": "SHA256=d3679f98f8f644791bebd1749c5ba77656442c3bf2bf66e41736ff2d3c405fab"
}

```

## 真实打印与逐页自检
# 最终A4 PDF逐页Read自检
2026-11-11 Asia/Shanghai；WeasyPrint70.0打印11页A4，每页已pdftoppm转PNG并通过Read逐张查看；同一worker，不是独立审核。

|页|观察|PNG SHA256|
|---|---|---|
|1|封面重点、边界与来源完整|6859d790400cce89a6dfdea4b8bf5fdf5aa4fb63875cda2c9e186fe940da32d1|
|2|Q01/02答案及SVG完整|8a71665707593f8b3174f4092e3afc1019fe985b174f34ac3a9ee12fbdc9f683|
|3|Q03/04答案及SVG完整|eb79ce5a38c403d4723c6790added1f7a0adaa27241ab5ad845f4422eae43bb9|
|4|Q05/06答案及SVG完整|76ba870bf0c62e6fe61a49c7e3024791889a624aa23df9c7abc84652f56b24b9|
|5|Q07/08答案及SVG完整|c55db6b48122a4ccce0fe74128952ba3e50729e1515525b1546ca636d1db2fd8|
|6|Q09/10答案及SVG完整|bc065f981795108f721515714a2767dec48cf5046f1b9ce4e960032320c4e5a8|
|7|4用途、去重增量与契约完整|26511aa2abb465a87430c95a3fb4fa28577acca4936ebeea997c8ff525ca5a21|
|8|步骤1–2命令/结果/验证无截断|005124f349e063e6dc0bada960c1866065d970c98b733e40d7b2d2ce7e2833fc|
|9|步骤3–4命令/结果/验证无截断|4095b264139371fed85df586b5908e556cfd7dac5c1ce64b36ce192327b53cce|
|10|步骤5–6长命令正确折行，无越界|61a48c89a6a6925701942a3d2c979ced2560893e99345d50067b5111e0fa94f0|
|11|四张抽帧、验收与待验证文字完整|5ff9ddedb0ab56e6a4c7173a5eef2d0b7218e0dab67179382e2a7d049202494c|

完整PNG留云端pdf-pages/，轻量包仅带逐页哈希。HTML不嵌字体集，仅低分辨率JPEG和内联SVG；PDF嵌字体子集、压缩流，保持中文可读。

CLI小差异：remotion --version打印版本与help后退出1，不是额度错误；真实渲染/tsc/混流/verify均退出0。Node依赖沿用第4项，未声称本轮重新联网安装；没有人工听评，只有输入来源检查与PCM数值/音轨验证。

## 实际打包命令
```bash
python3 research/finish_delivery.py /workspace/reminder-batch/item06
```
Python zipfile.DEFLATED level9；exercise和light均testzip；MANIFEST逐文件SHA256。脚本保留云端。视频不在轻量包；依赖锁文件可恢复，未把用户任务勾为完成。
