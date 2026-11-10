# Agent 不是员工人设，而是可撤销授权的岗位 · 实验日志

运行时间：2026-11-11 01:29:55 北京时间 UTC+8

范围：公开来源+合成夹具。自编实验不冒充上游实现；仅 item16 明确调用上游 runtime API。

## 步骤 1：填写岗位五栏
目的：填写岗位五栏

```bash
cd /workspace/chen-jiao-batch2-20261111/item09
python3 exercise/lab.py prepare
```
真实结果 exit=0：
```text
{"owns": "公开资料对比报告", "inputs": ["三条公开资料"], "may": ["read", "draft"], "must_ask": ["send", "delete"], "done": ["来源齐全", "缺口明确"]}

```
验证：读取 role.json，检查 may 与 must_ask 分开

## 步骤 2：检查动作白名单
目的：检查动作白名单

```bash
cd /workspace/chen-jiao-batch2-20261111/item09
python3 exercise/lab.py gate
```
真实结果 exit=0：
```text
{'read': 'allow', 'draft': 'allow', 'send': 'park', 'delete': 'park', 'unknown': 'park'}

```
验证：read/draft 放行，send/delete/unknown 暂停

## 步骤 3：模拟精确绑定与一次性消费
目的：模拟精确绑定与一次性消费

```bash
cd /workspace/chen-jiao-batch2-20261111/item09
python3 exercise/lab.py binding
```
真实结果 exit=0：
```text
changed_parameters=rejected replay=rejected; external_sent=0 (local token simulation only)

```
验证：更改正文、重放原批准均被拒；实际发送为零

## 步骤 4：检查晋级必要条件
目的：检查晋级必要条件

```bash
cd /workspace/chen-jiao-batch2-20261111/item09
python3 exercise/lab.py probation
```
真实结果 exit=0：
```text
5 clean + rollback => eligible; failure/no rollback => denied; 0.8^5= 0.3276800000000001

```
验证：缺回滚证据或最近五次含失败不能晋级

## 未验证边界
待验证：真实 Agent 行为、模型随机性、身份认证、数据库原子审批、跨进程竞争和实际回滚。脚本不是平台权限系统。
