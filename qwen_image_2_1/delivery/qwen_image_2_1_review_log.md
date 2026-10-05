# Qwen Image 2.1 公开整理与知识合并独立审核

审核时间：2026-10-05 19:57 UTC。

## 本次结论与最终冻结条件

**内容审核通过，限定于六份公开学习材料及八份知识库文件。** 本审核独立于公开副本整理者及知识合并者，直接核对原件、最终公开文件、差异、固定源码与许可、历史执行证据、知识关联和新增内容的公开边界，并重新渲染、实际打开最终 PDF 的全部 11 页。没有直接复用原学习审核或作者自检作为本次通过依据。

发布前仍须生成同目录 [publication-manifest.json](publication-manifest.json)，逐项核验十四份已审文件的完整路径、最终字节与 SHA-256、六份学习交付的原件来源指纹、七份既有知识库文件的公开基线指纹，以及清单自身的公开内容和十五项精确文件白名单。该最终冻结核验通过前不批准发布；任何字节改变都须复核。本日志不记录自身散列，由发布清单记录最终指纹，避免循环自引用。远端发布成功仍须单独以实际提交及回读证明。

本轮**没有重跑学习实验、上游接口函数或消费者策略**，没有安装依赖、加载图片、下载权重、调用模型或 API、使用 GPU、进行付费实验或重试 HTML 浏览器及 HTML 转 PDF。下半部分的五步重放、21 项上游行为检查、6 个消费者策略样本及原版 PDF 检查均属于原学习历史。本次执行的是文件、内容、来源、链接、公开边界与版面审核。

## 原件与历史执行证据

重新计算原六份学习成品的字节数与 SHA-256，全部符合原最终清单，原件总计 163,319 字节且未被改写。公开副本与历史原件使用各自的指纹，不能把历史文件散列当作当前验收结果。

最终 ZIP 有九个文件，展开总字节 55,437，CRC 正常；路径全部相对，无父目录穿越、符号链接、Git 元数据、虚拟环境或字节码。与原 ZIP 逐成员比较，仅 README 增加原学习日期与当前未重跑说明，其余八个成员逐字节不变，包括全部脚本、来源说明、历史预期 JSON、完整官方源码、LICENSE 与 NOTICE。

将包内完整 pe_core.py 与固定 Git 提交 6627d87c6433151463ec4b48b8945a24fcf16a35 的对象逐字节核对，SHA-256 为 fd9732bbba71468fb24bd81de5c209f0db2941f01d1e556d52b5a6deba0f1fe5。完整 LICENSE 与固定代码 Git 对象和已保存模型许可一致，SHA-256 为 8dc973f024ff95966bea25866efa443fd16776dcb1001e681e3d467ea572b28d；NOTICE 的要求归属文字保留。上游材料仍适用 Qwen Research License，研究/评估与商业另行许可边界保留，没有被无声改为仓库或其他组件的许可证。Diffusers 的 Apache-2.0 不替代 Qwen 材料许可。

公开实验日志的十一段 fenced 命令、输出及完整结果 JSON 与原件逐字符相同。ZIP 内预期结果、原实验结果与历史独立函数重放结果的结构和值相同；每项实际值、预期值及通过标记一致。作者五步运行发生在 2026-10-05 07:05 UTC，历史独立重放发生在 07:06 UTC；当前公开整理没有创造新的运行结果。

计数严格分开：

- 21 项是针对真实上游源码编写的预期行为检查：2 个任务 profile、16 个解析用例、1 个消息顺序用例、2 个记录检查；不是 21 个解析样本、官方测试套件或模型质量测试
- 21/21 包括预期出现的四类宽松解析：未知比例、编辑同时给两个比例字段、两个都缺失、越界参考；通过不代表验证缺口已修复
- 另一个独立编写的消费者策略从这些回答中选择 6 例，历史结果为 2 接受、4 拒绝，6/6 符合练习规则；不合并成“27 项上游测试”，也不代表官方完整 schema、通用安全校验或图像质量
- synthetic 图片标记和普通物体回答均为合成输入，只按字符串处理。json_repair 缺席是历史实验的明确条件；未测试路径继续明确标注

## 教学内容、命令与链接

最终 PDF、HTML、ZIP README 与实验日志的五条命令逐项静态比对一致，没有为验证说明而执行这些命令。教材保留普通物体的合成样本、输入与结果对应、成功判据、历史 UTC 时间及有限验证范围。

HTML 保留十二个问题、十二张可解析的内联 SVG、五项能力、五种用途与五步练习；ID 唯一、目录锚点存在，没有脚本、iframe、事件处理器或外链媒体/样式资源。十二个问题及 SVG 与原件逐字节相同。PDF 四个固定公开来源链接与原版一致，分别指向已核验代码提交的 README、核心接口、LICENSE 及固定模型树。未声称进行实时外站可达性测试。

PDF 只有第 1、9、11 页的内容流改变，用于历史运行日期和公开知识范围说明；其他八页内容流与原件完全相同。知识笔记保留十九篇原学习公开正文来源及指纹；当前合并说明与历史候选内容分开，避免将早期提案当成最新合并状态。

## 本次 PDF 的逐页实际视觉检查

最终公开 PDF 为 11 页 A4，45,377 字节，SHA-256 为 92fac69cc18ae6904b2e325de6a48952b3ada33a3942501c1826d6b85a7d2555。独立审核者用 Poppler 按 120 dpi 重新渲染最终文件，于 2026-10-05 19:51:36–19:51:51 UTC 实际打开全部十一张页面图像，没有用作者截图或文字提取代替视觉检查。

1. 第 1 页：标题、十二问路线、历史运行日期、无推理边界及许可说明完整
2. 第 2 页：统一任务与生成管线两问，文字和图形没有裁切
3. 第 3 页：7B 与全套管线的区别、单流结构、单位和长标识可读
4. 第 4 页：混合粒度注意力与调度器说明、箭头及示意标签完整
5. 第 5 页：潜空间尺寸与 RGBA/alpha 分层可读，棋盘格仅作示意
6. 第 6 页：参考图顺序与前缀缓存说明完整，未把顺序测试当作图片理解
7. 第 7 页：改写器与生成器、解析与领域验证的区别清晰
8. 第 8 页：五项能力和五种用途完整，官方声明与未验收效果区分明确
9. 第 9 页：历史运行、当前未重跑声明及前三步命令、时间、判据无裁切
10. 第 10 页：后两步命令、21 项上游检查与 6 个策略样本分开呈现
11. 第 11 页：394/19/375 的历史公开读取范围、固定来源、许可与未验证事项完整

未观察到缺字方框、文字覆盖、命令越界或页脚异常。字体缓存不可写警告未阻止渲染，也未通过修改系统权限处理。PDF 不含 JavaScript、表单、打开动作或嵌入附件；ReportLab 直接生成的 PDF 视觉通过，不等于 HTML 的浏览器视觉或跨浏览器兼容性通过。

## 知识合并、去重与双向关联

当前合并以公开仓库提交 da063bc9b39722bb5fc7345dadb2f42a59ddda4d、树 33c29723dfe90afe0b31debe4bd4b26082f346ff 为基线。合并者本轮通过连接器取得三十二份完整公开正文；审核逐一比对其原始读取响应、保存字节、树中的 Git blob 和大小，以及 SHA-256，全部一致。这里是独立复核本轮读取证据，不声称审核者另外发起过一轮远端查询。

合并者的完整正文读取范围为总览、方法、仓库说明、两份模板、20 篇相关概念与 7 篇项目笔记。固定树有 304 篇概念、102 篇项目笔记，其余 284 篇概念与 95 篇项目只做路径/标题层筛查。原学习的 394 条元数据、19 篇公开全文、375 篇仅元数据是另一时点的范围，未混作当前统计，也没有声称全库全文查重。

最终知识库范围：

- vault/00-总览.md
- vault/项目笔记/qwen_image_2_1.md
- vault/概念/Agent输出协议契约.md
- vault/概念/PromptAsCode提示词即代码.md
- vault/概念/图像提示八要素.md
- vault/概念/开源验货三查.md
- vault/概念/接缝与桩实现StubSeam.md
- vault/概念/棋盘格假透明修复.md

新增一篇项目笔记、向六篇现有概念追加案例，不新建概念。六份概念旧字节完整保留为前缀；总览只插入一组关联和一行项目索引，没有删除旧行、改写历史累计计数或覆盖先前项目正文。

合并决策与已有概念一致：解析/契约/任务分层补入输出协议；检查点与提示配套作为 Prompt as Code 的项目案例，未与变量槽位、采样机制或跨文件时间漂移强行合为同义概念；参考顺序、输入输出通道、组件许可、函数夹具与桩后端边界分别补入既有主题。旧提示词分数、透明修复精度、其他项目许可与性能没有转作 Qwen 证据。

对上述八份文件的新增文本，七十二个 wikilink 及相对链接均唯一解析到固定树或本次交付。项目与六篇追加概念双向关联；总览可达项目，项目能找到六份交付材料及总览。发布清单链接将在最终冻结核验中确认实际存在。

## 公开边界与本轮更正

审核扫描六份交付全文、HTML、PDF 提取文本与元数据、ZIP 每个成员、八份知识库新增文本，并对 36 个已知非公开标识或来源值做精确匹配，同时检查 UUID、凭据形态、真实工作区绝对路径与非教学内部标记，未发现新增残留。最终发布清单也须通过同样核验。

逐文件证据记录了可公开核对的 preimage URL、Git blob、SHA-256、最终文件指纹及新增差分。旧总览的历史短标识和其他既有公开内容保持原样，不误算为本轮新增私人信息，也不声称已清理整个旧库。新增内容中的 parse_ok、wh_ratio、ratio_follow、profile、source commit 等是公开源码字段或来源指纹；比例和 image 标记是普通教学合成值，没有携带真实账户、任务、会话标识或私人路径。

本轮要求补充知识笔记的当前合并说明，并把后续候选文字标为历史；其余通过项来自实际文件与证据核对。没有尚未解决的内容阻断项。许可、图像质量、透明边缘、多图理解、真实改写、显存、速度、量化及完整部署的未验证边界继续适用，公开发布本身不能补足这些证据。

以下保留原学习独立审核的公开化历史记录；其中“本次”“最终版”、五步重放及相关时间均指原学习阶段，不表示本次公开整理再次执行过这些活动。

# Qwen Image 2.1 历史学习审核记录

原审核日期：2026-10-05 UTC。

以下为原学习交付审核的公开整理版，保留当时实际执行、输出、计数与原版本指纹；它不是当前公开副本的发布验收。公开副本已清理无关流程信息并更新知识范围说明，须另做独立发布审核。

## 历史结论

原版本通过当时限定范围内的交付审核。已独立复现练习包的五条命令，检查原始结果、固定上游字节与许可，重新渲染并逐页查看最终 11 页 PDF，核对 HTML 的 12 问与 12 张内联 SVG，以及知识查重范围和指纹。

历史结论仅认可原版本研究学习材料与 CPU 接口实验的证据完整性，不代表图像模型已部署、生成质量已验收或读者已经掌握。

## 1 独立性与实际操作

本审核由不同于教材作者的独立执行者完成；没有编辑作者的 PDF、HTML、ZIP、实验日志或知识笔记。审核使用新建的空目录解压最终 ZIP，并以其中的脚本和未修改上游代码执行。没有借作者的汇总代替实际运行，没有把更换任务所有者当作独立审核。

原审核没有安装依赖、获取密钥、启动模型服务或执行图片加载。实验审计钩子只属于该次短生命 Python 进程，不是全局设置或操作系统沙箱。

## 2 固定来源与许可

- 官方代码固定提交：6627d87c6433151463ec4b48b8945a24fcf16a35
- 模型元数据固定版本：d26bb61231c349cf6b7896fa83353113880e1ba3
- 独立核对本地正常 Git 检出 HEAD；11 份小型源码快照均与该提交的 Git 对象字节、长度和 SHA-256 相符
- 16 份模型小文件与读取的固定版本清单及 Git blob 指纹相符；没有下载或校验完整权重文件，远程权重大小与哈希仍属于元数据
- ZIP 中完整 pe_core.py 与固定 Git 对象逐字节相同，SHA-256 为 fd9732bbba71468fb24bd81de5c209f0db2941f01d1e556d52b5a6deba0f1fe5
- ZIP 内完整 LICENSE 与固定源码和模型许可逐字节相同，SHA-256 为 8dc973f024ff95966bea25866efa443fd16776dcb1001e681e3d467ea572b28d
- NOTICE 保留许可要求的完整归属文字，新增练习脚本与未修改官方源码明确区分
- 教材正确注明 Qwen Research License 的研究/评估范围与商业用途另行许可边界；没有用 Diffusers 的 Apache-2.0 替代模型和 Qwen 代码许可

可核对来源：[固定源码](https://github.com/QwenLM/Qwen-Image-2.1/blob/6627d87c6433151463ec4b48b8945a24fcf16a35/prompt_rewrite/pe_core.py)、[完整许可](https://github.com/QwenLM/Qwen-Image-2.1/blob/6627d87c6433151463ec4b48b8945a24fcf16a35/LICENSE)、[固定模型版本](https://huggingface.co/Qwen/Qwen-Image-2.1/tree/d26bb61231c349cf6b7896fa83353113880e1ba3)。

## 3 最终 ZIP 的五步独立复现

环境为 Python 3.12.14、Linux Bash。五条命令与最终 PDF、HTML、ZIP README 和实验日志一致。执行目录为新解压包中的 exercise；所有命令退出码为 0，标准错误为空。
### 步骤 1

```bash
python3 -I -S -B check_environment.py
```

独立重跑 UTC：2026-10-05T07:06:31.537564+00:00 至 2026-10-05T07:06:31.568919+00:00；退出码 0。

实际标准输出：

```text
experiment/upstream/pe_core.py: SHA256 OK fd9732bbba71468fb24bd81de5c209f0db2941f01d1e556d52b5a6deba0f1fe5
experiment/upstream/LICENSE: SHA256 OK 8dc973f024ff95966bea25866efa443fd16776dcb1001e681e3d467ea572b28d
Python 3.12.14
isolated=True no_site=True no_bytecode=True
READY: stdlib-only CPU exercise; no model, image loading, API or network
```

### 步骤 2

```bash
python3 -I -S -B experiment/verify_contract.py > results.json
```

独立重跑 UTC：2026-10-05T07:06:31.568953+00:00 至 2026-10-05T07:06:31.626836+00:00；退出码 0。

标准输出按命令重定向为 results.json，没有把终端空输出当作测试结果。

### 步骤 3

```bash
python3 -I -S -B inspect_results.py messages
```

独立重跑 UTC：2026-10-05T07:06:31.626892+00:00 至 2026-10-05T07:06:31.653619+00:00；退出码 0。

实际标准输出：

```text
1. image_url: synthetic:image1:blue_cube
2. image_url: synthetic:image2:wooden_shelf
3. text: Place the cube on the shelf
ORDER PASS: image1, image2, text; markers were not fetched or decoded
```

### 步骤 4

```bash
python3 -I -S -B inspect_results.py parser
```

独立重跑 UTC：2026-10-05T07:06:31.653647+00:00 至 2026-10-05T07:06:31.678422+00:00；退出码 0。

实际标准输出：

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

### 步骤 5

```bash
python3 -I -S -B inspect_results.py validate
```

独立重跑 UTC：2026-10-05T07:06:31.678452+00:00 至 2026-10-05T07:06:31.704340+00:00；退出码 0。

实际标准输出：

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

### 原始结果与负对照

- 新生成 results.json、ZIP 的 expected_upstream_results.json、最终实验日志里的完整 JSON 三者结构和值完全相同
- 上游共 21 项预期行为检查：2 个任务 profile、16 个解析用例、1 个消息顺序用例和 2 个记录检查；全部通过
- 正对照包括正常文生图/编辑对象、字符串内花括号和转义引号、旧字段拼写及末尾有效候选
- 负对照包括无 JSON、截断 JSON、尾逗号及空提示字符串；在 json_repair 缺席的本次环境下进入 parse_ok=false 回退
- 4 个领域约束缺口样本分别是未知比例、编辑同时给两个比例字段、两个都缺失和越界 <image99>；上游仍返回 parse_ok=true。通过指观察到预期的宽松行为，不是上游已修复或语义校验通过
- 独立编写的 local_policy 对上述 6 个选定样本给出 2 接受、4 拒绝，6/6 符合练习规则；它不是官方完整 schema、通用安全验证器或模型质量测试
- 两个 synthetic: 图像标记只作为字符串进入消息，没有获取或解码图片；上游代码的可选 json_repair 未加载，成功运行没有触发被阻止的审计事件

未运行模型、客户端、load_image、系统提示文件读取、输入文件/图片路径解析或其他未列出的上游路径。没有把静态源码观察计入实际函数覆盖率。

## 4 PDF 与 HTML 检查

使用 Poppler 的 pdftoppm 重新渲染最终 PDF 为 11 张 PNG，逐张实际打开查看，而不是只读提取文本。最终 PDF 的 SHA-256 为 21f63d40194220e9e59c8e660d6c7783b2134b5149e809ff51726a25f024b5a5。

- 第 1 页：标题、范围、12 问阅读路线、许可与无推理边界清楚
- 第 2 页：问题 1–2、统一任务与管线示意，文字和图形完整
- 第 3 页：问题 3–4、参数归属与单流示意，单位与代码标识可读
- 第 4 页：问题 5–6、注意力和调度器示意，没有越界或覆盖
- 第 5 页：问题 7–8、潜空间及 RGBA，静态观察与未测试 alpha 边界可见
- 第 6 页：问题 9–10、参考图顺序与前缀 KV 缓存，长标识完整
- 第 7 页：问题 11–12、独立改写器与解析/验证分层，说明和图示齐全
- 第 8 页：五项能力与五种具体用途均可读；能力声明与实测区分明确
- 第 9 页：步骤 1–3 的命令、目的、实际结果和成功判据完整
- 第 10 页：步骤 4–5 和两类测试计数分开呈现，无命令裁切
- 第 11 页：当时的知识范围、固定来源、两套版本与未验证事项完整

初稿发现页脚分隔符显示为缺字方框，并提出英文标识和标点换行改进；作者修正后，本审核重新渲染并查看全部最终页面。最终版未发现缺字方框、裁切或重叠。渲染过程中有 Fontconfig 缓存不可写提示，工具仍正常生成全部页面，未因此更改全局目录权限。

HTML 只做结构检查：12 个问题区段、12 张可解析的内联 SVG、唯一编号与有效内部目录目标、五条命令与日志一致。未发现 script、iframe、外部图片或其他活动嵌入。没有浏览器视觉验收，也没有重试受阻的预览/HTML 转 PDF 路线。PDF 为 ReportLab 直接生成，不能把它的视觉通过等同于 HTML 在所有浏览器的显示通过。

## 5 历史公开知识依据核验

- 公开知识索引固定提交：1f61909da967cea8bc68dbfaffc642a4331b3352
- 相关公开正文固定提交：1043e9d6080bff7af9724162e2c44559fab63e40
- 原审核核验了固定索引及 19 篇实际读取的公开正文，其字节数、SHA-256 和 Git blob 指纹相符；配套知识笔记保留这 19 篇的来源和 SHA-256
- 公开索引共有 394 条元数据；另 375 篇只做元数据检索，没有声称全库全文阅读
- 这些数字描述原学习时的公开快照范围，不能证明读者已经掌握或覆盖了其他版本

## 6 资源与证据限制

独立重新求和权重元数据：7 个 safetensors 文件合计 33,115,613,408 字节，约 30.841 GiB。审核时可用磁盘约 29.19 GiB，连这些权重文件自身也无法容纳；未发现 nvidia-smi 路径或 /dev/nvidia 设备节点。这些探测没有替代实际 CUDA/推理验收，也没有从权重体积推出峰值显存。

本次不认可任何关于真实图像质量、透明边缘、多图一致性、文字正确率、推理耗时、显存、量化效果或全管线部署成功的实测断言。教材保持这些项目未验证。所有图示是人工绘制的教学 SVG，所有函数输入/答复是普通物体合成样本。

## 7 原学习版本五份作者文件的历史指纹

以下指纹只对应原学习版本，不是经过公开整理后的现行文件指纹。当前公开副本应以独立发布审核的清单为准；不得将这些历史指纹冒充为当前验收结果。

- qwen_image_2_1_exercise.zip：20257 字节；SHA-256 7bb83b0dab1b873fa6798f60776398309cede5f306b9032cda3bd5e86341f700

- qwen_image_2_1_experiment_log.md：22972 字节；SHA-256 d6ef4b23d64ecfec91e0becbd3fd0546064a92ddf8f2fad0c08453c24af68ea3

- qwen_image_2_1_guide.html：42101 字节；SHA-256 ee29c69b4b388aadee58c45c148978a97c7ce765983176f14818d6a8374da378

- qwen_image_2_1_guide.pdf：45449 字节；SHA-256 21f63d40194220e9e59c8e660d6c7783b2134b5149e809ff51726a25f024b5a5

- qwen_image_2_1_knowledge_notes.md：20198 字节；SHA-256 983e719a25b96a91943efa8e0eb36e57ca1855bb6cac22705d0b80f0772f514e

原学习版本五份作者文件合计 150,977 字节，原六份文件合计 163,319 字节。公开副本的大小和 SHA-256 需单独核验。
