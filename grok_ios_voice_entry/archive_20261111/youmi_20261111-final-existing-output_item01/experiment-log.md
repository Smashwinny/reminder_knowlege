# 真实实验日志
重建时间：2026-11-11T01:05:29.657269+08:00（Asia/Shanghai）
因共享同名目录冲突，已在独立worker目录从公开证据与本worker源码重新执行。无模型API、用户密钥或私人资料。

## 1
```bash
cd /workspace/reminder-batch/worker-689b81da/item01
python3 exercise/voice_entry_lab.py manifest
```
```text
[
  {
    "file": "source-post-raw.txt",
    "bytes": 5405,
    "sha256": "06ba9679ce0b96c025f551cf91a533312f50b57e148828e045043935754fa450"
  },
  {
    "file": "apple-vocal.html",
    "bytes": 1451091,
    "sha256": "7edffb40ed061aaeb1395595248fea4fda79fd51a5e71317a3950e85e46fc61f"
  },
  {
    "file": "apple-shortcuts.html",
    "bytes": 644106,
    "sha256": "3ef2709667960caf877f53fc45cb43a45b2bc24984f9b1accc64c9031440e6b8"
  }
]

```
退出码：0

## 2
```bash
cd /workspace/reminder-batch/worker-689b81da/item01
python3 exercise/voice_entry_lab.py matrix
```
```text
[
  {
    "case": 1,
    "lock": "unlocked",
    "noise": "quiet",
    "network": "online",
    "trigger_observed": null,
    "app_open_observed": null,
    "reply_observed": null,
    "latency_ms": null,
    "status": "待真机验证"
  },
  {
    "case": 2,
    "lock": "unlocked",
    "noise": "quiet",
    "network": "offline",
    "trigger_observed": null,
    "app_open_observed": null,
    "reply_observed": null,
    "latency_ms": null,
    "status": "待真机验证"
  },
  {
    "case": 3,
    "lock": "unlocked",
    "noise": "noisy",
    "network": "online",
    "trigger_observed": null,
    "app_open_observed": null,
    "reply_observed": null,
    "latency_ms": null,
    "status": "待真机验证"
  },
  {
    "case": 4,
    "lock": "unlocked",
    "noise": "noisy",
    "network": "offline",
    "trigger_observed": null,
    "app_open_observed": null,
    "reply_observed": null,
    "latency_ms": null,
    "status": "待真机验证"
  },
  {
    "case": 5,
    "lock": "locked",
    "noise": "quiet",
    "network": "online",
    "trigger_observed": null,
    "app_open_observed": null,
    "reply_observed": null,
    "latency_ms": null,
    "status": "待真机验证"
  },
  {
    "case": 6,
    "lock": "locked",
    "noise": "quiet",
    "network": "offline",
    "trigger_observed": null,
    "app_open_observed": null,
    "reply_observed": null,
    "latency_ms": null,
    "status": "待真机验证"
  },
  {
    "case": 7,
    "lock": "locked",
    "noise": "noisy",
    "network": "online",
    "trigger_observed": null,
    "app_open_observed": null,
    "reply_observed": null,
    "latency_ms": null,
    "status": "待真机验证"
  },
  {
    "case": 8,
    "lock": "locked",
    "noise": "noisy",
    "network": "offline",
    "trigger_observed": null,
    "app_open_observed": null,
    "reply_observed": null,
    "latency_ms": null,
    "status": "待真机验证"
  }
]

```
退出码：0

## 3
```bash
cd /workspace/reminder-batch/worker-689b81da/item01
python3 exercise/voice_entry_lab.py negative
```
```text
{
  "synthetic_input": [
    {
      "case": 1,
      "status": "真实完成",
      "trigger_observed": true,
      "app_open_observed": true,
      "reply_observed": null
    }
  ],
  "rejected_cases": [
    1
  ],
  "meaning": "检测到缺少语音回复证据；不是设备故障实测"
}

```
退出码：0

## 4
```bash
cd /workspace/reminder-batch/worker-689b81da/item01
python3 exercise/voice_entry_lab.py test
```
```text
test_complete (__main__.Tests.test_complete) ... ok
test_false_success (__main__.Tests.test_false_success) ... ok
test_partial (__main__.Tests.test_partial) ... ok
test_pending (__main__.Tests.test_pending) ... ok
test_zero_not_missing (__main__.Tests.test_zero_not_missing) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK

```
退出码：0

## 5
```bash
cd /workspace/reminder-batch/worker-689b81da/item01
python3 exercise/voice_entry_lab.py report
```
```text
{
  "matrix_cases": 8,
  "measured_device_cases": 0,
  "pending_device_cases": 8,
  "false_success_in_matrix": [],
  "cloud_scope": "来源指纹、试验设计、证据护栏；未操作iPhone"
}

```
退出码：0

范围：item01设备矩阵8格全部待真机验证；item02选定上游5测试与自写8检查分别计数，未运行完整App/模型/GUI/持久化。
