# hand-drawn-styles 实验日志

范围：固定上游Python文本渲染、输入拒绝与原创PNG校验的离线实验。没有真实锚点下载、图像模型/API/付费服务、真实个人图片、生产图像验收或全局skill安装。HTML浏览器与HTML转PDF沿既有受阻路径未重试；PDF直接由ReportLab生成并逐页渲染审核。

上游 4132988b8596bfa36321c970a4472d4e3bb25d96

执行入口在exercise目录，环境变量HAND_DRAWN_OFFLINE=1和独立empty-cache由lab.py设置；不会联网下载参考图。

## 列菜单并固定版本

命令：python -B lab.py catalog

目的/实际结果：实际得到21种唯一配方编号，含3.1；3个检查通过。

失败条件：数量不符或退出码非0即失败。

```json

{
  "step": "catalog",
  "startUtc": "2026-10-11T07:49:05.751851+00:00",
  "endUtc": "2026-10-11T07:49:05.834424+00:00",
  "checks": [
    {
      "check": "exit --list",
      "passed": true
    },
    {
      "check": "21 unique style identifiers",
      "passed": true
    },
    {
      "check": "3.1 included",
      "passed": true
    }
  ],
  "result": {
    "styleCount": 21,
    "ids": [
      "1",
      "2",
      "3",
      "3.1",
      "4",
      "5",
      "6",
      "7",
      "8",
      "9",
      "10",
      "11",
      "12",
      "13",
      "14",
      "15",
      "16",
      "17",
      "18",
      "19",
      "20"
    ],
    "python": "3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]",
    "catalog": [
      {
        "style_id": "1",
        "name": "极简黑白线条讲解漫画(xkcd 火柴人)",
        "aliases": [
          "minimal-line",
          "stickman",
          "xkcd",
          "极简线条",
          "火柴人"
        ],
        "parameters": [
          "N",
          "分镜列表"
        ],
        "references": []
      },
      {
        "style_id": "2",
        "name": "蜡笔童涂(5岁小孩坏画)",
        "aliases": [
          "crayon",
          "kid-crayon",
          "蜡笔童涂"
        ],
        "parameters": [
          "主体",
          "主色调",
          "标题词"
        ],
        "references": []
      },
      {
        "style_id": "3",
        "name": "吉卜力风",
        "aliases": [
          "ghibli",
          "吉卜力",
          "吉卜力风"
        ],
        "parameters": [
          "主体"
        ],
        "references": []
      },
      {
        "style_id": "3.1",
        "name": "蜡笔童涂-潦草自画版",
        "aliases": [
          "family-crayon-card",
          "kid-scrawl",
          "parent-child-crayon",
          "rawkid",
          "stick-kid",
          "submission-crayon",
          "亲子手绘",
          "亲子投稿蜡笔故事卡",
          "亲子蜡笔故事",
          "家庭投稿蜡笔卡",
          "家庭蜡笔画",
          "潦草自画版",
          "蜡笔童涂-潦草自画版",
          "蜡笔童涂潦草版"
        ],
        "parameters": [
          "主体",
          "文字"
        ],
        "references": [
          "https://gentle-starburst-99bd99.netlify.app/hand-drawn/assets/style-3.1/anchor-family.png"
        ]
      },
      {
        "style_id": "4",
        "name": "小豆人黑色涂鸦信息图",
        "aliases": [
          "bean",
          "blob",
          "小豆人",
          "小豆人涂鸦信息图"
        ],
        "parameters": [
          "N",
          "分镜列表"
        ],
        "references": []
      },
      {
        "style_id": "5",
        "name": "MS Paint 烂涂鸦(the worse, the better)",
        "aliases": [
          "bad-doodle",
          "ms paint",
          "ms-paint",
          "ugly"
        ],
        "parameters": [
          "主体"
        ],
        "references": []
      },
      {
        "style_id": "6",
        "name": "圆珠笔单线涂鸦(scribble)",
        "aliases": [
          "ballpoint",
          "pen-scribble",
          "scribble",
          "圆珠笔"
        ],
        "parameters": [
          "主体"
        ],
        "references": []
      },
      {
        "style_id": "7",
        "name": "蜡笔实拍(真·儿童手涂纸张)",
        "aliases": [
          "crayon-photo",
          "real-crayon",
          "蜡笔实拍"
        ],
        "parameters": [
          "主体",
          "主色调",
          "标题词"
        ],
        "references": []
      },
      {
        "style_id": "8",
        "name": "水墨写意",
        "aliases": [
          "chinese-painting",
          "ink",
          "ink-wash",
          "shuimo",
          "水墨"
        ],
        "parameters": [
          "主体"
        ],
        "references": []
      },
      {
        "style_id": "9",
        "name": "复古像素",
        "aliases": [
          "16-bit",
          "8-bit",
          "pixel",
          "pixel-art",
          "像素"
        ],
        "parameters": [
          "主体",
          "主色调"
        ],
        "references": []
      },
      {
        "style_id": "10",
        "name": "情绪叙事淡彩速写",
        "aliases": [
          "emo-sketch",
          "light-watercolor",
          "story-sketch",
          "watercolor-sketch",
          "情绪叙事",
          "淡彩速写"
        ],
        "parameters": [
          "主体",
          "文字",
          "橙色关键物"
        ],
        "references": []
      },
      {
        "style_id": "11",
        "name": "二维水彩风格(复古动画概念稿)",
        "aliases": [
          "concept-art",
          "gouache-concept",
          "mid-century",
          "retro-concept",
          "二维水彩"
        ],
        "parameters": [
          "主体",
          "文字",
          "构图",
          "焦点物件",
          "背景浓度"
        ],
        "references": []
      },
      {
        "style_id": "12",
        "name": "暖光童画(动画概念暖绘)",
        "aliases": [
          "storybook-visdev",
          "sunlit-storybook",
          "vis-dev",
          "暖光童画"
        ],
        "parameters": [
          "主体",
          "场景",
          "文字",
          "构图"
        ],
        "references": []
      },
      {
        "style_id": "13",
        "name": "北欧纸雕(paper-folk)",
        "aliases": [
          "nordic-papercraft",
          "paper-folk",
          "paper-sculpture",
          "papercraft",
          "quilling",
          "剪纸民俗",
          "北欧纸雕"
        ],
        "parameters": [
          "主体",
          "底色",
          "构图",
          "点缀元素"
        ],
        "references": [
          "https://gentle-starburst-99bd99.netlify.app/hand-drawn/examples/13-paper-folk-musician.png",
          "https://gentle-starburst-99bd99.netlify.app/hand-drawn/examples/13-paper-folk.png"
        ]
      },
      {
        "style_id": "14",
        "name": "北欧绘本水粉(nordic-storybook)",
        "aliases": [
          "nordic-storybook",
          "scandi-gouache",
          "scandinavian-storybook",
          "soft-gouache",
          "北欧绘本水粉"
        ],
        "parameters": [
          "主体",
          "光影",
          "构图",
          "纸底色"
        ],
        "references": []
      },
      {
        "style_id": "15",
        "name": "大鼻软偶(softnose-vinyl)",
        "aliases": [
          "art-toy",
          "bignose-toy",
          "softnose",
          "softnose-vinyl",
          "vinyl-toy",
          "大鼻软偶"
        ],
        "parameters": [
          "主体",
          "构图",
          "眼型",
          "穿搭",
          "肤色",
          "背景底色",
          "胡茬"
        ],
        "references": []
      },
      {
        "style_id": "16",
        "name": "聚光水粉立绘(gouache-spotlight)",
        "aliases": [
          "character-spotlight",
          "gouache-spotlight",
          "spotlight-gouache",
          "聚光水粉立绘"
        ],
        "parameters": [
          "主体",
          "文字",
          "构图",
          "背景色"
        ],
        "references": []
      },
      {
        "style_id": "17",
        "name": "墨线绘本(inked-storybook)",
        "aliases": [
          "ink-storybook",
          "inked-storybook",
          "sketch-storybook",
          "storybook-ink",
          "墨线绘本"
        ],
        "parameters": [
          "主体",
          "文字",
          "构图",
          "背景色",
          "配色"
        ],
        "references": []
      },
      {
        "style_id": "18",
        "name": "暖色扁平绘本(warm-flat-storybook)",
        "aliases": [
          "flat-storybook",
          "geometric-storybook",
          "warm-flat",
          "warm-flat-storybook",
          "暖色扁平绘本"
        ],
        "parameters": [
          "主体",
          "文字",
          "构图"
        ],
        "references": []
      },
      {
        "style_id": "19",
        "name": "圆头红线极简童画(roundhead-redline)",
        "aliases": [
          "graphite-redline",
          "redline-roundhead",
          "roundhead-redline",
          "圆头红线",
          "圆头红线极简童画",
          "黑红白圆头童画"
        ],
        "parameters": [
          "主体",
          "文字"
        ],
        "references": [
          "https://gentle-starburst-99bd99.netlify.app/hand-drawn/assets/style-19/anchor-roundhead-redline.png"
        ]
      },
      {
        "style_id": "20",
        "name": "暖黄墨线情绪小剧场(warm-yellow-ink-story)",
        "aliases": [
          "mustard-ink-story",
          "warm-yellow-ink-story",
          "yellow-ink-story",
          "暖黄墨线",
          "暖黄墨线情绪小剧场"
        ],
        "parameters": [
          "主体",
          "文字"
        ],
        "references": [
          "https://gentle-starburst-99bd99.netlify.app/hand-drawn/assets/style-20/anchor-warm-yellow-ink-story.png"
        ]
      }
    ]
  }
}


```

## 编号与别名、单次替换

命令：python -B lab.py template

目的/实际结果：编号1与xkcd输出字节一致；【短句】和固定标点标签保留；6个检查通过。

失败条件：输出不同、剩余原参数或丢失文字即失败。

```json

{
  "step": "template",
  "startUtc": "2026-10-11T07:49:05.898790+00:00",
  "endUtc": "2026-10-11T07:49:06.027528+00:00",
  "checks": [
    {
      "check": "exit --style 1 --var N=3 --var '分镜列表=IMU测量【短句】；驱动读取；定位融合'",
      "passed": true
    },
    {
      "check": "exit --style xkcd --var N=3 --var '分镜列表=IMU测量【短句】；驱动读取；定位融合'",
      "passed": true
    },
    {
      "check": "alias byte equivalent",
      "passed": true
    },
    {
      "check": "literal user brackets preserved",
      "passed": true
    },
    {
      "check": "fixed punctuation label preserved",
      "passed": true
    },
    {
      "check": "declared slots filled",
      "passed": true
    }
  ],
  "result": {
    "equal": true,
    "promptSha256": "8352b22872f87cafa955176d5852bfc73403821f5e22a356c3d06d28fb155b6e"
  }
}


```

## 四类输入反例

命令：python -B lab.py guards

目的/实际结果：缺参数、未知参数、未知编号、空参数均退出2并给具体错误，输出为空；12个检查通过。

失败条件：任一反例被接受或错误消息不符即失败。

```json

{
  "step": "guards",
  "startUtc": "2026-10-11T07:49:06.095922+00:00",
  "endUtc": "2026-10-11T07:49:06.355402+00:00",
  "checks": [
    {
      "check": "exit --style 1 --var N=3",
      "passed": true
    },
    {
      "check": "diagnostic 缺少占位符",
      "passed": true
    },
    {
      "check": "no output on rejection",
      "passed": true
    },
    {
      "check": "exit --style 1 --var N=3 --var '分镜列表=测试' --var '多余=内容'",
      "passed": true
    },
    {
      "check": "diagnostic 配方不包含",
      "passed": true
    },
    {
      "check": "no output on rejection",
      "passed": true
    },
    {
      "check": "exit --style 999",
      "passed": true
    },
    {
      "check": "diagnostic 不存在画风",
      "passed": true
    },
    {
      "check": "no output on rejection",
      "passed": true
    },
    {
      "check": "exit --style 1 --var N=",
      "passed": true
    },
    {
      "check": "diagnostic 不能为空",
      "passed": true
    },
    {
      "check": "no output on rejection",
      "passed": true
    }
  ],
  "result": {
    "cases": [
      {
        "args": [
          "--style",
          "1",
          "--var",
          "N=3"
        ],
        "exit": 2,
        "stderr": "render_prompt: 缺少占位符: 分镜列表\n"
      },
      {
        "args": [
          "--style",
          "1",
          "--var",
          "N=3",
          "--var",
          "分镜列表=测试",
          "--var",
          "多余=内容"
        ],
        "exit": 2,
        "stderr": "render_prompt: 配方不包含这些占位符: 多余\n"
      },
      {
        "args": [
          "--style",
          "999"
        ],
        "exit": 2,
        "stderr": "render_prompt: STYLES.md 中不存在画风 999 的代码块配方\n"
      },
      {
        "args": [
          "--style",
          "1",
          "--var",
          "N="
        ],
        "exit": 2,
        "stderr": "render_prompt: --var 的名称和内容都不能为空: N=\n"
      }
    ]
  }
}


```

## 比例正反对照

命令：python -B lab.py aspect

目的/实际结果：无比例、16:9、not-a-ratio三次均退出0；上游接受任意比例文本的边界被保留；6个检查通过。

失败条件：输出与观察预期不符即失败；不把任意字符串接受当有效比例。

```json

{
  "step": "aspect",
  "startUtc": "2026-10-11T07:49:06.425066+00:00",
  "endUtc": "2026-10-11T07:49:06.613550+00:00",
  "checks": [
    {
      "check": "exit --style 1 --var N=3 --var '分镜列表=测量；传输；融合'",
      "passed": true
    },
    {
      "check": "exit --style 1 --var N=3 --var '分镜列表=测量；传输；融合' --aspect 16:9",
      "passed": true
    },
    {
      "check": "exit --style 1 --var N=3 --var '分镜列表=测量；传输；融合' --aspect not-a-ratio",
      "passed": true
    },
    {
      "check": "no numeric aspect automatically appended",
      "passed": true
    },
    {
      "check": "explicit aspect appended",
      "passed": true
    },
    {
      "check": "arbitrary aspect accepted by upstream",
      "passed": true
    }
  ],
  "result": {
    "noAspectSuffix": true,
    "explicitAspect": true,
    "arbitraryAspectAccepted": true,
    "limit": "CLI appends arbitrary aspect; consumer validation still needed. No model call."
  }
}


```

## 正式路径缺条件时拒绝

命令：python -B lab.py offline

目的/实际结果：独立空缓存离线：缺锚点JSON与未批准纯文本生产均退出2；5个检查通过。

失败条件：不得产生正式payload或自行下载/退回生产预览。

```json

{
  "step": "offline",
  "startUtc": "2026-10-11T07:49:06.681131+00:00",
  "endUtc": "2026-10-11T07:49:06.808450+00:00",
  "checks": [
    {
      "check": "exit --style 19 --subject 'a robot holding a lantern' --format json",
      "passed": true
    },
    {
      "check": "missing cache fails closed",
      "passed": true
    },
    {
      "check": "no production payload",
      "passed": true
    },
    {
      "check": "exit --style 19 --subject 'a robot holding a lantern' --format text",
      "passed": true
    },
    {
      "check": "text-only production refused",
      "passed": true
    }
  ],
  "result": {
    "missingAnchorExit": 2,
    "textOnlyExit": 2,
    "scope": "Expected negative tests only. No reference downloads, production image or API call."
  }
}


```

## 文件与像素指纹分层

命令：python -B lab.py integrity

目的/实际结果：原创2×2 PNG：元数据改变文件hash不改变像素hash，像素改变则hash变；错误字节被拒；5个检查通过。

失败条件：任何相等/不等关系与预期不符或错误字节被接受即失败。

```json

{
  "step": "integrity",
  "startUtc": "2026-10-11T07:49:06.874852+00:00",
  "endUtc": "2026-10-11T07:49:06.875639+00:00",
  "checks": [
    {
      "check": "file hash changes with metadata",
      "passed": true
    },
    {
      "check": "pixel hash unchanged by metadata",
      "passed": true
    },
    {
      "check": "pixel hash changes with pixels",
      "passed": true
    },
    {
      "check": "valid bytes accepted",
      "passed": true
    },
    {
      "check": "changed bytes rejected",
      "passed": true
    }
  ],
  "result": {
    "fixtureDimensions": [
      2,
      2
    ],
    "pixelSha256": "e0c644c801cee721861b30d6a9e7f172ad8459cff1ef21ce9b29d2c890ace689",
    "metadataPixelSha256": "e0c644c801cee721861b30d6a9e7f172ad8459cff1ef21ce9b29d2c890ace689",
    "changedPixelSha256": "61d2393ce936f31fe2707fd6ed554d9fcd4564dd0df7dfb344a135fad5c1de9b",
    "scope": "Original 2x2 PNG fixture, not real style anchor or visual model test."
  }
}


```

## 全部CLI子进程原输出

```jsonl

{"utc": "2026-10-11T07:49:05.751865+00:00", "command": "python -B upstream/scripts/render_prompt.py --list", "cwd": "exercise", "environment": {"HAND_DRAWN_OFFLINE": "1", "HAND_DRAWN_IMAGE_CACHE": "exercise/empty-cache"}, "exit": 0, "expectedExit": 0, "stdout": "[\n  {\n    \"style_id\": \"1\",\n    \"name\": \"极简黑白线条讲解漫画(xkcd 火柴人)\",\n    \"aliases\": [\n      \"minimal-line\",\n      \"stickman\",\n      \"xkcd\",\n      \"极简线条\",\n      \"火柴人\"\n    ],\n    \"parameters\": [\n      \"N\",\n      \"分镜列表\"\n    ],\n    \"references\": []\n  },\n  {\n    \"style_id\": \"2\",\n    \"name\": \"蜡笔童涂(5岁小孩坏画)\",\n    \"aliases\": [\n      \"crayon\",\n      \"kid-crayon\",\n      \"蜡笔童涂\"\n    ],\n    \"parameters\": [\n      \"主体\",\n      \"主色调\",\n      \"标题词\"\n    ],\n    \"references\": []\n  },\n  {\n    \"style_id\": \"3\",\n    \"name\": \"吉卜力风\",\n    \"aliases\": [\n      \"ghibli\",\n      \"吉卜力\",\n      \"吉卜力风\"\n    ],\n    \"parameters\": [\n      \"主体\"\n    ],\n    \"references\": []\n  },\n  {\n    \"style_id\": \"3.1\",\n    \"name\": \"蜡笔童涂-潦草自画版\",\n    \"aliases\": [\n      \"family-crayon-card\",\n      \"kid-scrawl\",\n      \"parent-child-crayon\",\n      \"rawkid\",\n      \"stick-kid\",\n      \"submission-crayon\",\n      \"亲子手绘\",\n      \"亲子投稿蜡笔故事卡\",\n      \"亲子蜡笔故事\",\n      \"家庭投稿蜡笔卡\",\n      \"家庭蜡笔画\",\n      \"潦草自画版\",\n      \"蜡笔童涂-潦草自画版\",\n      \"蜡笔童涂潦草版\"\n    ],\n    \"parameters\": [\n      \"主体\",\n      \"文字\"\n    ],\n    \"references\": [\n      \"https://gentle-starburst-99bd99.netlify.app/hand-drawn/assets/style-3.1/anchor-family.png\"\n    ]\n  },\n  {\n    \"style_id\": \"4\",\n    \"name\": \"小豆人黑色涂鸦信息图\",\n    \"aliases\": [\n      \"bean\",\n      \"blob\",\n      \"小豆人\",\n      \"小豆人涂鸦信息图\"\n    ],\n    \"parameters\": [\n      \"N\",\n      \"分镜列表\"\n    ],\n    \"references\": []\n  },\n  {\n    \"style_id\": \"5\",\n    \"name\": \"MS Paint 烂涂鸦(the worse, the better)\",\n    \"aliases\": [\n      \"bad-doodle\",\n      \"ms paint\",\n      \"ms-paint\",\n      \"ugly\"\n    ],\n    \"parameters\": [\n      \"主体\"\n    ],\n    \"references\": []\n  },\n  {\n    \"style_id\": \"6\",\n    \"name\": \"圆珠笔单线涂鸦(scribble)\",\n    \"aliases\": [\n      \"ballpoint\",\n      \"pen-scribble\",\n      \"scribble\",\n      \"圆珠笔\"\n    ],\n    \"parameters\": [\n      \"主体\"\n    ],\n    \"references\": []\n  },\n  {\n    \"style_id\": \"7\",\n    \"name\": \"蜡笔实拍(真·儿童手涂纸张)\",\n    \"aliases\": [\n      \"crayon-photo\",\n      \"real-crayon\",\n      \"蜡笔实拍\"\n    ],\n    \"parameters\": [\n      \"主体\",\n      \"主色调\",\n      \"标题词\"\n    ],\n    \"references\": []\n  },\n  {\n    \"style_id\": \"8\",\n    \"name\": \"水墨写意\",\n    \"aliases\": [\n      \"chinese-painting\",\n      \"ink\",\n      \"ink-wash\",\n      \"shuimo\",\n      \"水墨\"\n    ],\n    \"parameters\": [\n      \"主体\"\n    ],\n    \"references\": []\n  },\n  {\n    \"style_id\": \"9\",\n    \"name\": \"复古像素\",\n    \"aliases\": [\n      \"16-bit\",\n      \"8-bit\",\n      \"pixel\",\n      \"pixel-art\",\n      \"像素\"\n    ],\n    \"parameters\": [\n      \"主体\",\n      \"主色调\"\n    ],\n    \"references\": []\n  },\n  {\n    \"style_id\": \"10\",\n    \"name\": \"情绪叙事淡彩速写\",\n    \"aliases\": [\n      \"emo-sketch\",\n      \"light-watercolor\",\n      \"story-sketch\",\n      \"watercolor-sketch\",\n      \"情绪叙事\",\n      \"淡彩速写\"\n    ],\n    \"parameters\": [\n      \"主体\",\n      \"文字\",\n      \"橙色关键物\"\n    ],\n    \"references\": []\n  },\n  {\n    \"style_id\": \"11\",\n    \"name\": \"二维水彩风格(复古动画概念稿)\",\n    \"aliases\": [\n      \"concept-art\",\n      \"gouache-concept\",\n      \"mid-century\",\n      \"retro-concept\",\n      \"二维水彩\"\n    ],\n    \"parameters\": [\n      \"主体\",\n      \"文字\",\n      \"构图\",\n      \"焦点物件\",\n      \"背景浓度\"\n    ],\n    \"references\": []\n  },\n  {\n    \"style_id\": \"12\",\n    \"name\": \"暖光童画(动画概念暖绘)\",\n    \"aliases\": [\n      \"storybook-visdev\",\n      \"sunlit-storybook\",\n      \"vis-dev\",\n      \"暖光童画\"\n    ],\n    \"parameters\": [\n      \"主体\",\n      \"场景\",\n      \"文字\",\n      \"构图\"\n    ],\n    \"references\": []\n  },\n  {\n    \"style_id\": \"13\",\n    \"name\": \"北欧纸雕(paper-folk)\",\n    \"aliases\": [\n      \"nordic-papercraft\",\n      \"paper-folk\",\n      \"paper-sculpture\",\n      \"papercraft\",\n      \"quilling\",\n      \"剪纸民俗\",\n      \"北欧纸雕\"\n    ],\n    \"parameters\": [\n      \"主体\",\n      \"底色\",\n      \"构图\",\n      \"点缀元素\"\n    ],\n    \"references\": [\n      \"https://gentle-starburst-99bd99.netlify.app/hand-drawn/examples/13-paper-folk-musician.png\",\n      \"https://gentle-starburst-99bd99.netlify.app/hand-drawn/examples/13-paper-folk.png\"\n    ]\n  },\n  {\n    \"style_id\": \"14\",\n    \"name\": \"北欧绘本水粉(nordic-storybook)\",\n    \"aliases\": [\n      \"nordic-storybook\",\n      \"scandi-gouache\",\n      \"scandinavian-storybook\",\n      \"soft-gouache\",\n      \"北欧绘本水粉\"\n    ],\n    \"parameters\": [\n      \"主体\",\n      \"光影\",\n      \"构图\",\n      \"纸底色\"\n    ],\n    \"references\": []\n  },\n  {\n    \"style_id\": \"15\",\n    \"name\": \"大鼻软偶(softnose-vinyl)\",\n    \"aliases\": [\n      \"art-toy\",\n      \"bignose-toy\",\n      \"softnose\",\n      \"softnose-vinyl\",\n      \"vinyl-toy\",\n      \"大鼻软偶\"\n    ],\n    \"parameters\": [\n      \"主体\",\n      \"构图\",\n      \"眼型\",\n      \"穿搭\",\n      \"肤色\",\n      \"背景底色\",\n      \"胡茬\"\n    ],\n    \"references\": []\n  },\n  {\n    \"style_id\": \"16\",\n    \"name\": \"聚光水粉立绘(gouache-spotlight)\",\n    \"aliases\": [\n      \"character-spotlight\",\n      \"gouache-spotlight\",\n      \"spotlight-gouache\",\n      \"聚光水粉立绘\"\n    ],\n    \"parameters\": [\n      \"主体\",\n      \"文字\",\n      \"构图\",\n      \"背景色\"\n    ],\n    \"references\": []\n  },\n  {\n    \"style_id\": \"17\",\n    \"name\": \"墨线绘本(inked-storybook)\",\n    \"aliases\": [\n      \"ink-storybook\",\n      \"inked-storybook\",\n      \"sketch-storybook\",\n      \"storybook-ink\",\n      \"墨线绘本\"\n    ],\n    \"parameters\": [\n      \"主体\",\n      \"文字\",\n      \"构图\",\n      \"背景色\",\n      \"配色\"\n    ],\n    \"references\": []\n  },\n  {\n    \"style_id\": \"18\",\n    \"name\": \"暖色扁平绘本(warm-flat-storybook)\",\n    \"aliases\": [\n      \"flat-storybook\",\n      \"geometric-storybook\",\n      \"warm-flat\",\n      \"warm-flat-storybook\",\n      \"暖色扁平绘本\"\n    ],\n    \"parameters\": [\n      \"主体\",\n      \"文字\",\n      \"构图\"\n    ],\n    \"references\": []\n  },\n  {\n    \"style_id\": \"19\",\n    \"name\": \"圆头红线极简童画(roundhead-redline)\",\n    \"aliases\": [\n      \"graphite-redline\",\n      \"redline-roundhead\",\n      \"roundhead-redline\",\n      \"圆头红线\",\n      \"圆头红线极简童画\",\n      \"黑红白圆头童画\"\n    ],\n    \"parameters\": [\n      \"主体\",\n      \"文字\"\n    ],\n    \"references\": [\n      \"https://gentle-starburst-99bd99.netlify.app/hand-drawn/assets/style-19/anchor-roundhead-redline.png\"\n    ]\n  },\n  {\n    \"style_id\": \"20\",\n    \"name\": \"暖黄墨线情绪小剧场(warm-yellow-ink-story)\",\n    \"aliases\": [\n      \"mustard-ink-story\",\n      \"warm-yellow-ink-story\",\n      \"yellow-ink-story\",\n      \"暖黄墨线\",\n      \"暖黄墨线情绪小剧场\"\n    ],\n    \"parameters\": [\n      \"主体\",\n      \"文字\"\n    ],\n    \"references\": [\n      \"https://gentle-starburst-99bd99.netlify.app/hand-drawn/assets/style-20/anchor-warm-yellow-ink-story.png\"\n    ]\n  }\n]\n", "stderr": ""}
{"utc": "2026-10-11T07:49:05.898802+00:00", "command": "python -B upstream/scripts/render_prompt.py --style 1 --var N=3 --var '分镜列表=IMU测量【短句】；驱动读取；定位融合'", "cwd": "exercise", "environment": {"HAND_DRAWN_OFFLINE": "1", "HAND_DRAWN_IMAGE_CACHE": "exercise/empty-cache"}, "exit": 0, "expectedExit": 0, "stdout": "xkcd 风格的极简黑白火柴人讲解漫画,画在米白/奶油色纸上。\n【最重要·硬性负向约束】严禁实心黑色填充、严禁剪影、严禁排线与阴影、严禁明暗与体积感、严禁厚涂或氛围渲染。人物与物体一律只用细线描边。\n角色:简单火柴人——圆圈头 + 极简点线五官,身体四肢是细单线;用小道具(帽子、杯子、书等)表示身份,不画细节。\n线条:细、均匀、略带手抖的黑色钢笔线,纯轮廓线稿,平面二维,无透视。\n版式:3格面板组成网格,每格用手绘略歪的圆角矩形框住,面板之间大量留白。\n色彩:纯黑白单色,黑线 + 米白纸,无任何其它颜色,无灰阶。\n文字:每格顶部加粗手写中文小标题,下方一句手写中文说明;可加简短对话气泡。中文清楚可读,不得错字、乱码或伪中文。\n调性:概念化、示意图式、略带幽默的讲解感,像 xkcd / 技术科普涂鸦。\n分镜:\nIMU测量【短句】；驱动读取；定位融合\n", "stderr": ""}
{"utc": "2026-10-11T07:49:05.961464+00:00", "command": "python -B upstream/scripts/render_prompt.py --style xkcd --var N=3 --var '分镜列表=IMU测量【短句】；驱动读取；定位融合'", "cwd": "exercise", "environment": {"HAND_DRAWN_OFFLINE": "1", "HAND_DRAWN_IMAGE_CACHE": "exercise/empty-cache"}, "exit": 0, "expectedExit": 0, "stdout": "xkcd 风格的极简黑白火柴人讲解漫画,画在米白/奶油色纸上。\n【最重要·硬性负向约束】严禁实心黑色填充、严禁剪影、严禁排线与阴影、严禁明暗与体积感、严禁厚涂或氛围渲染。人物与物体一律只用细线描边。\n角色:简单火柴人——圆圈头 + 极简点线五官,身体四肢是细单线;用小道具(帽子、杯子、书等)表示身份,不画细节。\n线条:细、均匀、略带手抖的黑色钢笔线,纯轮廓线稿,平面二维,无透视。\n版式:3格面板组成网格,每格用手绘略歪的圆角矩形框住,面板之间大量留白。\n色彩:纯黑白单色,黑线 + 米白纸,无任何其它颜色,无灰阶。\n文字:每格顶部加粗手写中文小标题,下方一句手写中文说明;可加简短对话气泡。中文清楚可读,不得错字、乱码或伪中文。\n调性:概念化、示意图式、略带幽默的讲解感,像 xkcd / 技术科普涂鸦。\n分镜:\nIMU测量【短句】；驱动读取；定位融合\n", "stderr": ""}
{"utc": "2026-10-11T07:49:06.095935+00:00", "command": "python -B upstream/scripts/render_prompt.py --style 1 --var N=3", "cwd": "exercise", "environment": {"HAND_DRAWN_OFFLINE": "1", "HAND_DRAWN_IMAGE_CACHE": "exercise/empty-cache"}, "exit": 2, "expectedExit": 2, "stdout": "", "stderr": "render_prompt: 缺少占位符: 分镜列表\n"}
{"utc": "2026-10-11T07:49:06.163459+00:00", "command": "python -B upstream/scripts/render_prompt.py --style 1 --var N=3 --var '分镜列表=测试' --var '多余=内容'", "cwd": "exercise", "environment": {"HAND_DRAWN_OFFLINE": "1", "HAND_DRAWN_IMAGE_CACHE": "exercise/empty-cache"}, "exit": 2, "expectedExit": 2, "stdout": "", "stderr": "render_prompt: 配方不包含这些占位符: 多余\n"}
{"utc": "2026-10-11T07:49:06.228892+00:00", "command": "python -B upstream/scripts/render_prompt.py --style 999", "cwd": "exercise", "environment": {"HAND_DRAWN_OFFLINE": "1", "HAND_DRAWN_IMAGE_CACHE": "exercise/empty-cache"}, "exit": 2, "expectedExit": 2, "stdout": "", "stderr": "render_prompt: STYLES.md 中不存在画风 999 的代码块配方\n"}
{"utc": "2026-10-11T07:49:06.292596+00:00", "command": "python -B upstream/scripts/render_prompt.py --style 1 --var N=", "cwd": "exercise", "environment": {"HAND_DRAWN_OFFLINE": "1", "HAND_DRAWN_IMAGE_CACHE": "exercise/empty-cache"}, "exit": 2, "expectedExit": 2, "stdout": "", "stderr": "render_prompt: --var 的名称和内容都不能为空: N=\n"}
{"utc": "2026-10-11T07:49:06.425081+00:00", "command": "python -B upstream/scripts/render_prompt.py --style 1 --var N=3 --var '分镜列表=测量；传输；融合'", "cwd": "exercise", "environment": {"HAND_DRAWN_OFFLINE": "1", "HAND_DRAWN_IMAGE_CACHE": "exercise/empty-cache"}, "exit": 0, "expectedExit": 0, "stdout": "xkcd 风格的极简黑白火柴人讲解漫画,画在米白/奶油色纸上。\n【最重要·硬性负向约束】严禁实心黑色填充、严禁剪影、严禁排线与阴影、严禁明暗与体积感、严禁厚涂或氛围渲染。人物与物体一律只用细线描边。\n角色:简单火柴人——圆圈头 + 极简点线五官,身体四肢是细单线;用小道具(帽子、杯子、书等)表示身份,不画细节。\n线条:细、均匀、略带手抖的黑色钢笔线,纯轮廓线稿,平面二维,无透视。\n版式:3格面板组成网格,每格用手绘略歪的圆角矩形框住,面板之间大量留白。\n色彩:纯黑白单色,黑线 + 米白纸,无任何其它颜色,无灰阶。\n文字:每格顶部加粗手写中文小标题,下方一句手写中文说明;可加简短对话气泡。中文清楚可读,不得错字、乱码或伪中文。\n调性:概念化、示意图式、略带幽默的讲解感,像 xkcd / 技术科普涂鸦。\n分镜:\n测量；传输；融合\n", "stderr": ""}
{"utc": "2026-10-11T07:49:06.488109+00:00", "command": "python -B upstream/scripts/render_prompt.py --style 1 --var N=3 --var '分镜列表=测量；传输；融合' --aspect 16:9", "cwd": "exercise", "environment": {"HAND_DRAWN_OFFLINE": "1", "HAND_DRAWN_IMAGE_CACHE": "exercise/empty-cache"}, "exit": 0, "expectedExit": 0, "stdout": "xkcd 风格的极简黑白火柴人讲解漫画,画在米白/奶油色纸上。\n【最重要·硬性负向约束】严禁实心黑色填充、严禁剪影、严禁排线与阴影、严禁明暗与体积感、严禁厚涂或氛围渲染。人物与物体一律只用细线描边。\n角色:简单火柴人——圆圈头 + 极简点线五官,身体四肢是细单线;用小道具(帽子、杯子、书等)表示身份,不画细节。\n线条:细、均匀、略带手抖的黑色钢笔线,纯轮廓线稿,平面二维,无透视。\n版式:3格面板组成网格,每格用手绘略歪的圆角矩形框住,面板之间大量留白。\n色彩:纯黑白单色,黑线 + 米白纸,无任何其它颜色,无灰阶。\n文字:每格顶部加粗手写中文小标题,下方一句手写中文说明;可加简短对话气泡。中文清楚可读,不得错字、乱码或伪中文。\n调性:概念化、示意图式、略带幽默的讲解感,像 xkcd / 技术科普涂鸦。\n分镜:\n测量；传输；融合\n\n画幅比例:16:9。\n", "stderr": ""}
{"utc": "2026-10-11T07:49:06.550169+00:00", "command": "python -B upstream/scripts/render_prompt.py --style 1 --var N=3 --var '分镜列表=测量；传输；融合' --aspect not-a-ratio", "cwd": "exercise", "environment": {"HAND_DRAWN_OFFLINE": "1", "HAND_DRAWN_IMAGE_CACHE": "exercise/empty-cache"}, "exit": 0, "expectedExit": 0, "stdout": "xkcd 风格的极简黑白火柴人讲解漫画,画在米白/奶油色纸上。\n【最重要·硬性负向约束】严禁实心黑色填充、严禁剪影、严禁排线与阴影、严禁明暗与体积感、严禁厚涂或氛围渲染。人物与物体一律只用细线描边。\n角色:简单火柴人——圆圈头 + 极简点线五官,身体四肢是细单线;用小道具(帽子、杯子、书等)表示身份,不画细节。\n线条:细、均匀、略带手抖的黑色钢笔线,纯轮廓线稿,平面二维,无透视。\n版式:3格面板组成网格,每格用手绘略歪的圆角矩形框住,面板之间大量留白。\n色彩:纯黑白单色,黑线 + 米白纸,无任何其它颜色,无灰阶。\n文字:每格顶部加粗手写中文小标题,下方一句手写中文说明;可加简短对话气泡。中文清楚可读,不得错字、乱码或伪中文。\n调性:概念化、示意图式、略带幽默的讲解感,像 xkcd / 技术科普涂鸦。\n分镜:\n测量；传输；融合\n\n画幅比例:not-a-ratio。\n", "stderr": ""}
{"utc": "2026-10-11T07:49:06.681146+00:00", "command": "python -B upstream/scripts/render_prompt.py --style 19 --subject 'a robot holding a lantern' --format json", "cwd": "exercise", "environment": {"HAND_DRAWN_OFFLINE": "1", "HAND_DRAWN_IMAGE_CACHE": "exercise/empty-cache"}, "exit": 2, "expectedExit": 2, "stdout": "", "stderr": "render_prompt: 离线缓存缺少有效图片: assets/style-19/anchor-roundhead-redline.png;请联网运行 hosted_images.py fetch\n"}
{"utc": "2026-10-11T07:49:06.746803+00:00", "command": "python -B upstream/scripts/render_prompt.py --style 19 --subject 'a robot holding a lantern' --format text", "cwd": "exercise", "environment": {"HAND_DRAWN_OFFLINE": "1", "HAND_DRAWN_IMAGE_CACHE": "exercise/empty-cache"}, "exit": 2, "expectedExit": 2, "stdout": "", "stderr": "render_prompt: 画风 19 正式生产不能只输出 prompt;请使用 --format json,或仅在非生产预览时显式加 --text-only-preview\n"}


```

完整入口命令、直接函数调用与输入生成见lab.py。12个CLI结果中6个exit0、6个预期exit2；37是harness内明确check条目数，不是模型成功率。公开日志将项目绝对路径及Python安装路径替换为占位符，原始证据留于exercise。
