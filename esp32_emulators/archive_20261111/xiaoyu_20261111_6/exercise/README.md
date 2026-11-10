# 练习代码（第 6 项）

教学脚本，不捆绑上游模拟器二进制、mask ROM 或 4MB flash 镜像。

```sh
python3 exercise/lab.py env
python3 exercise/lab.py matrix
python3 exercise/lab.py flash
python3 exercise/lab.py observed
python3 exercise/lab.py verify
```

- `flash` 会在 `exercise/results/` 写下合成镜像和摘要。合成头合法，但不能启动芯片。
- `observed` 只复述本批已经捕获的串口对照，不会重新启动模拟器。
- 完整模拟器命令见指南主实验与 `experiment-log.md`。需要自行下载：
  - `esp-emu` v1.0.0-rc2（校验 SHA256SUMS）
  - `espressif/qemu` 预编译 `esp-develop-9.2.2-20261109`
  - `esp32sim` v0.3.0 与 `espressif/esp-rom-elfs` 20260528
  - 官方 examples 固件或仓库内公开 hello_world 分段镜像
