# ESP32 小黄人：从单麦到声源转向 · 真实实验日志

执行时间：2026-11-11 01:06:20 CST（UTC+8）

只读公共研究＋云端隔离实验。自编程序不是上游实现，除明确标出的官方构建。

## 合成五组双麦输入
目的：固定种子与理想远场几何

```bash
cd /workspace/reminder-batch-2026-11-11/item-2-esp32-minion
python3 exercise/direction.py fixture
```

真实输出（exit=0）：
```text
5 ideal broadband pairs; fs=48000 Hz, spacing=0.08 m; synthetic only

```
验证：fs=48000、d=0.08、角度−60/−30/0/30/60

## 估计方向与限幅
目的：用完整互相关最大峰估计整数样本时差

```bash
cd /workspace/reminder-batch-2026-11-11/item-2-esp32-minion
python3 exercise/direction.py run
```

真实输出（exit=0）：
```text
[
  {
    "truth": -60,
    "lag_samples": -10,
    "estimate_deg": -63.282,
    "error_deg": 3.282,
    "target_deg": 30.0,
    "first_command_deg": 80.0
  },
  {
    "truth": -30,
    "lag_samples": -6,
    "estimate_deg": -32.408,
    "error_deg": 2.408,
    "target_deg": 57.592,
    "first_command_deg": 80.0
  },
  {
    "truth": 0,
    "lag_samples": 0,
    "estimate_deg": 0.0,
    "error_deg": 0.0,
    "target_deg": 90.0,
    "first_command_deg": 90.0
  },
  {
    "truth": 30,
    "lag_samples": 6,
    "estimate_deg": 32.408,
    "error_deg": 2.408,
    "target_deg": 122.408,
    "first_command_deg": 100.0
  },
  {
    "truth": 60,
    "lag_samples": 10,
    "estimate_deg": 63.282,
    "error_deg": 3.282,
    "target_deg": 150.0,
    "first_command_deg": 100.0
  }
]

```
验证：负角对应负时差，零角为0样本

## 运行误差与边界断言
目的：验证5个必要但非充分的验收条件

```bash
cd /workspace/reminder-batch-2026-11-11/item-2-esp32-minion
python3 exercise/direction.py verify
```

真实输出（exit=0）：
```text
PASS 5 assertions; max error 3.282 deg; no noise, reverberation, servo, board or API tested

```
验证：最大误差<5°；目标30–150°；单步≤10°

## 锁定输入输出
目的：记录本次代码与夹具的实际指纹

```bash
cd /workspace/reminder-batch-2026-11-11/item-2-esp32-minion
sha256sum exercise/direction.py exercise/signals.npz exercise/results.json
```

真实输出（exit=0）：
```text
76aea76758513c4dcb65ecfff1af8aac475d696ef97ebdec8849fe013f7dd346  exercise/direction.py
f3011e977c7031446be531f25aae8ac5926d176a10bae1fb8d91010dbbd613e6  exercise/signals.npz
be23129a0a1d23d81396d02bef6a85d0ae277f995064053e6f8b1badf4b76eae  exercise/results.json

```
验证：按日志定位本次数据；NPZ重新生成可能含归档元信息差异


## 未验证边界
没有 ESP32、双麦阵列、屏幕、凸透镜、驱动、电池、相机或真实音频；混响、噪声、回声、DMA同步、前后歧义、功耗和总价待验证。
