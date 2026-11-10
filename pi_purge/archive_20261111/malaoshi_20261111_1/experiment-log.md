# 真实云端实验记录

时间：2026-11-11 Asia/Shanghai (UTC+8)。目录：/workspace/reminder-batch/item-1-pi-purge。只运行自有夹具与审读后的公开扩展，不启动 Pi、不用账户/用户密钥、不调用模型。

## 真实部分与替代部分
当前扩展原样运行；原帖固定扩展仅将 EMBEDDED_PERSONA 替为无害常量。Pi 提示构造器去 import/export 和类型后在 VM 中执行；config 路径与 skills renderer 是桩；当前 sections 拼接为夹具。VM/全局 fetch 抛错不是强安全沙箱，也不是全进程网络审计。

## 准备步骤实录
`node --version && python3 exercise/verify.py`
```text
v24.22.1
PASS 20 artifact SHA-256 checks; pinned persona is explicitly redacted; no original payload execution
```

## run-compat.txt
```text
Time Asia/Shanghai: 2026-11-11T00:57:06.075864
CWD: /workspace/reminder-batch/item-1-pi-purge
COMMAND: node exercise/lab.mjs compat
EXIT: 0
STDOUT:
PASS latest identity anchor no match
PASS latest docs anchor no match
PASS replace latest behaves like prepend
PASS strict latest drops all host sections
PASS partial match removes identity independently
Compatibility: 0.84.2 markers match; 1.5.2 current markers changed. CLI/E2E not executed.
RESULT stage=compat checks=5; zero model client; fixture-level only

STDERR:
(node:134265) ExperimentalWarning: stripTypeScriptTypes is an experimental feature and might change at any time
(Use `node --trace-warnings ...` to show where the warning was created)

```

## run-env.txt
```text
Time Asia/Shanghai: 2026-11-11T00:57:06.288325
CWD: /workspace/reminder-batch/item-1-pi-purge/evidence/purge-current
COMMAND: node test/pi-purge-env-source.test.mjs
EXIT: 0
STDOUT:
OK — PI_PURGE_SOURCE 断言通过

STDERR:

```

## run-lifecycle.txt
```text
Time Asia/Shanghai: 2026-11-11T00:57:05.970111
CWD: /workspace/reminder-batch/item-1-pi-purge
COMMAND: node exercise/lab.mjs lifecycle
EXIT: 0
STDOUT:
PASS session_start disables
PASS mode does NOT reset on session_start
PASS append status retains stale cut
PASS README reload command not implemented
PASS bad source reports error
PASS bad source rollback keeps persona
PASS same-module multiple registrations share state
RESULT stage=lifecycle checks=7; zero model client; fixture-level only

STDERR:
(node:134255) ExperimentalWarning: stripTypeScriptTypes is an experimental feature and might change at any time
(Use `node --trace-warnings ...` to show where the warning was created)

```

## run-modes.txt
```text
Time Asia/Shanghai: 2026-11-11T00:57:05.844089
CWD: /workspace/reminder-batch/item-1-pi-purge
COMMAND: node exercise/lab.mjs modes
EXIT: 0
STDOUT:
PASS purge-current default disabled
PASS purge-current strict retains cwd
PASS purge-current strict drops project/tools
PASS purge-current replace removes old identity
PASS purge-current replace removes old docs
PASS purge-current replace retains project
PASS purge-current append is actually prepend
{"label":"purge-current","hostChars":1713,"strictChars":518,"replaceChars":1006,"appendChars":2198}
PASS purge-post default disabled
PASS purge-post strict retains cwd
PASS purge-post strict drops project/tools
PASS purge-post replace removes old identity
PASS purge-post replace removes old docs
PASS purge-post replace retains project
PASS purge-post append is actually prepend
{"label":"purge-post","hostChars":1713,"strictChars":91,"replaceChars":579,"appendChars":1771}
RESULT stage=modes checks=14; zero model client; fixture-level only

STDERR:
(node:134230) ExperimentalWarning: stripTypeScriptTypes is an experimental feature and might change at any time
(Use `node --trace-warnings ...` to show where the warning was created)

```

## run-upstream.txt
```text
Time Asia/Shanghai: 2026-11-11T00:57:06.183629
CWD: /workspace/reminder-batch/item-1-pi-purge/evidence/purge-current
COMMAND: node test/pi-purge.test.mjs
EXIT: 0
STDOUT:
OK — 9 组断言全部通过
内嵌人设注入后: 524 字符

STDERR:

```

## 失败与未验证
准备阶段 python 不存在退出127；两类错误路径/未下载文件及 dsh 404 详见 sources.md。5 个实验子进程均退出0，无模型客户端导入或模型调用。26 条自写特征化检查与上游9组+环境源套件分开计数，不凑成功率。CLI、TUI、类型兼容、真实 provider、RAE、多进程调度与用户本机仍待验证。

## 步骤6真实回读
命令：
```bash
python3 -c "from pathlib import Path; fs=sorted(Path('evidence').glob('run-*.txt')); print([(p.name, 'EXIT: 0' in p.read_text()) for p in fs]); assert len(fs)==5 and all('EXIT: 0' in p.read_text() for p in fs)"
```
真实输出：五份 run-compat/env/lifecycle/modes/upstream.txt 都为 True，命令退出0。

## PDF实际打印与逐页自检（不是独立审核）
命令：
```bash
/usr/bin/google-chrome --headless --no-sandbox --disable-dev-shm-usage --no-pdf-header-footer --print-to-pdf=/workspace/reminder-batch/item-1-pi-purge/pi-purge.pdf file:///workspace/reminder-batch/item-1-pi-purge/index.html
pdfinfo pi-purge.pdf
pdftoppm -scale-to 1200 -png pi-purge.pdf evidence/final-page
```
Chrome仅打开自有静态HTML打印，没有接管用户浏览器或更改系统安全配置。初次打印11页：证据索引溢出到尾页；缩短可见链接（完整URL仍为可点击目标且sources.md保留）后重打10页。最终pdfinfo：10页，594.96×841.92pt(A4)，PDF1.4，957981 bytes。打印时间2026-11-11 01:00:08 Asia/Shanghai(UTC+8)。

已用 Read 实际逐页查看 evidence/final-page-01.png 至 final-page-10.png：
- 1：封面/用途/边界完整，无裁切。
- 2：SHA表/查重说明完整，无列溢出。
- 3：疑问1-2与2个SVG完整。
- 4：疑问3-4与2个SVG完整。
- 5：疑问5-6与2个SVG完整。
- 6：疑问7-8与2个SVG完整。
- 7：疑问9-10与2个SVG完整。
- 8：步骤1-3命令/结果/验证完整。
- 9：步骤4-6命令自动折行、尾注完整。
- 10：19条证据锚点与未验证说明完整，无额外空白页。
这是制作者自检，不冒充他人独立审核。
