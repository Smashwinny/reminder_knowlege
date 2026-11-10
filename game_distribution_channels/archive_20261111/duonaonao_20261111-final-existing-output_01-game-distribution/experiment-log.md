# 实验日志（真实执行）

环境：Linux-6.12.113+-x86_64-with-glibc2.41；Python 3.13.5。所有时间Asia/Shanghai。

实验使用官方公开规则的人工结构化数据，以及3个合成画像；不是用户实际项目、帐号或收入。只在box独立目录运行，执行阶段无网络、无注册/支付/提审。来源获取独立于实验命令。

初始抓取总览时，未对中文URL编码，出现UnicodeEncodeError；修正公开URL编码后成功，见source快照。它是数据获取错误，非实验通过项。

## 冻结结构化输入

- 目的：把公开规则写成有来源ID的数据，并显式区分合成画像与用户数据。
- 完整命令：
```bash
cd /workspace/learn-batch/01-game-distribution
python3 exercise/lab.py init
```
- 执行：2026-11-11T01:02:30.167901+08:00（Asia/Shanghai），exit=0
- stdout（原样）：
```text
init: 7渠道记录，3个合成画像；官方费用+人工结构化，画像不是用户数据
```
- stderr：空
- 验证：检查exercise/data/channels.json恰有7条；profiles.json恰有A/B/C三条，Poki/微信费用为null。

## 验证来源与未知

- 目的：拒绝负费用、重复ID或不存在的来源ID，避免无来源填表。
- 完整命令：
```bash
cd /workspace/learn-batch/01-game-distribution
python3 exercise/lab.py validate
```
- 执行：2026-11-11T01:02:30.207507+08:00（Asia/Shanghai），exit=0
- stdout（原样）：
```text
{"channels": 7, "source_ids_used": 13, "unknown_fee_channels": ["poki", "wechat"]}
```
- stderr：空
- 验证：validation.json中channels=7、source_ids_used=13，unknown_fee_channels=[poki,wechat]。这是ID完整性检查，不证明原页当前未变。

## 进行硬门初筛

- 目的：对三画像逐渠道匹配构建、模式、预算、独占；unknown不按0或通过处理。
- 完整命令：
```bash
cd /workspace/learn-batch/01-game-distribution
python3 exercise/lab.py shortlist
```
- 执行：2026-11-11T01:02:30.237824+08:00（Asia/Shanghai），exit=0
- stdout（原样）：
```text
A: {"候选": ["itch-html5"], "待核": [], "排除": ["apple", "play", "steam", "itch-download", "poki", "wechat"]}
B: {"候选": ["steam", "itch-download"], "待核": [], "排除": ["apple", "play", "itch-html5", "poki", "wechat"]}
C: {"候选": [], "待核": ["wechat"], "排除": ["apple", "play", "steam", "itch-download", "itch-html5", "poki"]}
```
- stderr：空
- 验证：shortlist.json与CSV应有21条：A仅itch-html5候选，B有steam/itch-download候选，C微信待核；所有结果保留未验证列表。

## 统一周期与app数

- 目的：分别算1年1款、3年2款准入费用；不把未发生的Steam回收提前扣除。
- 完整命令：
```bash
cd /workspace/learn-batch/01-game-distribution
python3 exercise/lab.py costs
```
- 执行：2026-11-11T01:02:30.274575+08:00（Asia/Shanghai），exit=0
- stdout（原样）：
```text
{"apple": {"1年1款": 99, "3年2款": 297}, "play": {"1年1款": 25, "3年2款": 25}, "steam": {"1年1款": 100, "3年2款": 200}, "itch-download": {"1年1款": 0, "3年2款": 0}, "itch-html5": {"1年1款": 0, "3年2款": 0}, "poki": {"1年1款": null, "3年2款": null}, "wechat": {"1年1款": null, "3年2款": null}}
仅准入费；Steam回收未抵扣；税费/制作/抽成/退款/支付费未计入
```
- stderr：空
- 验证：costs.json应显示Apple297、Play25、Steam200（3年2款）；Poki/微信仍null。对照官方收费单位手算核对。

## 正反例验收

- 目的：用边界和冲突验证本模型：未知、独占、预算、变现模式、伪来源都不可被美化。
- 完整命令：
```bash
cd /workspace/learn-batch/01-game-distribution
python3 exercise/lab.py test
```
- 执行：2026-11-11T01:02:30.304279+08:00（Asia/Shanghai），exit=0
- stdout（原样）：
```text
PASS 14/14 自编模型断言；非平台接入验收
```
- stderr：空
- 验证：tests.json应列14条。实际结果14/14；它是作者自编局部规则断言，不是独立审核或真实平台SDK验收。

## 保存可追溯输出

- 目的：为输入与结果生成SHA256指纹；日志、代码和来源交给协调者复核。
- 完整命令：
```bash
cd /workspace/learn-batch/01-game-distribution
python3 exercise/lab.py audit
```
- 执行：2026-11-11T01:02:30.345103+08:00（Asia/Shanghai），exit=0
- stdout（原样）：
```text
audit: 8个文件指纹；无网络调用，无发布，无账号操作
```
- stderr：空
- 验证：results/manifest.json列8个文件指纹；重算sha256比对。本步骤不发网、不发布、不改任何平台状态。

## 真实完成与未验证

六命令exit0；7渠道×3合成画像=21评估，14自编断言通过。来源ID有效性是结构验证，不保证内容正确；费用归一只算准入费；不是真实平台SDK测试或独立审核。

待验证：用户主体/所在地、国内出版与备案路径、广告流量主、硬件真机、SDK、合同独占范围、平台接纳、付款、税务与结算。未使用用户密钥、未改变安全设置、未上传私密记录、未发布任何内容。PDF打印/逐页查看另见verification/pdf-review.md。

## 本批PDF补全
WeasyPrint实际打印成功；pdftoppm全部15页转图并逐页目视自检，见pdf-review-batch2.md。未重跑旧实验。

实际PDF补全命令exit0：
```bash
/workspace/jingjing-duonaonao-batch2-20261111/.render-venv/bin/weasyprint /workspace/jingjing-duonaonao-batch2-20261111/01-game-distribution/game-distribution-guide.html /workspace/jingjing-duonaonao-batch2-20261111/01-game-distribution/guide.pdf
pdftoppm -scale-to 900 -png /workspace/jingjing-duonaonao-batch2-20261111/01-game-distribution/guide.pdf /workspace/jingjing-duonaonao-batch2-20261111/01-game-distribution/verification/page
```
