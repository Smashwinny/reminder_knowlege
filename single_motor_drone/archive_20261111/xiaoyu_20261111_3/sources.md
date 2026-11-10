# 来源清单 · 03-single-motor-drone

时间一律给出 Asia/Shanghai（UTC+8）。带 Z 或显式偏移的时间已换算。

## 查重

| 项 | 值 |
| --- | --- |
| 仓库 | https://github.com/Smashwinny/reminder_knowlege |
| SHA | `a8674777e18302b8804b137212b1396cbfe5a747` |
| 提交时间 | 2026-11-04 17:42:58 Asia/Shanghai |
| 文件 | `vault/00-总览.md`（本地副本 `sources/reminder_knowlege__vault__00-总览.md`） |
| 结论 | 无 Joshua Bird / 单电机铰链桨 / Paulos 条目；仅有无关的 fly-brain-drone |

## 原帖（实读）

| 项 | 值 |
| --- | --- |
| 清单 URL | https://x.com/i/status/2113707112736145852 |
| 规范 URL | https://x.com/Moath_Abuaysha/status/2113707112736145852 |
| 作者 | @Moath_Abuaysha（user id 258682322） |
| 创建 | 2026-10-24 03:00:21 Asia/Shanghai |
| 读取 | X 公开工具 `get_posts_by_id`，2026-11-11 约 01:08 Asia/Shanghai；`note_tweet` 已展开 |
| 指标（读取时） | 14182 展示 / 114 赞 / 8 转帖 / 0 回复 / 86 书签 |
| 正文备份 | `sources/original-post.md` |

嵌入视频源帖：

| 项 | 值 |
| --- | --- |
| URL | https://x.com/IlirAliu_/status/2113175022877761659 |
| 作者 | @IlirAliu_ |
| 创建 | 2026-10-22 15:46:01 Asia/Shanghai |
| 时长 | 192833 ms（约 193 s），854×640 |
| 指标（读取时） | 104439 展示 / 2826 赞 / 365 转帖 |
| 指向 | https://github.com/jyjblrd/single-propeller-drone 与 https://youtu.be/Ndftcft6XhU |

完整视频未打进 delivery.zip（轻量要求）。YouTube 官方英文字幕未能下载（timedtext 空、yt-dlp 429）。

## 作者一手仓库与视频

| 项 | 值 |
| --- | --- |
| 飞机仓库 | https://github.com/jyjblrd/single-propeller-drone |
| 描述 | Under-actuated drone with only one motor |
| 默认分支 / SHA | `main` / `efc9176bfc83777b870b967c1f62a686c099be2c` |
| 提交时间 | 2026-10-11 06:21:51 Asia/Shanghai（「Link ArduPilot and moteus forks from README」） |
| 创建 / push | 创建 2026-10-10 22:14:38Z；push 2026-10-10 22:21:52Z |
| 许可 | API 记录为 None（README 未声明许可证，复刻前要自行确认） |
| 内容 | README、body/prop plate/prop v1 v2 的 f3d/f3z/STEP、media 图 |
| YouTube | https://www.youtube.com/watch?v=Ndftcft6XhU 「I Built a Drone With Only One Motor」，频道 Joshua Bird，发布 2026-10-17 21:00:33 Asia/Shanghai（源时区 −07:00），时长 564 s |
| 视频说明章节 | 00:00 Intro；00:36 How it steers；01:29 Switching to moteus；02:04 Fixing timing；02:37 New hub design；04:04 First test flight；05:23 Poor man's high-speed camera；06:53 Test stand；08:22 It works |

## 固件 fork（钉住 SHA）

| 仓库 | SHA | 提交时间（Asia/Shanghai） | 要点 |
| --- | --- | --- | --- |
| https://github.com/jyjblrd/moteus （fork of mjbots/moteus） | `704a0dd9f30a3704e8915a82c1631301fdbff9bd` | 2026-10-17 06:27:17 | MCOUT 收包；`servo.cyclic` 在 PWM 频率按编码器角度计算正弦力矩；指南明确忽略 yaw 混控。许可 Apache-2.0 |
| https://github.com/jyjblrd/ardupilot （fork of ArduPilot/ardupilot） | `455b266cc2a73505eb98c56a8049fa6a4d50f9bf` | 2026-10-17 06:27:15 | `AP_MotorControlOutput`（84 字节、魔数 0xC04D、最高 400 Hz、921600 baud）、`AP_IRBeaconYaw`、`MCOUT_PASS` 模式 |

文档冲突：moteus 指南 `SERIALx_PROTOCOL=50`，ArduPilot README `=51`。本地副本在 `sources/firmware/`。

## 论文

| 文献 | 状态 | 说明 |
| --- | --- | --- |
| J. Paulos, M. Yim, “An Underactuated Propeller for Attitude Control in Micro Air Vehicles,” IROS 2013, pp. 1374–1379 | 全文已读 | 本地 `sources/paulos-iros-2013.pdf`（来自 vigir.missouri.edu 会议光盘镜像，%PDF-1.5，1,730,051 字节）及 `paulos-iros-2013.txt`。38.6 cm 桨、约 1200 RPM / 1 N、30 N·mm、358 g 共轴双电机、12 位磁编码器、氙灯频闪 |
| J. Paulos, M. Yim, “Cyclic Blade Pitch Control Without a Swashplate for Small Helicopters,” JGCD 41(3):689–700, 2018, doi:10.2514/1.G002683 | PDF 受阻（modlab 429） | 使用站点公开索引到的摘要/结论：斜置滞后-变距铰链 + 挥舞铰链，台架最小周期变距约 ±7° |
| J. Paulos, M. Yim, “Scalability of Cyclic Control without Blade Pitch Actuators,” AIAA 2018 | PDF 受阻（modlab 429） | 10 cm 与 1 m 桨的尺度讨论，未当作已读全文 |
| HKU PULSAR, *Science Robotics* 2023, doi:10.1126/scirobotics.ade4538 | 未付费下载全文 | 桨径 37.6 cm 引自 HKU 报道页；自转机体，架构与 Bird 不同。面积比 6.087 待用 PDF 再核直径 |

## 二级报道（只用来交叉核对，不替代一手）

- DroneXL，2026-10-20：https://dronexl.co/2026/10/20/joshua-bird-single-motor-drone-hinged-propeller/（160 Hz、TPU 开裂、红外信标、moteus 约 $94）
- Tom's Hardware，2026-10-19：sub-0.2 ms 固件
- Hackster，Nick Bild：单枢轴、PPA-CF、配重、防扭鳍
- Hackaday，Maya Posch，2026-10-17

作者 X 账号 `from:jyjblrd` 检索无结果，未把第三方转述当成作者原帖。
