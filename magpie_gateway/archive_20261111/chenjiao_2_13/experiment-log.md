# Magpie 网关：协议统一不等于权限统一 · 实验日志

运行时间：2026-11-11 01:29:55 北京时间 UTC+8

范围：公开来源+合成夹具。自编实验不冒充上游实现；仅 item16 明确调用上游 runtime API。

## 步骤 1：冻结无密钥 mock 配置
目的：冻结无密钥 mock 配置

```bash
cd /workspace/chen-jiao-batch2-20261111/item13
python3 exercise/lab.py prepare
```
真实结果 exit=0：
```text
{'bind': '127.0.0.1', 'upstreams': ['local-429', 'local-ok'], 'real_keys': False}

```
验证：监听只在 127.0.0.1，真实密钥为 false

## 步骤 2：真实本地 HTTP 429 后切换
目的：真实本地 HTTP 429 后切换

```bash
cd /workspace/chen-jiao-batch2-20261111/item13
python3 exercise/lab.py failover
```
真实结果 exit=0：
```text
attempts= [429, 200] counts= {'bad': 1, 'good': 1}

```
验证：最多两次，结果 [429,200]

## 步骤 3：真实本地 HTTP 401 后停止
目的：真实本地 HTTP 401 后停止

```bash
cd /workspace/chen-jiao-batch2-20261111/item13
python3 exercise/lab.py auth
```
真实结果 exit=0：
```text
attempts= [401] counts= {'bad': 1, 'good': 0}

```
验证：仅一次尝试，good 桩计数为零

## 步骤 4：模拟合成预算预留
目的：模拟合成预算预留

```bash
cd /workspace/chen-jiao-batch2-20261111/item13
python3 exercise/lab.py budget
```
真实结果 exit=0：
```text
synthetic reservations= [True, True, False] reserved_tokens= 90 external_requests=0; NOT Magpie execution

```
验证：40/50 放行，30 拒绝，总预留 90

## 未验证边界
待验证：Magpie 编译、运行、订阅/模型、协议转换、流式、真实预算和 Web 权限。没有启动 Magpie、读取凭据、改 Agent 配置或改收费/安全设置。
