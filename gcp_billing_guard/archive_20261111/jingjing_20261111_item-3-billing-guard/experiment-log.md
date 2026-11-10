# GCP 预算熔断：90%不是费用硬上限 · 真实实验日志

执行时间：2026-11-11 01:07:46 CST（UTC+8）

只读公共研究＋云端隔离实验。自编程序不是上游实现，除明确标出的官方构建。

## 固定8种预算消息
目的：创建正常、临界、dryRun和畸形字段场景

```bash
cd /workspace/reminder-batch-2026-11-11/item-3-billing-guard
node exercise/mock.mjs fixture
```

真实输出（exit=0）：
```text
8 synthetic payloads written; no credentials, SDK or network

```
验证：没有用户项目ID、SDK凭据和网络调用

## 真实函数接入内存桩
目的：只替换SDK与export入口后执行固定版本函数

```bash
cd /workspace/reminder-batch-2026-11-11/item-3-billing-guard
node exercise/mock.mjs run
```

真实输出（exit=0）：
```text
[
  {
    "name": "below",
    "get": 0,
    "unlink_stub": 0
  },
  {
    "name": "at90",
    "get": 1,
    "unlink_stub": 1
  },
  {
    "name": "threshold",
    "get": 1,
    "unlink_stub": 1
  },
  {
    "name": "dry",
    "get": 1,
    "unlink_stub": 0
  },
  {
    "name": "bad-number",
    "get": 1,
    "unlink_stub": 1
  },
  {
    "name": "string-false-force",
    "get": 1,
    "unlink_stub": 1
  },
  {
    "name": "already-off",
    "get": 1,
    "unlink_stub": 0
  },
  {
    "name": "missing-budget",
    "get": 0,
    "unlink_stub": 0
  }
]

```
验证：below/dry/已关闭没有update；异常场景结果不掩盖

## 特征化断言
目的：按实际源码语义检查8个场景，包含不安全反例

```bash
cd /workspace/reminder-batch-2026-11-11/item-3-billing-guard
node exercise/mock.mjs verify
```

真实输出（exit=0）：
```text
PASS 8 upstream-characterisation checks. Two unsafe synthetic inputs trigger unlink STUB: NaN cost and string forceKill=false. This is a finding, not safety validation.

```
验证：错误字段触发桩解绑必须被报告为发现

## 扫描延迟穿透
目的：计算0/0.5/1/24小时延迟下的合成总费用

```bash
cd /workspace/reminder-batch-2026-11-11/item-3-billing-guard
node exercise/mock.mjs delay
```

真实输出（exit=0）：
```text
{"synthetic":true,"budget":10,"delay_hours":0,"rate_per_hour":2,"cost_when_action":9,"overshoot":0}
{"synthetic":true,"budget":10,"delay_hours":0.5,"rate_per_hour":2,"cost_when_action":10,"overshoot":0}
{"synthetic":true,"budget":10,"delay_hours":1,"rate_per_hour":2,"cost_when_action":11,"overshoot":1}
{"synthetic":true,"budget":10,"delay_hours":24,"rate_per_hour":2,"cost_when_action":57,"overshoot":47}
real Billing/Cloud Run/PubSub/IAM calls = 0

```
验证：B=10,r=2,阈值0.9；原始数值见日志


## 未验证边界
未登录GCP、未查用户抵免/订阅、未部署Pub/Sub/Cloud Run/IAM、未解绑或恢复结算、未调用任何收费模型；真实延迟、失效恢复与超额金额待验证。
