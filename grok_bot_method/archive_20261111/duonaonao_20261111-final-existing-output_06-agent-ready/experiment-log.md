# 真实实验日志

执行环境：Linux云电脑，Python标准库；2026-11-11T01:13:53+08:00（北京时间）。
本地基线SHA：`c35c8c30c6fa157284d7dce3a70bbc3b7ad85006`。没有remote，没有push，没有真实merge。

## 复跑
将exercise.zip解压到全新目录（不要覆盖已有runs），执行：
```sh
unzip exercise.zip -d /tmp/agent-ready-lab
cd /tmp/agent-ready-lab
python3 lab.py 1
python3 lab.py 2
python3 lab.py 3
python3 lab.py 4
python3 lab.py 5
```

## 首轮失败保留
首轮第4步预期红灯实际全绿，断言失败，未把它当完成。根因：复制基线含pyc；短时间等长源改动复用了旧字节码。修复复制时ignore __pycache__/*.pyc，改用runs-v2全新目录，完整五步重新执行。不是模型能力实测，也不是安全审计。

## 第1步 初始化可信基线
目的：生成 AGENTS.md、纯函数、3条测试、lint、ci.sh、GitHub workflow，创建无remote的本地Git仓库。
命令：`cd /workspace/learn-batch/06-agent-ready/exercise && python3 lab.py 1`
真实结果：BASE_SHA=c35c8c30c6fa157284d7dce3a70bbc3b7ad85006；git remote -v 无输出。
验证：git rev-parse HEAD；检查 AGENTS.md 与 tests/、tools/、.github/ 都已提交。

```text
$ git init -b main
Initialized empty Git repository in /workspace/learn-batch/06-agent-ready/exercise/runs-v2/base/.git/
exit_code=0
$ git config user.name Local educational fixture
exit_code=0
$ git config user.email fixture@example.invalid
exit_code=0
$ git add .
exit_code=0
$ git commit -m baseline contract, tests and CI
[main (root-commit) c35c8c3] baseline contract, tests and CI
 8 files changed, 56 insertions(+)
 create mode 100644 .github/workflows/ci.yml
 create mode 100644 .gitignore
 create mode 100644 AGENTS.md
 create mode 100644 ci.sh
 create mode 100644 docs/architecture.md
 create mode 100644 src/calc.py
 create mode 100644 tests/test_calc.py
 create mode 100644 tools/lint.py
exit_code=0
BASE_SHA=c35c8c30c6fa157284d7dce3a70bbc3b7ad85006
$ git remote -v
exit_code=0

```

## 第2步 执行质量基线
目的：真实运行unittest和自定义AST/空白lint；再运行相同ci.sh验证一键入口。
命令：`cd /workspace/learn-batch/06-agent-ready/exercise && python3 lab.py 2`
真实结果：Ran 3 tests；OK；lint_files=2, errors=[]；sh ci.sh退出0。
验证：baseline-ci.json中tests/lint都为true，sha与基线相等。

```text
$ /usr/bin/python3 -m unittest discover -s tests -v
test_negative (test_calc.TestCalc.test_negative) ... ok
test_positive (test_calc.TestCalc.test_positive) ... ok
test_zero (test_calc.TestCalc.test_zero) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
exit_code=0
$ /usr/bin/python3 /workspace/learn-batch/06-agent-ready/exercise/lab.py lint --repo /workspace/learn-batch/06-agent-ready/exercise/runs-v2/base
{"lint_files": 2, "errors": []}
exit_code=0
BASELINE_VALIDATED={"sha": "c35c8c30c6fa157284d7dce3a70bbc3b7ad85006", "checks": {"tests": true, "lint": true}}

```

## 第3步 通过样本不是直接合并
目的：从基线复制两个隔离仓库；提交合法文档与纯函数docstring改动，再实际跑检查。
命令：`cd /workspace/learn-batch/06-agent-ready/exercise && python3 lab.py 3`
真实结果：good-docs 和 good-code 均 eligible=true；merged=false。
验证：阅读两份JSON；代码样本reviewer仅合成夹具，非真实审阅。

```text
$ git add .
exit_code=0
$ git commit -m good-docs
[main bf2b76a] good-docs
 1 file changed, 2 insertions(+)
 create mode 100644 docs/usage.md
exit_code=0
$ /usr/bin/python3 -m unittest discover -s tests -v
test_negative (test_calc.TestCalc.test_negative) ... ok
test_positive (test_calc.TestCalc.test_positive) ... ok
test_zero (test_calc.TestCalc.test_zero) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
exit_code=0
$ /usr/bin/python3 /workspace/learn-batch/06-agent-ready/exercise/lab.py lint --repo /workspace/learn-batch/06-agent-ready/exercise/runs-v2/good-docs
{"lint_files": 2, "errors": []}
exit_code=0
RESULT={"scenario": "good-docs", "sha": "bf2b76ad66aeeb9021674ffdaf208dbc6b0b6054", "changed": ["docs/usage.md"], "eligible": true, "reasons": [], "review_is_synthetic": true, "merged": false}
$ git add .
exit_code=0
$ git commit -m good-code
[main 8af55c9] good-code
 1 file changed, 1 insertion(+)
exit_code=0
$ /usr/bin/python3 -m unittest discover -s tests -v
test_negative (test_calc.TestCalc.test_negative) ... ok
test_positive (test_calc.TestCalc.test_positive) ... ok
test_zero (test_calc.TestCalc.test_zero) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
exit_code=0
$ /usr/bin/python3 /workspace/learn-batch/06-agent-ready/exercise/lab.py lint --repo /workspace/learn-batch/06-agent-ready/exercise/runs-v2/good-code
{"lint_files": 2, "errors": []}
exit_code=0
RESULT={"scenario": "good-code", "sha": "8af55c9f902a2d58dbceb566f5bafddf6bcc34d9", "changed": ["src/calc.py"], "eligible": true, "reasons": [], "review_is_synthetic": true, "merged": false}

```

## 第4步 复现质量失败
目的：将加法改成减法，另加尾随空格；分别运行测试与lint。
命令：`cd /workspace/learn-batch/06-agent-ready/exercise && python3 lab.py 4`
真实结果：bad-regression：2个测试失败；bad-lint：trailing whitespace；两个都blocked。
验证：原始step-4-v2.log有失败堆栈与退出码；场景断言确保拒绝。

```text
$ git add .
exit_code=0
$ git commit -m bad-regression
[main d5ace67] bad-regression
 1 file changed, 1 insertion(+), 1 deletion(-)
exit_code=0
$ /usr/bin/python3 -m unittest discover -s tests -v
test_negative (test_calc.TestCalc.test_negative) ... FAIL
test_positive (test_calc.TestCalc.test_positive) ... FAIL
test_zero (test_calc.TestCalc.test_zero) ... ok

======================================================================
FAIL: test_negative (test_calc.TestCalc.test_negative)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/workspace/learn-batch/06-agent-ready/exercise/runs-v2/bad-regression/tests/test_calc.py", line 10, in test_negative
    self.assertEqual(add(-2, 3), 1)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
AssertionError: -5 != 1

======================================================================
FAIL: test_positive (test_calc.TestCalc.test_positive)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/workspace/learn-batch/06-agent-ready/exercise/runs-v2/bad-regression/tests/test_calc.py", line 7, in test_positive
    self.assertEqual(add(2, 3), 5)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
AssertionError: -1 != 5

----------------------------------------------------------------------
Ran 3 tests in 0.001s

FAILED (failures=2)
exit_code=1
$ /usr/bin/python3 /workspace/learn-batch/06-agent-ready/exercise/lab.py lint --repo /workspace/learn-batch/06-agent-ready/exercise/runs-v2/bad-regression
{"lint_files": 2, "errors": []}
exit_code=0
RESULT={"scenario": "bad-regression", "sha": "d5ace674203001ecc14dbb31bf4df53fc514645d", "changed": ["src/calc.py"], "eligible": false, "reasons": ["required check not green: tests"], "review_is_synthetic": true, "merged": false}
$ git add .
exit_code=0
$ git commit -m bad-lint
[main 1b9e9b9] bad-lint
 1 file changed, 1 insertion(+), 1 deletion(-)
exit_code=0
$ /usr/bin/python3 -m unittest discover -s tests -v
test_negative (test_calc.TestCalc.test_negative) ... ok
test_positive (test_calc.TestCalc.test_positive) ... ok
test_zero (test_calc.TestCalc.test_zero) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
exit_code=0
$ /usr/bin/python3 /workspace/learn-batch/06-agent-ready/exercise/lab.py lint --repo /workspace/learn-batch/06-agent-ready/exercise/runs-v2/bad-lint
{"lint_files": 2, "errors": ["src/calc.py:2: trailing whitespace"]}
exit_code=1
RESULT={"scenario": "bad-lint", "sha": "1b9e9b9daf98307a0e02c34fba02db0cf2246641", "changed": ["src/calc.py"], "eligible": false, "reasons": ["required check not green: lint"], "review_is_synthetic": true, "merged": false}

```

## 第5步 复现治理失败
目的：生成CI路径修改、过期SHA、缺失lint、作者自审四种夹具并验证拒绝。
命令：`cd /workspace/learn-batch/06-agent-ready/exercise && python3 lab.py 5`
真实结果：SUMMARY={"scenarios":8,"eligible":2,"blocked":6,"actual_remote_merges":0,"independent_reviews_performed":0}
验证：每份JSON含changed、sha、reasons；脚本assert验证预期。

```text
$ git add .
exit_code=0
$ git commit -m bad-policy
[main 2f11f03] bad-policy
 1 file changed, 1 insertion(+), 14 deletions(-)
exit_code=0
$ /usr/bin/python3 -m unittest discover -s tests -v
test_negative (test_calc.TestCalc.test_negative) ... ok
test_positive (test_calc.TestCalc.test_positive) ... ok
test_zero (test_calc.TestCalc.test_zero) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
exit_code=0
$ /usr/bin/python3 /workspace/learn-batch/06-agent-ready/exercise/lab.py lint --repo /workspace/learn-batch/06-agent-ready/exercise/runs-v2/bad-policy
{"lint_files": 2, "errors": []}
exit_code=0
RESULT={"scenario": "bad-policy", "sha": "2f11f03b8decb8bee5227be5e9e3d7d44ff28ca7", "changed": [".github/workflows/ci.yml"], "eligible": false, "reasons": ["protected or unknown path"], "review_is_synthetic": true, "merged": false}
$ git add .
exit_code=0
$ git commit -m bad-stale
[main 94aa9c0] bad-stale
 1 file changed, 2 insertions(+)
 create mode 100644 docs/new.md
exit_code=0
$ /usr/bin/python3 -m unittest discover -s tests -v
test_negative (test_calc.TestCalc.test_negative) ... ok
test_positive (test_calc.TestCalc.test_positive) ... ok
test_zero (test_calc.TestCalc.test_zero) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
exit_code=0
$ /usr/bin/python3 /workspace/learn-batch/06-agent-ready/exercise/lab.py lint --repo /workspace/learn-batch/06-agent-ready/exercise/runs-v2/bad-stale
{"lint_files": 2, "errors": []}
exit_code=0
RESULT={"scenario": "bad-stale", "sha": "94aa9c0ef58f621ebc509af3be56f7dd1b18e33f", "changed": ["docs/new.md"], "eligible": false, "reasons": ["stale CI SHA"], "review_is_synthetic": true, "merged": false}
$ git add .
exit_code=0
$ git commit -m bad-missing
[main 3bde387] bad-missing
 1 file changed, 2 insertions(+)
 create mode 100644 docs/new.md
exit_code=0
$ /usr/bin/python3 -m unittest discover -s tests -v
test_negative (test_calc.TestCalc.test_negative) ... ok
test_positive (test_calc.TestCalc.test_positive) ... ok
test_zero (test_calc.TestCalc.test_zero) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
exit_code=0
$ /usr/bin/python3 /workspace/learn-batch/06-agent-ready/exercise/lab.py lint --repo /workspace/learn-batch/06-agent-ready/exercise/runs-v2/bad-missing
{"lint_files": 2, "errors": []}
exit_code=0
RESULT={"scenario": "bad-missing", "sha": "3bde3879a823a88184a42af24a59c660e6a698e1", "changed": ["docs/new.md"], "eligible": false, "reasons": ["required check not green: lint"], "review_is_synthetic": true, "merged": false}
$ git add .
exit_code=0
$ git commit -m bad-self-review
[main f83c872] bad-self-review
 1 file changed, 1 insertion(+)
exit_code=0
$ /usr/bin/python3 -m unittest discover -s tests -v
test_negative (test_calc.TestCalc.test_negative) ... ok
test_positive (test_calc.TestCalc.test_positive) ... ok
test_zero (test_calc.TestCalc.test_zero) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
exit_code=0
$ /usr/bin/python3 /workspace/learn-batch/06-agent-ready/exercise/lab.py lint --repo /workspace/learn-batch/06-agent-ready/exercise/runs-v2/bad-self-review
{"lint_files": 2, "errors": []}
exit_code=0
RESULT={"scenario": "bad-self-review", "sha": "f83c8721c1a87a9767bf855b22eb8160370e3b10", "changed": ["src/calc.py"], "eligible": false, "reasons": ["independent approval absent (fixture)"], "review_is_synthetic": true, "merged": false}
SUMMARY={"scenarios": 8, "eligible": 2, "blocked": 6, "actual_remote_merges": 0, "independent_reviews_performed": 0}

```

## 首轮原始失败日志
```text
$ git add .
exit_code=0
$ git commit -m bad-regression
[main 8fa85ca] bad-regression
 1 file changed, 1 insertion(+), 1 deletion(-)
exit_code=0
$ /usr/bin/python3 -m unittest discover -s tests -v
test_negative (test_calc.TestCalc.test_negative) ... ok
test_positive (test_calc.TestCalc.test_positive) ... ok
test_zero (test_calc.TestCalc.test_zero) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
exit_code=0
$ /usr/bin/python3 /workspace/learn-batch/06-agent-ready/exercise/lab.py lint --repo /workspace/learn-batch/06-agent-ready/exercise/runs/bad-regression
{"lint_files": 2, "errors": []}
exit_code=0
Traceback (most recent call last):
  File "/workspace/learn-batch/06-agent-ready/exercise/lab.py", line 141, in <module>
    globals()['step' + a.step]()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/workspace/learn-batch/06-agent-ready/exercise/lab.py", line 122, in step4
    scenario('bad-regression', lambda r: put(r, 'src/calc.py', 'def add(a, b):\n    return a - b\n'), False)
    ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/learn-batch/06-agent-ready/exercise/lab.py", line 112, in scenario
    assert result['eligible'] is expected, result
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: {'sha': '8fa85ca2e5388dafbc5828afdcf9d16258bc5700', 'changed': ['src/calc.py'], 'eligible': True, 'reasons': [], 'review_is_synthetic': True, 'merged': False}

```

## CI一键入口独立调用（仍是本作者自测，不是独立审阅）
```text
$ cd exercise/runs-v2/base && sh ci.sh
[]
test_negative (test_calc.TestCalc.test_negative) ... ok
test_positive (test_calc.TestCalc.test_positive) ... ok
test_zero (test_calc.TestCalc.test_zero) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
exit_code=0
```

## 代码包实际复跑
将exercise.zip真实解压到repro-check/，python3 lab.py 1至5全部exit 0，原始输出见zip-reproduction.log。不是第二个人的独立审核。

## PDF未渲染
两次默认沙箱打印90秒/45秒超时；无PDF，无pdftoppm检查；详细过程pdf-review.md。

## 首轮假绿根因补证（真实读取旧pyc）
```text
Original source: def add(a, b):
    return a - b

source mtime_seconds=1794330676, size=32
pyc flags=0, timestamp_seconds=1794330676, source_size=32
Cached bytecode:
  0           RESUME                   0

  1           LOAD_CONST               0 (<code object add at 0x7f9f60d1b210, file "/workspace/learn-batch/06-agent-ready/exercise/runs/base/src/calc.py", line 1>)
              MAKE_FUNCTION
              STORE_NAME               0 (add)
              RETURN_CONST             1 (None)

Disassembly of <code object add at 0x7f9f60d1b210, file "/workspace/learn-batch/06-agent-ready/exercise/runs/base/src/calc.py", line 1>:
  1           RESUME                   0

  2           LOAD_FAST_LOAD_FAST      1 (a, b)
              BINARY_OP                0 (+)
              RETURN_VALUE

```
源代码是减法，缓存字节码却仍含BINARY_OP (+)，且mtime秒和大小匹配，直接验证了缓存假绿，不仅凭重跑推测。

## 本批PDF补全
WeasyPrint实际打印成功；pdftoppm全部11页转图并逐页目视自检，见pdf-review-batch2.md。未重跑旧实验。

实际PDF补全命令（exit0）：
```bash
/workspace/jingjing-duonaonao-batch2-20261111/.render-venv/bin/weasyprint /workspace/jingjing-duonaonao-batch2-20261111/06-agent-ready/guide.html /workspace/jingjing-duonaonao-batch2-20261111/06-agent-ready/guide.pdf
pdftoppm -scale-to 900 -png /workspace/jingjing-duonaonao-batch2-20261111/06-agent-ready/guide.pdf /workspace/jingjing-duonaonao-batch2-20261111/06-agent-ready/verification/page
```
第6项更正历史未渲染文案后重印，PNG哈希确认仅第11页变化，已再次查看；其余10页与首次目检相同。
