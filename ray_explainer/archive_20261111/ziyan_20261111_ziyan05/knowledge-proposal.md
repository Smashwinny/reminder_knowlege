---
tags: [项目, 候选增量, 视频, 失败传播]
日期: 2026-11-11 Asia/Shanghai
上游: https://github.com/imraywang/rayskills
上游SHA: ca254f09a17e2e2c0aba7651c36688c322b1f2b2
---
# ray-explainer：将作者工作流拆成可离线验证层

## 查重
本次vault main a8674777e18302b8804b137212b1396cbfe5a747。已存在[[React逐帧视频渲染]]、[[动效描述词表]]、[[项目笔记/ai-video-pipeline]]和[[项目笔记/huashu_art_motion]]；本提案不复制这些概念定义，未合入共享vault。

## 建议新增项目笔记
仓库实际名为imraywang/rayskills，ray-explainer不仅是提示词：有scaffold、Canvas kit、字幕overlay、Puppeteer/FFmpeg渲染、HyperFrames构建回归测试、QA工具；不必用Remotion复刻冒充上游运行。

### 增量1：失败传播比“生成了文件”更重要
固定SHA的render.js gate()在106–117行捕获qa_video.py非零退出并打印，不向上抛错；最终进程只由pageErr决定。实测静音fixture：渲染退出0，直接QA退出1；有音轨和音画同长通过，响度-70 LUFS与峰值None失败。应在调用方显式运行qa_video.py并检查退出码；本任务未修改上游。

### 增量2：时间轴存在不同证据等级
手工绝对时间、按字数回退的短语估时、Whisper逐字chars不可混称。本例12秒3幕timeline由worker手写，没有调用TTS或Whisper。上游HyperFrames锚点测试真实验证了重配音模拟+1.3秒时，phrase/line/clip/cap锚点随之重算，但测试timeline也是合成夹具，不是模型或配音实测。

### 增量3：画面切点不一定等于首句开口
review.py from_timeline以sc.lines[0].start作为后续场景切点。本例实际场景在4.0/8.0秒开始，QA默认切点图落4.35/8.35秒；另显式提供scenes.json按实际4.0/8.0重新生成切点检查，未篡改上游。提醒新项目分开“声音段落边界”和“画面切换边界”。

### 增量4：确定性验证要限定环境
两次独立浏览器进程在同一环境渲染t=2.5秒，JPEG SHA256一致；只证明此环境同一输入重复一致，不证明跨系统字体和浏览器逐像素一致。Linux正文使用系统字体fallback，字幕使用仓库字体；未冒称macOS手写字体原貌。

### 增量5：许可与身份不是模板默认值能授权的
仓库CC BY-NC 4.0，huashu子组件MIT，字体单独许可；商业部署须另核。默认Ray复刻音色/头像属于作者配置，不能当作用户身份授权。这里只做不带人物、不带克隆音色的离线静音fixture，不索要密钥、不运行API自检，不发布。

## 状态
真实完成：原帖与引用、源码学习、上游scaffold、上游sheet/stills/video、离线回归测试、同环境重复帧检查、ffprobe与失败QA证据、指南与打印PDF。
待验证：完整1.5–3分钟解说片、Claude/Opus导演、TTS/Whisper、数字人/复刻音色、增长宣称、观众效果。
未通过：本例静音fixture按设计未过原版音频QA，不伪装完整成片。待验证：Opus/付费API、真实TTS/Whisper/人物流程均未尝试；无平台额度阻断。

## 交付证据
12问逐问回答与SVG、4种用途、6步主实验；12页A4 PDF全部转PNG并Read自检。exercise.zip已解包另跑37项检查、scaffold/初始化器及t=2.5秒静帧；使用本批既有Node依赖和字体，未声称新机器联网安装已测。发现并隔离旧误标原帖文件，精确ID复读取回正确帖子。
