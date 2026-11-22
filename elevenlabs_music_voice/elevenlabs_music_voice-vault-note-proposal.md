# ElevenLabs 配乐与音色 知识入库提案（vault-note-proposal）

> 提案性质：供协调者查重合并用，worker 不直写 vault。
> 关联任务：27853f54-7fef-4326-92b8-9554d76f7cef ｜ 项目目录：F:\reminder\elevenlabs_music_voice

## 一、新概念笔记（建议新建，vault 查重未见同名）

### 1. 条件生成 vs 自动成片
- 一句话定义：AI 接口"给视频生成配乐"输出的是音乐轨（条件生成），混音、响度、对白避让仍是剪辑环节责任——接口存在≠流水线自动完成。
- 领域：AI / 音视频
- 已有概念关联：[[证据优先质检ProofOverClaims]]；[[混合模型分工流水线]]（工序责任边界）
- 来源项目：elevenlabs_music_voice（video-to-music 契约直读）

### 2. 声音克隆两路线（IVC/PVC）
- 一句话定义：IVC=推理时挂参考音频不动权重（秒级、素材 1-5 分钟）；PVC=训练专属模型（3-6 小时、素材 ≥30 分钟、需声纹验证）——按素材量与时效选型。
- 领域：AI / 语音
- 已有概念关联：[[级联语音管线]]；[[LoRA低秩适配微调]]（不动权重 vs 训练的小模型版同构）
- 来源项目：elevenlabs_music_voice（官方文档+检索核实）

### 3. 混音响度验收
- 一句话定义：人声与 BGM 的响度差用 RMS dBFS 客观测量，人声领先 6~10dB 为清晰区；<4dB 浑浊、>15dB 配乐失存——音频验收机检化。
- 领域：AI / 音视频
- 已有概念关联：[[证据优先质检ProofOverClaims]]（音频版）；[[规格书先行SpecDriven]]（分贝差当合同）
- 来源项目：elevenlabs_music_voice（合成样本实测 -22.0/-26.1 dBFS，三档混音）

## 二、项目笔记（建议新建 vault\项目笔记\elevenlabs_music_voice.md）
- 项目是什么：X 帖《面试鸭》宣传片流程（Claude 编排 + ElevenLabs 配乐 + 克隆声）的接口级解读
- 带来的概念：[[条件生成 vs 自动成片]]、[[声音克隆两路线（IVC/PVC）]]、[[混音响度验收]]
- 实验做了什么：video-to-music 契约直读、401 只读探针、IVC/PVC 对比核实、纯 Python 合成+混音 RMS 实验
- 坑与结论：高档音质格式要 Creator/Pro+；克隆需声音权利与同意；原帖效果无凭据

## 三、合并建议（不新建，增补已有笔记）
- [[级联语音管线]]：增补 IVC/PVC 选型维度
- [[证据优先质检ProofOverClaims]]：增补 RMS 分贝差验收实例

## 四、MOC 更新建议
"AI / 视频"或"音乐技术"分区增补三条新概念；项目索引加 elevenlabs_music_voice。
