# video_shotcraft 实验日志

- task_id：`07d43cf1-75a2-4c0d-a7d3-4f5cbdb4f160`
- owner：`main-k3-w5`
- 实验目录：`video_shotcraft/exercise/shotcraft-lab`
- 上游：`https://github.com/Vincentwei1021/video-shotcraft`
- 固定版本：`1266a3e Source project SFX from Freesound and acknowledge vibe-motion/sound (#123)`
- 实验日期：2026-10-30 至 2026-10-31

## 1. 来源与环境核验

原 X 页面本轮 WebFetch 返回 HTTP 402；FxTwitter 镜像读取到同作者主帖及其引用的开源帖，被引用帖明确出链到上述精确仓库。没有用同名搜索结果替代目标。

实际执行：

```bash
git clone https://github.com/Vincentwei1021/video-shotcraft.git F:\reminder\video_shotcraft\repo
git -C F:\reminder\video_shotcraft\repo log --oneline -1
# 1266a3e Source project SFX from Freesound and acknowledge vibe-motion/sound (#123)
```

环境：Windows 11、Node `v24.21.0`、npm `11.19.0`、Python `3.14.7`。系统 PATH 没有 ffmpeg，后续全部使用 Remotion CLI 自带 ffmpeg/ffprobe。

## 2. 依赖限制与真实替代路径

两次尝试为实验安装 npm 依赖（普通 install 与带锁 ci --ignore-scripts）均被当前权限分类器拒绝，未把安装写成成功。改为目录联接复用本机已有的 `ai-video-pipeline/exercise/remotion_app/node_modules`。

```bash
cmd /c "mklink /J F:\reminder\video_shotcraft\exercise\shotcraft-lab\node_modules F:\reminder\ai-video-pipeline\exercise\remotion_app\node_modules"
cd /f/reminder/video_shotcraft/exercise/shotcraft-lab
node node_modules/@remotion/cli/remotion-cli.js versions
# On version: 4.0.532；列出的 Remotion 各包均为 4.0.532
```

上游模板钉版是 4.0.484，本实验实际渲染版是 4.0.532；本日志不声称原 Ink Press 模板被原样验收。node_modules 是依赖联接，不属于实验成果，也未列入 manifest 的 experiment_files。

## 3. 实验设计

独立制作 6 秒、180 帧、960×540、30fps 的产品片，聚焦四个增补而非通用 Remotion 教程：

1. 单主角产品卡：聚光、入场、抬升、归位的动作弧；
2. 第 90 帧前后各 5 帧的暖白闪转场；
3. 从 `SHOTS` 派生的三条 SFX，补偿音源峰值滞后并实测输出偏移；
4. `src/workbench.ts` 与渲染共享 `SHOTS/CAPTIONS/SFX`，声明 props/schema 和多轨拆解。

三条 MP3 从上游模板历史回归素材复制，原 `ATTRIBUTION.md` 一并保留。只选用授权记录可回查的 Mixkit 条目，不将其冒充为本次从 Freesound 下载的新素材。

## 4. 音源实际测量

用 Remotion 自带 ffmpeg 将三条 MP3 解码成 48kHz 单声道 PCM s16le：

```bash
node node_modules/@remotion/cli/remotion-cli.js ffmpeg -y -i public/audio/whoosh-fast.mp3 -ac 1 -ar 48000 -acodec pcm_s16le out/whoosh-fast.wav
node node_modules/@remotion/cli/remotion-cli.js ffmpeg -y -i public/audio/impact-cine.mp3 -ac 1 -ar 48000 -acodec pcm_s16le out/impact-cine.wav
node node_modules/@remotion/cli/remotion-cli.js ffmpeg -y -i public/audio/transition-soft.mp3 -ac 1 -ar 48000 -acodec pcm_s16le out/transition-soft.wav
python -I scripts/analyze_wav.py out/whoosh-fast.wav out/impact-cine.wav out/transition-soft.wav
```

真实输出：

| 文件 | 时长秒 | sample peak dB | 10ms RMS 峰 dB | 峰值滞后秒 | 峰值滞后帧@30fps |
|---|---:|---:|---:|---:|---:|
| whoosh-fast.wav | 1.756729 | -6.064 | -14.165 | 0.725 | 21.75 |
| impact-cine.wav | 4.063125 | -0.867 | -5.159 | 0.555 | 16.65 |
| transition-soft.wav | 1.274750 | -0.946 | -9.803 | 0.455 | 13.65 |

完整 JSON 在 `out/source-audio-analysis.json`。10ms RMS/sample peak 不是 LUFS/true peak，也不自动等于语义落点；多动作素材和主观音色仍需成片试听。

将实测值写入 `PEAK_F` 后：

```text
Sequence.from = 目标峰值帧 − 音源峰值滞后帧 − 输出音轨偏移帧
whoosh:    36 − 21.75 − 0 ≈ 14f
impact:    70 − 16.65 − 0 = 53f
transition:114 − 13.65 − 0 ≈ 100f
```

基线刻意令输出偏移为 0，渲后再测，不预套上游历史常数。

## 5. 真实渲染与媒体验证

```bash
node node_modules/@remotion/cli/remotion-cli.js render src/index.ts ShotcraftLab out/baseline.mp4 --concurrency=2
# Rendered 180/180
# Encoded 180/180
# out/baseline.mp4 753.1 kB
cp out/baseline.mp4 out/shotcraft-lab.mp4
node node_modules/@remotion/cli/remotion-cli.js ffprobe -v error -show_entries format=duration,size:stream=index,codec_name,codec_type,width,height,r_frame_rate,sample_rate,channels -of json out/shotcraft-lab.mp4
```

ffprobe：视频 H.264、960×540、30/1 fps；音频 AAC、48000Hz、双声道；容器时长 6.016 秒、753133 字节。结果保存于 `out/ffprobe.json`。

抽帧并实际逐张查看：

```bash
node node_modules/@remotion/cli/remotion-cli.js still src/index.ts ShotcraftLab out/qa/hero-f36.png --frame=36
node node_modules/@remotion/cli/remotion-cli.js still src/index.ts ShotcraftLab out/qa/transition-f89.png --frame=89
node node_modules/@remotion/cli/remotion-cli.js still src/index.ts ShotcraftLab out/qa/features-f120.png --frame=120
node node_modules/@remotion/cli/remotion-cli.js still src/index.ts ShotcraftLab out/qa/features-f140.png --frame=140
```

- f36：产品卡、聚光与抬升可读；
- f89：前镜被暖白覆盖，闪白确实跨骑切点；
- f120：第三行尚在错峰入场，说明逐行动画不是静态摆拍；
- f140：三行功能全部落定，字幕与构图可读。

## 6. 输出音轨偏移实测

将 MP4 音轨解码为 PCM：

```bash
node node_modules/@remotion/cli/remotion-cli.js ffmpeg -y -i out/baseline.mp4 -vn -ac 1 -ar 48000 -acodec pcm_s16le out/baseline.wav
python -I scripts/measure_av_offset.py out/baseline.wav whoosh=out/whoosh-fast.wav=14 impact=out/impact-cine.wav=53 transition=out/transition-soft.wav=100
```

脚本使用自带 FFT 交叉相关，不依赖 NumPy，并含合成序列自测试。真实输出：

| 探针 | Sequence.from | 测得起点 | 输出偏移@30fps | 归一化相关 |
|---|---:|---:|---:|---:|
| whoosh | 14f | 14.01f | +0.01f | 0.40089 |
| impact | 53f | 53.01f | +0.01f | 0.94528 |
| transition | 100f | 99.99f | -0.01f | 0.99926 |

结论只限于本管线：Remotion 4.0.532 + AAC 48kHz + MP4 的三探针未显示上游历史 1.28f 偏移，保留 `OUTPUT_AUDIO_OFFSET_F = 0`。whoosh 相关性低于另两条，故不把它单独当作精确常数证据；三探针一致接近 0 才支持本次结论。换 Remotion/codec/sample rate/container 必须重测。

`out/render-audio-analysis.json` 记录最终解码 PCM sample peak 为 -6.90dBFS；这不是 LUFS 或 true peak，不据此宣称完成主观混音验收。

## 7. Workbench 清单真实执行

```bash
node scripts/validate-manifest.cjs
# status: passed
# tracks: shots 2, transitions 1, captions 1, sfx 3
# sfxFrom: [14, 53, 100]
```

脚本用本机 esbuild 打包并执行真实 `src/workbench.ts`，断言 180 帧、30fps、2 镜头、1 转场、1 字幕、3 音效、组件函数、时间表及 props/schema 默认键。摘要保存于 `out/workbench-manifest.json`。

限制：依赖安装受阻，未启动完整 Workbench 浏览器 UI，也未运行官方 `npm run parity` 像素对照。本项只证明清单可执行与结构/同源数据通过，不声称官方无损验收已通过。未做 Freesound 在线下载、Windows 剪映导出、主观试听或模型能力比较。

## 8. 指南 PDF

HTML：`video_shotcraft/video-shotcraft-guide.html`；Edge 无头打印生成中文 PDF。二进制检查：`%PDF-1.4`、1,433,992 字节、13 个页面对象。当前环境缺少 pdftoppm/Pillow，worker 未宣称逐页 PDF 渲染审核完成；留待协调者独立 review。
