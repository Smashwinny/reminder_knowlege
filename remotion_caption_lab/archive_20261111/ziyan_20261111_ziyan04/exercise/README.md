# 第4项：静音字幕主轨 Remotion 重放练习

这是 worker 直接编写的 React/Remotion 组件，不是原帖模型或付费 API 的产物。原实验 MP4 保留在源目录；本练习输出 `caption-lab-replay.mp4`，不覆盖原作。

- 固定依赖：Remotion / CLI 4.0.542，React 19.1.0，TypeScript 5.9.3。
- 画面：4 个 `Sequence`，每段 90 帧；总计 360 帧、30fps、1920×1080、12 秒、零音轨。
- 许可：`LICENSE-Remotion.md` 是固定来源的 Remotion 许可快照，不是对所有组织免费或对本例代码另作授权的法律结论。
- ZIP 只含源码、锁文件、验证脚本、文档与许可；不要加入 `node_modules`。

## 已实测范围

本次在 Windows/MSYS 新空目录执行：Node v24.21.0、npm 11.19.0、Python 3.14.7、Chrome 156.0.8078.80。`npm ci --ignore-scripts --no-audit --no-fund` 和 `npx tsc --noEmit` 均退出 0。Remotion 渲染前两次因临时目录问题退出 1，第三次将 `TMP/TEMP` 指向可写隔离目录后退出 0。详见交付的 `experiment-log.md`。

下面的主配方使用 Bash。`/usr/bin/google-chrome` 是 **Linux 示例**，须替换为本机实际 Chrome；本次没有据此宣称 Linux 已测。Windows/MSYS 的临时目录命令已实测。`ffmpeg/ffprobe` 不是渲染前置条件，但有 ffprobe 时可获得更完整的流探测；没有时 `verify.py` 只读 MP4 容器，不声称解码或连续播放。

## 一个六步复现实验

### 1. 准备干净目录、目录结构和环境

目的：避免写死 worker 路径，并提前建立日志、静帧和临时目录。

```bash
export PROJECT_ROOT="$HOME/remotion-caption-lab"
export EXERCISE_ZIP=/path/to/exercise.zip  # 改成实际ZIP路径
mkdir -p "$PROJECT_ROOT"
cd "$PROJECT_ROOT"
unzip -t "$EXERCISE_ZIP"
unzip "$EXERCISE_ZIP"
mkdir -p research frames work/tmp
node --version
npm --version
export PYTHON=python3                 # 本次Windows/MSYS：export PYTHON=python
"$PYTHON" --version
export CHROME_BIN=/usr/bin/google-chrome  # Linux示例，按本机替换
# 本次Windows/MSYS实际值：
# export CHROME_BIN='C:\Program Files\Google\Chrome\Application\chrome.exe'
```

验证：`unzip -t` 无错误，`exercise/src/index.tsx`、`research/`、`frames/`、`work/tmp/` 存在。交付 ZIP 另已用脚本拒绝绝对路径、`..`、盘符/ADS、符号链接、重复目标和覆盖已有文件；不要解压来源不明的压缩包。

### 2. 用锁文件干净安装

目的：真实验证 `npm ci`，且不执行依赖生命周期脚本、不修改 npm 安全设置。

```bash
cd "$PROJECT_ROOT/exercise"
test ! -e node_modules
set -o pipefail
npm ci --ignore-scripts --no-audit --no-fund 2>&1 \
  | tee "$PROJECT_ROOT/research/npm-ci.txt"
npm_status=${PIPESTATUS[0]}
echo "npm_ci_exit=$npm_status"
test "$npm_status" -eq 0
```

验证：`npm_ci_exit=0`，不是仅看“added”文字。本次新增 245 包，约 15 秒；审计和 funding 按命令要求跳过，不能写成完成安全审计。

### 3. 阅读组件并单独做类型检查

目的：先确认场景行为，再验证 TypeScript；渲染打包不替代 `tsc`。

```bash
cd "$PROJECT_ROOT/exercise"
npx tsc --noEmit 2>&1 | tee "$PROJECT_ROOT/research/typecheck.txt"
tsc_status=${PIPESTATUS[0]}
echo "tsc_exit=$tsc_status"
test "$tsc_status" -eq 0
```

验证：`tsc_exit=0`。`src/index.tsx` 应有四段 90 帧、标题 spring、三卡 `frame-i*7-8` 和 0–359 的进度映射。

### 4. 用官方 Remotion CLI 渲染独立重放

目的：真正渲染 360 帧，不覆盖原成果。Remotion 可以启动自己的无头渲染流程；这里不操作用户浏览器页面。

```bash
# Windows/MSYS：本次实际需要的可写临时目录
export TMP="$(cygpath -w "$PROJECT_ROOT/work/tmp")"
export TEMP="$TMP"
# Linux 使用下行，不执行上面的 cygpath 两行：
# export TMPDIR="$PROJECT_ROOT/work/tmp"

cd "$PROJECT_ROOT/exercise"
out=../caption-lab-replay.mp4
opts=(--concurrency=2 --browser-executable="$CHROME_BIN")
npx remotion render src/index.tsx CaptionLab "$out" "${opts[@]}" 2>&1 \
  | tee "$PROJECT_ROOT/research/render.txt"
render_status=${PIPESTATUS[0]}
echo "render_exit=$render_status"
test "$render_status" -eq 0
```

验证：`render_exit=0` 且 `$PROJECT_ROOT/caption-lab-replay.mp4` 存在。若失败，保留日志并先检查临时目录写权限；不要删旧失败记录或把后续成功追溯写成首试成功。

### 5. 验证 MP4 并查看四个中点静帧

目的：分别检查容器硬规格与画面。静帧由组件 CLI 直接生成，不冒充从 MP4 抽帧。

```bash
cd "$PROJECT_ROOT/exercise"
"$PYTHON" verify.py ../caption-lab-replay.mp4 2>&1 \
  | tee "$PROJECT_ROOT/research/verify.txt"
verify_status=${PIPESTATUS[0]}
echo "verify_exit=$verify_status"
test "$verify_status" -eq 0

opts=(--browser-executable="$CHROME_BIN")
for item in 01:45 02:135 03:225 04:315; do
  n=${item%%:*}; f=${item##*:}
  out="../frames/replay-$n.png"
  npx remotion still src/index.tsx CaptionLab "$out" --frame="$f" "${opts[@]}"
done
```

若有 ffprobe，可另存完整流信息；本次没有执行这条可选命令：

```bash
ffprobe -v error -show_streams -show_format -of json \
  "$PROJECT_ROOT/caption-lab-replay.mp4" > "$PROJECT_ROOT/research/ffprobe.json"
```

验证：六项规格均 PASS，且四张静帧逐张查看中文、标题、三卡、字幕边界。容器回退只证明 avc1、尺寸、平均帧率、时长、样本数和轨道，不证明全帧解码、播放连续性或所有字幕都安全。

### 6. 用 allowlist 重打源码包并交接 HTML 打印

目的：避免把安装后的 `node_modules`、缓存或视频打入 ZIP。此处在干净复现目录生成 `exercise-rebuilt.zip`，不覆盖输入 ZIP。

```bash
cd "$PROJECT_ROOT"
"$PYTHON" - <<'PY'
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
names = [
    'README.md', 'package.json', 'package-lock.json', 'tsconfig.json',
    'verify.py', 'LICENSE-Remotion.md', 'src/index.tsx',
]
with ZipFile('exercise-rebuilt.zip', 'x', ZIP_DEFLATED) as z:
    for name in names:
        p = Path('exercise') / name
        z.write(p, p.as_posix())
with ZipFile('exercise-rebuilt.zip') as z:
    assert len(z.namelist()) == len(set(z.namelist())) == len(names)
    assert not any('node_modules' in n or '..' in Path(n).parts for n in z.namelist())
    bad = z.testzip()
    assert bad is None, bad
print('exercise-rebuilt.zip', Path('exercise-rebuilt.zip').stat().st_size, 'bytes')
PY
```

验证：7 个 allowlist 文件、CRC 正常、无 `node_modules`。本次修订不生成 PDF；root 负责用 Edge 打开 `guide.html`、实际打印 A4、逐页检查中文/命令/图片/分页，再交独立验收。不要将旧 WeasyPrint PDF 当作本次 Edge 打印结果。
