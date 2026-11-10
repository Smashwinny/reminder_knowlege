# 第1项真实实验日志
执行时间：2026-11-11T00:58:16.305444+08:00 Asia/Shanghai
环境：Linux云电脑；全部为受控数据。

## 步骤 1
```sh
cd /workspace/reminder-batch-2026-11-11/item01/exercise
python3 lab.py 1
```
退出码：0
```text
{"python": "3.13.5", "scope": "离线ADB帧与可逆状态夹具；无设备连接"}

```

## 步骤 2
```sh
cd /workspace/reminder-batch-2026-11-11/item01/exercise
python3 lab.py 2
```
退出码：0
```text
{"frame_hex": "30303065686f73743a646576696365732d6c", "payload": "host:devices-l", "prefix": "000e", "truncated": "rejected"}

```

## 步骤 3
```sh
cd /workspace/reminder-batch-2026-11-11/item01/exercise
python3 lab.py 3
```
退出码：0
```text
{"changes": [{"key": "launcher", "new": "demo.home", "old": "vendor.home"}, {"key": "ad.demo", "new": false, "old": true}], "hardware": "待验证", "restored": true}

```

## 步骤 4
```sh
cd /workspace/reminder-batch-2026-11-11/item01/exercise
python3 lab.py 4
```
退出码：0
```text
{"claims": "只验证模拟控制值，不证明灯具/相机兼容", "invalid": "rejected", "scene": [{"brightness": 0}, {"brightness": 25}, {"brightness": 50}, {"brightness": 100}]}

```
