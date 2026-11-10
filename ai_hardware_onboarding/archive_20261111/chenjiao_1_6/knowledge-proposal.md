---
tags: [候选成果, 增量学习, 未合入]
created: 2026-11-11
---
# 第6项 knowledge proposal：AI辅助硬件入门：把验收写进每一步

## 查重与差异
固定main：a8674777e18302b8804b137212b1396cbfe5a747。已读00-总览及相关概念正文。总览未列本批七条原帖的专门项目记录；没有据此断言全仓库绝无重叠。
只补充现有规格书先行、护栏和证据优先概念的硬件学习实例；不把80%经验说法当量化结果，也不复制旧MCP基础概念。

## 建议追加的项目案例（待协调者审核）
来源：https://x.com/i/status/2112021182568632361；一手SHA见sources.md。

### 为什么第一步只读识别？
同名芯片可能对应不同Flash容量和板载外设。先定位真实设备和兼容固件，再备份，最后才考虑写入。本批没有USB设备，因此只执行文件层实验，不虚构串口和芯片检测输出。

### 损坏一个字节为什么要拒绝？
固件、资源和分区内容对字节敏感。练习把偏移100的一个字节翻转，哈希由c8f5…变成0f1b…，校验门输出REJECT。它演示完整性检测，不证明真实芯片会如何启动。

### 怎么结束一轮而不是无限折腾？
预先定义有限验收，例如指定文件大小、哈希一致、反例拒收、恢复相等，逐项保存日志。本批不勾选用户Reminder，不创建日程；文件实验结束后只把真实硬件环节标待验证，不谎称板子已完成。

## 建议互链，不新建同义概念
[[接缝与桩实现StubSeam]]、[[级联语音管线]]、[[证据优先质检ProofOverClaims]]、[[规格书先行SpecDriven]]。按实际概念选择落点，禁止把整个案例机械加到全部笔记。

## 本批状态
待验证：原经验帖与其引用长教程已读；合成文件备份、损坏拒收和恢复真实完成。没有真实板子识别、固件备份或烧录。

## 可复核结果
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

## 合入边界
仅为隔离候选提案，没有合入共享vault、改变网站标签、勾选Reminder或Git发布。自检不是独立审核；待协调者复核。
