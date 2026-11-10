# experiment-log：真实云端运行

运行日：2026-11-11（Asia/Shanghai）。已真实启动官方预编译模拟器和公开固件；没有 ESP-IDF Docker 现编译，没有 Velxio 网页交互，没有实物板，没有作者私有验收固件。

## 环境与依赖

- 主机：Linux 6.12.113+ x86_64，Python 3.13.5，无 Docker，无 NVIDIA。
- `esp-emu` 1.0.0-rc2，静态链接，SHA256 与官方 SHA256SUMS 一致。
- `qemu-system-{riscv32,xtensa}` 9.2.2（`esp_develop_9.2.2_20261109`），校验和一致。首次启动因缺少 `libslirp.so.0` 失败；本机 apt 源对 deb.debian.org 返回 500。随后从 `http://archive.ubuntu.com/ubuntu/pool/main/libs/libslirp/libslirp0_4.7.0-1ubuntu3_amd64.deb` 解出库，用 `LD_LIBRARY_PATH` 启动成功。deb SHA256：`1da5239a2829ad5e91da02e8a56fd3cb8cff116e7adafeb07f9c9d6e7804f0f3`。
- `esp32sim` 0.3.0 linux-x86_64，校验和一致。mask ROM 来自 espressif/esp-rom-elfs 20260528，哈希与官方 fetch 脚本一致。
- 教学脚本：`python3 exercise/lab.py verify`，8 组自写检查通过。合成 2MiB 镜像由脚本生成，不能启动芯片。

## 六步主实验的真实输出

完整命令见指南。下面保留关键标准输出，而非手写预期。原始全文在 `sources/run-logs/`。

### E2 拒绝经典芯片 + 按键固件就绪

`esp-emu --chip esp32 ...` 退出码 2：

```text
error: invalid value 'esp32' for '--chip <CHIP>'
  [possible values: esp32c3, esp32c5, esp32c6, esp32h2, esp32p4, esp32s3, esp32s31]
  tip: a similar value exists: 'esp32s3'
```

按键固件（222224 字节，未填充）启动成功，退出码 0。摘录：

```text
[INFO  cli::run] TAP auto-probe failed (TUNSETIFF failed for 'tap0': Operation not permitted (os error 1)); falling back to --net user
[INFO  cli::run] Loaded ROM ELF: <embedded esp32c3> (556332 bytes)
ESP-ROM:esp32c3-api1-20210207
I (7) boot: ESP-IDF v6.1-1055-gf0114250e20 2nd stage bootloader
I (29) app_init: Project name:     gpio_button
I (29) app_init: App version:      v1.0.0-rc2
I (29) cpu_start: Unicore app
BUTTON: ready level=1
[INFO  cli::run] Exit-on string 'BUTTON: ready' found in output
```

### E3 控制通道按/放

控制通道：

```text
> part list
< ok button
> part button input press
< ok
> part button input release
< ok
exit=0
```

串口顺序：`BUTTON: ready level=1` → `BUTTON: pressed` → `BUTTON: released`。

### E4 QEMU 尺寸错误与默认电平

未填充：

```text
qemu-system-riscv32: Drive size error: only 2, 4, 8, and 16MB images are supported
exit=1
```

填充到 4MB 后同一固件启动，timeout 结束（124）：

```text
I (28) app_init: Project name:     gpio_button
W (29) spi_flash: Detected size(4096k) larger than the size in the binary image header(2048k). Using the size in the binary image header.
BUTTON: ready level=0
qemu-system-riscv32: terminating on signal 15 from pid ... (timeout)
```

对照：esp-emu（有上拉零件）level=1；QEMU（无零件）level=0。

### E5 同一份 C3 hello_world

三工具均打印：

```text
Hello world!
This is esp32c3 chip with 1 CPU core(s), WiFi/BLE, silicon revision v0.3, 2MB external flash
Minimum free heap size: 331296 bytes
```

其中 esp32sim 将 revision 显示为 v0.4，闪存为 generic；esp-emu 与 QEMU 为 v0.3、gd。ELF SHA 前缀均为 `4812b1c53`，IDF v5.5.4，编译时间 Aug 29 2026 12:37:37。

### E6 经典 ESP32 hello_world

QEMU `-machine esp32`：

```text
Hello world!
This is esp32 chip with 2 CPU core(s), WiFi/BTBLE, silicon revision v0.0, 4MB external flash
Minimum free heap size: 303972 bytes
```

esp32sim `--chip esp32`：

```text
W (11) rtc_clk_init: Bogus XTAL freq: 8MHz
W (12) rtc_clk_init: Possibly invalid CONFIG_XTAL_FREQ setting (40MHz). Detected 0MHz.
I (4) boot: chip revision: v2.0
Hello world!
This is esp32 chip with 2 CPU core(s), WiFi/BTBLE, silicon revision v2.0, 4MB external flash
Minimum free heap size: 303972 bytes
[emu] stop: Halted — core0 5277916 + core1 1262073 insns in 0.2s wall = 31.0 Minsn/s; emulated 8.000s
```

ELF SHA 前缀 `262a8b0a1`。XTAL 警告如实保留；不把 early 支持写成与硅片一致。

## 执行边界

- 未运行 Velxio（无 Docker，未打开 velxio.dev 做交互动画）。
- 未运行网页版 esp-emulator / esp32sim playground。
- 未使用作者私有验收固件，因此不声称复现点灯/NVS/PSRAM/LVGL。
- 未做真实 Wi-Fi 关联或外网 HTTP 往返；只观察到 esp-emu 的 user-net 后端就绪。
- QEMU 的 124 退出码来自 timeout，不是固件 panic。
- lab.py 的 verify 是同一作者自写检查，不能称独立审核或上游测试套件通过。

## PDF 真实打印

2026-11-11 01:19:26（Asia/Shanghai），Chromium（Playwright，Skia/PDF m158）输出 A4 PDF，pdfinfo 确认 11 页，约 1004KB。
打印命令：`/workspace/learn-batch/01-lingbot-map/.print-env/bin/python print_guide.py`（复用已有 Playwright 环境，未另装）。
逐页渲染命令：`pdftoppm -scale-to 1200 -png ESP32模拟器选型-增量学习指南.pdf qa/page`。
检查方法：逐一读取 qa/page-01.png 至 page-11.png；各页中文、图、表、命令完整可见，无横向溢出、截字或额外空白页。完整检查见 qa/page-check.md。

