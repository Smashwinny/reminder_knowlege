# 第二大脑离线实验日志
2026-11-11（Asia/Shanghai）。Python3.13标准库，自写确定性模型，3份合成JSON；无LLM、无真实Bot、无routine、无账户资料。
半成品核验见../REUSE-AUDIT.md。解析缓存包装首次失败，改读取第3行JSON后成功。原帖引用AI教育长文已实读但与主题不同，不用于支持第二大脑。

## 1
```bash
cd /workspace/reminder-batch/worker-689b81da/item05
python3 exercise/brain_lab.py setup
```
```text
{
  "root": "/workspace/reminder-batch/worker-689b81da/item05/scratch/brain",
  "directories": [
    "raw",
    "wiki",
    "out"
  ],
  "rules": "2026-11-11｜单主题HTTP缓存；事实需来源；外发不执行；检查只报告。\n",
  "real_bots_created": 0,
  "routines_created": 0
}

```
exit=0

## 2
```bash
cd /workspace/reminder-batch/worker-689b81da/item05
python3 exercise/brain_lab.py collect
```
```text
[
  {
    "name": 1,
    "sha256": "e67cbaf9ec90e41122a13a4e1ebf14f110c023f409e1ab41c35669d860bfc603",
    "status": "written"
  },
  {
    "name": 2,
    "sha256": "db315475fe53fd1cbfc127095e4ceef8c23df0ab1b0dc640d43df4b397b1624f",
    "status": "written"
  },
  {
    "name": 3,
    "sha256": "9967333d233bf4bf30052e67e65fa2b10bb6dc617e8c76381d6327c7cbbde51e",
    "status": "written"
  }
]

```
exit=0

## 3
```bash
cd /workspace/reminder-batch/worker-689b81da/item05
python3 exercise/brain_lab.py compile
```
```text
{
  "fact_count": 2,
  "guess_count": 1,
  "raw_unchanged": true,
  "wiki_pages": 3
}

```
exit=0

## 4
```bash
cd /workspace/reminder-batch/worker-689b81da/item05
python3 exercise/brain_lab.py check
```
```text
{
  "conflicts": {
    "ttl": [
      "120",
      "60"
    ]
  },
  "stale": [
    {
      "page": "cache",
      "source": "raw/source1.json",
      "state": "未确认"
    }
  ],
  "orphans": [
    "orphan"
  ],
  "wiki_unchanged": true
}

```
exit=0

## 5
```bash
cd /workspace/reminder-batch/worker-689b81da/item05
python3 exercise/brain_lab.py boundaries
```
```text
{
  "compile_denied": [
    "reader",
    "checker"
  ],
  "duplicate_rejected": true,
  "raw1_unchanged": true,
  "external_without_approval": {
    "send": "blocked:explicit approval required",
    "buy": "blocked:explicit approval required",
    "delete": "blocked:explicit approval required",
    "publish": "blocked:explicit approval required"
  },
  "external_with_approval_still_unsupported": "unsupported:no executor"
}

```
exit=0

## 6
```bash
cd /workspace/reminder-batch/worker-689b81da/item05
python3 exercise/brain_lab.py test
```
```text
test_bad_name (__main__.Tests.test_bad_name) ... ok
test_conflict (__main__.Tests.test_conflict) ... ok
test_duplicate (__main__.Tests.test_duplicate) ... ok
test_fact_guess (__main__.Tests.test_fact_guess) ... ok
test_librarian (__main__.Tests.test_librarian) ... ok
test_no_executor (__main__.Tests.test_no_executor) ... ok
test_no_send (__main__.Tests.test_no_send) ... ok
test_orphan (__main__.Tests.test_orphan) ... ok
test_raw_hash (__main__.Tests.test_raw_hash) ... ok
test_reader (__main__.Tests.test_reader) ... ok
test_readonly (__main__.Tests.test_readonly) ... ok
test_stale (__main__.Tests.test_stale) ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.010s

OK

```
exit=0