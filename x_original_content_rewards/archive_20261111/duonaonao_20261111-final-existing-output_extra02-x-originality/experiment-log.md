# 真实实验日志

2026-11-11 Asia/Shanghai。所有稿件和语料均为自写合成夹具；脚本不访问X、不搜索全网、不判定法律，也不发帖。即便no_rule_hit仍需人工审查；许可充分不保证符合原创奖励政策。官方帮助页访问403，截图只证明作者当时展示的文字，不证明当天全部项目规则；未代用户申请或购买。


## 1. 初始化固定夹具
目的：生成10条合成稿件与4条合成语料；不读取真实账号。
```bash
cd /workspace/jingjing-duonaonao-batch2-20261111/extra02-x-originality
python3 exercise/lab.py init
```
实际exit0，stdout/stderr原文：
```text
created 10 synthetic drafts + 4 synthetic sources; no real account data
```
验证：检查out/fixtures.json含正反例及已知边界。

## 2. 离线扫描
目的：用显式引用、权利和0.85词面阈值分流，不联网。
```bash
cd /workspace/jingjing-duonaonao-batch2-20261111/extra02-x-originality
python3 exercise/lab.py scan
```
实际exit0，stdout/stderr原文：
```text
drafts= 10 review= 7 no_rule_hit= 3
No-rule-hit != original / legal / approved; nothing published
```
验证：真实输出7条review、3条no_rule_hit；后者不是可发许可。

## 3. 边界与回归断言
目的：验证10个预注册夹具，包括全角文本、语义漏检、常见短语误报。
```bash
cd /workspace/jingjing-duonaonao-batch2-20261111/extra02-x-originality
python3 exercise/lab.py test
```
实际exit0，stdout/stderr原文：
```text
10/10 fixture assertions passed; explicitly reproduced 1 semantic miss + 1 common-phrase false alarm
Rules catch ledger gaps, not plagiarism in general; no external search coverage
```
验证：10/10断言通过，同时公开已知漏检和误报各1例。

## 4. 生成人工队列
目的：将全部10条保留供人工复核而非自动放行。
```bash
cd /workspace/jingjing-duonaonao-batch2-20261111/extra02-x-originality
python3 exercise/lab.py report
```
实际exit0，stdout/stderr原文：
```text
wrote out/review-queue.md; 10 drafts queued for human review; posting calls=0
```
验证：out/review-queue.md共10条；posting calls=0。

## 5. 哈希与无放行标记验收
目的：固定生成物指纹，保证未声明法律/平台通过。
```bash
cd /workspace/jingjing-duonaonao-batch2-20261111/extra02-x-originality
python3 exercise/lab.py audit
```
实际exit0，stdout/stderr原文：
```text
sha256 manifest entries= 3
legal_clearance=false and platform_approval=false for all 10 drafts; network calls=0
```
验证：3个文件哈希写入manifest，10条两个approval字段均false。

官方帮助页访问记录见evidence/access-record.md。原帖截图Original Content Rewards不能以2025 Creator Revenue Sharing替代；2026年Original条款已curl实读。人工自检，不是独立审核。