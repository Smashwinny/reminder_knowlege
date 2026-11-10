# 真实实验日志：DSH 实用插件挑选
2026-11-11，全部时间 Asia/Shanghai UTC+8。自写夹具直接调用固定上游实现；不是上游全测试套件，也不是独立审核。下载源码为准备阶段，以下六步离线执行，不安装依赖或宿主。
## 1 固定身份与文件指纹

时间：2026-11-11T01:05:07.881476+08:00（Asia/Shanghai UTC+8）
工作目录：`/workspace/reminder-batch/item-4-dsh-plugin-picks/exercise`

```bash
python3 identity.py
```

真实输出：
```text
SiriLee/dsh-rewind f5668ded87eb5c230916e288f26a887c633b4154 dsh-rewind-plugin@0.21.2
Han-1413141/dsh-cost-meter c876735d80760fc89d88fa99c19c90c56e984c23 dsh-cost-meter@1.9.64
MichengAI/dsh-code-review 89cc7166972e4d3c8bf482ee505d8d58c106fa13 @michengai/dsh-code-review@1.0.10
f-e-n-g-0531/dsh-code-review 0d3f6b03f9080153cc01fb8b75a79ddcbcae86d4 @feng0531/dsh-code-review@0.92.3
tt-a1i/archify 7e45f36c66de1254d5ad6ba1d878f6499ea269fd @tt-a1i/archify-dsh@1.1.0
PASS: 5 repository identities; 21 unmodified upstream files hash-verified

```
退出码：0

## 2 四桶 Token 计费

时间：2026-11-11T01:05:07.905107+08:00（Asia/Shanghai UTC+8）
工作目录：`/workspace/reminder-batch/item-4-dsh-plugin-picks/exercise`

```bash
node --import ./network-guard.mjs buckets.mjs
```

真实输出：
```text
{"label":"four buckets","tokens":{"input":100000,"cacheRead":50000,"cacheWrite":10000,"output":20000},"got":0.415,"want":0.415}
{"label":"one million input","tokens":{"input":1000000},"got":2,"want":2}
{"label":"fallback write rate","tokens":{"cacheWrite":1000000},"got":0.5,"want":0.5}
{"label":"invalid token amounts","tokens":{"input":-2,"output":null,"cacheRead":null},"got":0,"want":0}
PASS: 4 synthetic cost scenarios; network attempts=0; rates are fixtures, not market prices

```
退出码：0

## 3 长上下文边界与聚合反例

时间：2026-11-11T01:05:07.983499+08:00（Asia/Shanghai UTC+8）
工作目录：`/workspace/reminder-batch/item-4-dsh-plugin-picks/exercise`

```bash
node --import ./network-guard.mjs threshold.mjs
```

真实输出：
```text
{"label":"exactly threshold","got":0.4,"want":0.4}
{"label":"one above","got":0.800004,"want":0.800004}
{"label":"cache participates","got":0.600002,"want":0.600002}
{"label":"output excluded from threshold","got":2.400002,"want":2.400002}
{"counterexample":"sum two per-call charges, not aggregate tokens then charge","separate":0.5,"aggregated":1}
PASS: 4 boundaries + aggregation counterexample; network attempts=0

```
退出码：0

## 4 币种倍率与未知价格

时间：2026-11-11T01:05:08.049051+08:00（Asia/Shanghai UTC+8）
工作目录：`/workspace/reminder-batch/item-4-dsh-plugin-picks/exercise`

```bash
node --import ./network-guard.mjs currency.mjs
```

真实输出：
```text
multiplier: raw input=2; factor=.8; effective cost=1.6; renormalize unchanged
currency: synthetic CNY 7.2 -> USD 1 -> display ¥7.2
unknown price: {} -> null; explicit unpriced retained (not evidence of free use)
negative/infinite/string multipliers rejected; explicit factor=0 computes 0
PASS: multiplier/currency/unknown validation; network attempts=0; not a bill or quota test

```
退出码：0

## 5 回退快照格式与拒绝分支

时间：2026-11-11T01:05:08.118629+08:00（Asia/Shanghai UTC+8）
工作目录：`/workspace/reminder-batch/item-4-dsh-plugin-picks/exercise`

```bash
node --import ./network-guard.mjs --experimental-transform-types rewind-format.mjs
```

真实输出：
```text
{"label":"session-dot","got":"session","want":"session"}
{"label":"session-slashes","got":".._x","want":".._x"}
{"label":"link-valid","got":true,"want":true}
{"label":"link-traversal","got":false,"want":false}
{"label":"link-absolute","got":false,"want":false}
{"label":"backup-valid","got":true,"want":true}
{"label":"rescue-valid","got":true,"want":true}
{"label":"backup-traversal","got":false,"want":false}
{"label":"backup-backslash","got":false,"want":false}
{"label":"plain-utf8","got":"text","want":"text"}
{"label":"lossy-utf8","got":"lossyText","want":"lossyText"}
(node:160089) ExperimentalWarning: Transform Types is an experimental feature and might change at any time
(Use `node --trace-warnings ...` to show where the warning was created)
future store=99: UnknownStoreVersionError (fail closed)
corrupt JSON: undefined (not guessed into a delete)
inconsistent absent-file marker with size=2: rejected
PASS: 11 validators/byte classifications + 3 codec cases; network attempts=0; no real restore

```
退出码：0

## 6 审查模型发送授权门

时间：2026-11-11T01:05:08.265870+08:00（Asia/Shanghai UTC+8）
工作目录：`/workspace/reminder-batch/item-4-dsh-plugin-picks/exercise`

```bash
node --import ./network-guard.mjs approval.mjs
```

真实输出：
```text
allowed-once -> accepted
{"result":"rejected","accepted":false}
{"result":"cancelled","accepted":false}
{"result":"unavailable","accepted":false}
{"result":true,"accepted":false}
{"result":"<undefined>","accepted":false}
missing approval service -> rejected
PASS: 7 mock-host approval outcomes; network attempts=0; not real host authorization or code review

```
退出码：0

## 准备阶段失败（未隐藏）
首次依赖扫描正则误匹配注释中的 from 字样，manifest未生成，正式首步退出1；原样保留 evidence/experiment-first-failure.md。改成只匹配 import 行后，复制21文件，六步重新执行全部退出0。此日志上方为成功复跑真实输出。

## 目的与验证
1. 固定身份与字节：五候选、21文件哈希校验成功。
2. 四桶费用：0.415/2/0.5/0四样例；Infinity/NaN经JSON展示为null，脚本传入保留真实非有限值。
3. 跨档边界：200000基础，200001长上下文；先按请求计费0.5，误聚合得到1。
4. 倍率/币种/未知：重规范化不复乘、人工汇率换算，未知不作免费承诺。
5. 快照格式：11验证/字节分类+3编解码案例通过；只写练习JSON，不做恢复。
6. 模拟授权门：7结果符合预期，无真实模型调用。
五个JS进程网络尝试均0（进程内guard，非OS隔离）。完整目的/边界亦在HTML实验页。
