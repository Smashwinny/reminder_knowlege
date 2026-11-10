# 真实实验日志
重建时间：2026-11-11T01:05:29.868101+08:00（Asia/Shanghai）
因共享同名目录冲突，已在独立worker目录从公开证据与本worker源码重新执行。无模型API、用户密钥或私人资料。

## 1
```bash
cd /workspace/reminder-batch/worker-689b81da/item02
node exercise/lab.mjs extract
```
```text
Extracted upstream pure group: 5 it() tests; no tool/store tests selected.

```
退出码：0

## 2
```bash
cd /workspace/reminder-batch/worker-689b81da/item02
node exercise/lab.mjs manifest
```
```text
[
  {
    "path": "README.md",
    "bytes": 6084,
    "sha256": "1cbb4a7ce7b9be1515d993f6585c9ea9a4a87a6b80e935c0bcd5afc3b6b24b08"
  },
  {
    "path": "LICENSE",
    "bytes": 34523,
    "sha256": "0d96a4ff68ad6d4b6f1f30f713b18d5184912ba8dd389f86aa7710db079abcb0"
  },
  {
    "path": "package.json",
    "bytes": 3270,
    "sha256": "ed310c3d8deefb10f3ecbe0be880ccfb0d06e2db662906a3ceb254ba49b9da84"
  },
  {
    "path": "docs/architecture.md",
    "bytes": 19747,
    "sha256": "ac898e5b14067a1bf57b1e8918432be8b223b7081bd702cfe65fee93143919cf"
  },
  {
    "path": "docs/development.md",
    "bytes": 8893,
    "sha256": "0f5e7d0985d29d2b7583156e785ded2de7f0021a1ab725317d3e4ab9bfef0dbe"
  },
  {
    "path": "docs/teaching-methodology.md",
    "bytes": 10937,
    "sha256": "814b1e617abda7b389a9fa91923da41f72fa7fd6be0e91d1eac4443d5f8fe929"
  },
  {
    "path": "src/core/plan-tree.ts",
    "bytes": 5430,
    "sha256": "230121b62e2f5e76e22bd39044398b90fbd08679185a409ed9273b8f4e9bc9e8"
  },
  {
    "path": "src/agent/tools/mermaid-plan.ts",
    "bytes": 6653,
    "sha256": "c7ce84a7f0416f16995e33d894678e3325e7d476713b338dac998697e30016c7"
  },
  {
    "path": "tests/plan-tree.test.ts",
    "bytes": 18466,
    "sha256": "60e315b204af7e755107918173b258765cc41a1a9388c60713cfaceba301d291"
  }
]

```
退出码：0

## 3
```bash
cd /workspace/reminder-batch/worker-689b81da/item02
node --test exercise/upstream-pure.test.ts
```
```text
▶ plan-tree pure ops
  ✔ createTree builds version 1 with no mutation of its inputs (1.465192ms)
  ✔ createTree rejects duplicate node ids (0.272941ms)
  ✔ createTree rejects edges with missing endpoints (0.174751ms)
  ✔ createTree rejects self-loops, duplicates, and cycles (0.238553ms)
  ✔ createTree rejects invalid node shapes (0.618353ms)
✔ plan-tree pure ops (3.838463ms)
ℹ tests 5
ℹ suites 1
ℹ pass 5
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 110.792125

```
退出码：0

## 4
```bash
cd /workspace/reminder-batch/worker-689b81da/item02
node exercise/lab.mjs positive
```
```text
{
  "input": "合成的分数→比例→概率，不是模型或学习者数据",
  "tree": {
    "nodes": [
      {
        "id": "fractions",
        "title": "分数"
      },
      {
        "id": "ratio",
        "title": "比例"
      },
      {
        "id": "probability",
        "title": "概率"
      }
    ],
    "edges": [
      {
        "from": "fractions",
        "to": "ratio"
      },
      {
        "from": "ratio",
        "to": "probability"
      }
    ],
    "version": 1
  },
  "edgeMeaning": "from 必须先于 to 理解；仅结构，不证明知识已掌握"
}

```
退出码：0

## 5
```bash
cd /workspace/reminder-batch/worker-689b81da/item02
node exercise/lab.mjs negative
```
```text
[
  {
    "id": "cycle",
    "stage": "DAG",
    "error": "Edge \"b\" → \"a\" would create a cycle: \"a\" already leads (directly or transitively) back to \"b\". \"from\" must be understood before \"to\" — the tree is a DAG."
  },
  {
    "id": "invalid-slug",
    "stage": "parse",
    "problems": [
      "line 2: node id `Bad.id` must be a lowercase slug (a-z, 0-9, joined by hyphens or underscores — e.g. `chain-rule-intuition`); ids are permanent and checks reference them."
    ]
  },
  {
    "id": "missing-header",
    "stage": "parse",
    "problems": [
      "line 1: expected the header `graph TD` (or flowchart TD/TB) first, got `a --> b`."
    ]
  }
]

```
退出码：0

## 6
```bash
cd /workspace/reminder-batch/worker-689b81da/item02
node exercise/lab.mjs selftest
```
```text
PASS empty version zero
PASS parser deduplicates edges
PASS core rejects duplicate edges
PASS parser first label wins
PASS parser accepts underscore
PASS core alone accepts uppercase ids
PASS parser rejects uppercase ids
PASS output not linked to caller arrays
{
  "self_authored_checks": 8,
  "passed": 8,
  "scope": "原始纯模块；非UI、推理、教学效果或完整上游套件"
}

```
退出码：0

范围：item01设备矩阵8格全部待真机验证；item02选定上游5测试与自写8检查分别计数，未运行完整App/模型/GUI/持久化。
