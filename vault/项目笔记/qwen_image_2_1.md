---
tags: [项目笔记, 图像模型, 接口契约]
类别: 模型与源码学习（研究用途）
学习审核日期: 2026-10-05
固定代码: 6627d87c6433151463ec4b48b8945a24fcf16a35
固定模型元数据: d26bb61231c349cf6b7896fa83353113880e1ba3
许可: Qwen RESEARCH LICENSE AGREEMENT
验证范围: CPU 上的改写器接口函数与独立消费者策略
---

# Qwen-Image-2.1：图像模型与提示改写契约

## 是什么，能学到什么

Qwen-Image-2.1 是官方提供的图像生成与编辑模型；本页只讨论普通物体、图标及一般图像模型工程。学习重点是区分模型说明、静态配置、实际接口执行与真实图像效果，尤其是独立提示改写器的协议如何被下游正确消费。

可以借此学习：区分生成器、文本编码器和提示改写器；保存检查点与提示协议的完整配置；保留参考图顺序和画布字段；对宽松解析补充明确的消费者校验；按组件核对许可、资源与实际验证范围。图标、几何纹样、杯子改色或普通物体构图只是可讨论的研究用途，不是此次已生成的成果或商业部署方案。

## 模型架构与证据层

固定官方说明描述 32 层单流 DiT 视觉生成组件，标称 7B 参数；另有标称 8B 的 Qwen3-VL 文本编码器和 VAE。7B 不是全套管线的参数总和，也不是独立提示改写器的大小。官方说明的混合粒度注意力、`causal_condition` 与条件前缀 KV 复用属于文档与静态配置观察，没有运行注意力、缓存或推理速度实验。

固定 VAE 配置包含 64 个潜通道、16 倍空间缩放和四通道输入输出设置。它与 README 的 RGBA 声明可以互相定位，但配置存在不等于本次已获得有效 alpha 输出，更不等于透明边缘质量通过。独立改写器的图片预处理转 RGB 与生成器的输出通道是不同路径，见 [[棋盘格假透明修复]]。

## 已有知识怎样合并

- [[Agent输出协议契约]]：追加解析成功、消费者约束、真实任务正确三层证据；不另建“解析与语义校验”同义条目
- [[PromptAsCode提示词即代码]]：追加检查点、系统提示、任务 profile 与实际采样配置共同固定的项目案例；关联 [[提示词模板]]、[[LLM采样与温度]]，不宣称模板能保证跨模型通用
- [[图像提示八要素]]：追加参考图编号与输入顺序、画布字段的接口约束；关联 [[修改与约束分离]]，文字保留要求不等于像素保护
- [[棋盘格假透明修复]]：追加输入 RGB、模型 RGBA 声明、实际 alpha 与合成边缘分别取证
- [[开源验货三查]]：追加研究许可、商业另行许可与组件划界；关联 [[内容型开源与双许可]]，不套用旧项目的许可证组合
- [[接缝与桩实现StubSeam]]：追加函数夹具、桩服务、真实模型与端到端结果的覆盖边界
- [[代码管边界提示词管判断]]、[[证据状态机]]、[[证据优先质检ProofOverClaims]]、[[源码取证图]]：复用证据纪律，不把声明、源码、合成执行和图像产物混为一层
- [[本地推理引擎]]、[[量化与GGUF]]、[[项目笔记/ollama]]：只关联表示与运行时区别，旧语言模型的显存、速度和文件大小经验不迁移为本模型部署结论
- [[固定版本中的跨文件时间漂移]]、[[快照契约与不可变只读]]、[[单一馈送与schema冻结]]、[[ChatModel与消息类型]]：分别用于版本、输入固定、消费者契约和消息形状对照，不据此声称本项目采用相同实现

[[项目笔记/awesome_gpt_image_2]]、[[项目笔记/gpt_image_prompting]] 提供提示词结构化背景，其文本 Lint 分数没有在本次证明与出图质量相关。[[项目笔记/replicate-hype]] 是趋势聚合站，与本模型部署不是同义主题。[[项目笔记/google_colab_cli]]、[[项目笔记/metrik]]、[[项目笔记/easel]] 只提供日志、计量和产物证据的相关方法；它们的历史实验与平台结论不迁移成 Qwen 实测。

## 已有五步实验与真实结果

原学习在 Linux / Python 3.12.14 中，以 `-I -S -B` 启动标准库练习；直接执行固定版、未修改的 `pe_core.py`，SHA-256 为 `fd9732bbba71468fb24bd81de5c209f0db2941f01d1e556d52b5a6deba0f1fe5`。`json_repair` 未加载。五步依次是文件及环境核验、执行接口检查、读取消息顺序、读取解析结果、运行自写消费者策略。历史独立审核已从全新解压包逐条重放，五条命令均退出 0。

- **21/21 上游源码预期行为检查**：2 个任务 profile、16 个解析用例、1 个消息顺序用例、2 个记录检查；这是练习针对真实上游代码写的检查，不是上游官方测试套件或全函数覆盖
- **6/6 自写消费者策略示例**：从上述回答中另选 6 例，2 接受、4 拒绝；不是另外 6 次模型调用，不合并为 27 项上游测试
- 输入与回答都是合成样本；两个 `synthetic:` 图片标记仅以字符串进入消息，没有请求或解码图片

本次公开知识合并复用已有实验和独立审核记录，没有重新执行学习实验。历史审核认可当时材料与 CPU 接口证据的完整性，不代表公开副本每次修改后都自动通过审核，更不代表本人已掌握全部内容。完整命令、时刻、输出与审核范围见配套日志。

## 核心发现与坑

1. **`parse_ok` 不是严格语义门。** 非空 `rewritten_prompt` 可被提取就可能为 true；兼容旧拼写 `rewrited_prompt`，从后向前找有效候选。未知比例、编辑双比例字段、缺少画布选择、越界 `<image99>` 均真实观察到 true。
2. **失败回退要保留身份。** 无 JSON、截断 JSON、空提示、无 repair 时的尾逗号对象进入 fallback，原回答进入 `positive_prompt`，同时 `parse_ok=false`；原文还在不能当成改写成功。
3. **策略须由消费者显式执行。** 练习策略检查七个给定比例、编辑恰选一个画布字段、引用落在假定两张图内；它不是官方完整 schema、通用安全验证器或意图正确性评估器。
4. **检查点与系统提示配套。** 官方改写器文档描述两个经后训练的 Qwen3.5-VL 9B 检查点，分别服务 t2i 与 edit；不是把基础模型换个名称即可。系统提示文件选择规则不验证权重兼容；任务 profile 与实际采样覆盖项也应记录。
5. **顺序、编号与比例都带语义。** `build_messages` 保留参考图先后，`wh_ratio/ratio_follow` 决定画布意图；只拿改写文本会遗漏契约。字符串顺序正确仍不证明模型理解了图片角色。
6. **进程守卫不是 OS 沙箱。** 首轮加载器曾因探测字节码路径被自身读取白名单拦住，改为编译已校验的源字节后通过；上游代码未改。该经历不升级为任意代码安全保证。

## 未验证边界与许可

没有运行真实提示改写、模型权重推理、完整生成管线、图像生成或编辑、真实 API、GPU 测速、峰值显存、量化质量、文字准确率、多图理解、像素保持、透明 alpha 或生产部署。`load_system_prompt`、`load_cases`、`resolve_image_paths`、`load_image`、`split_thinking`、`write_records`、`report_parse_failures` 等未列入本次执行路径；其源码描述不计入 21 项实测覆盖。

七个权重文件元数据合计 33,115,613,408 字节，约 30.841 GiB。原审核记录当时可用磁盘约 29.19 GiB，且未发现可用 NVIDIA 设备证据；没有下载完整权重，也没有由文件体积推出显存需求。元数据读取和小型配置校验不等于完整模型已就绪。

固定代码与模型许可为 **Qwen RESEARCH LICENSE AGREEMENT**，仅限研究或评估用途；商业用途需要另行取得商业许可。练习包保留完整协议与 NOTICE。推理框架的 Apache-2.0 不覆盖 Qwen 材料自己的条款。本页提供固定许可的阅读摘要，不代替独立商业授权判断。

原 PDF 为 ReportLab 直接生成的 11 页彩色指南，历史审核逐页查看渲染像素；HTML 只有结构核验，没有浏览器视觉验收。教学示意图和合成函数输入都不是模型生成图像。公开整理不扩大原学习验证范围。

## 最新公开知识库的实际读取范围

合并基于 GitHub `main` 固定快照 `da063bc9b39722bb5fc7345dadb2f42a59ddda4d`，对应树 `33c29723dfe90afe0b31debe4bd4b26082f346ff`。本次通过 GitHub 连接器完整读取并逐文件核对 blob SHA、UTF-8 字节数与 SHA-256：MOC、学习方法、仓库说明、两份模板、20 篇相关概念、7 篇相关项目笔记，共 32 份正文。

20 篇概念就是上方“已有知识怎样合并”中列出的全部概念；7 篇项目为 awesome_gpt_image_2、gpt_image_prompting、ollama、replicate-hype、google_colab_cli、metrik、easel。该树共有 304 篇概念与 102 篇项目笔记，其他 284 篇概念、95 篇项目笔记只做路径/标题层筛查，没有全文阅读；不能声称全库正文查重或其他设备、未发布内容已核对。

本次新增一篇项目笔记、向六篇已有概念追加案例，并更新 MOC；不新增概念、不改写历史累计计数，不覆盖先前 Easel、Colab 或 Metrik 的正文。早期知识稿保留当时的查重范围与提案性质，本页记录较新公开快照的合并决策。

## 六份配套学习材料

- [彩色 PDF 指南](../../qwen_image_2_1/delivery/qwen_image_2_1_guide.pdf)
- [HTML 指南](../../qwen_image_2_1/delivery/qwen_image_2_1_guide.html)
- [离线练习包](../../qwen_image_2_1/delivery/qwen_image_2_1_exercise.zip)
- [实验日志](../../qwen_image_2_1/delivery/qwen_image_2_1_experiment_log.md)
- [知识笔记](../../qwen_image_2_1/delivery/qwen_image_2_1_knowledge_notes.md)
- [审核日志](../../qwen_image_2_1/delivery/qwen_image_2_1_review_log.md)

返回 [[00-总览|知识库总览]]。

## 固定来源

- [官方代码 README](https://github.com/QwenLM/Qwen-Image-2.1/blob/6627d87c6433151463ec4b48b8945a24fcf16a35/README.md)、[提示改写器说明](https://github.com/QwenLM/Qwen-Image-2.1/blob/6627d87c6433151463ec4b48b8945a24fcf16a35/prompt_rewrite/README.md)、[核心接口源码](https://github.com/QwenLM/Qwen-Image-2.1/blob/6627d87c6433151463ec4b48b8945a24fcf16a35/prompt_rewrite/pe_core.py)
- [固定模型卡](https://huggingface.co/Qwen/Qwen-Image-2.1/blob/d26bb61231c349cf6b7896fa83353113880e1ba3/README.md)、[Transformer 配置](https://huggingface.co/Qwen/Qwen-Image-2.1/blob/d26bb61231c349cf6b7896fa83353113880e1ba3/transformer/config.json)、[VAE 配置](https://huggingface.co/Qwen/Qwen-Image-2.1/blob/d26bb61231c349cf6b7896fa83353113880e1ba3/vae/config.json)、[调度器配置](https://huggingface.co/Qwen/Qwen-Image-2.1/blob/d26bb61231c349cf6b7896fa83353113880e1ba3/scheduler/scheduler_config.json)
- [官方代码许可](https://github.com/QwenLM/Qwen-Image-2.1/blob/6627d87c6433151463ec4b48b8945a24fcf16a35/LICENSE)、[官方模型许可](https://huggingface.co/Qwen/Qwen-Image-2.1/blob/d26bb61231c349cf6b7896fa83353113880e1ba3/LICENSE)
- [此次读取的学习方法](https://github.com/Smashwinny/reminder_knowlege/blob/da063bc9b39722bb5fc7345dadb2f42a59ddda4d/.claude/skills/learn-project/SKILL.md)
