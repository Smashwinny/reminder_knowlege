# 知识入库提案 · muse_gadget_sdk

- 任务：92100bf6-10ff-4494-9625-4538006a1739
- worker：kimi-pool-20261007-w1（2026-10-07）
- 查重范围：`vault/概念/`、`vault/项目笔记/`、队列表

## 查重结果

- vault 无 Meta Muse 硬件 SDK 条目；`vault/项目笔记/openmuse.md` 是 CopilotKit/OpenMuse 任务引擎（任务 d57e48ae 已学），**同名异质**，需防混淆（已在指南 Q8 和本笔记写明）。
- 队列内 Muse 产品家族条目（muse_tutorial_index、muse_tailscale、awesome-muse-connectors 等，dot-cloud 过期租约）是不同组件，不重复；建议协调者确认这些条目的 owner 状态，未来合并时互链。
- 无同义概念：Noise 协议、BLE 配对、IoT 隧道均无既有笔记。

## 提案 1：新建项目笔记（worker 已按裁定直接新建）

`vault/项目笔记/muse_gadget_sdk.md` —— 已写入：定位、两 SDK 结构、连接架构（BLE 配对→Noise 隧道→云）、43 技能目录意义、132 测试实测、与 OpenMuse 的区分、门槛清单。

## 提案 2：新建概念（请协调者终审合并，2 条）

**① `vault/概念/硬件AI分工范式.md`**
一句话：便宜 MCU（$3 ESP32）只做感知/显示/执行 I/O，AI 推理全在云端——设备智能化不需要设备算力。
要点：设备=外设+加密通道；门槛从"算力"变成"连接与安全"（配对、隧道、OTA）；断网即退化的边界；隐私模型=数据过云。反模式：在 MCU 上硬塞推理、忽视配对中间人风险。
链接：`[[项目笔记/muse_gadget_sdk]]`、`[[本地推理引擎]]`（对照：什么时候该把推理放回本地）。

**② `vault/概念/设备技能即提示词.md`**
一句话：给 AI 的每台设备一份 SKILL.md 说明书（识别特征/前置条件/操作规则/安全红线），AI 就获得操作该设备的能力——设备生态扩展从"写驱动"变成"写文档"。
要点：43 份 gadget SKILL.md 实例；规则化红线（音频-only 不选视频行为、用当前服务端点不用记忆地址）= 提示词护栏；与 [[AgentSkills技能包]] 同思想跨领域复用。
链接：`[[AgentSkills技能包]]`、`[[护栏模式Guardrails]]`、`[[项目笔记/muse_gadget_sdk]]`。

## 总览/索引更新

请协调者在 `vault/00-总览.md` 项目清单补一行 muse_gadget_sdk（worker 不动总览）。
