# Easel 本地组件实验日志

原学习日期：2026-10-05 UTC。下述实验与指南命令在原学习阶段实际运行。此公开副本保留原时间、结果、退出码和失败过程；只规范化内部绝对路径并移除非教学所需的来源与操作上下文，不代表本次重新执行学习实验。

路径记号：<EXERCISE_ROOT> 表示原实验解包根目录，<PYTHON_STDLIB> 表示原Python标准库目录。它们仅替代历史日志中的路径；可执行的6条学习命令保持不变，重放时使用读者自己的新解包目录。

## 环境与执行边界

Linux x86_64，Python 3.12.14，标准库。练习包带必要源码副本、Apache-2.0根许可和指纹清单；复放不需安装依赖。env -i移除继承凭据，进程内审计hook限制网络、子进程与越界写入；它不是操作系统沙箱，也没有安装全局hook。

主实验采用六个学习步骤：第1步运行含六个内部阶段的自建harness；后5步读取并验证真实产物。上游模块保持原字节，runpy按日志argv执行；画像路径由harness指向虚构夹具。没有运行Easel主CLI、模型或发布器。

原始实跑UTC 2026-10-05 13:46:00.680168至13:46:00.810746，六个内部阶段完成。15/15自写检查、3/3上游selftest入口、20次组件调用分别记录。365字初稿被拒，143字修订稿通过本地两项检查，项目仍为draft。

不等于生成了高质量文案、跑通完整发布检查Skill、真实社媒发布或端到端工作台。模型、OpenClaw、Web、全局同步、账号登录、归因和媒体制作均未执行；archive/--apply排除。

## 原始尝试与恢复

harness首次在上游调用前被自身审计hook阻止。只将环境描述从platform.platform改为os.uname，再执行成功；未修改上游源文件。

原始社媒材料访问返回HTTP 403，未读取全文；仓库源码已检查。

时间口径：外层与本文命令为UTC；manifest为UTC+8；原asset索引使用主机当地UTC-7。

## 指南6条原样可复制命令

先把easel-exercise.zip解到新的空目录，在解包根打开终端。第1条实际运行所有内部阶段；后5条读取与断言真实产物。每次复放使用新目录。以下短行命令为最终PDF和HTML实际版本，均另在全新目录逐条运行。

### 步骤 1 运行完整六阶段实验

输入与目的：输入是练习ZIP内固定源码、六份虚构画像的生成规则和自写中文短文。第1步一次执行全部六个内部阶段；后5步只读取并核对这次运行的真实产物。

```bash

mkdir -p runtime/home runtime/tmp logs
env -i PATH="$PATH" HOME="$PWD/runtime/home" \
  TMPDIR="$PWD/runtime/tmp" LANG=C.UTF-8 \
  PYTHONDONTWRITEBYTECODE=1 python -B run_exercise.py

```

UTC 2026-10-05T14:02:22.013907+00:00；耗时 0.197209秒；退出码 0

stdout：

```text

{
  "started_utc": "2026-10-05T14:02:22.049063+00:00",
  "finished_utc": "2026-10-05T14:02:22.197096+00:00",
  "custom_cases_passed": 15,
  "custom_cases_total": 15,
  "upstream_selftest_entrypoints_passed": 3,
  "operations_total": 20
}

```

stderr：

```text

(empty)

```

实际结果：生成虚构画像、前后正文、元数据和日志；完成15个自写命名检查、3个上游自测入口、20次组件调用。

验证：检查退出码0，并确认 results.json 与 snapshots/、logs/ 已生成；三种统计单位不能相加。

失败判据：若目录已有 fixtures，换全新空目录解包；缺 Python 3.10+ 或断言失败应停止，保留stderr，不能改预期凑通过。

### 步骤 2 核对画像修改及记忆范围

输入与目的：输入 snapshots/profile-load.json；对比六维画像的前后指纹，观察只有style被修改，并读取真实拼接前缀。

```bash

python -B -c 'import json
from pathlib import Path
d=json.loads(Path("snapshots/profile-load.json").read_text())
before=d["before_sha256"]; after=d["after_sha256"]
changed=[k for k in before if before[k]!=after[k]]
print("files=",len(after),"changed=",changed)
print(d["prefix"])
print(d["loaded_after"].split("修改：")[1].split("\n")[0])
assert changed==["style.md"]'

```

UTC 2026-10-05T14:02:22.211155+00:00；耗时 0.026821秒；退出码 0

stdout：

```text

files= 6 changed= ['style.md']
我当前使用的画像是「纸页角落虚构账号」。本会话的账号长期记忆仅使用 profiles/纸页角落虚构账号/memory.md，不要使用工作区全局 MEMORY.md 作为账号记忆。
最后只问一个具体问题，不要求转发或关注。

```

stderr：

```text

(empty)

```

实际结果：共6份文件，仅style.md指纹变化；输出新增的“最后只问一个具体问题”规则。没有模型生成。

验证：changed 必须只有style.md；prefix包含当前虚构画像的memory.md；检查loaded_after中修改可见。

失败判据：变更多个文件、前缀错指其他画像或缺失新增规则，均不通过；存在目录不代表平台登录。

### 步骤 3 查看初稿为何被拒绝

输入与目的：输入3份失败分支日志：字数、泄露扫描、latest。读取上游真实stdout/stderr与退出码，确认失败也进入步骤历史。

```bash

python -B -c 'import json
from pathlib import Path
load=lambda p:json.loads(Path("logs/"+p+".json").read_text())
a=load("03-before-length-rejection")
b=load("03-before-contentguard-rejection")
c=load("03-latest-includes-failed")
count=json.loads(a["stdout"])["actual"]
last=json.loads(c["stdout"])["step"]["status"]
print("count=",count,"length_exit=",a["exit_code"])
print(b["stderr"].strip())
print("guard_exit=",b["exit_code"],"latest=",last)
assert a["exit_code"]==1 and b["exit_code"]==7'

```

UTC 2026-10-05T14:02:22.238002+00:00；耗时 0.026643秒；退出码 0

stdout：

```text

count= 365 length_exit= 1
❌ 检出 1 处敏感信息（密钥/内部地址等，发布会被拦截）：
  · [med] proxy-ip｜私网/代理 IP：…使用习惯。 虚构测试串：【10.2***28】
guard_exit= 7 latest= failed

```

stderr：

```text

(empty)

```

实际结果：初稿social_count=365；目标140±5%即133–147，字数退出1。合成私网IP命中1处，扫描退出7；latest返回failed。

验证：输出必须同时含365、length_exit=1、guard_exit=7及latest=failed；7是退出码，不是7个命中。

失败判据：若无失败记录、错误被吞掉或latest变成done则检查不符；本例合成IP不是用户秘密，不能换成真实凭证。

### 步骤 4 检查修订成品与状态变化

输入与目的：输入修订扫描日志、manifest-after和post-after正文。对比人工给定修订稿与原稿，检查字段保留和步骤历史。

```bash

python -B -c 'import json
from pathlib import Path
load=lambda p:json.loads(Path(p).read_text())
a=load("logs/04-after-length-pass.json")
b=load("logs/04-after-contentguard-pass.json")
m=load("snapshots/manifest-after.json")
count=json.loads(a["stdout"])["actual"]
states=[x["status"] for x in m["steps"]]
print("count=",count,"guard_exit=",b["exit_code"])
print("project=",m["status"],"steps=",states)
print(Path("snapshots/post-after.md").read_text())
assert m["status"]=="draft" and b["exit_code"]==0'

```

UTC 2026-10-05T14:02:22.264673+00:00；耗时 0.027692秒；退出码 0

stdout：

```text

count= 143 guard_exit= 0
project= draft steps= ['done', 'failed', 'done']
书桌总是越收越乱？先别急着买收纳盒。

今晚只试三步：把明天要读的一本书放在手边；给正在用的笔留一个固定位置；把暂时不用的纸放进同一个纸袋。做完就停，不需要把每个角落整理得像照片。

明天坐下时，看看能不能更快找到第一件要用的东西。你书桌上最容易找不到什么？评论里聊聊。

#书桌整理# #阅读日常#

```

stderr：

```text

(empty)

```

实际结果：修订稿计数143，扫描退出0；步骤历史done、failed、done，项目仍draft。完整正文在命令输出和后附样例页。

验证：核对143落在133–147；保留之前失败记录；项目状态draft，不能写成已经发布。

失败判据：只看done而忽略项目/外部效果，或宣称143是微博官方硬限制，都是错误；扫描0仍不证明质量、版权和授权。

### 步骤 5 从索引检索回那份成品

输入与目的：输入真实INDEX.json及asset-search日志；确认文件数量、平台推断、标签修改和检索结果。

```bash

python -B -c 'import json
from pathlib import Path
a=json.loads(Path("logs/05-asset-search.json").read_text())
p=next(Path("fixtures/outputs").glob("INDEX.json"))
d=json.loads(p.read_text())
print("indexed=",d["count"])
print(a["stdout"])
assert d["count"]==3 and a["exit_code"]==0'

```

UTC 2026-10-05T14:02:22.292393+00:00；耗时 0.035873秒；退出码 0

stdout：

```text

indexed= 3
找到 1 个匹配项：
日期          平台           类型            大小  路径
2026-10-05  weibo        text          0K  雨天书桌微整理/weibo-post.md  #已本地检查 #虚构画像

```

stderr：

```text

(empty)

```

实际结果：索引共3项，包含.easel.json、简报和正文；weibo平台与两标签筛选只返回1份正文。

验证：检索路径应指向雨天书桌微整理/weibo-post.md，标签包含已本地检查与虚构画像，已移除待修订。

失败判据：不应把3个索引项说成3份成品；platform来自路径规则，不能拿它证明manifest字段被扫描器消费。

### 步骤 6 核对自测与源码未变

输入与目的：输入results.json和source-lock.json；逐份计算上游副本SHA-256，分别报告自写检查、上游入口与组件调用数量。

```bash

python -B -c 'import json,hashlib
from pathlib import Path
load=lambda p:json.loads(Path(p).read_text())
r=load("results.json"); s=load("source-lock.json")
ok=True
for x in s["copied_files"]:
 p=Path("upstream")/x["path"]
 ok &= hashlib.sha256(p.read_bytes()).hexdigest()==x["sha256"]
c=r["custom_cases_passed"]; total=r["custom_cases_total"]
st=r["upstream_selftest_entrypoints_passed"]
print("custom=",c,"/",total)
print("selftest_entrypoints=",st)
print("invocations=",r["operations_total"])
print("source_hashes_match=",ok)
assert ok and c==15 and st==3'

```

UTC 2026-10-05T14:02:22.328295+00:00；耗时 0.029704秒；退出码 0

stdout：

```text

custom= 15 / 15
selftest_entrypoints= 3
invocations= 20
source_hashes_match= True

```

stderr：

```text

(empty)

```

实际结果：15/15自写命名检查；3/3上游selftest入口；20次组件调用；上游副本指纹一致。

验证：custom=15/15、selftest_entrypoints=3、invocations=20、source_hashes_match=True同时出现；完整自测stdout见日志。

失败判据：没有运行全量pytest，也没有覆盖所有技能。上游manifest自测故意输出非法kind的stderr而整体退出0，应结合退出码和断言解释。

## 原始六个内部阶段

```json

[
  {
    "number": 1,
    "title": "Pin source and create/edit fictional six-file profile",
    "started_utc": "2026-10-05T13:46:00.680198+00:00",
    "elapsed_seconds": 0.004645,
    "passed": true
  },
  {
    "number": 2,
    "title": "Validate output paths and persist draft project",
    "started_utc": "2026-10-05T13:46:00.685068+00:00",
    "elapsed_seconds": 0.015373,
    "passed": true
  },
  {
    "number": 3,
    "title": "Run actual failing prepublication component checks",
    "started_utc": "2026-10-05T13:46:00.700810+00:00",
    "elapsed_seconds": 0.024629,
    "passed": true
  },
  {
    "number": 4,
    "title": "Repair text and metadata then recheck",
    "started_utc": "2026-10-05T13:46:00.725880+00:00",
    "elapsed_seconds": 0.023561,
    "passed": true
  },
  {
    "number": 5,
    "title": "Index tag and retrieve the saved content artifact",
    "started_utc": "2026-10-05T13:46:00.749952+00:00",
    "elapsed_seconds": 0.026848,
    "passed": true
  },
  {
    "number": 6,
    "title": "Run original selftests and verify isolation",
    "started_utc": "2026-10-05T13:46:00.777357+00:00",
    "elapsed_seconds": 0.032668,
    "passed": true
  }
]

```

## 二十次上游组件调用 历史日志公开副本

以下保留runpy实际source/argv与输出，内部绝对路径已按上述规则替换；这些是历史执行记录，不是未经运行的shell建议。退出1、2、7出现在设计的负例中；外层检查预期行为而退出0。

### 02-record-local-fixture

```json

{
  "label": "02-record-local-fixture",
  "source": "skills/shared/scripts/manifest.py",
  "argv": [
    "record",
    "--topic",
    "雨天书桌微整理",
    "--profile",
    "纸页角落虚构账号",
    "--layer",
    "produce",
    "--skill",
    "local-authored-fixture",
    "--outputs",
    "weibo-post.md,assets/brief.md",
    "--summary",
    "本地合成文案；未运行Easel Agent生成"
  ],
  "started_utc": "2026-10-05T13:46:00.696177+00:00",
  "elapsed_seconds": 0.003847,
  "exit_code": 0,
  "expected_exit": 0,
  "stdout": "{\n  \"ok\": true,\n  \"topic\": \"雨天书桌微整理\",\n  \"step_index\": 0,\n  \"step\": {\n    \"layer\": \"produce\",\n    \"skill\": \"local-authored-fixture\",\n    \"at\": \"2026-10-05T21:46:00+08:00\",\n    \"status\": \"done\",\n    \"outputs\": [\n      \"weibo-post.md\",\n      \"assets/brief.md\"\n    ],\n    \"upstream\": [],\n    \"summary\": \"本地合成文案；未运行Easel Agent生成\"\n  },\n  \"path\": \"<EXERCISE_ROOT>/fixtures/outputs/雨天书桌微整理/.easel.json\"\n}\n",
  "stderr": ""
}

```

### 02-save-metadata

```json

{
  "label": "02-save-metadata",
  "source": "skills/shared/scripts/manifest.py",
  "argv": [
    "meta",
    "--topic",
    "雨天书桌微整理",
    "--profile",
    "纸页角落虚构账号",
    "--title",
    "初稿：雨天书桌微整理",
    "--platform",
    "微博",
    "--kind",
    "other",
    "--status",
    "draft",
    "--tags",
    "书桌整理,阅读日常",
    "--deliverables",
    "weibo-post.md"
  ],
  "started_utc": "2026-10-05T13:46:00.688382+00:00",
  "elapsed_seconds": 0.007601,
  "exit_code": 0,
  "expected_exit": 0,
  "stdout": "{\n  \"ok\": true,\n  \"topic\": \"雨天书桌微整理\",\n  \"meta\": {\n    \"title\": \"初稿：雨天书桌微整理\",\n    \"platform\": \"微博\",\n    \"kind\": \"other\",\n    \"status\": \"draft\",\n    \"tags\": [\n      \"书桌整理\",\n      \"阅读日常\"\n    ],\n    \"deliverables\": [\n      \"weibo-post.md\"\n    ]\n  },\n  \"path\": \"<EXERCISE_ROOT>/fixtures/outputs/雨天书桌微整理/.easel.json\"\n}\n",
  "stderr": ""
}

```

### 03-before-contentguard-rejection

```json

{
  "label": "03-before-contentguard-rejection",
  "source": "skills/shared/scripts/content_guard.py",
  "argv": [
    "scan",
    "--file",
    "<EXERCISE_ROOT>/fixtures/outputs/雨天书桌微整理/weibo-post.md"
  ],
  "started_utc": "2026-10-05T13:46:00.705807+00:00",
  "elapsed_seconds": 0.010991,
  "exit_code": 7,
  "expected_exit": 7,
  "stdout": "",
  "stderr": "❌ 检出 1 处敏感信息（密钥/内部地址等，发布会被拦截）：\n  · [med] proxy-ip｜私网/代理 IP：…使用习惯。 虚构测试串：【10.2***28】 \n"
}

```

### 03-before-length-rejection

```json

{
  "label": "03-before-length-rejection",
  "source": "skills/shared/scripts/wordcount.py",
  "argv": [
    "check",
    "--target",
    "140",
    "--tolerance",
    "0.05",
    "--file",
    "<EXERCISE_ROOT>/fixtures/outputs/雨天书桌微整理/weibo-post.md",
    "--json"
  ],
  "started_utc": "2026-10-05T13:46:00.700820+00:00",
  "elapsed_seconds": 0.004747,
  "exit_code": 1,
  "expected_exit": 1,
  "stdout": "{\n  \"pass\": false,\n  \"status\": \"over\",\n  \"metric\": \"social_count\",\n  \"target\": 140,\n  \"tolerance\": 0.05,\n  \"range\": [\n    133,\n    147\n  ],\n  \"actual\": 365,\n  \"adjust\": 218,\n  \"advice\": \"超了，至少再删 218 字（当前 365，上限 147）\",\n  \"stats\": {\n    \"cjk_chars\": 328,\n    \"en_words\": 0,\n    \"num_groups\": 2,\n    \"punct\": 35,\n    \"total_chars\": 385,\n    \"no_space_chars\": 375,\n    \"social_count\": 365\n  }\n}\n",
  "stderr": ""
}

```

### 03-latest-includes-failed

```json

{
  "label": "03-latest-includes-failed",
  "source": "skills/shared/scripts/manifest.py",
  "argv": [
    "latest",
    "--topic",
    "雨天书桌微整理",
    "--layer",
    "publish"
  ],
  "started_utc": "2026-10-05T13:46:00.720828+00:00",
  "elapsed_seconds": 0.002983,
  "exit_code": 0,
  "expected_exit": 0,
  "stdout": "{\n  \"found\": true,\n  \"topic\": \"雨天书桌微整理\",\n  \"profile\": \"纸页角落虚构账号\",\n  \"step\": {\n    \"layer\": \"publish\",\n    \"skill\": \"offline-component-preflight\",\n    \"at\": \"2026-10-05T21:46:00+08:00\",\n    \"status\": \"failed\",\n    \"outputs\": [],\n    \"upstream\": [\n      \"weibo-post.md\"\n    ],\n    \"summary\": \"本地字数超标且合成私网IP被拦；未调用发布器\"\n  }\n}\n",
  "stderr": ""
}

```

### 03-record-preflight-failed

```json

{
  "label": "03-record-preflight-failed",
  "source": "skills/shared/scripts/manifest.py",
  "argv": [
    "record",
    "--topic",
    "雨天书桌微整理",
    "--layer",
    "publish",
    "--skill",
    "offline-component-preflight",
    "--status",
    "failed",
    "--upstream",
    "weibo-post.md",
    "--summary",
    "本地字数超标且合成私网IP被拦；未调用发布器"
  ],
  "started_utc": "2026-10-05T13:46:00.717047+00:00",
  "elapsed_seconds": 0.00358,
  "exit_code": 0,
  "expected_exit": 0,
  "stdout": "{\n  \"ok\": true,\n  \"topic\": \"雨天书桌微整理\",\n  \"step_index\": 1,\n  \"step\": {\n    \"layer\": \"publish\",\n    \"skill\": \"offline-component-preflight\",\n    \"at\": \"2026-10-05T21:46:00+08:00\",\n    \"status\": \"failed\",\n    \"outputs\": [],\n    \"upstream\": [\n      \"weibo-post.md\"\n    ],\n    \"summary\": \"本地字数超标且合成私网IP被拦；未调用发布器\"\n  },\n  \"path\": \"<EXERCISE_ROOT>/fixtures/outputs/雨天书桌微整理/.easel.json\"\n}\n",
  "stderr": ""
}

```

### 04-after-contentguard-pass

```json

{
  "label": "04-after-contentguard-pass",
  "source": "skills/shared/scripts/content_guard.py",
  "argv": [
    "scan",
    "--file",
    "<EXERCISE_ROOT>/fixtures/outputs/雨天书桌微整理/weibo-post.md"
  ],
  "started_utc": "2026-10-05T13:46:00.730526+00:00",
  "elapsed_seconds": 0.00368,
  "exit_code": 0,
  "expected_exit": 0,
  "stdout": "✅ 未检出敏感信息。\n",
  "stderr": ""
}

```

### 04-after-length-pass

```json

{
  "label": "04-after-length-pass",
  "source": "skills/shared/scripts/wordcount.py",
  "argv": [
    "check",
    "--target",
    "140",
    "--tolerance",
    "0.05",
    "--file",
    "<EXERCISE_ROOT>/fixtures/outputs/雨天书桌微整理/weibo-post.md",
    "--json"
  ],
  "started_utc": "2026-10-05T13:46:00.726422+00:00",
  "elapsed_seconds": 0.003865,
  "exit_code": 0,
  "expected_exit": 0,
  "stdout": "{\n  \"pass\": true,\n  \"status\": \"ok\",\n  \"metric\": \"social_count\",\n  \"target\": 140,\n  \"tolerance\": 0.05,\n  \"range\": [\n    133,\n    147\n  ],\n  \"actual\": 143,\n  \"adjust\": 0,\n  \"advice\": \"达标（133 ≤ 143 ≤ 147）\",\n  \"stats\": {\n    \"cjk_chars\": 127,\n    \"en_words\": 0,\n    \"num_groups\": 0,\n    \"punct\": 16,\n    \"total_chars\": 151,\n    \"no_space_chars\": 143,\n    \"social_count\": 143\n  }\n}\n",
  "stderr": ""
}

```

### 04-invalid-kind-rejected

```json

{
  "label": "04-invalid-kind-rejected",
  "source": "skills/shared/scripts/manifest.py",
  "argv": [
    "meta",
    "--topic",
    "雨天书桌微整理",
    "--kind",
    "not-a-real-kind"
  ],
  "started_utc": "2026-10-05T13:46:00.745390+00:00",
  "elapsed_seconds": 0.003465,
  "exit_code": 2,
  "expected_exit": 2,
  "stdout": "",
  "stderr": "usage: manifest.py meta [-h] [--topic TOPIC] [--data DATA] [--profile PROFILE]\n                        [--title TITLE] [--summary SUMMARY]\n                        [--platform PLATFORM]\n                        [--kind {article,xhs-note,video,cards,poster,audio,other}]\n                        [--status {draft,ready,published}] [--tags TAGS]\n                        [--cover COVER] [--deliverables DELIVERABLES]\nmanifest.py meta: error: argument --kind: invalid choice: 'not-a-real-kind' (choose from article, xhs-note, video, cards, poster, audio, other)\n"
}

```

### 04-latest-preflight-passed

```json

{
  "label": "04-latest-preflight-passed",
  "source": "skills/shared/scripts/manifest.py",
  "argv": [
    "latest",
    "--topic",
    "雨天书桌微整理",
    "--layer",
    "publish"
  ],
  "started_utc": "2026-10-05T13:46:00.741929+00:00",
  "elapsed_seconds": 0.003146,
  "exit_code": 0,
  "expected_exit": 0,
  "stdout": "{\n  \"found\": true,\n  \"topic\": \"雨天书桌微整理\",\n  \"profile\": \"纸页角落虚构账号\",\n  \"step\": {\n    \"layer\": \"publish\",\n    \"skill\": \"offline-component-preflight\",\n    \"at\": \"2026-10-05T21:46:00+08:00\",\n    \"status\": \"done\",\n    \"outputs\": [],\n    \"upstream\": [\n      \"weibo-post.md\"\n    ],\n    \"summary\": \"仅本地字数与泄露扫描通过；无真实发布、无完整语义审核\"\n  }\n}\n",
  "stderr": ""
}

```

### 04-record-preflight-passed

```json

{
  "label": "04-record-preflight-passed",
  "source": "skills/shared/scripts/manifest.py",
  "argv": [
    "record",
    "--topic",
    "雨天书桌微整理",
    "--layer",
    "publish",
    "--skill",
    "offline-component-preflight",
    "--status",
    "done",
    "--upstream",
    "weibo-post.md",
    "--summary",
    "仅本地字数与泄露扫描通过；无真实发布、无完整语义审核"
  ],
  "started_utc": "2026-10-05T13:46:00.738157+00:00",
  "elapsed_seconds": 0.003474,
  "exit_code": 0,
  "expected_exit": 0,
  "stdout": "{\n  \"ok\": true,\n  \"topic\": \"雨天书桌微整理\",\n  \"step_index\": 2,\n  \"step\": {\n    \"layer\": \"publish\",\n    \"skill\": \"offline-component-preflight\",\n    \"at\": \"2026-10-05T21:46:00+08:00\",\n    \"status\": \"done\",\n    \"outputs\": [],\n    \"upstream\": [\n      \"weibo-post.md\"\n    ],\n    \"summary\": \"仅本地字数与泄露扫描通过；无真实发布、无完整语义审核\"\n  },\n  \"path\": \"<EXERCISE_ROOT>/fixtures/outputs/雨天书桌微整理/.easel.json\"\n}\n",
  "stderr": ""
}

```

### 04-update-selected-metadata

```json

{
  "label": "04-update-selected-metadata",
  "source": "skills/shared/scripts/manifest.py",
  "argv": [
    "meta",
    "--topic",
    "雨天书桌微整理",
    "--title",
    "书桌微整理：从三件小事开始",
    "--tags",
    "书桌整理,阅读日常,本地实验"
  ],
  "started_utc": "2026-10-05T13:46:00.734452+00:00",
  "elapsed_seconds": 0.003424,
  "exit_code": 0,
  "expected_exit": 0,
  "stdout": "{\n  \"ok\": true,\n  \"topic\": \"雨天书桌微整理\",\n  \"meta\": {\n    \"title\": \"书桌微整理：从三件小事开始\",\n    \"platform\": \"微博\",\n    \"kind\": \"other\",\n    \"status\": \"draft\",\n    \"tags\": [\n      \"书桌整理\",\n      \"阅读日常\",\n      \"本地实验\"\n    ],\n    \"deliverables\": [\n      \"weibo-post.md\"\n    ]\n  },\n  \"path\": \"<EXERCISE_ROOT>/fixtures/outputs/雨天书桌微整理/.easel.json\"\n}\n",
  "stderr": ""
}

```

### 05-asset-report

```json

{
  "label": "05-asset-report",
  "source": "skills/openclaw/asset-manager/scripts/assets.py",
  "argv": [
    "--root",
    "<EXERCISE_ROOT>/fixtures/outputs",
    "report"
  ],
  "started_utc": "2026-10-05T13:46:00.772011+00:00",
  "elapsed_seconds": 0.004568,
  "exit_code": 0,
  "expected_exit": 0,
  "stdout": "# 素材统计（<EXERCISE_ROOT>/fixtures/outputs）— 共 3 个文件\n\n## 按类型\n  text        3  (100%)\n\n## 按平台\n  unknown         2  最近 2026-10-05\n  weibo           1  最近 2026-10-05\n\n## 按日期（近 14 天有产出的）\n  2026-10-05    3\n",
  "stderr": ""
}

```

### 05-asset-retag

```json

{
  "label": "05-asset-retag",
  "source": "skills/openclaw/asset-manager/scripts/assets.py",
  "argv": [
    "--root",
    "<EXERCISE_ROOT>/fixtures/outputs",
    "tag",
    "雨天书桌微整理/weibo-post.md",
    "--add",
    "已本地检查",
    "--remove",
    "待修订"
  ],
  "started_utc": "2026-10-05T13:46:00.761629+00:00",
  "elapsed_seconds": 0.005616,
  "exit_code": 0,
  "expected_exit": 0,
  "stdout": "雨天书桌微整理/weibo-post.md 标签: #已本地检查 #虚构画像\n",
  "stderr": ""
}

```

### 05-asset-scan

```json

{
  "label": "05-asset-scan",
  "source": "skills/openclaw/asset-manager/scripts/assets.py",
  "argv": [
    "--root",
    "<EXERCISE_ROOT>/fixtures/outputs",
    "scan"
  ],
  "started_utc": "2026-10-05T13:46:00.749964+00:00",
  "elapsed_seconds": 0.005125,
  "exit_code": 0,
  "expected_exit": 0,
  "stdout": "已索引 3 个文件，共 0.00 MB -> <EXERCISE_ROOT>/fixtures/outputs/INDEX.json\n",
  "stderr": ""
}

```

### 05-asset-search

```json

{
  "label": "05-asset-search",
  "source": "skills/openclaw/asset-manager/scripts/assets.py",
  "argv": [
    "--root",
    "<EXERCISE_ROOT>/fixtures/outputs",
    "search",
    "书桌",
    "--platform",
    "weibo",
    "--tag",
    "虚构画像,已本地检查"
  ],
  "started_utc": "2026-10-05T13:46:00.767446+00:00",
  "elapsed_seconds": 0.004276,
  "exit_code": 0,
  "expected_exit": 0,
  "stdout": "找到 1 个匹配项：\n日期          平台           类型            大小  路径\n2026-10-05  weibo        text          0K  雨天书桌微整理/weibo-post.md  #已本地检查 #虚构画像\n",
  "stderr": ""
}

```

### 05-asset-tag-draft

```json

{
  "label": "05-asset-tag-draft",
  "source": "skills/openclaw/asset-manager/scripts/assets.py",
  "argv": [
    "--root",
    "<EXERCISE_ROOT>/fixtures/outputs",
    "tag",
    "雨天书桌微整理/weibo-post.md",
    "--add",
    "虚构画像,待修订"
  ],
  "started_utc": "2026-10-05T13:46:00.755240+00:00",
  "elapsed_seconds": 0.005761,
  "exit_code": 0,
  "expected_exit": 0,
  "stdout": "雨天书桌微整理/weibo-post.md 标签: #待修订 #虚构画像\n",
  "stderr": ""
}

```

### 06-upstream-selftest-content_guard

```json

{
  "label": "06-upstream-selftest-content_guard",
  "source": "skills/shared/scripts/content_guard.py",
  "argv": [
    "selftest"
  ],
  "started_utc": "2026-10-05T13:46:00.799243+00:00",
  "elapsed_seconds": 0.010273,
  "exit_code": 0,
  "expected_exit": 0,
  "stdout": "selftest 通过（BLOCK 正例 12 必拦 / WARN 正例 7 只提醒不拦 / 反例 6 放行 + redact + guard）\n",
  "stderr": ""
}

```

### 06-upstream-selftest-manifest

```json

{
  "label": "06-upstream-selftest-manifest",
  "source": "skills/shared/scripts/manifest.py",
  "argv": [
    "selftest"
  ],
  "started_utc": "2026-10-05T13:46:00.777366+00:00",
  "elapsed_seconds": 0.019486,
  "exit_code": 0,
  "expected_exit": 0,
  "stdout": "manifest.py selftest: OK\n",
  "stderr": "usage: manifest.py meta [-h] [--topic TOPIC] [--data DATA] [--profile PROFILE]\n                        [--title TITLE] [--summary SUMMARY]\n                        [--platform PLATFORM]\n                        [--kind {article,xhs-note,video,cards,poster,audio,other}]\n                        [--status {draft,ready,published}] [--tags TAGS]\n                        [--cover COVER] [--deliverables DELIVERABLES]\nmanifest.py meta: error: argument --kind: invalid choice: '不存在' (choose from article, xhs-note, video, cards, poster, audio, other)\n"
}

```

### 06-upstream-selftest-wordcount

```json

{
  "label": "06-upstream-selftest-wordcount",
  "source": "skills/shared/scripts/wordcount.py",
  "argv": [
    "selftest"
  ],
  "started_utc": "2026-10-05T13:46:00.797029+00:00",
  "elapsed_seconds": 0.001996,
  "exit_code": 0,
  "expected_exit": 0,
  "stdout": "[PASS] cjk 4\n[PASS] en 2 words\n[PASS] mixed\n[PASS] num group\n[PASS] check ok\n[PASS] check under\n[PASS] check over\n[PASS] empty target 0\n",
  "stderr": ""
}

```

## 路径拒绝详情

```json

[
  {
    "input": "outputs/loose.md",
    "error": "内容产物必须写入 outputs/<具体主题>/，不能散落在根目录"
  },
  {
    "input": "outputs/test/result.md",
    "error": "项目目录名过于泛化: test"
  },
  {
    "input": "outputs/_scratch/file.md",
    "error": "内容产物不能写入系统路径"
  },
  {
    "input": "outputs/主题/../../escape.md",
    "error": "输出必须位于 <EXERCISE_ROOT>/fixtures/outputs内: outputs/主题/../../escape.md"
  }
]

```

## 首次尝试错误 历史路径已规范化

```text

(empty)

```

```text

Traceback (most recent call last):
  File "<EXERCISE_ROOT>/run_exercise.py", line 48, in <module>
    RESULT={'started_utc':stamp(),'python':sys.version,'platform':platform.platform(),'steps':[], 'upstream_selftests':[], 'custom_cases':[], 'operations':[], 'limitations':[
                                                                  ^^^^^^^^^^^^^^^^^^^
  File "<PYTHON_STDLIB>/platform.py", line 1245, in platform
    system, node, release, version, machine, processor = uname()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<PYTHON_STDLIB>/platform.py", line 865, in __iter__
    (self.processor,)
     ^^^^^^^^^^^^^^
  File "<PYTHON_STDLIB>/functools.py", line 998, in __get__
    val = self.func(instance)
          ^^^^^^^^^^^^^^^^^^^
  File "<PYTHON_STDLIB>/platform.py", line 860, in processor
    return _unknown_as_blank(_Processor.get())
                             ^^^^^^^^^^^^^^^^
  File "<PYTHON_STDLIB>/platform.py", line 800, in get
    return func() or ''
           ^^^^^^
  File "<PYTHON_STDLIB>/platform.py", line 828, in from_subprocess
    return subprocess.check_output(
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "<PYTHON_STDLIB>/subprocess.py", line 466, in check_output
    return run(*popenargs, stdout=PIPE, timeout=timeout, check=True,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<PYTHON_STDLIB>/subprocess.py", line 548, in run
    with Popen(*popenargs, **kwargs) as process:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<PYTHON_STDLIB>/subprocess.py", line 992, in __init__
    errread, errwrite) = self._get_handles(stdin, stdout, stderr)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<PYTHON_STDLIB>/subprocess.py", line 1740, in _get_handles
    errwrite = self._get_devnull()
               ^^^^^^^^^^^^^^^^^^^
  File "<PYTHON_STDLIB>/subprocess.py", line 1137, in _get_devnull
    self._devnull = os.open(os.devnull, os.O_RDWR)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<EXERCISE_ROOT>/run_exercise.py", line 35, in audit
    if writing and not within(p): raise RuntimeError('Write outside exercise: '+str(p))
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: Write outside exercise: /dev/null

```

## 真实源码锁定

```json

{
  "repo_url": "https://github.com/ZJU-REAL/Easel",
  "commit": "6c049ceb73b1b74a73448664dcd4dbc7e051442a",
  "commit_datetime": "2026-10-05T06:38:03Z",
  "git_describe": "v0.2.1-79-g6c049ce",
  "pyproject_version": "0.2.1",
  "package_init_version": "0.1.1",
  "license": "Apache-2.0 at repository root; no NOTICE present. Bundled skill/reference licensing not comprehensively certified.",
  "copied_files": [
    {
      "path": "easel/persona.py",
      "sha256": "bb8f43f6e478d440acb67bc69ee7fa1d3f4e1353e18385071eba4771fc4ae1b0",
      "bytes": 4342
    },
    {
      "path": "skills/shared/scripts/manifest.py",
      "sha256": "84f12643ee833696107caaaf2b4fcc82c11b5755c2ade49d770fa14cda8cc58c",
      "bytes": 16727
    },
    {
      "path": "skills/shared/scripts/output_paths.py",
      "sha256": "00672d9b6129acae8c0e08764f6b6d5787f501326b077b396734e942bb197139",
      "bytes": 3628
    },
    {
      "path": "skills/shared/scripts/wordcount.py",
      "sha256": "67a5be020d330dd32479907cad8de14b728fd9418b557fd64c5638799c92da0d",
      "bytes": 7513
    },
    {
      "path": "skills/shared/scripts/content_guard.py",
      "sha256": "f459c857f7aa841b63f0050a65a59957022a6f1da3749e6ace62f1a7c734b866",
      "bytes": 21848
    },
    {
      "path": "skills/openclaw/asset-manager/scripts/assets.py",
      "sha256": "33512eafa3896624b1a5cc57a39264c49e6577975798eaaabd1a8d48f8d19fc1",
      "bytes": 17859
    },
    {
      "path": "LICENSE",
      "sha256": "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4",
      "bytes": 11357
    }
  ],
  "source_social_post": {
    "historical_access_status": "HTTP 403; source text was not retrieved"
  },
  "scope": "Exact original stdlib components copied; no upstream code modified, no full installer, no gateway, no LLM, no publishing."
}

```

## 成功标准和未测范围

15/15是自写命名检查；3/3是上游selftest入口；20是组件调用。wordcount的8条内部PASS与content_guard内部分类统计不相加。完整pytest未运行。

未运行模型、OpenClaw、Web、Easel主CLI、真实账户登录、发布、归因、archive/--apply或全局hook。扫描通过只说明本例规则命中行为，不等于完整内容审核或外部平台接收。

历史证据公开副本保存在ZIP的evidence目录，重放会写出自己的logs/results/snapshots；绝对路径和时间戳变化属预期。
