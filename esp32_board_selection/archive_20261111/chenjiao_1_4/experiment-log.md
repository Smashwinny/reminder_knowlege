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
