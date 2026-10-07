# Qwen-Image-2.1 知识笔记

日期：2026-10-05 UTC。主题：普通物体、图标与一般图像模型工程；不包含特殊用途示例。

本文保留原学习的资料、接口实验与候选方案，并先说明本次公开整理已经准备好的知识合并范围。笔记存在不代表读者已经掌握。

## 本次公开整理的已准备合并

以公开知识库提交 da063bc9b39722bb5fc7345dadb2f42a59ddda4d 为基线，已经准备 8 份知识库文件的合并内容：给 6 个既有概念追加 Qwen 项目案例，新增 1 篇 [Qwen-Image-2.1 项目笔记](../../vault/项目笔记/qwen_image_2_1.md)，并以插入方式更新知识总览。没有新建概念条目，原概念正文保留。

六个追加案例的概念是 Agent输出协议契约、PromptAsCode提示词即代码、图像提示八要素、棋盘格假透明修复、开源验货三查、接缝与桩实现StubSeam。这里确认的是已准备并核对的合并内容，不提前声称远程发布已经完成。

以下编号章节与末尾实验补充保留原学习时的笔记和候选方案，供追溯判断依据；其中“候选”“建议”和旧版查重数量属于历史记录，当前采用的合并范围以上述 8 份文件和项目笔记为准。本次公开整理没有重新运行学习实验，原 21 项上游预期行为检查与独立的 6 项消费者策略示例继续分别记账。

## 1. 历史学习时的知识查重范围

- 扫描固定公开索引 394 条元数据，全文读取并核验 19 篇相关公开概念/项目笔记；其余 375 篇只有元数据检索，不能宣称全库全文已读
- 公开知识索引固定于 1f61909da967cea8bc68dbfaffc642a4331b3352；相关公开正文固定于 1043e9d6080bff7af9724162e2c44559fab63e40
- 上述范围只描述本次实际读取的公开快照，不是全库全文覆盖；笔记存在也不代表读者已经掌握

## 2. 优先复用的概念

1. [[量化与GGUF]]、[[本地推理引擎]]、[[ollama]]：只回顾权重表示与运行时的区分。旧语言模型的文件体积经验值、显存和首 token 时间不适用于本图像模型的资源估算；GGUF 格式存在也不保证某运行时已支持该模型
2. [[图像提示八要素]]、[[PromptAsCode提示词即代码]]、[[提示词模板]]：沿用需求结构化、槽位和版本化思想；新增本项目真实消息构建器、任务 profile 与解析器的接口案例。旧提示词 Lint 分数只是规则检查结果，没有证明出图质量相关性
3. [[修改与约束分离]]：沿用修改区、保留区和排除区的写法。例如只改杯子的颜色，同时保留构图和背景。文字约束不会自动形成像素级保护，也不是程序权限
4. [[棋盘格假透明修复]]：沿用“视觉像透明”与“实际有透明通道”分开检查。旧修复算法和精度不迁移为 Qwen 保证；输入预处理、输出通道与下游合成分别取证
5. [[Agent输出协议契约]]、[[代码管边界提示词管判断]]：已有严格 schema 门和强制边界的思路；本项目的 parse_ok 需按具体实现解释，不能因返回 JSON 就当成严格语义验证
6. [[接缝与桩实现StubSeam]]：外部模型调用和本地胶水代码应各自验证。直接给解析函数输入合成回答是 fixture 测试，不自动等于已经接通模型后端或端到端桩服务
7. [[证据状态机]]、[[证据优先质检ProofOverClaims]]、[[源码取证图]]：分别记录作者主张、静态代码、实际执行和未知项，固定 commit 与输入指纹，不把源码存在当作能力实测
8. [[开源验货三查]]、[[内容型开源与双许可]]：沿用代码、权重、素材分别查许可的方法。旧项目的许可和简化口号不适用于新项目；模型卡的标签也不能代替许可正文
9. [[replicate-hype]]：这是趋势聚合站的已有笔记，只因名字涉及 Replicate 不构成本图像模型部署的同义知识，避免误合并

## 3. 历史候选增量：解析成功、契约有效与任务正确分层

一句话定义：一段输出能被解析成字段、字段满足下游约束、结果符合用户意图，是三项不同判断，必须分别验证。

领域：模型应用工程、协议设计、可靠性测试。

本项目的静态源码例子：
- parse_answer 从后向前扫描完整花括号候选，寻找非空的 rewritten_prompt 字符串，也兼容旧拼写 rewrited_prompt
- wh_ratio 与 ratio_follow 会经字符串转换；该函数没有校验长宽比是否为允许值、引用的图片是否存在，也不证明改写后的意思符合输入
- t2i 不向输出保留 ratio_follow；edit 可以保留该字段，属于任务输出形状差异
- 没有可用对象时，把原回答保存在 positive_prompt 并令 parse_ok=false。原文还在不等于规范改写成功
- 可选 json_repair 的安装状态会改变近似 JSON 的可接受范围；复现实验应记录依赖状态，不能只说“同一个 Python 文件”

普通物体例子：一条声称画“蓝色杯子”的回答即使能提取 prompt，若 ratio 字段是任意字符串，或参考图索引越界，仍不能直接认定它能安全交给下游生成器。实际生成的杯子颜色是否正确，又是另一个需要图像验收的问题。

查重建议：优先增补 [[Agent输出协议契约]] 的“解析与语义验证分层”小节，并链接 [[代码管边界提示词管判断]]、[[证据优先质检ProofOverClaims]]；确认没有同义条目后再考虑独立成篇。

证据等级：上述是固定源码的静态观察；哪些分支已实跑，需与本次实验日志中的具体用例对应，不能把整段描述视作全覆盖测试。

来源：[pe_core.py](https://github.com/QwenLM/Qwen-Image-2.1/blob/6627d87c6433151463ec4b48b8945a24fcf16a35/prompt_rewrite/pe_core.py)

## 4. 历史候选增量：模型检查点与提示协议一起版本化

一句话定义：模型检查点、对应的系统提示、任务输入形状和采样配置共同构成可复现的调用条件；只固定权重名称不够。

领域：模型部署、可复现工程、配置管理。

固定 pe_core.py 为 t2i 与 edit 分别定义 profile，包含不同的 presence_penalty、token 预算和图片输入要求。load_system_prompt 优先采用明确指定的文件，否则寻找检查点目录中的 system_prompt.txt。这个查找规则能减少错配，却不验证提示文件与权重真正匹配，也不能保证用户覆盖的文件正确。

一个能讲清的实验差异：同一输入若换任务 profile，消息形状和字段意义可能变化。t2i 输入图片会被路径处理函数拒绝；edit 则要求至少一张图片。文件存在检查不等于图片已成功解码，也不等于格式完整或输入安全。

查重建议：与 [[提示词模板]]、[[PromptAsCode提示词即代码]] 相关但不完全同义。优先作为 Qwen 项目案例补充“配置整体固定”，同义核对后再决定独立概念。

来源：[任务核心](https://github.com/QwenLM/Qwen-Image-2.1/blob/6627d87c6433151463ec4b48b8945a24fcf16a35/prompt_rewrite/pe_core.py)、[改写器说明](https://github.com/QwenLM/Qwen-Image-2.1/blob/6627d87c6433151463ec4b48b8945a24fcf16a35/prompt_rewrite/README.md)

## 5. 项目案例：参考图顺序与输入通道是契约的一部分

一句话定义：参考图片的排列、编号和进入模型前的像素表示，会改变指令的实际含义；它们不是可随意丢弃的包装。

领域：多模态输入、图像编辑、接口工程。

build_messages 按输入顺序先放图片、再放用户文本。普通图标例子：第一张为杯子轮廓，第二张为调色板；交换两图就会改变“参考第一张形状、第二张颜色”的含义。顺序保留是接口行为，不能证明模型实际理解了角色分工。

load_image 会将输入转换为 RGB，并按像素上限缩小。这是提示改写器的源图预处理路径，不是 Qwen-Image 输出图像的通道证明；不能由这里推出图像生成器有无 RGBA 能力。某流程若依赖透明度，应明确 alpha 在哪里读取、丢弃或输出。

查重建议：把参考图角色分配补充进 [[图像提示八要素]]，把输入/输出透明度分层补充进 [[棋盘格假透明修复]]；不重复建立“参考图提示”和“假透明”同义条目。

来源：[pe_core.py](https://github.com/QwenLM/Qwen-Image-2.1/blob/6627d87c6433151463ec4b48b8945a24fcf16a35/prompt_rewrite/pe_core.py)

## 6. 历史项目笔记提案：Qwen-Image-2.1

本次关注图像模型的公开架构、一般用途与部署条件，以及独立提示改写器的可检查接口。上游宣称的生成/编辑能力、静态模块配置、离线接口函数执行和实际模型输出是不同证据层。

固定来源：
- 代码仓库 QwenLM/Qwen-Image-2.1：6627d87c6433151463ec4b48b8945a24fcf16a35
- 模型仓库 Qwen/Qwen-Image-2.1：d26bb61231c349cf6b7896fa83353113880e1ba3

与已有知识的主要关联：[[量化与GGUF]]、[[本地推理引擎]]、[[提示词模板]]、[[Agent输出协议契约]]、[[棋盘格假透明修复]]、[[证据优先质检ProofOverClaims]]。

本轮实际运行：Python 3.12.14，未修改的上游 pe_core.py，SHA-256 为 fd9732bbba71468fb24bd81de5c209f0db2941f01d1e556d52b5a6deba0f1fe5；21 项预期行为检查全部通过。调用范围是任务 profile、消息构建、回答解析与记录构建。json_repair 未安装；图像标记只是合成字符串，没有抓取或解码图片。

观察到的关键结果：任意比例字符串、edit 同时给出两个比例字段、缺失两个比例字段，以及不存在的 <image99> 引用都能产生 parse_ok=true；说明这不是完整的下游语义校验。无 JSON、截断 JSON、空提示，以及无 repair 时的尾逗号对象进入 fallback。带有多个可用对象时优先取靠后的对象。这里“通过”指源码行为符合预设观察结果，包括验证缺口，不能解读成不存在缺陷。

本轮离线实验的核心边界：输入与回答均明确标为合成数据，没有模型权重推理、真实提示改写、GPU 出图、付费 API、速度/显存测量或图像质量对比。输入文件/图片路径检查、系统提示读取和 RGB 预处理在本文属于源码观察，不属于上述 21 项实跑覆盖。

许可分层：固定版本官方模型与代码的许可为 Qwen RESEARCH LICENSE AGREEMENT，限定研究或评估用途；商业用途需要另行取得商业许可。练习包应保留完整协议和所需 NOTICE。相关框架的 Apache-2.0 许可不能代替模型/官方代码自己的许可。本说明是读取固定许可的边界摘要，不是商业使用授权。

许可来源：[官方代码许可](https://github.com/QwenLM/Qwen-Image-2.1/blob/6627d87c6433151463ec4b48b8945a24fcf16a35/LICENSE)、[官方模型许可](https://huggingface.co/Qwen/Qwen-Image-2.1/blob/d26bb61231c349cf6b7896fa83353113880e1ba3/LICENSE)

未验证事项：Qwen-Image 完整推理部署、生成效果、图像文字正确率、编辑内容保持、多图理解准确率、真正输出 alpha 的可用性、不同量化实现的质量与资源变化、具体硬件的吞吐和峰值显存。模型卡列出的配置不自动证明任意电脑都能运行。

普通用途的后续验证可以选择杯子图标、几何纹样、普通物体改色或多参考物体构图。未来真出图时需固定模型版本、完整参数、输入文件指纹和评价标准；先核对资源、必要许可与预算，再把实际图像和运行日志补到本项目，不能用本轮合成回答代替。

来源：[代码说明](https://github.com/QwenLM/Qwen-Image-2.1/blob/6627d87c6433151463ec4b48b8945a24fcf16a35/README.md)、[模型卡](https://huggingface.co/Qwen/Qwen-Image-2.1/blob/d26bb61231c349cf6b7896fa83353113880e1ba3/README.md)

## 7. 复用时的边界

把本项目作为已有提示词、契约、透明度和证据概念的具体案例；候选概念先做同义检索，再决定是否独立成篇。引用旧材料的方法不等于重新验证旧项目的外部结论，也不能把其他项目的测试数量、硬件成绩、政策或许可转给 Qwen。

复用时保留固定来源、实际命令、合成输入标识、原始输出、许可与未执行边界。合并内容应保留已有编辑；索引元数据没有命中，不能据此推断未读正文没有相关知识。

## 8. 实际全文读取的公开知识来源

以下清单只记录已读正文和指纹，不附原文。旧笔记中的历史服务事实、性能、产品命名和外部来源没有在本轮逐项复验。

1. [Agent输出协议契约](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/Agent%E8%BE%93%E5%87%BA%E5%8D%8F%E8%AE%AE%E5%A5%91%E7%BA%A6.md)
   UTF-8：1742 字节；SHA-256：85b2ef5207651ba4807bd3da205a45c72c1fe38a5cb8ce91a052f66dea5bba4e

2. [PromptAsCode提示词即代码](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/PromptAsCode%E6%8F%90%E7%A4%BA%E8%AF%8D%E5%8D%B3%E4%BB%A3%E7%A0%81.md)
   UTF-8：1971 字节；SHA-256：de8df816c830acb11ff89f89662f0468bbdb5ebbca67e4f07b6bf8ca94026d70

3. [awesome_gpt_image_2](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/awesome_gpt_image_2.md)
   UTF-8：2242 字节；SHA-256：f1e72ebd4437ef406afc437f00742394b4ea8425010cb2f0b8680ee63340e452

4. [gpt_image_prompting](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/gpt_image_prompting.md)
   UTF-8：5392 字节；SHA-256：ff9cd7c86487e45dc3467de0d55113c0a8285e48e9061c59f613b63e543edae6

5. [ollama](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/ollama.md)
   UTF-8：2619 字节；SHA-256：c8373b36ef5d662194afd08d21f0d8f05398ce198982be8ac904c0c67f48208c

6. [replicate-hype](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E9%A1%B9%E7%9B%AE%E7%AC%94%E8%AE%B0/replicate-hype.md)
   UTF-8：2276 字节；SHA-256：53caf8d9fb548de52235dabac238d7ee9dffe24ffe0289dca0e12071f4590543

7. [代码管边界提示词管判断](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E4%BB%A3%E7%A0%81%E7%AE%A1%E8%BE%B9%E7%95%8C%E6%8F%90%E7%A4%BA%E8%AF%8D%E7%AE%A1%E5%88%A4%E6%96%AD.md)
   UTF-8：1427 字节；SHA-256：82baf8f30c908b3ea424d15f82b6d3124e40b3c1b023961bfd0c8abd1eb8b86d

8. [修改与约束分离](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E4%BF%AE%E6%94%B9%E4%B8%8E%E7%BA%A6%E6%9D%9F%E5%88%86%E7%A6%BB.md)
   UTF-8：2625 字节；SHA-256：e4fcd8e5b32997c473240296081e74f1923cfbfa87cb0a4e5da3e37ea46d6494

9. [内容型开源与双许可](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%86%85%E5%AE%B9%E5%9E%8B%E5%BC%80%E6%BA%90%E4%B8%8E%E5%8F%8C%E8%AE%B8%E5%8F%AF.md)
   UTF-8：1994 字节；SHA-256：37a76743f06d6bc1248c21d08a7e459b3cf588df93fc59db0f1db77ee54c27b2

10. [图像提示八要素](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%9B%BE%E5%83%8F%E6%8F%90%E7%A4%BA%E5%85%AB%E8%A6%81%E7%B4%A0.md)
   UTF-8：2408 字节；SHA-256：652f097bd319294e764558409bd2975d10fc4d94e251d9afe203eeb7e5bf12d1

11. [开源验货三查](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E5%BC%80%E6%BA%90%E9%AA%8C%E8%B4%A7%E4%B8%89%E6%9F%A5.md)
   UTF-8：1815 字节；SHA-256：836585db83f85f393815551357aad9b894567c5e57bc7c4623e088040c50b0ce

12. [接缝与桩实现StubSeam](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%8E%A5%E7%BC%9D%E4%B8%8E%E6%A1%A9%E5%AE%9E%E7%8E%B0StubSeam.md)
   UTF-8：1752 字节；SHA-256：83decb2724ea3ac736e0f9c4c89e17e043504be4733162e6ee44d7988c976804

13. [提示词模板](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%8F%90%E7%A4%BA%E8%AF%8D%E6%A8%A1%E6%9D%BF.md)
   UTF-8：1147 字节；SHA-256：96f7b18a973e2f4d5fd2a86ea967011c6e12ced0ab50ce8029232bdf8098ea21

14. [本地推理引擎](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%9C%AC%E5%9C%B0%E6%8E%A8%E7%90%86%E5%BC%95%E6%93%8E.md)
   UTF-8：1212 字节；SHA-256：9e505aef5f9caa9ccab79a31c3096a337f691af11d4c9f6666d8d91c74b1212e

15. [棋盘格假透明修复](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%A3%8B%E7%9B%98%E6%A0%BC%E5%81%87%E9%80%8F%E6%98%8E%E4%BF%AE%E5%A4%8D.md)
   UTF-8：1752 字节；SHA-256：a8ad7a8842dfca4066b90cdcf0ff7af47d06cddc178f348e4d89fe831a8b6871

16. [源码取证图](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E6%BA%90%E7%A0%81%E5%8F%96%E8%AF%81%E5%9B%BE.md)
   UTF-8：1529 字节；SHA-256：6ee5e93541998ff102231366c65c1d1b8fa7fbde5825cbb82fdd6d115124c018

17. [证据优先质检ProofOverClaims](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%AF%81%E6%8D%AE%E4%BC%98%E5%85%88%E8%B4%A8%E6%A3%80ProofOverClaims.md)
   UTF-8：3593 字节；SHA-256：c54ea2f3bcfe830556942d04c502ba84472a7382c45b76dd07401861e44c2fac

18. [证据状态机](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E8%AF%81%E6%8D%AE%E7%8A%B6%E6%80%81%E6%9C%BA.md)
   UTF-8：2488 字节；SHA-256：4ac12b197891357591ebd092a9120bd67fa6fa1a09a407ed9c0fea3bc9b97328

19. [量化与GGUF](https://raw.githubusercontent.com/Smashwinny/reminder_knowlege/1043e9d6080bff7af9724162e2c44559fab63e40/vault/%E6%A6%82%E5%BF%B5/%E9%87%8F%E5%8C%96%E4%B8%8EGGUF.md)
   UTF-8：1205 字节；SHA-256：2b05b14f3b1512872f4a588179d3812d6df09e8ba16b3bbb2de44eb9a1c160d1

## 追加的可复现消费者策略实验

完整上游实测仍为 21/21。练习包另含独立编写的 inspect_results.py，其 local_policy 只属于本练习的下游消费者策略，没有修改 pe_core.py，也不代表官方完整 schema。它要求文生图选择规定比例；编辑恰好选择 wh_ratio 或 ratio_follow；引用落在假定的两张图范围内。

从全新解压的 ZIP 执行五个命令，全部退出码为 0。第 5 步的 6 个样本中，2 个正常样本接受、4 个上游可解析但不满足本策略的样本拒绝，6/6 符合预期。该实验是 [[Agent输出协议契约]] 的具体消费者校验例子，不是图像质量或真实改写能力测试。命令、时间和逐例输出见实验日志。

模型架构增量可加入项目笔记：官方 README 的单流 32 层 DiT 与混合粒度注意力；模型配置的 64 通道、空间缩放 16 的四通道 VAE；causal_condition 与条件前缀 KV 复用。上述为官方说明或静态配置核对，不是此次纯函数实测。7B 指视觉生成组件，另有官方称为 8B 的文本编码器和 VAE。完整权重元数据约 30.841 GiB，大于本次约 29.19 GiB 可用磁盘；没有由此推出显存需求。
