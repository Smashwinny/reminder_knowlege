# 第6项实际实验日志
2026-11-11（Asia/Shanghai）；node24.22.1，TypeScript5.9.3，Python3.13.5。
command -v tsc未找到预装编译器；安装：npm install --prefix /workspace/reminder-batch/worker-689b81da/item06/exercise --ignore-scripts --no-audit --no-fund typescript@5.9.3
真实输出：added 1 package in 532ms。未安装pstack。

## 1
```bash
cd /workspace/reminder-batch/worker-689b81da/item06
python3 exercise/guard_lab.py legacy
```
```text
{
  "compiler": {
    "command": [
      "node",
      "/workspace/reminder-batch/worker-689b81da/item06/exercise/node_modules/typescript/bin/tsc",
      "--strict",
      "--target",
      "ES2022",
      "--module",
      "commonjs",
      "--outDir",
      "/workspace/reminder-batch/worker-689b81da/item06/results/compiled",
      "legacy.ts"
    ],
    "exit": 0,
    "stdout": "",
    "stderr": ""
  },
  "runtime": {
    "command": [
      "node",
      "/workspace/reminder-batch/worker-689b81da/item06/results/compiled/legacy.js"
    ],
    "exit": 0,
    "stdout": "{\"approved\":false,\"sent\":true}\n",
    "stderr": ""
  },
  "meaning": "逻辑非法组合在宽松结构里可编译，负对照"
}

```
runner exit=0

## 2
```bash
cd /workspace/reminder-batch/worker-689b81da/item06
python3 exercise/guard_lab.py types
```
```text
{
  "fixed": {
    "command": [
      "node",
      "/workspace/reminder-batch/worker-689b81da/item06/exercise/node_modules/typescript/bin/tsc",
      "--strict",
      "--target",
      "ES2022",
      "--module",
      "commonjs",
      "--noEmit",
      "fixed.ts"
    ],
    "exit": 0,
    "stdout": "",
    "stderr": ""
  },
  "negative_expected_failure": {
    "command": [
      "node",
      "/workspace/reminder-batch/worker-689b81da/item06/exercise/node_modules/typescript/bin/tsc",
      "--strict",
      "--target",
      "ES2022",
      "--module",
      "commonjs",
      "--noEmit",
      "negative.ts"
    ],
    "exit": 2,
    "stdout": "negative.ts(3,17): error TS2345: Argument of type 'Draft' is not assignable to parameter of type 'Approved'.\n  Property 'approvalId' is missing in type 'Draft' but required in type 'Approved'.\n",
    "stderr": ""
  }
}

```
runner exit=0

## 3
```bash
cd /workspace/reminder-batch/worker-689b81da/item06
python3 exercise/guard_lab.py runtime
```
```text
{
  "run": {
    "command": [
      "node",
      "/workspace/reminder-batch/worker-689b81da/item06/results/compiled/fixed.js"
    ],
    "exit": 0,
    "stdout": "{\"synthetic_only\":true,\"accepted\":1,\"rejected\":3,\"receipt\":{\"kind\":\"sent\",\"text\":\"hello\",\"approvalId\":\"fixture-consent\"}}\n",
    "stderr": ""
  },
  "mutant_compiler": {
    "command": [
      "node",
      "/workspace/reminder-batch/worker-689b81da/item06/exercise/node_modules/typescript/bin/tsc",
      "--strict",
      "--target",
      "ES2022",
      "--module",
      "commonjs",
      "--noEmit",
      "mutant.ts"
    ],
    "exit": 0,
    "stdout": "",
    "stderr": ""
  },
  "local_static_scan_mutant_rejected": true,
  "fixed_scan_rejected": false,
  "note": "静态扫描为自写单规则，不称ESLint；receipt完全合成无transport"
}

```
runner exit=0

## 4
```bash
cd /workspace/reminder-batch/worker-689b81da/item06
python3 exercise/guard_lab.py unsafe
```
```text
{
  "safe_model": false,
  "states": 6,
  "states_and_shortest_paths": [
    {
      "approved": false,
      "delivered": 0,
      "trace": []
    },
    {
      "approved": true,
      "delivered": 0,
      "trace": [
        "approve"
      ]
    },
    {
      "approved": false,
      "delivered": 1,
      "trace": [
        "send"
      ]
    },
    {
      "approved": true,
      "delivered": 1,
      "trace": [
        "approve",
        "send"
      ]
    },
    {
      "approved": false,
      "delivered": 2,
      "trace": [
        "send",
        "send"
      ]
    },
    {
      "approved": true,
      "delivered": 2,
      "trace": [
        "approve",
        "send",
        "send"
      ]
    }
  ],
  "violations": [
    {
      "state": [
        false,
        1
      ],
      "trace": [
        "send"
      ]
    },
    {
      "state": [
        false,
        2
      ],
      "trace": [
        "send",
        "send"
      ]
    },
    {
      "state": [
        true,
        2
      ],
      "trace": [
        "approve",
        "send",
        "send"
      ]
    }
  ],
  "bound": "count<=2, no revocation/crash/network/real approval"
}

```
runner exit=0

## 5
```bash
cd /workspace/reminder-batch/worker-689b81da/item06
python3 exercise/guard_lab.py guarded
```
```text
{
  "safe_model": true,
  "states": 3,
  "states_and_shortest_paths": [
    {
      "approved": false,
      "delivered": 0,
      "trace": []
    },
    {
      "approved": true,
      "delivered": 0,
      "trace": [
        "approve"
      ]
    },
    {
      "approved": true,
      "delivered": 1,
      "trace": [
        "approve",
        "send"
      ]
    }
  ],
  "violations": [],
  "bound": "count<=2, no revocation/crash/network/real approval"
}

```
runner exit=0

## 6
```bash
cd /workspace/reminder-batch/worker-689b81da/item06
python3 exercise/guard_lab.py test
```
```text
test_any_lint (__main__.Tests.test_any_lint) ... ok
test_bad_states (__main__.Tests.test_bad_states) ... ok
test_double_send (__main__.Tests.test_double_send) ... ok
test_good_states (__main__.Tests.test_good_states) ... ok
test_no_double_safe (__main__.Tests.test_no_double_safe) ... ok
test_no_early_safe (__main__.Tests.test_no_early_safe) ... ok
test_no_good_violation (__main__.Tests.test_no_good_violation) ... ok
test_plain (__main__.Tests.test_plain) ... ok
test_real_fixed (__main__.Tests.test_real_fixed) ... ok
test_real_mutant (__main__.Tests.test_real_mutant) ... ok
test_shortest (__main__.Tests.test_shortest) ... ok
test_version_pin (__main__.Tests.test_version_pin) ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.001s

OK

```
runner exit=0

negative.ts预期编译退出2，不是修正后代码失败；TS2345证明类型边界。mutant使用as any仍能编译，说明类型可被断言绕过，自写规则扫描仅捕捉特定语法，非全面安全证明。有限模型枚举不是TLA+/TLC或全程序证明。
没有执行帖子里的安装/Slack/recall/历史挖掘/创建Project/合并代码等指令。
