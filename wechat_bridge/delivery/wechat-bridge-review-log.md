# WeChatBridge 本地候选材料独立审核日志

审核日期：2026-10-06 UTC。结论：本地内容审核 PASS，范围是本日志列明的六份候选材料、保存的历史证据，以及下列指定基线上的六文件本地知识库增量。尚未发布文件，也未核验远端发布状态。此结论不是原生应用验收、真实微信接入或目标 AI 收件回执，也不代替用户确认任务完成。

## 当前检查与历史实验分开

本次审核者独立于五份候选材料的整理作者。当前操作仅为读取现有文件、计算摘要、检查归档、读取本地固定 Git 对象，以及渲染并逐页查看最终 PDF。没有执行 run.py、harness、上游程序、SDK 或夹具生成器，没有重新安装或下载依赖，也没有新增实验结果。

2026-10-05 的作者实验及独立新解包复验是历史记录。下面保留它们的命令、时间、失败、结果与有限结论；它们不因本次整理而变成新执行。历史六份交付原件共 348107 字节，逐份重新计算的大小和 SHA-256 与保存的原件备份及配套原件元数据一致；原件未修改。

## 最终 PDF 和 HTML

最终 PDF 为 15 页 A4，审核者将同一最终字节文件用 Poppler 以 110 DPI 重新渲染，实际打开第 1 至 15 页像素逐页检查。正文、图示、脚注、命令和来源页均可读，未观察到裁切、重叠、缺字或断裂命令。12 个中文问题各有图示，另有 5 项能力、5 个用途及 6 步实验；六步的输入、目的、输出、验证、失败处理和历史时间都保留。

HTML 静态检查确认 12 个问题、12 个内联 SVG、6 条完整命令、唯一锚点及有效的内部引用；没有脚本、事件处理器或外部媒体载入。PDF 的 36 个链接注释只含 URI 链接。指南和知识稿中的 20 个不同上游来源链接固定于同一提交，对应文件和行号范围已用现有本地 Git 对象核对；本次没有联网验证链接可用性。公开知识链接保留其历史固定版本，不据此声称核验了当前知识库。

PDF 由 ReportLab 直接生成。HTML 浏览器视觉和 HTML 转 PDF 的历史路线受环境限制，本次没有重试，也没有宣称浏览器渲染通过。

当前发现并修正两处展示问题：移除展示性学习编号；删除知识稿中指向未随六份候选交付提供的查重清单的说明，改为引导读者按笔记名查看已链接的固定公开版本。两处均未改变源码、夹具或历史实验结果。最终 PDF 已在展示编号移除后重新全量检查。

## 归档 原版源码与许可

练习 ZIP 共 105 个文件成员，原成员名和顺序保持不变；104 行 bundle_manifest.json 摘要逐项匹配当前成员字节。外层路径唯一且安全，无外层符号链接；CRC 检查通过。内部专门构造的路径越界、符号链接及损坏归档是历史测试输入，不应当作普通内容直接解压到任意目录。

固定源码为 [freestylefly/WeChatBridge@07b88822debc3bd544ae7a83bc207633b29c3a04](https://github.com/freestylefly/WeChatBridge/tree/07b88822debc3bd544ae7a83bc207633b29c3a04)。46 个 Windows.Core 源码、项目与资源文件，加构建属性、LICENSE 和 THIRD-PARTY-NOTICES，共 49 个上游文件，均与原 ZIP 和该提交的本地 Git blob 逐字节相同。harness、脚本、模块配置、输入清单和全部 20 份夹具保持原字节。stored/deflated 两种普通归档保存相同的 109 字节合成聊天文本和 64 字节附件；sample.bin 不代表已验证图片。

上游 MIT 正文及 Copyright (c) 2026 qzz0518 完整保留，第三方声明及练习自身许可未变。声明提到的 Sparkle 2.9.6 属于原生 macOS 应用范围，本练习没有编译或分发 Sparkle；SDK 和构建缓存不在 ZIP 内。许可信息不构成软件安全或原生功能验收。

归档有 19 个成员相对历史原件发生变化，范围限于整理说明、来源采集状态文字、历史证据中的角色路径替换和依赖的当前摘要清单。原有 stdout/stderr、错误、用例、UTC 时间和计时除路径表示外保持一致。EXPERIMENT_LOG 与 README 明确区分当前静态成员摘要和历史 68 个生成输出摘要，后者没有被伪装成新执行指纹。

## 历史执行证据

现有官方 .NET SDK 10.0.401 归档为 240059572 字节。当前只读取归档重新计算 SHA-512，并将其 4907 个普通成员与现有解压文件逐个比对，均一致；本次没有执行 SDK。历史记录的归档 SHA-512 为：

`51c8b999af9e8dd9998c9edc5944e19a90788862068acd38694e098889054ce8c23d4f0c5cccfa16bf187d044562359e5ee69a9f8ad0bbe913ba90311fbce25b`

历史独立复验从当时冻结 ZIP 新解包，仅复用经过上述核验的 SDK，没有复用旧构建产物或 NuGet 缓存。首次 SDK 网络下载分支没有在那次六步复验中重跑。下列秒数是历史命令外层进程耗时，脚本内部计时另见原始输出，二者口径不同。

- `python3 run.py setup`：UTC 2026-10-05T14:29:43.035634+00:00；4.050222 秒；退出码 0
- `python3 run.py verify`：UTC 2026-10-05T14:29:47.086510+00:00；0.062464 秒；退出码 0
- `python3 run.py fixtures`：UTC 2026-10-05T14:29:47.149306+00:00；0.093837 秒；退出码 0
- `python3 run.py build`：UTC 2026-10-05T14:29:47.243500+00:00；5.901316 秒；退出码 0
- `python3 run.py test`：UTC 2026-10-05T14:29:53.145440+00:00；0.864873 秒；退出码 0
- `python3 run.py report`：UTC 2026-10-05T14:29:54.010740+00:00；0.078951 秒；退出码 0

历史构建 0 warnings / 0 errors。42 个自建测试案例全部通过，归档 21、暂存 8、意图/状态 6、收集 7；一个案例可能包含多条断言。它们不是上游完整 xUnit 或 macOS 测试套件，作者与独立复验是同一组 42 个案例，不能相加成 84 个不同案例。作者六步结果 JSON 为 247.7362ms，独立复验 JSON 为 221.3802ms；独立控制台 SUMMARY 的 227.11ms 包括后续报告写入，均不是 SDK 下载或目标 AI 处理时间。

初次 /usr/bin/time 缺失、初次 41 passed / 1 failed 的 I05 时间精度比较错误及修正后 42/42 均完整保留。修正只涉及自建比较和计时方法，上游字节没有变化。原作者较早记录的 bundleFilesVerified=71 是当时包范围；最终历史独立复验为 104，当前候选清单也是 104。没有改写旧输出抹平这个差异。

作者和独立复验的历史报告各列出 68 个生成常规文件，本次逐项读取相应现存输出，大小和 SHA-256 均与各自历史报告一致。符号链接不在常规文件摘要数量内。随机 GUID 是合成输出身份；输出时间和 GUID 会随运行改变，不要求另一次重放的完整输出摘要逐位一致。

## 关键边界逐项收窄

- I01/I02 显式注入 2026-10-05T12:00:00Z 及 +89/+90 秒，确实检查 90 秒边界；未来一小时仍满足当前单向 age<90 秒条件，这只是行为刻画，不能推出完整防重放保证
- ConsumeIntent 先读取文本、再删除文件、随后解析和判断新鲜度；顺序再次扫描不重放，不能证明并发恰好一次执行，也没有验证删除后崩溃窗口
- Reader/CollectionService 的所谓恢复是在同一测试进程中新建对象并重读磁盘状态，部分中断状态由 harness 构造，没有强杀进程、断电、跨机或多消费者故障实验
- C05 只构造 schemaVersion=8 账本并验证拒绝且不覆盖文件；保留原始名称中的 corrupt，不将其扩大为损坏 JSON 收集账本已测
- InboxWriter 接受 .zip 后缀并不校验完整归档内容；MessageCount、GetTranscript 和 Extract 的检查入口不同，不互相背书
- manifest 随机 GUID 不是内容哈希；暂存后 Ready 可见不证明断电持久性或跨卷事务；回滚清理是 best-effort
- Copied/Delivered 本地状态不能证明原生剪贴板、目标 AI 读取或上传完成；未执行 Win32/WPF/Share Target、macOS Share Extension/AX/OCR、真实微信导出、数据库或账号、安装签名更新、目标应用或真实知识库交付
- 保留聊天原文不等于授权执行其中指令，捕获阶段不执行内容也不等于后续模型天然免疫提示注入

## 公开知识与隐私范围

知识稿保留历史公开查重边界：394 条索引元数据，15 篇相关公开全文，其余 379 篇只查元数据；这不是当前全库查重，也不保证全部未读正文无重复。概念复用、同名 handoff 区分、随机 ID 与内容寻址区分，以及收窄“天然免疫提示注入”的修正均保留。历史学习未重做；随后增加的本地知识库差异审核见下节，历史查重范围不替代该基线的实际读取范围。

已检查候选正文、PDF 提取文本及元数据、ZIP 各成员、普通嵌套样本内容。未发现原记录、账户、领取上下文、展示性学习编号或环境绝对路径泄漏。公开源码中的人名、项目名、许可署名、固定提交、文件哈希及合成 GUID 按证据用途保留。历史日志的环境绝对路径改为角色标签 `<EXERCISE_DIR>`、`<REVIEW_EXERCISE_DIR>`、`<PYTHON_RUNTIME>`；不更改相对路径、命令、结果或时间。

## 指定基线上的本地知识库增量审核

补充审核日期：2026-10-06 UTC。依据保存的连接器响应，候选基线为 main 提交 `66d9eeee243544aece8ab2b366e8604b354458f4`，树为 `16ab91267bdb88a600b39857f04f1c0f51071000`。本次审核只读取现有证据和本地候选字节，没有发出远端请求或写入；保存的基线响应不代表之后 main 永远不变，正式发布前仍需核对其前置条件。

增量共六份 vault 文件、168456 字节：一个新的 WeChatBridge 项目笔记，四篇已有概念的追加，以及 MOC 的两处插入；没有新概念。独立重建的完整 diff 与整理方保存的 diff 一致，删除全部新增片段后，五个既有文件逐字节恢复基线，并匹配 Git blob SHA、SHA-256 和长度。四篇概念各保持旧正文为完整前缀；MOC 历史短标识、项目表和累计文字均原样保留。110 份既有项目与 14 份 tools 文件不在修改范围内，后续应通过该基线树保留。

独立核对 25 份保存的完整正文与对应响应、基线树及摘要：13 篇概念、7 篇项目和 MOC/方法/说明/模板共 5 份。19 份复用阅读的正文与此前保存字节完全一致。该基线有 306 篇概念和 110 篇项目，其余 293/103 份只有路径或标题筛查；没有把元数据计作全文，也没有声称全库正文无重复。

对新增内容中的每个 wiki 链接和相对材料链接，按基线树及当前候选路径检查均可唯一解析；六份配套材料均存在。12 份固定上游来源的已保存连接器正文与本地提交对象逐字节一致，来源只支持原学习所述范围，没有据此执行新实验。

四项概念增补保留原有定义与历史案例，再追加源归档和模型解释分层、manifest/intent/state 的不同生命周期、一次性消费与并发外部效果区别，以及 Retry/Delivered 的证据层。旧“天然免疫提示注入”措辞以明确追加说明收窄，没有悄悄改写历史。项目笔记完整保留 42 个自建用例、初次 I05 失败、未来时间、C05 schemaVersion=8、同进程对象恢复及未调用原生接口等边界。

新增段落和新项目全文的隐私扫描通过；原 MOC 的既有公开历史只按原字节保留，没有将其短标识复写进新增内容。此前五份作者候选文件不变，只有本审核日志补充这段范围。最终发布清单尚需另行将所有候选字节、原件绑定和基线冻结在一起；本内容 PASS 本身不代表远端发布完成。

### 六份知识库候选指纹

- vault/00-总览.md：134021 字节；SHA-256 765ef05cae84ec592a04e675799e3bf9d216bb8b31cabba7f2baa8a580a4d435
- vault/概念/产物留痕与状态外置.md：6979 字节；SHA-256 f40989202b3156179ab2d1495966e5356946f05d00ed711a92fa7673224be68b
- vault/概念/原样捕获与工序分离.md：3334 字节；SHA-256 4e0e815c66b0b2bfdc87fe6aaee7abdecbb4e027a435096b7b536549e7cbb95b
- vault/概念/工具调用生命周期.md：2887 字节；SHA-256 abc8ef5334f84c19b866bb1ddfd742a35340a0f7f84fcff03b407fb31e0626f0
- vault/概念/证据状态机.md：7715 字节；SHA-256 6716ac478a6881bff50939f58355a33b1f6ab892f71324a382aa5b9e4abe0303
- vault/项目笔记/wechat_bridge.md：13520 字节；SHA-256 43f82c589b4f54f98e2c455bbb581480d8a7d684c3a129851877474be181a8f8

## 当前五份候选文件指纹

下列指纹针对本次最终候选文件；本审核日志自身摘要另列于本地六文件冻结清单，避免自包含哈希。

- wechat-bridge-guide.pdf：62892 字节；SHA-256 8c5c9f4f492f5dfaa9a624018a0cedfaed77fe6972c96bce1e7cdc3f3f403e05
- wechat-bridge-guide.html：49366 字节；SHA-256 fc7bb075fc2847219918bca92cc5982d3f2f7a8ccfae51d30773ec30f9061a85
- wechat-bridge-exercise.zip：195021 字节；SHA-256 13b444e0f69f01b311bda92d68ccf8a9589b4344327fc5abcc01e8273c29c4f4
- wechat-bridge-experiment-log.md：8355 字节；SHA-256 0c8ad2547694ad442a06a9f8265d612a33eae32e12a881d98ae33281cd8ae52d
- wechat-bridge-knowledge.md：17677 字节；SHA-256 fdc97fe5f446636e363fcc54eb8c50b21cb0d8515c02fc90505a5c732f8dcd62

## 历史六份原件指纹

以下只标识保留的历史原件，不冒充当前候选字节。

- wechat-bridge-guide.pdf：62978 字节；SHA-256 2d576ae7075c256776427ec7bf2fd08ddec49a3dd5110c4d2ac569d6cfe09c1b
- wechat-bridge-guide.html：49480 字节；SHA-256 c8f263da4e5471302368eccc7b1f5d10e9a567b5c9ad09a1583a8965d8fe6ca8
- wechat-bridge-exercise.zip：194829 字节；SHA-256 217652744cb061165213920046b3ee319f416f7fd3a800107c99bbbe239a7842
- wechat-bridge-experiment-log.md：7184 字节；SHA-256 7f3ab35c455b97a580926dfd0d356246ccd219836c7b726b5edbf4497f193b24
- wechat-bridge-knowledge.md：18346 字节；SHA-256 d90af3839f081d8911c23d4c3f11b4670b583016cb99c73be723752dd1cc87e5
- wechat-bridge-review-log.md：15290 字节；SHA-256 abd02cd585c81f56b8b35498316b75f65c4ef70255506814e462ffa6eeb203df

## 历史独立复验原始输出

以下收录 2026-10-05 六次命令的原始输出，仅以已声明角色标签替换环境绝对路径，并保留重复 ZIP 条目告警、内部计时及早期结果。它们与现存历史原始日志逐块核对，本次没有执行这些命令。

### python3 run.py setup

```text
10.0.401
{
  "version": "10.0.401",
  "officialUrl": "https://builds.dotnet.microsoft.com/dotnet/Sdk/10.0.401/dotnet-sdk-10.0.401-linux-x64.tar.gz",
  "publishedSha512": "51c8b999af9e8dd9998c9edc5944e19a90788862068acd38694e098889054ce8c23d4f0c5cccfa16bf187d044562359e5ee69a9f8ad0bbe913ba90311fbce25b",
  "mode": "explicit-existing-sdk",
  "verifiedSdkFiles": 4907,
  "archiveChecksumMatched": true
}
{
  "step": "setup",
  "startedAt": "2026-10-05T14:29:43.085536+00:00",
  "seconds": 3.988739,
  "status": "passed",
  "error": null
}
```

### python3 run.py verify

```text
{
  "sourceCommit": "07b88822debc3bd544ae7a83bc207633b29c3a04",
  "unchangedCoreFiles": 46,
  "bundleFilesVerified": 104,
  "license": "MIT; Copyright (c) 2026 qzz0518"
}
{
  "step": "verify",
  "startedAt": "2026-10-05T14:29:47.137022+00:00",
  "seconds": 0.003841,
  "status": "passed",
  "error": null
}
```

### python3 run.py fixtures

```text
<PYTHON_RUNTIME>/lib/python3.12/zipfile/__init__.py:1625: UserWarning: Duplicate name: 'same.bin'
  return self._open_to_write(zinfo, force_zip64=force_zip64)
{"syntheticOnly": true, "fixtures": 20, "inputDirectory": "inputs", "manifest": "inputs_manifest.json"}
{
  "step": "fixtures",
  "startedAt": "2026-10-05T14:29:47.193405+00:00",
  "seconds": 0.038668,
  "status": "passed",
  "error": null
}
```

### python3 run.py build

```text

Welcome to .NET 10.0!
---------------------
SDK Version: 10.0.401

----------------
Write your first app: https://aka.ms/dotnet-hello-world
Find out what's new: https://aka.ms/dotnet-whats-new
Explore documentation: https://aka.ms/dotnet-docs
Report issues and find source on GitHub: https://github.com/dotnet/core
Use 'dotnet --help' to see available commands or visit: https://aka.ms/dotnet-cli
--------------------------------------------------------------------------------------
  Determining projects to restore...
  Restored <REVIEW_EXERCISE_DIR>/upstream/windows/src/WeChatBridge.Windows.Core/WeChatBridge.Windows.Core.csproj (in 69 ms).
  Restored <REVIEW_EXERCISE_DIR>/harness/CoreExercise.csproj (in 28 ms).
  WeChatBridge.Windows.Core -> <REVIEW_EXERCISE_DIR>/upstream/windows/src/WeChatBridge.Windows.Core/bin/Release/net10.0/WeChatBridge.Windows.Core.dll
  CoreExercise -> <REVIEW_EXERCISE_DIR>/harness/bin/Release/net10.0/CoreExercise.dll

Build succeeded.
    0 Warning(s)
    0 Error(s)

Time Elapsed 00:00:04.67
{
  "step": "build",
  "startedAt": "2026-10-05T14:29:47.288370+00:00",
  "seconds": 5.845177,
  "status": "passed",
  "error": null
}
```

### python3 run.py test

```text
PASS A01: stored archive yields two synthetic messages and unchanged multiline transcript
PASS A02: deflated ZIP parses and extracts exact transcript and attachment bytes
PASS A03: stored ZIP extracts exact attachment bytes
PASS A04: unknown TXT is retained without inventing parsed messages
PASS A05: attachment-only ZIP is valid with unknown message count
PASS A06: BOM and CRLF preserve the two-message interpretation
PASS A-reject-empty.zip: archive integrity rejects empty.zip
PASS A-reject-empty-file.zip: archive integrity rejects empty-file.zip
PASS A-reject-not-a-zip.zip: archive integrity rejects not-a-zip.zip
PASS A-reject-bad-crc.zip: archive integrity rejects bad-crc.zip
PASS A-reject-unsupported-method.zip: archive integrity rejects unsupported-method.zip
PASS A-reject-encrypted-flag.zip: archive integrity rejects encrypted-flag.zip
PASS A-reject-oversized-declaration.zip: archive integrity rejects oversized-declaration.zip
PASS A-reject-duplicate.zip: archive integrity rejects duplicate.zip
PASS A-extract-reject-traversal.zip: unsafe extraction rejects traversal.zip without creating files
PASS A-extract-reject-absolute.zip: unsafe extraction rejects absolute.zip without creating files
PASS A-extract-reject-symlink.zip: unsafe extraction rejects symlink.zip without creating files
PASS A-extract-reject-case-alias.zip: unsafe extraction rejects case-alias.zip without creating files
PASS A19: nonempty extraction destination is refused and sentinel retained
PASS A20: pre-cancelled archive operation is stopped
PASS A21: raw transcript rejects malformed headers and impossible dates
PASS S01: Staging hidden before atomic Ready commit; original ZIP hash preserved
PASS S02: duplicate display names are disambiguated without overwriting originals
PASS S03: invalid second item rolls back entire staging batch and records failure
PASS S04: injected per-file limit rejects before Ready publication
PASS S05: injected total-size limit rejects whole batch
PASS S06: InboxWriter accepts .zip filename without validating archive integrity
PASS S07: pre-cancelled staging leaves no Ready or partial batch
PASS S08: source symlink is rejected
PASS I01: fresh intent is consumed once, including after reader restart
PASS I02: exactly 90-second-old intent is expired and consumed
PASS I03: malformed intent is deleted without executing
PASS I04: state initializes once and preserves target/chat/scene after outcome
PASS I05: clipboard initial state records copied metadata only; no clipboard API is called
PASS I06: future timestamps are considered fresh by current one-sided age check
PASS C01: freeze preserves batch order/hashes, blocks edits and splits late share
PASS C02: restart changes interrupted delivery to Retry and does not recollect
PASS C03: remove/undo across restart restores original bytes and member order
PASS C04: interrupted removal is recovered from on-disk undo record
PASS C05: newer or corrupt collection ledger is rejected without overwrite
PASS C06: unnamed collection cannot freeze without explicit synthetic name
PASS C07: protected pending collection survives retention including unreadable manifest
SUMMARY passed=42 failed=0 durationMs=227.11 results=<REVIEW_EXERCISE_DIR>/results/20261005T142953758Z
{
  "step": "test",
  "startedAt": "2026-10-05T14:29:53.192805+00:00",
  "seconds": 0.807538,
  "status": "passed",
  "error": null
}
```

### python3 run.py report

```text
{
  "sourceCommit": "07b88822debc3bd544ae7a83bc207633b29c3a04",
  "unchangedCoreFiles": 46,
  "bundleFilesVerified": 104,
  "license": "MIT; Copyright (c) 2026 qzz0518"
}
{
  "passed": 42,
  "failed": 0,
  "testDurationMs": 221.3802,
  "runDirectory": "<REVIEW_EXERCISE_DIR>/results/20261005T142953758Z",
  "sourceCommit": "07b88822debc3bd544ae7a83bc207633b29c3a04",
  "portableCoreOnly": true,
  "nativeIntegrationVerified": false,
  "limitations": [
    "No macOS Share Extension, AX, OCR, WeChat DB or real WeChat files",
    "No Windows WPF/Share Target, clipboard or real target-app delivery",
    "No exactly-once/concurrent-consumer guarantee",
    "InboxWriter stages .zip-named bytes; archive integrity is a separate check",
    "Future-dated intents are fresh under the current one-sided age check",
    "GUID IDs are not content hashes"
  ]
}
Hashed 68 output files; see experiment-report.json
{
  "step": "report",
  "startedAt": "2026-10-05T14:29:54.062529+00:00",
  "seconds": 0.014871,
  "status": "passed",
  "error": null
}
```

