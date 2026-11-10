# 真实实验日志

2026-11-11 Asia/Shanghai。自绘几何人偶与数值合成不是Seedance生成。账号/付费API/真实提示词/原视频完整观看/真人素材均未使用或验证；不购买、不登录、不发帖。


## 1. 固定变量表
目的：定义每条黑边比例、压边和背景平移，另存自拟提示。
```bash
cd /workspace/jingjing-duonaonao-batch2-20261111/extra01-frame-break
python3 exercise/lab.py init
```
实际exit0，stdout/stderr原文：
```text
12 deterministic cases: 3 per-bar ratios x 2 overlap states x 2 background pan levels; prompt strength NOT simulated
```
验证：variables.csv有12例；prompt_strength明确not simulated。

## 2. 生成受控帧
目的：自绘原创人偶，生成12个静帧与144个左右对照帧。
```bash
cd /workspace/jingjing-duonaonao-batch2-20261111/extra01-frame-break
python3 exercise/lab.py render
```
实际exit0，stdout/stderr原文：
```text
/workspace/jingjing-duonaonao-batch2-20261111/extra01-frame-break/exercise/lab.py:23: DeprecationWarning: Image.Image.getdata is deprecated and will be removed in Pillow 14 (2027-10-15). Use get_flattened_data instead.
  intended=sum(1 for v in cross.getdata() if v)
/workspace/jingjing-duonaonao-batch2-20261111/extra01-frame-break/exercise/lab.py:27: DeprecationWarning: Image.Image.getdata is deprecated and will be removed in Pillow 14 (2027-10-15). Use get_flattened_data instead.
  visible=sum(1 for v in ImageChops.multiply(subject.getchannel('A'),bar_mask).getdata() if v)
rendered 12 PNG cases + 144 comparison frames (960x300); all character art self-drawn; no model inference
```
验证：measurements.json保留逐例交集像素；尺寸960×300。

## 3. 真实编码视频
目的：FFmpeg把PNG序列编码为24fps H.264。
```bash
cd /workspace/jingjing-duonaonao-batch2-20261111/extra01-frame-break
python3 exercise/lab.py encode
```
实际exit0，stdout/stderr原文：
```text
ffmpeg -y -hide_banner -loglevel error -framerate 24 -i /workspace/jingjing-duonaonao-batch2-20261111/extra01-frame-break/exercise/out/frames/%03d.png -c:v libx264 -pix_fmt yuv420p -crf 23 /workspace/jingjing-duonaonao-batch2-20261111/extra01-frame-break/frame-break-demo.mp4
exit=0; encoded frame-break-demo.mp4 (not Seedance output)
```
验证：frame-break-demo.mp4真实存在；完整命令在stdout。

## 4. 验证几何及解码
目的：检查裁剪零越界、前景非零越界、黑边角像素和FFprobe帧数。
```bash
cd /workspace/jingjing-duonaonao-batch2-20261111/extra01-frame-break
python3 exercise/lab.py validate
```
实际exit0，stdout/stderr原文：
```text
/workspace/jingjing-duonaonao-batch2-20261111/extra01-frame-break/exercise/lab.py:23: DeprecationWarning: Image.Image.getdata is deprecated and will be removed in Pillow 14 (2027-10-15). Use get_flattened_data instead.
  intended=sum(1 for v in cross.getdata() if v)
/workspace/jingjing-duonaonao-batch2-20261111/extra01-frame-break/exercise/lab.py:27: DeprecationWarning: Image.Image.getdata is deprecated and will be removed in Pillow 14 (2027-10-15). Use get_flattened_data instead.
  visible=sum(1 for v in ImageChops.multiply(subject.getchannel('A'),bar_mask).getdata() if v)
{"cases": 12, "overlap_invariants": "PASS", "bar_px": [27, 49, 68], "frames": 144, "fps": 24, "duration_s": 6}
```
验证：validation.json中12例通过，144帧、6秒；作者自检非独立审核。

## 5. 固定产物指纹
目的：保存代码、输入、测量和视频的SHA256。
```bash
cd /workspace/jingjing-duonaonao-batch2-20261111/extra01-frame-break
python3 exercise/lab.py audit
```
实际exit0，stdout/stderr原文：
```text
5 SHA256 fingerprints saved; model generation/account/credits NOT used; prompt-strength effects await real testing
```
验证：manifest.json列5文件；模型生成与指令强度不在实测范围。


抽样检查：ffmpeg -i frame-break-demo.mp4 -vf "select=eq(n\,0)+eq(n\,48)+eq(n\,96),tile=1x3" -frames:v 1 demo-contact.png，实际成功并目视三比例左右对照；完整视频另存、不嵌HTML。
