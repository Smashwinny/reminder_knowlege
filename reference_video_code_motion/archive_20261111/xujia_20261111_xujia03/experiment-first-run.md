# 第3项真实实验日志

2026-11-11T01:20:08.384303+08:00（Asia/Shanghai）
教学代码为原创CPU三维投影/音频实验，不是作者源码或Opus输出，未执行onetake渲染脚本。

## 步骤1 已执行
```bash
cd /workspace/xujia-batch/item03/exercise
python3 lab.py source_audit
```
```text
{"source_tokens": ["window.__seek", "window.__ready", "SRGB_TO_LIN", "__motion", "--workers", "--gpu"], "tokens_verified": 6, "sha": "abb6d17279cdc749e27e99aa534a062d8fd01ced", "license": "PolyForm Noncommercial 1.0.0", "upstream_renderer_executed": false, "blender_executed": false, "paid_model_calls": 0}

exit_code=0
elapsed_wall_seconds=0.145
```

## 步骤2 已执行
```bash
cd /workspace/xujia-batch/item03/exercise
python3 lab.py timeline
```
```text
{"out_of_order_seek_identical": true, "max_boundary_delta": 1.6874999998917062e-05, "linear_light_black_white_average": 188, "gamma_space_average": 128, "frames": 312, "samples_audio": 624000, "duration_ratio": 4.166666666666667, "note": "continuous parameters only; not proof of subjective shot continuity or GPU rendering"}

exit_code=0
elapsed_wall_seconds=0.185
```

## 步骤3 已执行
```bash
cd /workspace/xujia-batch/item03/exercise
python3 lab.py audio
```
```text
{"samples": 624000, "duration_seconds": 13.0, "peak": 0.4526826221393474, "clipped_samples": 0, "event_marks": [{"event": "enter", "sample": 19200, "time": 0.4, "error": 0.0}, {"event": "land", "sample": 76800, "time": 1.6, "error": 0.0}, {"event": "orbit", "sample": 168000, "time": 3.5, "error": 0.0}, {"event": "reframe", "sample": 408000, "time": 8.5, "error": 0.0}, {"event": "settle", "sample": 537600, "time": 11.2, "error": 0.0}]}

exit_code=0
elapsed_wall_seconds=0.255
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
{"frames": 312, "size": [640, 360], "fps": 24, "duration_seconds": 13, "shutter_degrees": 180, "samples_per_frame": 4, "renderer": "original CPU perspective polygons, not Three.js/WebGL/onetake", "wall_seconds": 12.808}

exit_code=0
elapsed_wall_seconds=12.978
```

## 步骤5 已执行
```bash
cd /workspace/xujia-batch/item03/exercise
python3 lab.py encode
```
```text
{"video_frames": 312, "video_duration": "13.000000", "audio_duration": "13.000000", "decoded_without_errors": true, "sampled_unique_frame_hashes": 6, "sha256_mp4": "6810b76f63cf02bfda7b474ef0112f95555ca029807ca5325ac7b67ec03d18a2", "command": ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-framerate", "24", "-i", "/workspace/xujia-batch/item03/exercise/out/frames/%05d.png", "-i", "/workspace/xujia-batch/item03/exercise/out/score.wav", "-c:v", "libx264", "-preset", "fast", "-crf", "22", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", "/workspace/xujia-batch/item03/exercise/out/study.mp4"]}

exit_code=0
elapsed_wall_seconds=0.924
```

## 待验证
Opus 5.5/NotionAI输入参考视频→自动理解→索要素材→生成代码的作者工作流：没有调用，待验证。
Blender人物建模、Three.js/WebGL真实运行、上游onetake渲染、4K60性能和真人观感：均未实测。
作者原始工程、素材、提示及渲染日志未公开，不能声称独立复现或效果一致。
Chrome已按用户要求仅清理本任务残留，独立profile、--no-sandbox --disable-gpu、更长105s超时；结果另见qa/clean-chrome.stderr。未停止其他助手浏览器。