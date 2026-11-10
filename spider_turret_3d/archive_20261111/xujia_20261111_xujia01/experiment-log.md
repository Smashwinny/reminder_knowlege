# 真实实验日志

时间：2026-11-11T01:00:37.984187+08:00（Asia/Shanghai）

范围：零 API 离线证据练习。不是 iOS 实机；不冒称设备启动或锁屏结论。


## manifest
```bash
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


## matrix
```bash
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


## negative
```bash
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


## test
```bash
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


## report
```bash
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


## 交付ZIP全新复现（已执行）
时间：2026-11-11 01:02:27起（Asia/Shanghai）。工作目录 `/workspace/reminder-batch/item01/qa/repro/exercise`。

ZIP解压：`python3 -m zipfile -e item01/exercise.zip item01/qa/repro`（根目录 `/workspace/reminder-batch`）。以下是真实重新下载、安装与四项运行输出，整链退出0：

```text
$ python3 fetch_sources.py
AnimationStateMachine.js b256d9b80aaf332feba67cd613ec7dc743f866059048a7b977d37123822d88e2
TurretController.js e4a9ec278280eb215a0a371608b3ec2b7a97deb9dc06d68bc991540caeb0c7d7
LegIKSolver.js 12eb292742b6c828a33b13dbafc0e02f3769d9ff190c7f3c4fc6c7acb3600d18
QuadrupedGaitController.js e64b7b006ac6818b263f35643c1a4c9ad10d0fcb0ed5c46d93015c5685b0dd53
tslMaterials.js c1cb30febc455795ddf399bf4e057e58b77fb1a6203cb09de2845cf49c3ece0e
GLB SHA256 verified
$ npm ci --ignore-scripts --no-audit --no-fund

added 1 package in 508ms
$ python3 asset_audit.py
{"bytes": 7719160, "sha256": "b3c28c34e609e430911207a9aaf3b2adef47b2893017503f01176482d833d22f", "generator": "Khronos glTF Blender I/O v4.2.83", "nodes": 340, "meshes": 282, "skins": 0, "animations": 0, "required_nodes": 24, "missing": []}
$ node lab.mjs states
{"state_cases":6,"state_at_speed9":"FIRING_ACTIVE","actual_trigger_at_speed9":false,"frames":[{"hz":20,"trigger_count_2s":33,"first_trigger_s":0.35,"heat_after_2s":1},{"hz":30,"trigger_count_2s":36,"first_trigger_s":0.3333333333333333,"heat_after_2s":1},{"hz":60,"trigger_count_2s":35,"first_trigger_s":0.3333333333333333,"heat_after_2s":1},{"hz":120,"trigger_count_2s":35,"first_trigger_s":0.325,"heat_after_2s":1}],"note":"UI threshold 8 differs from actual trigger threshold 10; Hz are synthetic timesteps, not measured FPS"}
$ node lab.mjs ik
{"reachable_samples":101,"max_fk_error":4.1540741810552243e-16,"unreachable_target_error":8.760841100617018,"angles_finite":true,"note":"synthetic hierarchy follows solver comments; not a loaded-GLB animation test"}
$ node lab.mjs gait
{"steps":600,"simulated_seconds":10,"stance_samples":1389,"swing_samples":1011,"max_target_plant_drift":0,"note":"target planting only, not actual solved mesh feet or physical balance"}
```

全部与初次结果一致；本次完整五步命令链已实际执行，不再仅靠等效准备。
