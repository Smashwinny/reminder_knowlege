# Remotion 修订与重放真实实验日志

日期：2026-11-11（Asia/Shanghai）  
执行者：本地 claude_kimi 学习 worker。本文是执行记录与自检，不是独立审核通过。

## 范围与输入

目的：只修订 `review.md` 的 R1/R3/R4 与 HTML 体积问题，验证干净目录复现，保留原成果。

- 输入：`D:/agenttry/reminder-learning-20261110/cloud-review-remotion/`。
- 所有新文件：`D:/agenttry/reminder-learning-20261110/remotion-refined/`。
- 原 exercise ZIP：35,616 bytes，SHA256 `e9d9a9acfe21edfcc23d66c13f19af56d7af132d18b9c69f9b9e920ebbd9c3bb`。
- 原 MP4：1,271,452 bytes，SHA256 `94bb30211c135902f228081b43f276b6213a9cadd219aaa7d9b70dc206160e1d`；未修改、未重编码、未替换。
- 未操作共享 vault、Git、网站、数据库、凭据或日程；未使用子 agent、浏览器/CDP/Playwright 桌面自动化；未全局安装或修改安全设置。

先读原 `src/index.tsx`：4 个场景各 90 帧，总计 360 帧；标题 spring，三卡 `frame-i*7-8`，进度条 0–359 映射 0–100，Composition 为 1920×1080、30fps。修订后该源文件与原版 `cmp` 一致。

## 解包前置检查

目的：验证 ZIP 路径，避免穿越、覆盖和链接。

操作：用本次 `work/safe_extract.py` 检查绝对路径、`..`、反斜杠、盘符/ADS、符号链接、加密、重复目标、20MB 解压预算，并以独占创建写入新目录。

真实结果：首次运行脚本因反斜杠字符串语法错误退出 1，未解包；修正后成功。原 ZIP 为 6 个文件、144,715 解压 bytes，无 `node_modules`，结果 PASS。

验证：`evidence/zip-validation.json` 保存逐条名称、大小和 SHA256；目标为全新的 `repro/`。该脚本失败没有被写成项目复现成功。

## 六步主实验（本次隔离重放）

### 1. 准备目录并探测真实环境

**目的**：区分可替换项目根与当前实测路径，提前创建所有输出目录。

**操作**：

```bash
mkdir -p repro/research repro/frames work/tmp
uname -a
node --version
npm --version
python --version
command -v ffmpeg
command -v ffprobe
command -v fc-list
```

另用 PowerShell 只读查询 Chrome 文件版本和已安装字体，没有启动浏览器页面。

**真实结果**：Windows/MSYS (`MINGW64_NT-10.0-26200`)；Node v24.21.0、npm 11.19.0、Python 3.14.7、Chrome 156.0.8078.80。`ffmpeg`、`ffprobe`、`fc-list` 三个探测均退出 1；字体查询有 Noto Sans SC 和 Microsoft YaHei UI。未宣称 Linux 已测。

**验证**：`evidence/01-environment.txt` 逐命令保留退出码。README 的 `/usr/bin/google-chrome` 明确只是 Linux 示例，本次实际 `CHROME_BIN` 是 `C:\Program Files\Google\Chrome\Application\chrome.exe`。

### 2. 锁文件干净安装

**目的**：补上原评审指出的 `npm ci` 实跑证据，不执行依赖脚本。

**操作**：

```bash
cd remotion-refined/repro/exercise
test ! -e node_modules
npm ci --ignore-scripts --no-audit --no-fund
```

**真实结果**：前置 `test` 退出 0；新增 245 包，约 15 秒，npm 退出 0。按参数跳过 audit/funding，所以不写成“完成安全审计”。没有批准或补跑 esbuild 等安装脚本。

**验证**：`evidence/02-npm-ci.txt` 含原始输出和 `exit=0`。锁文件未改，`node_modules` 仅留在复现目录，最终 ZIP 使用 allowlist 排除它。

### 3. 独立 TypeScript 类型检查

**目的**：把类型检查与后续渲染编译分开。

**操作**：

```bash
cd remotion-refined/repro/exercise
npx tsc --noEmit
```

**真实结果**：无诊断，退出 0。

**验证**：`evidence/03-typecheck.txt` 明确包含 `exit=0`；不是用空日志单独推断成功。

### 4. 官方 Remotion CLI 渲染独立重放

**目的**：验证实际 360 帧渲染，同时保留原 MP4。

**操作与真实结果**：

1. 首试：

   ```bash
   npx remotion render src/index.tsx CaptionLab ../caption-lab-replay.mp4 --concurrency=2 --browser-executable="$CHROME_BIN"
   ```

   到 63/360 后出现 `Error: write EOF`，退出 1，没有生成 MP4。原始日志保存为 `evidence/04-render-attempt1.txt`。

2. 只做资源排障，将并发改为 1：

   ```bash
   npx remotion render src/index.tsx CaptionLab ../caption-lab-replay.mp4 --concurrency=1 --browser-executable="$CHROME_BIN"
   ```

   仍在 63/360 退出 1。底层日志明确：Remotion 自带 FFmpeg 无法创建 `F:\UserTemp\Windows\react-motion-render...\pre-encode.mp4`，`Permission denied`。日志为 `evidence/04-render-attempt2.txt`。

3. 不改安全设置，仅设置本进程临时目录后重试：

   ```bash
   export TMP='D:\agenttry\reminder-learning-20261110\remotion-refined\work\tmp'
   export TEMP="$TMP"
   npx remotion render src/index.tsx CaptionLab ../caption-lab-replay.mp4 --concurrency=2 --browser-executable="$CHROME_BIN"
   ```

   这次退出 0，生成 `repro/caption-lab-replay.mp4`，1,219,770 bytes，SHA256 `954072cae49ea5d5537395fa434461581d193468929b9e2973e6a8c21dc6f8ef`。完整日志为 `evidence/04-render.txt`。

**验证**：检查退出码、文件存在、字节数与 SHA256。第三次成功只证明这次重放，不回溯改写前两次失败，也不替代原成果。Remotion 使用官方 CLI 的离线无头渲染流程，没有操作用户浏览器页面。

### 5. 容器验证与四个中点静帧

**目的**：分别验证硬规格和可见画面，明确本机缺少 ffprobe 的证据边界。

**操作**：

```bash
cd remotion-refined/repro/exercise
python verify.py ../caption-lab-replay.mp4
# 在TMP/TEMP仍指向隔离目录、CHROME_BIN不变时：
for item in 01:45 02:135 03:225 04:315; do
  n=${item%%:*}; f=${item##*:}
  npx remotion still src/index.tsx CaptionLab "../frames/replay-$n.png" --frame="$f" --browser-executable="$CHROME_BIN"
done
```

`verify.py` 优先使用 ffprobe；没有时使用标准库读取真实 ISO-BMFF `moov/trak/mdia/mdhd/stsd/stsz`。它不是 mock，也不解码全帧。

**真实结果**：容器检查退出 0：1 个视频、0 个音频、avc1、1920×1080、30.0fps、12.0 秒、360 样本。四次 `remotion still` 均退出 0，输出 1920×1080 PNG。逐张查看 45/135/225/315：中文、标题、三卡和字幕完整，未见方框、裁切或重叠。

**验证**：`evidence/05-verify.txt` 有 `exit=0` 和范围声明；`evidence/05-stills.txt` 有四条命令各自 `exit=0`。静帧直接来自组件 CLI，**不是从 MP4 抽帧**；未证明全 360 帧、连续播放或观众阅读效果。

### 6. 图片压缩、HTML 与源码包

**目的**：HTML 小于 200KB，保留 12 问/12 SVG/4 用途/一个 6 步实验、可选文字和许可证；不生成 PDF。

**操作**：

- PowerShell `.ps1` 转换首次被执行策略阻止，未生成 JPEG；没有使用 Bypass 或修改策略。失败保存在 `evidence/image-compression-powershell-failure.txt`。
- 创建 `work/image-venv`，从官方 PyPI 安装 Pillow 13.0.0；安装记录为 `evidence/image-tool-install.txt`。只在本目录，未全局安装。
- 将原四张 1920×1080 PNG 用 LANCZOS 缩为 720×405，JPEG quality=70、optimize=True；原 PNG 不动。
- 修订原构建脚本的隔离副本：统一 Microsoft YaHei 系统字体，不嵌字体；命令取消任意字符断行；补术语、可替换路径、目录创建、退出码和真实结果。
- 用 7 文件 allowlist 打包 README、package/lock、tsconfig、verify、LICENSE 和 `src/index.tsx`。

**真实结果**：

| 图片 | 原PNG bytes | JPEG bytes |
|---|---:|---:|
| scene-01 | 368,732 | 20,218 |
| scene-02 | 353,159 | 19,992 |
| scene-03 | 340,501 | 18,733 |
| scene-04 | 385,404 | 21,583 |
| 合计 | 1,447,796 | 80,526 |

四张 JPEG 已逐张查看，A4 半栏所需正文和字幕可辨。`guide.html` 当前为 134,901 bytes，4 个 JPEG data URL、12 个内联 SVG，无脚本、无外链图片、无 `@font-face`。

首次最终 ZIP 误把绝对路径拼入条目，安全验证因 `exercise/D:/...` 拒绝；错误包保留为 `evidence/exercise-invalid-paths.zip`。修正后 `exercise.zip` 为 41,363 bytes，SHA256 `7b509e1106f49e5f76671327bf43af18a46f8e2f48829a323b49291cf1f786c7`，7 个相对路径文件，CRC 和安全验证 PASS。

**验证**：`evidence/image-compression.jsonl`、`evidence/final-zip-validation.json`、`evidence/06-package.json`。ZIP 不含 `node_modules`，许可证快照保留。HTML 结构由独立脚本重新计数，结果记入 `evidence/final-artifact-inspection.json`。

最终 ZIP 安全解包到另一干净副本后，又执行一次 `npm ci --ignore-scripts --no-audit --no-fund`：新增 245 包、约 9 秒、退出 0；随后 `npx tsc --noEmit` 退出 0。见 `evidence/final-zip-install-typecheck.txt`，因此安装与类型检查证据直接对应最终归档，而非只对应中间目录。

## 原实验记录与本次记录的关系

原云端 worker 已有真实 `npm install`、类型检查、CLI 渲染、ffprobe、ffmpeg 抽帧及 WeasyPrint PDF 记录，原件仍在源目录。本次没有重跑或篡改这些历史步骤，也没有把旧 PDF 当作 Edge 输出。本次新增的是干净目录 `npm ci`、独立退出码、本地重放、容器回退与 CLI 静帧证据。

**本次未生成 PDF。** root 需用 Edge 实际打开最终 `guide.html`、打印 A4、逐页目检，并确认命令复制、字体、SVG、四图和分页。最终独立审核须由另一方执行；本 worker 不自称通过。

## 仍未验证

外部模型一句话导演、原作者制作过程/视频归属、宣传 API/流量、真实观众阅读速度、全 360 帧连续播放、跨机器逐像素一致、新推荐 API 迁移、Linux 复现、最终 Edge 打印效果。
