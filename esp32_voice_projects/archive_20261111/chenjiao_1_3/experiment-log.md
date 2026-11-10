# 第3项真实实验日志
执行时间：2026-11-11T00:58:16.493075+08:00 Asia/Shanghai
环境：Linux云电脑；全部为受控数据。

## 步骤 1
```sh
cd /workspace/reminder-batch-2026-11-11/item03/exercise
python3 lab.py 1
```
退出码：0
```text
{"layers": ["设备固件", "ASR/TTS网关", "Agent或模型"], "python": "3.13.5", "scope": "合成输入路由，不是上游网关集成"}

```

## 步骤 2
```sh
cd /workspace/reminder-batch-2026-11-11/item03/exercise
python3 lab.py 2
```
退出码：0
```text
{"device_isolation": true, "routes": [["A", "claude"], ["B", "deepseek"], ["A", "claude"], ["B", "deepseek"]]}

```

## 步骤 3
```sh
cd /workspace/reminder-batch-2026-11-11/item03/exercise
python3 lab.py 3
```
退出码：0
```text
{"persistence": "仅本地JSON正常写读；非崩溃一致性证明", "reloaded": {"A": "claude", "B": "deepseek"}, "unknown_alias_policy": "保留既有路由或默认，不执行未知命令"}

```

## 步骤 4
```sh
cd /workspace/reminder-batch-2026-11-11/item03/exercise
python3 lab.py 4
```
退出码：0
```text
{"played": false, "retry_submissions": 0, "states": ["accepted", "waiting", "timed_out", "reply_ready"], "warning": "超时不是取消，也不是可以重新派单的证据"}

```
