---
tags: [候选成果, 增量学习, 未合入]
created: 2026-11-11
---
# 第7项 knowledge proposal：Ivy AI：让大工作集轮流用内存

## 查重与差异
固定main：a8674777e18302b8804b137212b1396cbfe5a747。已读00-总览及相关概念正文。总览未列本批七条原帖的专门项目记录；没有据此断言全仓库绝无重叠。
复用量化、KV缓存、级联语音和证据优先笔记，增加阶段arena所有权、连续块预算及同SHA文档漂移案例，不新建整套同义内存概念。

## 建议追加的项目案例（待协调者审核）
来源：https://x.com/i/status/2112109068584473072；一手SHA见sources.md。

### 轮流使用怎样改变峰值？
若生命周期不重叠，共用大块arena，理想阶段峰值由求和变为取最大值6.5MB，7MB示例arena余0.5MB。实际还要计算常驻对象、对齐、内部SRAM、DMA与驱动，不能只凭这个不等式保证启动。

### 对齐、容量和回退测试分别查什么？
alloc按align计算补齐字节并核对剩余容量；mark/rewind回到局部水位。上游测试覆盖16字节对齐、超容量返回NULL及结束后整块复用。测试输入不能穷尽所有align或竞态，PASS不是分配器安全认证。

### 5到6tok/s与63.3%能写成本批实测吗？
绝对不能。这是作者README在特定板上、特定模型与问题集的报告；本批只跑arena主机测试和预算算术，没有权重、语音识别、TTS、准确率评测或板上性能。规则代码处理时间等任务也是作者设计，不是本批模型能力。

## 建议互链，不新建同义概念
[[接缝与桩实现StubSeam]]、[[级联语音管线]]、[[证据优先质检ProofOverClaims]]、[[规格书先行SpecDriven]]。按实际概念选择落点，禁止把整个案例机械加到全部笔记。

## 本批状态
待验证：原帖已读，但所引用帖子实际讲Groki而非Ivy，已记录错链；通过项目官网和仓库核实Ivy。上游arena主机测试真实通过；未执行模型或ESP32语音。

## 可复核结果
# 第7项真实实验日志
执行时间：2026-11-11T00:58:17.408812+08:00 Asia/Shanghai
环境：Linux云电脑；全部为受控数据。

## 步骤 1
```sh
cd /workspace/reminder-batch-2026-11-11/item07/exercise
python3 lab.py 1
```
退出码：0
```text
{"python": "3.13.5", "scope": "真实上游C arena测试 + 教学内存预算"}

```

## 步骤 2
```sh
cd /workspace/reminder-batch-2026-11-11/item07/exercise
python3 lab.py 2
```
退出码：1
```text
In file included from upstream/components/story_core/story_arena.c:12:
upstream/components/story_core/include/story_log.h:19:10: fatal error: esp_log.h: No such file or directory
   19 | #include "esp_log.h"
      |          ^~~~~~~~~~~
compilation terminated.

Traceback (most recent call last):
  File "/workspace/reminder-batch-2026-11-11/item07/exercise/lab.py", line 14, in <module>
    r=subprocess.run(cmd,cwd=P,text=True,capture_output=True);print(r.stdout+r.stderr);assert r.returncode==0
                                                                                              ^^^^^^^^^^^^^^^
AssertionError

```

## 步骤 3
```sh
cd /workspace/reminder-batch-2026-11-11/item07/exercise
python3 lab.py 3
```
退出码：1
```text
Traceback (most recent call last):
  File "/workspace/reminder-batch-2026-11-11/item07/exercise/lab.py", line 18, in <module>
    r=subprocess.run(['./test_arena'],cwd=P,text=True,capture_output=True);print(r.stdout+r.stderr);assert r.returncode==0 and 'test_arena OK' in r.stdout
  File "/usr/lib/python3.13/subprocess.py", line 554, in run
    with Popen(*popenargs, **kwargs) as process:
         ~~~~~^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 1039, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        pass_fds, cwd, env,
                        ^^^^^^^^^^^^^^^^^^^
    ...<5 lines>...
                        gid, gids, uid, umask,
                        ^^^^^^^^^^^^^^^^^^^^^^
                        start_new_session, process_group)
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/subprocess.py", line 1972, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
FileNotFoundError: [Errno 2] No such file or directory: './test_arena'

```

## 步骤 4
```sh
cd /workspace/reminder-batch-2026-11-11/item07/exercise
python3 lab.py 4
```
退出码：0
```text
{"arena_MB": 7, "headroom_MB": 0.5, "illustrative_MB": {"LLM": 6.5, "STT": 5.4, "TTS": 2.5}, "sequential_peak_MB": 6.5, "simultaneous_MB": 14.4, "warning": "十进制教学近似；不含全部系统常驻内存，非ESP32测量"}

```

## 修复与复跑
首次漏加上游 host/stubs 的日志适配头；没有修改上游算法，只增加官方主机桩 include 路径。首次失败保留在前文。

```sh
cd /workspace/reminder-batch-2026-11-11/item07/exercise
python3 lab.py 2
```
退出码：0
```text
upstream/components/story_core/story_arena.c: In function ‘story_arena_log’:
upstream/components/story_core/story_arena.c:84:43: warning: unused parameter ‘a’ [-Wunused-parameter]
   84 | void story_arena_log(const story_arena_t *a, const char *why)
      |                      ~~~~~~~~~~~~~~~~~~~~~^
upstream/components/story_core/story_arena.c:84:58: warning: unused parameter ‘why’ [-Wunused-parameter]
   84 | void story_arena_log(const story_arena_t *a, const char *why)
      |                                              ~~~~~~~~~~~~^~~
upstream/components/story_core/story_arena.c: At top level:
upstream/components/story_core/story_arena.c:15:20: warning: ‘TAG’ defined but not used [-Wunused-variable]
   15 | static const char *TAG = "arena";
      |                    ^~~

{"command": ["gcc", "-std=c11", "-Wall", "-Wextra", "-Iupstream/components/story_core/include", "-Iupstream/host", "-Iupstream/host/stubs", "upstream/host/test_arena.c", "upstream/components/story_core/story_arena.c", "-o", "test_arena"], "compile_exit": 0}

```

```sh
cd /workspace/reminder-batch-2026-11-11/item07/exercise
python3 lab.py 3
```
退出码：0
```text
test_arena OK
alloc 16 B for 'no-owner' with no owning phase
begin('llm') refused: arena still owned by 'stt' (0 bytes used)
ALLOC FAILED: owner='stt' tag='too-big' want=5000 align=4 | used=80 free=4016 cap=4096
ALLOC FAILED: owner='llm' tag='over' want=1 align=1 | used=4096 free=0 cap=4096

{"exit_code": 0, "not_tested": ["模型推理", "ESP-IDF固件", "麦克风", "PSRAM时序"], "upstream_test": "test_arena OK"}

```

## 合入边界
仅为隔离候选提案，没有合入共享vault、改变网站标签、勾选Reminder或Git发布。自检不是独立审核；待协调者复核。
