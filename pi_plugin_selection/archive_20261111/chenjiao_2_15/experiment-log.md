# Pi 五类插件：选能力，不按下载量闭眼装 · 实验日志

运行时间：2026-11-11 01:29:55 北京时间 UTC+8

范围：公开来源+合成夹具。自编实验不冒充上游实现；仅 item16 明确调用上游 runtime API。

## 步骤 1：核对真实 npm 元数据
目的：核对真实 npm 元数据

```bash
cd /workspace/chen-jiao-batch2-20261111/item15
python3 exercise/lab.py inventory
```
真实结果 exit=0：
```text
billion-context 0.1.213 133f3525c628c4b959bb79ece82af6df82e131a3
pi-mcp-adapter 7.0.1 0beff98460567cd228ae08d99db5f169a1ad3034
pi-subagents 0.87.0 52e68e9ef0e563d5c97b28519f9999f1b5fbbbea
pi-web-access 0.47.0 322e44fafc1aaa691779cdf2116584e67edd7645
scoped-question 2.15.0 ce6d3530410812ca504ec294995581a52170f9e1

```
验证：输出五包版本及 gitHead

## 步骤 2：比较合成目录与代理字节
目的：比较合成目录与代理字节

```bash
cd /workspace/chen-jiao-batch2-20261111/item15
python3 exercise/lab.py catalog
```
真实结果 exit=0：
```text
synthetic catalog bytes= 55890 proxy bytes= 71 ratio= 787.18
bytes NOT model tokens; lookup and result costs excluded

```
验证：明确字节不是 token，且未包含发现开销

## 步骤 3：检测摘要字段遗失
目的：检测摘要字段遗失

```bash
cd /workspace/chen-jiao-batch2-20261111/item15
python3 exercise/lab.py compression
```
真实结果 exit=0：
```text
bad_summary=rejected good_summary=accepted; deterministic field retention, NOT plugin quality

```
验证：坏摘要拒绝，保留目标/禁止/未决的摘要通过

## 步骤 4：验证结构化追问模板
目的：验证结构化追问模板

```bash
cd /workspace/chen-jiao-batch2-20261111/item15
python3 exercise/lab.py question
```
真实结果 exit=0：
```text
{"question": "缺哪个输入？", "options": ["来源URL", "离线文件"], "other": true}
no UI invoked; plugins NOT installed; no real credentials read

```
验证：至少两个选项、允许其他；不实际调用 UI

## 未验证边界
待验证：五插件安装运行、真实 token、模型效果、子代理权限、压缩质量和 UI。未运行插件、读取密钥或改变 Pi 设置。
