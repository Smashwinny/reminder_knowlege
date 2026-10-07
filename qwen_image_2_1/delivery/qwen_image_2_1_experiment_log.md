# Qwen Image 2.1 实验日志

本材料记录 2026-10-05 07:05 UTC 的原学习实验。公开整理未重新运行实验；以下输出、时间与统计保留原始运行含义。

日期：2026-10-05 UTC。范围：普通物体的合成提示与消息接口纯函数；没有模型 / API 推理、真实图片加载或生成。

## 1 来源与环境

- 官方 GitHub 固定 commit：6627d87c6433151463ec4b48b8945a24fcf16a35
- 官方模型元数据固定 revision：d26bb61231c349cf6b7896fa83353113880e1ba3
- pe_core.py SHA-256：fd9732bbba71468fb24bd81de5c209f0db2941f01d1e556d52b5a6deba0f1fe5
- LICENSE SHA-256：8dc973f024ff95966bea25866efa443fd16776dcb1001e681e3d467ea572b28d
- Python 3.12.14，Linux Bash，Python -I -S -B；json_repair 不加载
- 权重文件元数据共 33,115,613,408 字节，约 30.841 GiB；检查时空闲磁盘 31,342,288,896 字节，约 29.19 GiB。未下载权重；没有可用 NVIDIA 设备证据
- 7B 仅指视觉 Transformer；官方架构还列 8B 文本编码器和 VAE。没有测量推理显存或延迟
- 代码和模型为 Qwen Research License，商业用途需另行许可；练习包保留 LICENSE 和 NOTICE。另一个库的 Apache 2.0 不替代 Qwen 许可

## 2 可复现步骤

先把 ZIP 解压到新的空目录，再进入 exercise 子目录。以下五条命令已在全新解压的包中逐条执行，不依赖父目录的其他脚本。全部输出码为 0。耗时只属于 CPU 接口测试，不能用于推理速度比较。

### 1 核验环境与固定代码

```bash
python3 -I -S -B check_environment.py
```

目的：确认 Python 至少为 3.10，隔离启动和两个固定文件哈希。

实际结果：Python 3.12.14；pe_core.py 和 LICENSE 均 SHA256 OK。

成功判据：最后一行含 READY；命令退出码为 0。

开始 UTC：2026-10-05T07:05:04.615+00:00

结束 UTC：2026-10-05T07:05:04.650+00:00

耗时：0.035357 秒；退出码：0

标准输出：
```text
experiment/upstream/pe_core.py: SHA256 OK fd9732bbba71468fb24bd81de5c209f0db2941f01d1e556d52b5a6deba0f1fe5
experiment/upstream/LICENSE: SHA256 OK 8dc973f024ff95966bea25866efa443fd16776dcb1001e681e3d467ea572b28d
Python 3.12.14
isolated=True no_site=True no_bytecode=True
READY: stdlib-only CPU exercise; no model, image loading, API or network
```

标准错误：空

### 2 真正运行官方纯函数

```bash
python3 -I -S -B experiment/verify_contract.py > results.json
```

目的：构造普通物体的合成输入，运行消息、解析与记录测试。

实际结果：写出 results.json；上游预期行为检查 21/21 通过。

成功判据：退出码 0；步骤 4 会显示 21/21，JSON 含逐例证据。

开始 UTC：2026-10-05T07:05:04.651+00:00

结束 UTC：2026-10-05T07:05:04.722+00:00

耗时：0.071567 秒；退出码：0

标准输出：
```text
(空；步骤 2 的 stdout 已重定向为 results.json)
```

标准错误：空

### 3 看见参考图顺序

```bash
python3 -I -S -B inspect_results.py messages
```

目的：从本次结果读取消息内容，核对引用的先后顺序。

实际结果：依次为 image1 标记、image2 标记、文本。

成功判据：输出 ORDER PASS；标记没有被请求或解码。

开始 UTC：2026-10-05T07:05:04.722+00:00

结束 UTC：2026-10-05T07:05:04.751+00:00

耗时：0.029295 秒；退出码：0

标准输出：
```text
1. image_url: synthetic:image1:blue_cube
2. image_url: synthetic:image2:wooden_shelf
3. text: Place the cube on the shelf
ORDER PASS: image1, image2, text; markers were not fetched or decoded
```

标准错误：空

### 4 比较能解析与不能解析

```bash
python3 -I -S -B inspect_results.py parser
```

目的：观察正常、兼容、末尾候选和坏 JSON 的真实结果。

实际结果：正常 JSON、旧键与末尾有效候选能提取；无 JSON、截断、尾逗号、空提示词回退为 False。

成功判据：共 21/21 预期行为检查通过；json_repair absent。

开始 UTC：2026-10-05T07:05:04.751+00:00

结束 UTC：2026-10-05T07:05:04.788+00:00

耗时：0.036235 秒；退出码：0

标准输出：
```text
valid_t2i: parse_ok=True; positive_prompt=A blue ceramic mug on a shelf
valid_edit: parse_ok=True; positive_prompt=Make the mug green
legacy_key: parse_ok=True; positive_prompt=A glass vase
final_candidate_wins: parse_ok=True; positive_prompt=A blue cube
no_json_fallback: parse_ok=False; positive_prompt=A yellow bowl
truncated_json_fallback: parse_ok=False; positive_prompt={"rewritten_prompt":"A yellow bowl"
trailing_comma_without_repair: parse_ok=False; positive_prompt={"rewritten_prompt":"A yellow bowl",}
empty_prompt_fallback: parse_ok=False; positive_prompt={"rewritten_prompt":"   ","wh_ratio":"1:1"}
UPSTREAM EXPECTED-BEHAVIOR CHECKS: 21/21 passed; json_repair absent
```

标准错误：空

### 5 给下游加一道自定检查

```bash
python3 -I -S -B inspect_results.py validate
```

目的：用独立编写的消费者策略，检查比例选项、编辑选择互斥与两张参考图范围；它不是官方 schema。

实际结果：上游可解析的 6 例中，本练习策略接受 2 例，拒绝 4 例；四例分别涉及双字段、未知比例、缺选择和越界引用。

成功判据：输出 LOCAL POLICY CHECKS: 6/6 matched; 2 ACCEPT; 4 REJECT。

开始 UTC：2026-10-05T07:05:04.788+00:00

结束 UTC：2026-10-05T07:05:04.811+00:00

耗时：0.023071 秒；退出码：0

标准输出：
```text
valid_t2i: upstream_parse_ok=True; local_policy=ACCEPT
valid_edit: upstream_parse_ok=True; local_policy=ACCEPT
edit_both_ratio_fields_accepted: upstream_parse_ok=True; local_policy=REJECT choose_exactly_one_canvas_selector
unknown_aspect_ratio_accepted: upstream_parse_ok=True; local_policy=REJECT unsupported_ratio
missing_ratio_fields_accepted: upstream_parse_ok=True; local_policy=REJECT choose_exactly_one_canvas_selector
unverified_image_reference_accepted: upstream_parse_ok=True; local_policy=REJECT reference_out_of_range
LOCAL POLICY CHECKS: 6/6 matched; 2 ACCEPT; 4 REJECT
Local policy is a teaching example, not upstream code or image-quality validation
```

标准错误：空

## 3 实际结果解释

上游 21 项检查覆盖 2 个 profile、16 个解析用例、1 个消息构造及 2 个记录检查。21/21 指“实际行为与预期一致”，包含预期存在的 4 种宽松解析情况。不是官方所有函数覆盖率，也不是模型成功率。

新增 local_policy 是本练习独立编写的消费者规则：t2i 需要 7 个给定比例之一；edit 恰好选择 wh_ratio 或 ratio_follow；引用须在假定的两张输入图之内。2 个正常样本接受、4 个越界样本拒绝，6/6 均符合预期。规则不修改上游，不是官方完整 schema。

没有实跑 load_system_prompt、load_cases、resolve_image_paths、load_image、split_thinking、write_records、report_parse_failures 等路径。没有导入模型、图像解码器或客户端。合成图像标记只作为字符串传递。Python audit guard 是防御性限制，不是操作系统沙箱；全部成功测试没有触发被阻止事件。

## 4 真实开发问题

首轮上游测试加载器曾因探测 .pyc 缓存路径触发自身读取白名单而停止；改为对已哈希核验的未修改源代码字节直接 compile/exec。修正后得到最终 21/21，且全新解压重跑结果与参考 JSON 完全一致。这个修正属于练习加载器，上游 pe_core.py 没有改动。

## 5 上游完整实测输出

```json
{
  "experiment": "Actual official pe_core.py pure-function contract tests; not model inference",
  "source_repository": "https://github.com/QwenLM/Qwen-Image-2.1",
  "source_revision": "6627d87c6433151463ec4b48b8945a24fcf16a35",
  "source_path": "prompt_rewrite/pe_core.py",
  "source_sha256": "fd9732bbba71468fb24bd81de5c209f0db2941f01d1e556d52b5a6deba0f1fe5",
  "python_version": "3.12.14",
  "isolation": {
    "isolated": true,
    "no_site": true,
    "no_bytecode": true,
    "json_repair": "absent",
    "audit_guard": "denies network/processes/filesystem writes; permits only source and stdlib file reads",
    "blocked_events": []
  },
  "test_count": 21,
  "passed_count": 21,
  "all_passed": true,
  "cases": [
    {
      "name": "profile_t2i",
      "category": "task profile",
      "input": "t2i",
      "actual": [
        false,
        false,
        1.5,
        16256
      ],
      "expected": [
        false,
        false,
        1.5,
        16256
      ],
      "passed": true
    },
    {
      "name": "profile_edit",
      "category": "task profile",
      "input": "edit",
      "actual": [
        true,
        true,
        0.0,
        24000
      ],
      "expected": [
        true,
        true,
        0.0,
        24000
      ],
      "passed": true
    },
    {
      "name": "valid_t2i",
      "category": "normal extraction",
      "input": {
        "task": "t2i",
        "answer": "{\"rewritten_prompt\":\"A blue ceramic mug on a shelf\",\"wh_ratio\":\"1:1\"}"
      },
      "actual": {
        "positive_prompt": "A blue ceramic mug on a shelf",
        "wh_ratio": "1:1",
        "ratio_follow": "",
        "parse_ok": true
      },
      "expected": {
        "positive_prompt": "A blue ceramic mug on a shelf",
        "wh_ratio": "1:1",
        "ratio_follow": "",
        "parse_ok": true
      },
      "passed": true
    },
    {
      "name": "valid_edit",
      "category": "normal extraction",
      "input": {
        "task": "edit",
        "answer": "{\"rewritten_prompt\":\"Make the mug green\",\"wh_ratio\":\"\",\"ratio_follow\":\"<image1>\"}"
      },
      "actual": {
        "positive_prompt": "Make the mug green",
        "wh_ratio": "",
        "ratio_follow": "<image1>",
        "parse_ok": true
      },
      "expected": {
        "positive_prompt": "Make the mug green",
        "wh_ratio": "",
        "ratio_follow": "<image1>",
        "parse_ok": true
      },
      "passed": true
    },
    {
      "name": "braces_in_string",
      "category": "benign parser edge",
      "input": {
        "task": "t2i",
        "answer": "{\"rewritten_prompt\":\"A mug with {leaf} printed on it\",\"wh_ratio\":\"4:3\"}"
      },
      "actual": {
        "positive_prompt": "A mug with {leaf} printed on it",
        "wh_ratio": "4:3",
        "ratio_follow": "",
        "parse_ok": true
      },
      "expected": {
        "positive_prompt": "A mug with {leaf} printed on it",
        "wh_ratio": "4:3",
        "ratio_follow": "",
        "parse_ok": true
      },
      "passed": true
    },
    {
      "name": "escaped_quotes",
      "category": "benign parser edge",
      "input": {
        "task": "t2i",
        "answer": "{\"rewritten_prompt\": \"A box labelled \\\"TOOLS\\\"\", \"wh_ratio\": \"1:1\"}"
      },
      "actual": {
        "positive_prompt": "A box labelled \"TOOLS\"",
        "wh_ratio": "1:1",
        "ratio_follow": "",
        "parse_ok": true
      },
      "expected": {
        "positive_prompt": "A box labelled \"TOOLS\"",
        "wh_ratio": "1:1",
        "ratio_follow": "",
        "parse_ok": true
      },
      "passed": true
    },
    {
      "name": "final_candidate_wins",
      "category": "benign parser edge",
      "input": {
        "task": "t2i",
        "answer": "{\"rewritten_prompt\":\"A red cube\"} Text {\"rewritten_prompt\":\"A blue cube\",\"wh_ratio\":\"16:9\"}"
      },
      "actual": {
        "positive_prompt": "A blue cube",
        "wh_ratio": "16:9",
        "ratio_follow": "",
        "parse_ok": true
      },
      "expected": {
        "positive_prompt": "A blue cube",
        "wh_ratio": "16:9",
        "ratio_follow": "",
        "parse_ok": true
      },
      "passed": true
    },
    {
      "name": "trailing_irrelevant_object",
      "category": "benign parser edge",
      "input": {
        "task": "t2i",
        "answer": "{\"rewritten_prompt\":\"A wooden spoon\",\"wh_ratio\":\"3:4\"} Note {\"status\":\"done\"}"
      },
      "actual": {
        "positive_prompt": "A wooden spoon",
        "wh_ratio": "3:4",
        "ratio_follow": "",
        "parse_ok": true
      },
      "expected": {
        "positive_prompt": "A wooden spoon",
        "wh_ratio": "3:4",
        "ratio_follow": "",
        "parse_ok": true
      },
      "passed": true
    },
    {
      "name": "legacy_key",
      "category": "compatibility",
      "input": {
        "task": "t2i",
        "answer": "{\"rewrited_prompt\":\"A glass vase\",\"wh_ratio\":\"2:3\"}"
      },
      "actual": {
        "positive_prompt": "A glass vase",
        "wh_ratio": "2:3",
        "ratio_follow": "",
        "parse_ok": true
      },
      "expected": {
        "positive_prompt": "A glass vase",
        "wh_ratio": "2:3",
        "ratio_follow": "",
        "parse_ok": true
      },
      "passed": true
    },
    {
      "name": "no_json_fallback",
      "category": "invalid extraction",
      "input": {
        "task": "t2i",
        "answer": "A yellow bowl"
      },
      "actual": {
        "positive_prompt": "A yellow bowl",
        "wh_ratio": "",
        "ratio_follow": "",
        "parse_ok": false
      },
      "expected": {
        "positive_prompt": "A yellow bowl",
        "wh_ratio": "",
        "ratio_follow": "",
        "parse_ok": false
      },
      "passed": true
    },
    {
      "name": "truncated_json_fallback",
      "category": "invalid extraction",
      "input": {
        "task": "t2i",
        "answer": "{\"rewritten_prompt\":\"A yellow bowl\""
      },
      "actual": {
        "positive_prompt": "{\"rewritten_prompt\":\"A yellow bowl\"",
        "wh_ratio": "",
        "ratio_follow": "",
        "parse_ok": false
      },
      "expected": {
        "positive_prompt": "{\"rewritten_prompt\":\"A yellow bowl\"",
        "wh_ratio": "",
        "ratio_follow": "",
        "parse_ok": false
      },
      "passed": true
    },
    {
      "name": "trailing_comma_without_repair",
      "category": "invalid extraction",
      "input": {
        "task": "t2i",
        "answer": "{\"rewritten_prompt\":\"A yellow bowl\",}"
      },
      "actual": {
        "positive_prompt": "{\"rewritten_prompt\":\"A yellow bowl\",}",
        "wh_ratio": "",
        "ratio_follow": "",
        "parse_ok": false
      },
      "expected": {
        "positive_prompt": "{\"rewritten_prompt\":\"A yellow bowl\",}",
        "wh_ratio": "",
        "ratio_follow": "",
        "parse_ok": false
      },
      "passed": true
    },
    {
      "name": "empty_prompt_fallback",
      "category": "invalid extraction",
      "input": {
        "task": "t2i",
        "answer": "{\"rewritten_prompt\":\"   \",\"wh_ratio\":\"1:1\"}"
      },
      "actual": {
        "positive_prompt": "{\"rewritten_prompt\":\"   \",\"wh_ratio\":\"1:1\"}",
        "wh_ratio": "",
        "ratio_follow": "",
        "parse_ok": false
      },
      "expected": {
        "positive_prompt": "{\"rewritten_prompt\":\"   \",\"wh_ratio\":\"1:1\"}",
        "wh_ratio": "",
        "ratio_follow": "",
        "parse_ok": false
      },
      "passed": true
    },
    {
      "name": "t2i_ignores_edit_reference",
      "category": "task-specific field",
      "input": {
        "task": "t2i",
        "answer": "{\"rewritten_prompt\":\"A folded paper boat\",\"wh_ratio\":\"3:2\",\"ratio_follow\":\"<image1>\"}"
      },
      "actual": {
        "positive_prompt": "A folded paper boat",
        "wh_ratio": "3:2",
        "ratio_follow": "",
        "parse_ok": true
      },
      "expected": {
        "positive_prompt": "A folded paper boat",
        "wh_ratio": "3:2",
        "ratio_follow": "",
        "parse_ok": true
      },
      "passed": true
    },
    {
      "name": "edit_both_ratio_fields_accepted",
      "category": "domain validation gap",
      "input": {
        "task": "edit",
        "answer": "{\"rewritten_prompt\":\"Make the cup blue\",\"wh_ratio\":\"16:9\",\"ratio_follow\":\"<image1>\"}"
      },
      "actual": {
        "positive_prompt": "Make the cup blue",
        "wh_ratio": "16:9",
        "ratio_follow": "<image1>",
        "parse_ok": true
      },
      "expected": {
        "positive_prompt": "Make the cup blue",
        "wh_ratio": "16:9",
        "ratio_follow": "<image1>",
        "parse_ok": true
      },
      "passed": true
    },
    {
      "name": "unknown_aspect_ratio_accepted",
      "category": "domain validation gap",
      "input": {
        "task": "t2i",
        "answer": "{\"rewritten_prompt\":\"A green notebook\",\"wh_ratio\":\"wide-ish\"}"
      },
      "actual": {
        "positive_prompt": "A green notebook",
        "wh_ratio": "wide-ish",
        "ratio_follow": "",
        "parse_ok": true
      },
      "expected": {
        "positive_prompt": "A green notebook",
        "wh_ratio": "wide-ish",
        "ratio_follow": "",
        "parse_ok": true
      },
      "passed": true
    },
    {
      "name": "missing_ratio_fields_accepted",
      "category": "domain validation gap",
      "input": {
        "task": "edit",
        "answer": "{\"rewritten_prompt\":\"Make the cube green\"}"
      },
      "actual": {
        "positive_prompt": "Make the cube green",
        "wh_ratio": "",
        "ratio_follow": "",
        "parse_ok": true
      },
      "expected": {
        "positive_prompt": "Make the cube green",
        "wh_ratio": "",
        "ratio_follow": "",
        "parse_ok": true
      },
      "passed": true
    },
    {
      "name": "unverified_image_reference_accepted",
      "category": "domain validation gap",
      "input": {
        "task": "edit",
        "answer": "{\"rewritten_prompt\":\"Make the cube green\",\"ratio_follow\":\"<image99>\"}"
      },
      "actual": {
        "positive_prompt": "Make the cube green",
        "wh_ratio": "",
        "ratio_follow": "<image99>",
        "parse_ok": true
      },
      "expected": {
        "positive_prompt": "Make the cube green",
        "wh_ratio": "",
        "ratio_follow": "<image99>",
        "parse_ok": true
      },
      "passed": true
    },
    {
      "name": "image_marker_order",
      "category": "message construction",
      "input": [
        "synthetic:image1:blue_cube",
        "synthetic:image2:wooden_shelf"
      ],
      "actual": [
        {
          "role": "system",
          "content": [
            {
              "type": "text",
              "text": "Describe ordinary objects"
            }
          ]
        },
        {
          "role": "user",
          "content": [
            {
              "type": "image_url",
              "image_url": {
                "url": "synthetic:image1:blue_cube"
              }
            },
            {
              "type": "image_url",
              "image_url": {
                "url": "synthetic:image2:wooden_shelf"
              }
            },
            {
              "type": "text",
              "text": "Place the cube on the shelf"
            }
          ]
        }
      ],
      "expected": [
        {
          "role": "system",
          "content": [
            {
              "type": "text",
              "text": "Describe ordinary objects"
            }
          ]
        },
        {
          "role": "user",
          "content": [
            {
              "type": "image_url",
              "image_url": {
                "url": "synthetic:image1:blue_cube"
              }
            },
            {
              "type": "image_url",
              "image_url": {
                "url": "synthetic:image2:wooden_shelf"
              }
            },
            {
              "type": "text",
              "text": "Place the cube on the shelf"
            }
          ]
        }
      ],
      "passed": true
    },
    {
      "name": "record_field_order",
      "category": "output contract",
      "input": {
        "id": "ordinary_object_1",
        "prompt": "A blue mug"
      },
      "actual": [
        "id",
        "task",
        "raw_prompt",
        "input_images",
        "task_type",
        "thinking",
        "positive_prompt",
        "negative_prompt",
        "wh_ratio",
        "ratio_follow",
        "parse_ok"
      ],
      "expected": [
        "id",
        "task",
        "raw_prompt",
        "input_images",
        "task_type",
        "thinking",
        "positive_prompt",
        "negative_prompt",
        "wh_ratio",
        "ratio_follow",
        "parse_ok"
      ],
      "passed": true
    },
    {
      "name": "record_contents",
      "category": "output contract",
      "input": {
        "id": "ordinary_object_1",
        "prompt": "A blue mug"
      },
      "actual": {
        "id": "ordinary_object_1",
        "task": "t2i",
        "raw_prompt": "A blue mug",
        "input_images": [],
        "task_type": "",
        "thinking": "",
        "positive_prompt": "A blue ceramic mug",
        "negative_prompt": "",
        "wh_ratio": "1:1",
        "ratio_follow": "",
        "parse_ok": true
      },
      "expected": {
        "id": "ordinary_object_1",
        "task": "t2i",
        "raw_prompt": "A blue mug",
        "input_images": [],
        "task_type": "",
        "thinking": "",
        "positive_prompt": "A blue ceramic mug",
        "negative_prompt": "",
        "wh_ratio": "1:1",
        "ratio_follow": "",
        "parse_ok": true
      },
      "passed": true
    }
  ],
  "interpretation": [
    "Pass means observed upstream behavior matches stated expectations, including observed validation gaps.",
    "parse_ok is extraction success, not complete schema/domain validation.",
    "No prompt rewriting, image loading, model inference, quality, transparency, GPU performance, or deployment was tested.",
    "Synthetic image markers were only copied as strings; they were not fetched or decoded.",
    "The Python audit guard is defense-in-depth, not a claim of OS-level sandboxing."
  ]
}
```

## 6 固定链接

- [官方源码](https://github.com/QwenLM/Qwen-Image-2.1/blob/6627d87c6433151463ec4b48b8945a24fcf16a35/prompt_rewrite/pe_core.py)
- [官方模型元数据](https://huggingface.co/Qwen/Qwen-Image-2.1/tree/d26bb61231c349cf6b7896fa83353113880e1ba3)
- [Qwen Research License](https://github.com/QwenLM/Qwen-Image-2.1/blob/6627d87c6433151463ec4b48b8945a24fcf16a35/LICENSE)

## 7 成稿检查记录

指南由 ReportLab 直接生成，A4 共 11 页；没有使用或重试 HTML 转 PDF。渲染命令为 pdftoppm -r 120 -png，PNG 逐页打开查看。初版页脚分隔符出现缺字方框，已换为 ASCII 分隔符；正文换行已调整为保留英文标识符、避免标点孤行。2026-10-05 07:08 UTC 已检查最终 11 页，每页均无缺字方框、文本重叠、越界或截断。

HTML 使用内联 CSS 与 SVG，无外部图片、脚本或跟踪资源。结构核对为 12 个问题、12 个独立 SVG、5 项能力、5 个用途、5 个已实跑步骤；没有声称 HTML 视觉预览通过。PDF 中 12 个概念图采用相同内容的矢量绘制。

独立审核由另一审核者单独出具第六份审核日志；本节仅记录作者自身的渲染与检查。
