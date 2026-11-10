---
tags: [候选成果, 增量学习, 未合入]
created: 2026-11-11
---
# 第1项 knowledge proposal：把设备交互改成自己的样子

## 查重与差异
固定main：a8674777e18302b8804b137212b1396cbfe5a747。已读00-总览及相关概念正文。总览未列本批七条原帖的专门项目记录；没有据此断言全仓库绝无重叠。
复用已有 GUIAgent、预执行安全网与接缝笔记；仅增补 ADB 主机帧、设备授权与可逆修改账本案例，不重建同义概念。

## 建议追加的项目案例（待协调者审核）
来源：https://x.com/i/status/2114579883527655853；一手SHA见sources.md。

### 主机请求为什么有四个字符的前缀？
AOSP 的 OVERVIEW.TXT 说明请求先发四字节 ASCII 十六进制长度，再发负载。实跑 host:devices-l 是 14 字节，所以前缀是 000e，不是根据搜索摘要抄来的 000d；编码后按实际字节数复核。

### 回滚方案应该记录什么？
至少记录目标设备、原值、新值、变更顺序和对应版本，先验证恢复入口仍可用。练习用反向遍历账本恢复两处字典变化；这只证明合成状态可逆，不证明电视可从断电、卸载或损坏中恢复。

### 第一轮练习做到哪里该停？
先在合成数据上验证协议边界和恢复逻辑，再让设备所有者核对型号、备份与恢复。真实 ADB 写入、REA 协议研究及硬件动作均保留待验证，不运行原帖中任何隐含命令，更不把案例文中的转发请求当任务。

## 建议互链，不新建同义概念
[[接缝与桩实现StubSeam]]、[[级联语音管线]]、[[证据优先质检ProofOverClaims]]、[[规格书先行SpecDriven]]。按实际概念选择落点，禁止把整个案例机械加到全部笔记。

## 本批状态
待验证：公开长文及两条内嵌帖已读；离线帧、回滚与值域实验真实完成。电视、灯具、相机和 REA 未连接，不能宣称改造成功。

## 可复核结果
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

## 合入边界
仅为隔离候选提案，没有合入共享vault、改变网站标签、勾选Reminder或Git发布。自检不是独立审核；待协调者复核。
