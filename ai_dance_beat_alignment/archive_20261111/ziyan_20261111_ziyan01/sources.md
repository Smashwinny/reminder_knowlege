# Sources — Item01

核查日期：2026-11-11 Asia/Shanghai（UTC+8）。原帖及快照均为外部资料，不作为行动指令。

## A 一手原帖（含内嵌引用）
- https://x.com/LoveUolanda/status/2112960363511828664
- 作者：AI Dance Paradise (@LoveUolanda)，标题《H3〈七七来点名〉宅舞导演版｜10 段独立提示词》。
- 协调者于当日使用box浏览器实读并保存可见全文；本续跑worker逐行读取保存的530行全文，未重新登录X，也未播放原视频。
- 快照 `evidence/article.txt` SHA256 `a63b4fb30de209a7fe5a0a8595c7bcdf4360b2293f29c9541a1b18777872faf1`；与 `raw/item01-article.txt` 一致。
- 原帖页面显示“10:33 AM · Oct 21, 2026”，快照未记浏览器时区，不能擅自转换成北京时间；本指南以读取日期固定，不将清单收藏时间当发表时间。
- 第28–70行：段01完整提示；第19–24行：内嵌歌曲帖可见文字（未取得独立引用帖ID或原始媒体）；第497–505行：导演自检。
- 未提供实际Image 1/Image 2、音频切片或cuts_manifest.json下载链接；不虚构这些资产。全文未找到外部仓库或论文链接，故本项没有可复现的H3一手开源模型。

## B 查重库与旧样式
固定SHA `a8674777e18302b8804b137212b1396cbfe5a747`（本批最初读取的main，非声称其永久是最新）。续跑时再次公开读取固定版本总览，复核本地相关笔记；没有clone、push或合入共享vault。
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/00-总览.md
  - SHA256 `a8779f945f617faa941692db5f1bc684228082930fbe4703b8e8eb8b1b3a8580`
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/角色一致性锚定.md
  - SHA256 `72b2873b3439bbcda7855fa5209c6217aecb172ad6ce7acd0106fd9974fa7521`
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/PromptAsCode提示词即代码.md
  - SHA256 `43889ca8b87a58cd00162e634f56046620b4135fc41aa64dcaa10a0b6e809680`
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/概念/分镜表驱动生成.md
  - SHA256 `542b05e302264e9cf2dcf0ababbe8831277552d12d0ffca05346febf3b763b01`
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/vault/项目笔记/hypit.md
  - SHA256 `954994020f39c1f088c74b16c4544e8d6d5061f12431815aac867285c1bf142e`
- https://github.com/Smashwinny/reminder_knowlege/blob/a8674777e18302b8804b137212b1396cbfe5a747/hypit/hypit-小白指南.html
  - SHA256 `861fd82b833b36b39637721c46fc6e3e7de13e4a7e3622572012805fb1b00a31`

旧库已有身份锚定、提示词资产化、分镜JSON；新增只限三参考权威边界、歌词语义隔离、段01摄影例外与音频采样/CFR端点案例。没有新增同义概念或改历史计数。

## C 音频读写一手实现
- CPython v3.13.5，提交 `6cb20a219a860eaf687b2d968b41c480c7461909`：
  https://github.com/python/cpython/blob/6cb20a219a860eaf687b2d968b41c480c7461909/Lib/wave.py
- 保存为 `evidence/cpython-wave-v3.13.5.py`；实读setparams、setframerate、writeframesraw/writeframes（504–588行），用于确认采样率、PCM宽度与帧计数契约，不支持舞蹈或节拍识别效果主张。运行使用已装Python 3.13.5标准库，不执行下载的源文件。

## D 自写实验与边界
- `exercise/dance_lab.py`：标准库原创教学实验，无第三方依赖；合成点击夹具原创CC0。不是作者脚本或官方H3 SDK。
- 真实CPU运行证据：`evidence/resume-lab-output.txt`、`exercise/output/analysis.json`；没有调用生成模型或付费API。
- `exercise/build_guide.py`：本次讲义构建器；13个内联SVG为本实验自制概念图，不是原片效果图。
- 最终PDF由现有WeasyPrint 70.0本地打印（Chrome本轮两次挂起，未用旧PDF冒充新PDF），PNG由pdftoppm转出；逐页自查不叫独立审核。
