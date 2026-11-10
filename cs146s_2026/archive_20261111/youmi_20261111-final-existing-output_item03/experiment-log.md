# CS146S真实实验日志
日期：2026-11-11T01:09:26.061167+08:00（Asia/Shanghai）
已实读原帖/引用、官方课纲公开chunk、两篇课程逐字稿和下载源码。通过AST仅装载5个已读函数，跳过API初始化和原主循环，无用户密钥、无模型调用。

## 1
```bash
cd /workspace/reminder-batch/worker-689b81da/item03
python3 exercise/course_lab.py manifest
```
```text
[
  {
    "file": "source-post.json",
    "bytes": 27201,
    "sha256": "548da72323ac09a8b50ec1a4660df2de3d688f78830f7c14467a5782afc3c9c1"
  },
  {
    "file": "course-home.html",
    "bytes": 27161,
    "sha256": "8566d8ad058d4e35a1040227d73e85886dc59919911e3c6663c6fe950b515129"
  },
  {
    "file": "course-calendar.txt",
    "bytes": 2611,
    "sha256": "d21a71cd8d5bd025073f938a5dff7fbd28deeeb0aa03676c229181be17de16fa"
  },
  {
    "file": "course2026-source-fragment.txt",
    "bytes": 7988,
    "sha256": "6e4ed32d910199629cda92797f0c0861719a6912ac5e887295b0659072ca92c8"
  },
  {
    "file": "transcript-0924.txt",
    "bytes": 39513,
    "sha256": "c19a165345967e2668c0273345e2eac2b42cc9386eede015ce6a0c36c5f5549b"
  },
  {
    "file": "transcript-1001.txt",
    "bytes": 29384,
    "sha256": "2d9e7eda8f8e8659d34ad4ae38cbbf19373517468fd8550b76f014e0cba3cd03"
  },
  {
    "file": "coding_agent_from_scratch.py",
    "bytes": 6395,
    "sha256": "a70a9bece7952abb6b466eb16ece51ae1716d177d0a1a85c5e017de85ebce2b4"
  }
]

```
退出码：0

## 2
```bash
cd /workspace/reminder-batch/worker-689b81da/item03
python3 exercise/course_lab.py inspect_source
```
```text
{
  "physical_lines": 193,
  "registry": [
    "read_file",
    "list_files",
    "edit_file"
  ],
  "has_bash": false,
  "selected_functions": [
    "edit_file_tool",
    "extract_tool_invocations",
    "list_files_tool",
    "read_file_tool",
    "resolve_abs_path"
  ],
  "global_api_initialization_skipped": true
}

```
退出码：0

## 3
```bash
cd /workspace/reminder-batch/worker-689b81da/item03
python3 exercise/course_lab.py parsing
```
```text
{
  "normal": [
    [
      "read_file",
      {
        "filename": "demo.txt"
      }
    ]
  ],
  "trailing": [
    [
      "read_file",
      {
        "filename": "demo.txt"
      }
    ]
  ],
  "array": [
    [
      "read_file",
      [
        1,
        2
      ]
    ]
  ],
  "unknown": [
    [
      "remove_everything",
      {}
    ]
  ],
  "malformed": []
}

```
退出码：0

## 4
```bash
cd /workspace/reminder-batch/worker-689b81da/item03
python3 exercise/course_lab.py file_tools
```
```text
/workspace/reminder-batch/worker-689b81da/item03/scratch/demo.txt
{
  "replace_first": {
    "path": "/workspace/reminder-batch/worker-689b81da/item03/scratch/demo.txt",
    "action": "edited"
  },
  "read_after_replace": {
    "file_path": "/workspace/reminder-batch/worker-689b81da/item03/scratch/demo.txt",
    "content": "beta alpha\n"
  },
  "missing_old": {
    "path": "/workspace/reminder-batch/worker-689b81da/item03/scratch/demo.txt",
    "action": "old_str not found"
  },
  "empty_old": {
    "path": "/workspace/reminder-batch/worker-689b81da/item03/scratch/demo.txt",
    "action": "created_file"
  },
  "final_content": "fresh\n"
}

```
退出码：0

## 5
```bash
cd /workspace/reminder-batch/worker-689b81da/item03
python3 exercise/course_lab.py replay
```
```text
/workspace/reminder-batch/worker-689b81da/item03/scratch/replay.txt
{
  "scripted_model": true,
  "max_steps": 4,
  "observed_steps": 3,
  "events": [
    {
      "step": 1,
      "tool": "edit_file",
      "result": {
        "path": "/workspace/reminder-batch/worker-689b81da/item03/scratch/replay.txt",
        "action": "created_file"
      }
    },
    {
      "step": 2,
      "tool": "read_file",
      "result": {
        "file_path": "/workspace/reminder-batch/worker-689b81da/item03/scratch/replay.txt",
        "content": "answer=42"
      }
    },
    {
      "step": 3,
      "assistant": "Finished: answer=42",
      "stop": true
    }
  ],
  "artifact": "answer=42"
}

```
退出码：0

## 6
```bash
cd /workspace/reminder-batch/worker-689b81da/item03
python3 exercise/course_lab.py test
```
```text
test_absolute_not_sandbox (__main__.Tests.test_absolute_not_sandbox) ... ok
test_array_accepted (__main__.Tests.test_array_accepted) ... ok
test_docstring (__main__.Tests.test_docstring) ... ok
test_malformed (__main__.Tests.test_malformed) ... ok
test_missing_closer_accepted (__main__.Tests.test_missing_closer_accepted) ... ok
test_normal (__main__.Tests.test_normal) ... ok
test_relative_can_leave_scratch (__main__.Tests.test_relative_can_leave_scratch) ... ok
test_trailing_accepted (__main__.Tests.test_trailing_accepted) ... ok
test_unknown_accepted (__main__.Tests.test_unknown_accepted) ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.001s

OK

```
退出码：0

真实下载最初返回Google Drive病毒扫描提示HTML（不是源码），随后沿页面公开下载表单读取源码并逐行审阅；未执行原始脚本顶层。课程网页无Git SHA，以内容SHA256与访问日期固定。未完整运行原Agent、付费模型、真实PR提交或课程学分评估。
