# NCE 播放器工程历史实验日志

公开副本说明：本次整理未重跑实验。命令、参数、合成输入、断言、开始/结束时间、耗时和退出码来自 2026-10-05 的历史实测。输出路径统一为 results/ 下的相对路径；其余数值和结果不变。

日期：2026-10-05 UTC。执行者：指南作者；独立审核另有文件。

## 实验边界

2026-10-05 在全新解包目录实际执行了下列六步。未安装 npm 包，没有打开真实浏览器，没有获取、生成、解码或试听音频。上游 14 个 JS 模块和 MIT 许可逐字节保留。仅实验子类覆盖 init() 以停止目录启动；DOM、音频、存储、时钟和定时器为受控替身。

历史原始练习 ZIP SHA-256（公开说明加入前）：8a3244c9c095a210bcd02c0c01496ac719221d9b7678979814ead0b815672552。Node 与 Python 的实际版本见第一步。

72 项完整集合包括 55 项行为断言、16 项完整性检查和 1 项无外联保护。每个分组都会重复同一项无外联保护；分组共 77 次断言命中，完整集合是 72 项独立检查，不能把六步计数相加当作独立用例数。行为特征通过不表示缺陷已经修复。

## 六步完整命令与实际输出

### 1. 解包与确认源码完整

目的：在全新目录运行，确认环境及 14 个模块和许可的字节。
开始：2026-10-05T09:59:34.538212+00:00；结束：2026-10-05T09:59:34.696238+00:00；实测耗时 0.158 秒；退出码：0。

```bash
python3 -m zipfile -e nce-player-exercise.zip replay
cd replay/nce-player-exercise
python3 --version
node --version
node run.mjs --group integrity --output results/01-integrity.json
```

实际结果：17/17：15 个文件哈希、14 个 JS 数量及无外联保护通过。
验证方法：核对 verifiedUpstreamFiles=15，failed=0。

历史标准输出（仅输出路径规范化）：
```text
Python 3.12.14
v24.19.0
{
  "passed": 17,
  "failed": 0,
  "assertions": 17,
  "groups": [
    "integrity",
    "safety"
  ],
  "verifiedUpstreamFiles": 15,
  "output": "results/01-integrity.json",
  "startedAt": "2026-10-05T09:59:34.673Z",
  "finishedAt": "2026-10-05T09:59:34.685Z",
  "scope": "Controlled component simulation using actual upstream modules; not full-player end-to-end, browser, layout, or playback testing."
}
```

### 2. 读出六条原创双语句子

目的：观察过滤规则、双语字段与按时间排序的实际结果。
开始：2026-10-05T09:59:34.697029+00:00；结束：2026-10-05T09:59:34.795737+00:00；实测耗时 0.099 秒；退出码：0。

```bash
node run.mjs --group parser --output results/02-parser.json
```

实际结果：7/7：六条原创记录按时间排序；无效格式被过滤。
验证方法：查看 tests 中六项 parser 行的 actual 与 expected。

历史标准输出（仅输出路径规范化）：
```text
{
  "passed": 7,
  "failed": 0,
  "assertions": 7,
  "groups": [
    "parser",
    "safety"
  ],
  "verifiedUpstreamFiles": 15,
  "output": "results/02-parser.json",
  "startedAt": "2026-10-05T09:59:34.776Z",
  "finishedAt": "2026-10-05T09:59:34.788Z",
  "scope": "Controlled component simulation using actual upstream modules; not full-player end-to-end, browser, layout, or playback testing."
}
```

### 3. 对照偏移与句子边界

目的：让 0 与 0.3 秒偏移的差别成为可见的数值。
开始：2026-10-05T09:59:34.796049+00:00；结束：2026-10-05T09:59:34.896702+00:00；实测耗时 0.101 秒；退出码：0。

```bash
node run.mjs --group timeline --output results/03-timeline.json
```

实际结果：11/11：首句 -0.2 秒；2.2 秒命中索引 3；索引 2 为零长度。
验证方法：对照两组时间数组、精确命中和最后一句 [5.7,8]。

历史标准输出（仅输出路径规范化）：
```text
{
  "passed": 11,
  "failed": 0,
  "assertions": 11,
  "groups": [
    "timeline",
    "safety"
  ],
  "verifiedUpstreamFiles": 15,
  "output": "results/03-timeline.json",
  "startedAt": "2026-10-05T09:59:34.881Z",
  "finishedAt": "2026-10-05T09:59:34.890Z",
  "scope": "Controlled component simulation using actual upstream modules; not full-player end-to-end, browser, layout, or playback testing."
}
```

### 4. 检查媒体控制事件

目的：在时长、进度条与时钟替身上执行真实 AudioController。
开始：2026-10-05T09:59:34.897034+00:00；结束：2026-10-05T09:59:34.986593+00:00；实测耗时 0.090 秒；退出码：0。

```bash
node run.mjs --group controller --output results/04-controller.json
```

实际结果：15/15：已知 8 秒时长下定位受限；恢复进度为 7.95 秒。
验证方法：未知时长负定位是特征记录；tick、拖动和销毁均有断言。

历史标准输出（仅输出路径规范化）：
```text
{
  "passed": 15,
  "failed": 0,
  "assertions": 15,
  "groups": [
    "controller",
    "safety"
  ],
  "verifiedUpstreamFiles": 15,
  "output": "results/04-controller.json",
  "startedAt": "2026-10-05T09:59:34.967Z",
  "finishedAt": "2026-10-05T09:59:34.977Z",
  "scope": "Controlled component simulation using actual upstream modules; not full-player end-to-end, browser, layout, or playback testing."
}
```

### 5. 检查句子显示与激活

目的：调用真实 LyricsView，观察渲染字符串、active 类与事件。
开始：2026-10-05T09:59:34.986952+00:00；结束：2026-10-05T09:59:35.096345+00:00；实测耗时 0.109 秒；退出码：0。

```bash
node run.mjs --group view --output results/05-view.json
```

实际结果：11/11：六个句子节点、高亮、点击与键盘激活通过。
验证方法：检查转义字符串、旧高亮移除和空列表；不是浏览器布局验收。

历史标准输出（仅输出路径规范化）：
```text
{
  "passed": 11,
  "failed": 0,
  "assertions": 11,
  "groups": [
    "view",
    "safety"
  ],
  "verifiedUpstreamFiles": 15,
  "output": "results/05-view.json",
  "startedAt": "2026-10-05T09:59:35.074Z",
  "finishedAt": "2026-10-05T09:59:35.089Z",
  "scope": "Controlled component simulation using actual upstream modules; not full-player end-to-end, browser, layout, or playback testing."
}
```

### 6. 贯通真实组件方法链

目的：验证点击到播放，以及 tick 到高亮和句末暂停的接线。
开始：2026-10-05T09:59:35.096665+00:00；结束：2026-10-05T09:59:35.302171+00:00；实测耗时 0.206 秒；退出码：0。

```bash
node run.mjs --group integration --output results/06-integration.json
node run.mjs --output results/07-all.json
```

实际结果：16/16；再跑完整集合 72/72。click 句尾回到 0.95 秒并暂停。
验证方法：全量为 55 项行为、16 项完整性和 1 项保护；非真实端到端。

历史标准输出（仅输出路径规范化）：
```text
{
  "passed": 16,
  "failed": 0,
  "assertions": 16,
  "groups": [
    "integration",
    "safety"
  ],
  "verifiedUpstreamFiles": 15,
  "output": "results/06-integration.json",
  "startedAt": "2026-10-05T09:59:35.180Z",
  "finishedAt": "2026-10-05T09:59:35.198Z",
  "scope": "Controlled component simulation using actual upstream modules; not full-player end-to-end, browser, layout, or playback testing."
}
{
  "passed": 72,
  "failed": 0,
  "assertions": 72,
  "groups": [
    "integrity",
    "parser",
    "timeline",
    "controller",
    "view",
    "integration",
    "safety"
  ],
  "verifiedUpstreamFiles": 15,
  "output": "results/07-all.json",
  "startedAt": "2026-10-05T09:59:35.281Z",
  "finishedAt": "2026-10-05T09:59:35.296Z",
  "scope": "Controlled component simulation using actual upstream modules; not full-player end-to-end, browser, layout, or playback testing."
}
```

## 完整集合的原始 JSON

以下结果来自第六步最后一条命令。每条记录在断言时冻结快照；已再次检查所有 pass=true 的 actual 与 expected 相等。时间是执行证据，不是性能基准。

```json
{
  "schema": 1,
  "startedAt": "2026-10-05T09:59:35.281Z",
  "node": "v24.19.0",
  "group": "all",
  "argv": [
    "--output",
    "results/07-all.json"
  ],
  "source": {
    "repository": "https://github.com/iChochy/NCE",
    "commit": "0a92ab5af50e2898a104f15eac7adb00f17bd96b",
    "commitTime": "2026-08-26T15:23:55+08:00",
    "observedAt": "2026-10-05T09:47:00Z",
    "license": "MIT; Copyright (c) 2025 iChochy; upstream/LICENSE retained verbatim",
    "contentBoundary": "The software license is not a license to third-party lessons, translations, or recordings. No course-resource files are included.",
    "officialCatalog": {
      "url": "https://nce.ichochy.com/data.json",
      "sha256": "858c86fc9b094c6ed1f68c1410d3739736cf5e2d07e323cc048321bf5616b64f",
      "matchesPinnedRepository": true,
      "observedBooks": 8,
      "resourceFilesFetched": 0
    },
    "files": {
      "LICENSE": "81467deceb4672ed5304e6d7751b7bdba03a7e69d9838c70bc3df779e1990a32",
      "js/ReadingSystem.js": "ba71932549951e66a835cd2dfe7624533907e1cd73d2cd862a106d62bee80c52",
      "js/config.js": "fb891186e2ff84b36ee7a1c8bd677b9ce1432c1096eae5b012191f11e65beb85",
      "js/managers/CacheManager.js": "50f1d3736fa668c79cf8d1198bc56b577832cef83598c6a932b4f5b13d5dfe43",
      "js/player/AudioController.js": "75d11d6383426228e9f63466f8008e421e560dfcfb4869e04d553926bd131a28",
      "js/services/BookService.js": "fe42e20d623c229c64dcddf5913895b90650238fe1d35f66c7d0ec1fb9f37b95",
      "js/services/PrefetchService.js": "11c206099dcdab93038c628b3fb34f7fe31e6bb9b94906491507ae37e31b5223",
      "js/ui/LyricsView.js": "cc40dab4d9b4784a14e9b0cdc15b7746a277a395363d0873bd90a5cfeb633e13",
      "js/ui/Toast.js": "dd7648aafcf7a600efb8deb65b7a29166bfb4a85676974c5757252e7fcb1f728",
      "js/ui/UnitView.js": "603f0fde725ed4ee90be2ad7acfb0479fc0467baa6ae640b8c2374f553002789",
      "js/utils/LRCParser.js": "903b788e4ea511b9a135568a6e033dd72428a1fc4dd2df5d9b3e6d7642ef9a18",
      "js/utils/dom.js": "44d83e2794e69e2f3e5719168f909561da1df365d9fbf337ca990ab56e1ec9a7",
      "js/utils/escape.js": "a4904e0230938d34858da10713b9d1b80000916994d830bd9c4fc2269443e847",
      "js/utils/helpers.js": "d6942c9d3e06e15b8f337c7da16d1d7265a52c03036b9192f29c58d7a75ee975",
      "js/utils/storage.js": "646b92d420848a234395a374176db11280f3a4c0ce4fdf197f2f29570ff8b530"
    }
  },
  "scope": "Controlled component simulation using actual upstream modules; not full-player end-to-end, browser, layout, or playback testing.",
  "interventions": [
    "ReadingSystem subclass overrides only init() to suppress catalog/book boot.",
    "DOM double recognizes only the exact lyric-line wrapper emitted by upstream render; it is not a browser HTML parser.",
    "Audio double records currentTime, duration, play/pause/load and emitted events; it does not decode or play audio.",
    "Map-backed storage, deterministic Date.now and queued-but-not-automatically-fired timers replace browser state.",
    "fetch and global Audio construction throw; source modules are loaded only from local unchanged files."
  ],
  "fixture": "# Original synthetic input written for this component experiment.\n\n[00:02.50]The green lamp glows. | 绿灯亮着。\n[00:00.10]A small bell rings. | 小铃响了。\n[00:01.25]Place the blue tile here. | 把蓝色方块放这里。\n[00:02.500]The red tile stays. | 红色方块留在原处。\n[00:04.125]Turn the dial once. | 把旋钮转一次。\n[00:06.00]Our tiny test is done. | 小测试结束了。\n",
  "fixtureSha256": "caf770ccdf6d5267565b269bc47082900f6d9cc411bf912b31bf957996f14159",
  "tests": [
    {
      "group": "integrity",
      "name": "Unchanged LICENSE",
      "pass": true,
      "actual": "81467deceb4672ed5304e6d7751b7bdba03a7e69d9838c70bc3df779e1990a32",
      "expected": "81467deceb4672ed5304e6d7751b7bdba03a7e69d9838c70bc3df779e1990a32"
    },
    {
      "group": "integrity",
      "name": "Unchanged js/ReadingSystem.js",
      "pass": true,
      "actual": "ba71932549951e66a835cd2dfe7624533907e1cd73d2cd862a106d62bee80c52",
      "expected": "ba71932549951e66a835cd2dfe7624533907e1cd73d2cd862a106d62bee80c52"
    },
    {
      "group": "integrity",
      "name": "Unchanged js/config.js",
      "pass": true,
      "actual": "fb891186e2ff84b36ee7a1c8bd677b9ce1432c1096eae5b012191f11e65beb85",
      "expected": "fb891186e2ff84b36ee7a1c8bd677b9ce1432c1096eae5b012191f11e65beb85"
    },
    {
      "group": "integrity",
      "name": "Unchanged js/managers/CacheManager.js",
      "pass": true,
      "actual": "50f1d3736fa668c79cf8d1198bc56b577832cef83598c6a932b4f5b13d5dfe43",
      "expected": "50f1d3736fa668c79cf8d1198bc56b577832cef83598c6a932b4f5b13d5dfe43"
    },
    {
      "group": "integrity",
      "name": "Unchanged js/player/AudioController.js",
      "pass": true,
      "actual": "75d11d6383426228e9f63466f8008e421e560dfcfb4869e04d553926bd131a28",
      "expected": "75d11d6383426228e9f63466f8008e421e560dfcfb4869e04d553926bd131a28"
    },
    {
      "group": "integrity",
      "name": "Unchanged js/services/BookService.js",
      "pass": true,
      "actual": "fe42e20d623c229c64dcddf5913895b90650238fe1d35f66c7d0ec1fb9f37b95",
      "expected": "fe42e20d623c229c64dcddf5913895b90650238fe1d35f66c7d0ec1fb9f37b95"
    },
    {
      "group": "integrity",
      "name": "Unchanged js/services/PrefetchService.js",
      "pass": true,
      "actual": "11c206099dcdab93038c628b3fb34f7fe31e6bb9b94906491507ae37e31b5223",
      "expected": "11c206099dcdab93038c628b3fb34f7fe31e6bb9b94906491507ae37e31b5223"
    },
    {
      "group": "integrity",
      "name": "Unchanged js/ui/LyricsView.js",
      "pass": true,
      "actual": "cc40dab4d9b4784a14e9b0cdc15b7746a277a395363d0873bd90a5cfeb633e13",
      "expected": "cc40dab4d9b4784a14e9b0cdc15b7746a277a395363d0873bd90a5cfeb633e13"
    },
    {
      "group": "integrity",
      "name": "Unchanged js/ui/Toast.js",
      "pass": true,
      "actual": "dd7648aafcf7a600efb8deb65b7a29166bfb4a85676974c5757252e7fcb1f728",
      "expected": "dd7648aafcf7a600efb8deb65b7a29166bfb4a85676974c5757252e7fcb1f728"
    },
    {
      "group": "integrity",
      "name": "Unchanged js/ui/UnitView.js",
      "pass": true,
      "actual": "603f0fde725ed4ee90be2ad7acfb0479fc0467baa6ae640b8c2374f553002789",
      "expected": "603f0fde725ed4ee90be2ad7acfb0479fc0467baa6ae640b8c2374f553002789"
    },
    {
      "group": "integrity",
      "name": "Unchanged js/utils/LRCParser.js",
      "pass": true,
      "actual": "903b788e4ea511b9a135568a6e033dd72428a1fc4dd2df5d9b3e6d7642ef9a18",
      "expected": "903b788e4ea511b9a135568a6e033dd72428a1fc4dd2df5d9b3e6d7642ef9a18"
    },
    {
      "group": "integrity",
      "name": "Unchanged js/utils/dom.js",
      "pass": true,
      "actual": "44d83e2794e69e2f3e5719168f909561da1df365d9fbf337ca990ab56e1ec9a7",
      "expected": "44d83e2794e69e2f3e5719168f909561da1df365d9fbf337ca990ab56e1ec9a7"
    },
    {
      "group": "integrity",
      "name": "Unchanged js/utils/escape.js",
      "pass": true,
      "actual": "a4904e0230938d34858da10713b9d1b80000916994d830bd9c4fc2269443e847",
      "expected": "a4904e0230938d34858da10713b9d1b80000916994d830bd9c4fc2269443e847"
    },
    {
      "group": "integrity",
      "name": "Unchanged js/utils/helpers.js",
      "pass": true,
      "actual": "d6942c9d3e06e15b8f337c7da16d1d7265a52c03036b9192f29c58d7a75ee975",
      "expected": "d6942c9d3e06e15b8f337c7da16d1d7265a52c03036b9192f29c58d7a75ee975"
    },
    {
      "group": "integrity",
      "name": "Unchanged js/utils/storage.js",
      "pass": true,
      "actual": "646b92d420848a234395a374176db11280f3a4c0ce4fdf197f2f29570ff8b530",
      "expected": "646b92d420848a234395a374176db11280f3a4c0ce4fdf197f2f29570ff8b530"
    },
    {
      "group": "integrity",
      "name": "Exactly 14 upstream JavaScript modules",
      "pass": true,
      "actual": 14,
      "expected": 14
    },
    {
      "group": "parser",
      "name": "Six original records parsed",
      "pass": true,
      "actual": 6,
      "expected": 6
    },
    {
      "group": "parser",
      "name": "Sorted source order including equal timestamps",
      "pass": true,
      "actual": [
        "A small bell rings.",
        "Place the blue tile here.",
        "The green lamp glows.",
        "The red tile stays.",
        "Turn the dial once.",
        "Our tiny test is done."
      ],
      "expected": [
        "A small bell rings.",
        "Place the blue tile here.",
        "The green lamp glows.",
        "The red tile stays.",
        "Turn the dial once.",
        "Our tiny test is done."
      ]
    },
    {
      "group": "parser",
      "name": "Unsupported formats, metadata and empty English are ignored",
      "pass": true,
      "actual": [],
      "expected": [],
      "input": "# comment\n\n[00:01]Missing fraction.\n[00:01.1]One fraction digit.\n[00:60.00]Invalid seconds.\n[100:00.00]Three minute digits.\n[00:01.0000]Four fraction digits.\n[00:02.00] | Only right side.\n[ar:Original test]\n[offset:500]"
    },
    {
      "group": "parser",
      "name": "Null and nonstring inputs return empty arrays",
      "pass": true,
      "actual": [
        [],
        [],
        [],
        []
      ],
      "expected": [
        [],
        [],
        [],
        []
      ]
    },
    {
      "group": "parser",
      "name": "One-digit minutes, CRLF and optional translation",
      "pass": true,
      "actual": [
        {
          "time": 1.2,
          "english": "Solo.",
          "chinese": "",
          "fullText": "Solo."
        },
        {
          "time": 2.125,
          "english": "Left",
          "chinese": "Right",
          "fullText": "Left | Right | Tail"
        }
      ],
      "expected": [
        {
          "time": 1.2,
          "english": "Solo.",
          "chinese": "",
          "fullText": "Solo."
        },
        {
          "time": 2.125,
          "english": "Left",
          "chinese": "Right",
          "fullText": "Left | Right | Tail"
        }
      ],
      "input": "[0:01.20] Solo.\r\n[00:02.125]Left | Right | Tail",
      "classification": "Extra pipe segments remain only in fullText."
    },
    {
      "group": "parser",
      "name": "Multiple timestamps are not expanded",
      "pass": true,
      "actual": [
        {
          "time": 1,
          "english": "[00:02.00]Marker stays.",
          "chinese": "",
          "fullText": "[00:02.00]Marker stays."
        }
      ],
      "expected": [
        {
          "time": 1,
          "english": "[00:02.00]Marker stays.",
          "chinese": "",
          "fullText": "[00:02.00]Marker stays."
        }
      ],
      "input": "[00:01.00][00:02.00]Marker stays."
    },
    {
      "group": "timeline",
      "name": "Configured offset is 0.3 seconds",
      "pass": true,
      "actual": 0.3,
      "expected": 0.3
    },
    {
      "group": "timeline",
      "name": "Parser default is no offset",
      "pass": true,
      "actual": [
        0.1,
        1.25,
        2.5,
        2.5,
        4.125,
        6
      ],
      "expected": [
        0.1,
        1.25,
        2.5,
        2.5,
        4.125,
        6
      ]
    },
    {
      "group": "timeline",
      "name": "App offset subtracts and preserves a negative first timestamp",
      "pass": true,
      "actual": [
        -0.2,
        0.95,
        2.2,
        2.2,
        3.825,
        5.7
      ],
      "expected": [
        -0.2,
        0.95,
        2.2,
        2.2,
        3.825,
        5.7
      ]
    },
    {
      "group": "timeline",
      "name": "Inclusive exact-time lookup and last-duplicate selection",
      "pass": true,
      "actual": [
        -1,
        0,
        0,
        0,
        1,
        1,
        3,
        3,
        4,
        5,
        5
      ],
      "expected": [
        -1,
        0,
        0,
        0,
        1,
        1,
        3,
        3,
        4,
        5,
        5
      ],
      "input": [
        -0.201,
        -0.2,
        0,
        0.949,
        0.95,
        2.199,
        2.2,
        3.824,
        3.825,
        5.7,
        8
      ]
    },
    {
      "group": "timeline",
      "name": "Empty lookup returns -1",
      "pass": true,
      "actual": -1,
      "expected": -1
    },
    {
      "group": "timeline",
      "name": "First duplicate has zero-length interval",
      "pass": true,
      "actual": {
        "startTime": 2.2,
        "endTime": 2.2,
        "index": 2
      },
      "expected": {
        "startTime": 2.2,
        "endTime": 2.2,
        "index": 2
      },
      "classification": "Observed edge behavior, not fixed."
    },
    {
      "group": "timeline",
      "name": "Second duplicate spans until next timestamp",
      "pass": true,
      "actual": {
        "startTime": 2.2,
        "endTime": 3.825,
        "index": 3
      },
      "expected": {
        "startTime": 2.2,
        "endTime": 3.825,
        "index": 3
      }
    },
    {
      "group": "timeline",
      "name": "Last line uses provided duration",
      "pass": true,
      "actual": {
        "startTime": 5.7,
        "endTime": 8,
        "index": 5
      },
      "expected": {
        "startTime": 5.7,
        "endTime": 8,
        "index": 5
      }
    },
    {
      "group": "timeline",
      "name": "Without duration, last line gets minimum 0.1 seconds",
      "pass": true,
      "actual": {
        "startTime": 5.7,
        "endTime": 5.8,
        "index": 5
      },
      "expected": {
        "startTime": 5.7,
        "endTime": 5.8,
        "index": 5
      }
    },
    {
      "group": "timeline",
      "name": "Invalid out-of-range boundaries return null",
      "pass": true,
      "actual": [
        null,
        null
      ],
      "expected": [
        null,
        null
      ]
    },
    {
      "group": "controller",
      "name": "Known-duration seek(-0.2)",
      "pass": true,
      "actual": 0,
      "expected": 0
    },
    {
      "group": "controller",
      "name": "Known-duration seek(2.2)",
      "pass": true,
      "actual": 2.2,
      "expected": 2.2
    },
    {
      "group": "controller",
      "name": "Known-duration seek(99)",
      "pass": true,
      "actual": 8,
      "expected": 8
    },
    {
      "group": "controller",
      "name": "Nonfinite seek is ignored",
      "pass": true,
      "actual": 8,
      "expected": 8
    },
    {
      "group": "controller",
      "name": "Unknown-duration direct negative seek assigns a negative value in the double",
      "pass": true,
      "actual": -0.2,
      "expected": -0.2,
      "classification": "Observed controller assignment only. Real HTMLMediaElement behavior untested."
    },
    {
      "group": "controller",
      "name": "Progress midpoint click seeks to media midpoint",
      "pass": true,
      "actual": 4,
      "expected": 4
    },
    {
      "group": "controller",
      "name": "Seek updates progress without invoking onTick",
      "pass": true,
      "actual": {
        "progress": "50%",
        "ticks": 0
      },
      "expected": {
        "progress": "50%",
        "ticks": 0
      }
    },
    {
      "group": "controller",
      "name": "Pointer drag reaches media end",
      "pass": true,
      "actual": {
        "current": 8,
        "dragging": true
      },
      "expected": {
        "current": 8,
        "dragging": true
      }
    },
    {
      "group": "controller",
      "name": "Pointer cancel ends dragging and persists",
      "pass": true,
      "actual": {
        "dragging": false,
        "stored": 8
      },
      "expected": {
        "dragging": false,
        "stored": 8
      }
    },
    {
      "group": "controller",
      "name": "Same-clock tick suppressed by actual throttle",
      "pass": true,
      "actual": [
        [
          1.25,
          8
        ]
      ],
      "expected": [
        [
          1.25,
          8
        ]
      ]
    },
    {
      "group": "controller",
      "name": "Later tick reads current media time",
      "pass": true,
      "actual": [
        2,
        8
      ],
      "expected": [
        2,
        8
      ]
    },
    {
      "group": "controller",
      "name": "Playback rate changes without rewriting source time",
      "pass": true,
      "actual": {
        "rate": 2,
        "time": 2
      },
      "expected": {
        "rate": 2,
        "time": 2
      }
    },
    {
      "group": "controller",
      "name": "Restored position stays 0.05 seconds before end",
      "pass": true,
      "actual": {
        "time": 7.95,
        "rate": 1.25,
        "loop": true,
        "disabled": false
      },
      "expected": {
        "time": 7.95,
        "rate": 1.25,
        "loop": true,
        "disabled": false
      }
    },
    {
      "group": "controller",
      "name": "Destroyed controller does not deliver new tick",
      "pass": true,
      "actual": 2,
      "expected": 2
    },
    {
      "group": "view",
      "name": "Actual render emits six line wrappers",
      "pass": true,
      "actual": 6,
      "expected": 6
    },
    {
      "group": "view",
      "name": "Rendered data-time preserves offset",
      "pass": true,
      "actual": [
        "-0.2",
        "0.95",
        "2.2",
        "2.2",
        "3.825",
        "5.7"
      ],
      "expected": [
        "-0.2",
        "0.95",
        "2.2",
        "2.2",
        "3.825",
        "5.7"
      ]
    },
    {
      "group": "view",
      "name": "Highlight removes old active class",
      "pass": true,
      "actual": [
        1
      ],
      "expected": [
        1
      ]
    },
    {
      "group": "view",
      "name": "Off-threshold line requests scroll",
      "pass": true,
      "actual": [
        {
          "behavior": "smooth",
          "block": "center"
        }
      ],
      "expected": [
        {
          "behavior": "smooth",
          "block": "center"
        }
      ],
      "classification": "Method call only; visual scroll unverified."
    },
    {
      "group": "view",
      "name": "Repeated highlight requests no extra scroll",
      "pass": true,
      "actual": 1,
      "expected": 1
    },
    {
      "group": "view",
      "name": "Negative index removes active class",
      "pass": true,
      "actual": [],
      "expected": []
    },
    {
      "group": "view",
      "name": "Click, Enter and Space activate actual callback",
      "pass": true,
      "actual": [
        [
          1,
          0.95
        ],
        [
          3,
          2.2
        ],
        [
          4,
          3.825
        ]
      ],
      "expected": [
        [
          1,
          0.95
        ],
        [
          3,
          2.2
        ],
        [
          4,
          3.825
        ]
      ]
    },
    {
      "group": "view",
      "name": "Enter and Space prevent default",
      "pass": true,
      "actual": [
        true,
        true
      ],
      "expected": [
        true,
        true
      ]
    },
    {
      "group": "view",
      "name": "Text is escaped by actual render helper",
      "pass": true,
      "actual": true,
      "expected": true
    },
    {
      "group": "view",
      "name": "Empty lyrics clear lines",
      "pass": true,
      "actual": {
        "lines": 0,
        "index": -1
      },
      "expected": {
        "lines": 0,
        "index": -1
      }
    },
    {
      "group": "integration",
      "name": "Only init is overridden",
      "pass": true,
      "actual": [
        "constructor",
        "init"
      ],
      "expected": [
        "constructor",
        "init"
      ]
    },
    {
      "group": "integration",
      "name": "Catalog boot suppressed",
      "pass": true,
      "actual": true,
      "expected": true
    },
    {
      "group": "integration",
      "name": "Normal timeline highlights early-offset first line at t=0",
      "pass": true,
      "actual": 0,
      "expected": 0
    },
    {
      "group": "integration",
      "name": "Normal timeline changes exactly at boundary",
      "pass": true,
      "actual": 1,
      "expected": 1
    },
    {
      "group": "integration",
      "name": "Normal timeline picks last duplicate at exact boundary",
      "pass": true,
      "actual": {
        "index": 3,
        "active": [
          3
        ]
      },
      "expected": {
        "index": 3,
        "active": [
          3
        ]
      }
    },
    {
      "group": "integration",
      "name": "Actual click chain highlights, seeks and calls play",
      "pass": true,
      "actual": {
        "time": 0.95,
        "index": 1,
        "paused": false,
        "persisted": "0.95"
      },
      "expected": {
        "time": 0.95,
        "index": 1,
        "paused": false,
        "persisted": "0.95"
      }
    },
    {
      "group": "integration",
      "name": "Direct seek does not immediately synchronize highlight",
      "pass": true,
      "actual": 1,
      "expected": 1,
      "classification": "Observed event timing: seek updates progress; highlight waits for next tick."
    },
    {
      "group": "integration",
      "name": "Next audio tick synchronizes highlight",
      "pass": true,
      "actual": 4,
      "expected": 4
    },
    {
      "group": "integration",
      "name": "Negative parsed timestamp click is clamped with known duration",
      "pass": true,
      "actual": {
        "parsed": -0.2,
        "media": 0,
        "index": 0
      },
      "expected": {
        "parsed": -0.2,
        "media": 0,
        "index": 0
      }
    },
    {
      "group": "integration",
      "name": "Click mode remains playing before sentence end",
      "pass": true,
      "actual": {
        "time": 2.199,
        "index": 1,
        "paused": false
      },
      "expected": {
        "time": 2.199,
        "index": 1,
        "paused": false
      }
    },
    {
      "group": "integration",
      "name": "Click mode resets and pauses at exact sentence end",
      "pass": true,
      "actual": {
        "time": 0.95,
        "index": 1,
        "paused": true
      },
      "expected": {
        "time": 0.95,
        "index": 1,
        "paused": true
      }
    },
    {
      "group": "integration",
      "name": "One mode resets at end without pausing",
      "pass": true,
      "actual": {
        "time": 0.95,
        "index": 1,
        "paused": false
      },
      "expected": {
        "time": 0.95,
        "index": 1,
        "paused": false
      }
    },
    {
      "group": "integration",
      "name": "First duplicate in click mode pauses on first same-time tick",
      "pass": true,
      "actual": {
        "time": 2.2,
        "index": 2,
        "paused": true
      },
      "expected": {
        "time": 2.2,
        "index": 2,
        "paused": true
      },
      "classification": "Zero-length interval observed; no automatic repair."
    },
    {
      "group": "integration",
      "name": "Last click-mode sentence stops at known media duration",
      "pass": true,
      "actual": {
        "time": 5.7,
        "index": 5,
        "paused": true
      },
      "expected": {
        "time": 5.7,
        "index": 5,
        "paused": true
      }
    },
    {
      "group": "integration",
      "name": "Destroyed actual system has no new timeline callbacks",
      "pass": true,
      "actual": 5,
      "expected": 5
    },
    {
      "group": "safety",
      "name": "No fetch or uncontrolled Audio construction attempted",
      "pass": true,
      "actual": [],
      "expected": []
    }
  ],
  "traces": {
    "parsedFixture": [
      {
        "time": -0.2,
        "english": "A small bell rings.",
        "chinese": "小铃响了。",
        "fullText": "A small bell rings. | 小铃响了。"
      },
      {
        "time": 0.95,
        "english": "Place the blue tile here.",
        "chinese": "把蓝色方块放这里。",
        "fullText": "Place the blue tile here. | 把蓝色方块放这里。"
      },
      {
        "time": 2.2,
        "english": "The green lamp glows.",
        "chinese": "绿灯亮着。",
        "fullText": "The green lamp glows. | 绿灯亮着。"
      },
      {
        "time": 2.2,
        "english": "The red tile stays.",
        "chinese": "红色方块留在原处。",
        "fullText": "The red tile stays. | 红色方块留在原处。"
      },
      {
        "time": 3.825,
        "english": "Turn the dial once.",
        "chinese": "把旋钮转一次。",
        "fullText": "Turn the dial once. | 把旋钮转一次。"
      },
      {
        "time": 5.7,
        "english": "Our tiny test is done.",
        "chinese": "小测试结束了。",
        "fullText": "Our tiny test is done. | 小测试结束了。"
      }
    ],
    "controller": {
      "calls": [
        {
          "action": "pause",
          "time": 2
        },
        {
          "action": "load",
          "src": "synthetic://no-real-media"
        },
        {
          "action": "pause",
          "time": 7.95
        },
        {
          "action": "load",
          "src": ""
        }
      ],
      "ticks": [
        [
          1.25,
          8
        ],
        [
          2,
          8
        ]
      ],
      "persistedTimes": [
        8
      ]
    },
    "view": {
      "activations": [
        [
          1,
          0.95
        ],
        [
          3,
          2.2
        ],
        [
          4,
          3.825
        ]
      ],
      "escapedHtml": "<div class=\"lyric-line\" data-index=\"0\" data-time=\"0\" tabindex=\"0\" role=\"button\" aria-label=\"播放第 1 句\">\n            <div class=\"lyric-text\">&lt;b&gt;Tile&lt;/b&gt; &amp; &quot;Lamp&quot;</div>\n            <div class=\"lyric-translation\">&lt;i&gt;标记&lt;/i&gt;</div>\n          </div>"
    },
    "integration": [
      {
        "action": "tick 0",
        "mediaTime": 0,
        "index": 0,
        "active": [
          0
        ],
        "mode": "off",
        "locked": -1,
        "paused": true
      },
      {
        "action": "tick 0.95",
        "mediaTime": 0.95,
        "index": 1,
        "active": [
          1
        ],
        "mode": "off",
        "locked": -1,
        "paused": true
      },
      {
        "action": "tick 2.2",
        "mediaTime": 2.2,
        "index": 3,
        "active": [
          3
        ],
        "mode": "off",
        "locked": -1,
        "paused": true
      },
      {
        "action": "click line 1",
        "mediaTime": 0.95,
        "index": 1,
        "active": [
          1
        ],
        "mode": "off",
        "locked": -1,
        "paused": false
      },
      {
        "action": "direct seek 3.825",
        "mediaTime": 3.825,
        "index": 1,
        "active": [
          1
        ],
        "mode": "off",
        "locked": -1,
        "paused": false
      },
      {
        "action": "tick after seek",
        "mediaTime": 3.825,
        "index": 4,
        "active": [
          4
        ],
        "mode": "off",
        "locked": -1,
        "paused": false
      },
      {
        "action": "click negative-offset line",
        "mediaTime": 0,
        "index": 0,
        "active": [
          0
        ],
        "mode": "off",
        "locked": -1,
        "paused": false
      },
      {
        "action": "click mode before end",
        "mediaTime": 2.199,
        "index": 1,
        "active": [
          1
        ],
        "mode": "click",
        "locked": 1,
        "paused": false
      },
      {
        "action": "click mode exact end",
        "mediaTime": 0.95,
        "index": 1,
        "active": [
          1
        ],
        "mode": "click",
        "locked": 1,
        "paused": true
      },
      {
        "action": "one mode exact end",
        "mediaTime": 0.95,
        "index": 1,
        "active": [
          1
        ],
        "mode": "one",
        "locked": 1,
        "paused": false
      },
      {
        "action": "click zero-length duplicate",
        "mediaTime": 2.2,
        "index": 2,
        "active": [
          2
        ],
        "mode": "click",
        "locked": 2,
        "paused": true
      },
      {
        "action": "last sentence end",
        "mediaTime": 5.7,
        "index": 5,
        "active": [
          5
        ],
        "mode": "click",
        "locked": 5,
        "paused": true
      }
    ],
    "integrationAudioCalls": [
      {
        "action": "play",
        "time": 0.95
      },
      {
        "action": "play",
        "time": 0
      },
      {
        "action": "play",
        "time": 0.95
      },
      {
        "action": "pause",
        "time": 0.95
      },
      {
        "action": "play",
        "time": 0.95
      },
      {
        "action": "play",
        "time": 2.2
      },
      {
        "action": "pause",
        "time": 2.2
      },
      {
        "action": "play",
        "time": 5.7
      },
      {
        "action": "pause",
        "time": 5.7
      },
      {
        "action": "pause",
        "time": 5.7
      },
      {
        "action": "load",
        "src": ""
      }
    ],
    "storage": {
      "ORIGINAL_SYNTHETIC/0/playTime": "5.7"
    }
  },
  "networkAttempts": [],
  "limitations": [
    "No actual audio downloaded, generated, decoded or heard.",
    "No browser opened, localhost server started or HTML visual inspection performed.",
    "No rendering quality, media seek precision, autoplay policy, CORS, fetch integration, network cancellation or real event cadence verified."
  ],
  "finishedAt": "2026-10-05T09:59:35.296Z",
  "summary": {
    "passed": 72,
    "failed": 0,
    "assertions": 72,
    "groups": [
      "integrity",
      "parser",
      "timeline",
      "controller",
      "view",
      "integration",
      "safety"
    ],
    "verifiedUpstreamFiles": 15
  }
}
```

## 结果解释与限制

首句时间从 0.1 变为 -0.2，正偏移使标签提前。精确 2.2 秒选择索引 3，而索引 2 的起止相同。已知正时长的 seek 将负值夹到 0；未知时长的负值分支仍可向替身写负数，真实媒体处理未测。直接 seek 不立即同步高亮；下一次 timeupdate 才更新。click 到句尾回到句首并暂停，one 回到句首并继续。

本日志不证明媒体内容准确、字幕真实同步、UI 像素布局、声音品质、学习效果、网络取消竞态、跨设备存储或浏览器自动播放政策。教材、原版音频、外部翻译没有随包分发。

## 历史制作检查

2026-10-05 的原指南使用直接 ReportLab PDF 流程；HTML 仅结构检查，不进行浏览器预览。作者已将最终 A4 PDF 的全部 11 页渲染为 PNG，并逐页实际查看：正文、命令、图示、页码均可读，未发现截断、重叠或缺字。HTML 用标准库 HTMLParser 检查到 12 个问题卡、12 张内联 SVG、6 步命令、12 个有效目录目标，未作浏览器视觉预览。独立审核结果另见审核日志。


## 当前公开副本说明

当前指南重新由 ReportLab 直接生成；HTML 仅做结构检查。HTML 浏览器视觉与 HTML 转 PDF 原路线受环境限制，本次未重试。当前 PDF 的逐页检查和公开副本审核范围另见独立审核日志。ZIP 中唯一变化为 README 的公开副本说明；七份 JSON 结果、实验脚本、原创样例、14 个上游模块与 MIT 许可均未修改，也未重新执行。

当前公开 ZIP：61578 字节；SHA-256 b3476ca284771a9899a66a63b8a6138ed0f87c4b59535da8b4cdc88f342f7d74
