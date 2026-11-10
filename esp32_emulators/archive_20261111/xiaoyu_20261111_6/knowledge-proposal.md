# knowledge-proposal（只供协调者合入，不自行提交）

## 状态
真实完成：原帖全文与关键回复、三仓库+官方 QEMU 定版、查重、12问+12个内联SVG、5个用途、六步主实验（含真实串口）、A4 打印与逐页自查。
部分待验证：Velxio/网页交互、作者私有验收固件（点灯/双核/NVS/PSRAM/LVGL）、真实 Wi-Fi/BLE/Thread、与实物板对照。不自动勾选用户任务。

## 查重基线
公开 main `a8674777e18302b8804b137212b1396cbfe5a747`，提交时间 2026-11-04 17:42:58（Asia/Shanghai）。已检索完整 git 树与 `vault/00-总览.md`：没有 Velxio、esp32sim、esp-emulator、espressif/qemu、ESP32 模拟器专条。相近领域只有「物联网 / 智能家居」（zigbee2mqtt），主题不重叠。并行批次若出现 ESP32/Tailscale 网络笔记，本批只互链「模拟器选型」，不重写家庭组网。

## 建议改动（候选，不是已执行）
1. 新增 `vault/项目笔记/esp-emulators.md`：以原帖三款为主，另记官方 qemu 是独立仓库；作者原话「官方是第三个」。固定本批 SHA 与发布版本。明确作者私有固件结果不得写成知识库已复现事实。
2. 可选新概念 `vault/概念/合并Flash镜像与模拟器契约.md`：应用分区 .bin ≠ merge-bin；QEMU 仅接受 2/4/8/16MB；C3 默认 0x0/0x8000/0x10000，经典 ESP32 bootloader 在 0x1000。用本批真实失败（未填充 Drive size error）做例子。
3. 可选短笔记：同一固件在不同模拟器上的默认 GPIO/eFuse/时钟可以不一致（按键 level=1 vs 0；C3 rev v0.3 vs v0.4；经典 XTAL 警告）。不必拆成过细原子概念，可先放在项目笔记对照表。
4. `vault/00-总览.md` 只追加项目索引，不改历史累计数量。

## 不应合入为事实的说法
- 「官方模拟器就是 espressif/qemu」。
- 「esp-emulator 已经开源」或「有 LICENSE 文件等于源码可构建」。issue #10 仍开放，官方回复尚未决定。
- 「本批复现了作者的点灯/双核/NVS/PSRAM/LVGL 验收」。只跑了公开 examples / hello_world。
- 「网页版也能直接上外网」；「20 FPS / 星标数字是当前规模」。
- 「独立审核已完成」：仅同一 worker 逐页自查。
- 把 TryBoard 预告或配图当成已发布、已实测产品。

建议索引标签：`学习交付完成；网页/真板/作者私有固件待验证`。任务状态与网站标签由协调者管理，本 worker 未触及。
