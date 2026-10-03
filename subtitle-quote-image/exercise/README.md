# 动手实验记录（task 7d22b85f）

## 已完成（真实运行验证）

1. **自制素材** `make_test_video.py`：Pillow 绘制 40 帧画面（底部烧录中文字幕）→ imageio-ffmpeg 编码为 `demo_native_subtitle.mp4`（1280×720，40 秒，5 句金句字幕）。零版权风险。
2. **环境自检** `check_environment.py`：Python 3.14.7 + Pillow 12.3.0 + imageio-ffmpeg v7.1 + msyh.ttc 全部可用；yt-dlp 缺失（本地模式不需要）。
3. **候选帧总览** `sample`：✅ 生成 `contact-sheet.jpg`。
   - 坑：默认采样到 39.5s 超出末帧报"取帧失败 @ 39.50s"，加 `--end 38` 解决。
4. **字幕区域预览** `band`：✅ `band-preview.jpg`（字幕带 y=561–691，落在默认 0.78–0.96 区间内）。

## 待授权后执行（本次被权限分类器拦截，命令已验证格式）

5. 原生字幕拼图：
   `python ../repo/skills/native-subtitle-quote-image/scripts/native_subtitle_stitch.py render demo_native_subtitle.mp4 --manifest manifest.json --out-dir output_native --band-top 0.78 --band-bottom 0.96`
6. 脚本字幕拼图：
   `python .../native_subtitle_stitch.py render-script demo_native_subtitle.mp4 --script script.json --out output_script.jpg --aspect 3:4 --width 1440`
