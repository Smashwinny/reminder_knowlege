# ELYTerminal 真实实验日志

时间均为 Asia/Shanghai（UTC+8）。自编驱动不等于独立审核；只运行指定组件，不是全应用验收。

初始环境探测中 `python` 命令不存在（退出 127），随后统一使用 `python3`；一次相对路径 `rg vault` 在上游目录失败（无该目录），改用知识库绝对路径后完成查重。未隐藏这两次失败。

## 2026-11-11T01:02:52.352053+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/01-elyterminal/exercise`

```sh
python3 lab.py baseline
```

真实输出：
```text
  File "/workspace/learn-batch/01-elyterminal/exercise/lab.py", line 37
    if b'
       ^
SyntaxError: unterminated string literal (detected at line 37)

```
退出码：1

## 2026-11-11T01:02:52.399331+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/01-elyterminal/exercise`

```sh
python3 lab.py shell
```

真实输出：
```text
  File "/workspace/learn-batch/01-elyterminal/exercise/lab.py", line 37
    if b'
       ^
SyntaxError: unterminated string literal (detected at line 37)

```
退出码：1

## 2026-11-11T01:03:06.982216+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/01-elyterminal/exercise`

```sh
python3 lab.py baseline
```

真实输出：
```text
系统: Linux-6.12.113+-x86_64-with-glibc2.41
Python: 3.13.5
GNU bash, version 5.2.37(1)-release (x86_64-pc-linux-gnu)
rustc 1.85.1 (4eb161250 2025-03-15) (built from a source tarball)
cargo 1.85.1 (d73d2caf9 2024-12-31)
marks.rs sha256 7ec85d6e42a531e8a67279f8883f0348eef2f7fa3389430f39a5f6148e8f0690
elyterminal.bash sha256 3beb33bb939736ddbb0c09a0c17e90ee4a5dacc006d17c95c6d024e013936b71
2 个上游副本字节一致：PASS
上游 Bash 语法检查：PASS

```
退出码：0

## 2026-11-11T01:03:07.057583+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/01-elyterminal/exercise`

```sh
python3 lab.py shell
```

真实输出：
```text
成功命令 PASS b'\x1b]133;D;0\x07'
失败命令 PASS b'\x1b]133;D;1\x07'
切换目录 PASS b'/space %25 dir\x07'
光标编辑 PASS b'EDIT_OK'
光标编辑边界：只证实 readline 接收方向键；未执行 ELY 鼠标定位
捕获 OSC 133 标记数量: 18
捕获字节数: 789
完整二进制: /workspace/learn-batch/01-elyterminal/exercise/results/pty.raw

```
退出码：0

## 2026-11-11T01:03:14.213941+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/01-elyterminal/exercise`

```sh
python3 lab.py contrast
```

真实输出：
```text
壁纸=(255, 255, 255) 不透明度=1.00 淡填充=1.291105:1 实线边=14.745685:1
壁纸=(255, 255, 255) 不透明度=0.60 淡填充=1.294972:1 实线边=15.151504:1
壁纸=(255, 255, 255) 不透明度=0.25 淡填充=1.298294:1 实线边=15.512682:1
壁纸=(30, 35, 55) 不透明度=1.00 淡填充=1.291105:1 实线边=14.745685:1
壁纸=(30, 35, 55) 不透明度=0.60 淡填充=1.165022:1 实线边=6.216109:1
壁纸=(30, 35, 55) 不透明度=0.25 淡填充=1.020013:1 实线边=2.234323:1
壁纸=(255, 140, 30) 不透明度=1.00 淡填充=1.291105:1 实线边=14.745685:1
壁纸=(255, 140, 30) 不透明度=0.60 淡填充=1.262771:1 实线边=10.686951:1
壁纸=(255, 140, 30) 不透明度=0.25 淡填充=1.244431:1 实线边=8.114042:1
9 个合成场景；两条数学端点断言通过；淡填充均不足 3:1。没有实机合规结论。

```
退出码：0

## 2026-11-11T01:03:14.300031+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/01-elyterminal/exercise`

```sh
python3 lab.py inventory
```

真实输出：
```text
上游 cargo metadata 退出码: 0
上游包版本: 0.2.4 最低 Rust: 1.95
本环境 rustc 1.85.1 < 1.95：完整应用未构建；不下载新工具链、不冒称全量测试。
待验证：macOS 11+ Apple silicon 安装、macOS 27 透明背景、GUI 多会话/宠物、中文软折行的点击光标定位。

```
退出码：0

## 2026-11-11T01:03:15.997273+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/01-elyterminal/exercise`

```sh
env CARGO_HOME=/workspace/learn-batch/_common/cargo-home cargo test -- --nocapture
```

真实输出：
```text
    Updating crates.io index
     Locking 1 package to latest compatible version
      Adding log v0.4.28 (available: v0.4.35)
 Downloading crates ...
  Downloaded log v0.4.28
   Compiling log v0.4.28
   Compiling ely-marks-learning v0.1.0 (/workspace/learn-batch/01-elyterminal/exercise)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 1.97s
     Running unittests src/main.rs (target/debug/deps/ely_marks_learning-5648c1793f95b06c)

running 3 tests
test marks::tests::a_mark_the_terminal_takes_no_action_on_reads_as_none ... ok
test marks::tests::each_mark_reads_with_its_options_as_ghostty_reads_it ... ok
test marks::tests::a_prompt_names_elyterminal_s_shell_by_aid ... ok

test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s


```
退出码：0

## 2026-11-11T01:03:16.363452+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/01-elyterminal/exercise`

```sh
env CARGO_HOME=/workspace/learn-batch/_common/cargo-home cargo run -- results/bodies.txt
```

真实输出：
```text
   Compiling ely-marks-learning v0.1.0 (/workspace/learn-batch/01-elyterminal/exercise)
warning: function `named` is never used
  --> src/../vendor/marks.rs:58:15
   |
58 | pub(crate) fn named(body: &[u8]) -> bool {
   |               ^^^^^
   |
   = note: `#[warn(dead_code)]` on by default

warning: `ely-marks-learning` (bin "ely-marks-learning") generated 1 warning
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.32s
     Running `target/debug/ely-marks-learning results/bodies.txt`
"A;aid=elyterminal" -> Some(Prompt(Arrows))
"B" -> Some(Input)
"C" -> Some(Output)
"D;0" -> Some(Done(Some(0)))
"A;aid=elyterminal" -> Some(Prompt(Arrows))
"B" -> Some(Input)
"C" -> Some(Output)
"D;1" -> Some(Done(Some(1)))
"A;aid=elyterminal" -> Some(Prompt(Arrows))
"B" -> Some(Input)
"C" -> Some(Output)
"D;0" -> Some(Done(Some(0)))
"A;aid=elyterminal" -> Some(Prompt(Arrows))
"B" -> Some(Input)
"C" -> Some(Output)
"D;0" -> Some(Done(Some(0)))
"A;aid=elyterminal" -> Some(Prompt(Arrows))
"B" -> Some(Input)

```
退出码：0

## 2026-11-11T01:08:07.766744+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/01-elyterminal`

```sh
python3 /workspace/learn-batch/_common/render_pdf.py '/workspace/learn-batch/01-elyterminal/ELYTerminal-学习指南.html' '/workspace/learn-batch/01-elyterminal/ELYTerminal-学习指南.pdf'
```

真实输出：
```text
命令： ['/opt/google/chrome/chrome', '--headless', '--disable-gpu', '--no-pdf-header-footer', '--disable-background-networking', '--user-data-dir=/workspace/learn-batch/01-elyterminal/render-profile', '--print-to-pdf=/workspace/learn-batch/01-elyterminal/ELYTerminal-学习指南.pdf', 'file:///workspace/learn-batch/01-elyterminal/ELYTerminal-%E5%AD%A6%E4%B9%A0%E6%8C%87%E5%8D%97.html']
[1111/010637.768122:WARNING:chrome/app/chrome_main_linux.cc:84] Read channel stable from /opt/google/chrome/CHROME_VERSION_EXTRA
[164659:164681:1111/010637.805035:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[164659:164681:1111/010637.834510:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[164659:164681:1111/010637.834961:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[164659:164681:1111/010637.835033:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[164659:164681:1111/010637.997082:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[164659:164681:1111/010637.997107:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[164659:164659:1111/010638.008142:ERROR:dbus/object_proxy.cc:572] Failed to call method: org.freedesktop.DBus.Properties.GetAll: object_path= /org/freedesktop/UPower/devices/DisplayDevice: unknown error type: 
Fontconfig error: Cannot load default config file: File not found
Created TensorFlow Lite XNNPACK delegate for CPU.
Traceback (most recent call last):
  File "/workspace/learn-batch/_common/render_pdf.py", line 7, in <module>
    print('命令：',cmd,flush=True);r=subprocess.run(cmd,timeout=90);raise SystemExit(r.returncode)
                                     ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 556, in run
    stdout, stderr = process.communicate(input, timeout=timeout)
                     ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 1222, in communicate
    stdout, stderr = self._communicate(input, endtime, timeout)
                     ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 2154, in _communicate
    self.wait(timeout=self._remaining_time(endtime))
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 1280, in wait
    return self._wait(timeout=timeout)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 2058, in _wait
    raise TimeoutExpired(self.args, timeout)
subprocess.TimeoutExpired: Command '['/opt/google/chrome/chrome', '--headless', '--disable-gpu', '--no-pdf-header-footer', '--disable-background-networking', '--user-data-dir=/workspace/learn-batch/01-elyterminal/render-profile', '--print-to-pdf=/workspace/learn-batch/01-elyterminal/ELYTerminal-学习指南.pdf', 'file:///workspace/learn-batch/01-elyterminal/ELYTerminal-%E5%AD%A6%E4%B9%A0%E6%8C%87%E5%8D%97.html']' timed out after 90 seconds

```
退出码：1

## 2026-11-11T01:10:11.163983+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/01-elyterminal`

```sh
python3 /workspace/learn-batch/01-elyterminal/_tools/render_pdf.py '/workspace/learn-batch/01-elyterminal/ELYTerminal-学习指南.html' '/workspace/learn-batch/01-elyterminal/ELYTerminal-学习指南.pdf'
```

真实输出：
```text
命令： ['/opt/google/chrome/chrome', '--headless', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--timeout=15000', '--no-pdf-header-footer', '--disable-background-networking', '--user-data-dir=/workspace/learn-batch/01-elyterminal/render-profile', '--print-to-pdf=/workspace/learn-batch/01-elyterminal/ELYTerminal-学习指南.pdf', 'file:///workspace/learn-batch/01-elyterminal/ELYTerminal-%E5%AD%A6%E4%B9%A0%E6%8C%87%E5%8D%97.html']
[1111/011010.111992:WARNING:chrome/app/chrome_main_linux.cc:84] Read channel stable from /opt/google/chrome/CHROME_VERSION_EXTRA
[177759:177780:1111/011010.149548:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[177759:177780:1111/011010.172841:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[177759:177780:1111/011010.172909:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[177759:177780:1111/011010.172922:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[177759:177780:1111/011010.330248:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[177759:177780:1111/011010.330275:ERROR:dbus/bus.cc:405] Failed to connect to the bus: Failed to connect to socket /run/dbus/system_bus_socket: No such file or directory
[177759:177759:1111/011010.340965:ERROR:dbus/object_proxy.cc:572] Failed to call method: org.freedesktop.DBus.Properties.GetAll: object_path= /org/freedesktop/UPower/devices/DisplayDevice: unknown error type: 
Created TensorFlow Lite XNNPACK delegate for CPU.
1227838 bytes written to file /workspace/learn-batch/01-elyterminal/ELYTerminal-学习指南.pdf

```
退出码：0

## 2026-11-11T01:10:50.957497+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/01-elyterminal/exercise`

```sh
env CARGO_HOME=/workspace/learn-batch/01-elyterminal/_tools/cargo-home cargo test -- --nocapture
```

真实输出：
```text
    Updating crates.io index
 Downloading crates ...
  Downloaded log v0.4.28
   Compiling log v0.4.28
   Compiling ely-marks-learning v0.1.0 (/workspace/learn-batch/01-elyterminal/exercise)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.71s
     Running unittests src/main.rs (target/debug/deps/ely_marks_learning-5648c1793f95b06c)

running 3 tests
test marks::tests::a_prompt_names_elyterminal_s_shell_by_aid ... ok
test marks::tests::each_mark_reads_with_its_options_as_ghostty_reads_it ... ok
test marks::tests::a_mark_the_terminal_takes_no_action_on_reads_as_none ... ok

test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s


```
退出码：0

## 2026-11-11T01:10:51.245886+08:00（Asia/Shanghai）

工作目录：`/workspace/learn-batch/01-elyterminal/exercise`

```sh
env CARGO_HOME=/workspace/learn-batch/01-elyterminal/_tools/cargo-home cargo run -- results/bodies.txt
```

真实输出：
```text
   Compiling ely-marks-learning v0.1.0 (/workspace/learn-batch/01-elyterminal/exercise)
warning: function `named` is never used
  --> src/../vendor/marks.rs:58:15
   |
58 | pub(crate) fn named(body: &[u8]) -> bool {
   |               ^^^^^
   |
   = note: `#[warn(dead_code)]` on by default

warning: `ely-marks-learning` (bin "ely-marks-learning") generated 1 warning
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.24s
     Running `target/debug/ely-marks-learning results/bodies.txt`
"A;aid=elyterminal" -> Some(Prompt(Arrows))
"B" -> Some(Input)
"C" -> Some(Output)
"D;0" -> Some(Done(Some(0)))
"A;aid=elyterminal" -> Some(Prompt(Arrows))
"B" -> Some(Input)
"C" -> Some(Output)
"D;1" -> Some(Done(Some(1)))
"A;aid=elyterminal" -> Some(Prompt(Arrows))
"B" -> Some(Input)
"C" -> Some(Output)
"D;0" -> Some(Done(Some(0)))
"A;aid=elyterminal" -> Some(Prompt(Arrows))
"B" -> Some(Input)
"C" -> Some(Output)
"D;0" -> Some(Done(Some(0)))
"A;aid=elyterminal" -> Some(Prompt(Arrows))
"B" -> Some(Input)

```
退出码：0

## 文档生成与续接说明（执行记录摘要，不冒充逐字命令输出）
- 文档生成器首版外围三引号与内部三引号冲突，产生 SyntaxError，初次未生成 HTML；恢复本项生成器后成功生成 12 分组 HTML。
- 第一次 Chrome 打印超时 90 秒、退出 1；当时输入尚未就绪，并有 Fontconfig 配置错误。失败完整输出保留在本日志。
- 后续在 HTML 已存在、显式 FONTCONFIG_FILE/PATH、跳过首次启动设置后，Chrome 默认沙箱打印成功，输出 1,227,838 字节。改动组合成功，不能单独归因于某一参数。没有关闭浏览器沙箱、修改系统安全设置或改变用户设备。
- 续接时遵照新范围，只写本项目录；自有脚本复制到本项 `_tools`，不再改共享 `_common`。原日志保留历史路径；为验证文档里迁移后的命令，只重放 Rust 两条命令，其余已完成实验未重做。
- 实际执行后处理：`pdfinfo ELYTerminal-学习指南.pdf`；`pdftoppm -scale-to 1500 -png ELYTerminal-学习指南.pdf pdf-pages/page`；`pdftotext -layout ELYTerminal-学习指南.pdf pdf-pages/extracted.txt`；`pdffonts ELYTerminal-学习指南.pdf`。均退出 0。
- pdfinfo：12 页，594.96 × 841.92 pt（A4），HeadlessChrome 156 / Skia PDF；中文 NotoSansCJKsc-Regular/Bold 已嵌入。无需安装字体。
- 页图 page-01.png 至 page-12.png 均逐页调用 Read 视觉自查，中文/内联 SVG 正常，无截断、无溢出；不是独立审核。
- 结构核查：12 问、12 内联 SVG、12 页；页脚 12/12 可提取；无外部图片或脚本。上游 `git status --short` 无输出，保持干净。
