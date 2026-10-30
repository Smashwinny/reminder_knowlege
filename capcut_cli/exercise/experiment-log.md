# capcut-cli 动手实验日志（task fc6b3e7b-4b5c-44d1-b3f6-ea15458366ba）

实验日期：2026-10-27
环境：Windows 11，Node v24.21.0，capcut-cli v0.31.1（源码构建，master @ f3d6c75）
说明：本机未安装 CapCut 应用与 ffmpeg/ffprobe；实验验证"无剪映环境下 CLI 建草稿 + 编辑 + 校验"链路，
真实打开剪映人工核验一步如实标注为未验证。

## 步骤与真实输出

### 步骤 1：源码构建

```
git clone --depth 1 https://github.com/renezander030/capcut-cli repo   # HEAD f3d6c75
npm install && npm run build   # tsc 编译，版本 0.31.1
node dist/index.js --version   # → 0.31.1 ✅
```
（bin 入口是 dist/index.js，不是 dist/cli.js——第一个小坑）

### 步骤 2：零素材准备（Python 标准库自造测试材料）

- `clip.png`：320x240 橙蓝条纹 PNG（905 字节，手写 zlib 编码器生成）
- `bgm.wav`：2 秒 44.1kHz 440Hz 正弦波单声道 WAV

### 步骤 3：一条命令建草稿（quickstart）

```
node dist/index.js quickstart demo1 --video clip.png --audio bgm.wav --ratio 16:9 --drafts ./drafts
```
✅ 真实输出四步全过：
- create：草稿创建并**注册进剪映工程索引**，画布 1920x1080
- add-video：图片无时长可读（无 ffprobe）→ 明示用 5 秒占位，素材登记入 draft_materials
- add-audio：WAV 时长 5.00s 识别成功
- lint：0 错误 0 警告

### 步骤 4：草稿结构与备份机制（ls drafts/demo1）

```
draft_content.json / draft_info.json / draft_meta_info.json
+ 同名的 .bak 三个备份文件 + assets/
```
→ 每次写都留 .bak，`capcut restore` 可撤销——原子写+备份是默认行为不是选项。

### 步骤 5：轨道查询与文本编辑

```
tracks → #0 video 5.00s / #1 audio 5.00s
add-text drafts/demo1 0 2 "hello capcut" --color "#FF2E88" --font-size 15
→ {"ok":true,"segment_id":"f29a6021-...","start_us":0,"duration_us":2000000}
tracks → #2 text 2.00s ✅ 新增独立文字轨道
```

### 步骤 6：dry-run 与版本/lint 校验

```
trim ... --dry-run → {"dryRun":true,...}   ✅ 预览不写盘，.bak 不动
version drafts/demo1 → 模板 app_version 6.5.0，schema 特性检测齐全，支持范围 6.x–9.x
lint drafts/demo1 → {"ok":true, errors:0, warnings:0}
```

## 结论

- v0.31.1 源码构建可跑通；Node≥18 零运行时依赖属实（仅开发依赖）；
- 无 CapCut、无 ffmpeg 也能完整建草稿并编辑：图片素材用 5 秒占位并明示，音频时长正常识别；
- 写操作默认原子写 + .bak 备份 + lint 门禁 + dry-run 预览，工程纪律完整；
- **未验证项**（如实记录）：真实打开 CapCut 人工核验轨道可编辑性；新版本多时间线（8.7 mirror）sync-timelines 路径；caption（需 Whisper）与 render（需 ffmpeg）命令。

## 产物

- `exercise/clip.png`、`exercise/bgm.wav` — 自造测试素材
- `exercise/drafts/demo1/` — 生成的真实剪映草稿（JSON + .bak）
- `exercise/experiment-log.md`（本文件）
