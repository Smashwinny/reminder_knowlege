# Remotion 第4项修订记录

日期：2026-11-11（Asia/Shanghai）  
范围：仅 `remotion-refined/`；源目录与已有 MP4 保持不变。本记录不是独立审核结论，也不表示已共享发布。

## R1：干净目录、真实安装与命令复现

- 在新的 `repro/` 安全解包，原 ZIP 6 文件、144,715 解压 bytes；拒绝绝对路径、`..`、盘符/ADS、链接、重复与覆盖。
- 实跑 `npm ci --ignore-scripts --no-audit --no-fund`：安装前无 `node_modules`，新增 245 包，退出 0。原始日志：`evidence/02-npm-ci.txt`。
- 实跑 `npx tsc --noEmit`：退出 0，显式记录退出码，不再用空日志代替结果。
- 实跑官方 Remotion CLI：并发 2 首试在 63 帧 `write EOF`；并发 1 重试定位为 F 盘临时文件 `Permission denied`；第三次仅改隔离 `TMP/TEMP` 后退出 0。三份日志均保留，成功文件名为 `caption-lab-replay.mp4`，没有覆盖原 MP4。
- 本机没有 `ffmpeg/ffprobe`，`verify.py` 新增真实 MP4 标准库容器回退；输出 avc1、1080p、30fps、12 秒、360 样本、零音轨并退出 0，同时明确“不解码全帧”。
- 四次 `remotion still`（45/135/225/315）均退出 0，四图逐张查看未见中文或布局异常；不称为从 MP4 抽帧。
- README 改为一个可复制的六步 Bash 配方，显式创建 `research/`、`frames/`、`work/tmp/`，使用 `$PROJECT_ROOT`、`$EXERCISE_ZIP`、`$CHROME_BIN`、`$PYTHON`。Linux 路径标注示例；Windows/MSYS 只声明本次实际范围。
- 移除教程对未打包 WeasyPrint 环境的依赖。本次不生成 PDF，root 负责 Edge 打印。

## R2：HTML 与交付体积

- `guide.html`：1,955,393 → **134,901 bytes**，减少 1,820,492 bytes（约 93.10%），低于 200KB。
- 四张原始 PNG data URL 改为 720×405、JPEG quality 70：20,218 / 19,992 / 18,733 / 21,583 bytes，合计 **80,526 bytes**。源 PNG 不变，JPEG 逐张检查可读。
- 保留 12 个 article、12 个内联 SVG、4 用途、6 步实验和可选择文字；无脚本、无外链图片、无 `@font-face`，统一 Microsoft YaHei 系统字体。
- `exercise.zip`：35,616 → **41,363 bytes**。增加完整六步 README、真实容器回退验证和 LICENSE；7 文件，安全路径及 CRC 通过，无 `node_modules`。
- 不生成或交付新 PDF；不把原 PDF 的体积或目检结果冒充本次 Edge 结果。

## R3：知识增量收窄

`knowledge-proposal.md` 改为“静音字幕主轨：这次真实样例的候选增补”：

1. 4×90 帧、30fps、12 秒、1080p、零音轨的真实样例；无口播与零音轨分开。
2. 7 帧错峰约 233ms 只是既有 spring/stagger 与局部帧知识的实例。
3. 增加原实验和本地重放的具体证据及失败/边界；链接旧验收概念。
4. 确定性渲染、验收合同、ProofOverClaims 不再写成新发明；远端最新 main 留待入库前重读。

## R4：术语与复制排版

- 首次出现处补充 Composition、spring、Sequence、interpolate 的中文定义。
- 说明 clamp 与 extend 的区别，以及 CSS opacity 最终显示钳制不等于插值输出自动钳制。
- 命令使用变量和较短参数数组；`pre` 不再 `overflow-wrap:anywhere`，避免 `--browser-` 等任意断词。长 SHA 放在单独证据段，不承担命令语义。

## 源码与原件

- `src/index.tsx` 与原版字节一致。
- `package.json` 只调整脚本：新增 `typecheck`，render 默认输出独立 replay 并移除写死 Chrome 路径；依赖和 lock 未改。
- `verify.py` 保留 ffprobe 优先路径，增加标准库容器回退。
- 新增 `LICENSE-Remotion.md` 许可快照。
- 原 MP4 仍为 1,271,452 bytes，SHA256 `94bb30211c135902f228081b43f276b6213a9cadd219aaa7d9b70dc206160e1d`。
- 本地重放为 1,219,770 bytes，SHA256 `954072cae49ea5d5537395fa434461581d193468929b9e2973e6a8c21dc6f8ef`；不回写原件。

## 失败与修正留档

- 安全解包脚本首次反斜杠语法错误，修正后才解包。
- 指南首次长 here-doc 写入因 Bash 引号解析失败，改用隔离副本逐项修订。
- PowerShell 图片脚本被执行策略阻止，没有绕过；改用本次虚拟环境 Pillow 13.0.0。
- 首次最终 ZIP 错含 `exercise/D:/...` 条目，被安全校验拒绝；错误包留档，修正后通过。
- Remotion 两次渲染失败完整保留，第三次成功不追溯改写历史。
- README 语法检查最初在 Python 文本管道模式遇到控制台编码/换行干扰，改用 UTF-8 bytes 重新执行；7 个 Bash 块最终 `bash -n` 均为 0，见 `evidence/readme-bash-syntax.json`。
- SHA 清单首次由 Windows 文本模式写成 CRLF，导致 `sha256sum -c` 把 `\r` 当文件名字符；改为二进制 LF 后重新生成并验证。

## 验证与 root 待办

机器结构检查见 `evidence/final-artifact-inspection.json`：12 问、12 SVG、4 JPEG、6 个步骤标题、4 个用途标记、无脚本/外链图/嵌入字体，ZIP 无依赖目录且根 README 与包内一致。最终 ZIP 的另一干净解包副本再次执行锁文件安装（245 包，约 9 秒）和类型检查，两者均退出 0，见 `evidence/final-zip-install-typecheck.txt`。

root 仍需：

1. 用 Edge 打开最终 `guide.html`，真实打印 A4，不沿用旧 PDF；逐页目检中文、SVG、命令、四图、分页和可复制性。
2. 安排另一方按最终 SHA 做独立验收；本 worker 不自称独立通过。
3. 入库前重新读取远端最新 main 并查重。
4. 如需发布，由 root 另行处理；本次未写共享 vault、Git、网站、数据库、凭据或日程。

最终七份交付的真实字节与 SHA256 另见 `SHA256SUMS.txt`，避免在本文件内自报一个会随编辑变化的自身大小。
