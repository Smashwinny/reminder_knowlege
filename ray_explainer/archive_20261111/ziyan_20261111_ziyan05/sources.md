# 第5项来源清单
读取日期：2026-11-11（Asia/Shanghai）。只处理公开资料；不含用户私密记录。

## 原帖与引用
- https://x.com/wangray/status/2110558713996275853 ，x MCP实读。发布时间2026-10-15 10:29:44（Asia/Shanghai）。
- https://x.com/wangray/status/2110343390911160489 ，同次MCP引用展开实读。发布时间2026-10-14 20:14:07（Asia/Shanghai）。
- https://t.co/FkzWTCsOGQ ，X原帖entities.expanded_url核验指向技能目录。摘录和未核验边界见research/x-post-reading.md。

## 一手技能仓库
https://github.com/imraywang/rayskills
main固定SHA：ca254f09a17e2e2c0aba7651c36688c322b1f2b2
技能固定路径：https://github.com/imraywang/rayskills/tree/ca254f09a17e2e2c0aba7651c36688c322b1f2b2/skills/ray-explainer
- skills/ray-explainer/SKILL.md：完整读取；路线、script、配音/校对、静帧和QA门禁。
- scripts/new_project.sh：真实运行；创建隔离目录。
- scripts/render.js：完整读取且真实执行sheet/stills/video。原版未改。
- assets/template/kit.js：本轮读取1–65及145–234行（确定性绘制、at回退、renderFrame）；没有声称全文逐行审计，原版未改。
- assets/template/overlay.js：本轮读取1–100行（字幕时间与回退）；其余随渲染执行，不声称全部逐行审计。
- assets/template/video.html、script.template.json：入口和默认值。
- scripts/qa_video.py与review.py：完整读取并实际用于QA；review_page.py作为依赖实际执行、未逐行全文复读。review.py的from_timeline把首句开始当切点。
- scripts/storyboard.py：真实运行；预计时长是估计，不是12秒fixture实测长度。
- scripts/test_hf_template.py、test_hf_anchors.py，assets/hf-template/build.py、make_beats.py、host_build.py：上游离线回归测试实际运行。测试自带合成timeline与占位文件，不证明数字人或语音生成已完成。
- references/qa.md：本轮完整读取；其余参考已存档，不把存在文件等同于本轮全文审读。未调用发布、配音或外部API入口。
- scripts/check_setup.sh：只读不执行；会读本机配置和探测API，本任务不索要key、不查用户配置。

固定文件链接格式：
https://github.com/imraywang/rayskills/blob/ca254f09a17e2e2c0aba7651c36688c322b1f2b2/skills/ray-explainer/scripts/render.js
https://github.com/imraywang/rayskills/blob/ca254f09a17e2e2c0aba7651c36688c322b1f2b2/skills/ray-explainer/scripts/qa_video.py

许可：根LICENSE为CC BY-NC 4.0（作者imraywang），本任务非商业学习；保留署名与修改说明。huashu子组件另有MIT及字体许可，不可把整个rayskills说成MIT。原始快照不改，worker新增的fixture脚本、文案、timeline、指南另列，未使用Ray头像/复刻声音。

## 查重与旧风格
https://github.com/Smashwinny/reminder_knowlege
沿用本批已读vault/00-总览.md的固定main快照，并复读相关笔记；基线SHA：a8674777e18302b8804b137212b1396cbfe5a747（本批保存基线，不声称最终打包时main未变）。
相关已读并复用同SHA快照：vault/概念/React逐帧视频渲染.md、vault/项目笔记/ai-video-pipeline.md、vault/项目笔记/huashu_art_motion.md、vault/概念/动效描述词表.md；旧HTML样式参照ai-video-pipeline/AI视频流水线-小白指南.html。
没有rayskills/ray-explainer同名成果；已有确定性、TTS、动画词表不再新建重复概念。

## 运行环境
Node v24.22.1，npm 11.21.1；Linux Chrome=/usr/bin/google-chrome；ffmpeg/ffprobe系统已安装。
puppeteer-core实装固定25.17.0（上游check_setup.sh固定23.11.1，本次不用它安装）；锁文件保留integrity。原版允许CHROME和RAY_EXPLAINER_DEPS环境参数，未改变安全设置。
WeasyPrint使用第4项已安装的隔离70.0环境，生成真实A4 PDF；PDF渲染不需要任何付费API。

## 最终核验与修正
- 2026-11-11 Asia/Shanghai，按两个精确post ID重新调用X公共读取，返回ID及引用已核对；source-post.json为正确原样JSON。旧同名文件实为其他帖子，已隔离history/source-post-mislabeled.json，绝不作为证据或放进轻量包。
- research/resume/source-blob-check.txt：64个保存上游文件的Git blob SHA1与固定SHA递归tree逐一一致（不意味着审读64个文件全部内容）。
- huashu/LICENSE原快照缺失，本轮从上述固定SHA的公开raw路径实读并补齐MIT文本；字体许可清单保留。
- PDF实际12页A4，所有字体均为嵌入子集（pdffonts的sub=yes），无整套字体文件；HTML仅3张300px JPEG小图，SVG内联。
- PDF逐页PNG及抽帧原证据保留云端，轻量包不携带大PNG或视频。
