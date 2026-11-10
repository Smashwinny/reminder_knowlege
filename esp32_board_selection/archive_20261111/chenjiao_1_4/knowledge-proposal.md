---
tags: [候选成果, 增量学习, 未合入]
created: 2026-11-11
---
# 第4项 knowledge proposal：ESP32选型先看项目契约

## 查重与差异
固定main：a8674777e18302b8804b137212b1396cbfe5a747。已读00-总览及相关概念正文。总览未列本批七条原帖的专门项目记录；没有据此断言全仓库绝无重叠。
不重复Muse/Gadgets分工概念，向规格书先行与源码取证补充板型契约案例；树文件数、目录数、发布变体数不能混用。

## 建议追加的项目案例（待协调者审核）
来源：https://x.com/i/status/2112357123246178332；一手SHA见sources.md。

### 两个S3 N16R8为什么仍不通用？
屏幕控制器、音频codec、I2S引脚、按钮和电源电路可能不同。合成契约仅把codec由ES8311换成other，即使芯片容量不变也拒绝；这不是真实板厂合格证，而是兼容性判定示范。

### 旧教程用ESP-IDF 5还能直接照做吗？
当前小智README_zh明确要求ESP-IDF v6.0.1或以上，推荐release/v6.1分支，不再支持5.x，并提到特定标签在C3上的问题。版本号与分支名不可混淆，本批没有安装SDK或实测这个问题。

### 没有硬件时今天能真正完成什么？
可以审计真实仓库树、解析规格表达、构造不兼容反例并保存输出。本批完成这些可在云端复跑的局部检查；USB识别、PSRAM读数、驱动、供电和烧录仍待真实设备与持有人配合。

## 建议互链，不新建同义概念
[[接缝与桩实现StubSeam]]、[[级联语音管线]]、[[证据优先质检ProofOverClaims]]、[[规格书先行SpecDriven]]。按实际概念选择落点，禁止把整个案例机械加到全部笔记。

## 本批状态
待验证：原长文和小智固定SHA支持树已读；真实886个板目录文件审计完成。未读出真实芯片容量、编译或烧录固件。

## 可复核结果
# 第4项真实实验日志
执行时间：2026-11-11T00:58:16.584257+08:00 Asia/Shanghai
环境：Linux云电脑；全部为受控数据。

## 步骤 1
```sh
cd /workspace/reminder-batch-2026-11-11/item04/exercise
python3 lab.py 1
```
退出码：0
```text
{"python": "3.13.5", "scope": "固件板目录审计与合成规格契约"}

```

## 步骤 2
```sh
cd /workspace/reminder-batch-2026-11-11/item04/exercise
python3 lab.py 2
```
退出码：0
```text
{"board_files": 886, "leaf_directories": 173, "matching_paths": ["main/boards/lckfb/szpi-esp32c3/README.md", "main/boards/lckfb/szpi-esp32c3/config.h", "main/boards/lckfb/szpi-esp32c3/config.json", "main/boards/lckfb/szpi-esp32c3/lichuang_c3_dev_board.cc", "main/boards/lckfb/szpi-esp32s3/config.h", "main/boards/lckfb/szpi-esp32s3/config.json", "main/boards/lckfb/szpi-esp32s3/lichuang_dev_board.cc", "main/boards/waveshare/esp32-s3-touch-amoled-1.75/README.md", "main/boards/waveshare/esp32-s3-touch-amoled-1.75/config.h", "main/boards/waveshare/esp32-s3-touch-amoled-1.75/config.json", "main/boards/waveshare/esp32-s3-touch-amoled-1.75/esp32-s3-touch-amoled-1.75.cc"], "sha": "a73e9a7e266e3196d1368ba46c30bee0d81f0a64"}

```

## 步骤 3
```sh
cd /workspace/reminder-batch-2026-11-11/item04/exercise
python3 lab.py 3
```
退出码：0
```text
{"illustrative_suffix_parser": {"ESP32-S3": null, "N16R8": {"flash_MiB": 16, "psram_MiB": 8}, "N8R2": {"flash_MiB": 8, "psram_MiB": 2}}, "warning": "商品缩写不证明真实容量，更不证明引脚兼容"}

```

## 步骤 4
```sh
cd /workspace/reminder-batch-2026-11-11/item04/exercise
python3 lab.py 4
```
退出码：0
```text
{"conclusion": "同芯片同容量但codec不同仍拒绝；清单不在场则未知", "synthetic_manifest_accepts": [true, false]}

```

## 合入边界
仅为隔离候选提案，没有合入共享vault、改变网站标签、勾选Reminder或Git发布。自检不是独立审核；待协调者复核。
