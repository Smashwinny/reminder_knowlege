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
