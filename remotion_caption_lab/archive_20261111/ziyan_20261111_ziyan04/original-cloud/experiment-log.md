# 第4项真实实验日志
日期：2026-11-11（Asia/Shanghai）
执行者：同一学习worker，自检不是独立审核。所有实验在box云端隔离目录完成；未访问本机F盘、未用用户密钥、未付费、未发布Git、未改任务或日程。

## 来源与查重
- 原帖及引用通过x MCP get_posts_by_id读取：2110962673219215719，引用2110634009890013442；正文摘录见research/x-post-reading.md。宣传部分仅记录、不采信；引用视频未观看。
- vault main固定a8674777e18302b8804b137212b1396cbfe5a747，读总览与相关笔记；已有Remotion/TTS与动效词表，增量见knowledge-proposal.md。
- Remotion main固定e3a1be5c8b29c07ec3d36efe16cbc69b6170cb5d，读取Composition/Sequence文档、interpolate源码、包版本及LICENSE；npm固定4.0.542。

## 实验步骤及真实命令
### 1 环境
```
node --version
npm --version
which ffmpeg ffprobe chromium google-chrome
fc-list :lang=zh family
```
实际：Node v24.22.1，npm 11.21.1；ffmpeg=/usr/bin/ffmpeg，ffprobe=/usr/bin/ffprobe，Chrome=/usr/bin/google-chrome；字体Noto Sans CJK SC可用。
初次研究脚本误用`python`，实际报`python: command not found`，退出127；改用已安装python3成功。没有安装Node，因为已存在。

### 2 scaffold
在exercise中创建package.json、src/index.tsx、tsconfig.json、README.md，手写最小Remotion scaffold，没有调用create-video模板，也没有调用原帖宣传模型。
```
cd /workspace/reminder-batch/item04/exercise
npm install 2>&1 | tee ../research/npm-install.txt
```
实际安装245包、审计246包、0 vulnerabilities（只是该次npm审计结果，不代表全面安全审计）。npm提示esbuild安装脚本未列入allowScripts；未更改安全设置、未运行approve；后续编译和渲染正常。
完整首次输出：
```

added 245 packages, and audited 246 packages in 10s

48 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
npm warn install-scripts 1 package has install scripts not yet covered by allowScripts:
npm warn install-scripts   esbuild@0.28.1 (postinstall: node install.js)
npm warn install-scripts
npm warn install-scripts Run `npm install-scripts ls` to review, or `npm install-scripts approve <pkg>` to allow.
```

### 3 组件与类型检查
worker直接编写4个scene，主题《把一句话变成可验收短片》，各90帧，1920×1080，30fps，共360帧；字幕承担叙事，无口播无音轨。标题位移spring，三卡7帧错峰spring，线性进度条；不使用随机数和真实时钟。
```
npx tsc --noEmit 2>&1 | tee ../research/typecheck.txt
```
实际退出0，无诊断，typecheck.txt为空。

### 4 真正渲染
```
set -o pipefail
npx remotion render src/index.tsx CaptionLab ../caption-lab.mp4 --concurrency=2 --browser-executable=/usr/bin/google-chrome 2>&1 | tee ../research/render.txt
```
类型检查＋渲染这次Shell任务实际退出0，工具记录总耗时40122ms（包含两命令与shell，不是作者性能，也不当成通用渲染benchmark）。未传改变安全策略的CLI参数。完整原始CLI输出在research/render.txt；末段原样：
```
dered 345/360, time remaining: 1s
Rendered 346/360, time remaining: 0s
Rendered 347/360, time remaining: 0s
Rendered 348/360, time remaining: 0s
Rendered 349/360, time remaining: 0s
Rendered 350/360, time remaining: 0s
Rendered 351/360, time remaining: 0s
Rendered 352/360, time remaining: 0s
Rendered 352/360, time remaining: 0s
Rendered 353/360, time remaining: 0s
Rendered 354/360, time remaining: 0s
Rendered 355/360, time remaining: 0s
Rendered 356/360, time remaining: 0s
Rendered 357/360, time remaining: 0s
Rendered 358/360, time remaining: 0s
Rendered 359/360, time remaining: 0s
Encoded 236/360
Encoded 242/360
Encoded 288/360
Encoded 360/360
+                    ../caption-lab.mp4 1.3 MB
```

### 5 ffprobe、抽帧与断言
```
cd /workspace/reminder-batch/item04
ffprobe -v error -show_streams -show_format -of json caption-lab.mp4 > research/ffprobe.json
ffmpeg -hide_banner -i caption-lab.mp4 -vf "select='eq(n,45)+eq(n,135)+eq(n,225)+eq(n,315)'" -vsync 0 frames/scene-%02d.png > research/extract.txt 2>&1
python3 exercise/verify.py
```
实际：H.264，1920×1080，30/1 fps，12.000000秒，360帧；仅1视频流、0音频流；文件1,271,452字节。
断言输出：
```
one_video PASS
1080p PASS
30fps PASS
12s PASS
360frames PASS
no_audio PASS
```
使用Read逐一查看frames/scene-01.png至scene-04.png（全局45/135/225/315帧）：中文正常，无方框；标题/卡片/字幕可辨；未见裁切或重叠。不是全帧审片，没有观众阅读实验。

完整ffprobe原始输出：
```json
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
            "coded_height": 1080,
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
            "refs": 1,
            "is_avc": "true",
            "nal_length_size": "4",
            "id": "0x1",
            "r_frame_rate": "30/1",
            "avg_frame_rate": "30/1",
            "time_base": "1/90000",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 1080000,
            "duration": "12.000000",
            "bit_rate": "844188",
            "bits_per_raw_sample": "8",
            "nb_frames": "360",
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
        "filename": "caption-lab.mp4",
        "nb_streams": 1,
        "nb_programs": 0,
        "nb_stream_groups": 0,
        "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
        "format_long_name": "QuickTime / MOV",
        "start_time": "0.000000",
        "duration": "12.000000",
        "size": "1271452",
        "bit_rate": "847634",
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

### 6 实际打印A4 PDF与逐页检查
```
python3 -m venv research/pdf-venv
research/pdf-venv/bin/pip install weasyprint
python3 research/build-guide.py
research/pdf-venv/bin/weasyprint guide.html guide.pdf
pdftoppm -scale-to 1100 -png guide.pdf pdf-pages/page
```
首版实际13页；已用Read检查第1–13页。发现末页状态表跨到第13页，不满意；通过只调末页evidence字号/行距/缩略图高度修正，不改正文或硬凑结果。
```
python3 research/build-guide.py
research/pdf-venv/bin/weasyprint guide.html guide.pdf > research/pdf-render.txt 2>&1
pdftoppm -scale-to 1100 -png guide.pdf pdf-pages/final
pdfinfo guide.pdf > research/pdfinfo.txt
```
最终实际12页A4。使用Read再次逐页查看pdf-pages/final-01.png至final-12.png：
- 01：封面、真实规格、版本边界，完整。
- 02：Q1–Q2，SVG与文字完整。
- 03：Q3–Q4，规格计算完整。
- 04：Q5–Q6，字幕时长和局部帧图完整。
- 05：Q7–Q8，确定性与插值图完整。
- 06：Q9–Q10，字体与验收图完整。
- 07：Q11–Q12，复现与边界图完整。
- 08：4种用途与改写提示词，无出界。
- 09：实验步骤1–2，命令正常换行。
- 10：实验步骤3–4，命令正常换行。
- 11：实验步骤5–6，代码与验证完整。
- 12：四抽帧、版本边界和完整状态表都在同页，无孤立表尾。
最终PDF信息原样：
```
Title:           Remotion无口播中文字幕｜第4项增量指南
Producer:        WeasyPrint 70.0
Custom Metadata: no
Metadata Stream: no
Tagged:          no
UserProperties:  no
Suspects:        no
Form:            none
JavaScript:      no
Pages:           12
Encrypted:       no
Page size:       595.276 x 841.89 pts (A4)
Page rot:        0
File size:       2126957 bytes
Optimized:       no
PDF version:     1.7
```
HTML为单文件（内嵌4张PNG与12个SVG），无外链脚本。没有伪造独立审核。

## 状态
真实完成：原帖/引用文字读取、仓库查重、固定来源、12问+SVG、4用途、6步实验、Remotion MP4、四帧自检、单文件HTML、A4 PDF实际打印与12页Read检查、代码ZIP与来源/候选增量。
待验证：原帖所谓模型的一句话导演能力、商业流量/效果、引用视频制作归属、长字幕观众阅读效果、跨机器逐像素一致性、新API迁移。
受阻：本项无剩余实验阻断。初次python命令不存在已明确改正。
未执行：Git发布、vault合入、任务勾选、日程创建、付费API调用。
