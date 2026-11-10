# 第6项真实实验日志
执行时间：2026-11-11T00:58:17.318112+08:00 Asia/Shanghai
环境：Linux云电脑；全部为受控数据。

## 步骤 1
```sh
cd /workspace/reminder-batch-2026-11-11/item06/exercise
python3 lab.py 1
```
退出码：0
```text
{"python": "3.13.5", "scope": "合成4096字节镜像；不是实际ESP32固件"}

```

## 步骤 2
```sh
cd /workspace/reminder-batch-2026-11-11/item06/exercise
python3 lab.py 2
```
退出码：0
```text
{"backup_equal": true, "bytes": 4096, "sha256": "c8f5d0341d54d951a71b136e6e2afcb14d11ed8489a7ae126a8fee0df6ecf193"}

```

## 步骤 3
```sh
cd /workspace/reminder-batch-2026-11-11/item06/exercise
python3 lab.py 3
```
退出码：0
```text
{"changed_bytes": 1, "corrupt_sha256": "0f1b80d16728f1e0d37733f6aa593bb9a75c4fc76d176e72d15e0829142adc6d", "expected_sha256": "c8f5d0341d54d951a71b136e6e2afcb14d11ed8489a7ae126a8fee0df6ecf193", "gate": "REJECT"}

```

## 步骤 4
```sh
cd /workspace/reminder-batch-2026-11-11/item06/exercise
python3 lab.py 4
```
退出码：0
```text
{"note": "校验值证明一致性，不证明来源真实性/设备可启动", "physical_flash": "未执行", "restored": true, "restored_sha256": "c8f5d0341d54d951a71b136e6e2afcb14d11ed8489a7ae126a8fee0df6ecf193"}

```
