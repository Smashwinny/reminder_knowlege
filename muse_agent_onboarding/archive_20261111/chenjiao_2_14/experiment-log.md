# 云端 Agent 上手：提示词、权限、验收分别写 · 实验日志

运行时间：2026-11-11 01:29:55 北京时间 UTC+8

范围：公开来源+合成夹具。自编实验不冒充上游实现；仅 item16 明确调用上游 runtime API。

## 步骤 1：保存九张合成用法卡
目的：保存九张合成用法卡

```bash
cd /workspace/chen-jiao-batch2-20261111/item14
python3 exercise/lab.py prepare
```
真实结果 exit=0：
```text
9 synthetic use cases saved; no service login

```
验证：tasks.json 明示合成、不访问账号

## 步骤 2：区分离线准备和待审批动作
目的：区分离线准备和待审批动作

```bash
cd /workspace/chen-jiao-batch2-20261111/item14
python3 exercise/lab.py classify
```
真实结果 exit=0：
```text
[('简报', 'allow-offline'), ('邮件分类', 'approval-required'), ('旅行备选', 'allow-offline'), ('订阅清单', 'allow-offline'), ('价格监控', 'approval-required'), ('文档总结', 'allow-offline'), ('社媒草稿', 'allow-offline'), ('研究报告', 'allow-offline'), ('目标追踪', 'approval-required')]

```
验证：归档与两类 schedule 共三项需审批

## 步骤 3：比较空泛与完整提示规格
目的：比较空泛与完整提示规格

```bash
cd /workspace/chen-jiao-batch2-20261111/item14
python3 exercise/lab.py lint
```
真实结果 exit=0：
```text
bad missing= ['inputs', 'scope', 'stop', 'done'] good missing= []

```
验证：差例缺四栏，好例五栏齐全

## 步骤 4：保持外部文本为数据
目的：保持外部文本为数据

```bash
cd /workspace/chen-jiao-batch2-20261111/item14
python3 exercise/lab.py injection
```
真实结果 exit=0：
```text
external text kept as DATA; actions= ['read', 'draft'] sent=0 (deterministic fixture, not LLM robustness test)

```
验证：计划仅 read/draft，发送计数零

## 未验证边界
待验证：产品实际账号、权限、设置路径、训练开关当前值、下载/收入宣传、真实代理表现。未登录、注册、建队列、发送或改设置。
