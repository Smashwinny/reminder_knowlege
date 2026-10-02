---
tags: [项目]
类别: 知识学习类（方法论拆解）
上游仓库: 无（游戏本体未开源；paperroute.lol 为打包产物）
完成日期: 2026-10-03
---

# paperroute

**这是什么**（一句话）：独立开发者 Emm Tee（@BuiltBySketch）用 GPT-5.6 Astra 做的浏览器 3D 送报游戏 PaperRoute，其价值不在游戏本身，而在**公开的 69 节点开发日志**（paperroute.lol/devlog）——一份"多模型分工把 AI Demo 磨成成品"的方法论标本；AYi 推文（2099090127452524615）做了拆解。

**它给我什么能力**：一套可复制的 AI 施工流水线——按任务类型路由生产者、机制/资产双泳道隔离、Headless 批产资产+质检门、帧级证据反馈、P0 基线先行、checkpoint 三件套交接。

**引入的概念**：
- [[机制流与资产流隔离]]（新）
- [[混合模型分工流水线]]（新）
- [[证据优先质检ProofOverClaims]]（补强：证据要可定位到帧，形容词反馈实测 19.5% vs 帧级 100%）

**实验记录**（exercise\，全部真跑通）：
- E1 `house_factory.py` + `glb_gate.py`：纯 Python 手写 GLB 二进制批产 4 户型族×3 变体=12 栋（1208~1216 bytes），质检门校验魔数/版本/块长/JSON/POSITION/索引 **12/12 PASS**——复刻"AI 写脚本 Headless 批产建筑 GLB"（本机无 Blender，模式同构）
- E2 `task_router.py`：12 条 devlog 真实任务规则路由，与作者实际选择**一致率 12/12**，成本系数 12.00→6.90（1.7x）
- E3 `frame_review_loop.py`：24 帧动画第 3 帧注入帽子偏移缺陷，形容词反馈修复率 **19.5%** vs 帧索引反馈 **100%**（200 轮，5.1x）

**关键一手数据**（devlog 统计面板）：1.56B Token（26.2M 输入/6.0M 输出/**1.53B 缓存=98%**）、API 估值 $2,175、39h 追踪覆盖（25.2h 人+13.8h 纯 agent，实测窗口 5.1:10.4）、90 commits、11 活跃天、769,390 行变更/4,458 文件；首个 commit="P0 baseline: PRD, engineering standards, architecture contract"（无可运行应用）；资产管线脚本入 ArtSource/；每 checkpoint 带正/侧/后转面图+SHA-256。

**坑与结论**：①推文口述与 devlog 互证时注意口径差（推文"四天 15.6 亿"实为 7/1–9/12 统计面板 1.56B；"39 工时"=追踪覆盖）。②游戏未开源，GitHub 搜 paperroute/builtbysketch 无作者仓库，判学习类的依据是**方法论具体可复现 + devlog 一手翔实**（参照 WikiSkill 先例）。③X 长文（article/2097705267689562112）需登录读不到，以推文全文+devlog 为准。

**后续可深入的方向**：装 Blender 真跑一次 headless 批产（`blender -b -P script.py`）；把 E2 的规则路由升级为小模型语义路由；Three.js 加载自制 GLB 拼一条街（衔接 [[Three.js与场景图]]）。
