# 2026-11-11 机器人学习成果归档

九个 Grok 机器人均已停止学习；本轮只收集既有成果、查重整理及归档发布。包含本地 claude_kimi 已经完成的修订；此前已发布的 Ultra-Water 继续使用既有版本。

本索引覆盖 **78 条产出记录、78 个不同来源、76 个项目目录**。这些数量表示收齐和整理的材料，不表示新完成了同等数量的完整学习。

## 阅读入口

| 机器人 | 学习主题 | 本次归档状态 | 材料 |
|---|---|---|---|
| 陈娇 | 把设备交互改成自己的样子 | 待验证（硬件或真实集成未验证） | [打开](../esp32_device_customization/archive_20261111/README.md) |
| 陈娇 | 浏览器学 Arduino：从演示到可检验的模型 | 待验证（硬件或真实集成未验证） | [打开](../arduino_browser_simulation/archive_20261111/README.md) |
| 陈娇 | 四个ESP32语音项目怎样分层 | 待验证（硬件或真实集成未验证） | [打开](../esp32_voice_projects/archive_20261111/README.md) |
| 陈娇 | ESP32选型先看项目契约 | 待验证（硬件或真实集成未验证） | [打开](../esp32_board_selection/archive_20261111/README.md) |
| 陈娇 | 圆屏Grok终端：把回执与回答分开 | 待验证（硬件或真实集成未验证） | [打开](../grok_round_display/archive_20261111/README.md) |
| 陈娇 | AI辅助硬件入门：把验收写进每一步 | 待验证（硬件或真实集成未验证） | [打开](../ai_hardware_onboarding/archive_20261111/README.md) |
| 陈娇 | Ivy AI：让大工作集轮流用内存 | 待验证（硬件或真实集成未验证） | [打开](../ivy_ai/archive_20261111/README.md) |
| 陈娇 | 一个域名背后的 Cloudflare 分层 | 待验证（离线实验材料） | [打开](../cloudflare_email_routing/archive_20261111/README.md) |
| 陈娇 | 小智硬件：规格、音频与内存预算 | 待验证（离线实验材料） | [打开](../xiaozhi_hardware_budget/archive_20261111/README.md) |
| 陈娇 | 内容流水线：幂等账本与离线字幕 | 待验证（离线实验材料） | [打开](../ai-video-pipeline/archive_20261111/README.md) |
| 陈娇 | 本地模型接入：接口兼容不等于无限额度 | 待验证（离线实验材料） | [打开](../local_model_api_contract/archive_20261111/README.md) |
| 陈娇 | X舆情模板：去重、缺失指标与数据边界 | 待验证（离线实验材料） | [打开](../x_sentiment_workflow/archive_20261111/README.md) |
| 陈娇 | map-motion：镜头表、坐标与可复现几何 | 待验证（离线实验材料） | [打开](../map_motion/archive_20261111/README.md) |
| 陈娇 | Pages与KV通用概念：不复现代理部分 | 受阻（仅通用Pages/KV离线实验） | [打开](../cloudflare_pages_kv/archive_20261111/README.md) |
| 陈娇 | 把工资焦虑框架改成可检验的能力盘点 | 待验证（离线实验材料） | [打开](../career_capability_inventory/archive_20261111/README.md) |
| 陈娇 | Agent 不是员工人设，而是可撤销授权的岗位 | 待验证（离线实验材料） | [打开](../agent_authorization_roles/archive_20261111/README.md) |
| 陈娇 | 9.9 到 29.9 的价差：先算亏损，再谈复制 | 待验证（离线实验材料） | [打开](../small_product_unit_economics/archive_20261111/README.md) |
| 陈娇 | 涨粉复盘：把成功故事改写成可检验假设 | 待验证（离线实验材料） | [打开](../creator_growth_experiments/archive_20261111/README.md) |
| 陈娇 | 七个 AI 信息入口：发现、原文与评测分工 | 待验证（离线实验材料） | [打开](../ai_information_sources/archive_20261111/README.md) |
| 陈娇 | Magpie 网关：协议统一不等于权限统一 | 待验证（离线实验材料） | [打开](../magpie_gateway/archive_20261111/README.md) |
| 陈娇 | 云端 Agent 上手：提示词、权限、验收分别写 | 待验证（离线实验材料） | [打开](../muse_agent_onboarding/archive_20261111/README.md) |
| 陈娇 | Pi 五类插件：选能力，不按下载量闭眼装 | 待验证（离线实验材料） | [打开](../pi_plugin_selection/archive_20261111/README.md) |
| 陈娇 | Mesh Avatar Studio：一张图到分层网格底稿 | 待验证（离线实验材料） | [打开](../mesh_avatar_studio/archive_20261111/README.md) |
| 马老师 | Pi-Purge 提示词“组合器”，不是权限开关 | 部分完成，待验证 | [打开](../pi_purge/archive_20261111/README.md) |
| 马老师 | Pi 不是一个包  但你的版本只有一个 | 离线/组件实验已交付，真实集成待验证 | [打开](../pi_architecture/archive_20261111/README.md) |
| 马老师 | 57个插件候选 先确认身份，再量成本 | 部分完成，待验证 | [打开](../dsh_plugin_catalog/archive_20261111/README.md) |
| 马老师 | 不是装满插件  而是补上一个痛点 | 离线/组件实验已交付，真实集成待验证 | [打开](../dsh_plugin_selection/archive_20261111/README.md) |
| 马老师 | Pi Durable 断了如何接上？ | 离线/组件实验已交付，真实集成待验证 | [打开](../pi_durable/archive_20261111/README.md) |
| 马老师 | magpie 本地网关 学转接与验证，不碰订阅反代 | 离线/组件实验已交付，真实集成待验证 | [打开](../magpie_gateway/archive_20261111/README.md) |
| 马老师 | 配置能恢复， 身份不要进备份 | 部分完成，待验证 | [打开](../bot_config_backup/archive_20261111/README.md) |
| 小钰 | LingBot-Map 增量学习 | 待验证（模拟/组件实验，真实硬件或服务未验证） | [打开](../lingbot_map/archive_20261111/README.md) |
| 小钰 | 盲装配与 mjfit | 待验证（模拟/组件实验，真实硬件或服务未验证） | [打开](../blind_assembly_mjfit/archive_20261111/README.md) |
| 小钰 | 单电机铰链桨无人机 | 待验证（模拟/组件实验，真实硬件或服务未验证） | [打开](../single_motor_drone/archive_20261111/README.md) |
| 小钰 | 开源机器人筛选 | 待验证（模拟/组件实验，真实硬件或服务未验证） | [打开](../open_robot_selection/archive_20261111/README.md) |
| 小钰 | ESP32、家庭网络与 Tailscale | 待验证（模拟/组件实验，真实硬件或服务未验证） | [打开](../esp32_tailscale/archive_20261111/README.md) |
| 小钰 | ESP32 模拟器选型 | 待验证（模拟/组件实验，真实硬件或服务未验证） | [打开](../esp32_emulators/archive_20261111/README.md) |
| 静静多闹闹 | 游戏分发渠道与准入证据 | 待验证 | [打开](../game_distribution_channels/archive_20261111/README.md) |
| 静静多闹闹 | 技术分析术语与无前视偏差合成回测 | 限定实验完成 | [打开](../technical_analysis_evidence/archive_20261111/README.md) |
| 静静多闹闹 | 照片转拼豆图纸（来源受阻记录） | 受阻 | [打开](../bead_pattern/archive_20261111/README.md) |
| 静静多闹闹 | 海报提示词商品化与样张实验 | 沿用云端旧成果 | [打开](../poster_prompt_service/archive_20261111/README.md) |
| 静静多闹闹 | 公众号选题与排版工具链 | 待验证 | [打开](../wechat_content_toolchain/archive_20261111/README.md) |
| 静静多闹闹 | 适合代理协作的仓库与合并闸门 | 待验证 | [打开](../grok_bot_method/archive_20261111/README.md) |
| 静静多闹闹 | 画框突破效果与遮挡对照 | 待验证 | [打开](../seedance_framebreak_prompt/archive_20261111/README.md) |
| 静静多闹闹 | X原创奖励条款与合成稿件检查 | 待验证 | [打开](../x_original_content_rewards/archive_20261111/README.md) |
| 静静多闹闹 | 螺旋动画生成器（叫停前资料） | 未完成 | [打开](../spiral_generator/archive_20261111/README.md) |
| 悠咪 | iOS语音入口与Vocal Shortcuts | 待验证 | [打开](../grok_ios_voice_entry/archive_20261111/README.md) |
| 悠咪 | LearnHarness计划树与教学结构 | 待验证 | [打开](../learnharness/archive_20261111/README.md) |
| 悠咪 | CS146S 2026现代软件开发课程 | 待验证 | [打开](../cs146s_2026/archive_20261111/README.md) |
| 悠咪 | 198个账号筛选与信息质量边界 | 待验证 | [打开](../ai_source_account_filter/archive_20261111/README.md) |
| 悠咪 | 单主题第二大脑的三角色边界 | 待验证 | [打开](../karpathy_second_brain/archive_20261111/README.md) |
| 悠咪 | Agent可信工作的结构化验证 | 待验证 | [打开](../agent_trust_verification/archive_20261111/README.md) |
| 悠咪 | 七类AI信源与可追溯选型 | 待验证 | [打开](../ai_information_sources/archive_20261111/README.md) |
| 静静 | Muse 电话辅助：翻译、身份与授权 | 待验证：仅离线授权/交接状态机 | [打开](../muse_phone_translation/archive_20261111/README.md) |
| 静静 | ESP32 小黄人：从单麦到声源转向 | 待验证：双麦数值模型 | [打开](../esp32_minion_sound_localization/archive_20261111/README.md) |
| 静静 | GCP 预算熔断：90%不是费用硬上限 | 待验证：原函数桩测试 | [打开](../gcp_billing_guard/archive_20261111/README.md) |
| 静静 | Anatomy Skill 与原理讲解形式 | 待验证：TCP教学及官方示例子集 | [打开](../anatomy_skill/archive_20261111/README.md) |
| 静静 | Dots 自动换题材与程序化低模试验 | 待验证：原创程序化低模 | [打开](../dots_lowpoly_exploration/archive_20261111/README.md) |
| 静静 | yigezi：一个字的形音义族时间轴 | 待验证：数据查询与占位演变 | [打开](../yigezi/archive_20261111/README.md) |
| 静静 | 先卖再开发，别把自述当成单位经济 | 待验证：公开自述与合成单位经济 | [打开](../founder_unit_economics/archive_20261111/README.md) |
| 静静 | 出海工具按阶段选，不要一次买齐 56 个 | 待验证：目录检查与HTTP记录 | [打开](../overseas_tool_selection/archive_20261111/README.md) |
| 徐佳 | 一张图的惊艳之后， 怎样检验机械动画？ | 待验证：CPU/GLB组件实验 | [打开](../spider_turret_3d/archive_20261111/README.md) |
| 徐佳 | 八技能做游戏 真正难的是交接 | 待验证：原创JS实验；PDF缺失 | [打开](../codex_game_skills/archive_20261111/README.md) |
| 徐佳 | 参照视频 → 代码动效 把时间变成输入 | 待验证：原创CPU音画实验；PDF缺失 | [打开](../reference_video_code_motion/archive_20261111/README.md) |
| 徐佳 | 个人作品集， 怎样从“好看”走向“可验收”？ | 待验证：原创网页Node/Chrome实验 | [打开](../personal_portfolio_site/archive_20261111/README.md) |
| 徐佳 | 十条游戏技能链接， 怎样变成可验证工作流？ | 待验证：原创游戏组件实验 | [打开](../wechat_minigame_skills/archive_20261111/README.md) |
| 徐佳 | AI改版剧情游戏， 怎样把惊艳变成证据？ | 待验证：原创叙事/WebGL方法实验 | [打开](../ai_3d_story_game/archive_20261111/README.md) |
| 徐佳 | 人形机器人： 从漂亮展台到可验证构建 | 受阻：GLB加载0/4，视觉未通过 | [打开](../bee_robot_showcase/archive_20261111/README.md) |
| 壮壮 | ELYTerminal 可爱的终端， 怎样认真验货？ | 待验证：Linux组件实验记录 | [打开](../elyterminal/archive_20261111/README.md) |
| 壮壮 | 两个入口， 不是两种能力 | 待验证：MCP mock与纯组件测试 | [打开](../lcu/archive_20261111/README.md) |
| 壮壮 | 先画清状态， 再让反例说话 | 待验证：有限合成模型已留日志 | [打开](../tla_state_machine/archive_20261111/README.md) |
| 壮壮 | 让任务看得见， 不让动画冒充事实 | 部分完成：用户叫停时研究笔记 | [打开](../agent_diorama/archive_20261111/README.md) |
| 紫嫣 | 身份、姿势、节拍 各管一件事 | 待验证：CPU节拍/时间线实验 | [打开](../ai_dance_beat_alignment/archive_20261111/README.md) |
| 紫嫣 | 换脸 MV 不靠运气 靠可追溯生产线 | 待验证：CPU与部分上游测试 | [打开](../recast_video_dgx/archive_20261111/README.md) |
| 紫嫣 | Item03 数字人场控：离线实证交付 | 待验证：离线队列/场控实验 | [打开](../ai_live_avatar/archive_20261111/README.md) |
| 紫嫣 | 把一句导演提示词 变成可验收短片 | 已有实验与本地修订候选；新PDF缺失 | [打开](../remotion_caption_lab/archive_20261111/README.md) |
| 紫嫣 | 从“起号推荐” 走到可验证执行层 | 待验证：原版Canvas样本；音频QA失败 | [打开](../ray_explainer/archive_20261111/README.md) |
| 紫嫣 | 文案不配音，也要有节奏证据 | 待验证：原创文案/BGM实验 | [打开](../text_bgm_motion/archive_20261111/README.md) |
| 紫嫣 | 先验证占位层，再连接数字人 | 待验证：占位人物/特效实验 | [打开](../avatar_fx_template/archive_20261111/README.md) |

## 查重与版本处理

- 以来源原帖、项目身份和文件 SHA256 交叉检查，复用既有项目目录；不同实验或修订保留来源关系。
- 同一项目压缩包和展开副本只选择一套；原始交付包完整保存在 F 盘的私有归档中。
- 静静第 7、8 项的不同版本各按一个项目汇总；Remotion 保留云端原版及本地 claude_kimi 修订的对应关系。
- 已发布的 [Ultra-Water](../ultra_water/) 不重复复制或计入本次产出记录。
- 第三方抓取全文、上游克隆、依赖缓存及内部运行信息不进入公开归档。

## 验证范围

归档检查覆盖文件完整性、来源对应、重复版本、公开文件范围、凭据形态及 PDF 可读性抽查。机器人日志中记录的实验只按其已声明范围保留；本轮未重新执行下载的练习，也未把离线模拟等同于真实硬件或外部服务成功。缺失 PDF、来源不可读、渲染失败和未启动的实验均保留各自限制。

知识提案随项目归档，尚未验证的断言不作为已验证概念覆盖现有知识库。Reminder 完成勾选、完整分析标签和历史完成纲要均未改变。

完整文件校验清单见 [manifest.json](manifest.json)，逐项机器可读目录见 [catalog.json](catalog.json)。
