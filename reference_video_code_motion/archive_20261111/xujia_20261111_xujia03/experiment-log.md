# 第3项真实实验日志

2026-11-11T01:25:43.404011+08:00（Asia/Shanghai）
教学代码为原创CPU三维投影/音频实验，不是作者源码或Opus输出，未执行onetake渲染脚本。

## 步骤1 已执行
```bash
cd /workspace/xujia-batch/item03/exercise
python3 lab.py source_audit
```
```text
{"source_tokens": ["window.__seek", "window.__ready", "SRGB_TO_LIN", "__motion", "--workers", "--gpu"], "tokens_verified": 6, "sha": "abb6d17279cdc749e27e99aa534a062d8fd01ced", "license": "PolyForm Noncommercial 1.0.0", "upstream_renderer_executed": false, "blender_executed": false, "paid_model_calls": 0}

exit_code=0
elapsed_wall_seconds=0.119
```

## 步骤2 已执行
```bash
cd /workspace/xujia-batch/item03/exercise
python3 lab.py timeline
```
```text
{"out_of_order_seek_identical": true, "max_boundary_delta": 1.6874999998917062e-05, "linear_light_black_white_average": 188, "gamma_space_average": 128, "frames": 312, "samples_audio": 624000, "duration_ratio": 4.166666666666667, "note": "continuous parameters only; not proof of subjective shot continuity or GPU rendering"}

exit_code=0
elapsed_wall_seconds=0.154
```

## 步骤3 已执行
```bash
cd /workspace/xujia-batch/item03/exercise
python3 lab.py audio
```
```text
{"samples": 624000, "duration_seconds": 13.0, "peak": 0.4526826221393474, "clipped_samples": 0, "event_marks": [{"event": "enter", "sample": 19200, "time": 0.4, "error": 0.0, "nearest_video_frame": 10, "nearest_frame_error_seconds": 0.016666666666666663}, {"event": "land", "sample": 76800, "time": 1.6, "error": 0.0, "nearest_video_frame": 38, "nearest_frame_error_seconds": 0.01666666666666683}, {"event": "orbit", "sample": 168000, "time": 3.5, "error": 0.0, "nearest_video_frame": 84, "nearest_frame_error_seconds": 0.0}, {"event": "reframe", "sample": 408000, "time": 8.5, "error": 0.0, "nearest_video_frame": 204, "nearest_frame_error_seconds": 0.0}, {"event": "settle", "sample": 537600, "time": 11.2, "error": 0.0, "nearest_video_frame": 269, "nearest_frame_error_seconds": 0.008333333333334636}]}

exit_code=0
elapsed_wall_seconds=0.229
```

## 步骤4 已执行
```bash
cd /workspace/xujia-batch/item03/exercise
python3 lab.py render
```
```text
rendered 0
rendered 72
rendered 144
rendered 216
rendered 288
{"frames": 312, "size": [640, 360], "fps": 24, "duration_seconds": 13, "shutter_degrees": 180, "samples_per_frame": 4, "renderer": "original CPU perspective polygons, not Three.js/WebGL/onetake", "wall_seconds": 13.833}

exit_code=0
elapsed_wall_seconds=14.025
```

## 步骤5 已执行
```bash
cd /workspace/xujia-batch/item03/exercise
python3 lab.py encode
```
```text
{"video_frames": 312, "video_duration": "13.000000", "audio_duration": "13.000000", "decoded_without_errors": true, "sampled_unique_frame_hashes": 6, "sha256_mp4": "6810b76f63cf02bfda7b474ef0112f95555ca029807ca5325ac7b67ec03d18a2", "command": ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-framerate", "24", "-i", "/workspace/xujia-batch/item03/exercise/out/frames/%05d.png", "-i", "/workspace/xujia-batch/item03/exercise/out/score.wav", "-c:v", "libx264", "-preset", "fast", "-crf", "22", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", "/workspace/xujia-batch/item03/exercise/out/study.mp4"]}

exit_code=0
elapsed_wall_seconds=1.277
```

## 待验证
Opus 5.5/NotionAI输入参考视频→自动理解→索要素材→生成代码的作者工作流：没有调用，待验证。
Blender人物建模、Three.js/WebGL真实运行、上游onetake渲染、4K60性能和真人观感：均未实测。
作者原始工程、素材、提示及渲染日志未公开，不能声称独立复现或效果一致。
Chrome已按用户要求仅清理本任务残留，独立profile、--no-sandbox --disable-gpu、更长105s超时；结果另见qa/clean-chrome.stderr。未停止其他助手浏览器。

## 补充媒体验证 已执行
使用FFmpeg对成片0、1.6、3.5、8.5、11.2、12.95秒分别执行：
```bash
ffmpeg -hide_banner -loglevel error -ss <秒> -i exercise/out/study.mp4 -frames:v 1 -y qa/study-XX.png
```
随后Python/NumPy在y=80..309像素区域对G>95且B>100像素取包围盒，排除标题与时钟标签，得到：
```json
[{"t": 0, "bbox": [119, 155, 138, 206]}, {"t": 1.6, "bbox": [247, 106, 393, 249]}, {"t": 3.5, "bbox": [247, 106, 393, 249]}, {"t": 8.5, "bbox": [278, 80, 473, 309]}, {"t": 11.2, "bbox": [248, 108, 391, 251]}, {"t": 12.95, "bbox": [248, 108, 391, 251]}]
```
不同包围盒数=4，断言≥3通过。已实际查看qa/study-contact.png：厚片与符号可辨，正侧面/缩放改变，无界面文字遮盖主体；未试听或做人类审美认证。

## 干净Chrome重试 已执行但失败
```bash
timeout -k 5s 105s /usr/bin/google-chrome --headless=new --no-sandbox --disable-gpu --disable-dev-shm-usage --no-first-run --no-default-browser-check --disable-extensions --user-data-dir=/workspace/xujia-batch/item03/qa/clean-profile --print-to-pdf=/workspace/xujia-batch/item02/guide.pdf --no-pdf-header-footer file:///workspace/xujia-batch/item02/guide.html
```
exit_code=124，105秒，无guide.pdf。仅清理本任务专属profile，不停止同机其他助手的Chrome。stderr见qa/clean-chrome.stderr；DBus/UPower警告不等于已确诊根因。第2项PDF与ZIP未能补更新；第3项未重复启动同一已失败打印条件，PDF状态未渲染，无逐页检查。
