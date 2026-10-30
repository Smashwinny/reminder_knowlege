# hand-drawn-styles 独立交付审核记录

结论：PASS。通过范围是下列确定字节的五件学习交付、五份公开 vault 候选及本审核记录。37 个检查是已有离线实验的预期行为检查，不是模型质量通过率。远端发布、知识网站保存、Git 提交推送与 Windows 备份均须另行取得回执，本记录不替代这些状态。

审核标识：HDS-REVIEW-20261011-A。由与制作执行者不同的独立审核会话完成。审核日期：2026-10-11 UTC。
本次审核只读取既有文档、图像、源码、压缩包与去标识汇总；未运行 lab.py、未重跑上游 CLI、未调用图像模型或下载真实锚点，未访问私有知识站点，未执行 Git 命令、Reminder 操作或外部发布。仅在审核通过后新增本文件。

## 逐页视觉审核

实际逐张打开最终渲染的 page-01.png 至 page-11.png，11/11 页全部检查。最终 PDF 为 ReportLab 直接生成的 A4、11 页文件。其最终字节指纹见下表；PDF 元数据没有用户姓名、嵌入 JavaScript、表单或加密。未把文本提取当作视觉审核。

1. 第 1 页：主题、范围与 12 个递进问题齐全；范围明确限定文本与合成 PNG。
2. 第 2 页：问题 1–2 的配方工具定位和知识增量清楚，未声称已运行模型。
3. 第 3 页：问题 3–4 的编号/别名与一次替换说明可读；中文括号例子完整。
4. 第 4 页：问题 5–6 正确区分预期拒绝与比例字符串被接受的验证缺口。
5. 第 5 页：问题 7–8 正确区分文本、调用包、画风参考和角色参考。
6. 第 6 页：问题 9–10 的文件/像素哈希和缺锚点拒绝说明完整。
7. 第 7 页：问题 11–12 的 candidate/final 边界及安全接入范围完整。
8. 第 8 页：能力、四个用途、知识查重范围与未验证项清楚。
9. 第 9 页：实验 1–3 的命令、实际观察和失败条件完整。
10. 第 10 页：实验 4–6 的比例反例、正式路径拒绝和 PNG 指纹范围完整。
11. 第 11 页：12 次 CLI、37 checks、版本、许可与六个固定来源链接均可读。

全部页面均未观察到文字截断、重叠、缺字方框或页码错序。HTML 只做静态结构审核：12 个唯一问题锚点、12 个内嵌 SVG、目录链接全部可解析，无 script、iframe、form 或外部资源加载标签。HTML 浏览器呈现及 HTML→PDF 路径没有验收，既有受阻路线未重试；该 PDF 不是 HTML 转换产物。

## 固定来源和原样依赖

上游固定提交：4132988b8596bfa36321c970a4472d4e3bb25d96。只读解析本地该提交对象与树，核对以下七个文件的提交树字节、工作副本、练习副本及 ZIP 内容一致。README、PROTOCOL、STYLES 的相关配方/合同，render_prompt.py 的路由、参数、单次替换、比例追加、PNG 解码及 payload/CLI 路径，hosted_images.py 的清单、文件哈希与离线拒绝机制均与学习材料的有限结论一致。

对 STYLES 的核对包括编号结构和本次所用画风 1，以及 3.1/19/20 的合同条款；没有声称执行了全部 21 套配方或所有别名。上游关于模型快照、历史样图及视觉效果的声明只作为固定版本中的设计/来源声明，不作本轮实测背书。

| 上游文件 | SHA-256 |
|---|---|
| README.md | bff2b62e4eaa04953c60d5576223c48af93c357286d54161257a9ad7daaef60c |
| PROTOCOL.md | 27f42c6c8f7b99f782c0adc58dc76bddcb46412b49a0b3367e5285604913468e |
| STYLES.md | c1793d1514bd01bc8ec511c1072bdeea37281c435a42944a38613ea037480887 |
| LICENSE | 1315a1123cedfccc762cfbf2685be6abf61b56714866928d9eb7ab6e52a505ca |
| scripts/render_prompt.py | 8eb9fa27a918db2d9e3c715584067731cc4a59b9f1e036d148e7e01b47f360eb |
| scripts/hosted_images.py | 89fc8e59b615be9473af1d6cd1bfe5158319f8f78f9d32a157beb4bb6097b232 |
| assets/image-manifest.json | 9c6b57ae20bb4fcf7487763adfd4558c1c52b96e669bb1eacd868b5f241c3caf |

MIT LICENSE 的版权声明和许可全文完整保留，未改写原样上游文件。练习包是限定离线教学所需的最小依赖集合，并非完整生产安装包；其中不含真实锚点，也没有执行生产图像验收器。

## 既有实验证据复核

逐条读取原始 commands.jsonl、lab.py、六份 out/*.json 和六份 out-*.txt。六份标准输出捕获与六个结果对象完全一致；公开实验日志嵌入的六个结果也逐对象一致。既有执行时间为 2026-10-11 07:49:05.751851 至 07:49:06.875639 UTC。

| 步骤 | 显式 checks | CLI 次数 | 退出分布 | 证据限定 |
|---|---:|---:|---|---|
| catalog | 3 | 1 | 1 × 0 | 21 个唯一编号，含 3.1 |
| template | 6 | 2 | 2 × 0 | 仅编号 1 与 xkcd 的字节等价、单次替换 |
| guards | 12 | 4 | 4 × 2 | 缺参数、多参数、未知编号、空 N 四个预期拒绝 |
| aspect | 6 | 3 | 3 × 0 | 无比例、16:9、not-a-ratio 三例；最后一例是验证缺口 |
| offline | 5 | 2 | 2 × 2 | 画风 19 缺锚点及未许可纯文本生产两个负例 |
| integrity | 5 | 0 | 直接函数调用 | 原创 2×2 PNG 文件及像素指纹 |
| 合计 | 37 | 12 | 6 × 0；6 × 预期 2 | 全部符合各自预期 |

12 条原始 CLI 记录都有 UTC、参数、cwd、环境、实际/预期退出码、stdout 和 stderr。lab.py 固定 HAND_DRAWN_OFFLINE=1 及独立空缓存；既有调用记录没有模型/API 或参考图下载命令。offline 两次拒绝均无 stdout，不能计为已取得正式 JSON 包或生产出图成功。37 中包含直接函数检查，不可写成 37 次 CLI 或模型测试。

原始 commands.jsonl SHA-256：ac09d4532fad4bd0da5e8817441c99fe36e9a4c4d4f8542d77c68dfda00de90e。
lab.py SHA-256：524d23346abb9940884dbf23f67c1d10eebd73a763ee59da0339d4ba1ee54ce8。

公开日志和 ZIP 的 commands.jsonl 只把解释器安装路径改为 python；逐行比较后，其余参数、环境、时间、退出码、stdout/stderr 完全保持，公开日志与 ZIP 的 12 条记录一致。审核中发现的“声称脱敏但仍含解释器绝对路径”问题已由制作方修正，并对最终文件重验。原始记录未改动。

对已存在的三张 PNG 另做只读解码核对：均为 2×2 RGB；fixture 与 metadata 的像素 SHA-256 同为 e0c644c801cee721861b30d6a9e7f172ad8459cff1ef21ce9b29d2c890ace689；changed 为 61d2393ce936f31fe2707fd6ed554d9fcd4564dd0df7dfb344a135fad5c1de9b。该核对只是检查既有证据，不新增实验计数。metadata 仅含 original synthetic fixture 备注；文件字节哈希与像素哈希的区分真实存在。

3.1 的三阶段、19 的 candidate-only 评分门和 20 的 final-candidate 验收器仅核对设计与有限拒绝路径。未验证真实模型、快照可用性、参考输入保真、角色保持率、成图评分或生产环境完整性。

## 知识复用和候选增量

公开知识基线为 81732d1b7d14d1e4fd457d6f8218cb966aadf0b5。对提供的六份基线材料逐文件重新计算 UTF-8 字节长度、SHA-256 与 Git blob SHA-1，全部匹配取证指纹和基线树切片。六份为总览、提示词模板、PromptAsCode提示词即代码、Agent输出协议契约、图像提示八要素、快照契约与不可变只读。相关概念正文及 Qwen 模板/协议分层段落已核对；总览主要用于结构、查重和追加前缀检查，不声称逐项复验其历史内容。

去标识网站取证汇总记录 17 篇、29 页、142 块、全部重建 SHA 匹配，以及项目名称 0 命中。补充汇总明确：协调者精读 Qwen-Image-2.1 的模板/PromptAsCode、解析与契约分层、参考图有序角色和未执行模型边界；其余内容只重建校验与名称检索。审核者只复核该汇总及公开材料，没有独立重取或重读 17 篇私有网站原文。名称 0 命中不等于全库语义去重完成。

该去标识汇总 SHA-256：f73b035ee11fb1bb30bdc31390840627b870f88f6ebde36e0b185301ad14ad99。

五份公开候选的准确增量：
- 总览追加本次项目与三个概念链接，原有 138464 字节保持精确前缀。
- 提示词模板追加一次替换与四类错误输入；原有 1147 字节保持精确前缀。
- PromptAsCode 提示词即代码追加配方/脚本/资产固定与两类指纹；原有 3946 字节保持精确前缀。
- Agent 输出协议契约追加实际拒绝门和比例语义缺口；原有 8304 字节保持精确前缀。
- 新增项目笔记 hand_drawn_styles；没有新建模板或输出契约同义概念。图像提示八要素与快照契约仅关联，未改写。

新增项目中的六个交付链接与预期仓库根目录 hand_drawn_styles/delivery 的文件名一致；发布时须将六件一起放在该位置。本审核不把本地候选链接检查写成远端可访问验证。未读取用户本机最新 vault，也未复验旧项目产品命名、法规或模型质量。

## 隐私与压缩包完整性

检查五件交付、ZIP 全部 26 个成员及五份公开候选。未发现私有网站原记录、私有记录/用户标识、账号凭据、令牌或用户机器路径；ZIP 没有 Git 元数据、缓存、身份回执或私有站点导出。包内网址来自固定上游公开 GitHub、公开图片托管与徽章；HTML 的 www.w3.org 仅是 SVG 命名空间。既有公开 vault 内容保持原样，本次增量不携带私有知识原记录。此结论是对列明候选的检查结果，不是对任意未来增补的保证。

ZIP CRC 全部通过，26 个成员无重复路径、路径越界或符号链接，解压后总字节数 233381。所有成员均计算 SHA-256 并与本地对应来源比较；唯一有意差异是公开 commands.jsonl 的解释器路径脱敏，SOURCE.txt 为原创来源说明。以下是完整成员清单。

| ZIP 成员 | 字节 | SHA-256 |
|---|---:|---|
| exercise/commands.jsonl | 17725 | bc4a0b2ef74dbf5dcf26f6c2a4dbfc2cbaf9db6f15541af321b8e00cb0ef0e0f |
| exercise/lab.py | 5524 | 524d23346abb9940884dbf23f67c1d10eebd73a763ee59da0339d4ba1ee54ce8 |
| exercise/out/aspect.json | 1009 | ced5651fddc019179f8cafa0bd8ba096ab195451dba6aced2529f34657d79571 |
| exercise/out/catalog.json | 9356 | 5b32d741cbf922f9741cdaa6eb6682dcfd3dd59e2a0c638f2088d0fce497f7c1 |
| exercise/out/changed.png | 73 | 15fc975aec957e942fcbcdb1f4bafde664ff170e0f5a52bab715918a585a66a4 |
| exercise/out/fixture.png | 73 | 784cb9d63b17875d24b9b7240a598a0e6fae13d5bb00fd6ceaada220b1dd41bf |
| exercise/out/guards.json | 2060 | 4cfb750fc3d0ed27aa0a5998cf32a4843fc6e30d233ed7c75ec90438f9e38f65 |
| exercise/out/integrity.json | 973 | 1b42e2d9d79bbd1325ed5574008b8fff93ef10ff1747aeed83ab93c13ca08f41 |
| exercise/out/metadata.png | 119 | f8b93507020da7122f9926fd5c67b15dadbc1f5f699f7e2034ff10b6c888126e |
| exercise/out/offline.json | 783 | ddec8d92003030117ce9b0dea717059ea1a2fceab6636dddf4d4997dcd2e8a69 |
| exercise/out/prompt.txt | 1018 | 8352b22872f87cafa955176d5852bfc73403821f5e22a356c3d06d28fb155b6e |
| exercise/out/template.json | 887 | decdb6f4bf407694fe09ce6d2cee0b4d5fb5cf87b09a01efa7e19dc7e5d2dd71 |
| exercise/out-aspect.txt | 841 | 31bfea9232d6d9f2896e44c2dc04b9d3f94d8128bfee086eb1d05ca34d3a4e90 |
| exercise/out-catalog.txt | 5782 | c86d8e83bc8f11328f821447519cf036a49985db6c095ddfe3b4aa51856059bc |
| exercise/out-guards.txt | 1394 | a1687a8765e3f80bc24f6821c453a526b59343ed250850afc69146157c1b39c6 |
| exercise/out-integrity.txt | 805 | 30ca18d89ace575e61ba7a17ee15ba055f25a7925a2d697852a9112f9ebdc78b |
| exercise/out-offline.txt | 641 | 480a84e3a621a79e4d70a51f311d983fca77b6f80c238e0a1a08487a7779fe6d |
| exercise/out-template.txt | 727 | e0a7a7eb0b2bb3843806a89dc9dff84197bd96695cea81c7d26de9e4bb1a21ee |
| exercise/upstream/LICENSE | 1063 | 1315a1123cedfccc762cfbf2685be6abf61b56714866928d9eb7ab6e52a505ca |
| exercise/upstream/PROTOCOL.md | 19428 | 27f42c6c8f7b99f782c0adc58dc76bddcb46412b49a0b3367e5285604913468e |
| exercise/upstream/README.md | 19304 | bff2b62e4eaa04953c60d5576223c48af93c357286d54161257a9ad7daaef60c |
| exercise/upstream/STYLES.md | 71892 | c1793d1514bd01bc8ec511c1072bdeea37281c435a42944a38613ea037480887 |
| exercise/upstream/assets/image-manifest.json | 20439 | 9c6b57ae20bb4fcf7487763adfd4558c1c52b96e669bb1eacd868b5f241c3caf |
| exercise/upstream/scripts/hosted_images.py | 11632 | 89fc8e59b615be9473af1d6cd1bfe5158319f8f78f9d32a157beb4bb6097b232 |
| exercise/upstream/scripts/render_prompt.py | 39589 | 8eb9fa27a918db2d9e3c715584067731cc4a59b9f1e036d148e7e01b47f360eb |
| exercise/SOURCE.txt | 244 | 691c60f700d5d6d4e836c2212842332f0b5103e1e6e49cada598e36f8d3794d1 |

## 最终五件被审核交付

| 文件 | 字节 | SHA-256 |
|---|---:|---|
| hand-drawn-styles-exercise.zip | 88223 | 48331c6aa184156eb58ecf9f26a4ed32d0e5348a05243e99874146f7b4a68295 |
| hand-drawn-styles-experiment-log.md | 35388 | 929ae9bc8907473cc26408e3732a5bb309a0368379f22cc1e7ad42cb373eed78 |
| hand-drawn-styles-guide.html | 20653 | db2fed1a89aea7e1a500da907a0906ef954c955be6c16a0fac3ed5273ba5e36f |
| hand-drawn-styles-guide.pdf | 26711 | a1dda26334fc35813ce38e649291e2b358083b5a8643883a16c2ba1a597f0cbd |
| hand-drawn-styles-knowledge.md | 1481 | 032f7726bbf793891347d984ceddb2665a89fbc96d6cb937eef8113e4b5c1a32 |

## 最终五份公开 vault 候选

| 文件 | 字节 | SHA-256 |
|---|---:|---|
| vault/00-总览.md | 138880 | 8de39924847a289a7d85036cd6440c29146cc84f098b5b81677b1bf7fddf2e82 |
| vault/概念/Agent输出协议契约.md | 9375 | 8f90e61f7be53f3b537b4107454000fc46f94ad1b5c854f10e6290bf04a16e73 |
| vault/概念/PromptAsCode提示词即代码.md | 5286 | 93f7fa5b22363ecd530ea24b19e7802710823045957b002a131aa31467b0278a |
| vault/概念/提示词模板.md | 2038 | 961181b6c4a77faf523ea5ec358bf97c44194508b65dc066ec798af0e0c37519 |
| vault/项目笔记/hand_drawn_styles.md | 2248 | 8be08d923b672f579a15eeea7c1d6d8f0336ab5fba1ad10b38874255efa56faa |

## 封存边界

前述五件原件共 172456 字节。本审核记录作为第六件加入后，六件合计 186774 字节，小于 1000000 字节，也小于 1 MiB。本记录有意不嵌入自身哈希；应由外部最终清单记录其 SHA-256。
任何交付或公开候选字节变化都需重新核对相应指纹；影响内容、实验范围或版式的变化需重新审核。通过本记录不代表用户已确认任务完成，也不代表任何网站或仓库已经发布。
